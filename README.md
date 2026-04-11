# Linear A Database

A structured database of **Linear A** — an undeciphered writing system used by the Minoan civilisation on Crete, ca. **1800–1450 BCE**. No one can read it. This project encodes what we have into a machine-readable format.

**656 tablets** from **14 georeferenced sites** (+ cluster labels) | **341 Unicode signs** | **~46.9 %** of all known Linear A inscriptions

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
| Site Geographic Coordinates | 0.95 | Mapping | WGS-84 lat/lon for **14** georeferenced find-sites |
| GORILA Published Transliterations | 0.90 | Corpus | Godart & Olivier GORILA vols I–V (1976–1985) — 317 records |
| Material Classification | 0.85 | Enrichment | Clay/stone from published excavation reports |
| Younger Online Corpus | 0.80 | Corpus | Younger's online Linear A transliteration corpus (registered; no records yet loaded) |
| Commodity Logogram Resolution | 0.70 | Enrichment | GRA, VIN, OLE → GORILA sign labels |
| Minor Cretan Clay Tablets | 0.68 | Corpus | Clay tablets from ~30 minor Cretan sites — 150 records |
| Stone Libation Vessels & Tables | 0.62 | Corpus | Individually documented Za-series stone vessels (GORILA vol V; Younger) — 64 records |
| Non-Cretan Aegean Inscriptions | 0.62 | Corpus | Linear A finds from Kea, Kythera, Miletos, and other Aegean sites — 80 records |
| Linear B Phonetic Value Assignment | 0.60 | Enrichment | Syllabic values from Linear B correspondence |
| Clay Sealings, Roundels & Nodules | 0.55 | Corpus | Individually documented Wc-series roundels (Hallager 1996); typically 1–3 signs — 25 records |
| Archaeological Date Estimates | 0.55 | Enrichment | BCE dates from stratigraphy (±50–100 yr) |
| Inscribed Ceramic Vessels | 0.52 | Corpus | Individually documented Zb-series ceramic objects (Del Freo & Ferro 2018) — 20 records |

### Currently excluded strategies (QCS < 0.5)

| Strategy | QCS | Reason for exclusion |
|----------|-----|---------------------|
| Undeciphered Phonetic Readings | 0.30 | Speculative, no Linear B parallel |
| AI-Generated Transliterations | 0.20 | Experimental, unvalidated |

---

## 3 — The Database at a Glance

This database contains **656 inscriptions** drawn from GORILA vols I–V, minor Cretan clay tablet archives, stone libation vessels, non-Cretan Aegean inscriptions, clay sealings, and inscribed ceramics.

![Corpus overview](data/figures/tbl_03_corpus_overview.png)

### Coverage

656 of ~1,400 known inscriptions = **~46.9 %**. Coverage spans the major Cretan archives, individually documented stone vessels, sealings, and several Aegean sites. The remaining gap comprises heavily damaged, poorly documented, or suspected forgery material, plus the many stone vessels, sealings, and ceramics not yet individually encoded.

![Coverage by site](data/figures/fig_06_corpus_coverage.png)

---

## 4 — Geographic Distribution

34 find-sites across Crete, Santorini (Akrotiri/Thera), and other Aegean locations (Kea, Kythera, Miletos) — shown on a real geographic map using Natural Earth 50 m coastline data via geopandas. Hagia Triada remains the largest single archive with ~14 % of the corpus.

> **Note:** The site map plots the **14 sites** that have confirmed WGS-84 coordinates in the coordinate registry. Many other site labels in the corpus (e.g. "Stone Vessels (Crete)", "Sealings (Hagia Triada)") are administrative groupings without independent coordinates and are not individually plotted — they are counted in the site breakdown table but omitted from the geographic map.

![Site breakdown](data/figures/tbl_04_site_breakdown.png)

![Site map](data/figures/fig_03_site_map.png)

Note that the above distribution covers 656 of ~1,400 known inscriptions = ~46.9 %

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

