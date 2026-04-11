# Linear A Database

A structured database of **Linear A** — an undeciphered writing system used by the Minoan civilisation on Crete, ca. **1800–1450 BCE**. No one can read it. This project encodes what we have into a machine-readable format.

**317 tablets** from **14 archaeological sites** | **341 Unicode signs** | **~22.6 %** of all known Linear A inscriptions

---

## 1 — What Is This?

Linear A is the main script of Bronze Age Crete. It appears on clay accounting tablets, stone libation vessels, and a handful of other objects. Despite a century of study, the underlying language remains unknown. The writing system uses three types of signs:

![Sign catalog overview](data/figures/tbl_01_catalog_overview.png)

![Sign categories](data/figures/fig_01_catalog_categories.png)

- **Syllabic** (81 signs) — phonetic syllabograms, values inferred from the later Linear B script
- **Logographic** (230 signs) — ideograms for objects and commodities (grain, wine, oil, livestock)
- **Numeric/fraction** (30 signs) — quantity notation

These signs combine into **sign groups** — the "words" on each tablet:

![Sign group types](data/figures/tbl_02_sign_group_types.png)

---

## 2 — Quality Confidence Scores (QCS)

Every data source and enrichment method that feeds this database is assigned a **Quality Confidence Score (QCS)** — a value between 0 and 1 that expresses how likely the data is to be correct:

| QCS | Interpretation |
|-----|---------------|
| **1.0** | Definitely correct (e.g. Unicode standard definitions) |
| **0.75** | Strong scholarly consensus, minor uncertainties remain |
| **0.5** | More likely correct than incorrect — **inclusion threshold** |
| **< 0.5** | More likely incorrect — excluded from the database |

The default inclusion threshold is **0.5**: only strategies scoring at or above this cutoff contribute to the final cleaned database. This threshold is configurable via the `qcs_threshold` parameter on `LinaBaseBuilder`.

![QCS strategy scores](data/figures/fig_07_qcs_strategies.png)

Strategies above the red dashed line are included; those below (shown in red) are excluded. Each tablet in the database inherits the QCS of its source strategy, ensuring traceability from record to quality rationale.

### Currently included strategies (QCS ≥ 0.5)

| Strategy | QCS | Category | Description |
|----------|-----|----------|-------------|
| Unicode Sign Catalog | 1.00 | Mapping | 341 signs from Unicode Standard U+10600–U+1077F |
| Site Geographic Coordinates | 0.95 | Mapping | WGS-84 lat/lon for 14 find-sites |
| GORILA Published Transliterations | 0.90 | Corpus | Godart & Olivier GORILA vols I–V (1976–1985) |
| Material Classification | 0.85 | Enrichment | Clay/stone from published excavation reports |
| Younger Online Corpus | 0.80 | Corpus | Younger's online Linear A transliteration corpus |
| Commodity Logogram Resolution | 0.70 | Enrichment | GRA, VIN, OLE → GORILA sign labels |
| Linear B Phonetic Value Assignment | 0.60 | Enrichment | Syllabic values from Linear B correspondence |
| Archaeological Date Estimates | 0.55 | Enrichment | BCE dates from stratigraphy (±50–100 yr) |

### Currently excluded strategies (QCS < 0.5)

| Strategy | QCS | Reason for exclusion |
|----------|-----|---------------------|
| Undeciphered Phonetic Readings | 0.30 | Speculative, no Linear B parallel |
| AI-Generated Transliterations | 0.20 | Experimental, unvalidated |

---

## 3 — The Database at a Glance

This database contains **317 inscriptions** drawn from GORILA vols I–V and Younger's transliteration corpus.

![Corpus overview](data/figures/tbl_03_corpus_overview.png)

### Coverage

317 of ~1,400 known inscriptions = **~22.6 %**. Coverage is high for the major Cretan archives and zero for the long tail of minor sites, sealings, and non-Cretan finds.

![Coverage by site](data/figures/fig_06_corpus_coverage.png)

---

## 4 — Geographic Distribution

All 13 Cretan sites plus Akrotiri on Santorini (Thera) — 14 find-sites total — shown on a real geographic map using Natural Earth 50 m coastline data via geopandas. Hagia Triada dominates with ~43 % of the corpus.

![Site breakdown](data/figures/tbl_04_site_breakdown.png)

