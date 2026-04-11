"""
main.py – entry point for the lina_database_builder pipeline.

Run with:
    python main.py
    python main.py --qcs-threshold 0.6    # stricter quality filter
"""

import argparse

from model import LinaBaseBuilder


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Build the Linear A database from embedded corpus data."
    )
    parser.add_argument(
        "--qcs-threshold",
        type=float,
        default=0.5,
        help="Quality Confidence Score inclusion threshold (default: 0.5). "
             "Only strategies with QCS >= this value are included.",
    )
    args = parser.parse_args()

    builder = LinaBaseBuilder(qcs_threshold=args.qcs_threshold)
    builder.run()
