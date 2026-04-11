"""
lina_sign_catalog.py – Exhaustive Linear A sign catalog and transliteration utilities.

Derives all 341 Linear A code points directly from Python's built-in
`unicodedata` module (Unicode Standard ≥ 9.0, Linear A block U+10600–U+1077F).

Provides:
  - build_sign_catalog()            → list of 341 sign dicts
  - build_label_to_char_map()       → {sign_label: unicode_char}
  - build_char_to_id_map()          → {unicode_char: sign_id}
  - parse_sign_groups()             → tokenise a transliteration string
  - sign_group_to_unicode()         → one sign group → Unicode Linear A string
  - transliteration_to_unicode_string() → full transliteration → Unicode string

References
----------
  Godart, L. & Olivier, J.-P. (1976–1985). GORILA (Recueil des inscriptions
      en linéaire A), vols I–V. Paris: Geuthner.
  Younger, J.G. Linear A Texts in Transliteration (online corpus).
  Unicode Standard – Linear A block chart U+10600.
"""

import re
import unicodedata
from typing import Dict, List, Optional

# ---------------------------------------------------------------------------
# Block constants
# ---------------------------------------------------------------------------

LINA_BLOCK_START = 0x10600
LINA_BLOCK_END   = 0x1077F


# ---------------------------------------------------------------------------
# Catalog builder
# ---------------------------------------------------------------------------

def build_sign_catalog() -> List[dict]:
    """Return the exhaustive list of all 341 Linear A sign entries.

    Each entry is a dict with keys:
        sign_id      : int  – stable ID = codepoint − 0x10600 (0-based, sparse)
        sign_label   : str  – GORILA identifier extracted from the Unicode name
                              (e.g. 'AB001', 'A301', 'A309A', 'AB021F')
        char         : str  – the Unicode character
        codepoint    : int  – Unicode code point (decimal)
        hex_code     : str  – '0x10600' style
        unicode_name : str  – full Unicode character name
        category     : str  – 'syllabic' | 'logographic' | 'numeric_fraction'
                              | 'punctuation' | 'other'
    """
    catalog = []
    for cp in range(LINA_BLOCK_START, LINA_BLOCK_END + 1):
        try:
            uname = unicodedata.name(chr(cp))
        except ValueError:
            continue
        if not uname.startswith("LINEAR A"):
            continue

        m = re.match(r"LINEAR A SIGN (.+)", uname)
        sign_label = m.group(1) if m else uname.replace("LINEAR A ", "")

        # Categorise by sign_label pattern
        if sign_label.startswith("AB"):
            category = "syllabic"
        elif re.match(r"A[7-9]\d{2}", sign_label) or re.match(r"A[7-9]\d{2}", sign_label[:4]):
            category = "numeric_fraction"
        elif re.match(r"A8\d{2}", sign_label):
            category = "punctuation"
        elif re.match(r"A\d", sign_label):
            category = "logographic"
        else:
            category = "other"

        catalog.append({
            "sign_id":      cp - LINA_BLOCK_START,
            "sign_label":   sign_label,
            "char":         chr(cp),
            "codepoint":    cp,
            "hex_code":     hex(cp),
            "unicode_name": uname,
            "category":     category,
        })

    return catalog


# ---------------------------------------------------------------------------
# Convenience lookup maps
# ---------------------------------------------------------------------------

def build_label_to_char_map(catalog: Optional[List[dict]] = None) -> Dict[str, str]:
    """Return {sign_label: unicode_char} for all 341 catalog entries."""
    if catalog is None:
        catalog = build_sign_catalog()
    return {entry["sign_label"]: entry["char"] for entry in catalog}


def build_char_to_id_map(catalog: Optional[List[dict]] = None) -> Dict[str, int]:
    """Return {unicode_char: sign_id} for all 341 catalog entries."""
    if catalog is None:
        catalog = build_sign_catalog()
    return {entry["char"]: entry["sign_id"] for entry in catalog}


# ---------------------------------------------------------------------------
# Transliteration → sign-label mappings
# ---------------------------------------------------------------------------
# Based on: Godart & Olivier GORILA (1976–1985); Younger online corpus.
# Phonetic assignments follow the Linear B correspondence convention used
# in scholarly transliteration of Linear A (many values remain uncertain).

PHONETIC_TO_SIGN_LABEL: Dict[str, str] = {
    # ── Vowels ──────────────────────────────────────────────────────────────
    "A":   "AB001",  "E":   "AB038",  "I":   "AB028",
    "O":   "AB061",  "U":   "AB010",
    "A2":  "AB008",  # raised-A / HA variant

    # ── Labials ─────────────────────────────────────────────────────────────
    "PA":  "AB003",  "PI":  "AB039",  "PO":  "AB011",
    "PU":  "AB050",  "PA3": "AB056",  "PU2": "AB085",

    # ── Dentals ─────────────────────────────────────────────────────────────
    "TA":  "AB059",  "TE":  "AB004",  "TI":  "AB037",
    "TO":  "AB005",  "TU":  "AB069",  "TA2": "AB066",
    "DA":  "AB045",  "DE":  "AB045",  "DI":  "AB007",
    "DU":  "AB051",

    # ── Nasals ──────────────────────────────────────────────────────────────
    "NA":  "AB006",  "NE":  "AB024",  "NI":  "AB030",
    "NO":  "AB055",  "NU":  "AB034",

    # ── Sibilants ───────────────────────────────────────────────────────────
    "SA":  "AB031",  "SE":  "AB009",  "SI":  "AB029",
    "SU":  "AB058",

    # ── Resonants ───────────────────────────────────────────────────────────
    "RA":  "AB060",  "RE":  "AB027",  "RI":  "AB053",
    "RO":  "AB002",  "RU":  "AB026",  "RA2": "AB057",

    # ── Velars ──────────────────────────────────────────────────────────────
    "KA":  "AB077",  "KE":  "AB044",  "KI":  "AB067",
    "KO":  "AB070",  "KU":  "AB081",

    # ── Labiovelars ─────────────────────────────────────────────────────────
    "QA":  "AB016",  "QE":  "AB078",  "QI":  "AB021",
    "QO":  "AB082",

    # ── Semivowels ──────────────────────────────────────────────────────────
    "JA":  "AB046",  "JU":  "AB065",
    "WA":  "AB054",  "WI":  "AB040",

    # ── Other ───────────────────────────────────────────────────────────────
    "ZA":  "AB017",  "ZU":  "AB079",  "ZO":  "AB020",
    "MA":  "AB080",  "ME":  "AB013",  "MI":  "AB022",
    "MU":  "AB023",
}

