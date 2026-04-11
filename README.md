# lina_database_builder

**Project Description:** This is an attempt of creating a database of the tablets found identified as the undecyphered Linear A Minoan writing system. 

Below, first the database included on this repository is explored. second the structure and underlying sources & assumptions of the tool are summarized.

This tool loads a curated corpus of Minoan Linear A tablet transcriptions, converts each tablet to Unicode Linear A characters, saves the database in both CSV and XLSX format, and produces a set of self-contained summary statistics and visualisations — all at the click of a button via `python main.py`.


---

## Project structure

```
lina_database_builder/
├── main.py                      Entry point — run this to execute the full pipeline
├── model.py                     Orchestrator (LinaBaseBuilder.run())
├── builder_lina_loader.py       Component 1 – loads corpus, builds DataFrame
├── builder_lina_cleaner.py      Component 2 – passthrough placeholder for data cleaning
├── builder_lina_stats.py        Component 3 – statistics, PNG figures and tables
├── builder_lina_saver.py        Component 4 – saves CSVs and assembles xlsx report
├── lina_sign_catalog.py         Sign catalog (341 Unicode Linear A signs) + converters
├── lina_corpus_embedded.py      Embedded seed corpus (48 tablets, 9 Cretan sites)
├── lina_site_coordinates.py     WGS-84 coordinates for each find-site + map outlines
├── requirements.txt             Python dependencies
└── data/                        Generated output (created on first run)
    ├── lina_database_raw.csv    Raw corpus as CSV
    ├── lina_database_clean.csv  Cleaned corpus as CSV (identical to raw for now)
    ├── lina_report.xlsx         Multi-tab xlsx report (databases + all figures)
    └── figures/                 Individual PNG figures and table images
        ├── tbl_01_catalog_overview.png
        ├── tbl_02_sign_group_types.png
        ├── fig_01_catalog_categories.png
        ├── fig_02_sign_group_frequencies.png
        ├── tbl_03_corpus_overview.png
        ├── tbl_04_site_breakdown.png
        ├── fig_03_site_map.png
        ├── fig_04_timeline.png
        └── fig_05_signs_per_tablet.png
```

---

## How to run

```bash
pip install -r requirements.txt
python main.py
```

All outputs are written to the `data/` directory.

---

## Major functions

### `lina_sign_catalog.py`
| Function | Description |
|---|---|
| `build_sign_catalog()` | Returns list of 341 sign dicts derived from Python's `unicodedata` (Unicode block U+10600–U+1077F). Each dict contains sign_label, category, char, codepoint, hex_code, unicode_name. |
| `build_label_to_char_map()` | Dict mapping GORILA sign label (e.g. `AB001`) to Unicode character. |
| `build_char_to_id_map()` | Dict mapping Unicode character to numeric sign ID (cp − 0x10600). |
| `parse_sign_groups(transliteration)` | Tokenises a transliteration string into sign-group tokens (whitespace-delimited, numerics dropped). |
| `sign_group_to_unicode(group, label_map)` | Converts one sign group (e.g. `KU-RO`) to a Unicode Linear A string. |
| `transliteration_to_unicode_string(transliteration, label_map)` | Converts a full tablet transliteration to a space-segmented Unicode Linear A string. |

### `lina_site_coordinates.py`
| Name | Description |
|---|---|
| `SITE_COORDINATES` | Dict of WGS-84 coordinates (lat, lon) for all 9 Cretan find-sites. |
| `CRETE_OUTLINE`, `GREECE_OUTLINE`, `TURKEY_W_OUTLINE` | Simplified coastline polygon coordinates used for the map figure. |
| `get_site_summary_df(corpus_df)` | Joins tablet counts, material breakdown and date range to site coordinates. |

### `builder_lina_loader.py`
| Function | Description |
|---|---|
| `load_data(data_dir)` | Builds the catalog, loads the embedded corpus, converts transliterations to Unicode and returns the canonical 10-column DataFrame. |

### `builder_lina_stats.py`
| Function | Description |
|---|---|
| `report_stats(df)` | Main entry point: prints statistics, generates all 9 PNGs, returns list of `(tab_name, title, path)` for xlsx assembly. |
| `_tbl_catalog_overview()` | Table PNG: sign counts by category. |
| `_tbl_sign_group_types()` | Table PNG: sign group type taxonomy from GORILA literature. |
| `_fig_catalog_categories()` | Pie chart: sign category proportions. |
| `_fig_sign_group_frequencies()` | Horizontal bar: top-15 sign groups, colour-coded by functional type. |
| `_tbl_corpus_overview()` | Table PNG: headline corpus statistics. |
| `_tbl_site_breakdown()` | Table PNG: tablets per find-site with coordinates and date range. |
| `_fig_site_map()` | Map of Crete and Aegean showing site locations (no external data needed). |
| `_fig_timeline()` | Scatter of tablets by estimated date × site, distinguishing clay and stone. |
| `_fig_signs_per_tablet()` | Histogram of sign count per tablet with mean/median lines. |

### `builder_lina_saver.py`
| Function | Description |
|---|---|
| `save_data(df, output_path)` | Saves a DataFrame as CSV. |
| `save_report(raw_df, clean_df, catalog, figures, xlsx_path)` | Assembles the multi-tab xlsx report: three formatted DataFrame tabs (raw DB, clean DB, sign catalog) followed by one tab per PNG figure. |

