"""
builder_lina_validator.py – Component 2b: data validation.

Responsibilities:
  - Validate the corpus DataFrame against the canonical schema.
  - Detect duplicate tablet identifiers.
  - Check QCS and source-strategy consistency with the registry.
  - Flag out-of-range dates and missing site coordinates.
  - Verify internal consistency of sign-count fields.
  - Return a structured list of findings so the pipeline can decide
    whether to proceed, warn, or abort.

Each finding is a dict with keys:
    severity  : 'error' | 'warning'
    check     : short machine-readable check name
    message   : human-readable description
    rows      : list of affected row indices (may be empty for global checks)
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional

import pandas as pd

from builder_qcs_registry import DATA_STRATEGIES
from lina_site_coordinates import SITE_COORDINATES

# ---------------------------------------------------------------------------
# Schema definition – expected columns, types, and nullability
# ---------------------------------------------------------------------------

_REQUIRED_COLUMNS: Dict[str, Dict[str, Any]] = {
    "tablet_id":             {"dtype": "string",  "nullable": False},
    "site":                  {"dtype": "string",  "nullable": False},
    "date_est":              {"dtype": "numeric", "nullable": True},
    "date_uncertainty_yrs":  {"dtype": "numeric", "nullable": True},
    "material":              {"dtype": "string",  "nullable": False},
    "source_strategy":       {"dtype": "string",  "nullable": False},
    "qcs":                   {"dtype": "numeric", "nullable": False},
    "is_synthetic":          {"dtype": "bool",    "nullable": False},
    "transliteration":       {"dtype": "string",  "nullable": False},
    "sign_groups":           {"dtype": "string",  "nullable": False},
    "sign_sequence_unicode": {"dtype": "string",  "nullable": False},
    "sign_sequence_ids":     {"dtype": "string",  "nullable": True},
    "sign_group_count":      {"dtype": "numeric", "nullable": False},
    "sign_count":            {"dtype": "numeric", "nullable": False},
}

# Bronze Age date bounds (all values are negative BCE integers)
_DATE_MIN = -3000  # earliest plausible Linear A date
_DATE_MAX = -1050  # latest plausible Linear A date (LM IIIB)

# ---------------------------------------------------------------------------
# Public entry-point
# ---------------------------------------------------------------------------


def validate_dataframe(
    df: pd.DataFrame,
    *,
    label: str = "corpus",
) -> List[Dict[str, Any]]:
    """Run all validation checks on *df* and return a list of findings.

    Parameters
    ----------
    df : pd.DataFrame
        The corpus DataFrame to validate.
    label : str
        Human-readable label used in log messages (e.g. ``'raw'``,
        ``'clean'``).

    Returns
    -------
    list[dict]
        Each element is a finding dict with keys ``severity``, ``check``,
        ``message``, and ``rows``.
    """
    findings: List[Dict[str, Any]] = []

    print(f"\n[validator] ── validating '{label}' ({len(df)} rows) ──")

    if df.empty:
        findings.append(_finding("warning", "empty_dataframe",
                                 "DataFrame is empty – nothing to validate."))
        _print_summary(findings, label)
        return findings

    # Run all checks
    _check_schema(df, findings)
    _check_duplicates(df, findings)
    _check_qcs_range(df, findings)
    _check_source_strategies(df, findings)
    _check_date_range(df, findings)
    _check_site_coordinates(df, findings)
    _check_sign_count_consistency(df, findings)
    _check_blank_critical_fields(df, findings)

    _print_summary(findings, label)
    return findings


# ---------------------------------------------------------------------------
# Individual checks
# ---------------------------------------------------------------------------


def _check_schema(df: pd.DataFrame, findings: List[Dict]) -> None:
    """Verify that all required columns are present."""
    missing = [c for c in _REQUIRED_COLUMNS if c not in df.columns]
    if missing:
        findings.append(_finding(
            "error", "missing_columns",
            f"Missing required column(s): {', '.join(missing)}",
        ))


def _check_duplicates(df: pd.DataFrame, findings: List[Dict]) -> None:
    """Flag duplicate tablet_id values."""
    if "tablet_id" not in df.columns:
        return
    dup_mask = df.duplicated(subset=["tablet_id"], keep=False)
    if dup_mask.any():
        dup_ids = df.loc[dup_mask, "tablet_id"].unique().tolist()
        findings.append(_finding(
            "warning", "duplicate_tablet_id",
            f"{len(dup_ids)} duplicate tablet_id(s) detected: "
            f"{', '.join(str(d) for d in dup_ids[:10])}"
            + (" …" if len(dup_ids) > 10 else ""),
            rows=df.index[dup_mask].tolist(),
        ))


def _check_qcs_range(df: pd.DataFrame, findings: List[Dict]) -> None:
    """Every QCS value must be in [0, 1]."""
    if "qcs" not in df.columns:
        return
    bad = df[(df["qcs"] < 0) | (df["qcs"] > 1)]
    if not bad.empty:
        findings.append(_finding(
            "error", "qcs_out_of_range",
            f"{len(bad)} row(s) have QCS outside [0, 1].",
            rows=bad.index.tolist(),
        ))


def _check_source_strategies(df: pd.DataFrame, findings: List[Dict]) -> None:
    """Every source_strategy value must exist in the QCS registry."""
    if "source_strategy" not in df.columns:
        return
    known_keys = {s["key"] for s in DATA_STRATEGIES}
    unknown = set(df["source_strategy"].unique()) - known_keys
    if unknown:
        findings.append(_finding(
            "error", "unknown_source_strategy",
            f"Unknown source_strategy key(s): {', '.join(sorted(unknown))}",
        ))


def _check_date_range(df: pd.DataFrame, findings: List[Dict]) -> None:
    """Non-null dates must fall within plausible Bronze Age bounds."""
    if "date_est" not in df.columns:
        return
    dates = df["date_est"].dropna()
    if dates.empty:
        return
    out_of_range = dates[(dates < _DATE_MIN) | (dates > _DATE_MAX)]
    if not out_of_range.empty:
        findings.append(_finding(
            "warning", "date_out_of_range",
            f"{len(out_of_range)} row(s) have date_est outside "
            f"[{_DATE_MIN}, {_DATE_MAX}].",
            rows=out_of_range.index.tolist(),
        ))


def _check_site_coordinates(df: pd.DataFrame, findings: List[Dict]) -> None:
    """Warn when a site in the corpus has no entry in SITE_COORDINATES."""
    if "site" not in df.columns:
        return
    corpus_sites = set(df["site"].dropna().unique())
    known_sites = set(SITE_COORDINATES.keys())
    unmapped = corpus_sites - known_sites
    if unmapped:
        counts = (
            df[df["site"].isin(unmapped)]
            .groupby("site")
            .size()
            .sort_values(ascending=False)
        )
        detail = ", ".join(
            f"{site} ({n})" for site, n in counts.items()
        )
        findings.append(_finding(
            "warning", "unmapped_sites",
            f"{len(unmapped)} site(s) lack geographic coordinates: {detail}",
        ))


def _check_sign_count_consistency(
    df: pd.DataFrame, findings: List[Dict]
) -> None:
    """sign_group_count must match the pipe-delimited sign_groups field."""
    if "sign_groups" not in df.columns or "sign_group_count" not in df.columns:
        return

    mismatches: List[int] = []
    for idx, row in df.iterrows():
        groups_str = row["sign_groups"]
        expected = len(groups_str.split("|")) if groups_str else 0
        if row["sign_group_count"] != expected:
            mismatches.append(idx)

    if mismatches:
        findings.append(_finding(
            "warning", "sign_group_count_mismatch",
            f"{len(mismatches)} row(s) have sign_group_count that "
            f"doesn't match the pipe-delimited sign_groups field.",
            rows=mismatches[:20],
        ))


def _check_blank_critical_fields(
    df: pd.DataFrame, findings: List[Dict]
) -> None:
    """Critical string columns must not be empty or whitespace-only."""
    critical = ["tablet_id", "site", "transliteration"]
    for col in critical:
        if col not in df.columns:
            continue
        blank_mask = df[col].astype(str).str.strip().eq("")
        if blank_mask.any():
            findings.append(_finding(
                "error", f"blank_{col}",
                f"{blank_mask.sum()} row(s) have blank or empty '{col}'.",
                rows=df.index[blank_mask].tolist(),
            ))


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _finding(
    severity: str,
    check: str,
    message: str,
    rows: Optional[List[int]] = None,
) -> Dict[str, Any]:
    """Create a standardised finding dict."""
    return {
        "severity": severity,
        "check": check,
        "message": message,
        "rows": rows or [],
    }


def _print_summary(
    findings: List[Dict[str, Any]], label: str
) -> None:
    """Print a compact summary of findings to stdout."""
    errors = [f for f in findings if f["severity"] == "error"]
    warnings = [f for f in findings if f["severity"] == "warning"]
    print(f"[validator] '{label}' result: "
          f"{len(errors)} error(s), {len(warnings)} warning(s)")
    for f in findings:
        icon = "✗" if f["severity"] == "error" else "⚠"
        row_info = f" (rows: {len(f['rows'])})" if f["rows"] else ""
        print(f"  {icon} [{f['check']}] {f['message']}{row_info}")
    if not findings:
        print("  ✓ all checks passed")
