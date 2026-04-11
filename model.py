"""
model.py – defines LinaBaseBuilder, the top-level orchestrator for the
lina_database_builder pipeline.
"""

import os

from builder_lina_loader import load_data
from builder_lina_cleaner import clean_data
from builder_lina_stats import report_stats
from builder_lina_saver import save_data

# ---------------------------------------------------------------------------
# Configuration – adjust these paths as needed
# ---------------------------------------------------------------------------
DATA_DIR = os.path.join(os.path.dirname(__file__), "data", "raw")
OUTPUT_PATH = os.path.join(os.path.dirname(__file__), "data", "lina_database.csv")


class LinaBaseBuilder:
    """Top-level orchestrator that runs the full Linear-A database pipeline."""

    def run(self):
        """Run all pipeline components sequentially."""
        print("=== LinaBaseBuilder: starting pipeline ===")

        # 1. Load / initialise raw data
        raw_df = load_data(DATA_DIR)

        # 2. Clean data
        clean_df = clean_data(raw_df)

        # 3. Summary statistics & visualisation
        report_stats(clean_df)

        # 4. Save database
        save_data(clean_df, OUTPUT_PATH)

        print("=== LinaBaseBuilder: pipeline complete ===")
