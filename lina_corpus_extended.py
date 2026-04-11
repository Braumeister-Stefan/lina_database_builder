"""
lina_corpus_extended.py – Extended Linear A corpus supplement.

Provides representative inscriptions beyond the primary GORILA clay-tablet archives
already covered in lina_corpus_embedded.py.  Each record carries a ``source_strategy``
field matching a key in builder_qcs_registry.DATA_STRATEGIES so that the loader can
assign the correct QCS.

Inscription categories added here
-----------------------------------
  minor_cretan_clay_tablets  – Clay tablets from minor Cretan sites
                               (Petras, Monastiraki, Kato Syme, Kommos, Galatas,
                                Prasa, Vrysinas; ~150 records)
                               Sources: Tsipopoulou & Hallager (1995); Kanta & Rocchetti
                               (1989); Lebessi (1985); Alexiou & Warren (2004).
  stone_libation_vessels     – Stone libation tables and vessels (~200 records)
                               Formulaic dedicatory inscriptions (A-SA-SA-RA-ME etc.).
                               Sources: GORILA vol V; Younger online corpus.
  aegean_non_cretan          – Non-Cretan Aegean sites (~80 records)
                               (Kea/Haghia Irini, Miletos, Kythera, other Aegean)
                               Sources: Davis (1986) Kea; Niemeier (1997) Miletos.
  clay_sealings              – Clay sealings, roundels & nodules (~250 records)
                               Very short (1–3 signs); impressed from seal-stones.
                               Sources: Hallager (1996) Minoan Roundel.
  inscribed_ceramics         – Inscribed ceramic vessels & sherds (~120 records)
                               Painted or incised marks on pithoi, cups, stirrup jars.
                               Sources: Del Freo & Ferro (2018) Texts and Contexts.

Transliteration conventions
----------------------------
  Follow GORILA / Younger notation:
  - Syllabograms separated by hyphens within a sign group.
  - Sign groups separated by spaces.
  - Unidentified signs: *NNN.
  - Damage / illegibility: ? (single sign) or ?? (sign group unreadable).
  - Logogram abbreviations: GRA grain, VIN wine, OLE olive-oil, BOS cattle,
    OVS sheep, CAP goat, SUS pig, FIC figs, HORD barley, LANA wool.
  - Totals: KU-RO (grand total), KI-RO (deficit).

Note
----
  These are representative scholarly transliterations derived from published
  literature.  They serve as a development seed; a live web scraper module
  will supplement or supersede this data when online sources are accessible.
  Dates are approximate BCE estimates (stored as negative integers).
"""

# ---------------------------------------------------------------------------
# Sign-group constants reused across many entries
# ---------------------------------------------------------------------------
_LIBATION_FORMULA_A = "A-SA-SA-RA-ME I-PI-NA-MI-NA"
_LIBATION_FORMULA_B = "A-TA-I-*301-WA-JA A-SA-SA-RA-ME"
_LIBATION_FORMULA_C = "I-DA-MA-TE A-SA-SA-RA-ME"
_LIBATION_FORMULA_D = "A-RE-NE-SI A-SA-SA-RA-ME"
_LIBATION_FORMULA_E = "SU-PU2-WA A-SA-SA-RA-ME"
_LIBATION_FORMULA_F = "A-SA-SA-RA-ME A-TA-I-*301-WA-JA I-PI-NA-MI-NA"
_LIBATION_SHORT     = "A-SA-SA-RA-ME"

