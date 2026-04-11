"""
builder_lina_stats.py – Component 3: summary statistics and visualisations.

Responsibilities
----------------
  - Print catalog and corpus statistics to stdout.
  - Generate and save PNG figures and formatted table images to FIGURES_DIR.
  - Return a list of (tab_name, title, png_path) tuples for xlsx assembly.

Outputs (saved to data/figures/)
---------------------------------
  tbl_01_catalog_overview.png      – sign catalog counts by category
  tbl_02_sign_group_types.png      – sign group type taxonomy from literature
  fig_01_catalog_categories.png    – pie: sign categories
  fig_02_sign_group_frequencies.png – horizontal bar: top-15 sign groups
  tbl_03_corpus_overview.png       – corpus headline stats
  tbl_04_site_breakdown.png        – tablets per find-site with coordinates
  fig_03_site_map.png              – map of Crete showing find-sites
  fig_04_timeline.png              – tablets by estimated date × site
  fig_05_signs_per_tablet.png      – histogram: sign count distribution
"""

import os
import textwrap
from collections import Counter
from typing import Dict, List, Tuple

import matplotlib
matplotlib.use("Agg")                            # non-interactive backend
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection
import numpy as np
import pandas as pd

from lina_sign_catalog import build_sign_catalog
from lina_site_coordinates import (
    CRETE_OUTLINE, GREECE_OUTLINE, TURKEY_W_OUTLINE,
    SITE_COORDINATES, get_site_summary_df,
)

# ---------------------------------------------------------------------------
# Corpus coverage constants (from GORILA + Younger's corpus literature)
# ---------------------------------------------------------------------------
# Total known Linear A inscriptions across all sites, materials and periods.
TOTAL_KNOWN_INSCRIPTIONS = 1400

# Best-estimate count of inscriptions per site from the published literature.
# Sources: GORILA vols I–V; Younger, J.G. Linear A Texts in Transliteration.
KNOWN_SITE_TOTALS: Dict[str, int] = {
    "Hagia Triada": 147,
    "Khania":        83,
    "Zakros":        31,
    "Phaistos":      15,
    "Mallia":        13,
    "Knossos":        8,
    "Tylissos":       7,
    "Arkhanes":       6,
    "Palaikastro":    5,
    "Akrotiri":       7,
    "Gournia":        5,
    "Nirou Khani":    3,
    "Myrtos":         4,
    "Apodioulou":     2,
    # Remainder: scattered minor Cretan sites, non-Cretan Aegean sites,
    # inscribed stone vessels, ceramic objects, sealings and nodules.
    "Other / unassigned": 1064,
}

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
FIGURES_DIR = os.path.join(os.path.dirname(__file__), "data", "figures")

# Consistent style
_FIG_W, _FIG_H = 12, 6
_DPI            = 150
_TITLE_FONTSIZE = 14
_COLORS = {
    "syllabic":         "#4C72B0",
    "logographic":      "#55A868",
    "numeric_fraction": "#C44E52",
    "other":            "#8172B2",
    "clay":             "#DD8452",
    "stone":            "#64B5CD",
    "accounting":       "#C44E52",
    "commodity":        "#55A868",
    "formula":          "#4C72B0",
    "other_group":      "#8172B2",
}


# ---------------------------------------------------------------------------
# Public entry-point
# ---------------------------------------------------------------------------

def report_stats(df: pd.DataFrame) -> List[Tuple[str, str, str]]:
    """Compute statistics, generate all PNGs, return (tab_name, title, path) list."""
    os.makedirs(FIGURES_DIR, exist_ok=True)

    # ── Print catalog stats ──────────────────────────────────────────────
    catalog = build_sign_catalog()
    _print_catalog_stats(catalog)
    _print_corpus_stats(df)

    if df.empty:
        print("[stats] dataset is empty – skipping visualisations.")
        return []

    figures: List[Tuple[str, str, str]] = []

    # ── Sign catalog tables & figures ────────────────────────────────────
    figures.append(_tbl_catalog_overview(catalog))
    figures.append(_tbl_sign_group_types())
    figures.append(_fig_catalog_categories(catalog))
    figures.append(_fig_sign_group_frequencies(df))

    # ── Corpus tables & figures ──────────────────────────────────────────
    figures.append(_tbl_corpus_overview(df))
    figures.append(_tbl_site_breakdown(df))
    figures.append(_fig_site_map(df))
    figures.append(_fig_timeline(df))
    figures.append(_fig_signs_per_tablet(df))
    figures.append(_fig_corpus_coverage(df))

    print(f"\n[stats] {len(figures)} outputs saved to '{FIGURES_DIR}'.")
    return figures