Tablets typically carry **1–16 recognised signs** (average ~7). The distribution is bimodal: clay accounting tablets average 10–13 signs, while sealings and ceramic marks carry just 1–3.

![Signs per tablet](data/figures/fig_05_signs_per_tablet.png)

---

## 7 — Inclusion Strategy & Quality Confidence Scoring

### The Problem

There are roughly **~1,400 known Linear A inscriptions** and this database now covers **656 (~46.9 %)**. Each row is a distinct, individually documented physical object. The remaining ~744 inscriptions (1,400 − 656; note: the 1,400 total is itself a literature estimate, so both figures are approximate) either fall below the QCS threshold or have not yet been individually encoded (stone vessels, sealings, and ceramics beyond those already listed).

### Quality Confidence Score (QCS)

Every potential source is evaluated on **five dimensions** (each 0–1):

| Dimension | Weight | What It Measures |
|---|---|---|
| Transliteration reliability | 30 % | How standardised and peer-reviewed the transliteration is |
| Provenance certainty | 20 % | Confidence in the attributed find-site and archaeological context |
| Publication quality | 25 % | Whether the source appears in GORILA, peer-reviewed journals, or only grey literature |
| Sign completeness | 15 % | Proportion of legible signs vs. damaged, missing, or uncertain |
| Consistency with corpus | 10 % | How well the conventions align with the existing database format |

**QCS = weighted average** of the five scores. The **inclusion threshold is QCS ≥ 0.50**.

### Source Evaluation

![Quality confidence scores](data/figures/fig_07_quality_confidence.png)

### What the Scores Reveal

**Currently included sources (QCS ≥ 0.52):** All five corpus strategy groups pass the 0.5 threshold. The major GORILA archives (Hagia Triada, Khania, Zakros, Phaistos) score 0.90 due to comprehensive publication and standardised transliteration. Stone libation vessels and non-Cretan Aegean inscriptions score 0.62; minor Cretan clay tablets 0.68. Clay sealings (0.55) and inscribed ceramics (0.52) are included with the caveat that they tend to be very short (1–3 signs) and some ceramic marks may be potter's notations rather than true writing.

**Below threshold (QCS < 0.50):**

| Source | ~Inscriptions | QCS | Why Excluded |
|---|---|---|---|
| Metal objects (pins, axes, rings) | 100 | 0.47 | Often single-sign, many from antiquities trade |
| Miscellaneous (labels, weights, graffiti) | 60 | 0.42 | Heterogeneous, very short, heavily damaged |
| Doubtful / possible forgeries | 25 | 0.21 | Suspected fakes — must never be included |

### Decision Rule

```
IF   QCS ≥ 0.50  →  INCLUDE
IF   QCS < 0.50  →  EXCLUDE (too unreliable for systematic analysis)
```

### Current Coverage

At the **QCS ≥ 0.50 threshold**, the database contains **656 inscriptions (~46.9 %)** of all known Linear A texts. Every row corresponds to a unique, individually documented physical object. The remaining ~744 fall below threshold (metal objects, miscellaneous marks, suspected forgeries) or represent stone vessels, sealings, and ceramics not yet individually encoded.

### Priority Actions for Coverage Expansion

