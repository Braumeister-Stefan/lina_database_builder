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
├── lina_corpus_embedded.py      Embedded corpus (317 tablets, 14 sites)
├── lina_site_coordinates.py     WGS-84 coordinates for each find-site + map outlines
└── requirements.txt             Python dependencies
```

---

## How to run

```bash
pip install -r requirements.txt
python main.py
```

All outputs are written to the `data/` directory (`data/lina_database_raw.csv`, `data/lina_database_clean.csv`, `data/lina_report.xlsx`, `data/figures/*.png`).

---

## Database description

### Sign catalog

The sign catalog is derived directly from Python's built-in `unicodedata` module — every character in Unicode block U+10600–U+1077F that carries a `LINEAR A SIGN …` name is included, giving **341 signs** split across three functional categories.

![Sign catalog overview](data/figures/tbl_01_catalog_overview.png)

![Sign category pie chart](data/figures/fig_01_catalog_categories.png)

Signs in the **syllabic** category (AB-series, 81 signs) carry phonetic values extrapolated from the parallel Linear B script. **Logographic** signs (A-series, 230 signs) represent objects, commodities and administrative concepts. **Numeric/fraction** signs (30 signs) encode quantities.

---

### Sign group types

Linear A tablets use a small number of recurring sign group patterns. The table below summarises the functional taxonomy used throughout this database.

![Sign group types](data/figures/tbl_02_sign_group_types.png)

---

### Corpus overview

The embedded corpus currently contains **317 inscriptions** across **14 find-sites**, drawn from GORILA vols I–V and Younger's online corpus. This represents approximately **22.6 %** of the ~1,400 known Linear A inscriptions.

![Corpus overview statistics](data/figures/tbl_03_corpus_overview.png)

---

### Coverage vs total known corpus

The chart below shows how many inscriptions from each site are in this database versus the total published count. Sites for which the full known record is encoded appear at 100 %. The large **Other / unassigned** category (stone vessels, sealings, nodules, minor Aegean sites) is not yet in scope.

![Corpus coverage](data/figures/fig_06_corpus_coverage.png)

---

### Tablets by find-site

![Site breakdown table](data/figures/tbl_04_site_breakdown.png)

![Site map](data/figures/fig_03_site_map.png)

All 13 Cretan sites lie within the island. Akrotiri (Thera / Santorini) plots north of Crete in the Aegean. Circle size on the map is proportional to tablet count.

---

### Temporal distribution

Each point below represents one tablet. The x-axis shows approximate BCE date (older to the left); rows are ordered by median date. Khania (KH) stands out as the **latest** Linear A archive (~1350 BCE, LM IIIB), post-dating most Cretan archives by over a century.

![Timeline](data/figures/fig_04_timeline.png)

---

### Sign group frequency

The 15 most frequent sign groups in the corpus, colour-coded by functional type. **GRA** (grain logogram) and **KU-RO** (grand total) dominate, reflecting the administrative accounting nature of most clay tablets. Personal names such as **A-DU**, **KU-PA3-NU** and **DA-QE-RA** rank among the top syllabic entries.

![Sign group frequencies](data/figures/fig_02_sign_group_frequencies.png)

---

### Distribution of signs per tablet

Most tablets carry between **8 and 13** recognised signs. The relatively narrow distribution reflects the formulaic nature of the administrative record (personal name + commodity logogram + quantity, closed by KU-RO). Stone libation formulae, which carry fewer but longer sign groups, pull the lower tail.

![Signs per tablet histogram](data/figures/fig_05_signs_per_tablet.png)

---

## DataFrame schema

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

## Major functions

### `lina_sign_catalog.py`
| Function | Description |
|---|---|
| `build_sign_catalog()` | Returns list of 341 sign dicts (sign_label, category, char, codepoint, hex_code, unicode_name). |
| `build_label_to_char_map()` | Dict mapping GORILA sign label (e.g. `AB001`) to Unicode character. |
| `build_char_to_id_map()` | Dict mapping Unicode character to numeric sign ID (cp − 0x10600). |
| `parse_sign_groups(transliteration)` | Tokenises a transliteration string into sign-group tokens; drops numerics and damage markers. |
| `sign_group_to_unicode(group, label_map)` | Converts one sign group (e.g. `KU-RO`) to a Unicode Linear A string. |

### `lina_site_coordinates.py`
| Name | Description |
|---|---|
| `SITE_COORDINATES` | WGS-84 coordinates (lat, lon) for all 14 find-sites. |
| `CRETE_OUTLINE`, `GREECE_OUTLINE`, `TURKEY_W_OUTLINE` | Simplified coastline polygons for the map figure. |
| `get_site_summary_df(corpus_df)` | Joins tablet counts, material breakdown and date range to site coordinates. |

### `builder_lina_loader.py`
| Function | Description |
|---|---|
| `load_data(data_dir)` | Builds the catalog, loads the embedded corpus, converts transliterations to Unicode and returns the canonical 10-column DataFrame. |

### `builder_lina_stats.py`
| Function | Description |
|---|---|
| `report_stats(df)` | Main entry point: prints statistics, generates all 10 PNGs, returns list of `(tab_name, title, path)` for xlsx assembly. |

### `builder_lina_saver.py`
| Function | Description |
|---|---|
| `save_data(df, output_path)` | Saves a DataFrame as CSV. |
| `save_report(raw_df, clean_df, catalog, figures, xlsx_path)` | Assembles the 13-tab xlsx report. |

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
- Category assignments (syllabic, logographic, numeric_fraction) are derived purely from GORILA sign-label prefixes (AB vs. A3xx vs. A7xx). The Unicode Standard itself does not label functional categories.
- Phonetic values assigned in `PHONETIC_TO_SIGN_LABEL` follow the Linear B correspondence convention, which is widely used in scholarship but not definitively proven for Linear A.

### Corpus (embedded dataset)
- The **317 tablets** cover 14 find-sites (13 Cretan + Akrotiri/Thera) and represent the most-studied sites and document types (administrative clay tablets and stone libation formulae). They are **not** an exhaustive record of all ~1,400 known Linear A inscriptions (~22.6% coverage).
- Date estimates are approximate centuries (e.g. −1500 for most HT clay tablets) rather than precise dates. Real tablets often lack secure stratigraphy.
- Transliterations follow GORILA conventions but have been simplified for machine readability: damage markers (lacunae, brackets) are stripped, and numeric quantities are dropped during tokenisation.
- **Damage markers stripped**: Lacunae `[ ]`, restored readings `( )`, and uncertain sign-dots are removed before tokenisation. Partially preserved tablets are included using surviving sign-groups only.
- **Multi-sided tablets encoded separately**: Tablets with distinct a/b sides would be encoded as separate rows (e.g. `HT 31a`, `HT 31b`); no multi-sided tablets are present in the current sample.
- **Unresolved star-notation signs**: Signs with no Unicode mapping are excluded from sign counts but retained in the raw transliteration string.
- **Akrotiri date fixed to −1628 BCE**: The volcanic destruction horizon provides the only absolute date in the entire Linear A corpus; all Akrotiri inscriptions use this terminus ante quem.
- **Minor sites included individually**: Sites with fewer than 5 inscriptions (Nirou Khani, Apodioulou) are labelled individually in the DB; summary visualisations may pool them in an "Other" category as needed.

### Geographic coordinates
- Coordinates are approximate centroids for each site, accurate to ±0.1°. They are sufficient for the map figure but should not be used for precise spatial analysis.
- The coastline polygons (Crete, Greece, Turkey) are manually simplified; they are suitable for visualisation at ~1:2 000 000 scale only.
- Akrotiri (Santorini/Thera) plots north of Crete in the Aegean Sea area on the map, outside the Cretan landmass.

### Weaknesses and areas of low scientific confidence
| Area | Issue |
|---|---|
| Phonetic values | Most Linear A phonetic assignments are extrapolated from Linear B; ~30% of signs have no agreed value. The `PHONETIC_TO_SIGN_LABEL` mapping should be treated as hypothetical. |
| Logogram-to-commodity mapping | Commodity logograms (GRA = grain, VIN = wine, etc.) are consensus readings but not fully proven; a minority of scholars dispute some identifications. |
| Corpus completeness | 317 tablets represent ~22.6% of the known Linear A corpus (~1,400 inscriptions). Statistics derived from this sample may not fully generalise to the complete corpus, particularly for rare sign groups and minor sites. |
| Date estimates | All BCE dates are broad estimates (±50–100 years); the corpus shows limited temporal variation by design. |
| KH transliteration conventions | Khania (LM IIIB, ~1350 BCE) tablets use a higher proportion of unidentified signs. KH-specific personal names (KA-PA, DU-WA-TO, SE-TO-I-JA, etc.) are drawn from the GORILA record; some assignments remain debated. |
| Cleaning pipeline | The cleaner is a passthrough. No deduplication, normalisation or error-correction has been applied. |

