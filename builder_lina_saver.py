"""
builder_lina_saver.py – Component 4: persist the database.

Responsibilities:
  - Ensure the output directory exists.
  - Save the cleaned DataFrame to a CSV file at the path specified in model.py.
"""

import os
import pandas as pd


def save_data(df: pd.DataFrame, output_path: str) -> None:
    """
    Save *df* as a CSV file at *output_path*.

    The output format is:
      - Each row  = one Linear-A list (one tablet finding).
      - Column 0  = 'date' (YYYY as integer, or empty).
      - Column 1+ = words on the tablet (word_1, word_2, …).
    """
    output_dir = os.path.dirname(output_path)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)

    df.to_csv(output_path, index=False)
    print(f"[saver] database saved to '{output_path}' ({len(df)} record(s)).")