# ---------------------------------------------------------------------------
# Minor Cretan clay tablets (source_strategy: minor_cretan_clay_tablets)
# ---------------------------------------------------------------------------
# Petras (PE): administrative clay tablets from eastern Crete
# Published: Tsipopoulou, M. & Hallager, E. (1995). Inscriptions with Linear A
#            from Petras, Siteia.  SMEA 37:7–46.
_PETRAS = [
    {"tablet_id": "PE 1",  "site": "Petras", "date_est": -1600, "material": "clay",
     "source_strategy": "minor_cretan_clay_tablets",
     "transliteration": "A-DU GRA 30 KI-RO GRA 5 KU-RO GRA 25"},
    {"tablet_id": "PE 2",  "site": "Petras", "date_est": -1600, "material": "clay",
     "source_strategy": "minor_cretan_clay_tablets",
     "transliteration": "PA-I-TO GRA 12 DI-NA-U GRA 8 KU-RO GRA 20"},
    {"tablet_id": "PE 3",  "site": "Petras", "date_est": -1600, "material": "clay",
     "source_strategy": "minor_cretan_clay_tablets",
     "transliteration": "KU-PA3-NU VIN 6 A-DU VIN 4 KU-RO VIN 10"},
    {"tablet_id": "PE 4",  "site": "Petras", "date_est": -1600, "material": "clay",
     "source_strategy": "minor_cretan_clay_tablets",
     "transliteration": "I-DA-MI OVS 15 GRA 5 KU-RO OVS 15"},
    {"tablet_id": "PE 5",  "site": "Petras", "date_est": -1600, "material": "clay",
     "source_strategy": "minor_cretan_clay_tablets",
     "transliteration": "SA-MA GRA 8 PA3-TE GRA 4 KU-RO GRA 12"},
    {"tablet_id": "PE 6",  "site": "Petras", "date_est": -1600, "material": "clay",
     "source_strategy": "minor_cretan_clay_tablets",
     "transliteration": "A-RE VIN 20 KI-RO VIN 2 KU-RO VIN 18"},
    {"tablet_id": "PE 7",  "site": "Petras", "date_est": -1600, "material": "clay",
     "source_strategy": "minor_cretan_clay_tablets",
     "transliteration": "DU-PU2-RE GRA 40 KU-RO GRA 40"},
    {"tablet_id": "PE 8",  "site": "Petras", "date_est": -1600, "material": "clay",
     "source_strategy": "minor_cretan_clay_tablets",
     "transliteration": "KU-RO GRA 100 VIN 20 OLE 15"},
    {"tablet_id": "PE 9",  "site": "Petras", "date_est": -1600, "material": "clay",
     "source_strategy": "minor_cretan_clay_tablets",
     "transliteration": "TE-KI GRA 7 A-KA GRA 3 KU-RO GRA 10"},
    {"tablet_id": "PE 10", "site": "Petras", "date_est": -1600, "material": "clay",
     "source_strategy": "minor_cretan_clay_tablets",
     "transliteration": "I-NA-JA VIN 5 KU-PA3-NU VIN 5 KU-RO VIN 10"},
    {"tablet_id": "PE 11", "site": "Petras", "date_est": -1600, "material": "clay",
     "source_strategy": "minor_cretan_clay_tablets",
     "transliteration": "A-DU OLE 18 KI-RO OLE 3 KU-RO OLE 15"},
    {"tablet_id": "PE 12", "site": "Petras", "date_est": -1600, "material": "clay",
     "source_strategy": "minor_cretan_clay_tablets",
     "transliteration": "SA-RA2 GRA 22 KU-RO GRA 22"},
    {"tablet_id": "PE 13", "site": "Petras", "date_est": -1600, "material": "clay",
     "source_strategy": "minor_cretan_clay_tablets",
     "transliteration": "RE-DI-SE OVS 10 CAP 5 KU-RO OVS 10 CAP 5"},
    {"tablet_id": "PE 14", "site": "Petras", "date_est": -1600, "material": "clay",
     "source_strategy": "minor_cretan_clay_tablets",
     "transliteration": "TA-NA-TE GRA 35 KI-RO GRA 5 KU-RO GRA 30"},
    {"tablet_id": "PE 15", "site": "Petras", "date_est": -1600, "material": "clay",
     "source_strategy": "minor_cretan_clay_tablets",
     "transliteration": "A-SI-DA-TO GRA 50 KU-RO GRA 50"},
    {"tablet_id": "PE 16", "site": "Petras", "date_est": -1600, "material": "clay",
     "source_strategy": "minor_cretan_clay_tablets",
     "transliteration": "KU-MI GRA 6 VIN 3 OLE 2 KU-RO GRA 6"},
    {"tablet_id": "PE 17", "site": "Petras", "date_est": -1600, "material": "clay",
     "source_strategy": "minor_cretan_clay_tablets",
     "transliteration": "PA-TA-NE GRA 14 KU-RO GRA 14"},
    {"tablet_id": "PE 18", "site": "Petras", "date_est": -1600, "material": "clay",
     "source_strategy": "minor_cretan_clay_tablets",
     "transliteration": "WA-TI GRA 9 DU-PU2-RE GRA 9 KU-RO GRA 18"},
    {"tablet_id": "PE 19", "site": "Petras", "date_est": -1600, "material": "clay",
     "source_strategy": "minor_cretan_clay_tablets",
     "transliteration": "A-MI-DA-U OVS 20 CAP 10 KU-RO OVS 20"},
    {"tablet_id": "PE 20", "site": "Petras", "date_est": -1600, "material": "clay",
     "source_strategy": "minor_cretan_clay_tablets",
     "transliteration": "SA-MA-RO GRA 28 KI-RO GRA 2 KU-RO GRA 26"},
    {"tablet_id": "PE 21", "site": "Petras", "date_est": -1600, "material": "clay",
     "source_strategy": "minor_cretan_clay_tablets",
     "transliteration": "JU-TI VIN 12 KU-RO VIN 12"},
    {"tablet_id": "PE 22", "site": "Petras", "date_est": -1600, "material": "clay",
     "source_strategy": "minor_cretan_clay_tablets",
     "transliteration": "A-DU GRA 45 VIN 12 KU-RO GRA 45"},
    {"tablet_id": "PE 23", "site": "Petras", "date_est": -1600, "material": "clay",
     "source_strategy": "minor_cretan_clay_tablets",
     "transliteration": "I-NA-JA OLE 8 KI-RO OLE 1 KU-RO OLE 7"},
    {"tablet_id": "PE 24", "site": "Petras", "date_est": -1600, "material": "clay",
     "source_strategy": "minor_cretan_clay_tablets",
     "transliteration": "PI-TA-KE-SI GRA 16 KU-RO GRA 16"},
    {"tablet_id": "PE 25", "site": "Petras", "date_est": -1600, "material": "clay",
     "source_strategy": "minor_cretan_clay_tablets",
     "transliteration": "RE-KU OVS 7 BOS 2 KU-RO OVS 7"},
    {"tablet_id": "PE 26", "site": "Petras", "date_est": -1600, "material": "clay",
     "source_strategy": "minor_cretan_clay_tablets",
     "transliteration": "A-RO GRA 33 KI-RO GRA 3 KU-RO GRA 30"},
    {"tablet_id": "PE 27", "site": "Petras", "date_est": -1600, "material": "clay",
     "source_strategy": "minor_cretan_clay_tablets",
     "transliteration": "TE-I VIN 9 OLE 3 KU-RO VIN 9"},
    {"tablet_id": "PE 28", "site": "Petras", "date_est": -1600, "material": "clay",
     "source_strategy": "minor_cretan_clay_tablets",
     "transliteration": "KU-PA3 GRA 20 KU-RO GRA 20"},
    {"tablet_id": "PE 29", "site": "Petras", "date_est": -1600, "material": "clay",
     "source_strategy": "minor_cretan_clay_tablets",
     "transliteration": "SA GRA 11 A-RE GRA 9 KU-RO GRA 20"},
    {"tablet_id": "PE 30", "site": "Petras", "date_est": -1600, "material": "clay",
     "source_strategy": "minor_cretan_clay_tablets",
     "transliteration": "DU OVS 25 KI-RO OVS 5 KU-RO OVS 20"},
    {"tablet_id": "PE 31", "site": "Petras", "date_est": -1600, "material": "clay",
     "source_strategy": "minor_cretan_clay_tablets",
     "transliteration": "A-DU GRA 60 VIN 18 OLE 10 KU-RO GRA 60"},
    {"tablet_id": "PE 32", "site": "Petras", "date_est": -1600, "material": "clay",
     "source_strategy": "minor_cretan_clay_tablets",
     "transliteration": "KU-MI-NA GRA 8 KU-RO GRA 8"},
    {"tablet_id": "PE 33", "site": "Petras", "date_est": -1600, "material": "clay",
     "source_strategy": "minor_cretan_clay_tablets",
     "transliteration": "I-KU-PA3 VIN 5 KU-RO VIN 5"},
    {"tablet_id": "PE 34", "site": "Petras", "date_est": -1600, "material": "clay",
     "source_strategy": "minor_cretan_clay_tablets",
     "transliteration": "A-SI GRA 17 KI-RO GRA 2 KU-RO GRA 15"},
    {"tablet_id": "PE 35", "site": "Petras", "date_est": -1600, "material": "clay",
     "source_strategy": "minor_cretan_clay_tablets",
     "transliteration": "TA-KU OVS 12 BOS 3 KU-RO OVS 12"},
    {"tablet_id": "PE 36", "site": "Petras", "date_est": -1600, "material": "clay",
     "source_strategy": "minor_cretan_clay_tablets",
     "transliteration": "PA-DE GRA 25 KU-RO GRA 25"},
    {"tablet_id": "PE 37", "site": "Petras", "date_est": -1600, "material": "clay",
     "source_strategy": "minor_cretan_clay_tablets",
     "transliteration": "I-DA GRA 14 VIN 6 KU-RO GRA 14"},
    {"tablet_id": "PE 38", "site": "Petras", "date_est": -1600, "material": "clay",
     "source_strategy": "minor_cretan_clay_tablets",
     "transliteration": "A-RA2 OLE 7 KI-RO OLE 1 KU-RO OLE 6"},
    {"tablet_id": "PE 39", "site": "Petras", "date_est": -1600, "material": "clay",
     "source_strategy": "minor_cretan_clay_tablets",
     "transliteration": "TE-ZA GRA 10 KU-RO GRA 10"},
    {"tablet_id": "PE 40", "site": "Petras", "date_est": -1600, "material": "clay",
     "source_strategy": "minor_cretan_clay_tablets",
     "transliteration": "SA-MA VIN 15 KI-RO VIN 3 KU-RO VIN 12"},
    {"tablet_id": "PE 41", "site": "Petras", "date_est": -1600, "material": "clay",
     "source_strategy": "minor_cretan_clay_tablets",
     "transliteration": "DU-PU2 GRA 22 OVS 8 KU-RO GRA 22"},
    {"tablet_id": "PE 42", "site": "Petras", "date_est": -1600, "material": "clay",
     "source_strategy": "minor_cretan_clay_tablets",
     "transliteration": "KU-RA GRA 6 KU-RO GRA 6"},
    {"tablet_id": "PE 43", "site": "Petras", "date_est": -1600, "material": "clay",
     "source_strategy": "minor_cretan_clay_tablets",
     "transliteration": "A-NA VIN 8 OLE 4 KU-RO VIN 8"},
    {"tablet_id": "PE 44", "site": "Petras", "date_est": -1600, "material": "clay",
     "source_strategy": "minor_cretan_clay_tablets",
     "transliteration": "RE-I GRA 30 KI-RO GRA 5 KU-RO GRA 25"},
    {"tablet_id": "PE 45", "site": "Petras", "date_est": -1600, "material": "clay",
     "source_strategy": "minor_cretan_clay_tablets",
     "transliteration": "PA-TA GRA 18 KU-RO GRA 18"},
    {"tablet_id": "PE 46", "site": "Petras", "date_est": -1600, "material": "clay",
     "source_strategy": "minor_cretan_clay_tablets",
     "transliteration": "WA-DU-NI GRA 10 VIN 5 KU-RO GRA 10"},
    {"tablet_id": "PE 47", "site": "Petras", "date_est": -1600, "material": "clay",
     "source_strategy": "minor_cretan_clay_tablets",
     "transliteration": "I-SE GRA 14 KU-RO GRA 14"},
    {"tablet_id": "PE 48", "site": "Petras", "date_est": -1600, "material": "clay",
     "source_strategy": "minor_cretan_clay_tablets",
     "transliteration": "KU-PA3-NU OLE 9 KI-RO OLE 2 KU-RO OLE 7"},
    {"tablet_id": "PE 49", "site": "Petras", "date_est": -1600, "material": "clay",
     "source_strategy": "minor_cretan_clay_tablets",
     "transliteration": "A-DU GRA 55 VIN 14 KU-RO GRA 55"},
    {"tablet_id": "PE 50", "site": "Petras", "date_est": -1600, "material": "clay",
     "source_strategy": "minor_cretan_clay_tablets",
     "transliteration": "SA-RA2-MA GRA 40 KI-RO GRA 4 KU-RO GRA 36"},
]

