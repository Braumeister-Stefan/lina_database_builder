"""
builder_lina_loader.py – Component 1: data loading.

Responsibilities:
  - Create the local data directory if it does not exist.
  - Call the scraper placeholder (lina_scraper) to populate raw data.
  - Return a DataFrame in the canonical output format:
      * Row  = one Linear-A list (one archaeological tablet finding).
      * Col 0 = 'date' (YYYY as nullable integer, or empty).
      * Col 1+ = words found on the tablet (word_1, word_2, …).
"""

import os
import pandas as pd


# ---------------------------------------------------------------------------
# Public entry-point called by model.py
# ---------------------------------------------------------------------------

def load_data(data_dir: str) -> pd.DataFrame:
    """
    Ensure *data_dir* exists, attempt to scrape / load data, and return
    a DataFrame in the canonical format.
    """
    _ensure_directory(data_dir)
    df = _lina_scraper(data_dir)
    print(f"[loader] loaded {len(df)} record(s) from '{data_dir}'.")
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
        print(f"[loader] data directory already exists: {path}")


# ---------------------------------------------------------------------------
# Helper: web scraper – placeholder
# ---------------------------------------------------------------------------

def _lina_scraper(data_dir: str) -> pd.DataFrame:
    """
    Placeholder scraper.

    Future development: retrieve Linear-A tablet data from web-based sources
    (e.g. DĀMOS, the Mycenaean Atlas, or dedicated Linear-A corpora) and
    return a populated DataFrame.

    For now this returns an empty DataFrame that matches the output schema:
      date (Int64 nullable), word_1 (str), word_2 (str), …
    """
    print("[scraper] placeholder – returning empty dataset.")
    df = pd.DataFrame(columns=["date"])
    # Ensure 'date' uses a nullable integer type so it can hold NaN values.
    df["date"] = df["date"].astype("Int64")
    return df
