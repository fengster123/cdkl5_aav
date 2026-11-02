r"""BLIND extraction of CDKL5 mutations from the report screenshots.

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

Run with the scratch OCR env, from the ``cdkl5_aav`` folder:
    C:\temp\ocr_env\Scripts\python.exe -m projects.chinese_mutations_survey.extract_blind_mutations

Then derive the CDKL5-only tables from the OCR text with
``build_cdkl5_blind_table.py`` (it re-tokenises with the same scanner and adds the
line/transcript-based gene attribution).
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

from projects.chinese_mutations_survey.cdna_tokens import iter_cdna_tokens, norm_width
from projects.chinese_mutations_survey.workbook_sheets import (
    MASTER,
    RAW_XLSX,
    load_all_children,
    slug_map,
)

BASE = Path(__file__).resolve().parent
SHOTS = BASE / "screenshots"
OUT_DIR = BASE / "blind_ocr"
OUT_CSV = OUT_DIR / "blind_mutations.csv"
OUT_JSONL = OUT_DIR / "ocr_text.jsonl"

FORBIDDEN = BASE / "output" / "cdkl5_cn_patients.csv"

COL_NAME, COL_WX, COL_BIRTH, COL_AREA = 2, 3, 5, 6

# Protein token, e.g. 'p.Y168Tfs*60'. The cDNA side uses the shared scanner in
# cdna_tokens.py so the survey and the screenshots are tokenised identically.
PROTEIN_RE = re.compile(r"[pP]\s*\.\s*[A-Za-z]{1,3}\d+[0-9A-Za-z_*>]*")
# 'row012_c110_陈熠泰.jpeg' (consolidated tab) or 'm202501_row005_c033_李一一.png'
ROW_COL_RE = re.compile(r"^(?:(?P<slug>[a-z][a-z0-9]*?)_)?row(?P<row>\d+)_c(?P<col>\d+)_(?P<name>.*)$")

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
    slug = (m.group("slug") or "master") if m else "master"
    row = int(m.group("row")) if m else -1
    col = int(m.group("col")) if m else -1

    started = time.time()
    result, _ = _engine()(str(path))
    elapsed = time.time() - started

    lines = [t for _, t, _ in (result or [])]
    scores = [float(s) for _, _, s in (result or [])]
    joined = "\n".join(lines)

    cdna = sorted({x for x in iter_cdna_tokens(norm_width(joined))})
    protein = sorted({x.group(0).strip() for x in PROTEIN_RE.finditer(joined)})

    return {
        "file": path.name,
        "slug": slug,
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


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=0, help="only the first N images (smoke test)")
    ap.add_argument("--workers", type=int, default=8)
    ap.add_argument("--shots", default=str(SHOTS), help="folder of screenshots to OCR")
    ap.add_argument("--out-jsonl", default=str(OUT_JSONL), help="page-level OCR output")
    ap.add_argument("--out-csv", default=str(OUT_CSV), help="per-child summary output")
    args, _ = ap.parse_known_args()

    if FORBIDDEN.name and str(FORBIDDEN) in " ".join(sys.argv):
        raise SystemExit("refusing to run: this script must stay blind to the survey output")

    shots = Path(args.shots)
    out_jsonl = Path(args.out_jsonl)
    out_csv = Path(args.out_csv)

    images = sorted(p for p in shots.glob("*") if p.is_file())
    if not images:
        raise SystemExit(f"no screenshots found in {shots}")
    if args.limit:
        images = images[: args.limit]

    print(f"images to OCR: {len(images)}   workers: {args.workers}   folder: {shots.name}")
    out_jsonl.parent.mkdir(parents=True, exist_ok=True)
    out_csv.parent.mkdir(parents=True, exist_ok=True)

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

    records.sort(key=lambda r: (r["slug"], r["form_row"], r["col"]))

    with out_jsonl.open("w", encoding="utf-8") as fh:
        for r in records:
            fh.write(json.dumps(r, ensure_ascii=False) + "\n")

    sheets = slug_map()
    children = load_all_children(list(sheets.values()))
    by_key: dict[str, list[dict]] = {}
    for r in records:
        by_key.setdefault(f"{r['slug']}:{r['form_row']}", []).append(r)

    rows = []
    for key in sorted(by_key):
        recs = by_key[key]
        info = children.get(key, {})
        cdna = sorted({t for r in recs for t in r["cdna"]})
        norm = sorted({_norm_token(t) for r in recs for t in r["cdna"]})
        protein = sorted({t for r in recs for t in r["protein"]})
        rows.append(
            {
                "child_key": key,
                "source_sheet": info.get("source_sheet", sheets.get(key.split(":")[0])),
                "form_row": int(key.split(":")[1]),
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
    df.to_csv(out_csv, index=False, encoding="utf-8-sig")

    print("")
    print(f"children with >=1 image: {len(df)}")
    print(f"children with >=1 cDNA token: {int((df['cdna_norm'] != '').sum())}")
    print(
        f"children with >1 distinct token: {int(df['cdna_norm'].str.count(';').gt(0).sum())}"
    )
    print(f"by tab:\n{df.groupby('source_sheet').size().to_string()}")
    print(f"total OCR time: {(time.time() - started) / 60:.1f} min")
    print(f"wrote {out_csv}")
    print(f"wrote {out_jsonl}")


if __name__ == "__main__":
    main()