---

## Inputs and outputs

**Inputs**
- No external data required. The corpus is fully embedded in `lina_corpus_embedded.py`.
- Future: `_lina_scraper()` in `builder_lina_loader.py` can be extended to pull from online corpora (DĀMOS, Younger's corpus).

**Outputs**
| File | Contents |
|---|---|
| `data/lina_database_raw.csv` | Full corpus DataFrame (48 tablets × 10 columns) |
| `data/lina_database_clean.csv` | Identical to raw (cleaning is a passthrough for now) |
| `data/lina_report.xlsx` | 12-tab xlsx: Raw Database, Clean Database, Sign Catalog, + 9 figure/table tabs |
| `data/figures/*.png` | Individual PNG for each figure and formatted table |

**DataFrame columns**
| Column | Type | Description |
|---|---|---|
| `tablet_id` | str | GORILA reference (e.g. `HT 1`) |
| `site` | str | Find-site name |
| `date_est` | Int64 | Approximate BCE date (stored as negative integer) |
| `material` | str | `clay` or `stone` |
| `transliteration` | str | Scholarly transliteration string |
| `sign_groups` | str | Pipe-separated sign group tokens (e.g. `A-DU\|GRA\|KU-RO`) |
| `sign_sequence_unicode` | str | Space-separated Unicode Linear A string |
| `sign_sequence_ids` | str | Comma-separated sign IDs (codepoint − 0x10600) |
| `sign_group_count` | int | Number of sign groups per tablet |
| `sign_count` | int | Number of recognised individual signs per tablet |

---

## Dependencies

```
pandas          – DataFrame operations
matplotlib      – all figures and table PNGs
seaborn         – imported (available for future use)
openpyxl        – xlsx assembly
Pillow          – image handling for xlsx embedding
geopandas       – site coordinate utilities (optional; map uses built-in polygons)
geodatasets     – Natural Earth data (used if internet access is available)
requests        – HTTP utilities (future scraper)
```

---

## Literature consulted

- Godart, L. & Olivier, J.-P. (1976–1985). *GORILA* (Recueil des inscriptions en linéaire A), vols I–V. Paris: Geuthner. — Primary reference for tablet transliterations, sign numbering and site provenances.
- Younger, J.G. *Linear A Texts in Transliteration* (online corpus). — Source for transliteration conventions and additional tablet records.
- Unicode Standard, Chapter 10: South Asian Scripts. *Linear A block U+10600–U+1077F* — authoritative sign list and codepoint assignments.
- Hooker, J.T. (1990). *Reading the Past: Linear B and Related Scripts*. London: British Museum Press. — Background on Aegean scripts and the AB-numbering convention shared with Linear B.
- Packard, D.W. (1974). *Minoan Linear A*. Berkeley: UC Press. — Early systematic treatment of the sign inventory.

---

## Core assumptions

### Sign catalog
- All 341 signs in Unicode block U+10600–U+1077F are included. No signs have been added or removed.
- The category assignments (syllabic, logographic, numeric_fraction) are derived purely from the GORILA sign-label prefixes (AB vs. A3xx vs. A7xx). The Unicode Standard itself does not label functional categories.
- Phonetic values assigned in `PHONETIC_TO_SIGN_LABEL` follow the Linear B correspondence convention, which is widely used in scholarship but not definitively proven for Linear A.

### Corpus (embedded dataset)
- The 48 tablets are a representative sample drawn from the main published corpora. They cover the most-studied sites and document types (administrative clay tablets and stone libation formulae). They are **not** an exhaustive record of all ~1,500 known Linear A inscriptions.
- Date estimates are approximate centuries (e.g. −1500 for all HT clay tablets) rather than precise dates. Real tablets often lack secure stratigraphy.
- Transliterations follow GORILA conventions but have been simplified for machine readability: damage markers (lacunae, brackets) are stripped, and numeric quantities are dropped during tokenisation.

### Geographic coordinates
- Coordinates are approximate centroids for each site, accurate to ±0.1°. They are sufficient for the map figure but should not be used for precise spatial analysis.
- The coastline polygons (Crete, Greece, Turkey) are manually simplified; they are suitable for visualisation at ~1:2 000 000 scale only.

### Weaknesses and areas of low scientific confidence
| Area | Issue |
|---|---|
| Phonetic values | Most Linear A phonetic assignments are extrapolated from Linear B; ~30% of signs have no agreed value. The `PHONETIC_TO_SIGN_LABEL` mapping should be treated as hypothetical. |
| Logogram-to-commodity mapping | Commodity logograms (GRA = grain, VIN = wine, etc.) are consensus readings but not fully proven; a minority of scholars dispute some identifications. |
| Corpus completeness | 48 tablets represent ~3% of the known Linear A corpus. Statistics derived from this sample may not generalise. |
| Date estimates | All BCE dates are broad estimates (±50–100 years); the corpus shows limited temporal variation by design. |
| Cleaning pipeline | The cleaner is a passthrough. No deduplication, normalisation or error-correction has been applied. |