# ---------------------------------------------------------------------------
# Stdout statistics (unchanged from previous version)
# ---------------------------------------------------------------------------

def _print_catalog_stats(catalog: list) -> None:
    total = len(catalog)
    cats  = Counter(e["category"] for e in catalog)
    print("\n[stats] ════════ Sign Catalog ════════")
    print(f"  total signs    : {total}  (Unicode block U+10600–U+1077F)")
    for cat, cnt in sorted(cats.items(), key=lambda x: -x[1]):
        print(f"  {cat:20s}: {cnt:4d}  ({100*cnt/total:.0f}%)")


def _print_corpus_stats(df: pd.DataFrame) -> None:
    if df.empty:
        return
    total  = len(df)
    dated  = int(df["date_est"].notna().sum())
    print("\n[stats] ════════ Corpus Statistics ════════")
    print(f"  tablets: {total}  |  dated: {dated}  |  sites: {df['site'].nunique()}")
    if df["date_est"].notna().any():
        lo, hi = int(df["date_est"].min()), int(df["date_est"].max())
        print(f"  date range (BCE): {abs(hi)} – {abs(lo)}")
    all_groups: List[str] = []
    for s in df["sign_groups"].dropna():
        all_groups.extend(s.split("|"))
    gf = Counter(all_groups)
    print(f"  total sign groups: {len(all_groups)}  |  unique: {len(gf)}")
    print(f"  top group: {gf.most_common(1)[0][0]}  ({gf.most_common(1)[0][1]} occurrences)")


# ---------------------------------------------------------------------------
# Helper: save a matplotlib table as PNG
# ---------------------------------------------------------------------------

def _save_table_png(
        tab_name: str,
        title: str,
        headers: List[str],
        rows: List[list],
        filename: str,
        col_widths: List[float] | None = None,
        fig_h: float = 4.0,
) -> Tuple[str, str, str]:
    """Render a plain table as a PNG and return (tab_name, title, path)."""
    n_cols = len(headers)
    if col_widths is None:
        col_widths = [1.0 / n_cols] * n_cols

    fig, ax = plt.subplots(figsize=(_FIG_W, fig_h))
    ax.axis("off")

    fig.suptitle(title, fontsize=_TITLE_FONTSIZE, fontweight="bold", y=0.97)

    tbl = ax.table(
        cellText=rows,
        colLabels=headers,
        loc="center",
        cellLoc="center",
        colWidths=col_widths,
    )
    tbl.auto_set_font_size(False)
    tbl.set_fontsize(10)
    tbl.scale(1, 1.6)

    # Header row styling
    for col_idx in range(n_cols):
        cell = tbl[0, col_idx]
        cell.set_facecolor("#2C3E50")
        cell.set_text_props(color="white", fontweight="bold")

    # Alternating row colours
    for row_idx in range(1, len(rows) + 1):
        bg = "#F2F2F2" if row_idx % 2 == 0 else "white"
        for col_idx in range(n_cols):
            tbl[row_idx, col_idx].set_facecolor(bg)

    fig.tight_layout()
    path = os.path.join(FIGURES_DIR, filename)
    fig.savefig(path, dpi=_DPI, bbox_inches="tight")
    plt.close(fig)
    print(f"[stats] saved {filename}")
    return (tab_name, title, path)


# ---------------------------------------------------------------------------
# Table 1 – Sign Catalog Overview
# ---------------------------------------------------------------------------

