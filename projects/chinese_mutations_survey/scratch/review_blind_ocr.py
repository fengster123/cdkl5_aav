"""Reviewer-side sanity checks for the BLIND OCR extraction.

Reads ONLY the blind extraction outputs:
    blind_ocr/blind_mutations.csv
    blind_ocr/ocr_text.jsonl

It never touches output/cdkl5_cn_patients.csv, the .md transcriptions, or the
survey workbook, so the blind comparison stays clean.

Run:
    & "C:\\temp\\ocr_env\\Scripts\\python.exe" scratch\\review_blind_ocr.py
"""

from __future__ import annotations

import json
import re
from collections import Counter
from pathlib import Path

import pandas as pd

BASE = Path(__file__).resolve().parent.parent
CSV = BASE / "blind_ocr" / "blind_mutations.csv"
JSONL = BASE / "blind_ocr" / "ocr_text.jsonl"

pd.set_option("display.width", 250)
pd.set_option("display.max_colwidth", 200)
pd.set_option("display.max_rows", 500)


def sep(title: str) -> None:
    print("\n" + "=" * 78)
    print(title)
    print("=" * 78)


def main() -> None:
    df = pd.read_csv(CSV, encoding="utf-8-sig", dtype=object)
    recs = [json.loads(line) for line in JSONL.read_text(encoding="utf-8").splitlines() if line.strip()]

    sep("1. blind_mutations.csv shape / columns")
    print(f"rows: {len(df)}")
    print(f"columns ({len(df.columns)}): {list(df.columns)}")

    sep("2. per-image (ocr_text.jsonl)")
    print(f"image records: {len(recs)}")
    n_img_with_cdna = sum(1 for r in recs if r["cdna"])
    print(f"images with >=1 cDNA token: {n_img_with_cdna}")
    print(f"images with 0 cDNA token:   {len(recs) - n_img_with_cdna}")

    sep("3. children coverage")
    n_children = len(df)
    has_token = df["cdna_norm"].fillna("").astype(str).str.strip() != ""
    print(f"children with >=1 image:      {n_children}")
    print(f"children with >=1 cDNA token: {int(has_token.sum())}")
    print(f"children with 0 cDNA token:   {int((~has_token).sum())}")
    multi = df[df["cdna_norm"].fillna("").astype(str).str.contains(";")]
    print(f"children with >1 distinct normalized token: {len(multi)}")
    for _, r in multi.iterrows():
        print(f"  row={r['form_row']}  name={r['real_name']}  wx={r['wx_nickname']}  norm={r['cdna_norm']}")
        print(f"      raw={r['cdna_tokens']}")

    sep("4. children with no token at all")
    empty = df[~has_token]
    for _, r in empty.iterrows():
        print(f"  row={r['form_row']}  name={r['real_name']}  n_images={r['n_images']}  protein='{r['protein_tokens']}'")

    sep("5. images with no OCR text at all")
    no_text = [r for r in recs if r["n_lines"] == 0]
    print(f"count: {len(no_text)}")
    for r in no_text:
        print(f"  {r['file']}  score={r['mean_score']}  seconds={r['seconds']}")

    sep("6. images with mean confidence < 0.90")
    low = sorted([r for r in recs if r["mean_score"] < 0.90], key=lambda r: r["mean_score"])
    print(f"count: {len(low)}")
    for r in low:
        print(f"  {r['file']}  mean={r['mean_score']}  min={r['min_score']}  lines={r['n_lines']}  cdna={r['cdna']}")

    sep("7. token inventory (raw -> count of images)")
    raw_counts: Counter[str] = Counter()
    for r in recs:
        for t in r["cdna"]:
            raw_counts[t] += 1
    print(f"distinct raw tokens: {len(raw_counts)}")
    for t, c in sorted(raw_counts.items(), key=lambda kv: (-kv[1], kv[0])):
        print(f"  {c:3d}  {t!r}")

    sep("8. suspicious tokens")
    # A clean token should look like  c.<digits><change>  and contain a '>' or a del/ins marker
    WELL_FORMED = re.compile(r"^c\.\d+[ACGT]?>[ACGT]?$|^c\.\d+_\d+(del|ins|dup)[A-Z]*$")
    suspicious = []
    for t, c in raw_counts.items():
        norm = t.replace(" ", "").replace("＞", ">").replace("，", ",")
        if not WELL_FORMED.match(norm):
            suspicious.append((t, norm, c))
    print(f"count: {len(suspicious)}")
    for t, norm, c in sorted(suspicious):
        print(f"  raw={t!r}  norm={norm!r}  images={c}")

    sep("9. required metadata non-null counts")
    for col in ["form_row", "real_name", "wx_nickname", "birth_raw", "area"]:
        s = df[col]
        print(f"  {col:12s} non-null={int(s.notna().sum()):4d}  null={int(s.isna().sum()):4d}")

    sep("10. images per child distribution")
    print(df["n_images"].astype(int).describe().to_string())
    print(f"total images assigned: {int(df['n_images'].astype(int).sum())}")
    print(f"images OCR'd:          {len(recs)}")

    sep("11. children whose name is missing from the workbook mapping")
    miss = df[df["real_name"].isna()]
    print(f"count: {len(miss)}")
    for _, r in miss.iterrows():
        print(f"  row={r['form_row']}  n_images={r['n_images']}  tokens={r['cdna_norm']}")

    sep("12. OCR timing")
    tot = sum(r["seconds"] for r in recs)
    print(f"sum of per-image ocr seconds: {tot:.1f}s ({tot/60:.1f} min)")
    print(f"mean per-image: {tot/len(recs):.2f}s   max: {max(r['seconds'] for r in recs):.2f}s")


if __name__ == "__main__":
    main()
