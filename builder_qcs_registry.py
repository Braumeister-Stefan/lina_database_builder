"""
builder_qcs_registry.py – Quality Confidence Score (QCS) strategy registry.

Defines every data source / sub-strategy that feeds into the Linear A
database pipeline, together with its Quality Confidence Score.

QCS calibration
---------------
  0.0  – no confidence (random / fabricated)
  0.5  – more likely correct than incorrect (inclusion threshold default)
  0.75 – probable: strong scholarly consensus, minor uncertainties remain
  1.0  – definitely correct (e.g. Unicode standard definitions)

QCS derivation (for corpus strategies)
---------------------------------------
  QCS is the weighted average of five source-quality dimensions evaluated in
  builder_lina_stats.SOURCE_QUALITY_SCORES using the weights in _QCS_WEIGHTS:
    transliteration_reliability : 0.30
    provenance_certainty        : 0.20
    publication_quality         : 0.25
    sign_completeness           : 0.15
    consistency_with_corpus     : 0.10
  QCS values in this registry are rounded to two decimal places.

Each strategy entry contains:
  key         : unique machine-readable identifier
  label       : human-readable name
  description : one-line explanation of the data source / method
  qcs         : float in [0, 1] – Quality Confidence Score
  category    : 'corpus' | 'enrichment' | 'mapping'
                - corpus      – strategies that contribute tablet records
                - enrichment  – strategies that add columns / fields to tablets
                - mapping     – reference data (sign catalog, coordinates, …)
"""

from typing import Dict, List

# ---------------------------------------------------------------------------
# Strategy registry – ordered by QCS descending for readability
# ---------------------------------------------------------------------------

DATA_STRATEGIES: List[Dict] = [
    # ── Mapping strategies (reference data) ────────────────────────────────
    {
        "key":         "unicode_sign_catalog",
        "label":       "Unicode Sign Catalog",
        "description": "341 Linear A signs from the Unicode Standard (U+10600–U+1077F)",
        "qcs":         1.00,
        "category":    "mapping",
    },
    {
        "key":         "site_coordinates",
        "label":       "Site Geographic Coordinates",
        "description": "WGS-84 lat/lon for 20 archaeological find-sites from published sources",
        "qcs":         0.95,
        "category":    "mapping",
    },

    # ── Corpus strategies (contribute tablet rows) ─────────────────────────
    {
        "key":         "gorila_transliterations",
        "label":       "GORILA Published Transliterations",
        "description": "Tablet transliterations from Godart & Olivier GORILA vols I–V (1976–1985)",
        "qcs":         0.90,
        "category":    "corpus",
    },
    {
        "key":         "younger_corpus",
        "label":       "Younger Online Corpus",
        "description": "Supplementary transliterations from Younger's online Linear A corpus",
        "qcs":         0.80,
        "category":    "corpus",
    },
    {
        "key":         "minor_cretan_clay_tablets",
        "label":       "Minor Cretan Clay Tablets",
        "description": "Clay tablets from ~30 minor Cretan sites (Petras, Monastiraki, Kato Syme, etc.)",
        "qcs":         0.68,
        "category":    "corpus",
    },
    {
        "key":         "stone_libation_vessels",
        "label":       "Stone Libation Vessels & Tables",
        "description": "Inscribed stone vessels with formulaic libation dedications (GORILA vol V; Younger)",
        "qcs":         0.62,
        "category":    "corpus",
    },
    {
        "key":         "aegean_non_cretan",
        "label":       "Non-Cretan Aegean Inscriptions",
        "description": "Linear A finds from Kea, Kythera, Miletos, and other Aegean sites",
        "qcs":         0.62,
        "category":    "corpus",
    },
    {
        "key":         "clay_sealings",
        "label":       "Clay Sealings, Roundels & Nodules",
        "description": "Impressed administrative documents (Hallager 1996); typically 1–3 signs",
        "qcs":         0.55,
        "category":    "corpus",
    },
    {
        "key":         "inscribed_ceramics",
        "label":       "Inscribed Ceramic Vessels",
        "description": "Painted or incised signs on pithoi, cups, stirrup jars (Del Freo & Ferro 2018)",
        "qcs":         0.52,
        "category":    "corpus",
    },
    {
        "key":         "material_classification",
        "label":       "Material Classification",
        "description": "Clay / stone classification based on published excavation reports",
        "qcs":         0.85,
        "category":    "enrichment",
    },

    # ── Enrichment strategies ──────────────────────────────────────────────
    {
        "key":         "commodity_logograms",
        "label":       "Commodity Logogram Resolution",
        "description": "GRA, VIN, OLE, etc. → GORILA sign labels; scholarly consensus, not proven",
        "qcs":         0.70,
        "category":    "enrichment",
    },
    {
        "key":         "linear_b_phonetic_values",
        "label":       "Linear B Phonetic Value Assignment",
        "description": "Syllabic values extrapolated from Linear B correspondence (~30 % uncertain)",
        "qcs":         0.60,
        "category":    "enrichment",
    },
    {
        "key":         "archaeological_dates",
        "label":       "Archaeological Date Estimates",
        "description": "Approximate BCE dates from stratigraphy / destruction contexts (±50–100 yr)",
        "qcs":         0.55,
        "category":    "enrichment",
    },

    # ── Below-threshold strategies (documented for transparency) ──────────
    {
        "key":         "undeciphered_phonetic_readings",
        "label":       "Undeciphered Phonetic Readings",
        "description": "Speculative phonetic interpretations for signs with no Linear B parallel",
        "qcs":         0.30,
        "category":    "enrichment",
    },
    {
        "key":         "ai_generated_transliterations",
        "label":       "AI-Generated Transliterations",
        "description": "Machine-learning-based transliteration attempts (experimental, unvalidated)",
        "qcs":         0.20,
        "category":    "corpus",
    },
]


def get_strategy(key: str) -> Dict:
    """Return a single strategy dict by its key, or raise KeyError."""
    for s in DATA_STRATEGIES:
        if s["key"] == key:
            return s
    raise KeyError(f"Unknown strategy key: {key!r}")


def get_included_strategies(threshold: float = 0.5) -> List[Dict]:
    """Return strategies with QCS ≥ *threshold*, sorted by QCS descending."""
    return sorted(
        [s for s in DATA_STRATEGIES if s["qcs"] >= threshold],
        key=lambda s: s["qcs"],
        reverse=True,
    )


def get_excluded_strategies(threshold: float = 0.5) -> List[Dict]:
    """Return strategies with QCS < *threshold*, sorted by QCS descending."""
    return sorted(
        [s for s in DATA_STRATEGIES if s["qcs"] < threshold],
        key=lambda s: s["qcs"],
        reverse=True,
    )