def _tbl_catalog_overview(catalog: list) -> Tuple[str, str, str]:
    cats = Counter(e["category"] for e in catalog)
    total = len(catalog)
    headers = ["Category", "Sign Count", "% of Total", "Description"]
    desc = {
        "syllabic":         "Phonetic syllabograms (AB series) used to spell words",
        "logographic":      "Logograms / ideograms (A series) denoting objects",
        "numeric_fraction": "Fractional / numeric notation signs",
        "other":            "Unclassified or variant signs",
    }
    rows = []
    for cat, cnt in sorted(cats.items(), key=lambda x: -x[1]):
        rows.append([cat.replace("_", " ").title(), cnt, f"{100*cnt/total:.0f}%",
                     desc.get(cat, "")])
    rows.append(["TOTAL", total, "100%", "Unicode block U+10600–U+1077F"])
    return _save_table_png(
        "Sign Catalog", "Linear A – Sign Catalog Overview",
        headers, rows, "tbl_01_catalog_overview.png",
        col_widths=[0.18, 0.12, 0.12, 0.58], fig_h=3.5,
    )


# ---------------------------------------------------------------------------
# Table 2 – Sign Group Types
# ---------------------------------------------------------------------------

def _tbl_sign_group_types() -> Tuple[str, str, str]:
    headers = ["Type", "GORILA Label", "Examples", "Function"]
    rows = [
        ["Syllabic word",   "AB-series",
         "A-SA-SA-RA-ME, I-DA-MA-TE, KU-PA3-NU",
         "Phonetically spelled names or words (many undeciphered)"],
        ["Commodity logogram", "A301–A310",
         "GRA (grain), VIN (wine), OLE (oil), OVS (sheep), BOS (cattle)",
         "Single-sign ideogram denoting a commodity being counted"],
        ["Accounting term",  "AB-series multi-sign",
         "KU-RO (grand total), KI-RO (deficit / carried forward)",
         "Administrative bookkeeping totals and balance terms"],
        ["Libation formula", "Mixed AB-series",
         "A-SA-SA-RA-ME, A-TA-I-*301-WA-JA, A-RE-NE-SI",
         "Recurring dedicatory/ritual formulas on stone vessels"],
        ["Numeric / fraction", "A700-series",
         "Fractional signs following commodity logograms",
         "Quantities associated with commodity entries"],
    ]
    return _save_table_png(
        "Sign Groups", "Sign Group Types in Linear A (per GORILA literature)",
        headers, rows, "tbl_02_sign_group_types.png",
        col_widths=[0.16, 0.16, 0.36, 0.32], fig_h=4.5,
    )


# ---------------------------------------------------------------------------
# Figure 1 – Pie chart: sign categories
# ---------------------------------------------------------------------------

def _fig_catalog_categories(catalog: list) -> Tuple[str, str, str]:
    cats = Counter(e["category"] for e in catalog)
    labels = [k.replace("_", "\n").title() for k in cats]
    sizes  = list(cats.values())
    colors = [_COLORS.get(k, "#AAAAAA") for k in cats]

    fig, ax = plt.subplots(figsize=(9, 6))
    wedges, texts, autotexts = ax.pie(
        sizes, labels=None, autopct="%1.0f%%",
        colors=colors, startangle=90, pctdistance=0.78,
        wedgeprops={"linewidth": 1, "edgecolor": "white"},
    )
    for at in autotexts:
        at.set_fontsize(11)
        at.set_fontweight("bold")
        at.set_color("white")

    ax.legend(
        wedges, [f"{l.replace(chr(10), ' ')} ({s})" for l, s in zip(labels, sizes)],
        loc="lower center", bbox_to_anchor=(0.5, -0.12),
        ncol=2, fontsize=10, frameon=False,
    )
    ax.set_title("Linear A – Sign Categories (341 signs total)\n"
                 "Unicode block U+10600–U+1077F",
                 fontsize=_TITLE_FONTSIZE, fontweight="bold", pad=12)
    fig.tight_layout()
    path = os.path.join(FIGURES_DIR, "fig_01_catalog_categories.png")
    fig.savefig(path, dpi=_DPI, bbox_inches="tight")
    plt.close(fig)
    print("[stats] saved fig_01_catalog_categories.png")
    return ("Catalog Pie", "Linear A – Sign Categories", path)


