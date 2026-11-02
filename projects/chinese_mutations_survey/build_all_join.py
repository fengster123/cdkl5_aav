"""Build ``blind_ocr/comparison_all_join.csv`` — a full outer join of both sides.

``comparison.csv`` is a **left** join: it has one row per child with screenshots
(197) and drops the survey rows that no child matched. This script keeps
everything, tagging each row with which side(s) it came from:

* ``both``              — child with screenshots and a matched survey row
* ``screenshots_only``  — child with screenshots, no survey row could be matched
* ``survey_only``       — survey row that no child with screenshots matched

``outcome`` keeps its ``comparison.csv`` meaning for ``both``; the extra sides get
``UNLINKED`` (screenshots only) and ``SURVEY_ONLY`` (survey only).

Run from the ``cdkl5_aav`` folder:

    python -m projects.chinese_mutations_survey.build_all_join
"""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

BASE = Path(__file__).resolve().parent
SURVEY_CSV = BASE / "output" / "cdkl5_cn_patients.csv"
CMP_CSV = BASE / "blind_ocr" / "comparison.csv"
OUT_CSV = BASE / "blind_ocr" / "comparison_all_join.csv"

OUT_COLS = [
    "join_side", "child_key", "source_sheet", "form_row", "real_name", "wx_nickname",
    "survey_idx", "survey_nick", "match_basis",
    "survey_mutation", "blind_tokens", "n_ocr_tokens", "blind_status",
    "outcome", "detail", "survey_birth", "blind_birth", "survey_area", "blind_area",
]


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true", help="print the summary, write nothing")
    args, _ = ap.parse_known_args()

    for path in (SURVEY_CSV, CMP_CSV):
        if not path.exists():
            raise SystemExit(f"missing {path}\nrun rescore_blind_comparison.py first")

    cmp_df = pd.read_csv(CMP_CSV, encoding="utf-8-sig", dtype=object)
    survey = pd.read_csv(SURVEY_CSV, encoding="utf-8-sig", dtype=object)
    if "survey_idx" not in cmp_df.columns:
        raise SystemExit("comparison.csv has no survey_idx column; re-run rescore_blind_comparison.py")

    cmpd = cmp_df.copy()
    cmpd["survey_idx"] = pd.to_numeric(cmpd["survey_idx"], errors="coerce")
    used = set(cmpd["survey_idx"].dropna().astype(int))

    rows: list[dict] = []
    for _, r in cmpd.iterrows():
        matched = pd.notna(r["survey_idx"])
        rec = {c: r.get(c) for c in OUT_COLS if c != "join_side"}
        rec["join_side"] = "both" if matched else "screenshots_only"
        if not matched:
            rec["outcome"] = "UNLINKED"
        rows.append(rec)

    for idx, s in survey.iterrows():
        if idx in used:
            continue
        rows.append(
            {
                "join_side": "survey_only",
                "child_key": None,
                "source_sheet": None,
                "form_row": None,
                "real_name": None,
                "wx_nickname": None,
                "survey_idx": idx,
                "survey_nick": s["宝贝昵称"],
                "match_basis": None,
                "survey_mutation": s["基因变异点位"] if pd.notna(s["基因变异点位"]) else None,
                "blind_tokens": None,
                "n_ocr_tokens": 0,
                "blind_status": None,
                "outcome": "SURVEY_ONLY",
                "detail": "survey row has no child with screenshots",
                "survey_birth": s["出生年份"] if pd.notna(s["出生年份"]) else None,
                "blind_birth": None,
                "survey_area": s["所在地区（省市）"] if pd.notna(s["所在地区（省市）"]) else None,
                "blind_area": None,
            }
        )

    df = pd.DataFrame(rows)[OUT_COLS].sort_values(
        ["join_side", "source_sheet", "form_row", "survey_idx"], na_position="last"
    )

    print(f"comparison.csv (left join):  {len(cmp_df)} rows")
    print(f"survey rows:                 {len(survey)}")
    print(f"survey rows already used:    {len(used)}")
    print(f"all-join rows:               {len(df)}")
    print()
    print(df["join_side"].value_counts().to_string())
    print()
    print(df["outcome"].value_counts().to_string())

    if args.dry_run:
        print("\ndry run - nothing written")
        return

    df.to_csv(OUT_CSV, index=False, encoding="utf-8-sig")
    print(f"\nwrote {OUT_CSV}")


if __name__ == "__main__":
    main()
