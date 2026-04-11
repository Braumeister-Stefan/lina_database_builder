"""
model.py – defines LinaBaseBuilder, the top-level orchestrator for the
lina_database_builder pipeline.
"""

import os

from builder_lina_loader import load_data
from builder_lina_cleaner import clean_data
from builder_lina_stats import report_stats
from builder_lina_saver import save_data, save_report
from lina_sign_catalog import build_sign_catalog

# ---------------------------------------------------------------------------
# Configuration – adjust these paths as needed
# ---------------------------------------------------------------------------
DATA_DIR     = os.path.join(os.path.dirname(__file__), "data", "raw")
OUTPUT_DIR   = os.path.join(os.path.dirname(__file__), "data")
RAW_CSV      = os.path.join(OUTPUT_DIR, "lina_database_raw.csv")
CLEAN_CSV    = os.path.join(OUTPUT_DIR, "lina_database_clean.csv")
REPORT_XLSX  = os.path.join(OUTPUT_DIR, "lina_report.xlsx")


class LinaBaseBuilder:
    """Top-level orchestrator that runs the full Linear-A database pipeline."""

    def run(self):
        """Run all pipeline components sequentially."""
        print("=== LinaBaseBuilder: starting pipeline ===")

        # 1. Load / initialise raw data
        raw_df = load_data(DATA_DIR)

        # 2. Clean data (passthrough placeholder)
        clean_df = clean_data(raw_df)

        # 3. Summary statistics & generate PNG figures
        figures = report_stats(clean_df)

        # 4. Save CSV databases
        save_data(raw_df,   RAW_CSV)
        save_data(clean_df, CLEAN_CSV)

        # 5. Assemble xlsx report (databases + all PNG figures)
        catalog = build_sign_catalog()
        save_report(raw_df, clean_df, catalog, figures, REPORT_XLSX)

        print("=== LinaBaseBuilder: pipeline complete ===")
        print(f"    Raw CSV     : {RAW_CSV}")
        print(f"    Clean CSV   : {CLEAN_CSV}")
        print(f"    XLSX report : {REPORT_XLSX}")