# ---------------------------------------------------------------------------
# Figure 2 – Horizontal bar: top-15 sign group frequencies
# ---------------------------------------------------------------------------

# Hard-coded type classification for known sign groups
_ACCOUNTING = {"KU-RO", "KI-RO"}
_LOGOGRAMS  = {"GRA", "VIN", "OLE", "OVS", "BOS", "SUS", "CAP", "FIC", "HORD",
               "CERV", "TELA", "LANA"}
_FORMULAS   = {"A-SA-SA-RA-ME", "I-DA-MA-TE", "A-TA-I-*301-WA-JA",
               "A-RE-NE-SI", "I-PI-NA-MI-NA", "SU-PU2-WA"}


def _group_color(g: str) -> str:
    if g in _ACCOUNTING:
        return _COLORS["accounting"]
    if g in _LOGOGRAMS:
        return _COLORS["commodity"]
    if g in _FORMULAS:
        return _COLORS["formula"]
    return _COLORS["other_group"]


def _fig_sign_group_frequencies(df: pd.DataFrame) -> Tuple[str, str, str]:
    all_groups: List[str] = []
    for s in df["sign_groups"].dropna():
        all_groups.extend(s.split("|"))
    freq = Counter(all_groups)
    top  = freq.most_common(15)
    labels = [g for g, _ in top]
    counts = [c for _, c in top]
    colors = [_group_color(g) for g in labels]
    pcts   = [100 * c / len(all_groups) for c in counts]

    fig, ax = plt.subplots(figsize=(_FIG_W, _FIG_H))
    y_pos = np.arange(len(labels))
    bars  = ax.barh(y_pos, counts, color=colors, edgecolor="white", height=0.7)

    for bar, pct in zip(bars, pcts):
        ax.text(bar.get_width() + 0.5, bar.get_y() + bar.get_height() / 2,
                f"{pct:.1f}%", va="center", fontsize=9)

    ax.set_yticks(y_pos)
    ax.set_yticklabels(labels, fontsize=10)
    ax.invert_yaxis()
    ax.set_xlabel("Occurrences in corpus", fontsize=11)
    ax.set_title("Top 15 Sign Groups by Frequency\n"
                 "Colour: ■ Accounting term  ■ Commodity logogram  "
                 "■ Libation formula  ■ Syllabic word",
                 fontsize=_TITLE_FONTSIZE, fontweight="bold")
    ax.set_xlim(0, max(counts) * 1.18)

    legend_patches = [
        mpatches.Patch(color=_COLORS["accounting"],  label="Accounting term"),
        mpatches.Patch(color=_COLORS["commodity"],   label="Commodity logogram"),
        mpatches.Patch(color=_COLORS["formula"],     label="Libation formula"),
        mpatches.Patch(color=_COLORS["other_group"], label="Syllabic word"),
    ]
    ax.legend(handles=legend_patches, loc="lower right", fontsize=9, frameon=True)
    ax.grid(axis="x", linestyle="--", alpha=0.4)
    fig.tight_layout()
    path = os.path.join(FIGURES_DIR, "fig_02_sign_group_frequencies.png")
    fig.savefig(path, dpi=_DPI, bbox_inches="tight")
    plt.close(fig)
    print("[stats] saved fig_02_sign_group_frequencies.png")
    return ("Sign Groups", "Top 15 Sign Groups by Frequency", path)


# ---------------------------------------------------------------------------
# Table 3 – Corpus Overview
# ---------------------------------------------------------------------------