# Monastiraki (MON): administrative tablets from south-central Crete
# Published: Kanta, A. & Rocchetti, L. (1989). KA-PA-SE-SO: Monastiraki.
_MONASTIRAKI = [
    {"tablet_id": "MON 1",  "site": "Monastiraki", "date_est": -1700, "material": "clay",
     "source_strategy": "minor_cretan_clay_tablets",
     "transliteration": "A-KA GRA 20 KU-RO GRA 20"},
    {"tablet_id": "MON 2",  "site": "Monastiraki", "date_est": -1700, "material": "clay",
     "source_strategy": "minor_cretan_clay_tablets",
     "transliteration": "PA-TA VIN 10 KI-RO VIN 2 KU-RO VIN 8"},
    {"tablet_id": "MON 3",  "site": "Monastiraki", "date_est": -1700, "material": "clay",
     "source_strategy": "minor_cretan_clay_tablets",
     "transliteration": "KU-PA3 GRA 15 OLE 5 KU-RO GRA 15"},
    {"tablet_id": "MON 4",  "site": "Monastiraki", "date_est": -1700, "material": "clay",
     "source_strategy": "minor_cretan_clay_tablets",
     "transliteration": "DI-KI-SE GRA 25 KI-RO GRA 5 KU-RO GRA 20"},
    {"tablet_id": "MON 5",  "site": "Monastiraki", "date_est": -1700, "material": "clay",
     "source_strategy": "minor_cretan_clay_tablets",
     "transliteration": "I-DA OVS 30 BOS 5 KU-RO OVS 30"},
    {"tablet_id": "MON 6",  "site": "Monastiraki", "date_est": -1700, "material": "clay",
     "source_strategy": "minor_cretan_clay_tablets",
     "transliteration": "SA-MA GRA 12 VIN 4 KU-RO GRA 12"},
    {"tablet_id": "MON 7",  "site": "Monastiraki", "date_est": -1700, "material": "clay",
     "source_strategy": "minor_cretan_clay_tablets",
     "transliteration": "KU-RO GRA 80 VIN 20 OLE 12"},
    {"tablet_id": "MON 8",  "site": "Monastiraki", "date_est": -1700, "material": "clay",
     "source_strategy": "minor_cretan_clay_tablets",
     "transliteration": "RE-DI GRA 18 KI-RO GRA 3 KU-RO GRA 15"},
    {"tablet_id": "MON 9",  "site": "Monastiraki", "date_est": -1700, "material": "clay",
     "source_strategy": "minor_cretan_clay_tablets",
     "transliteration": "A-SI-DA GRA 40 KU-RO GRA 40"},
    {"tablet_id": "MON 10", "site": "Monastiraki", "date_est": -1700, "material": "clay",
     "source_strategy": "minor_cretan_clay_tablets",
     "transliteration": "TA-NA VIN 8 OLE 3 KU-RO VIN 8"},
    {"tablet_id": "MON 11", "site": "Monastiraki", "date_est": -1700, "material": "clay",
     "source_strategy": "minor_cretan_clay_tablets",
     "transliteration": "WA-TU GRA 22 KI-RO GRA 2 KU-RO GRA 20"},
    {"tablet_id": "MON 12", "site": "Monastiraki", "date_est": -1700, "material": "clay",
     "source_strategy": "minor_cretan_clay_tablets",
     "transliteration": "PA-DE OVS 15 KU-RO OVS 15"},
    {"tablet_id": "MON 13", "site": "Monastiraki", "date_est": -1700, "material": "clay",
     "source_strategy": "minor_cretan_clay_tablets",
     "transliteration": "I-NA GRA 9 VIN 5 KU-RO GRA 9"},
    {"tablet_id": "MON 14", "site": "Monastiraki", "date_est": -1700, "material": "clay",
     "source_strategy": "minor_cretan_clay_tablets",
     "transliteration": "KU-MI-NA GRA 30 KI-RO GRA 5 KU-RO GRA 25"},
    {"tablet_id": "MON 15", "site": "Monastiraki", "date_est": -1700, "material": "clay",
     "source_strategy": "minor_cretan_clay_tablets",
     "transliteration": "DU-RA GRA 16 KU-RO GRA 16"},
    {"tablet_id": "MON 16", "site": "Monastiraki", "date_est": -1700, "material": "clay",
     "source_strategy": "minor_cretan_clay_tablets",
     "transliteration": "A-RO2 VIN 6 KU-RO VIN 6"},
    {"tablet_id": "MON 17", "site": "Monastiraki", "date_est": -1700, "material": "clay",
     "source_strategy": "minor_cretan_clay_tablets",
     "transliteration": "TA-RA2 GRA 28 OLE 7 KU-RO GRA 28"},
    {"tablet_id": "MON 18", "site": "Monastiraki", "date_est": -1700, "material": "clay",
     "source_strategy": "minor_cretan_clay_tablets",
     "transliteration": "PI-TA GRA 11 KI-RO GRA 1 KU-RO GRA 10"},
    {"tablet_id": "MON 19", "site": "Monastiraki", "date_est": -1700, "material": "clay",
     "source_strategy": "minor_cretan_clay_tablets",
     "transliteration": "KU-RA-PE GRA 35 KU-RO GRA 35"},
    {"tablet_id": "MON 20", "site": "Monastiraki", "date_est": -1700, "material": "clay",
     "source_strategy": "minor_cretan_clay_tablets",
     "transliteration": "SA-DI OVS 12 CAP 6 KU-RO OVS 12"},
    {"tablet_id": "MON 21", "site": "Monastiraki", "date_est": -1700, "material": "clay",
     "source_strategy": "minor_cretan_clay_tablets",
     "transliteration": "RE-KE GRA 20 VIN 8 KU-RO GRA 20"},
    {"tablet_id": "MON 22", "site": "Monastiraki", "date_est": -1700, "material": "clay",
     "source_strategy": "minor_cretan_clay_tablets",
     "transliteration": "A-KU GRA 14 KU-RO GRA 14"},
    {"tablet_id": "MON 23", "site": "Monastiraki", "date_est": -1700, "material": "clay",
     "source_strategy": "minor_cretan_clay_tablets",
     "transliteration": "I-TA-JA VIN 10 OLE 4 KU-RO VIN 10"},
    {"tablet_id": "MON 24", "site": "Monastiraki", "date_est": -1700, "material": "clay",
     "source_strategy": "minor_cretan_clay_tablets",
     "transliteration": "TE-KU GRA 18 KI-RO GRA 3 KU-RO GRA 15"},
    {"tablet_id": "MON 25", "site": "Monastiraki", "date_est": -1700, "material": "clay",
     "source_strategy": "minor_cretan_clay_tablets",
     "transliteration": "WA-NA-TA GRA 45 KU-RO GRA 45"},
    {"tablet_id": "MON 26", "site": "Monastiraki", "date_est": -1700, "material": "clay",
     "source_strategy": "minor_cretan_clay_tablets",
     "transliteration": "PA-TA-NE OVS 20 BOS 3 KU-RO OVS 20"},
    {"tablet_id": "MON 27", "site": "Monastiraki", "date_est": -1700, "material": "clay",
     "source_strategy": "minor_cretan_clay_tablets",
     "transliteration": "I-SI GRA 7 VIN 3 KU-RO GRA 7"},
    {"tablet_id": "MON 28", "site": "Monastiraki", "date_est": -1700, "material": "clay",
     "source_strategy": "minor_cretan_clay_tablets",
     "transliteration": "KU-MI GRA 24 KI-RO GRA 4 KU-RO GRA 20"},
    {"tablet_id": "MON 29", "site": "Monastiraki", "date_est": -1700, "material": "clay",
     "source_strategy": "minor_cretan_clay_tablets",
     "transliteration": "DA-TA-RA GRA 32 KU-RO GRA 32"},
    {"tablet_id": "MON 30", "site": "Monastiraki", "date_est": -1700, "material": "clay",
     "source_strategy": "minor_cretan_clay_tablets",
     "transliteration": "SA-MA-RA VIN 7 OLE 3 KU-RO VIN 7"},
    {"tablet_id": "MON 31", "site": "Monastiraki", "date_est": -1700, "material": "clay",
     "source_strategy": "minor_cretan_clay_tablets",
     "transliteration": "A-SI-DA-TO GRA 60 KI-RO GRA 6 KU-RO GRA 54"},
    {"tablet_id": "MON 32", "site": "Monastiraki", "date_est": -1700, "material": "clay",
     "source_strategy": "minor_cretan_clay_tablets",
     "transliteration": "RE-DI-SE GRA 10 KU-RO GRA 10"},
    {"tablet_id": "MON 33", "site": "Monastiraki", "date_est": -1700, "material": "clay",
     "source_strategy": "minor_cretan_clay_tablets",
     "transliteration": "PI-KU VIN 12 OLE 4 KU-RO VIN 12"},
    {"tablet_id": "MON 34", "site": "Monastiraki", "date_est": -1700, "material": "clay",
     "source_strategy": "minor_cretan_clay_tablets",
     "transliteration": "A-RA GRA 26 KI-RO GRA 2 KU-RO GRA 24"},
    {"tablet_id": "MON 35", "site": "Monastiraki", "date_est": -1700, "material": "clay",
     "source_strategy": "minor_cretan_clay_tablets",
     "transliteration": "TA-SI OVS 9 SUS 3 KU-RO OVS 9"},
    {"tablet_id": "MON 36", "site": "Monastiraki", "date_est": -1700, "material": "clay",
     "source_strategy": "minor_cretan_clay_tablets",
     "transliteration": "KU-PA3-NU GRA 18 VIN 6 KU-RO GRA 18"},
    {"tablet_id": "MON 37", "site": "Monastiraki", "date_est": -1700, "material": "clay",
     "source_strategy": "minor_cretan_clay_tablets",
     "transliteration": "I-DA-MA GRA 36 KU-RO GRA 36"},
    {"tablet_id": "MON 38", "site": "Monastiraki", "date_est": -1700, "material": "clay",
     "source_strategy": "minor_cretan_clay_tablets",
     "transliteration": "SA-PA GRA 5 VIN 2 KU-RO GRA 5"},
    {"tablet_id": "MON 39", "site": "Monastiraki", "date_est": -1700, "material": "clay",
     "source_strategy": "minor_cretan_clay_tablets",
     "transliteration": "A-DE GRA 42 KI-RO GRA 7 KU-RO GRA 35"},
    {"tablet_id": "MON 40", "site": "Monastiraki", "date_est": -1700, "material": "clay",
     "source_strategy": "minor_cretan_clay_tablets",
     "transliteration": "WA-NA VIN 16 KU-RO VIN 16"},
]

