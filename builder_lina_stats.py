"""
builder_lina_stats.py – Component 3: summary statistics & visualisation.

Responsibilities:
  - Print the sign-catalog overview (size, category breakdown).
  - Compute and print descriptive statistics on the cleaned corpus DataFrame.
  - Produce visualisations (placeholder – saves figures to disk when data is
    available; skips gracefully on an empty dataset).

Statistics reported
-------------------
  Catalog      : total signs, syllabic vs. logographic vs. numeric breakdown
  Corpus       : tablets, sites, date range, material types
  Sign groups  : total, unique, frequency table (top 20)
  Signs        : total, unique, frequency table (top 20)
  Group length : distribution of signs per group (1-sign, 2-sign, …)
"""

import os
from collections import Counter
from typing import List

import pandas as pd

from lina_sign_catalog import build_sign_catalog

# Directory where figures are written (relative to this file).
FIGURES_DIR = os.path.join(os.path.dirname(__file__), "data", "figures")


# ---------------------------------------------------------------------------
# Public entry-point called by model.py
# ---------------------------------------------------------------------------

def report_stats(df: pd.DataFrame) -> None:
    """Print sign-catalog and corpus statistics, then generate visualisations."""
    print("\n[stats] ════════════════════════════════════════")
    print("[stats] Sign Catalog")
    print("[stats] ════════════════════════════════════════")
    _print_catalog_stats()

    print("\n[stats] ════════════════════════════════════════")
    print("[stats] Corpus Statistics")
    print("[stats] ════════════════════════════════════════")
    _print_corpus_stats(df)

    _generate_plots(df)


# ---------------------------------------------------------------------------
# Catalog statistics
# ---------------------------------------------------------------------------

def _print_catalog_stats() -> None:
    """Print the sign-catalog breakdown by category."""
    catalog = build_sign_catalog()
    total = len(catalog)

    from collections import Counter as _Counter
    cats = _Counter(entry["category"] for entry in catalog)

    print(f"  total signs      : {total}")
    print(f"  Unicode block    : U+10600 – U+1077F")
    for cat, cnt in sorted(cats.items(), key=lambda x: -x[1]):
        print(f"  {cat:20s} : {cnt:4d} signs  ({100*cnt/total:.0f}%)")


# ---------------------------------------------------------------------------
# Corpus statistics
# ---------------------------------------------------------------------------

def _print_corpus_stats(df: pd.DataFrame) -> None:
    """Print descriptive statistics for the tablet corpus."""
    if df.empty:
        print("[stats] dataset is empty – no statistics to report.")
        return

    total   = len(df)
    dated   = int(df["date_est"].notna().sum())

    # ── Corpus overview ──────────────────────────────────────────────────
    print(f"\n  ── Corpus overview ──────────────────────────────")
    print(f"  total tablets    : {total}")
    print(f"  dated tablets    : {dated}  ({100*dated/total:.0f}%)")
    if df["date_est"].notna().any():
        lo = int(df["date_est"].min())
        hi = int(df["date_est"].max())
        print(f"  date range (BCE) : {abs(hi)} – {abs(lo)}")

    # ── Sites ─────────────────────────────────────────────────────────────
    print(f"\n  ── Tablets per site ─────────────────────────────")
    for site, cnt in df["site"].value_counts().items():
        print(f"  {site:25s}: {cnt:3d}")

    # ── Materials ─────────────────────────────────────────────────────────
    print(f"\n  ── Tablets by material ──────────────────────────")
    for mat, cnt in df["material"].value_counts().items():
        print(f"  {mat:20s}: {cnt:3d}")

    # ── Sign group statistics ─────────────────────────────────────────────
    all_groups: List[str] = []
    for groups_str in df["sign_groups"].dropna():
        all_groups.extend(groups_str.split("|"))

    n_groups  = len(all_groups)
    n_unique  = len(set(all_groups))
    sgc       = df["sign_group_count"]

    print(f"\n  ── Sign group statistics ────────────────────────")
    print(f"  total sign groups in corpus : {n_groups}")
    print(f"  unique sign groups          : {n_unique}")
    print(f"  avg sign groups per tablet  : {n_groups / total:.1f}")
    print(f"  sign groups per tablet      : "
          f"min={int(sgc.min())}  max={int(sgc.max())}  "
          f"mean={sgc.mean():.1f}  median={sgc.median():.1f}")

    # ── Individual sign statistics ────────────────────────────────────────
    total_signs  = int(df["sign_count"].sum())
    avg_signs    = df["sign_count"].mean()
    sc           = df["sign_count"]

    print(f"\n  ── Individual sign statistics ───────────────────")
    print(f"  total signs in corpus       : {total_signs}")
    print(f"  avg signs per tablet        : {avg_signs:.1f}")
    print(f"  signs per tablet            : "
          f"min={int(sc.min())}  max={int(sc.max())}  "
          f"mean={sc.mean():.1f}  median={sc.median():.1f}")

    # ── Top 20 most frequent sign groups ─────────────────────────────────
    group_freq = Counter(all_groups)
    print(f"\n  ── Top 20 most frequent sign groups ─────────────")
    for group, cnt in group_freq.most_common(20):
        pct = 100 * cnt / n_groups
        print(f"  {group:30s}: {cnt:4d}  ({pct:.1f}%)")

    # ── Top 20 most frequent individual signs ─────────────────────────────
    all_signs: List[str] = []
    for groups_str in df["sign_groups"].dropna():
        for group in groups_str.split("|"):
            all_signs.extend(group.split("-"))

    sign_freq  = Counter(all_signs)
    n_signs    = len(all_signs)
    n_u_signs  = len(sign_freq)

    print(f"\n  ── Top 20 most frequent individual signs ─────────")
    print(f"  (unique syllabic/logographic tokens: {n_u_signs})")
    for sign, cnt in sign_freq.most_common(20):
        pct = 100 * cnt / n_signs
        print(f"  {sign:20s}: {cnt:4d}  ({pct:.1f}%)")

    # ── Sign group length distribution ───────────────────────────────────
    lengths     = [len(g.split("-")) for g in all_groups]
    length_dist = Counter(lengths)
    print(f"\n  ── Sign group length distribution ───────────────")
    for length in sorted(length_dist):
        cnt = length_dist[length]
        bar = "█" * min(cnt, 40)
        print(f"  {length:2d} sign(s) per group: {cnt:4d}  {bar}")


# ---------------------------------------------------------------------------
# Visualisation placeholder
# ---------------------------------------------------------------------------

def _generate_plots(df: pd.DataFrame) -> None:
    """
    Placeholder for matplotlib / seaborn visualisation.

    Future development: produce bar charts, timeline plots, frequency
    heat-maps, and sign-usage distributions, saving figures to FIGURES_DIR.
    """
    if df.empty:
        print("[stats] dataset is empty – skipping visualisation.")
        return

    os.makedirs(FIGURES_DIR, exist_ok=True)
    print(f"\n[stats] visualisation placeholder – figures would be saved to "
          f"'{FIGURES_DIR}'.")