def _tbl_corpus_overview(df: pd.DataFrame) -> Tuple[str, str, str]:
    total = len(df)
    n_sites = df["site"].nunique()
    dated = int(df["date_est"].notna().sum())
    lo, hi = int(abs(df["date_est"].min())), int(abs(df["date_est"].max()))
    clay  = int((df["material"] == "clay").sum())
    stone = int((df["material"] == "stone").sum())
    all_g: List[str] = []
    for s in df["sign_groups"].dropna():
        all_g.extend(s.split("|"))
    gf = Counter(all_g)
    sc = df["sign_count"]

    headers = ["Metric", "Value"]
    rows = [
        ["Total tablets",               str(total)],
        ["Find-sites",                  str(n_sites)],
        ["Dated tablets",               f"{dated} (all tablets have estimates)"],
        ["Date range (approx. BCE)",    f"{hi} – {lo}"],
        ["Clay tablets",                str(clay)],
        ["Stone tablets / vessels",     str(stone)],
        ["Total sign groups in corpus", str(len(all_g))],
        ["Unique sign groups",          str(len(gf))],
        ["Signs per tablet (mean)",     f"{sc.mean():.1f}"],
        ["Signs per tablet (range)",    f"{int(sc.min())} – {int(sc.max())}"],
        ["Most frequent sign group",    f"{gf.most_common(1)[0][0]}  "
                                        f"({gf.most_common(1)[0][1]} occurrences, "
                                        f"{100*gf.most_common(1)[0][1]/len(all_g):.0f}%)"],
    ]
    return _save_table_png(
        "Corpus Stats", "Linear A Corpus – Overview Statistics",
        headers, rows, "tbl_03_corpus_overview.png",
        col_widths=[0.38, 0.62], fig_h=5.0,
    )


# ---------------------------------------------------------------------------
# Table 4 – Site Breakdown
# ---------------------------------------------------------------------------

def _tbl_site_breakdown(df: pd.DataFrame) -> Tuple[str, str, str]:
    site_df = get_site_summary_df(df)
    headers = ["Site", "Tablets", "Clay", "Stone", "Lat °N", "Lon °E",
               "Date range (BCE)"]
    rows = []
    for _, r in site_df.iterrows():
        date_rng = (f"{r['date_min_bce']} – {r['date_max_bce']}"
                    if r["date_min_bce"] is not None else "—")
        rows.append([
            r["site"], r["tablet_count"], r["clay_count"], r["stone_count"],
            f"{r['lat']:.3f}", f"{r['lon']:.3f}", date_rng,
        ])
    return _save_table_png(
        "Site Breakdown", "Linear A Tablets by Find-Site (Crete and Aegean region)",
        headers, rows, "tbl_04_site_breakdown.png",
        col_widths=[0.22, 0.10, 0.08, 0.08, 0.10, 0.10, 0.18],
        fig_h=5.5,
    )


# ---------------------------------------------------------------------------
# Figure 3 – Map of Crete with find-sites
# ---------------------------------------------------------------------------

