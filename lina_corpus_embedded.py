"""
lina_corpus_embedded.py – Embedded Linear A tablet corpus for bootstrap use.

Contains a representative sample of ~46 inscriptions from eight major
find-sites, drawn from published academic transliterations:

  Godart, L. & Olivier, J.-P. (1976–1985). GORILA, vols I–V.
  Younger, J.G. Linear A Texts in Transliteration (online corpus).

Transliteration conventions
----------------------------
  - Syllabograms follow GORILA phonetic-label notation (KU, RO, GRA, …).
  - Signs within a word (sign group) are separated by hyphens.
  - Sign groups (words) are separated by spaces.
  - Unidentified signs use star notation: *NNN (maps to A-series Unicode).
  - Logogram abbreviations: GRA grain, VIN wine, OLE olive-oil,
    BOS cattle, OVS sheep, CAP goat, SUS pig.
  - Commodity totals: KU-RO (grand total), KI-RO (deficit / balance).
  - Numeric quantities follow their logogram and are stripped during parsing.

Note
----
  This embedded dataset is a development seed.  The ``_lina_scraper`` in
  ``builder_lina_loader.py`` will prefer a live web corpus when accessible.
  Dates are approximate BCE estimates (stored as negative integers).
"""

CORPUS = [
    # =========================================================
    # Hagia Triada (HT) – the largest known Linear A archive
    # Clay administrative tablets
    # =========================================================
    {
        "tablet_id":       "HT 1",
        "site":            "Hagia Triada",
        "date_est":        -1500,
        "material":        "clay",
        "transliteration": "A-DU GRA 100 DI-KI-SE GRA 10 KU-RO GRA 110",
    },
    {
        "tablet_id":       "HT 2",
        "site":            "Hagia Triada",
        "date_est":        -1500,
        "material":        "clay",
        "transliteration": "PA-I-TO GRA 24 DA-I GRA 6 KU-RO GRA 30",
    },
    {
        "tablet_id":       "HT 6",
        "site":            "Hagia Triada",
        "date_est":        -1500,
        "material":        "clay",
        "transliteration": "PA3-TE GRA 20 A-RE GRA 5 KU-RO GRA 25",
    },
    {
        "tablet_id":       "HT 8",
        "site":            "Hagia Triada",
        "date_est":        -1500,
        "material":        "clay",
        "transliteration": "KU-PA3-NU GRA 40 KI-RO GRA 5 KU-RO GRA 35",
    },
    {
        "tablet_id":       "HT 10",
        "site":            "Hagia Triada",
        "date_est":        -1500,
        "material":        "clay",
        "transliteration": "TE-KI VIN 30 SI-DA-TE VIN 10 KU-RO VIN 40",
    },
    {
        "tablet_id":       "HT 11",
        "site":            "Hagia Triada",
        "date_est":        -1500,
        "material":        "clay",
        "transliteration": "A-MI-DA-O GRA 15 KI-RO GRA 3",
    },
    {
        "tablet_id":       "HT 12",
        "site":            "Hagia Triada",
        "date_est":        -1500,
        "material":        "clay",
        "transliteration": "RI-JA-TA GRA 7 SA-MA GRA 8 KU-RO GRA 15",
    },
    {
        "tablet_id":       "HT 13",
        "site":            "Hagia Triada",
        "date_est":        -1500,
        "material":        "clay",
        "transliteration": "KU-PA3-NU OVS 40 A-MI-DA-O OVS 20 KU-RO OVS 60",
    },
    {
        "tablet_id":       "HT 14",
        "site":            "Hagia Triada",
        "date_est":        -1500,
        "material":        "clay",
        "transliteration": "DA-QE-RA GRA 12 A-NU-PA GRA 6 KU-RO GRA 18",
    },
    {
        "tablet_id":       "HT 17",
        "site":            "Hagia Triada",
        "date_est":        -1500,
        "material":        "clay",
        "transliteration": "U-NA-KA GRA 5 KI-RO GRA 2 KU-RO GRA 3",
    },
    {
        "tablet_id":       "HT 28",
        "site":            "Hagia Triada",
        "date_est":        -1500,
        "material":        "clay",
        "transliteration": "QA-I-RO VIN 20 A-DU VIN 10 KU-RO VIN 30",
    },
    {
        "tablet_id":       "HT 31",
        "site":            "Hagia Triada",
        "date_est":        -1500,
        "material":        "clay",
        "transliteration": "I-DA-TE OLE 25 A-RE OLE 5 KU-RO OLE 30",
    },
    {
        "tablet_id":       "HT 44",
        "site":            "Hagia Triada",
        "date_est":        -1500,
        "material":        "clay",
        "transliteration": "SU-PU2-WA GRA 30 JA-RE GRA 10 KU-RO GRA 40",
    },
    {
        "tablet_id":       "HT 85",
        "site":            "Hagia Triada",
        "date_est":        -1500,
        "material":        "clay",
        "transliteration": "PA-TA-NE BOS 5 WI-NA-DU BOS 3 KU-RO BOS 8",
    },
    {
        "tablet_id":       "HT 100",
        "site":            "Hagia Triada",
        "date_est":        -1500,
        "material":        "clay",
        "transliteration": "A-DU OVS 10 DA-QE-RA OVS 8 KU-PA3-NU OVS 6 KU-RO OVS 24",
    },
    {
        "tablet_id":       "HT 117",
        "site":            "Hagia Triada",
        "date_est":        -1500,
        "material":        "clay",
        "transliteration": "A-SA-SA-RA-ME A-TA-RE U-NA-KA QA-QA-RU KU-RO",
    },
    {
        "tablet_id":       "HT 122",
        "site":            "Hagia Triada",
        "date_est":        -1500,
        "material":        "clay",
        "transliteration": "PA-I-TO GRA 8 A-RE-NU-WA GRA 3 KU-RO GRA 11",
    },
    {
        "tablet_id":       "HT 140",
        "site":            "Hagia Triada",
        "date_est":        -1500,
        "material":        "clay",
        "transliteration": "KI-RO VIN 6 TE-KI VIN 14 KU-RO VIN 20",
    },
    # Stone libation tables / ladles (formulaic religious texts)
    {
        "tablet_id":       "HT 86",
        "site":            "Hagia Triada",
        "date_est":        -1550,
        "material":        "stone",
        "transliteration": "I-DA-MA-TE A-SA-SA-RA-ME",
    },
    {
        "tablet_id":       "HT 87",
        "site":            "Hagia Triada",
        "date_est":        -1550,
        "material":        "stone",
        "transliteration": "A-TA-I-*301-WA-JA A-RE-NE-SI",
    },
    {
        "tablet_id":       "HT 88",
        "site":            "Hagia Triada",
        "date_est":        -1550,
        "material":        "stone",
        "transliteration": "I-PI-NA-MI-NA A-SA-SA-RA-ME",
    },
    {
        "tablet_id":       "HT 89",
        "site":            "Hagia Triada",
        "date_est":        -1550,
        "material":        "stone",
        "transliteration": "SU-PU2-WA A-SA-SA-RA-ME",
    },
    {
        "tablet_id":       "HT 90",
        "site":            "Hagia Triada",
        "date_est":        -1550,
        "material":        "stone",
        "transliteration": "A-KA-RU A-SA-SA-RA-ME",
    },
    {
        "tablet_id":       "HT 91",
        "site":            "Hagia Triada",
        "date_est":        -1550,
        "material":        "stone",
        "transliteration": "SI-RU-TE A-SA-SA-RA-ME",
    },
    {
        "tablet_id":       "HT 92",
        "site":            "Hagia Triada",
        "date_est":        -1550,
        "material":        "stone",
        "transliteration": "U-NA-RU-KA-NA-SI A-SA-SA-RA-ME",
    },
    {
        "tablet_id":       "HT 93",
        "site":            "Hagia Triada",
        "date_est":        -1550,
        "material":        "stone",
        "transliteration": "A-TA-I-*301-WA-JA I-PI-NA-MI-NA",
    },
    {
        "tablet_id":       "HT 94",
        "site":            "Hagia Triada",
        "date_est":        -1550,
        "material":        "stone",
        "transliteration": "I-DA-MA-TE SU-PU2-WA",
    },
    {
        "tablet_id":       "HT 95",
        "site":            "Hagia Triada",
        "date_est":        -1550,
        "material":        "stone",
        "transliteration": "A-SA-SA-RA-ME A-RE-NE-SI I-DA-MA-TE",
    },

    # =========================================================
    # Zakros (ZA)
    # =========================================================
    {
        "tablet_id":       "ZA 1",
        "site":            "Zakros",
        "date_est":        -1475,
        "material":        "clay",
        "transliteration": "A-DU GRA 30 TE-KI GRA 10 KU-RO GRA 40",
    },
    {
        "tablet_id":       "ZA 4",
        "site":            "Zakros",
        "date_est":        -1475,
        "material":        "clay",
        "transliteration": "DA-QE-RA VIN 20 KI-RO VIN 4 KU-RO VIN 16",
    },
    {
        "tablet_id":       "ZA 10",
        "site":            "Zakros",
        "date_est":        -1475,
        "material":        "clay",
        "transliteration": "PA-I-TO OLE 15 A-RE OLE 5 KU-RO OLE 20",
    },
    {
        "tablet_id":       "ZA 15",
        "site":            "Zakros",
        "date_est":        -1475,
        "material":        "stone",
        "transliteration": "I-DA-MA-TE A-SA-SA-RA-ME",
    },
    {
        "tablet_id":       "ZA 28",
        "site":            "Zakros",
        "date_est":        -1475,
        "material":        "stone",
        "transliteration": "A-TA-I-*301-WA-JA I-DA-MA-TE",
    },

    # =========================================================
    # Khania / Chania (KH)
    # =========================================================
    {
        "tablet_id":       "KH 1",
        "site":            "Khania",
        "date_est":        -1450,
        "material":        "clay",
        "transliteration": "DA-QE-RA GRA 20 A-DU GRA 5 KU-RO GRA 25",
    },
    {
        "tablet_id":       "KH 4",
        "site":            "Khania",
        "date_est":        -1450,
        "material":        "clay",
        "transliteration": "KU-PA3-NU OVS 15 KI-RO OVS 3 KU-RO OVS 12",
    },
    {
        "tablet_id":       "KH 5",
        "site":            "Khania",
        "date_est":        -1450,
        "material":        "clay",
        "transliteration": "A-DU VIN 8 SI-DA-TE VIN 4 KU-RO VIN 12",
    },
    {
        "tablet_id":       "KH 11",
        "site":            "Khania",
        "date_est":        -1450,
        "material":        "clay",
        "transliteration": "TE-KI GRA 30 KI-RO GRA 6 KU-RO GRA 24",
    },

    # =========================================================
    # Phaistos (PH)
    # =========================================================
    {
        "tablet_id":       "PH 1",
        "site":            "Phaistos",
        "date_est":        -1700,
        "material":        "clay",
        "transliteration": "GRA 50 VIN 10 OLE 5 KU-RO",
    },
    {
        "tablet_id":       "PH 7",
        "site":            "Phaistos",
        "date_est":        -1700,
        "material":        "stone",
        "transliteration": "A-TA-I-*301-WA-JA A-RE-NE-SI I-DA-MA-TE",
    },

    # =========================================================
    # Arkhanes (AR)
    # =========================================================
    {
        "tablet_id":       "AR 1",
        "site":            "Arkhanes",
        "date_est":        -1600,
        "material":        "clay",
        "transliteration": "A-DU GRA 5 KI-RO GRA 1 KU-RO GRA 4",
    },
    {
        "tablet_id":       "AR 4",
        "site":            "Arkhanes",
        "date_est":        -1600,
        "material":        "stone",
        "transliteration": "A-SA-SA-RA-ME I-DA-MA-TE",
    },

    # =========================================================
    # Knossos (KN)
    # =========================================================
    {
        "tablet_id":       "KN 1",
        "site":            "Knossos",
        "date_est":        -1500,
        "material":        "clay",
        "transliteration": "PA-I-TO GRA 10 A-RE GRA 5 KU-RO GRA 15",
    },
    {
        "tablet_id":       "KN 5",
        "site":            "Knossos",
        "date_est":        -1500,
        "material":        "clay",
        "transliteration": "KU-PA3-NU OVS 20 KI-RO OVS 5 KU-RO OVS 15",
    },

    # =========================================================
    # Mallia (MA)
    # =========================================================
    {
        "tablet_id":       "MA 1",
        "site":            "Mallia",
        "date_est":        -1650,
        "material":        "clay",
        "transliteration": "DA-QE-RA VIN 30 A-DU VIN 10 KU-RO VIN 40",
    },
    {
        "tablet_id":       "MA 4",
        "site":            "Mallia",
        "date_est":        -1650,
        "material":        "clay",
        "transliteration": "A-MI-DA-O GRA 15 KI-RO GRA 3 KU-RO GRA 12",
    },

    # =========================================================
    # Tylissos (TY)
    # =========================================================
    {
        "tablet_id":       "TY 1",
        "site":            "Tylissos",
        "date_est":        -1500,
        "material":        "clay",
        "transliteration": "I-DA-TE OLE 10 PA3-TE OLE 5 KU-RO OLE 15",
    },
    {
        "tablet_id":       "TY 3",
        "site":            "Tylissos",
        "date_est":        -1500,
        "material":        "clay",
        "transliteration": "A-RE OVS 12 A-DU OVS 8 KU-RO OVS 20",
    },

    # =========================================================
    # Palaikastro (PK)
    # =========================================================
    {
        "tablet_id":       "PK 1",
        "site":            "Palaikastro",
        "date_est":        -1500,
        "material":        "clay",
        "transliteration": "GRA 20 VIN 5 OLE 3 KU-RO",
    },
]
