"""Flag the redundant rows in a review copy of the full join, without touching it.

``comparison_all_join_checked.csv`` is a hand-annotated copy of
``comparison_all_join.csv`` (359 rows = 301 child rows + 58 survey-only rows). Eleven
children submitted the form more than once, so 12 of those child rows are the same
child seen again. This script adds one column, ``suggest_to_delete``, holding ``X``
on the rows that can be dropped, and writes the result to a **new** file; the input
is never modified.

Which row of a group survives: the one with a variant, then the one linked to a
survey row, then the better ``blind_status``, then the consolidated tab, then the
lowest Excel row. Everything else in the group is marked.

Rows are grouped exactly as ``build_distinct_children.py`` groups them:

* real name + exact birth date + province, and
* exact birth date + exact district + identical variant (needed because one
  submission typed the baby's nickname into the name field).

``survey_only`` rows carry no child, so they are never flagged.

Run from the ``cdkl5_aav`` folder::

    python -m projects.chinese_mutations_survey.flag_duplicate_children
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path

import pandas as pd

from projects.chinese_mutations_survey.build_distinct_children import UnionFind
from projects.chinese_mutations_survey.link_pairs import province_of, text

BASE = Path(__file__).resolve().parent
SRC = BASE / "blind_ocr" / "comparison_all_join_checked.csv"
DST = BASE / "blind_ocr" / "comparison_all_join_checked_flagged.csv"
MASTER = "希舞宝贝情况登记（收集结果）"

_STATUS_RANK = {"complete": 0, "cnv": 1, "partial_only": 2, "none": 3}
FLAG_COL = "suggest_to_delete"


def identity_keys(row) -> list[str]:
    """The same two keys used to collapse the child list."""
    name = text(row.get("real_name"))
    birth = text(row.get("blind_birth"))
    area = text(row.get("blind_area"))
    call = text(row.get("blind_tokens")).upper().replace(" ", "")

    keys: list[str] = []
    if name and birth and area:
        keys.append(f"name|{name}|{birth}|{province_of(area)}")
    if birth and area and call:
        keys.append(f"call|{birth}|{re.sub(r'[/、,， ]+', '', area)}|{call}")
    return keys


def keep_score(row, excel_row: int) -> tuple:
    """Higher wins: has a variant, is linked, better status, consolidated tab, top row."""
    return (
        bool(text(row.get("blind_tokens"))),
        not pd.isna(row.get("survey_idx")),
        -_STATUS_RANK.get(text(row.get("blind_status")), 9),
        text(row.get("source_sheet")) == MASTER,
        -excel_row,
    )


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", default=str(SRC))
    ap.add_argument("--dst", default=str(DST))
    args, _ = ap.parse_known_args()
    src, dst = Path(args.src), Path(args.dst)
    if src.resolve() == dst.resolve():
        raise SystemExit("refusing to overwrite the input file; choose a different --dst")

    df = pd.read_csv(src, encoding="utf-8-sig", dtype=object)
    df.insert(0, "excel_row", range(2, len(df) + 2))
    df[FLAG_COL] = ""

    uf = UnionFind()
    first_key: list[str | None] = []
    for _, r in df.iterrows():
        keys = identity_keys(r)
        first_key.append(keys[0] if keys else None)
        for extra in keys[1:]:
            uf.union(keys[0], extra)

    df["_group"] = [uf.find(k) if k else None for k in first_key]

    report: list[dict] = []
    for group, part in df[df["_group"].notna()].groupby("_group"):
        if len(part) < 2:
            continue
        scored = [(keep_score(r, int(r["excel_row"])), int(r["excel_row"])) for _, r in part.iterrows()]
        _, keeper = max(scored)
        for _, r in part.iterrows():
            if int(r["excel_row"]) == keeper:
                continue
            df.loc[r.name, FLAG_COL] = "X"
        report.append(
            {
                "group": group,
                "rows": "; ".join(str(int(v)) for v in sorted(part["excel_row"])),
                "keep": keeper,
                "keep_key": text(part.loc[part["excel_row"] == keeper, "child_key"].iloc[0]),
                "child": text(part.loc[part["excel_row"] == keeper, "real_name"].iloc[0]),
                "variant": text(part.loc[part["excel_row"] == keeper, "blind_tokens"].iloc[0]),
            }
        )

    n_flag = int((df[FLAG_COL] == "X").sum())
    n_child = int(df["child_key"].notna().sum())
    print(f"input : {src.name}  ({len(df)} rows, {n_child} child rows)")
    print(f"flagged: {n_flag} rows  -> {n_child - n_flag} distinct children")
    print()
    for r in sorted(report, key=lambda x: x["keep"]):
        print(f"  keep {r['keep']:>3} {r['keep_key']:<13} {r['child']:<8} {r['variant']:<28} "
              f"flag rows {r['rows']}")

    df.drop(columns=["_group"]).to_csv(dst, index=False, encoding="utf-8-sig")
    print(f"\nwrote {dst}")


if __name__ == "__main__":
    main()
