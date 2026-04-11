"""
builder_lina_cleaner.py – Component 2: basic cleaning.

Responsibilities:
  - Print first-round summary statistics on the raw DataFrame.
  - Apply cleaning steps (placeholder for now).
  - Return the cleaned DataFrame.
"""

import pandas as pd


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Print basic summary statistics, apply cleaning steps, and return the
    cleaned DataFrame.
    """
    print("\n[cleaner] --- raw data summary ---")
    _print_summary(df)

    df = _apply_cleaning(df)

    print("[cleaner] --- cleaned data summary ---")
    _print_summary(df)

    return df


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _print_summary(df: pd.DataFrame) -> None:
    """Print basic summary statistics to stdout."""
    print(f"  shape         : {df.shape[0]} rows × {df.shape[1]} columns")
    print(f"  columns       : {list(df.columns)}")
    if not df.empty:
        missing = df.isnull().sum().sum()
        print(f"  missing values: {missing}")
        print(df.describe(include="all").to_string())
    else:
        print("  (dataset is empty)")


def _apply_cleaning(df: pd.DataFrame) -> pd.DataFrame:
    """
    Placeholder for cleaning logic.

    Future development:
      - Remove duplicate tablet records.
      - Standardise date values.
      - Strip / normalise word tokens.
      - Handle missing / malformed entries.
    """
    print("[cleaner] cleaning placeholder – no changes applied.")
    return df.copy()
