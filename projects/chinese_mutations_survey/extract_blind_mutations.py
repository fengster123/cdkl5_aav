"""BLIND extraction of CDKL5 mutations from the report screenshots.

This script exists to be run without any knowledge of the already-transcribed
values. It reads:

  * the raw form workbook  C:\\temp\\希舞宝贝情况登记（收集结果）.xlsx
    (child name, WeChat nickname, birth date, area) — never the mutation column
  * the extracted report screenshots in  projects/chinese_mutations_survey/screenshots

and writes  projects/chinese_mutations_survey/blind_ocr/blind_mutations.csv

It deliberately does NOT read ``output/cdkl5_cn_patients.csv`` and there is a
runtime guard that aborts if that path is ever passed to it.

Output columns
--------------
form_row        Excel row in the raw workbook (1-based)
real_name       孩子姓名
wx_nickname     微信群昵称
birth_raw       出生日期 (raw as stored)
area            所在地区（省市）
n_images        how many screenshots are attached to this child
cdna_tokens     every distinct cDNA token OCR found, '; '-joined (raw OCR spelling)
cdna_norm       same tokens normalised (upper, spaces removed), '; '-joined
protein_tokens  every distinct p. token found
n_pages_without_token  screenshots that yielded no cDNA token
ocr_seconds     total OCR time for this child

Companion file ``ocr_text.jsonl`` holds the full text of every screenshot so the
extraction can be audited line by line.

Run with the scratch OCR env:
    C:\\temp\\ocr_env\\Scripts\\python.exe extract_blind_mutations.py [--limit N] [--workers W]
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import time
from multiprocessing import Pool
from pathlib import Path

import pandas as pd

BASE = Path(__file__).resolve().parent
RAW_XLSX = Path(r"C:\temp\希舞宝贝情况登记（收集结果）.xlsx")
SHOTS = BASE / "screenshots"
OUT_DIR = BASE / "blind_ocr"
OUT_CSV = OUT_DIR / "blind_mutations.csv"
OUT_JSONL = OUT_DIR / "ocr_text.jsonl"

FORBIDDEN = BASE / "output" / "cdkl5_cn_patients.csv"

MASTER = "希舞宝贝情况登记（收集结果）"
COL_NAME, COL_WX, COL_BIRTH, COL_AREA = 2, 3, 5, 6

# cDNA token: 'c.' + position, then the rest of the change.
CDNA_RE = re.compile(r"[cC]\s*[.\-·]\s*\d[0-9A-Za-z_+\->.*]*")
PROTEIN_RE = re.compile(r"[pP]\s*\.\s*[A-Za-z]{1,3}\d+[0-9A-Za-z_*>]*")
ROW_COL_RE = re.compile(r"^row(\d+)_c(\d+)_(.*)$")

_ENGINE = None


def _engine():
    global _ENGINE
    if _ENGINE is None:
        from rapidocr_onnxruntime import RapidOCR

        _ENGINE = RapidOCR()
    return _ENGINE


def _norm_token(t: str) -> str:
    s = re.sub(r"\s+", "", t)
    s = s.replace("＞", ">").replace("，", ",").replace("：", ":")
    return s.upper()


def ocr_one(path_str: str) -> dict:
    """OCR a single image. Runs in a worker process."""
    path = Path(path_str)
    m = ROW_COL_RE.match(path.stem)
    row = int(m.group(1)) if m else -1
    col = int(m.group(2)) if m else -1

    started = time.time()
    result, _ = _engine()(str(path))
    elapsed = time.time() - started

    lines = [t for _, t, _ in (result or [])]
    scores = [float(s) for _, _, s in (result or [])]
    joined = "\n".join(lines)

    cdna = sorted({x.group(0).strip() for x in CDNA_RE.finditer(joined)})
    protein = sorted({x.group(0).strip() for x in PROTEIN_RE.finditer(joined)})

    return {
        "file": path.name,
        "form_row": row,
        "col": col,
        "seconds": round(elapsed, 2),
        "n_lines": len(lines),
        "mean_score": round(sum(scores) / len(scores), 3) if scores else 0.0,
        "min_score": round(min(scores), 3) if scores else 0.0,
        "cdna": cdna,
        "protein": protein,
        "text": joined,
    }


def load_children() -> dict[int, dict]:
    """form_row (Excel 1-based) -> child info, for rows that have a name."""
    raw = pd.read_excel(RAW_XLSX, sheet_name=MASTER, header=None, dtype=object)
    out: dict[int, dict] = {}
    for excel_row in range(2, len(raw) + 1):  # Excel row 1 is the header
        rec = raw.iloc[excel_row - 1]
        name = rec.iloc[COL_NAME]
        if pd.isna(name):
            continue
        out[excel_row] = {
            "real_name": str(name).strip(),
            "wx_nickname": rec.iloc[COL_WX] if pd.notna(rec.iloc[COL_WX]) else None,
            "birth_raw": rec.iloc[COL_BIRTH] if pd.notna(rec.iloc[COL_BIRTH]) else None,
            "area": rec.iloc[COL_AREA] if pd.notna(rec.iloc[COL_AREA]) else None,
        }
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--limit", type=int, default=0, help="only the first N images (smoke test)"
    )
    ap.add_argument("--workers", type=int, default=8)
    args, _ = ap.parse_known_args()

    if FORBIDDEN.name and str(FORBIDDEN) in " ".join(sys.argv):
        raise SystemExit(
            "refusing to run: this script must stay blind to the survey output"
        )

    images = sorted(SHOTS.glob("row*"))
    if not images:
        raise SystemExit(f"no screenshots found in {SHOTS}")
    if args.limit:
        images = images[: args.limit]

    print(f"images to OCR: {len(images)}   workers: {args.workers}")
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    started = time.time()
    records: list[dict] = []
    with Pool(processes=args.workers) as pool:
        for i, rec in enumerate(
            pool.imap_unordered(ocr_one, [str(p) for p in images], chunksize=4), 1
        ):
            records.append(rec)
            if i % 25 == 0 or i == len(images):
                rate = (time.time() - started) / i
                print(
                    f"  {i}/{len(images)}  {rate:.1f}s/image  eta {(len(images) - i) * rate / 60:.1f} min"
                )

    records.sort(key=lambda r: (r["form_row"], r["col"]))

    with OUT_JSONL.open("w", encoding="utf-8") as fh:
        for r in records:
            fh.write(json.dumps(r, ensure_ascii=False) + "\n")

    children = load_children()
    by_row: dict[int, list[dict]] = {}
    for r in records:
        by_row.setdefault(r["form_row"], []).append(r)

    rows = []
    for form_row in sorted(by_row):
        recs = by_row[form_row]
        info = children.get(form_row, {})
        cdna = sorted({t for r in recs for t in r["cdna"]})
        norm = sorted({_norm_token(t) for r in recs for t in r["cdna"]})
        protein = sorted({t for r in recs for t in r["protein"]})
        rows.append(
            {
                "form_row": form_row,
                "real_name": info.get("real_name"),
                "wx_nickname": info.get("wx_nickname"),
                "birth_raw": info.get("birth_raw"),
                "area": info.get("area"),
                "n_images": len(recs),
                "cdna_tokens": "; ".join(cdna),
                "cdna_norm": "; ".join(norm),
                "protein_tokens": "; ".join(protein),
                "n_pages_without_token": sum(1 for r in recs if not r["cdna"]),
                "ocr_seconds": round(sum(r["seconds"] for r in recs), 1),
                "min_page_score": min((r["min_score"] for r in recs), default=0.0),
            }
        )

    df = pd.DataFrame(rows)
    df.to_csv(OUT_CSV, index=False, encoding="utf-8-sig")

    print("")
    print(f"children with >=1 image: {len(df)}")
    print(f"children with >=1 cDNA token: {int((df['cdna_norm'] != '').sum())}")
    print(
        f"children with >1 distinct token: {int(df['cdna_norm'].str.count(';').gt(0).sum())}"
    )
    print(f"total OCR time: {(time.time() - started) / 60:.1f} min")
    print(f"wrote {OUT_CSV}")
    print(f"wrote {OUT_JSONL}")


if __name__ == "__main__":
    main()