![Site map](data/figures/fig_03_site_map.png)

Note that the above distribution covers 317 of ~1,400 known inscriptions = ~22.6 %

---

## 5 — Temporal Distribution

Most tablets cluster around **1500 BCE** (Late Minoan I). Khania is the outlier — its archive dates to ~1350 BCE, over a century later than the rest.

![Timeline](data/figures/fig_04_timeline.png)

---

## 6 — Sign Group Frequencies

**GRA** (grain) and **KU-RO** (grand total) dominate — reflecting that most tablets are commodity accounting records. Personal names (A-DU, KU-PA3-NU, DA-QE-RA) appear among the top syllabic entries.

![Sign group frequencies](data/figures/fig_02_sign_group_frequencies.png)

---

## 7 — Signs per Tablet

Tablets typically carry **8–13 recognised signs**. The narrow range reflects formulaic accounting: name + commodity + quantity + total.

![Signs per tablet](data/figures/fig_05_signs_per_tablet.png)

---

## 7 — Inclusion Strategy & Quality Confidence Scoring

### The Problem

There are roughly **~1,400 known Linear A inscriptions** but this database currently covers only **317 (~22.6 %)**. Should we include everything? No — the remaining ~1,083 inscriptions vary enormously in quality, legibility, provenance certainty, and publication rigour. Including poor-quality data would degrade the database for any downstream analysis (sign frequency, phonetic distribution, geographic modelling, decipherment attempts).

### Quality Confidence Score (QCS)

Every potential source is evaluated on **five dimensions** (each 0–1):

| Dimension | Weight | What It Measures |
|---|---|---|
| Transliteration reliability | 30 % | How standardised and peer-reviewed the transliteration is |
| Provenance certainty | 20 % | Confidence in the attributed find-site and archaeological context |
| Publication quality | 25 % | Whether the source appears in GORILA, peer-reviewed journals, or only grey literature |
| Sign completeness | 15 % | Proportion of legible signs vs. damaged, missing, or uncertain |
| Consistency with corpus | 10 % | How well the conventions align with the existing database format |

**QCS = weighted average** of the five scores. The **inclusion threshold is QCS ≥ 0.60**.

### Source Evaluation

![Quality confidence scores](data/figures/fig_07_quality_confidence.png)

### What the Scores Reveal

**Currently included sources (QCS 0.76–0.94):** All 14 sites comfortably pass the threshold. The major GORILA archives (Hagia Triada, Khania, Zakros, Phaistos) score 0.90+ due to comprehensive publication and standardised transliteration. Minor sites (Apodioulou, Myrtos, Nirou Khani) score lower (0.76–0.79) due to fragmentary tablets and small sample sizes, but still pass comfortably.

**Recommended for inclusion (QCS 0.62–0.68):**

| Source | ~Inscriptions | QCS | Key Challenge |
|---|---|---|---|
| Minor Cretan sites – remaining clay tablets | 150 | 0.68 | Scattered across ~30 sites, published in diverse excavation reports |
| Non-Cretan Aegean finds (Kea, Kythera, Miletos) | 80 | 0.62 | Varied materials, some well-published, some isolated |
| Stone libation vessels & tables | 200 | 0.62 | Ritual texts, many unprovenanced museum pieces, deviant sign forms |

**Below threshold (QCS 0.42–0.55):**

| Source | ~Inscriptions | QCS | Why Excluded |
|---|---|---|---|
| Clay sealings, roundels & nodules | 250 | 0.55 | 1–3 signs per item, poor legibility, Hieroglyphic overlap |
| Inscribed ceramic vessels & sherds | 120 | 0.52 | May be potter's marks not writing, high ambiguity |
| Metal objects (pins, axes, rings) | 100 | 0.47 | Often single-sign, many from antiquities trade |
| Miscellaneous (labels, weights, graffiti) | 60 | 0.42 | Heterogeneous, very short, heavily damaged |
| Doubtful / possible forgeries | 25 | 0.21 | Suspected fakes — must never be included |

### Decision Rule

```
IF   QCS ≥ 0.60  →  INCLUDE (subject to transliteration encoding)
IF   0.50 ≤ QCS < 0.60  →  REVIEW (include only with manual verification)
IF   QCS < 0.50  →  EXCLUDE (too unreliable for systematic analysis)
```

### Achievable Coverage

