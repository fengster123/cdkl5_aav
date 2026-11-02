"""Collapse the per-tab child rows into **one row per child**.

A child can submit twice — once on the consolidated tab and again on the monthly tab
of their submission month — and their photographs then land on both rows (different
pictures, so the content-hash de-duplication in ``export_screenshots.py`` keeps
both). Three children in this workbook do exactly that, plus one father/mother
double form. Listing them twice would inflate the child count and let one row say
"no variant found" while the other carries the variant.

Identity is ``(real_name, birth_raw, province)``: the same name, the exact same date
of birth and the same province is the same child. When any of those is missing the
row is left on its own, because a nickname alone is not an identity.

The **primary** row of a group is the one with a complete cDNA call, else one with a
CNV call, else the first; its ``child_key`` is kept as the group id, and the tokens
of every member are unioned so no information is lost.

Run from the ``cdkl5_aav`` folder::

    python -m projects.chinese_mutations_survey.build_distinct_children

Output ``blind_ocr/cdkl5_distinct_children.csv`` — the authoritative picture-derived
list: one row per child, one ``cdna_cdkl5``/``cnv_cdkl5`` value per row.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

from projects.chinese_mutations_survey.link_pairs import province_of, text

BASE = Path(__file__).resolve().parent
BLIND_DIR = BASE / "blind_ocr"
CDKL5_CSV = BLIND_DIR / "blind_mutations_cdkl5.csv"
OUT_CSV = BLIND_DIR / "cdkl5_distinct_children.csv"

OUT_COLS = [
    "child_key", "source_sheet", "form_row", "real_name", "wx_nickname", "birth_raw",
    "area", "n_images", "cdna_cdkl5", "cnv_cdkl5", "token_status", "n_sources",
    "sources",
]

_STATUS_RANK = {"complete": 0, "cnv": 1, "partial_only": 2, "none": 3}


def identity_keys(row) -> list[str]:
    """Every key that says "this row is that child".

    1. **real name + exact birth date + province** — the strongest key, and what most
       children are grouped by;
    2. **exact birth date + exact district + identical variant** — needed because one
       submission typed the baby's nickname (``糖果``) into the name field, so key 1
       cannot see that it is another submission for the same child (唐握瑜).

    Two children would have to share a date of birth, a district and the same rare
    variant for key 2 to over-merge, which is not a realistic collision here.
    """
    name, birth = text(row.get("real_name")), text(row.get("birth_raw"))
    area, prov = text(row.get("area")), province_of(row.get("area"))
    call = text(row.get("cdna_cdkl5")).upper() or text(row.get("cnv_cdkl5"))

    keys: list[str] = []
    if name and birth and prov:
        keys.append(f"name|{name}|{birth}|{prov}")
    if birth and area and call:
        keys.append(f"call|{birth}|{area}|{call}")
    return keys or [f"key:{row['child_key']}"]


class UnionFind:
    """Union rows that share *any* identity key, not just the first one."""

    def __init__(self) -> None:
        self.parent: dict[str, str] = {}

    def find(self, x: str) -> str:
        self.parent.setdefault(x, x)
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]
            x = self.parent[x]
        return x

    def union(self, a: str, b: str) -> None:
        ra, rb = self.find(a), self.find(b)
        if ra != rb:
            self.parent[rb] = ra


def _split(value) -> list[str]:
    s = text(value)
    return [x.strip() for x in s.split(";") if x.strip()] if s else []


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true", help="print the merges, write nothing")
    args, _ = ap.parse_known_args()

    df = pd.read_csv(CDKL5_CSV, encoding="utf-8-sig", dtype=object)
    uf = UnionFind()
    row_keys = []
    for _, r in df.iterrows():
        keys = identity_keys(r)
        row_keys.append(keys[0])
        for extra in keys[1:]:
            uf.union(keys[0], extra)
    df["group"] = [uf.find(k) for k in row_keys]

    rows: list[dict] = []
    merges: list[dict] = []
    for group, part in df.groupby("group", sort=False):
        part = part.assign(_rank=part["token_status"].map(_STATUS_RANK).fillna(9)).sort_values(
            ["_rank", "child_key"]
        )
        primary = part.iloc[0]
        cdna = list(dict.fromkeys(t for _, r in part.iterrows() for t in _split(r["cdna_cdkl5"])))
        cnv = [c for c in (text(r["cnv_cdkl5"]) for _, r in part.iterrows()) if c]
        statuses = [str(s) for s in part["token_status"]]
        status = min(statuses, key=lambda s: _STATUS_RANK.get(s, 9))

        rows.append(
            {
                "child_key": primary["child_key"],
                "source_sheet": primary["source_sheet"],
                "form_row": int(primary["form_row"]),
                "real_name": primary["real_name"],
                "wx_nickname": primary["wx_nickname"],
                "birth_raw": primary["birth_raw"],
                "area": primary["area"],
                "n_images": int(part["n_images"].astype(int).sum()),
                "cdna_cdkl5": "; ".join(cdna),
                "cnv_cdkl5": "; ".join(cnv),
                "token_status": status,
                "n_sources": len(part),
                "sources": "; ".join(str(k) for k in part["child_key"]),
            }
        )
        if len(part) > 1:
            merges.append(
                {
                    "group": group,
                    "primary": primary["child_key"],
                    "merged": "; ".join(str(k) for k in part["child_key"][1:]),
                    "cdna": "; ".join(cdna),
                    "cnv": "; ".join(cnv),
                }
            )

    out = pd.DataFrame(rows)[OUT_COLS].sort_values(["source_sheet", "form_row"])

    print(f"child rows before collapsing: {len(df)}")
    print(f"distinct children:            {len(out)}")
    print(f"groups merged:                {len(merges)}")
    print()
    print(out["token_status"].value_counts().to_string())
    print()
    n_call = int(((out["cdna_cdkl5"] != "") | (out["cnv_cdkl5"] != "")).sum())
    print(f"children with a CDKL5 call:   {n_call}")
    print(f"  with a complete c. token:   {int((out['cdna_cdkl5'] != '').sum())}")
    print(f"  CNV only:                   {int(((out['cdna_cdkl5'] == '') & (out['cnv_cdkl5'] != '')).sum())}")

    if merges:
        print("\nmerged groups:")
        print(pd.DataFrame(merges).to_string(index=False))

    if args.dry_run:
        print("\ndry run - nothing written")
        return

    out.to_csv(OUT_CSV, index=False, encoding="utf-8-sig")
    print(f"\nwrote {OUT_CSV}")


if __name__ == "__main__":
    main()
