"""
model.py – defines LinaBaseBuilder, the top-level orchestrator for the
lina_database_builder pipeline.
"""

import os

from builder_lina_loader import load_data
from builder_lina_cleaner import clean_data
from builder_lina_validator import validate_dataframe
from builder_lina_stats import report_stats
from builder_lina_saver import save_data, save_report
from lina_sign_catalog import build_sign_catalog
from builder_qcs_registry import (
    DATA_STRATEGIES,
    get_included_strategies,
    get_excluded_strategies,
)

# ---------------------------------------------------------------------------
# Configuration – adjust these paths as needed
# ---------------------------------------------------------------------------
DATA_DIR     = os.path.join(os.path.dirname(__file__), "data", "raw")
OUTPUT_DIR   = os.path.join(os.path.dirname(__file__), "data")
RAW_CSV      = os.path.join(OUTPUT_DIR, "lina_database_raw.csv")
CLEAN_CSV    = os.path.join(OUTPUT_DIR, "lina_database_clean.csv")
REPORT_XLSX  = os.path.join(OUTPUT_DIR, "lina_report.xlsx")


class LinaBaseBuilder:
    """Top-level orchestrator that runs the full Linear-A database pipeline.

    Parameters
    ----------
    qcs_threshold : float, default 0.5
        Quality Confidence Score inclusion threshold.  Only data
        strategies whose QCS ≥ this value contribute to the final
        cleaned database and exported CSV.

        Calibration:
          0.0  – no confidence
          0.5  – more likely correct than incorrect  (default cutoff)
          0.75 – strong scholarly consensus
          1.0  – definitely correct

        Adjust this value to tighten or loosen quality requirements.
    """

    def __init__(self, qcs_threshold: float = 0.5):
        if not 0.0 <= qcs_threshold <= 1.0:
            raise ValueError(
                f"qcs_threshold must be in [0, 1], got {qcs_threshold}"
            )
        self.qcs_threshold = qcs_threshold

    # -----------------------------------------------------------------------
    # Pipeline
    # -----------------------------------------------------------------------

    def run(self):
        """Run all pipeline components sequentially."""
        print("=== LinaBaseBuilder: starting pipeline ===")
        print(f"    QCS threshold : {self.qcs_threshold}")

        included = get_included_strategies(self.qcs_threshold)
        excluded = get_excluded_strategies(self.qcs_threshold)
        print(f"    Strategies included : {len(included)} / {len(DATA_STRATEGIES)}")
        for s in included:
            print(f"      ✓ {s['label']:42s} QCS {s['qcs']:.2f}")
        for s in excluded:
            print(f"      ✗ {s['label']:42s} QCS {s['qcs']:.2f}  (below threshold)")

        # 1. Load / initialise raw data (all strategies, unfiltered)
        raw_df = load_data(DATA_DIR)

        # 1b. Validate raw data
        raw_findings = validate_dataframe(raw_df, label="raw")

        # 2. Clean data (passthrough placeholder)
        clean_df = clean_data(raw_df)

        # 3. Apply QCS threshold – keep only tablets from included strategies
        clean_df = self._apply_qcs_filter(clean_df)

        # 3b. Validate cleaned & filtered data
        clean_findings = validate_dataframe(clean_df, label="clean")

        # 4. Summary statistics & generate PNG figures
        figures = report_stats(
            clean_df,
            qcs_threshold=self.qcs_threshold,
            all_strategies=DATA_STRATEGIES,
        )

        # 5. Save CSV databases
        save_data(raw_df,   RAW_CSV)
        save_data(clean_df, CLEAN_CSV)

        # 6. Assemble xlsx report (databases + all PNG figures)
        catalog = build_sign_catalog()
        save_report(raw_df, clean_df, catalog, figures, REPORT_XLSX)

        print("=== LinaBaseBuilder: pipeline complete ===")
        print(f"    Raw CSV     : {RAW_CSV}  ({len(raw_df)} records)")
        print(f"    Clean CSV   : {CLEAN_CSV}  ({len(clean_df)} records)")
        print(f"    XLSX report : {REPORT_XLSX}")

    # -----------------------------------------------------------------------
    # QCS filter
    # -----------------------------------------------------------------------

    def _apply_qcs_filter(self, df):
        """Keep only rows whose source_strategy QCS ≥ self.qcs_threshold."""
        if "qcs" not in df.columns:
            print("[model] WARNING: no 'qcs' column – skipping QCS filter")
            return df

        before = len(df)
        filtered = df[df["qcs"] >= self.qcs_threshold].copy()
        dropped = before - len(filtered)
        print(f"[model] QCS filter (≥ {self.qcs_threshold}): "
              f"kept {len(filtered)}, dropped {dropped} of {before} records")
        return filtered