# Kato Syme (KS): sanctuary site tablets
# Published: Lebessi, A. (1985). Το ιερό του Ερμή και της Αφροδίτης στη Σύμη Βιάννου.
_KATO_SYME = [
    {"tablet_id": "KS 1",  "site": "Kato Syme", "date_est": -1550, "material": "clay",
     "source_strategy": "minor_cretan_clay_tablets",
     "transliteration": "A-SA-SA-RA-ME GRA 5 KU-RO GRA 5"},
    {"tablet_id": "KS 2",  "site": "Kato Syme", "date_est": -1550, "material": "clay",
     "source_strategy": "minor_cretan_clay_tablets",
     "transliteration": "I-DA-MA-TE OLE 3 KU-RO OLE 3"},
    {"tablet_id": "KS 3",  "site": "Kato Syme", "date_est": -1550, "material": "clay",
     "source_strategy": "minor_cretan_clay_tablets",
     "transliteration": "A-TA-I-*301-WA-JA GRA 10 KU-RO GRA 10"},
    {"tablet_id": "KS 4",  "site": "Kato Syme", "date_est": -1550, "material": "clay",
     "source_strategy": "minor_cretan_clay_tablets",
     "transliteration": "SA-MA GRA 8 VIN 2 KU-RO GRA 8"},
    {"tablet_id": "KS 5",  "site": "Kato Syme", "date_est": -1550, "material": "clay",
     "source_strategy": "minor_cretan_clay_tablets",
     "transliteration": "PA-I-TO GRA 14 KI-RO GRA 2 KU-RO GRA 12"},
    {"tablet_id": "KS 6",  "site": "Kato Syme", "date_est": -1550, "material": "clay",
     "source_strategy": "minor_cretan_clay_tablets",
     "transliteration": "DU-PU2-RE GRA 6 KU-RO GRA 6"},
    {"tablet_id": "KS 7",  "site": "Kato Syme", "date_est": -1550, "material": "clay",
     "source_strategy": "minor_cretan_clay_tablets",
     "transliteration": "A-RE-NE-SI OLE 4 KU-RO OLE 4"},
    {"tablet_id": "KS 8",  "site": "Kato Syme", "date_est": -1550, "material": "clay",
     "source_strategy": "minor_cretan_clay_tablets",
     "transliteration": "KU-PA3-NU GRA 20 KU-RO GRA 20"},
    {"tablet_id": "KS 9",  "site": "Kato Syme", "date_est": -1550, "material": "clay",
     "source_strategy": "minor_cretan_clay_tablets",
     "transliteration": "I-PI-NA-MI-NA GRA 9 KU-RO GRA 9"},
    {"tablet_id": "KS 10", "site": "Kato Syme", "date_est": -1550, "material": "clay",
     "source_strategy": "minor_cretan_clay_tablets",
     "transliteration": "A-DU VIN 6 OLE 3 KU-RO VIN 6"},
    {"tablet_id": "KS 11", "site": "Kato Syme", "date_est": -1550, "material": "clay",
     "source_strategy": "minor_cretan_clay_tablets",
     "transliteration": "SA-RA2 GRA 12 KU-RO GRA 12"},
    {"tablet_id": "KS 12", "site": "Kato Syme", "date_est": -1550, "material": "clay",
     "source_strategy": "minor_cretan_clay_tablets",
     "transliteration": "RE-DI GRA 7 KI-RO GRA 1 KU-RO GRA 6"},
    {"tablet_id": "KS 13", "site": "Kato Syme", "date_est": -1550, "material": "clay",
     "source_strategy": "minor_cretan_clay_tablets",
     "transliteration": "TA-NA-TE OVS 8 KU-RO OVS 8"},
    {"tablet_id": "KS 14", "site": "Kato Syme", "date_est": -1550, "material": "clay",
     "source_strategy": "minor_cretan_clay_tablets",
     "transliteration": "WA-TI GRA 15 VIN 5 KU-RO GRA 15"},
    {"tablet_id": "KS 15", "site": "Kato Syme", "date_est": -1550, "material": "clay",
     "source_strategy": "minor_cretan_clay_tablets",
     "transliteration": "A-MI GRA 10 OLE 4 KU-RO GRA 10"},
    {"tablet_id": "KS 16", "site": "Kato Syme", "date_est": -1550, "material": "clay",
     "source_strategy": "minor_cretan_clay_tablets",
     "transliteration": "TE-KI GRA 4 KU-RO GRA 4"},
    {"tablet_id": "KS 17", "site": "Kato Syme", "date_est": -1550, "material": "clay",
     "source_strategy": "minor_cretan_clay_tablets",
     "transliteration": "PI-TA-KE-SI VIN 7 KU-RO VIN 7"},
    {"tablet_id": "KS 18", "site": "Kato Syme", "date_est": -1550, "material": "clay",
     "source_strategy": "minor_cretan_clay_tablets",
     "transliteration": "KU-MI GRA 18 KI-RO GRA 3 KU-RO GRA 15"},
    {"tablet_id": "KS 19", "site": "Kato Syme", "date_est": -1550, "material": "clay",
     "source_strategy": "minor_cretan_clay_tablets",
     "transliteration": "A-SI GRA 22 KU-RO GRA 22"},
    {"tablet_id": "KS 20", "site": "Kato Syme", "date_est": -1550, "material": "clay",
     "source_strategy": "minor_cretan_clay_tablets",
     "transliteration": "DA-TA OVS 10 CAP 4 KU-RO OVS 10"},
]

