"""
lina_site_coordinates.py – Geographic coordinates for Linear A find-sites.

Sites are on the island of Crete, Greece, or the broader Aegean region
(Akrotiri/Thera is on the island of Santorini).
Coordinates are WGS-84 decimal degrees (lat N, lon E).

Sources
-------
  Godart & Olivier GORILA (1976-1985), site provenances.
  Standard geographic references for Cretan Bronze Age sites.
"""

from typing import Dict, Any
import pandas as pd

# ---------------------------------------------------------------------------
# Site coordinate lookup
# ---------------------------------------------------------------------------
# Each entry: lat (decimal degrees N), lon (decimal degrees E), island
SITE_COORDINATES: Dict[str, Dict[str, Any]] = {
    "Hagia Triada": {"lat": 35.060, "lon": 24.798, "island": "Crete"},
    "Phaistos":     {"lat": 35.052, "lon": 24.808, "island": "Crete"},
    "Zakros":       {"lat": 35.099, "lon": 26.260, "island": "Crete"},
    "Khania":       {"lat": 35.513, "lon": 24.018, "island": "Crete"},
    "Knossos":      {"lat": 35.298, "lon": 25.163, "island": "Crete"},
    "Arkhanes":     {"lat": 35.161, "lon": 25.163, "island": "Crete"},
    "Mallia":       {"lat": 35.296, "lon": 25.469, "island": "Crete"},
    "Tylissos":     {"lat": 35.307, "lon": 25.010, "island": "Crete"},
    "Palaikastro":  {"lat": 35.208, "lon": 26.241, "island": "Crete"},
    # Aegean (non-Cretan) site
    "Akrotiri":     {"lat": 36.352, "lon": 25.406, "island": "Thera"},
    # Minor Cretan sites
    "Gournia":      {"lat": 35.178, "lon": 25.696, "island": "Crete"},
    "Nirou Khani":  {"lat": 35.333, "lon": 25.344, "island": "Crete"},
    "Myrtos":       {"lat": 34.935, "lon": 25.641, "island": "Crete"},
    "Apodioulou":   {"lat": 35.179, "lon": 24.634, "island": "Crete"},
}

# Simplified coastline polygon for Crete (lon, lat order for matplotlib).
# Approximate outline, suitable for map backgrounds at 1:2 000 000 scale.
CRETE_OUTLINE = [
    (23.52, 35.55), (23.75, 35.62), (24.00, 35.61), (24.25, 35.57),
    (24.50, 35.55), (24.75, 35.43), (25.00, 35.35), (25.25, 35.30),
    (25.50, 35.27), (25.75, 35.22), (26.00, 35.19), (26.20, 35.18),
    (26.35, 35.21), (26.30, 35.05), (26.10, 34.96), (25.85, 34.93),
    (25.55, 35.00), (25.25, 35.03), (25.00, 35.05), (24.75, 35.00),
    (24.50, 34.92), (24.25, 34.88), (24.00, 34.88), (23.80, 35.02),
    (23.60, 35.20), (23.52, 35.55),
]

# Simplified outline for mainland Greece / Peloponnese (lon, lat).
GREECE_OUTLINE = [
    (20.0, 42.1), (21.0, 41.3), (22.0, 41.1), (23.0, 41.4),
    (24.0, 41.1), (25.0, 41.3), (26.0, 41.0), (26.5, 40.7),
    (26.0, 40.2), (25.5, 40.5), (25.0, 40.8), (24.5, 40.6),
    (24.0, 40.0), (23.5, 38.8), (23.0, 38.0), (22.5, 37.5),
    (22.0, 37.0), (21.8, 36.9), (21.5, 37.3), (21.3, 38.0),
    (21.0, 38.5), (20.7, 39.2), (20.3, 40.0), (20.1, 41.0),
    (20.0, 42.1),
]

# Simplified western Turkey coast (lon, lat).
TURKEY_W_OUTLINE = [
    (26.5, 40.7), (26.3, 40.2), (26.2, 39.8), (26.5, 39.2),
    (27.0, 38.5), (27.5, 37.8), (27.8, 37.3), (28.0, 36.8),
    (28.2, 36.4), (28.0, 36.2), (27.5, 36.5), (27.0, 36.8),
    (26.8, 37.2), (26.4, 38.0), (26.1, 38.5), (26.0, 39.0),
    (26.5, 40.7),
]


def get_site_summary_df(corpus_df: pd.DataFrame) -> pd.DataFrame:
    """Return a per-site summary DataFrame with coordinates and tablet counts.

    Columns: site, lat, lon, island, tablet_count, clay_count, stone_count,
             date_min_bce, date_max_bce
    """
    rows = []
    for site, grp in corpus_df.groupby("site"):
        coords = SITE_COORDINATES.get(site, {"lat": None, "lon": None, "island": "unknown"})
        dates = grp["date_est"].dropna()
        rows.append({
            "site":          site,
            "lat":           coords["lat"],
            "lon":           coords["lon"],
            "island":        coords["island"],
            "tablet_count":  len(grp),
            "clay_count":    int((grp["material"] == "clay").sum()),
            "stone_count":   int((grp["material"] == "stone").sum()),
            "date_min_bce":  int(abs(dates.min())) if not dates.empty else None,
            "date_max_bce":  int(abs(dates.max())) if not dates.empty else None,
        })
    return pd.DataFrame(rows).sort_values("tablet_count", ascending=False).reset_index(drop=True)