# Logogram (descriptive) names → GORILA sign labels.
# Commodity and livestock logograms are in the A300 range.
LOGOGRAM_TO_SIGN_LABEL: Dict[str, str] = {
    # ── Commodity logograms (A301–A315) ────────────────────────────────────
    "GRA":   "A301",   # grain / wheat
    "HORD":  "A302",   # barley
    "VIN":   "A303",   # wine
    "FIC":   "A304",   # figs
    "SUS":   "A305",   # pig
    "OLE":   "A306",   # olive oil
    "OLIV":  "A306",
    "CERV":  "A307",   # deer
    "CAP":   "A308",   # goat (CAPRA)
    "CAPRA": "A308",
    "OVS":   "A309A",  # sheep (OVIS) – first Unicode variant
    "OVIS":  "A309A",
    "BOS":   "A310",   # cattle (BOS)
    # ── Textiles / manufactured goods ──────────────────────────────────────
    "TELA":  "A516",   # cloth / textile (approximate GORILA reference)
    "LANA":  "A517",   # wool (approximate)
}


# ---------------------------------------------------------------------------
# Parsing and conversion
# ---------------------------------------------------------------------------

def parse_sign_groups(transliteration: str) -> List[str]:
    """Tokenise a transliteration string into sign-group tokens.

    Rules
    -----
    - Words (sign groups) are whitespace-delimited.
    - Signs within a group are joined by hyphens (kept intact).
    - Pure numeric tokens (quantities) are dropped.
    - Damage / lacuna markers (brackets, interpuncts) are stripped.

    Returns a list such as ``['A-DU', 'GRA', 'KU-RO', 'GRA']``.
    """
    # Remove damage / lacuna markers
    text = re.sub(r'\[.*?\]', ' ', transliteration)
    text = re.sub(r'\(.*?\)', ' ', text)
    text = text.replace('·', ' ').replace('•', ' ').replace(',', ' ')

    groups: List[str] = []
    for tok in text.split():
        tok = tok.strip()
        if not tok:
            continue
        # Drop pure numeric quantities (e.g. '100', '3/4', '1.5')
        if re.fullmatch(r'\d+([./]\d+)?', tok):
            continue
        # Strip trailing digits only when the token is NOT an AB/A sign label
        if not re.match(r'^(AB|A)\d', tok):
            tok = re.sub(r'\d+$', '', tok).strip()
        if tok:
            groups.append(tok)

    return groups


def sign_group_to_unicode(
        sign_group: str,
        label_map: Dict[str, str],
        phonetic_map: Optional[Dict[str, str]] = None,
        logogram_map: Optional[Dict[str, str]] = None,
) -> str:
    """Convert one sign group (e.g. ``'KU-RO'``, ``'GRA'``) to Unicode Linear A.

    Lookup order for each hyphen-separated element:
      1. Phonetic label map  (e.g. KU → AB081 → char)
      2. Logogram name map   (e.g. GRA → A301 → char)
      3. Direct sign label   (e.g. AB001, A301)
      4. Star notation       (e.g. *301 → A301)
      5. Fallback            → '?'

    Returns a concatenated Unicode string (no spaces or hyphens within group).
    """
    if phonetic_map is None:
        phonetic_map = PHONETIC_TO_SIGN_LABEL
    if logogram_map is None:
        logogram_map = LOGOGRAM_TO_SIGN_LABEL

    parts = sign_group.split('-') if '-' in sign_group else [sign_group]
    result: List[str] = []

    for part in parts:
        key = part.strip().upper()

        # 1. Phonetic label
        sl = phonetic_map.get(key)
        if sl and sl in label_map:
            result.append(label_map[sl])
            continue

        # 2. Logogram name
        sl = logogram_map.get(key)
        if sl and sl in label_map:
            result.append(label_map[sl])
            continue

        # 3. Direct sign label (AB###, A###, A###A, etc.)
        if key in label_map:
            result.append(label_map[key])
            continue

        # 4. Star notation *NNN or *NNNA
        m = re.match(r'\*(\d+[A-Z]?)$', key)
        if m:
            for candidate in (f"A{m.group(1)}", f"AB{m.group(1)}"):
                if candidate in label_map:
                    result.append(label_map[candidate])
                    break
            else:
                result.append('?')
            continue

        # 5. Unrecognised
        result.append('?')

    return ''.join(result)


def transliteration_to_unicode_string(
        transliteration: str,
        label_map: Dict[str, str],
) -> str:
    """Convert a full tablet transliteration to a segmented Unicode Linear A string.

    Sign groups are separated by a single space in the output, giving a
    human-readable segmentation of the writing into individual words.
    Unrecognised signs are rendered as '?'.
    """
    groups = parse_sign_groups(transliteration)
    return ' '.join(
        sign_group_to_unicode(g, label_map) for g in groups
    )