At the **QCS ≥ 0.60 threshold**, achievable coverage rises from the current 317 to approximately **766 inscriptions (~55 %)** of all known Linear A texts. This represents the realistic ceiling for a high-confidence database.

Lowering the threshold to 0.55 would add sealings, pushing to ~1,016 (~73 %), but at the cost of including many 1–3 sign items with poor legibility and Cretan Hieroglyphic contamination. This is not recommended without per-inscription manual quality review.

### Priority Actions for Coverage Expansion

| Priority | Action | +Inscriptions | Complexity | Quality Risk |
|---|---|---|---|---|
| 1 | Encode minor Cretan site clay tablets | +150 | Medium | Low |
| 2 | Encode stone libation vessels (GORILA vol V) | +200 | Medium | Medium |
| 3 | Encode non-Cretan Aegean finds | +80 | Low–Medium | Low |

---

## Quick Start

```bash
pip install -r requirements.txt
python main.py
```

### Customising the QCS threshold

```python
from model import LinaBaseBuilder

# Default: include strategies with QCS >= 0.5
builder = LinaBaseBuilder()
builder.run()

# Stricter: only high-confidence sources
builder = LinaBaseBuilder(qcs_threshold=0.75)
builder.run()
```

Or from the command line:

```bash
python main.py --qcs-threshold 0.6
```

Outputs: `data/lina_database_raw.csv`, `data/lina_database_clean.csv`, `data/lina_report.xlsx`, `data/figures/*.png`

---

## Schema

| Column | Type | Example |
|---|---|---|
| `tablet_id` | str | `HT 1` |
| `site` | str | `Hagia Triada` |
| `date_est` | Int64 | `-1500` |
| `material` | str | `clay` / `stone` |
| `source_strategy` | str | `gorila_transliterations` |
| `qcs` | float | `0.90` |
| `transliteration` | str | `A-DU GRA KU-RO` |
| `sign_groups` | str | `A-DU\|GRA\|KU-RO` |
| `sign_sequence_unicode` | str | Unicode Linear A characters |
| `sign_sequence_ids` | str | `3,26,52,11` |
| `sign_group_count` | int | `3` |
| `sign_count` | int | `5` |

---

## Assumptions & Limitations

| # | Area | Note |
|---|---|---|
| 1 | **QCS threshold** | The default inclusion threshold of **0.5** means "more likely correct than incorrect". A QCS of 1.0 means "definitely correct". Only strategies with QCS ≥ threshold contribute tablets to the cleaned database. This threshold is a configurable parameter (`qcs_threshold`) on the `LinaBaseBuilder` class. |
| 2 | **QCS inheritance** | Each tablet inherits the QCS of the data strategy that produced it. All tablets currently originate from the GORILA Published Transliterations strategy (QCS 0.90). |
| 3 | **Coverage** | 22.6 % of ~1,400 known inscriptions. Statistics may not generalise to the full corpus. |
| 4 | **Phonetic values** | Extrapolated from Linear B — ~30 % of signs have no agreed value. Treat as hypothetical. (QCS 0.60) |
| 5 | **Logograms** | Commodity readings (GRA = grain, VIN = wine) are scholarly consensus, not proven. (QCS 0.70) |
| 6 | **Dates** | Broad estimates (±50–100 years). Akrotiri fixed to 1628 BCE (volcanic destruction). (QCS 0.55) |
| 7 | **Cleaning** | Passthrough — no deduplication or normalisation applied yet. |
| 8 | **Transliteration** | Damage markers stripped; star-notation signs excluded from counts. |
| 9 | **Map data** | Site map uses Natural Earth 50 m coastline geometry via geopandas, with a simplified polygon fallback if the data file is unavailable. |

---

## Sources

- Godart & Olivier (1976–1985). *GORILA*, vols I–V. Paris: Geuthner.
- Younger, J.G. *Linear A Texts in Transliteration* (online).
- Schoep, I. (2002). *The Administration of Neopalatial Crete*. Minos supplement.
- Hallager, E. (1996). *The Minoan Roundel and Other Sealed Documents*.
- Del Freo & Ferro (2018). "Texts and Contexts" – review of inscribed objects.
- Unicode Standard — Linear A block U+10600–U+1077F.
- Natural Earth — Free vector map data at naturalearthdata.com (CC0 licence).