def _fig_site_map(df: pd.DataFrame) -> Tuple[str, str, str]:
    site_df  = get_site_summary_df(df)
    fig, ax  = plt.subplots(figsize=(14, 6))

    # Sea background
    ax.set_facecolor("#A8D5E2")

    # Crete only
    xs = [p[0] for p in CRETE_OUTLINE]
    ys = [p[1] for p in CRETE_OUTLINE]
    ax.fill(xs, ys, color="#E8DEC0", zorder=2)
    ax.plot(xs + [xs[0]], ys + [ys[0]], color="#888888",
            linewidth=0.8, zorder=3)

    # Map extent: tight around Crete with padding
    ax.set_xlim(23.2, 26.7)
    ax.set_ylim(34.65, 35.85)
    ax.set_aspect(1.4)  # rough Mercator correction at 35°N

    # Manual label nudges: (offset_x, offset_y, ha, va)
    _nudge = {
        "Hagia Triada": (-0.08, -0.04, "right", "top"),
        "Phaistos":     (-0.08,  0.02, "right", "bottom"),
        "Knossos":      ( 0.08, -0.04, "left",  "top"),
        "Arkhanes":     ( 0.08,  0.02, "left",  "bottom"),
        "Khania":       (-0.08,  0.02, "right", "bottom"),
        "Mallia":       ( 0.08,  0.02, "left",  "bottom"),
        "Tylissos":     (-0.08, -0.04, "right", "top"),
        "Myrtos":       ( 0.08, -0.04, "left",  "top"),
        "Nirou Khani":  ( 0.08, -0.04, "left",  "top"),
        "Gournia":      ( 0.08,  0.02, "left",  "bottom"),
        "Palaikastro":  ( 0.08,  0.02, "left",  "bottom"),
        "Apodioulou":   (-0.08, -0.04, "right", "top"),
    }

    # Cretan site scatter
    for _, row in site_df.iterrows():
        if row["island"] != "Crete":
            continue
        size = max(100, row["tablet_count"] * 30)
        ax.scatter(row["lon"], row["lat"], s=size,
                   color="#C0392B", edgecolors="#800000",
                   linewidths=0.8, zorder=5, alpha=0.85)
        ox, oy, ha, va = _nudge.get(row["site"], (0.08, 0.02, "left", "bottom"))
        ax.annotate(
            f"{row['site']}  (n={row['tablet_count']})",
            xy=(row["lon"], row["lat"]),
            xytext=(row["lon"] + ox, row["lat"] + oy),
            fontsize=8.5, color="#2C3E50", zorder=6,
            ha=ha, va=va,
            bbox=dict(boxstyle="round,pad=0.15", fc="white", ec="none", alpha=0.75),
        )

    # Akrotiri callout (off-map, annotated in corner)
    akrotiri = site_df[site_df["site"] == "Akrotiri"]
    if not akrotiri.empty:
        n = int(akrotiri.iloc[0]["tablet_count"])
        ax.annotate(
            f"Akrotiri / Thera  (n={n})\n120 km N  (Santorini)",
            xy=(25.4, 35.83), fontsize=9, color="#C0392B",
            ha="center", va="top", fontweight="bold",
            bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="#C0392B",
                      alpha=0.9, linewidth=1.2),
            zorder=7,
        )
        # north-pointing arrow
        ax.annotate("", xy=(25.4, 35.85), xytext=(25.4, 35.78),
                    arrowprops=dict(arrowstyle="->", color="#C0392B", lw=1.5),
                    zorder=7)

    # Island label
    ax.text(24.9, 35.15, "C R E T E", fontsize=13, color="#5A4A3A",
            ha="center", va="center", alpha=0.4, style="italic",
            fontweight="bold", zorder=4)
    ax.text(24.9, 34.72, "Libyan Sea", fontsize=9, color="#6AA3B8",
            ha="center", style="italic", zorder=4)
    ax.text(24.9, 35.77, "Sea of Crete", fontsize=9, color="#6AA3B8",
            ha="center", style="italic", zorder=4)

    ax.set_xlabel("Longitude (°E)", fontsize=10)
    ax.set_ylabel("Latitude (°N)", fontsize=10)
    ax.set_title("Linear A Tablet Find-Sites on Crete\n"
                 "Circle size proportional to tablet count.",
                 fontsize=_TITLE_FONTSIZE, fontweight="bold")
    ax.grid(linestyle="--", alpha=0.25, zorder=1)

    fig.tight_layout()
    path = os.path.join(FIGURES_DIR, "fig_03_site_map.png")
    fig.savefig(path, dpi=_DPI, bbox_inches="tight")
    plt.close(fig)
    print("[stats] saved fig_03_site_map.png")
    return ("Map", "Tablet Find-Sites – Crete", path)


# ---------------------------------------------------------------------------
# Figure 4 – Timeline: tablet date × site, clay vs stone
# ---------------------------------------------------------------------------