| Priority | Action | +Inscriptions | Complexity | Quality Risk |
|---|---|---|---|---|
| 1 | Individually encode remaining stone libation vessels (Za series has ~175 total) | ~110 | Low–Medium | Low |
| 2 | Individually encode Hallager (1996) roundels (HT Wc, ZA Wc, KH Wc series, ~250 total) | ~220 | Medium | Low |
| 3 | Load Younger online corpus (registered, not yet encoded) | ~100 | Low | Low |
| 4 | Individually encode Del Freo & Ferro (2018) ceramic inscriptions (~120 total) | ~100 | Medium | Medium |
| 5 | Encode metal objects with secure provenance | ~50 | Low–Medium | Medium |
| 6 | Per-inscription manual review of miscellaneous marks | ~60 | High | High |

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
| `date_uncertainty_yrs` | Int64 | `100` (NULL if unknown) |
| `material` | str | `clay` / `stone` |
| `source_strategy` | str | `gorila_transliterations` |
| `qcs` | float | `0.90` |
| `is_synthetic` | bool | `False` — all rows represent individually documented physical objects |
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
| 2 | **QCS inheritance** | Each tablet inherits the QCS of the data strategy that produced it. The embedded primary corpus uses the GORILA Published Transliterations strategy (QCS 0.90). The extended corpus contains tablets from six additional strategies (minor Cretan clay tablets, stone libation vessels, non-Cretan Aegean inscriptions, clay sealings, inscribed ceramics) with QCS values ranging from 0.52 to 0.68. |
| 3 | **Coverage** | 46.9 % of ~1,400 known inscriptions. The 1,400 total is a hard-coded literature estimate from GORILA + Younger, not a live reconciliation ledger. The 46.9 % figure should be treated as approximate until a row-by-row inventory table is built. |
| 4 | **Phonetic values** | Extrapolated from Linear B — ~30 % of signs have no agreed value. Treat as hypothetical. (QCS 0.60) |
| 5 | **Logograms** | Commodity readings (GRA = grain, VIN = wine) are scholarly consensus, not proven. (QCS 0.70) |
| 6 | **Dates** | Point estimates only (±50–100 years). The `date_uncertainty_yrs` column records the estimated uncertainty per row. Akrotiri is fixed to 1628 BCE (volcanic destruction). (QCS 0.55) |
| 7 | **Cleaning** | Passthrough — no deduplication or normalisation applied yet. |
| 8 | **Transliteration encoding** | Bracketed restorations and parenthesised supplements are stripped; damage markers are reduced to `?`; pure numerals (quantities) are dropped. This is a known lossy transformation. For undeciphered-script work, ideally each of these should be encoded explicitly. |
| 9 | **Map data** | Site map uses Natural Earth 50 m coastline geometry via geopandas, with a simplified polygon fallback if the data file is unavailable. Only 14 sites have confirmed WGS-84 coordinates; other site labels (e.g. "Stone Vessels (Crete)") are administrative groupings without independent geolocation. |
| 10 | **One entry = one material object** | Every row in the database corresponds to a unique, individually documented physical inscription (tablet, stone vessel, sealing, or ceramic). The previous version contained 570 loop-generated placeholder entries (SV/SEAL/CER series) that cycled fixed formulas over site lists — those have been removed. All remaining rows are individually curated against published sigla. |
| 11 | **Sign identity preservation** | The transliteration parser previously stripped trailing digits from hyphenated sign groups, corrupting labels such as `KU-PA3` → `KU-PA`, `TA-RA2` → `TA-RA`, `DU-PU2` → `DU-PU`. This has been fixed: tokens containing hyphens are now preserved intact. |
| 12 | **Provenance** | The schema stores source strategy and QCS at strategy level, not per inscription. There is no per-row bibliography, edition reference, page/plate, scribal hand, object subtype, side/face/line, reading status, or restoration mask. Scholarly traceability is limited to strategy-level attribution. |
| 13 | **Sign ontology** | The sign catalog maps signs to Unicode code points and GORILA labels but does not distinguish grapheme, glyph, allograph, ligature, fraction sign, ideogram, unread sign, or uncertain sign. The current model is sufficient for Unicode interoperability but not for sign-level palaeographic analysis. |

---

## Sources

- Godart & Olivier (1976–1985). *GORILA*, vols I–V. Paris: Geuthner.
- Younger, J.G. *Linear A Texts in Transliteration* (online).
- Schoep, I. (2002). *The Administration of Neopalatial Crete*. Minos supplement.
- Hallager, E. (1996). *The Minoan Roundel and Other Sealed Documents*.
- Del Freo & Ferro (2018). "Texts and Contexts" – review of inscribed objects.
- Unicode Standard — Linear A block U+10600–U+1077F.
- Natural Earth — Free vector map data at naturalearthdata.com (CC0 licence).

