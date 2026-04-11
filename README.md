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

All 13 Cretan sites plus Akrotiri (Santorini). Hagia Triada dominates with ~45 % of the corpus. The map below uses **Natural Earth 50 m** coastline data via geopandas for accurate geographic rendering.

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
- Unicode Standard — Linear A block U+10600–U+1077F.
- Natural Earth — 50 m land polygons (public domain).
