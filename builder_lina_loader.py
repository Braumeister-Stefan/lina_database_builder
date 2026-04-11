"""
builder_lina_loader.py – Component 1: data loading.

Responsibilities:
  - Create the local data directory if it does not exist.
  - Build the sign catalog (341 Unicode Linear A signs).
  - Load the embedded tablet corpus and convert each record to the
    canonical DataFrame format.
  - Assign a *source_strategy* and *qcs* (Quality Confidence Score) to
    every tablet so downstream components can filter by quality.
  - Future: replace / supplement the embedded corpus with a live web scraper.

Output DataFrame schema (one row per tablet)
--------------------------------------------
  tablet_id             str        e.g. 'HT 1'
  site                  str        e.g. 'Hagia Triada'
  date_est              Int64      approximate BCE year (negative), nullable
  material              str        'clay' | 'stone' | …
  source_strategy       str        key from builder_qcs_registry
  qcs                   float      Quality Confidence Score [0, 1]
  transliteration       str        original scholarly transliteration string
  sign_groups           str        pipe-separated sign group tokens
                                   e.g. 'A-DU|GRA|KU-RO|GRA'
  sign_sequence_unicode str        Unicode Linear A string, groups space-separated
  sign_sequence_ids     str        comma-separated sign IDs (cp − 0x10600)
  sign_group_count      int        number of sign groups (words)
  sign_count            int        total individual Linear A signs (excl. '?')
"""

import os

import pandas as pd

from lina_sign_catalog import (
    build_sign_catalog,
    build_label_to_char_map,
    build_char_to_id_map,
    parse_sign_groups,
    sign_group_to_unicode,
)
from lina_corpus_embedded import CORPUS
from builder_qcs_registry import get_strategy


# ---------------------------------------------------------------------------
# Public entry-point called by model.py
# ---------------------------------------------------------------------------

def load_data(data_dir: str) -> pd.DataFrame:
    """Ensure *data_dir* exists, build the corpus DataFrame, and return it."""
    _ensure_directory(data_dir)
    df = _build_dataframe()
    print(f"[loader] loaded {len(df)} record(s).")
    return df


# ---------------------------------------------------------------------------
# Helper: directory setup
# ---------------------------------------------------------------------------

def _ensure_directory(path: str) -> None:
    """Create *path* (and any parent directories) if it does not exist."""
    if not os.path.exists(path):
        os.makedirs(path, exist_ok=True)
        print(f"[loader] created data directory: {path}")
    else:
        print(f"[loader] data directory exists: {path}")


# ---------------------------------------------------------------------------
# Helper: build the full DataFrame from the embedded corpus
# ---------------------------------------------------------------------------

def _build_dataframe() -> pd.DataFrame:
    """Convert the embedded CORPUS list into the canonical DataFrame.

    Each tablet is tagged with the ``source_strategy`` that produced it
    and inherits that strategy's QCS so downstream filters can select by
    quality.
    """
    catalog    = build_sign_catalog()
    label_map  = build_label_to_char_map(catalog)
    char_to_id = build_char_to_id_map(catalog)

    print(f"[loader] sign catalog: {len(catalog)} signs (Unicode Linear A block).")

    # Look up the corpus strategy once – every embedded tablet inherits it.
    gorila_strategy = get_strategy("gorila_transliterations")

    rows = []
    for tablet in CORPUS:
        raw    = tablet["transliteration"]
        groups = parse_sign_groups(raw)

        # Pipe-separated list of sign group strings (human-readable)
        sign_groups_str = "|".join(groups)

        # Unicode Linear A string – sign groups separated by a space
        uni_parts = [sign_group_to_unicode(g, label_map) for g in groups]
        sign_unicode = " ".join(uni_parts)

        # Collect recognised Unicode characters (exclude '?' placeholders)
        recognised_chars = [
            ch for part in uni_parts for ch in part if ch != '?'
        ]

        # Flat comma-separated sign-ID list
        sign_ids_str = ",".join(
            str(char_to_id[ch]) for ch in recognised_chars if ch in char_to_id
        )

        sign_count = len(recognised_chars)

        # Tablets inherit the QCS of their source strategy
        rows.append({
            "tablet_id":             tablet["tablet_id"],
            "site":                  tablet["site"],
            "date_est":              tablet.get("date_est"),
            "material":              tablet.get("material", "clay"),
            "source_strategy":       gorila_strategy["key"],
            "qcs":                   gorila_strategy["qcs"],
            "transliteration":       raw,
            "sign_groups":           sign_groups_str,
            "sign_sequence_unicode": sign_unicode,
            "sign_sequence_ids":     sign_ids_str,
            "sign_group_count":      len(groups),
            "sign_count":            sign_count,
        })

    df = pd.DataFrame(rows)
    df["date_est"] = df["date_est"].astype("Int64")
    return df