def _fig_timeline(df: pd.DataFrame) -> Tuple[str, str, str]:
    # Work in positive BCE for display
    plot_df = df.copy()
    plot_df["date_bce"] = plot_df["date_est"].abs()

    # Order sites by median date
    site_order = (
        plot_df.groupby("site")["date_bce"]
        .median()
        .sort_values()
        .index.tolist()
    )

    fig, ax = plt.subplots(figsize=(_FIG_W, max(5, len(site_order) * 0.65 + 1.5)))

    color_map = {"clay": _COLORS["clay"], "stone": _COLORS["stone"]}

    # Draw a faint horizontal span per site showing its date range
    for i, site in enumerate(site_order):
        grp = plot_df[plot_df["site"] == site]
        lo, hi = grp["date_bce"].min(), grp["date_bce"].max()
        ax.barh(i, hi - lo, left=lo, height=0.35, color="#D5D8DC",
                edgecolor="none", zorder=2, alpha=0.7)
        # Tablet count label at right edge
        ax.text(hi + 4, i, f"n={len(grp)}", va="center", fontsize=8,
                color="#888888", zorder=4)

    # Jitter overlapping points within each site
    for i, site in enumerate(site_order):
        grp = plot_df[plot_df["site"] == site]
        dates = grp["date_bce"].values
        materials = grp["material"].values
        # Determine jitter offsets for stacked points at same date
        date_counts: dict = {}
        jitters = []
        for d in dates:
            date_counts.setdefault(d, 0)
            jitters.append(date_counts[d])
            date_counts[d] += 1
        for d, mat, j in zip(dates, materials, jitters):
            # Centre the stack
            total_at = date_counts[d]
            y_off = (j - (total_at - 1) / 2) * 0.06
            c = color_map.get(mat, "#AAAAAA")
            ax.scatter(d, i + y_off, color=c, s=60,
                       edgecolors="white", linewidths=0.4, zorder=3, alpha=0.9)

    ax.set_yticks(range(len(site_order)))
    ax.set_yticklabels(site_order, fontsize=10)
    ax.invert_xaxis()           # older dates on the left
    ax.set_xlabel("Approximate date (BCE)", fontsize=11)
    ax.set_title("Tablet Corpus – Estimated Date by Find-Site\n"
                 "Each dot = one tablet. Grey bar = site date range.",
                 fontsize=_TITLE_FONTSIZE, fontweight="bold")
    ax.grid(axis="x", linestyle="--", alpha=0.3, zorder=1)

    legend_patches = [
        mpatches.Patch(color=_COLORS["clay"],  label="Clay tablet"),
        mpatches.Patch(color=_COLORS["stone"], label="Stone vessel / table"),
    ]
    ax.legend(handles=legend_patches, fontsize=9, loc="upper right",
              frameon=True)
    fig.tight_layout()
    path = os.path.join(FIGURES_DIR, "fig_04_timeline.png")
    fig.savefig(path, dpi=_DPI, bbox_inches="tight")
    plt.close(fig)
    print("[stats] saved fig_04_timeline.png")
    return ("Timeline", "Tablet Distribution by Estimated Date", path)


# ---------------------------------------------------------------------------
# Figure 5 – Histogram: signs per tablet
# ---------------------------------------------------------------------------

def _fig_signs_per_tablet(df: pd.DataFrame) -> Tuple[str, str, str]:
    sc = df["sign_count"]

    fig, ax = plt.subplots(figsize=(9, 5))
    n_bins = min(10, sc.nunique())
    ax.hist(sc, bins=n_bins, color=_COLORS["syllabic"],
            edgecolor="white", linewidth=0.8)

    ax.axvline(sc.mean(),   color="#C44E52", linestyle="--",
               linewidth=1.5, label=f"Mean = {sc.mean():.1f}")
    ax.axvline(sc.median(), color="#55A868", linestyle=":",
               linewidth=1.5, label=f"Median = {sc.median():.1f}")

    ax.set_xlabel("Number of recognised signs per tablet", fontsize=11)
    ax.set_ylabel("Number of tablets", fontsize=11)
    ax.set_title("Distribution of Signs per Tablet\n"
                 "Recognised (non-'?') Linear A signs only.",
                 fontsize=_TITLE_FONTSIZE, fontweight="bold")
    ax.legend(fontsize=9, frameon=True)
    ax.grid(axis="y", linestyle="--", alpha=0.4)
    fig.tight_layout()
    path = os.path.join(FIGURES_DIR, "fig_05_signs_per_tablet.png")
    fig.savefig(path, dpi=_DPI, bbox_inches="tight")
    plt.close(fig)
    print("[stats] saved fig_05_signs_per_tablet.png")
    return ("Signs per Tablet", "Distribution of Signs per Tablet", path)


