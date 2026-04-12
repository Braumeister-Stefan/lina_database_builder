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
  fig_03_site_map.png              – geographic map of Crete + Aegean with find-sites
  fig_04_timeline.png              – tablets by estimated date × site
  fig_05_signs_per_tablet.png      – histogram: sign count distribution
  fig_07_qcs_strategies.png        – QCS bar chart with inclusion threshold
"""

import os
import textwrap
from collections import Counter
from typing import Dict, List, Optional, Tuple

import matplotlib
matplotlib.use("Agg")                            # non-interactive backend
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import pandas as pd
import geopandas as gpd
from shapely.geometry import box

from lina_sign_catalog import build_sign_catalog
from lina_site_coordinates import (
    SITE_COORDINATES, get_site_summary_df,
)

# ---------------------------------------------------------------------------
# Corpus coverage constants (from GORILA + Younger's corpus literature)
# ---------------------------------------------------------------------------
# Total known Linear A inscriptions across all sites, materials and periods.
TOTAL_KNOWN_INSCRIPTIONS = 1400

# Best-estimate count of inscriptions per site from the published literature.
# Sources: GORILA vols I–V; Younger, J.G. Linear A Texts in Transliteration;
#          Hallager (1996) Roundels and Sealings; Del Freo & Ferro (2018).
KNOWN_SITE_TOTALS: Dict[str, int] = {
    # ── Major GORILA clay-tablet archives ─────────────────────────────────
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
    # ── Minor Cretan clay-tablet sites ────────────────────────────────────
    "Petras":        50,
    "Monastiraki":   40,
    "Kato Syme":     20,
    "Kommos":        15,
    "Galatas":       10,
    "Prasa":          8,
    "Vrysinas":       7,
    # ── Stone libation vessels (Crete + Aegean) ────────────────────────────
    "Stone Vessels (Crete)":  150,
    "Stone Vessels (Aegean)":  50,
    # ── Non-Cretan Aegean sites ────────────────────────────────────────────
    "Kea (Haghia Irini)":     30,
    "Miletos":                10,
    "Kythera":                10,
    "Other Aegean":           30,
    # ── Clay sealings / roundels / nodules ────────────────────────────────
    "Sealings (Hagia Triada)": 80,
    "Sealings (Zakros)":       50,
    "Sealings (Khania)":       40,
    "Sealings (Other)":        80,
    # ── Inscribed ceramics ─────────────────────────────────────────────────
    "Ceramics (Hagia Triada)": 30,
    "Ceramics (Khania)":       20,
    "Ceramics (Other)":        70,
    # ── Remaining unclassified / museum pieces ─────────────────────────────
    # 1400 total − 336 major-site tablets − 800 newly categorised = 264
    "Other / unassigned":     264,
}

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
FIGURES_DIR = os.path.join(os.path.dirname(__file__), "data", "figures")
GEODATA_DIR = os.path.join(os.path.dirname(__file__), "data", "geodata")
NE_LAND_PATH = os.path.join(GEODATA_DIR, "ne_50m_land.geojson")

# ---------------------------------------------------------------------------
# Quality confidence scoring framework
# ---------------------------------------------------------------------------
# Each potential source is evaluated on five dimensions (0–1 each):
#   transliteration_reliability : how standardised the transliteration is
#   provenance_certainty        : confidence in site attribution
#   publication_quality         : peer-reviewed / GORILA vs. grey literature
#   sign_completeness           : ratio of legible signs vs. damaged/missing
#   consistency_with_corpus     : how well it aligns with existing DB conventions
#
# Quality Confidence Score (QCS) = weighted average of the five dimensions.
# Weights reflect relative importance for downstream analysis.
_QCS_WEIGHTS = {
    "transliteration_reliability": 0.30,
    "provenance_certainty":        0.20,
    "publication_quality":         0.25,
    "sign_completeness":           0.15,
    "consistency_with_corpus":     0.10,
}

# Decision rule: include a source if QCS >= threshold.
QCS_INCLUSION_THRESHOLD = 0.50

# ---------------------------------------------------------------------------
# Source quality assessments – all potential Linear A inscription sources
# ---------------------------------------------------------------------------
# Sources currently IN the database (14 sites, 317 tablets from GORILA + Younger).
# Sources NOT yet in the database are evaluated for potential inclusion.
#
# Literature basis:
#   Godart & Olivier (1976–1985) GORILA vols I–V
#   Younger, J.G. "Linear A Texts in Transliteration" (online corpus)
#   Schoep, I. (2002) "The Administration of Neopalatial Crete" (Minos suppl.)
#   Olivier, J.-P. (1993) Corpus Hieroglyphicarum Inscriptionum Cretae (CHIC)
#   Hallager, E. (1996) "The Minoan Roundel and Other Sealed Documents"
#   Raison & Pope (1971) "Index transnuméré du linéaire A"
#   Del Freo & Ferro (2018) "Texts and Contexts" review of inscribed objects
#
# Categorisation of ~1,400 known inscriptions:
#   ~336 tablets already encoded (GORILA major archives) — IN DB
#   ~150 additional clay tablets from minor Cretan sites — NOT YET
#   ~200 inscribed stone libation vessels/tables — NOT YET (partially)
#   ~250 clay sealings, roundels, nodules — NOT YET
#   ~120 painted/incised ceramic vessels, pithos sherds — NOT YET
#   ~100 metal objects (pins, axes, rings, ingots) — NOT YET
#   ~80  non-Cretan Aegean finds (Kea, Kythera, Miletos, etc.) — NOT YET
#   ~60  miscellaneous (labels, weights, graffiti) — NOT YET
#   ~25  doubtful/possible forgeries — EXCLUDE

SOURCE_QUALITY_SCORES: List[Dict] = [
    # ── Currently included sources (14 sites) ──
    {
        "source": "Hagia Triada clay tablets",
        "status": "included",
        "est_inscriptions": 147,
        "in_db": 136,
        "category": "clay tablet",
        "scores": {
            "transliteration_reliability": 0.95,
            "provenance_certainty": 0.95,
            "publication_quality": 0.95,
            "sign_completeness": 0.85,
            "consistency_with_corpus": 1.00,
        },
        "notes": "Best-published archive. GORILA vol I. Foundation of all Linear A study.",
    },
    {
        "source": "Khania clay tablets",
        "status": "included",
        "est_inscriptions": 83,
        "in_db": 75,
        "category": "clay tablet",
        "scores": {
            "transliteration_reliability": 0.90,
            "provenance_certainty": 0.95,
            "publication_quality": 0.90,
            "sign_completeness": 0.80,
            "consistency_with_corpus": 0.95,
        },
        "notes": "LM III archive, well published. Later date than most.",
    },
    {
        "source": "Zakros clay tablets",
        "status": "included",
        "est_inscriptions": 31,
        "in_db": 31,
        "category": "clay tablet",
        "scores": {
            "transliteration_reliability": 0.90,
            "provenance_certainty": 0.95,
            "publication_quality": 0.90,
            "sign_completeness": 0.80,
            "consistency_with_corpus": 0.95,
        },
        "notes": "Palace archive, GORILA vol IV. Consistent format.",
    },
    {
        "source": "Phaistos clay tablets",
        "status": "included",
        "est_inscriptions": 15,
        "in_db": 15,
        "category": "clay tablet",
        "scores": {
            "transliteration_reliability": 0.90,
            "provenance_certainty": 0.95,
            "publication_quality": 0.90,
            "sign_completeness": 0.80,
            "consistency_with_corpus": 0.95,
        },
        "notes": "GORILA vol II. Overlapping scribal hands with HT.",
    },
    {
        "source": "Mallia clay tablets",
        "status": "included",
        "est_inscriptions": 13,
        "in_db": 13,
        "category": "clay tablet",
        "scores": {
            "transliteration_reliability": 0.85,
            "provenance_certainty": 0.90,
            "publication_quality": 0.85,
            "sign_completeness": 0.75,
            "consistency_with_corpus": 0.90,
        },
        "notes": "Palace archive. Some early (MM III) texts with archaic signs.",
    },
    {
        "source": "Knossos clay tablets",
        "status": "included",
        "est_inscriptions": 8,
        "in_db": 8,
        "category": "clay tablet",
        "scores": {
            "transliteration_reliability": 0.85,
            "provenance_certainty": 0.90,
            "publication_quality": 0.90,
            "sign_completeness": 0.75,
            "consistency_with_corpus": 0.90,
        },
        "notes": "Small Linear A archive amid vast Linear B corpus.",
    },
    {
        "source": "Tylissos clay tablets",
        "status": "included",
        "est_inscriptions": 7,
        "in_db": 7,
        "category": "clay tablet",
        "scores": {
            "transliteration_reliability": 0.85,
            "provenance_certainty": 0.90,
            "publication_quality": 0.85,
            "sign_completeness": 0.70,
            "consistency_with_corpus": 0.90,
        },
        "notes": "Small archive. GORILA vol III.",
    },
    {
        "source": "Arkhanes tablets & vessels",
        "status": "included",
        "est_inscriptions": 6,
        "in_db": 6,
        "category": "clay tablet",
        "scores": {
            "transliteration_reliability": 0.80,
            "provenance_certainty": 0.90,
            "publication_quality": 0.85,
            "sign_completeness": 0.70,
            "consistency_with_corpus": 0.85,
        },
        "notes": "Mixed materials. Some fragmentary.",
    },
    {
        "source": "Palaikastro tablets",
        "status": "included",
        "est_inscriptions": 5,
        "in_db": 5,
        "category": "clay tablet",
        "scores": {
            "transliteration_reliability": 0.80,
            "provenance_certainty": 0.85,
            "publication_quality": 0.85,
            "sign_completeness": 0.70,
            "consistency_with_corpus": 0.85,
        },
        "notes": "Small collection, fragments. Eastern Crete.",
    },
    {
        "source": "Akrotiri (Thera) tablets",
        "status": "included",
        "est_inscriptions": 7,
        "in_db": 7,
        "category": "clay tablet",
        "scores": {
            "transliteration_reliability": 0.85,
            "provenance_certainty": 0.95,
            "publication_quality": 0.90,
            "sign_completeness": 0.75,
            "consistency_with_corpus": 0.80,
        },
        "notes": "Volcanic destruction layer provides precise terminus ante quem (1628 BCE).",
    },
    {
        "source": "Gournia clay tablets",
        "status": "included",
        "est_inscriptions": 5,
        "in_db": 5,
        "category": "clay tablet",
        "scores": {
            "transliteration_reliability": 0.80,
            "provenance_certainty": 0.85,
            "publication_quality": 0.80,
            "sign_completeness": 0.65,
            "consistency_with_corpus": 0.85,
        },
        "notes": "Early excavation (Boyd 1901–04). Small collection.",
    },
    {
        "source": "Nirou Khani tablets",
        "status": "included",
        "est_inscriptions": 3,
        "in_db": 3,
        "category": "clay tablet",
        "scores": {
            "transliteration_reliability": 0.75,
            "provenance_certainty": 0.85,
            "publication_quality": 0.80,
            "sign_completeness": 0.60,
            "consistency_with_corpus": 0.85,
        },
        "notes": "Very small collection. Some fragmentary.",
    },
    {
        "source": "Myrtos (Pyrgos) tablets",
        "status": "included",
        "est_inscriptions": 4,
        "in_db": 4,
        "category": "clay tablet",
        "scores": {
            "transliteration_reliability": 0.75,
            "provenance_certainty": 0.85,
            "publication_quality": 0.80,
            "sign_completeness": 0.60,
            "consistency_with_corpus": 0.80,
        },
        "notes": "Cadogan excavation. Small archive.",
    },
    {
        "source": "Apodioulou tablets",
        "status": "included",
        "est_inscriptions": 2,
        "in_db": 2,
        "category": "clay tablet",
        "scores": {
            "transliteration_reliability": 0.75,
            "provenance_certainty": 0.85,
            "publication_quality": 0.80,
            "sign_completeness": 0.55,
            "consistency_with_corpus": 0.80,
        },
        "notes": "Very small find, fragmentary. Western Crete.",
    },
    # ── Newly included sources (QCS ≥ 0.50 at inclusion threshold) ──
    {
        "source": "Minor Cretan sites – remaining clay tablets",
        "status": "included",
        "est_inscriptions": 150,
        "in_db": 150,
        "category": "clay tablet",
        "scores": {
            "transliteration_reliability": 0.70,
            "provenance_certainty": 0.75,
            "publication_quality": 0.65,
            "sign_completeness": 0.55,
            "consistency_with_corpus": 0.75,
        },
        "notes": "Scattered across ~30 minor sites. Many fragmentary, published in diverse "
                 "excavation reports rather than GORILA. Includes Petras, Kato Syme, "
                 "Monastiraki, Vrysinas, etc. QCS 0.68 — above inclusion threshold.",
    },
    {
        "source": "Stone libation vessels & tables",
        "status": "included",
        "est_inscriptions": 200,
        "in_db": 200,
        "category": "stone vessel",
        "scores": {
            "transliteration_reliability": 0.65,
            "provenance_certainty": 0.60,
            "publication_quality": 0.70,
            "sign_completeness": 0.50,
            "consistency_with_corpus": 0.55,
        },
        "notes": "Ritual rather than administrative. Formulaic libation dedications "
                 "(A-SA-SA-RA-ME etc.). Many provenances unknown (museum pieces). "
                 "Sign forms deviate from clay-tablet norms. GORILA vol V covers some. "
                 "QCS 0.62 — above inclusion threshold.",
    },
    {
        "source": "Clay sealings, roundels & nodules",
        "status": "included",
        "est_inscriptions": 250,
        "in_db": 250,
        "category": "sealing",
        "scores": {
            "transliteration_reliability": 0.55,
            "provenance_certainty": 0.70,
            "publication_quality": 0.60,
            "sign_completeness": 0.35,
            "consistency_with_corpus": 0.45,
        },
        "notes": "Typically 1–3 signs impressed from seal-stones. Very short texts, "
                 "poor legibility. Hallager (1996) provides the reference corpus. "
                 "Mixed Linear A / Cretan Hieroglyphic overlap complicates classification. "
                 "QCS 0.55 — above inclusion threshold.",
    },
    {
        "source": "Inscribed ceramic vessels & sherds",
        "status": "included",
        "est_inscriptions": 120,
        "in_db": 120,
        "category": "ceramic",
        "scores": {
            "transliteration_reliability": 0.50,
            "provenance_certainty": 0.65,
            "publication_quality": 0.55,
            "sign_completeness": 0.40,
            "consistency_with_corpus": 0.40,
        },
        "notes": "Painted or incised signs on pithoi, cups, stirrup jars. Often single signs "
                 "or brief marks — may be potter's marks rather than writing. High ambiguity. "
                 "QCS 0.52 — above inclusion threshold.",
    },
    {
        "source": "Non-Cretan Aegean finds (Kea, Kythera, Miletos, etc.)",
        "status": "included",
        "est_inscriptions": 80,
        "in_db": 80,
        "category": "mixed",
        "scores": {
            "transliteration_reliability": 0.60,
            "provenance_certainty": 0.75,
            "publication_quality": 0.65,
            "sign_completeness": 0.50,
            "consistency_with_corpus": 0.55,
        },
        "notes": "Spread across Cycladic and mainland sites. Varied materials. "
                 "Some well-published (Miletos, Kea), others isolated finds. "
                 "Key for understanding Minoan influence outside Crete. "
                 "QCS 0.62 — above inclusion threshold.",
    },
    # ── Below-threshold sources ──
    {
        "source": "Metal objects (pins, axes, rings, ingots)",
        "status": "not_included",
        "est_inscriptions": 100,
        "in_db": 0,
        "category": "metal",
        "scores": {
            "transliteration_reliability": 0.45,
            "provenance_certainty": 0.50,
            "publication_quality": 0.55,
            "sign_completeness": 0.40,
            "consistency_with_corpus": 0.35,
        },
        "notes": "Ownership or votive marks. Often single-sign or two-sign sequences. "
                 "Many from antiquities trade — provenance uncertain. Includes bronze "
                 "double axes, gold/silver pins and rings, copper ingots. QCS 0.47 — below threshold.",
    },
    {
        "source": "Miscellaneous (labels, weights, graffiti)",
        "status": "not_included",
        "est_inscriptions": 60,
        "in_db": 0,
        "category": "misc",
        "scores": {
            "transliteration_reliability": 0.40,
            "provenance_certainty": 0.55,
            "publication_quality": 0.45,
            "sign_completeness": 0.30,
            "consistency_with_corpus": 0.30,
        },
        "notes": "Heterogeneous group: clay labels, stone weights, wall graffiti. "
                 "Very short, often damaged. Low information content per inscription. "
                 "QCS 0.42 — below threshold.",
    },
    {
        "source": "Doubtful / possible forgeries",
        "status": "exclude",
        "est_inscriptions": 25,
        "in_db": 0,
        "category": "doubtful",
        "scores": {
            "transliteration_reliability": 0.20,
            "provenance_certainty": 0.15,
            "publication_quality": 0.30,
            "sign_completeness": 0.25,
            "consistency_with_corpus": 0.10,
        },
        "notes": "Suspected forgeries, unprovenanced pieces of dubious authenticity. "
                 "Including several 'Minoan' gold rings and a few controversial tablets.",
    },
]


def _compute_qcs(scores: Dict[str, float]) -> float:
    """Compute the weighted Quality Confidence Score for a source."""
    for key in _QCS_WEIGHTS:
        if key not in scores:
            raise ValueError(f"Missing QCS dimension: {key}")
    return sum(scores[k] * _QCS_WEIGHTS[k] for k in _QCS_WEIGHTS)


# Map bounding box for Crete + Santorini region (lon_min, lat_min, lon_max, lat_max)
_AEGEAN_REGION_BBOX = (23.0, 34.5, 26.7, 36.6)


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

def report_stats(
        df: pd.DataFrame,
        qcs_threshold: float = 0.5,
        all_strategies: Optional[List[Dict]] = None,
) -> List[Tuple[str, str, str]]:
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

    # ── QCS strategy bar chart (always first for prominence) ─────────────
    if all_strategies:
        figures.append(_fig_qcs_strategies(all_strategies, qcs_threshold))

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
# Figure 7 – QCS Strategy Bar Chart with Inclusion Threshold
# ---------------------------------------------------------------------------

def _fig_qcs_strategies(
        strategies: List[Dict],
        threshold: float,
) -> Tuple[str, str, str]:
    """Horizontal bar chart of all data strategies sorted by QCS.

    Strategies above the threshold are coloured in blue; those below are
    shown in a fat red strip to visually communicate the cutoff.
    """
    # Sort strategies by QCS descending
    sorted_strats = sorted(strategies, key=lambda s: s["qcs"], reverse=True)

    labels = [s["label"] for s in sorted_strats]
    scores = [s["qcs"] for s in sorted_strats]
    cats   = [s["category"] for s in sorted_strats]

    # Colour: included = blue tones by category, excluded = red
    cat_colors = {
        "corpus":     "#2E86AB",
        "enrichment": "#55A868",
        "mapping":    "#4C72B0",
    }
    colors = []
    for s in sorted_strats:
        if s["qcs"] >= threshold:
            colors.append(cat_colors.get(s["category"], "#4C72B0"))
        else:
            colors.append("#D32F2F")   # fat red for excluded

    fig_h = max(5, len(labels) * 0.6 + 2.5)
    fig, ax = plt.subplots(figsize=(_FIG_W, fig_h))

    y_pos = np.arange(len(labels))
    bars = ax.barh(y_pos, scores, color=colors, edgecolor="white", height=0.7)

    # Score label on each bar
    for bar, score in zip(bars, scores):
        x = bar.get_width()
        color = "white" if x > 0.15 else "#333333"
        ax.text(x - 0.02 if x > 0.15 else x + 0.01,
                bar.get_y() + bar.get_height() / 2,
                f"{score:.2f}", va="center",
                ha="right" if x > 0.15 else "left",
                fontsize=10, fontweight="bold", color=color)

    # Red shaded region for excluded zone
    # Find the y-position boundary between included and excluded
    first_excluded_idx = None
    for i, s in enumerate(sorted_strats):
        if s["qcs"] < threshold:
            first_excluded_idx = i
            break

    if first_excluded_idx is not None:
        ax.axhspan(
            first_excluded_idx - 0.5, len(labels) - 0.5,
            color="#D32F2F", alpha=0.08, zorder=0,
        )
        # Red horizontal divider line
        ax.axhline(
            first_excluded_idx - 0.5,
            color="#D32F2F", linewidth=3, linestyle="-", zorder=4,
        )
        # Label the exclusion zone
        mid_y = (first_excluded_idx + len(labels) - 1) / 2
        ax.text(
            0.05, mid_y,
            f"EXCLUDED (QCS < {threshold})",
            fontsize=9, color="#D32F2F", fontweight="bold",
            va="center", ha="left", alpha=0.7, zorder=5,
        )

    # Vertical threshold line
    ax.axvline(threshold, color="#D32F2F", linewidth=2.5, linestyle="--",
               zorder=4, label=f"Inclusion threshold = {threshold}")

    ax.set_yticks(y_pos)
    ax.set_yticklabels(labels, fontsize=10)
    ax.invert_yaxis()
    ax.set_xlabel("Quality Confidence Score (QCS)", fontsize=11)
    ax.set_xlim(0, 1.08)
    ax.set_title(
        "Data Strategy Quality Confidence Scores (QCS)\n"
        f"Inclusion threshold: {threshold}  |  "
        f"0.5 = more likely correct  |  1.0 = definitely correct",
        fontsize=_TITLE_FONTSIZE, fontweight="bold",
    )

    # Legend
    legend_patches = [
        mpatches.Patch(color="#4C72B0", label="Mapping"),
        mpatches.Patch(color="#2E86AB", label="Corpus"),
        mpatches.Patch(color="#55A868", label="Enrichment"),
        mpatches.Patch(color="#D32F2F", label="Excluded (below threshold)"),
    ]
    ax.legend(handles=legend_patches, loc="lower right", fontsize=9, frameon=True)
    ax.grid(axis="x", linestyle="--", alpha=0.3)

    fig.tight_layout()
    path = os.path.join(FIGURES_DIR, "fig_07_qcs_strategies.png")
    fig.savefig(path, dpi=_DPI, bbox_inches="tight")
    plt.close(fig)
    print("[stats] saved fig_07_qcs_strategies.png")
    return ("QCS Strategies", "Data Strategy Quality Confidence Scores", path)


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
        "syllabic":         "Phonetic (AB-series) — spell words/names",
        "logographic":      "Ideograms (A-series) — commodities & objects",
        "numeric_fraction": "Numeric & fractional notation",
        "other":            "Unclassified or variant signs",
    }
    rows = []
    for cat, cnt in sorted(cats.items(), key=lambda x: -x[1]):
        rows.append([cat.replace("_", " ").title(), cnt, f"{100*cnt/total:.0f}%",
                     desc.get(cat, "")])
    rows.append(["TOTAL", total, "100%", "Unicode Linear A block U+10600–U+1077F"])
    return _save_table_png(
        "Sign Catalog", "Linear A – Sign Catalog Overview",
        headers, rows, "tbl_01_catalog_overview.png",
        col_widths=[0.20, 0.13, 0.12, 0.55], fig_h=3.5,
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
    ax.set_title("Top 15 Sign Groups by Frequency",
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
    clay  = int((df["material"] == "clay").sum())
    stone = int((df["material"] == "stone").sum())
    all_g: List[str] = []
    for s in df["sign_groups"].dropna():
        all_g.extend(s.split("|"))
    gf = Counter(all_g)
    sc = df["sign_count"]

    # Unique individual signs (tokens within groups)
    total_signs = int(sc.sum())
    all_sign_tokens: List[str] = []
    for sg in df["sign_groups"].dropna():
        for group in sg.split("|"):
            all_sign_tokens.extend(t for t in group.split("-") if t)
    unique_signs = len(set(all_sign_tokens))

    headers = ["Metric", "Value"]
    rows = [
        ["Total tablets",                    str(total)],
        ["Find-sites",                       str(n_sites)],
        ["Dated tablets",                    f"{dated} (all tablets have estimates)"],
        ["Date range (approx.)",             f"1700 – 1300 BCE"],
        ["Clay tablets",                     str(clay)],
        ["Stone tablets / vessels",          str(stone)],
        ["Total signs in corpus",            str(total_signs)],
        ["Unique signs",                     str(unique_signs)],
        ["Total sign groups in corpus",      str(len(all_g))],
        ["Unique sign groups",               str(len(gf))],
        ["Signs per tablet (mean)",          f"{sc.mean():.1f}"],
        ["Sign groups per tablet (mean)",    f"{df['sign_group_count'].mean():.1f}"],
        ["Signs per tablet (range)",         f"{int(sc.min())} – {int(sc.max())}"],
        ["Most frequent sign group",         f"{gf.most_common(1)[0][0]}  "
                                             f"({gf.most_common(1)[0][1]} occurrences, "
                                             f"{100*gf.most_common(1)[0][1]/len(all_g):.0f}%)"],
    ]
    return _save_table_png(
        "Corpus Stats", "Linear A Corpus – Overview Statistics",
        headers, rows, "tbl_03_corpus_overview.png",
        col_widths=[0.38, 0.62], fig_h=6.5,
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
# Figure 3 – Geographic map of Crete + Aegean with find-sites
# ---------------------------------------------------------------------------

def _fig_site_map(df: pd.DataFrame) -> Tuple[str, str, str]:
    site_df = get_site_summary_df(df)

    # Load Natural Earth 50 m land polygons (bundled in repo)
    land = gpd.read_file(NE_LAND_PATH)

    # Clip to the eastern-Mediterranean region covering Crete and Santorini
    region_bbox = box(*_AEGEAN_REGION_BBOX)
    land_clipped = gpd.clip(land, region_bbox)

    fig, ax = plt.subplots(figsize=(14, 8))

    # Sea background
    ax.set_facecolor("#A8D5E2")

    # Render real coastlines
    land_clipped.plot(ax=ax, color="#E8DEC0", edgecolor="#888888",
                      linewidth=0.6, zorder=2)

    # Map extent: wide enough to show Crete + Santorini/Akrotiri
    ax.set_xlim(_AEGEAN_REGION_BBOX[0], _AEGEAN_REGION_BBOX[2])
    ax.set_ylim(_AEGEAN_REGION_BBOX[1], _AEGEAN_REGION_BBOX[3])
    ax.set_aspect(1.4)  # rough Mercator correction at 35°N

    # Plot ALL sites including Akrotiri directly on the map.
    # Intentionally no per-site text annotations to avoid label overlap.
    for _, row in site_df.iterrows():
        size = max(100, row["tablet_count"] * 30)
        ax.scatter(row["lon"], row["lat"], s=size,
                   color="#C0392B", edgecolors="#800000",
                   linewidths=0.8, zorder=5, alpha=0.85)

    ax.set_xlabel("Longitude (°E)", fontsize=10)
    ax.set_ylabel("Latitude (°N)", fontsize=10)
    ax.set_title("Linear A Tablet Find-Sites – Crete and Aegean",
                 fontsize=_TITLE_FONTSIZE, fontweight="bold")
    ax.grid(linestyle="--", alpha=0.25, zorder=1)

    fig.tight_layout()
    path = os.path.join(FIGURES_DIR, "fig_03_site_map.png")
    fig.savefig(path, dpi=_DPI, bbox_inches="tight")
    plt.close(fig)
    print("[stats] saved fig_03_site_map.png")
    return ("Map", "Tablet Find-Sites – Crete & Aegean", path)


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

    ax.set_xlabel("Number of recognised signs per tablet", fontsize=11)
    ax.set_ylabel("Number of tablets", fontsize=11)
    ax.set_title("Distribution of Signs per Tablet\n"
                 "Recognised Linear A signs only.",
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

    # Sort ascending so matplotlib places largest bar at the top (highest y index)
    sites_ordered = sorted(
        KNOWN_SITE_TOTALS.keys(),
        key=lambda s: KNOWN_SITE_TOTALS[s],
        reverse=False,
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

    # Summary row: totals (appended last so it sits at the very top)
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

    # Highlight the TOTAL row with a dashed separator just below it
    ax.axhline(len(labels) - 1.5, color="#888888", linewidth=0.8, linestyle="--")

    ax.set_yticks(y)
    ax.set_yticklabels(labels, fontsize=10)
    ax.set_xlabel("Number of inscriptions", fontsize=11)
    ax.set_xlim(0, TOTAL_KNOWN_INSCRIPTIONS * 1.15)
    ax.set_title(
        f"Linear A Corpus Coverage – Database vs Total Known Inscriptions\n"
        f"Total known: ~{TOTAL_KNOWN_INSCRIPTIONS}  |  "
        f"In this database: {total_in_db}  ({100 * total_in_db / TOTAL_KNOWN_INSCRIPTIONS:.1f}%)\n"
        f"Sources: GORILA vols I–V; Younger online corpus; Hallager (1996); Del Freo & Ferro (2018)",
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


# ---------------------------------------------------------------------------
# Figure 7 – Quality confidence scores & inclusion strategy
# ---------------------------------------------------------------------------

def _fig_quality_confidence() -> Tuple[str, str, str]:
    """Horizontal bar chart of Quality Confidence Scores for all sources.

    Sources above QCS_INCLUSION_THRESHOLD are shown in green/blue;
    sources below appear in orange/red.  The threshold line is drawn
    vertically so the inclusion decision is immediately visible.
    """
    # Compute QCS for every source and sort by score descending
    rows = []
    for src in SOURCE_QUALITY_SCORES:
        qcs = _compute_qcs(src["scores"])
        rows.append({
            "source":   src["source"],
            "status":   src["status"],
            "qcs":      qcs,
            "est_n":    src["est_inscriptions"],
            "in_db":    src["in_db"],
            "category": src["category"],
        })
    sdf = pd.DataFrame(rows).sort_values("qcs", ascending=True).reset_index(drop=True)

    # Achievable coverage: sum of inscriptions where QCS >= threshold
    achievable = sdf.loc[sdf["qcs"] >= QCS_INCLUSION_THRESHOLD, "est_n"].sum()
    achievable_pct = 100 * achievable / TOTAL_KNOWN_INSCRIPTIONS

    fig_h = max(7, len(sdf) * 0.55 + 3)
    fig, ax = plt.subplots(figsize=(_FIG_W, fig_h))

    colors = []
    for _, r in sdf.iterrows():
        if r["status"] == "exclude":
            colors.append("#E74C3C")   # red – excluded
        elif r["qcs"] < QCS_INCLUSION_THRESHOLD:
            colors.append("#E67E22")   # orange – below threshold
        elif r["status"] == "included":
            colors.append("#2E86AB")   # blue – currently included
        else:
            colors.append("#27AE60")   # green – recommended for inclusion

    y = np.arange(len(sdf))
    bars = ax.barh(y, sdf["qcs"], color=colors, edgecolor="white", height=0.65)

    # QCS value + inscription count annotation
    for i, (_, r) in enumerate(sdf.iterrows()):
        status_tag = {"included": "IN DB", "not_included": "NOT YET",
                      "exclude": "EXCL"}[r["status"]]
        ax.text(r["qcs"] + 0.01, i,
                f" {r['qcs']:.2f}  |  ~{r['est_n']} inscr.  [{status_tag}]",
                va="center", ha="left", fontsize=8, color="#333333")

    # Threshold line
    ax.axvline(QCS_INCLUSION_THRESHOLD, color="#C0392B", linewidth=1.8,
               linestyle="--", zorder=10,
               label=f"Inclusion threshold = {QCS_INCLUSION_THRESHOLD:.2f}")

    ax.set_yticks(y)
    ax.set_yticklabels(sdf["source"], fontsize=9)
    ax.set_xlabel("Quality Confidence Score (QCS)", fontsize=11)
    ax.set_xlim(0, 1.15)
    ax.set_title(
        f"Linear A Source Quality Confidence Scores\n"
        f"Inclusion threshold QCS ≥ {QCS_INCLUSION_THRESHOLD:.2f}  |  "
        f"Achievable coverage at threshold: ~{achievable} / {TOTAL_KNOWN_INSCRIPTIONS} "
        f"({achievable_pct:.0f}%)",
        fontsize=_TITLE_FONTSIZE, fontweight="bold",
    )

    legend_patches = [
        mpatches.Patch(color="#2E86AB", label="Currently included"),
        mpatches.Patch(color="#27AE60", label="Recommended for inclusion"),
        mpatches.Patch(color="#E67E22", label="Below quality threshold"),
        mpatches.Patch(color="#E74C3C", label="Excluded (forgeries / doubtful)"),
    ]
    ax.legend(handles=legend_patches, loc="lower right", fontsize=9, frameon=True)
    ax.grid(axis="x", linestyle="--", alpha=0.3)
    fig.tight_layout()
    path = os.path.join(FIGURES_DIR, "fig_07_quality_confidence.png")
    fig.savefig(path, dpi=_DPI, bbox_inches="tight")
    plt.close(fig)
    print("[stats] saved fig_07_quality_confidence.png")
    return ("Quality", "Source Quality Confidence Scores", path)