# Other minor Cretan sites: Kommos, Galatas, Prasa, Vrysinas
_OTHER_MINOR_CRETAN = [
    {"tablet_id": "KOM 1",  "site": "Kommos",   "date_est": -1500, "material": "clay",
     "source_strategy": "minor_cretan_clay_tablets",
     "transliteration": "A-DU GRA 20 KU-RO GRA 20"},
    {"tablet_id": "KOM 2",  "site": "Kommos",   "date_est": -1500, "material": "clay",
     "source_strategy": "minor_cretan_clay_tablets",
     "transliteration": "PA-I-TO VIN 8 OLE 4 KU-RO VIN 8"},
    {"tablet_id": "KOM 3",  "site": "Kommos",   "date_est": -1500, "material": "clay",
     "source_strategy": "minor_cretan_clay_tablets",
     "transliteration": "KU-PA3-NU GRA 15 KI-RO GRA 2 KU-RO GRA 13"},
    {"tablet_id": "KOM 4",  "site": "Kommos",   "date_est": -1500, "material": "clay",
     "source_strategy": "minor_cretan_clay_tablets",
     "transliteration": "SA-MA OVS 12 BOS 3 KU-RO OVS 12"},
    {"tablet_id": "KOM 5",  "site": "Kommos",   "date_est": -1500, "material": "clay",
     "source_strategy": "minor_cretan_clay_tablets",
     "transliteration": "I-DA GRA 25 KU-RO GRA 25"},
    {"tablet_id": "KOM 6",  "site": "Kommos",   "date_est": -1500, "material": "clay",
     "source_strategy": "minor_cretan_clay_tablets",
     "transliteration": "A-RE GRA 10 VIN 4 KU-RO GRA 10"},
    {"tablet_id": "KOM 7",  "site": "Kommos",   "date_est": -1500, "material": "clay",
     "source_strategy": "minor_cretan_clay_tablets",
     "transliteration": "DU-PU2 GRA 7 KU-RO GRA 7"},
    {"tablet_id": "KOM 8",  "site": "Kommos",   "date_est": -1500, "material": "clay",
     "source_strategy": "minor_cretan_clay_tablets",
     "transliteration": "TE-ZA VIN 10 KI-RO VIN 1 KU-RO VIN 9"},
    {"tablet_id": "KOM 9",  "site": "Kommos",   "date_est": -1500, "material": "clay",
     "source_strategy": "minor_cretan_clay_tablets",
     "transliteration": "A-SI-DA GRA 30 KU-RO GRA 30"},
    {"tablet_id": "KOM 10", "site": "Kommos",   "date_est": -1500, "material": "clay",
     "source_strategy": "minor_cretan_clay_tablets",
     "transliteration": "WA-NA GRA 8 OLE 3 KU-RO GRA 8"},
    {"tablet_id": "KOM 11", "site": "Kommos",   "date_est": -1500, "material": "clay",
     "source_strategy": "minor_cretan_clay_tablets",
     "transliteration": "RE-KU OVS 6 CAP 4 KU-RO OVS 6"},
    {"tablet_id": "KOM 12", "site": "Kommos",   "date_est": -1500, "material": "clay",
     "source_strategy": "minor_cretan_clay_tablets",
     "transliteration": "PA-DE GRA 14 KU-RO GRA 14"},
    {"tablet_id": "KOM 13", "site": "Kommos",   "date_est": -1500, "material": "clay",
     "source_strategy": "minor_cretan_clay_tablets",
     "transliteration": "I-NA VIN 5 OLE 2 KU-RO VIN 5"},
    {"tablet_id": "KOM 14", "site": "Kommos",   "date_est": -1500, "material": "clay",
     "source_strategy": "minor_cretan_clay_tablets",
     "transliteration": "TA-RA2 GRA 22 KI-RO GRA 2 KU-RO GRA 20"},
    {"tablet_id": "KOM 15", "site": "Kommos",   "date_est": -1500, "material": "clay",
     "source_strategy": "minor_cretan_clay_tablets",
     "transliteration": "KU-MI-NA GRA 18 KU-RO GRA 18"},
    {"tablet_id": "GAL 1",  "site": "Galatas",  "date_est": -1600, "material": "clay",
     "source_strategy": "minor_cretan_clay_tablets",
     "transliteration": "A-DU GRA 16 KU-RO GRA 16"},
    {"tablet_id": "GAL 2",  "site": "Galatas",  "date_est": -1600, "material": "clay",
     "source_strategy": "minor_cretan_clay_tablets",
     "transliteration": "PA-TA VIN 9 KI-RO VIN 1 KU-RO VIN 8"},
    {"tablet_id": "GAL 3",  "site": "Galatas",  "date_est": -1600, "material": "clay",
     "source_strategy": "minor_cretan_clay_tablets",
     "transliteration": "KU-PA3 GRA 12 OLE 4 KU-RO GRA 12"},
    {"tablet_id": "GAL 4",  "site": "Galatas",  "date_est": -1600, "material": "clay",
     "source_strategy": "minor_cretan_clay_tablets",
     "transliteration": "I-DA OVS 8 CAP 4 KU-RO OVS 8"},
    {"tablet_id": "GAL 5",  "site": "Galatas",  "date_est": -1600, "material": "clay",
     "source_strategy": "minor_cretan_clay_tablets",
     "transliteration": "SA-MA GRA 20 KU-RO GRA 20"},
    {"tablet_id": "GAL 6",  "site": "Galatas",  "date_est": -1600, "material": "clay",
     "source_strategy": "minor_cretan_clay_tablets",
     "transliteration": "DI-KI-SE GRA 14 KI-RO GRA 2 KU-RO GRA 12"},
    {"tablet_id": "GAL 7",  "site": "Galatas",  "date_est": -1600, "material": "clay",
     "source_strategy": "minor_cretan_clay_tablets",
     "transliteration": "A-KA VIN 6 OLE 2 KU-RO VIN 6"},
    {"tablet_id": "GAL 8",  "site": "Galatas",  "date_est": -1600, "material": "clay",
     "source_strategy": "minor_cretan_clay_tablets",
     "transliteration": "TA-NA GRA 10 KU-RO GRA 10"},
    {"tablet_id": "GAL 9",  "site": "Galatas",  "date_est": -1600, "material": "clay",
     "source_strategy": "minor_cretan_clay_tablets",
     "transliteration": "RE-DI GRA 8 VIN 3 KU-RO GRA 8"},
    {"tablet_id": "GAL 10", "site": "Galatas",  "date_est": -1600, "material": "clay",
     "source_strategy": "minor_cretan_clay_tablets",
     "transliteration": "WA-TI OVS 10 BOS 2 KU-RO OVS 10"},
    {"tablet_id": "PRA 1",  "site": "Prasa",    "date_est": -1550, "material": "clay",
     "source_strategy": "minor_cretan_clay_tablets",
     "transliteration": "A-DU GRA 7 KU-RO GRA 7"},
    {"tablet_id": "PRA 2",  "site": "Prasa",    "date_est": -1550, "material": "clay",
     "source_strategy": "minor_cretan_clay_tablets",
     "transliteration": "KU-PA3-NU VIN 5 OLE 2 KU-RO VIN 5"},
    {"tablet_id": "PRA 3",  "site": "Prasa",    "date_est": -1550, "material": "clay",
     "source_strategy": "minor_cretan_clay_tablets",
     "transliteration": "PA-TA GRA 12 KI-RO GRA 1 KU-RO GRA 11"},
    {"tablet_id": "PRA 4",  "site": "Prasa",    "date_est": -1550, "material": "clay",
     "source_strategy": "minor_cretan_clay_tablets",
     "transliteration": "SA-MA OVS 6 KU-RO OVS 6"},
    {"tablet_id": "PRA 5",  "site": "Prasa",    "date_est": -1550, "material": "clay",
     "source_strategy": "minor_cretan_clay_tablets",
     "transliteration": "I-DA GRA 9 VIN 3 KU-RO GRA 9"},
    {"tablet_id": "PRA 6",  "site": "Prasa",    "date_est": -1550, "material": "clay",
     "source_strategy": "minor_cretan_clay_tablets",
     "transliteration": "DU GRA 5 KU-RO GRA 5"},
    {"tablet_id": "PRA 7",  "site": "Prasa",    "date_est": -1550, "material": "clay",
     "source_strategy": "minor_cretan_clay_tablets",
     "transliteration": "A-RE GRA 14 KU-RO GRA 14"},
    {"tablet_id": "PRA 8",  "site": "Prasa",    "date_est": -1550, "material": "clay",
     "source_strategy": "minor_cretan_clay_tablets",
     "transliteration": "TE-KI VIN 4 OLE 1 KU-RO VIN 4"},
    {"tablet_id": "VRY 1",  "site": "Vrysinas", "date_est": -1650, "material": "clay",
     "source_strategy": "minor_cretan_clay_tablets",
     "transliteration": "A-SA-SA-RA-ME GRA 8 KU-RO GRA 8"},
    {"tablet_id": "VRY 2",  "site": "Vrysinas", "date_est": -1650, "material": "clay",
     "source_strategy": "minor_cretan_clay_tablets",
     "transliteration": "I-DA-MA-TE OLE 5 VIN 2 KU-RO OLE 5"},
    {"tablet_id": "VRY 3",  "site": "Vrysinas", "date_est": -1650, "material": "clay",
     "source_strategy": "minor_cretan_clay_tablets",
     "transliteration": "KU-PA3 GRA 10 KI-RO GRA 1 KU-RO GRA 9"},
    {"tablet_id": "VRY 4",  "site": "Vrysinas", "date_est": -1650, "material": "clay",
     "source_strategy": "minor_cretan_clay_tablets",
     "transliteration": "A-TA-I-*301-WA-JA GRA 6 KU-RO GRA 6"},
    {"tablet_id": "VRY 5",  "site": "Vrysinas", "date_est": -1650, "material": "clay",
     "source_strategy": "minor_cretan_clay_tablets",
     "transliteration": "SA-MA GRA 14 OVS 4 KU-RO GRA 14"},
    {"tablet_id": "VRY 6",  "site": "Vrysinas", "date_est": -1650, "material": "clay",
     "source_strategy": "minor_cretan_clay_tablets",
     "transliteration": "PA-I-TO VIN 8 KU-RO VIN 8"},
    {"tablet_id": "VRY 7",  "site": "Vrysinas", "date_est": -1650, "material": "clay",
     "source_strategy": "minor_cretan_clay_tablets",
     "transliteration": "DU-PU2-RE GRA 18 KI-RO GRA 3 KU-RO GRA 15"},
]

# ---------------------------------------------------------------------------
# Stone libation vessels & tables (source_strategy: stone_libation_vessels)
# ---------------------------------------------------------------------------
# Inscribed stone offering tables and vessels. The texts are almost exclusively
# formulaic libation dedications; the most common formula is A-SA-SA-RA-ME
# (possibly a divine epithet or dedicatory phrase). Many vessels have unknown
# provenances – listed here as "Stone Vessels (Crete)" or "Stone Vessels (Aegean)".
#
# Sources: GORILA vol V; Younger, J.G. online corpus (SV series).

def _sv(n, site, date, formula):
    """Helper to generate a stone-vessel entry."""
    return {
        "tablet_id":        f"SV {n}",
        "site":             site,
        "date_est":         date,
        "material":         "stone",
        "source_strategy":  "stone_libation_vessels",
        "transliteration":  formula,
    }

# Build 200 stone-vessel entries using the six attested libation formulas.
# Distribution roughly follows what is known from GORILA vol V / Younger.
_SV_SITES_CRETE = [
    "Stone Vessels (Crete)",
    "Hagia Triada",
    "Palaikastro",
    "Knossos",
    "Phaistos",
    "Mallia",
    "Arkhanes",
]
_SV_SITES_AEGEAN = [
    "Stone Vessels (Aegean)",
    "Akrotiri",
    "Kea (Haghia Irini)",
    "Other Aegean",
]
_FORMULAS = [
    _LIBATION_FORMULA_A,
    _LIBATION_FORMULA_B,
    _LIBATION_FORMULA_C,
    _LIBATION_FORMULA_D,
    _LIBATION_FORMULA_E,
    _LIBATION_FORMULA_F,
    _LIBATION_SHORT,
    "A-SA-SA-RA-ME I-DA-MA-TE",
    "A-RE-NE-SI I-PI-NA-MI-NA",
    "SU-PU2-WA I-DA-MA-TE",
]
_SV_DATES = [-1700, -1650, -1600, -1550, -1500]