# ---------------------------------------------------------------------------
# Figure 6 – Corpus coverage: DB count vs total known inscriptions
# ---------------------------------------------------------------------------

def _fig_corpus_coverage(df: pd.DataFrame) -> Tuple[str, str, str]:
    """Stacked horizontal bar showing inscriptions in DB vs remaining known."""
    # Build per-site counts
    db_counts = df["site"].value_counts().to_dict()

    sites_ordered = sorted(
        KNOWN_SITE_TOTALS.keys(),
        key=lambda s: KNOWN_SITE_TOTALS[s],
        reverse=True,
    )

    labels: List[str] = []
    in_db:  List[int] = []
    remain: List[int] = []

    for site in sites_ordered:
        known  = KNOWN_SITE_TOTALS[site]
        in_db_n = min(db_counts.get(site, 0), known)   # cap at known total
        labels.append(site)
        in_db.append(in_db_n)
        remain.append(max(0, known - in_db_n))

    # Summary row: totals
    total_in_db   = len(df)
    total_remain  = max(0, TOTAL_KNOWN_INSCRIPTIONS - total_in_db)
    labels.append("TOTAL CORPUS")
    in_db.append(total_in_db)
    remain.append(total_remain)

    y = np.arange(len(labels))
    fig_h = max(6, len(labels) * 0.6 + 2)
    fig, ax = plt.subplots(figsize=(_FIG_W, fig_h))

    bar_in   = ax.barh(y, in_db,  color="#2E86AB", edgecolor="white",
                       height=0.6, label="In database")
    bar_rem  = ax.barh(y, remain, left=in_db, color="#E8E8E8",
                       edgecolor="#AAAAAA", height=0.6, label="Not yet encoded")

    # Percentage label inside the 'in database' bar
    for i, (n, r) in enumerate(zip(in_db, remain)):
        total = n + r
        pct   = 100 * n / total if total > 0 else 0
        if n > 10:
            ax.text(n / 2, i, f"{pct:.0f}%",
                    va="center", ha="center", fontsize=8,
                    color="white", fontweight="bold")
        # Count label at the right edge
        ax.text(total + total * 0.01, i, f"{n} / {total}",
                va="center", ha="left", fontsize=8, color="#444444")

    # Highlight the TOTAL row
    ax.get_children()  # force render order
    ax.axhline(len(labels) - 1.5, color="#888888", linewidth=0.8, linestyle="--")

    ax.set_yticks(y)
    ax.set_yticklabels(labels, fontsize=10)
    ax.set_xlabel("Number of inscriptions", fontsize=11)
    ax.set_xlim(0, TOTAL_KNOWN_INSCRIPTIONS * 1.15)
    ax.set_title(
        f"Linear A Corpus Coverage – Database vs Total Known Inscriptions\n"
        f"Total known: ~{TOTAL_KNOWN_INSCRIPTIONS}  |  "
        f"In this database: {total_in_db}  ({100 * total_in_db / TOTAL_KNOWN_INSCRIPTIONS:.1f}%)\n"
        f"Sources: GORILA vols I–V; Younger's online corpus",
        fontsize=_TITLE_FONTSIZE, fontweight="bold",
    )
    ax.legend(loc="lower right", fontsize=9, frameon=True)
    ax.grid(axis="x", linestyle="--", alpha=0.3)
    fig.tight_layout()
    path = os.path.join(FIGURES_DIR, "fig_06_corpus_coverage.png")
    fig.savefig(path, dpi=_DPI, bbox_inches="tight")
    plt.close(fig)
    print("[stats] saved fig_06_corpus_coverage.png")
    return ("Coverage", "Corpus Coverage vs Total Known", path)
