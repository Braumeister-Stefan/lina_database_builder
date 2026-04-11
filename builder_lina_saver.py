"""
builder_lina_saver.py – Component 4: persist databases and assemble xlsx report.

Responsibilities:
  - save_data()   : save a DataFrame as CSV.
  - save_report() : assemble a multi-tab xlsx workbook containing:
      * Raw database (as a worksheet table)
      * Cleaned database (as a worksheet table)
      * Sign catalog (as a worksheet table)
      * One tab per PNG figure / table image (title in row 1, image in row 2)
"""

import os
from typing import List, Tuple

import pandas as pd
import openpyxl
from openpyxl import Workbook
from openpyxl.drawing.image import Image as XLImage
from openpyxl.styles import Font, Alignment, PatternFill, Border, Side
from openpyxl.utils import get_column_letter


# ---------------------------------------------------------------------------
# CSV saver (unchanged from original)
# ---------------------------------------------------------------------------

def save_data(df: pd.DataFrame, output_path: str) -> None:
    """Save *df* as a CSV file at *output_path*."""
    output_dir = os.path.dirname(output_path)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f"[saver] database saved to '{output_path}' ({len(df)} record(s)).")


# ---------------------------------------------------------------------------
# XLSX report assembler
# ---------------------------------------------------------------------------

def save_report(
        raw_df:    pd.DataFrame,
        clean_df:  pd.DataFrame,
        catalog:   List[dict],
        figures:   List[Tuple[str, str, str]],
        xlsx_path: str,
) -> None:
    """Assemble the full xlsx report.

    Parameters
    ----------
    raw_df    : raw corpus DataFrame
    clean_df  : cleaned corpus DataFrame (passthrough for now)
    catalog   : list of sign-catalog dicts from build_sign_catalog()
    figures   : list of (tab_name, title, png_path) from report_stats()
    xlsx_path : destination file path
    """
    output_dir = os.path.dirname(xlsx_path)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)

    wb = Workbook()
    # Remove default empty sheet
    wb.remove(wb.active)

    # ── DataFrame tabs ──────────────────────────────────────────────────
    _df_to_sheet(wb, raw_df,   "Raw Database",     "Linear A Corpus – Raw Database")
    _df_to_sheet(wb, clean_df, "Clean Database",   "Linear A Corpus – Cleaned Database")

    catalog_df = pd.DataFrame(catalog)[
        ["sign_label", "category", "hex_code", "unicode_name"]
    ].rename(columns={
        "sign_label":   "Sign Label",
        "category":     "Category",
        "hex_code":     "Unicode Hex",
        "unicode_name": "Unicode Name",
    })
    _df_to_sheet(wb, catalog_df, "Sign Catalog", "Linear A – Complete Sign Catalog (341 signs)")

    # ── PNG figure tabs ─────────────────────────────────────────────────
    for tab_name, title, png_path in figures:
        if not os.path.exists(png_path):
            print(f"[saver] WARNING: PNG not found, skipping tab '{tab_name}'")
            continue
        _png_to_sheet(wb, tab_name, title, png_path)

    wb.save(xlsx_path)
    print(f"[saver] xlsx report saved to '{xlsx_path}'  "
          f"({len(wb.sheetnames)} tabs).")


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

_HEADER_FILL  = PatternFill("solid", fgColor="2C3E50")
_HEADER_FONT  = Font(color="FFFFFF", bold=True, size=10)
_TITLE_FONT   = Font(bold=True, size=13)
_ALT_FILL     = PatternFill("solid", fgColor="F2F2F2")
_THIN_BORDER  = Border(
    left=Side(style="thin"), right=Side(style="thin"),
    top=Side(style="thin"),  bottom=Side(style="thin"),
)


def _df_to_sheet(wb: Workbook, df: pd.DataFrame,
                 sheet_name: str, title: str) -> None:
    """Write a DataFrame to a new worksheet as a formatted table."""
    ws = wb.create_sheet(title=sheet_name[:31])

    # Title row
    ws.merge_cells(start_row=1, start_column=1,
                   end_row=1, end_column=len(df.columns))
    ws["A1"] = title
    ws["A1"].font      = _TITLE_FONT
    ws["A1"].alignment = Alignment(horizontal="left", vertical="center")
    ws.row_dimensions[1].height = 22

    # Header row (row 2)
    for col_idx, col_name in enumerate(df.columns, start=1):
        cell             = ws.cell(row=2, column=col_idx, value=str(col_name))
        cell.font        = _HEADER_FONT
        cell.fill        = _HEADER_FILL
        cell.alignment   = Alignment(horizontal="center", vertical="center")
        cell.border      = _THIN_BORDER
    ws.row_dimensions[2].height = 18

    # Data rows
    for row_idx, row in enumerate(df.itertuples(index=False), start=3):
        for col_idx, value in enumerate(row, start=1):
            # Convert pandas NA / numpy types to plain Python
            if pd.isna(value):
                value = ""
            elif hasattr(value, "item"):
                value = value.item()
            cell           = ws.cell(row=row_idx, column=col_idx, value=value)
            cell.border    = _THIN_BORDER
            cell.alignment = Alignment(vertical="center", wrap_text=False)
            if row_idx % 2 == 0:
                cell.fill = _ALT_FILL

    # Auto-width (cap at 60)
    for col_idx, col_name in enumerate(df.columns, start=1):
        max_len = max(
            len(str(col_name)),
            df.iloc[:, col_idx - 1].astype(str).str.len().max() if len(df) else 0,
        )
        ws.column_dimensions[get_column_letter(col_idx)].width = min(max_len + 3, 60)


def _png_to_sheet(wb: Workbook, sheet_name: str,
                  title: str, png_path: str) -> None:
    """Create a new worksheet with a title row and the PNG embedded below."""
    ws = wb.create_sheet(title=sheet_name[:31])

    ws["A1"] = title
    ws["A1"].font      = _TITLE_FONT
    ws["A1"].alignment = Alignment(horizontal="left", vertical="center")
    ws.row_dimensions[1].height = 22

    img = XLImage(png_path)
    # Fit image within roughly 1200 px wide at 96 dpi ≈ 900 pt wide
    max_w_px = 1100
    if img.width > max_w_px:
        scale   = max_w_px / img.width
        img.width  = int(img.width  * scale)
        img.height = int(img.height * scale)

    ws.add_image(img, "A2")
    # Expand row 2 to make the image visible in the sheet
    ws.row_dimensions[2].height = max(15, img.height * 0.75)
