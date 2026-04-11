"""
main.py – entry point for the lina_database_builder pipeline.

Run with:
    python main.py
"""

from model import LinaBaseBuilder


if __name__ == "__main__":
    builder = LinaBaseBuilder()
    builder.run()
