"""
builder_lina_loader.py – Component 1: data loading.

Responsibilities:
  - Create the local data directory if it does not exist.
  - Build the sign catalog (341 Unicode Linear A signs).
  - Load the embedded tablet corpus and convert each record to the
    canonical DataFrame format.
  - Future: replace / supplement the embedded corpus with a live web scraper.

Output DataFrame schema (one row per tablet)
--------------------------------------------
  tablet_id             str        e.g. 'HT 1'
  site                  str        e.g. 'Hagia Triada'
  date_est              Int64      approximate BCE year (negative), nullable
  material              str        'clay' | 'stone' | …
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
    """Convert the embedded CORPUS list into the canonical DataFrame."""
    catalog    = build_sign_catalog()
    label_map  = build_label_to_char_map(catalog)
    char_to_id = build_char_to_id_map(catalog)

    print(f"[loader] sign catalog: {len(catalog)} signs (Unicode Linear A block).")

    rows = []
    for tablet in CORPUS:
        raw    = tablet["transliteration"]
        groups = parse_sign_groups(raw)

        # Pipe-separated list of sign group strings (human-readable)
        sign_groups_str = "|".join(groups)

        # Unicode Linear A string – sign groups separated by a space
        uni_parts = [sign_group_to_unicode(g, label_map) for g in groups]
        sign_unicode = " ".join(uni_parts)

        # Flat comma-separated sign-ID list (omits '?' placeholders)
        ids = []
        for part in uni_parts:
            for ch in part:
                if ch != '?':
                    sid = char_to_id.get(ch)
                    if sid is not None:
                        ids.append(str(sid))
        sign_ids_str = ",".join(ids)

        # Count recognised signs (characters that are not '?')
        sign_count = sum(
            1 for part in uni_parts for ch in part if ch != '?'
        )

        rows.append({
            "tablet_id":             tablet["tablet_id"],
            "site":                  tablet["site"],
            "date_est":              tablet.get("date_est"),
            "material":              tablet.get("material", "clay"),
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
