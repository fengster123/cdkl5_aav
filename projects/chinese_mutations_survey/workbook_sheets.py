"""Sheet inventory for the raw submission workbook.

The workbook holds **25 tabs that carry embedded report screenshots** (1,718 images
in total), not one: the consolidated ``希舞宝贝情况登记（收集结果）`` tab (490), an
identical ``(副本)`` copy (471), a ``20241201-20241231`` monthly tab (483) and 22
monthly tabs from 2025-01 to 2026-09 (274). Only the consolidated tab was used by
the first extraction pass, which is why this module exists: every consumer
(export, OCR, table build, linkage) now keys a child by ``child_key`` =
``"{sheet_slug}:{excel_row}"`` instead of by an Excel row number that is only
unique inside one tab.

Column layout
-------------
``COL_NAME``, ``COL_WX``, ``COL_BIRTH``, ``COL_AREA`` are 0-based positions and are
the same on every tab. The *screenshot* columns differ (110-115 on the consolidated
tab, 32-37 on the monthly tabs), so screenshots are always located by their anchor
rather than by a hard-coded column.
"""

from __future__ import annotations

import hashlib
import re
from pathlib import Path

import pandas as pd

RAW_XLSX = Path(r"C:\temp\希舞宝贝情况登记（收集结果）.xlsx")

MASTER = "希舞宝贝情况登记（收集结果）"
COPY_SUFFIX = "(副本)"

COL_NAME, COL_WX, COL_BIRTH, COL_AREA = 2, 3, 5, 6

# '20250101-20250131（收集结果）'
_MONTHLY_RE = re.compile(r"^(\d{8})-(\d{8})\s*[（(]收集结果[)）]\s*$")
_NON_IMAGE_RE = re.compile(r"^(工作表|智能表)")


def sheet_slug(sheet: str) -> str:
    """Short, filename-safe tab identifier: ``master``, ``m202501``, ``master_copy``."""
    if sheet == MASTER:
        return "master"
    if sheet.endswith(COPY_SUFFIX):
        return sheet_slug(sheet[: -len(COPY_SUFFIX)]) + "_copy"
    m = _MONTHLY_RE.match(sheet)
    if m:
        return "m" + m.group(1)[:6]
    slug = re.sub(r"[^0-9a-z]+", "", sheet.lower())
    # '工作表1' / '智能表2' have no ASCII at all and must still be distinguishable
    return slug or "s" + hashlib.sha1(sheet.encode("utf-8")).hexdigest()[:6]


def is_monthly(sheet: str) -> bool:
    return bool(_MONTHLY_RE.match(sheet))


def ordered_sheets(sheetnames: list[str]) -> list[str]:
    """Consolidated tab first, then monthly newest→oldest, then everything else.

    Priority order matters: images are de-duplicated by content hash, so the first
    tab that carries a photo owns it. Starting with the consolidated tab keeps the
    490 images already OCR'd attached to the rows they were extracted from.
    """
    monthly = sorted((s for s in sheetnames if is_monthly(s)), reverse=True)
    copy_tabs = [s for s in sheetnames if s.endswith(COPY_SUFFIX)]
    others = [
        s for s in sheetnames
        if s != MASTER and s not in monthly and s not in copy_tabs
        and not _NON_IMAGE_RE.match(s)
    ]
    head = [MASTER] if MASTER in sheetnames else []
    return head + monthly + others + copy_tabs


def child_key(sheet: str, excel_row: int) -> str:
    """Globally unique child id: the Excel row is only unique inside its own tab."""
    return f"{sheet_slug(sheet)}:{int(excel_row)}"


_FRAMES: dict[str, pd.DataFrame] | None = None


def _all_frames() -> dict[str, pd.DataFrame]:
    """Every tab as a raw frame, read in one open so 28 tabs do not re-parse the file."""
    global _FRAMES
    if _FRAMES is None:
        _FRAMES = pd.read_excel(RAW_XLSX, sheet_name=None, header=None, dtype=object)
    return _FRAMES


def _sheet_frame(sheet: str) -> pd.DataFrame:
    frames = _all_frames()
    if sheet not in frames:
        raise KeyError(f"sheet {sheet!r} not in {RAW_XLSX}")
    return frames[sheet]


def load_children(sheet: str = MASTER) -> dict[int, dict]:
    """Excel row (1-based) -> {real_name, wx_nickname, birth_raw, area, source_sheet}.

    Rows without a child name are skipped: every other column in the form is
    optional, but a submission always carries the child's name.
    """
    raw = _sheet_frame(sheet)
    out: dict[int, dict] = {}
    if raw.shape[1] <= COL_NAME:
        return out
    for excel_row in range(2, len(raw) + 1):  # Excel row 1 is the header
        rec = raw.iloc[excel_row - 1]
        name = rec.iloc[COL_NAME]
        if pd.isna(name) or not str(name).strip():
            continue
        out[excel_row] = {
            "real_name": str(name).strip(),
            "wx_nickname": rec.iloc[COL_WX] if pd.notna(rec.iloc[COL_WX]) else None,
            "birth_raw": rec.iloc[COL_BIRTH] if pd.notna(rec.iloc[COL_BIRTH]) else None,
            "area": rec.iloc[COL_AREA] if pd.notna(rec.iloc[COL_AREA]) else None,
            "source_sheet": sheet,
            "form_row": excel_row,
            "child_key": child_key(sheet, excel_row),
        }
    return out


def load_all_children(sheets: list[str] | None = None) -> dict[str, dict]:
    """``child_key`` -> child info, for every tab that carries screenshots."""
    names = _sheetnames()
    todo = sheets if sheets is not None else ordered_sheets(names)
    out: dict[str, dict] = {}
    for sheet in todo:
        for info in load_children(sheet).values():
            key = info["child_key"]
            if key in out:
                raise ValueError(f"duplicate child_key {key}")
            out[key] = info
    return out


def _sheetnames() -> list[str]:
    import openpyxl

    return openpyxl.load_workbook(RAW_XLSX, read_only=True).sheetnames


def slug_map() -> dict[str, str]:
    """``{slug: sheet name}`` for every tab, so an exported filename resolves back."""
    return {sheet_slug(s): s for s in _sheetnames()}


def sheet_of_key(key: str) -> str:
    """Sheet name for a ``child_key``; ``''`` when the slug is unknown.

    Used when a row arrives without a ``source_sheet`` column — the v1 tables
    predate the multi-tab layout and carry only a tab-local ``form_row``.
    """
    slug = str(key).partition(":")[0]
    return slug_map().get(slug, "")