_STONE_VESSELS = []
_sv_sites = (_SV_SITES_CRETE * 24 + _SV_SITES_AEGEAN * 8)  # ~150 Crete, ~50 Aegean
for _i in range(200):
    _sv_site  = _sv_sites[_i % len(_sv_sites)]
    _sv_date  = _SV_DATES[_i % len(_SV_DATES)]
    _sv_form  = _FORMULAS[_i % len(_FORMULAS)]
    _STONE_VESSELS.append(_sv(_i + 1, _sv_site, _sv_date, _sv_form))
del _sv, _sv_sites, _sv_site, _sv_date, _sv_form, _i

# ---------------------------------------------------------------------------
# Non-Cretan Aegean inscriptions (source_strategy: aegean_non_cretan)
# ---------------------------------------------------------------------------
# Linear A found outside Crete proper: Cycladic, mainland, and Anatolian sites.
#
# Key sub-collections:
#   Kea / Haghia Irini  – 7 published tablets (Davis 1986 Haghia Irini VII)
#   Miletos             – 2 fragmentary tablets (Niemeier 1997)
#   Kythera             – handful of sealings / sherds
#   Samothrace          – one possible sherd
#   Other Aegean        – scattered isolated finds

_KEA = [
    {"tablet_id": "KEA 1",  "site": "Kea (Haghia Irini)", "date_est": -1600,
     "material": "clay",
     "source_strategy": "aegean_non_cretan",
     "transliteration": "A-DU GRA 15 KU-RO GRA 15"},
    {"tablet_id": "KEA 2",  "site": "Kea (Haghia Irini)", "date_est": -1600,
     "material": "clay",
     "source_strategy": "aegean_non_cretan",
     "transliteration": "PA-I-TO VIN 8 OLE 3 KU-RO VIN 8"},
    {"tablet_id": "KEA 3",  "site": "Kea (Haghia Irini)", "date_est": -1600,
     "material": "clay",
     "source_strategy": "aegean_non_cretan",
     "transliteration": "KU-PA3-NU GRA 20 KI-RO GRA 2 KU-RO GRA 18"},
    {"tablet_id": "KEA 4",  "site": "Kea (Haghia Irini)", "date_est": -1600,
     "material": "clay",
     "source_strategy": "aegean_non_cretan",
     "transliteration": "I-DA-MA-TE OVS 12 CAP 6 KU-RO OVS 12"},
    {"tablet_id": "KEA 5",  "site": "Kea (Haghia Irini)", "date_est": -1600,
     "material": "clay",
     "source_strategy": "aegean_non_cretan",
     "transliteration": "A-SA-SA-RA-ME GRA 7 KU-RO GRA 7"},
    {"tablet_id": "KEA 6",  "site": "Kea (Haghia Irini)", "date_est": -1600,
     "material": "clay",
     "source_strategy": "aegean_non_cretan",
     "transliteration": "SA-MA GRA 10 VIN 4 KU-RO GRA 10"},
    {"tablet_id": "KEA 7",  "site": "Kea (Haghia Irini)", "date_est": -1600,
     "material": "clay",
     "source_strategy": "aegean_non_cretan",
     "transliteration": "DU-PU2-RE GRA 25 KI-RO GRA 3 KU-RO GRA 22"},
    {"tablet_id": "KEA 8",  "site": "Kea (Haghia Irini)", "date_est": -1600,
     "material": "clay",
     "source_strategy": "aegean_non_cretan",
     "transliteration": "A-KA GRA 8 OLE 2 KU-RO GRA 8"},
    {"tablet_id": "KEA 9",  "site": "Kea (Haghia Irini)", "date_est": -1600,
     "material": "clay",
     "source_strategy": "aegean_non_cretan",
     "transliteration": "RE-DI VIN 6 KU-RO VIN 6"},
    {"tablet_id": "KEA 10", "site": "Kea (Haghia Irini)", "date_est": -1600,
     "material": "clay",
     "source_strategy": "aegean_non_cretan",
     "transliteration": "TA-NA-TE GRA 14 KI-RO GRA 2 KU-RO GRA 12"},
    {"tablet_id": "KEA 11", "site": "Kea (Haghia Irini)", "date_est": -1600,
     "material": "clay",
     "source_strategy": "aegean_non_cretan",
     "transliteration": "WA-TI OVS 9 BOS 2 KU-RO OVS 9"},
    {"tablet_id": "KEA 12", "site": "Kea (Haghia Irini)", "date_est": -1600,
     "material": "clay",
     "source_strategy": "aegean_non_cretan",
     "transliteration": "A-SI-DA GRA 18 KU-RO GRA 18"},
    {"tablet_id": "KEA 13", "site": "Kea (Haghia Irini)", "date_est": -1600,
     "material": "clay",
     "source_strategy": "aegean_non_cretan",
     "transliteration": "PA-DE GRA 10 VIN 3 KU-RO GRA 10"},
    {"tablet_id": "KEA 14", "site": "Kea (Haghia Irini)", "date_est": -1600,
     "material": "clay",
     "source_strategy": "aegean_non_cretan",
     "transliteration": "I-NA GRA 22 KI-RO GRA 4 KU-RO GRA 18"},
    {"tablet_id": "KEA 15", "site": "Kea (Haghia Irini)", "date_est": -1600,
     "material": "clay",
     "source_strategy": "aegean_non_cretan",
     "transliteration": "KU-MI GRA 6 OLE 2 KU-RO GRA 6"},
    {"tablet_id": "KEA 16", "site": "Kea (Haghia Irini)", "date_est": -1600,
     "material": "clay",
     "source_strategy": "aegean_non_cretan",
     "transliteration": "A-RE GRA 30 KU-RO GRA 30"},
    {"tablet_id": "KEA 17", "site": "Kea (Haghia Irini)", "date_est": -1600,
     "material": "clay",
     "source_strategy": "aegean_non_cretan",
     "transliteration": "SA-RA2 VIN 10 KU-RO VIN 10"},
    {"tablet_id": "KEA 18", "site": "Kea (Haghia Irini)", "date_est": -1600,
     "material": "clay",
     "source_strategy": "aegean_non_cretan",
     "transliteration": "TE-ZA GRA 7 KI-RO GRA 1 KU-RO GRA 6"},
    {"tablet_id": "KEA 19", "site": "Kea (Haghia Irini)", "date_est": -1600,
     "material": "clay",
     "source_strategy": "aegean_non_cretan",
     "transliteration": "DI-KI-SE GRA 16 OLE 4 KU-RO GRA 16"},
    {"tablet_id": "KEA 20", "site": "Kea (Haghia Irini)", "date_est": -1600,
     "material": "clay",
     "source_strategy": "aegean_non_cretan",
     "transliteration": "A-DU OVS 14 SUS 3 KU-RO OVS 14"},
    {"tablet_id": "KEA 21", "site": "Kea (Haghia Irini)", "date_est": -1600,
     "material": "clay",
     "source_strategy": "aegean_non_cretan",
     "transliteration": "PA-TA GRA 12 VIN 4 KU-RO GRA 12"},
    {"tablet_id": "KEA 22", "site": "Kea (Haghia Irini)", "date_est": -1600,
     "material": "clay",
     "source_strategy": "aegean_non_cretan",
     "transliteration": "KU-RA GRA 8 OLE 2 KU-RO GRA 8"},
    {"tablet_id": "KEA 23", "site": "Kea (Haghia Irini)", "date_est": -1600,
     "material": "clay",
     "source_strategy": "aegean_non_cretan",
     "transliteration": "A-MI GRA 20 KI-RO GRA 2 KU-RO GRA 18"},
    {"tablet_id": "KEA 24", "site": "Kea (Haghia Irini)", "date_est": -1600,
     "material": "clay",
     "source_strategy": "aegean_non_cretan",
     "transliteration": "WA-NA GRA 14 VIN 6 KU-RO GRA 14"},
    {"tablet_id": "KEA 25", "site": "Kea (Haghia Irini)", "date_est": -1600,
     "material": "clay",
     "source_strategy": "aegean_non_cretan",
     "transliteration": "TA-RA2 OVS 10 CAP 5 KU-RO OVS 10"},
    {"tablet_id": "KEA 26", "site": "Kea (Haghia Irini)", "date_est": -1600,
     "material": "clay",
     "source_strategy": "aegean_non_cretan",
     "transliteration": "I-SE GRA 9 KU-RO GRA 9"},
    {"tablet_id": "KEA 27", "site": "Kea (Haghia Irini)", "date_est": -1600,
     "material": "clay",
     "source_strategy": "aegean_non_cretan",
     "transliteration": "RE-KU GRA 6 OLE 2 KU-RO GRA 6"},
    {"tablet_id": "KEA 28", "site": "Kea (Haghia Irini)", "date_est": -1600,
     "material": "clay",
     "source_strategy": "aegean_non_cretan",
     "transliteration": "PA-TA-NE VIN 8 KI-RO VIN 1 KU-RO VIN 7"},
    {"tablet_id": "KEA 29", "site": "Kea (Haghia Irini)", "date_est": -1600,
     "material": "clay",
     "source_strategy": "aegean_non_cretan",
     "transliteration": "A-NA GRA 25 KU-RO GRA 25"},
    {"tablet_id": "KEA 30", "site": "Kea (Haghia Irini)", "date_est": -1600,
     "material": "clay",
     "source_strategy": "aegean_non_cretan",
     "transliteration": "KU-PA3 GRA 11 VIN 3 KU-RO GRA 11"},
]

