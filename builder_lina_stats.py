"""
builder_lina_stats.py – Component 3: summary statistics & visualisation.

Responsibilities:
  - Compute and report descriptive statistics on the cleaned dataset.
  - Produce visualisations (placeholder – saves figures to disk when data
    is available; skips gracefully on an empty dataset).
"""

import os
import pandas as pd


# Directory where figures are written (relative to this file).
FIGURES_DIR = os.path.join(os.path.dirname(__file__), "data", "figures")


def report_stats(df: pd.DataFrame) -> None:
    """Print summary statistics and generate visualisations for *df*."""
    print("\n[stats] --- summary statistics ---")
    _print_stats(df)
    _generate_plots(df)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _print_stats(df: pd.DataFrame) -> None:
    """Print descriptive statistics to stdout."""
    if df.empty:
        print("[stats] dataset is empty – no statistics to report.")
        return

    total_tablets = len(df)
    dated = df["date"].notna().sum() if "date" in df.columns else 0
    word_cols = [c for c in df.columns if c != "date"]

    print(f"  total tablets : {total_tablets}")
    print(f"  dated tablets : {dated}")
    print(f"  word columns  : {len(word_cols)}")

    if "date" in df.columns and df["date"].notna().any():
        print(f"  date range    : {int(df['date'].min())} – {int(df['date'].max())}")

    if word_cols:
        # Number of non-null words per tablet row
        word_counts = df[word_cols].notna().sum(axis=1)
        print(f"  words/tablet  : min={word_counts.min()}, "
              f"max={word_counts.max()}, "
              f"mean={word_counts.mean():.1f}")


def _generate_plots(df: pd.DataFrame) -> None:
    """
    Placeholder visualisation.

    Future development: produce histograms, word-frequency charts, timeline
    plots, etc. using matplotlib / seaborn and save them to FIGURES_DIR.
    """
    if df.empty:
        print("[stats] dataset is empty – skipping visualisation.")
        return

    # Ensure figures directory exists before attempting to write.
    os.makedirs(FIGURES_DIR, exist_ok=True)
    print(f"[stats] visualisation placeholder – figures would be saved to "
          f"'{FIGURES_DIR}'.")
