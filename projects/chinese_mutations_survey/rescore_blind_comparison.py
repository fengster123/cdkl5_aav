"""Re-score the screenshot-vs-survey comparison with the corrected blind tables.

Inputs
------
``output/cdkl5_cn_patients.csv``          the survey extract (Excel side)
``blind_ocr/blind_mutations_cdkl5.csv``   CDKL5-only OCR tokens (v2)
``blind_ocr/comparison.csv``              v1 pairs — reused for the linkage decision

The v1 file decided *which* child pairs with which survey row (by nickname, then
independently confirmed with birth date and city). That decision is kept as-is:
re-deriving linkage from scratch would silently reshuffle 152 pairs. Only the
blind value and the verdict are recomputed. Children that v1 never paired (e.g.
because they had no CDKL5 token) are linked here only when the match is
unambiguous, and never on the strength of the mutation value itself.

Every run copies the previous file to ``blind_ocr/v1_comparison.csv`` and writes a
``blind_ocr/comparison_changes.csv`` so each verdict change can be reviewed.

Run from the ``cdkl5_aav`` folder:

    python -m projects.chinese_mutations_survey.rescore_blind_comparison
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path

import pandas as pd

from projects.chinese_mutations_survey.link_pairs import POSITIVE_BASIS, TIEBREAK_SUFFIX, build_pairs, key_of
from projects.chinese_mutations_survey.workbook_sheets import MASTER, sheet_of_key

BASE = Path(__file__).resolve().parent
XLSX = BASE / "cdkl5_cn_survey (20240902).xlsx"
SURVEY_CSV = BASE / "output" / "cdkl5_cn_patients.csv"
BLIND_CSV = BASE / "blind_ocr" / "blind_mutations_cdkl5.csv"
CMP_CSV = BASE / "blind_ocr" / "comparison.csv"
CHANGES_CSV = BASE / "blind_ocr" / "comparison_changes.csv"

OUT_COLS = [
    "child_key", "source_sheet", "form_row", "real_name", "wx_nickname", "survey_idx",
    "survey_nick", "match_basis", "survey_mutation", "blind_tokens", "n_ocr_tokens",
    "blind_status", "outcome", "detail", "survey_birth", "blind_birth", "survey_area",
    "blind_area",
]


def norm(value) -> str:
    """Compare-ready form: no spaces, upper case, ASCII punctuation."""
    if pd.isna(value):
        return ""
    s = str(value).replace("＞", ">").replace("〉", ">").replace("，", ",")
    return re.sub(r"\s+", "", s).upper()


def canon(token: str) -> str:
    """Fold the OCR look-alikes that sit inside HGVS operation words.

    'c.524_525de1' and 'c.524_525del' are the same variant; so are 'DEIT'/'DELT'
    and 'DUF'/'DUP'. Only the operation word and the intron offset digit are
    touched — never a position or a base.
    """
    t = norm(token)
    t = re.sub(r"^C,?(?=\d)", "C.", t)  # c2277-3... or c,1051delG -> C.1051DELG
    t = re.sub(r"^C\.C(?=\d)", "C.", t)  # stray prefix in the survey cell: c.C338_340del
    t = re.sub(r"([-+])([IL])", r"\g<1>1", t)
    t = re.sub(r"DE[1I]", "DEL", t)
    t = re.sub(r"DU[FP]", "DUP", t)
    t = re.sub(r"IN[5S]", "INS", t)
    t = re.sub(r"(DEL[ACGT]*)P[A-Z]\d+[A-Z0-9*]*$", r"\1", t)  # c,1051deIGpV351X -> C.1051DELG
    return t


def loose_key(token: str) -> str:
    """Positions + operation only, so a listed base suffix cannot break a match.

    'c.1493-1494delTG' and 'c.1493_1494del' are the same change; 'c.533G>A' and
    'c.533G>C' are not, because a substitution keeps its base change in the key.
    """
    t = re.sub(r"^C\.(\d+)-(\d+)", r"C.\1_\2", canon(token))
    m = re.match(r"^C\.(\d+(?:_\d+)?)(.*)$", t)
    if not m:
        return t
    pos, rest = m.groups()
    sub = re.match(r"^[ACGT]>[ACGT]", rest)
    if sub:
        return f"{pos}{sub.group(0)}"
    op = re.match(r"^(DELINS|DEL|DUP|INS)", rest)
    return f"{pos}{op.group(1) if op else rest}"


def split_values(value, sep) -> list[str]:
    if pd.isna(value):
        return []
    return [v for v in (canon(x) for x in str(value).split(sep)) if v]


def load_raw_cnv_by_nick() -> dict[str, list[str]]:
    """Map survey nickname -> non-empty raw mutation cell strings from 智能表1."""
    if not XLSX.exists():
        return {}
    raw = pd.read_excel(XLSX, sheet_name="智能表1", header=None, dtype=object)
    body = raw.iloc[2:].copy()
    body = body[pd.to_numeric(body.iloc[:, 0], errors="coerce").notna()]
    out: dict[str, list[str]] = {}
    for _, r in body.iterrows():
        nick = "" if pd.isna(r.iloc[2]) else str(r.iloc[2]).strip()
        mut = "" if pd.isna(r.iloc[8]) else str(r.iloc[8]).strip()
        if nick and mut:
            out.setdefault(nick, []).append(mut)
    return out


def cnv_matches_raw(blind_cnv: str, raw_cells: list[str]) -> str:
    """Return the matching raw Excel CNV description if it corroborates blind_cnv."""
    if not blind_cnv or not raw_cells:
        return ""
    for cell in raw_cells:
        c = cell.upper()
        if any(k in c for k in ("缺失", "杂合缺", "重复", "DEL", "DUP", "LOSS")):
            return cell
    return ""


def classify(
    survey: list[str],
    blind: list[str],
    partial_only: bool,
    blind_cnv: str = "",
    raw_cells: list[str] | None = None,
) -> tuple[str, str]:
    """Verdict for one pair, given the survey value(s) and the OCR token(s)."""
    if not blind:
        if blind_cnv:
            raw_hit = cnv_matches_raw(blind_cnv, raw_cells or [])
            if raw_hit:
                return "MATCH", f"CNV/exon call matches raw survey cell ({raw_hit})"
            return "SURVEY_BLANK_OCR_HAS", f"survey cell is empty but the report shows {blind_cnv}"
        return "NOT_VERIFIABLE", "no CDKL5 cDNA token recovered from the screenshots"
    if not survey:
        return "SURVEY_BLANK_OCR_HAS", f"survey cell is empty but the report shows {'; '.join(blind)}"

    if set(survey) & set(blind) or {loose_key(s) for s in survey} & {loose_key(b) for b in blind}:
        if len(survey) == 1 and len(blind) == 1:
            return "MATCH", ""
        return "MATCH_1_OF_SEVERAL", f"{len(blind)} token(s) on the pages; the recorded one is among them"

    def related(a: str, b: str) -> bool:
        """One side captured only the position while the other has the full change (c.64+2 vs c.64+2delT)."""
        short, long_ = (a, b) if len(a) <= len(b) else (b, a)
        if len(short) < 3 or not long_.startswith(short):
            return False
        return not re.search(r">|DEL|DUP|INS", short)

    if any(related(a, b) for a in survey for b in blind):
        if len(survey[0]) < len(blind[0]):
            return "CONSISTENT_OCR_PARTIAL", f"survey recorded position only ({survey[0]}); report has {'; '.join(blind)}"
        return "CONSISTENT_OCR_PARTIAL", f"OCR captured only part of the change: {'; '.join(blind)}"

    if partial_only:
        return "NOT_VERIFIABLE", f"OCR read only a fragment ({'; '.join(blind)}); no contradiction"

    return "MISMATCH", f"survey {survey[0]} vs report {'; '.join(blind)}"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true", help="print the diff, write nothing")
    args, _ = ap.parse_known_args()

    for path in (SURVEY_CSV, BLIND_CSV, CMP_CSV):
        if not path.exists():
            raise SystemExit(f"missing {path}")

    survey = pd.read_csv(SURVEY_CSV, encoding="utf-8-sig", dtype=object)
    blind = pd.read_csv(BLIND_CSV, encoding="utf-8-sig", dtype=object)
    blind["form_row"] = blind["form_row"].astype(int)
    blind_by_key = {key_of(r): r for _, r in blind.iterrows()}

    baseline = CMP_CSV.with_name("v1_comparison.csv")
    source = baseline if baseline.exists() else CMP_CSV
    old = pd.read_csv(source, encoding="utf-8-sig", dtype=object)
    old["form_row"] = old["form_row"].astype(int)

    # Only pairs an earlier pass established are kept as anchors; the ones it
    # rejected are re-decided by the scored matcher, so a rejected first hit no
    # longer blocks a correct second one (郭萌 -> 郭暖暖).
    anchors = [
        r for r in old.to_dict("records")
        if str(r["match_basis"]).replace(TIEBREAK_SUFFIX, "") in POSITIVE_BASIS
    ]
    pairs, link_log = build_pairs(blind, survey, anchors)
    linked_rows = {key_of(p) for p in pairs}
    log_by_row = {key_of(e): e["reason"] for e in link_log if not e["reason"].startswith("linked")}

    out: list[dict] = []
    changes: list[dict] = []
    old_by_row = {key_of(r): r for r in old.to_dict("records")}
    raw_cnv_map = load_raw_cnv_by_nick()

    for pair in pairs:
        row = int(pair["form_row"])
        b = blind_by_key.get(key_of(pair))
        blind_vals = split_values(b["cdna_cdkl5"], ";") if b is not None else []
        blind_cnv = "" if b is None or pd.isna(b.get("cnv_cdkl5")) else str(b["cnv_cdkl5"]).strip()

        # A v1 pair carries a copy of the survey row as it read when the pair was made.
        # That copy can predate a correction to the extract (c.64+2 -> c.64+2delT), so
        # the comparison always re-reads the survey row it points at.
        idx = pair.get("survey_idx")
        if idx is not None and not pd.isna(idx):
            srow = survey.loc[int(idx)]
            surv_nick = srow["宝贝昵称"]
            surv_mut = srow["基因变异点位"]
            surv_birth = srow["出生年份"]
            surv_area = srow["所在地区（省市）"]
        else:
            surv_nick, surv_mut = pair["survey_nick"], pair["survey_mutation"]
            surv_birth, surv_area = pair["survey_birth"], pair["survey_area"]

        survey_vals = split_values(surv_mut, "|")
        raw_cells = raw_cnv_map.get(str(surv_nick).strip(), [])

        rec = {
            "child_key": key_of(pair),
            "source_sheet": pair.get("source_sheet") or sheet_of_key(key_of(pair)) or MASTER,
            "form_row": row,
            "real_name": pair["real_name"],
            "wx_nickname": pair["wx_nickname"],
            "survey_idx": idx,
            "survey_nick": surv_nick,
            "match_basis": pair["match_basis"],
            "survey_mutation": surv_mut,
            "blind_tokens": "; ".join(blind_vals) if blind_vals else (blind_cnv or None),
            "n_ocr_tokens": len(blind_vals) if blind_vals else (1 if blind_cnv else 0),
            "blind_status": (b["token_status"] if b is not None else "none"),
            "survey_birth": surv_birth,
            "blind_birth": pair["blind_birth"],
            "survey_area": surv_area,
            "blind_area": pair["blind_area"],
        }
        rec["outcome"], rec["detail"] = classify(
            survey_vals, blind_vals, rec["blind_status"] == "partial_only", blind_cnv, raw_cells
        )
        out.append(rec)

        prev = old_by_row.get(key_of(pair))
        before = "" if prev is None or pd.isna(prev.get("blind_tokens")) else str(prev["blind_tokens"])
        after = rec["blind_tokens"] or ""
        if norm(before) != norm(after) or (prev is None) or str(prev["outcome"]) != rec["outcome"]:
            changes.append(
                {
                    "child_key": rec["child_key"],
                    "form_row": row,
                    "real_name": pair["real_name"],
                    "old_blind": before,
                    "new_blind": after,
                    "old_outcome": "(new pair)" if prev is None else prev["outcome"],
                    "new_outcome": rec["outcome"],
                }
            )

    # every child with screenshots appears, so an unlinked child is visible rather
    # than silently missing from the table
    for child_key_, child in blind_by_key.items():
        if child_key_ in linked_rows:
            continue
        b_vals = split_values(child["cdna_cdkl5"], ";")
        b_cnv = "" if pd.isna(child.get("cnv_cdkl5")) else str(child["cnv_cdkl5"]).strip()
        reason = log_by_row.get(child_key_, "no survey row matches this child's nickname")
        out.append(
            {
                "child_key": child_key_,
                "source_sheet": child.get("source_sheet") or sheet_of_key(child_key_) or MASTER,
                "form_row": int(child["form_row"]),
                "real_name": child["real_name"],
                "wx_nickname": child["wx_nickname"],
                "survey_idx": None,
                "survey_nick": None,
                "match_basis": "unlinked",
                "survey_mutation": None,
                "blind_tokens": "; ".join(b_vals) if b_vals else (b_cnv or None),
                "n_ocr_tokens": len(b_vals) if b_vals else (1 if b_cnv else 0),
                "blind_status": child["token_status"],
                # UNLINKED: nothing to compare against. UNMATCHED: a candidate row
                # existed but several tied, so the pair is deliberately not guessed.
                "outcome": "UNMATCHED" if reason.startswith("ambiguous") else "UNLINKED",
                "detail": reason,
                "survey_birth": None,
                "blind_birth": child["birth_raw"],
                "survey_area": None,
                "blind_area": child["area"],
            }
        )

    df = pd.DataFrame(out).sort_values(["source_sheet", "form_row"], na_position="last")[OUT_COLS]
    ch = pd.DataFrame(changes)

    print(f"pairs scored:            {len(df)}   (v1 baseline: {len(old)}, added: {len(df) - len(old)})")
    print(f"verdicts changed:        {len(ch)}")
    print(df["outcome"].value_counts().to_string())
    print()
    print("verdict transitions:")
    print(
        ch.groupby(["old_outcome", "new_outcome"]).size().sort_values(ascending=False).to_string()
        if not ch.empty
        else "  (none)"
    )

    if args.dry_run:
        print("\ndry run - nothing written")
        print(ch.to_string(index=False))
        return

    for path, backup in ((CMP_CSV, CMP_CSV.with_name("v1_comparison.csv")),):
        if path.exists() and not backup.exists():
            backup.write_bytes(path.read_bytes())

    df.to_csv(CMP_CSV, index=False, encoding="utf-8-sig")
    ch.to_csv(CHANGES_CSV, index=False, encoding="utf-8-sig")
    print(f"\nwrote {CMP_CSV}")
    print(f"wrote {CHANGES_CSV}")


if __name__ == "__main__":
    main()