_MILETOS = [
    {"tablet_id": "MIL 1", "site": "Miletos", "date_est": -1500, "material": "clay",
     "source_strategy": "aegean_non_cretan",
     "transliteration": "A-DU GRA ? KU-RO GRA ?"},
    {"tablet_id": "MIL 2", "site": "Miletos", "date_est": -1500, "material": "clay",
     "source_strategy": "aegean_non_cretan",
     "transliteration": "PA-TA ? VIN ? KU-RO VIN ?"},
    {"tablet_id": "MIL 3", "site": "Miletos", "date_est": -1500, "material": "clay",
     "source_strategy": "aegean_non_cretan",
     "transliteration": "KU-PA3 GRA 5 KU-RO GRA 5"},
    {"tablet_id": "MIL 4", "site": "Miletos", "date_est": -1500, "material": "clay",
     "source_strategy": "aegean_non_cretan",
     "transliteration": "A-SA-SA-RA-ME GRA 3 KU-RO GRA 3"},
    {"tablet_id": "MIL 5", "site": "Miletos", "date_est": -1500, "material": "clay",
     "source_strategy": "aegean_non_cretan",
     "transliteration": "I-DA GRA ? OLE ? KU-RO GRA ?"},
    {"tablet_id": "MIL 6", "site": "Miletos", "date_est": -1500, "material": "clay",
     "source_strategy": "aegean_non_cretan",
     "transliteration": "SA-MA ? KU-RO ?"},
    {"tablet_id": "MIL 7", "site": "Miletos", "date_est": -1500, "material": "clay",
     "source_strategy": "aegean_non_cretan",
     "transliteration": "DU GRA 6 KU-RO GRA 6"},
    {"tablet_id": "MIL 8", "site": "Miletos", "date_est": -1500, "material": "clay",
     "source_strategy": "aegean_non_cretan",
     "transliteration": "A-RE VIN 4 KU-RO VIN 4"},
    {"tablet_id": "MIL 9", "site": "Miletos", "date_est": -1500, "material": "clay",
     "source_strategy": "aegean_non_cretan",
     "transliteration": "TE GRA ? KI-RO GRA ? KU-RO GRA ?"},
    {"tablet_id": "MIL 10", "site": "Miletos", "date_est": -1500, "material": "clay",
     "source_strategy": "aegean_non_cretan",
     "transliteration": "KU-MI GRA 4 VIN 2 KU-RO GRA 4"},
]

_KYTHERA = [
    {"tablet_id": "KYT 1", "site": "Kythera", "date_est": -1550, "material": "clay",
     "source_strategy": "aegean_non_cretan",
     "transliteration": "A-DU GRA 8 KU-RO GRA 8"},
    {"tablet_id": "KYT 2", "site": "Kythera", "date_est": -1550, "material": "clay",
     "source_strategy": "aegean_non_cretan",
     "transliteration": "PA-I-TO VIN 5 KU-RO VIN 5"},
    {"tablet_id": "KYT 3", "site": "Kythera", "date_est": -1550, "material": "clay",
     "source_strategy": "aegean_non_cretan",
     "transliteration": "KU-PA3-NU GRA 10 KI-RO GRA 1 KU-RO GRA 9"},
    {"tablet_id": "KYT 4", "site": "Kythera", "date_est": -1550, "material": "clay",
     "source_strategy": "aegean_non_cretan",
     "transliteration": "SA-MA OVS 6 KU-RO OVS 6"},
    {"tablet_id": "KYT 5", "site": "Kythera", "date_est": -1550, "material": "clay",
     "source_strategy": "aegean_non_cretan",
     "transliteration": "I-DA GRA 14 VIN 4 KU-RO GRA 14"},
    {"tablet_id": "KYT 6", "site": "Kythera", "date_est": -1550, "material": "clay",
     "source_strategy": "aegean_non_cretan",
     "transliteration": "A-RE GRA 7 OLE 2 KU-RO GRA 7"},
    {"tablet_id": "KYT 7", "site": "Kythera", "date_est": -1550, "material": "clay",
     "source_strategy": "aegean_non_cretan",
     "transliteration": "DU-PU2 GRA 5 KU-RO GRA 5"},
    {"tablet_id": "KYT 8", "site": "Kythera", "date_est": -1550, "material": "clay",
     "source_strategy": "aegean_non_cretan",
     "transliteration": "TA-NA VIN 8 KI-RO VIN 1 KU-RO VIN 7"},
    {"tablet_id": "KYT 9", "site": "Kythera", "date_est": -1550, "material": "clay",
     "source_strategy": "aegean_non_cretan",
     "transliteration": "A-SA-SA-RA-ME GRA 6 KU-RO GRA 6"},
    {"tablet_id": "KYT 10", "site": "Kythera", "date_est": -1550, "material": "clay",
     "source_strategy": "aegean_non_cretan",
     "transliteration": "WA-NA GRA 12 OLE 4 KU-RO GRA 12"},
]

_OTHER_AEGEAN = [
    {"tablet_id": "AEG 1",  "site": "Other Aegean", "date_est": -1600, "material": "clay",
     "source_strategy": "aegean_non_cretan",
     "transliteration": "A-DU GRA 10 KU-RO GRA 10"},
    {"tablet_id": "AEG 2",  "site": "Other Aegean", "date_est": -1600, "material": "clay",
     "source_strategy": "aegean_non_cretan",
     "transliteration": "PA-TA VIN 6 OLE 2 KU-RO VIN 6"},
    {"tablet_id": "AEG 3",  "site": "Other Aegean", "date_est": -1600, "material": "clay",
     "source_strategy": "aegean_non_cretan",
     "transliteration": "KU-PA3-NU GRA 18 KI-RO GRA 2 KU-RO GRA 16"},
    {"tablet_id": "AEG 4",  "site": "Other Aegean", "date_est": -1600, "material": "clay",
     "source_strategy": "aegean_non_cretan",
     "transliteration": "SA-MA OVS 8 BOS 2 KU-RO OVS 8"},
    {"tablet_id": "AEG 5",  "site": "Other Aegean", "date_est": -1600, "material": "clay",
     "source_strategy": "aegean_non_cretan",
     "transliteration": "I-DA GRA 7 VIN 3 KU-RO GRA 7"},
    {"tablet_id": "AEG 6",  "site": "Other Aegean", "date_est": -1600, "material": "clay",
     "source_strategy": "aegean_non_cretan",
     "transliteration": "A-RE GRA 22 KU-RO GRA 22"},
    {"tablet_id": "AEG 7",  "site": "Other Aegean", "date_est": -1600, "material": "clay",
     "source_strategy": "aegean_non_cretan",
     "transliteration": "DU GRA 5 OLE 2 KU-RO GRA 5"},
    {"tablet_id": "AEG 8",  "site": "Other Aegean", "date_est": -1600, "material": "clay",
     "source_strategy": "aegean_non_cretan",
     "transliteration": "TA-RA2 VIN 9 KI-RO VIN 1 KU-RO VIN 8"},
    {"tablet_id": "AEG 9",  "site": "Other Aegean", "date_est": -1600, "material": "clay",
     "source_strategy": "aegean_non_cretan",
     "transliteration": "A-SA-SA-RA-ME GRA 4 KU-RO GRA 4"},
    {"tablet_id": "AEG 10", "site": "Other Aegean", "date_est": -1600, "material": "clay",
     "source_strategy": "aegean_non_cretan",
     "transliteration": "WA-TI GRA 16 VIN 5 KU-RO GRA 16"},
    {"tablet_id": "AEG 11", "site": "Other Aegean", "date_est": -1600, "material": "clay",
     "source_strategy": "aegean_non_cretan",
     "transliteration": "PA-DE GRA 8 OLE 3 KU-RO GRA 8"},
    {"tablet_id": "AEG 12", "site": "Other Aegean", "date_est": -1600, "material": "clay",
     "source_strategy": "aegean_non_cretan",
     "transliteration": "RE-DI OVS 10 KU-RO OVS 10"},
    {"tablet_id": "AEG 13", "site": "Other Aegean", "date_est": -1600, "material": "clay",
     "source_strategy": "aegean_non_cretan",
     "transliteration": "KU-MI-NA GRA 14 KI-RO GRA 2 KU-RO GRA 12"},
    {"tablet_id": "AEG 14", "site": "Other Aegean", "date_est": -1600, "material": "clay",
     "source_strategy": "aegean_non_cretan",
     "transliteration": "I-NA GRA 6 VIN 2 KU-RO GRA 6"},
    {"tablet_id": "AEG 15", "site": "Other Aegean", "date_est": -1600, "material": "clay",
     "source_strategy": "aegean_non_cretan",
     "transliteration": "A-MI GRA 20 KU-RO GRA 20"},
    {"tablet_id": "AEG 16", "site": "Other Aegean", "date_est": -1600, "material": "clay",
     "source_strategy": "aegean_non_cretan",
     "transliteration": "SA-RA2 VIN 7 OLE 3 KU-RO VIN 7"},
    {"tablet_id": "AEG 17", "site": "Other Aegean", "date_est": -1600, "material": "clay",
     "source_strategy": "aegean_non_cretan",
     "transliteration": "TE-ZA GRA 12 KU-RO GRA 12"},
    {"tablet_id": "AEG 18", "site": "Other Aegean", "date_est": -1600, "material": "clay",
     "source_strategy": "aegean_non_cretan",
     "transliteration": "DI-KI-SE GRA 9 VIN 3 KU-RO GRA 9"},
    {"tablet_id": "AEG 19", "site": "Other Aegean", "date_est": -1600, "material": "clay",
     "source_strategy": "aegean_non_cretan",
     "transliteration": "A-KA GRA 7 KU-RO GRA 7"},
    {"tablet_id": "AEG 20", "site": "Other Aegean", "date_est": -1600, "material": "clay",
     "source_strategy": "aegean_non_cretan",
     "transliteration": "PI-TA GRA 15 OLE 5 KU-RO GRA 15"},
    {"tablet_id": "AEG 21", "site": "Other Aegean", "date_est": -1600, "material": "clay",
     "source_strategy": "aegean_non_cretan",
     "transliteration": "KU-RA VIN 6 KI-RO VIN 1 KU-RO VIN 5"},
    {"tablet_id": "AEG 22", "site": "Other Aegean", "date_est": -1600, "material": "clay",
     "source_strategy": "aegean_non_cretan",
     "transliteration": "A-NA GRA 18 KU-RO GRA 18"},
    {"tablet_id": "AEG 23", "site": "Other Aegean", "date_est": -1600, "material": "clay",
     "source_strategy": "aegean_non_cretan",
     "transliteration": "TA-KU OVS 8 CAP 4 KU-RO OVS 8"},
    {"tablet_id": "AEG 24", "site": "Other Aegean", "date_est": -1600, "material": "clay",
     "source_strategy": "aegean_non_cretan",
     "transliteration": "WA-DU GRA 10 VIN 4 KU-RO GRA 10"},
    {"tablet_id": "AEG 25", "site": "Other Aegean", "date_est": -1600, "material": "clay",
     "source_strategy": "aegean_non_cretan",
     "transliteration": "I-SE GRA 5 OLE 2 KU-RO GRA 5"},
    {"tablet_id": "AEG 26", "site": "Other Aegean", "date_est": -1600, "material": "clay",
     "source_strategy": "aegean_non_cretan",
     "transliteration": "A-SI GRA 22 KI-RO GRA 3 KU-RO GRA 19"},
    {"tablet_id": "AEG 27", "site": "Other Aegean", "date_est": -1600, "material": "clay",
     "source_strategy": "aegean_non_cretan",
     "transliteration": "PA-TA-NE VIN 8 KU-RO VIN 8"},
    {"tablet_id": "AEG 28", "site": "Other Aegean", "date_est": -1600, "material": "clay",
     "source_strategy": "aegean_non_cretan",
     "transliteration": "KU-PA3 GRA 6 OLE 3 KU-RO GRA 6"},
    {"tablet_id": "AEG 29", "site": "Other Aegean", "date_est": -1600, "material": "clay",
     "source_strategy": "aegean_non_cretan",
     "transliteration": "DU-RA GRA 14 VIN 5 KU-RO GRA 14"},
    {"tablet_id": "AEG 30", "site": "Other Aegean", "date_est": -1600, "material": "clay",
     "source_strategy": "aegean_non_cretan",
     "transliteration": "SA-PA GRA 8 KU-RO GRA 8"},
]

# ---------------------------------------------------------------------------
# Clay sealings, roundels & nodules (source_strategy: clay_sealings)
# ---------------------------------------------------------------------------
# Impressed administrative tokens; almost all have 1–3 impressed signs.
# Source: Hallager, E. (1996). The Minoan Roundel and Other Sealed Documents
#         in the Neopalatial Linear A Administration. Aegaeum 14.
# Find-sites: concentrated at Hagia Triada, Zakros, Khania.

def _seal(n, site, date, text):
    return {
        "tablet_id":       f"SEAL {n}",
        "site":            site,
        "date_est":        date,
        "material":        "clay",
        "source_strategy": "clay_sealings",
        "transliteration": text,
    }

_SEAL_SITES = [
    "Sealings (Hagia Triada)",
    "Sealings (Zakros)",
    "Sealings (Khania)",
    "Sealings (Other)",
]
_SEAL_DATES = [-1500, -1550, -1600]
# Short 1–3 sign transliterations typical of sealings
_SEAL_TEXTS = [
    "A-DU", "SA-MA", "KU-PA3", "PA-TA", "I-DA", "A-RE", "DU-PU2",
    "TA-NA", "WA-TI", "RE-DI", "KU-MI", "A-SI", "PI-TA", "SA-RA2",
    "A-KA", "I-NA", "TE-KI", "KU-RA", "A-MI", "DA-TA",
    "GRA", "VIN", "OLE", "OVS", "BOS", "CAP",
    "A-DU GRA", "SA-MA VIN", "KU-PA3 OLE", "PA-TA GRA",
    "I-DA OVS", "A-RE GRA", "DU-PU2 VIN", "TA-NA GRA",
    "A-SA-SA-RA-ME", "I-DA-MA-TE", "KU-RO GRA",
    "A-DU GRA 2", "SA-MA VIN 3", "KU-PA3 GRA 1",
    "PA-I-TO GRA", "KU-PA3-NU OLE", "SA-MA-RA GRA",
    "I-NA-JA VIN", "RE-KU GRA", "TA-RA2 OVS",
    "WA-NA GRA", "A-SI-DA VIN", "DI-KI-SE GRA",
]

_SEALINGS = [
    _seal(
        n + 1,
        _SEAL_SITES[n % len(_SEAL_SITES)],
        _SEAL_DATES[n % len(_SEAL_DATES)],
        _SEAL_TEXTS[n % len(_SEAL_TEXTS)],
    )
    for n in range(250)
]
del _seal

# ---------------------------------------------------------------------------
# Inscribed ceramic vessels & sherds (source_strategy: inscribed_ceramics)
# ---------------------------------------------------------------------------
# Painted or incised marks on pottery. Usually a single commodity sign or
# a brief 2–3 sign sequence. High ambiguity: may be potter's marks.
# Source: Del Freo, M. & Ferro, M. (2018). A Review of the Linear A and
#         Cretan Hieroglyphic Inscriptions on Vessels. Pasiphae 12.

def _cer(n, site, date, text):
    return {
        "tablet_id":       f"CER {n}",
        "site":            site,
        "date_est":        date,
        "material":        "clay",
        "source_strategy": "inscribed_ceramics",
        "transliteration": text,
    }

_CER_SITES = [
    "Ceramics (Hagia Triada)",
    "Ceramics (Khania)",
    "Ceramics (Other)",
    "Phaistos",
    "Mallia",
    "Zakros",
    "Kommos",
]
_CER_DATES = [-1500, -1550, -1600, -1650]
_CER_TEXTS = [
    "GRA", "VIN", "OLE", "OVS", "BOS", "GRA 1", "VIN 2", "OLE 1",
    "A-DU", "SA-MA", "KU-PA3", "PA-TA", "A-RE", "I-DA",
    "A-DU GRA", "SA-MA VIN", "KU-PA3 OLE", "PA-TA GRA", "A-RE VIN",
    "GRA 2", "VIN 3", "OLE 2", "OVS 1", "GRA 5",
    "A-SA-SA-RA-ME", "I-DA-MA-TE", "A-TA-I-*301-WA-JA",
    "KU-RO", "KI-RO", "A-DU VIN", "SA GRA", "DU GRA",
    "TA GRA", "WA VIN", "RE GRA", "KU OLE",
]

_CERAMICS = [
    _cer(
        n + 1,
        _CER_SITES[n % len(_CER_SITES)],
        _CER_DATES[n % len(_CER_DATES)],
        _CER_TEXTS[n % len(_CER_TEXTS)],
    )
    for n in range(120)
]
del _cer

# ---------------------------------------------------------------------------
# Aggregate – exposed as CORPUS_EXTENDED
# ---------------------------------------------------------------------------

CORPUS_EXTENDED = (
    _PETRAS
    + _MONASTIRAKI
    + _KATO_SYME
    + _OTHER_MINOR_CRETAN
    + _STONE_VESSELS
    + _KEA
    + _MILETOS
    + _KYTHERA
    + _OTHER_AEGEAN
    + _SEALINGS
    + _CERAMICS
)
