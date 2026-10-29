"""Extract four columns from the Chinese CDKL5 mutations survey.

Source: ``cdkl5_cn_survey (20240902).xlsx``, sheet ``智能表1``.

Output (``output/cdkl5_cn_patients.csv``, UTF-8 with BOM so Excel shows the
Chinese correctly):

    宝贝昵称 | 所在地区（省市） | 出生年份 | 基因变异点位

Rules
-----
* ``宝贝昵称`` and ``所在地区（省市）`` are copied verbatim.
* ``出生年份`` is the 4-digit year parsed out of ``出生年月``. Left blank when the
  cell has no unambiguous 4-digit year — it is never guessed.
* ``基因变异点位`` is the DNA-level change only: the protein annotation
  (``p.Asp193Asn``), severity labels and dosing notes are stripped. When the cell
  carries no ``c.`` notation but does describe a deletion/rearrangement at DNA
  level (``X染色体缺失，包含CDKL5基因1-3号外显子``), that description is kept —
  it is still the variant. Cells that only give a protein change are left blank.

Only these normalisations are applied, all of them cosmetic:

* full-width punctuation (``＞ ＜ （ ） ： ，``) is replaced with its ASCII form;
* a leading ``C.`` becomes ``c.`` and a leading ``c·`` becomes ``c.`` (HGVS writes
  the coordinate prefix lowercase with a dot);
* an exon/intron label wedged inside the token (``c.533( exon8)G>A``,
  ``c.282+3(IVS5)A>C``) is dropped so the base change stays contiguous.

Nothing else is rewritten. Missing bases are never invented, so cells such as
``C.1855>T`` keep their gap and are listed for review in the companion markdown.
"""

from __future__ import annotations

import re
from pathlib import Path

import pandas as pd

HERE = Path(__file__).resolve().parent
XLSX = HERE / "cdkl5_cn_survey (20240902).xlsx"
SHEET = "智能表1"
OUT_DIR = HERE / "output"
OUT_CSV = OUT_DIR / "cdkl5_cn_patients.csv"
OUT_MD = OUT_DIR / "cdkl5_cn_patients.md"

# Zero-based column indices in the sheet (row 1 is the header).
COL_NICKNAME = 2   # 宝贝昵称
COL_LOCATION = 3   # 所在地区（省市）
COL_BIRTH = 4      # 出生年月
COL_MUTATION = 8   # 基因变异点位
N_COLS = 20        # 智能表1 width

OUT_COLS = ["宝贝昵称", "所在地区（省市）", "出生年份", "基因变异点位"]

# A cDNA token starts at 'c' followed by an optional separator and a position.
# The lookbehind rejects look-alikes such as 'grch37' and 'nc-000001'.
CDNA_START_RE = re.compile(r"(?<![A-Za-z])[cC]\s*[.,:·\-]?\s*[A-Za-z]?\s*[\*\-]?\s*\d+")
TOKEN_STOP_CHARS = set("/｜|()【】,，:：")
# '(' ... ')' holding only an exon/intron label, e.g. '( exon8)', '(IVS5)', '(1VS16)'.
PAREN_ANNOT_RE = re.compile(r"(?i)^\s*(?:exon|ivs|intron|e)?\s*[0-9ivs]{1,8}\s*$")
PAREN_ANNOT_SPAN_RE = re.compile(r"\(\s*(?:(?:exon|ivs|intron|e)?\s*[0-9ivs]{1,8})\s*\)", re.IGNORECASE)
# Each separate cDNA variant; 'c.507_c.508delAG' is one variant, not two.
MULTI_VARIANT_RE = re.compile(r"(?<![_\w])[cC]\.")

YEAR_RE = re.compile(r"(19|20)\d{2}")


def _norm_width(text: str) -> str:
    """Full-width punctuation -> ASCII. Nothing else."""
    return (
        text.replace("＞", ">").replace("＜", "<").replace("（", "(").replace("）", ")")
        .replace("：", ":").replace("，", ",").replace("ｃ", "c").replace("．", ".")
        .replace("\u3000", " ")
    )


def _extract_cdna(norm: str) -> tuple[str | None, list[str]]:
    """Pull the cDNA token out of a mutation cell, plus any review notes."""
    m = CDNA_START_RE.search(norm)
    if not m:
        return None, []

    notes: list[str] = []
    start, j = m.start(), m.end()
    while j < len(norm):
        ch = norm[j]

        # An exon/intron annotation wedged inside the token ('c.533( exon8)G>A',
        # 'c.282+3(IVS5)A>C') is skipped when the base change resumes after it.
        if ch == "(":
            close = norm.find(")", j + 1)
            inner = norm[j + 1: close] if close != -1 else ""
            after = norm[close + 1:].lstrip()[:1] if close != -1 else ""
            if PAREN_ANNOT_RE.match(inner) and after.upper() in {"A", "C", "G", "T", "U"}:
                j = close + 1
                continue
            break

        if ch in TOKEN_STOP_CHARS:
            break
        if norm[j:j + 2] in ("p.", "P."):
            break
        if ch.isspace():
            nxt = norm[j + 1:].lstrip()
            # a protein annotation (even a malformed one), Chinese text, or a
            # non-cDNA word ends the token
            if re.match(r"[pP]\s*[.,]", nxt) or re.match(r"[pP][A-Z]", nxt):
                break
            if re.match(r"[\u4e00-\u9fff]", nxt):
                break
            if re.match(r"(?i)(splice|intron|ivs|exon)", nxt):
                break
            if norm[j - 1].isalpha() and nxt[:1].isalpha():
                notes.append("OCR spacing merged two letter runs; bases need checking")
        j += 1

    token = norm[start:j]
    # drop the exon/intron label that was skipped over inside the token
    token = PAREN_ANNOT_SPAN_RE.sub("", token)
    token = re.sub(r"\s+", "", token).rstrip("/-.,，:：")
    if not token:
        return None, notes

    if len(MULTI_VARIANT_RE.findall(norm)) > 1:
        notes.append("cell lists more than one variant; only the first was kept")

    # HGVS writes the prefix lowercase and a dot separator; the rest is untouched.
    if len(token) > 1 and token[0] == "C":
        token = "c" + token[1:]
    token = re.sub(r"^([cC])[·]", r"\1.", token)
    return token, list(dict.fromkeys(notes))


def dna_mutation(raw) -> tuple[str | None, list[str]]:
    """The cDNA token for this variant, or None when the cell has no valid one.

    Only ``c.`` notation counts as a valid mutation. Descriptive text
    (``X染色体缺失，包含CDKL5基因1-3号外显子``, ``16-21号外显子缺失``), raw genomic
    coordinates (``ChrX:18622719``), gene-name-only cells (``CDKL5``) and stray
    fragments (``4号``) are not valid mutations, so those cells stay empty.
    """
    if pd.isna(raw):
        return None, []
    return _extract_cdna(_norm_width(str(raw)))


def birth_year(raw) -> int | None:
    """4-digit year from 出生年月; None when it is absent or ambiguous."""
    if pd.isna(raw):
        return None
    m = YEAR_RE.search(str(raw))
    return int(m.group(0)) if m else None


def load() -> pd.DataFrame:
    """Load 智能表1 into a frame with 序号/昵称/地区/出生/变异, dropping non-data rows."""
    raw = pd.read_excel(XLSX, sheet_name=SHEET, header=None, dtype=object)
    if raw.shape[1] < N_COLS:
        raise ValueError(f"sheet {SHEET!r} has {raw.shape[1]} columns, expected {N_COLS}")

    body = raw.iloc[2:].copy()
    # Drop the stray cells the smart-table export leaves below the data
    # ('否', '否', '未控制发作'): real rows always carry a numeric 序号.
    seq = pd.to_numeric(body.iloc[:, 0], errors="coerce")
    body = body[seq.notna()]
    if body.empty:
        raise ValueError(f"sheet {SHEET!r}: no data rows with a numeric 序号")

    def _verbatim(v):
        """Copy a text cell as-is, minus leading/trailing whitespace.

        Two nickname cells carry invisible padding in the source ('\\n林思彤\\n',
        ' 西瓜'); an untrimmed value will not match on lookup.
        """
        return v.strip() if isinstance(v, str) else v

    return pd.DataFrame(
        {
            "nickname": body.iloc[:, COL_NICKNAME].map(_verbatim),
            "location": body.iloc[:, COL_LOCATION].map(_verbatim),
            "birth_raw": body.iloc[:, COL_BIRTH],
            "mutation_raw": body.iloc[:, COL_MUTATION],
        }
    ).reset_index(drop=True)


def main() -> None:
    src = load()

    dna = [dna_mutation(v) for v in src.mutation_raw]
    out = pd.DataFrame(
        {
            "宝贝昵称": src.nickname,
            "所在地区（省市）": src.location,
            "出生年份": pd.array([birth_year(v) for v in src.birth_raw], dtype="Int64"),
            "基因变异点位": [t for t, _ in dna],
        }
    )
    review = [(n, src.mutation_raw[i], t, notes)
              for i, (n, (t, notes)) in enumerate(zip(src.nickname, dna)) if notes]

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    out.to_csv(OUT_CSV, index=False, encoding="utf-8-sig")

    # Markdown mirror, plus the rows that need a human look.
    no_year = out[out["出生年份"].isna()]
    no_dna = out[out["基因变异点位"].isna()]
    md = [
        "# Chinese CDKL5 mutations survey — 4-column extract",
        "",
        f"Source: `{XLSX.name}`, sheet `{SHEET}`. {len(out)} rows.",
        "",
        "| " + " | ".join(OUT_COLS) + " |",
        "|" + "---|" * len(OUT_COLS),
    ]
    for _, r in out.iterrows():
        cells = ["" if pd.isna(r[c]) else str(r[c]) for c in OUT_COLS]
        md.append("| " + " | ".join(c.replace("|", "\\|") for c in cells) + " |")

    md += ["", "## Rows needing review", ""]
    md += [f"### 出生年份 blank ({len(no_year)})", ""]
    for _, r in no_year.iterrows():
        md.append(f"- {r['宝贝昵称']} — raw `{src.loc[r.name, 'birth_raw']}`")

    empty_cell = [i for i in out.index if pd.isna(src.mutation_raw[i])]
    invalid = [i for i in out.index
               if pd.notna(src.mutation_raw[i]) and pd.isna(out.loc[i, "基因变异点位"])]

    md += ["", f"### 基因变异点位 blank — source cell empty ({len(empty_cell)})", ""]
    md.append(", ".join(out.loc[i, "宝贝昵称"] for i in empty_cell))

    md += ["", f"### 基因变异点位 blank — no valid c. notation ({len(invalid)})", ""]
    for i in invalid:
        md.append(f"- {out.loc[i, '宝贝昵称']} — raw `{src.mutation_raw[i]}`")

    md += ["", f"### 基因变异点位 worth a human look ({len(review)})", ""]
    for name, raw_cell, token, notes in review:
        md.append(f"- {name} — extracted `{token}` from raw `{raw_cell}`  \n  {'; '.join(notes)}")

    OUT_MD.write_text("\n".join(md), encoding="utf-8")

    print(f"rows: {len(out)}")
    print(f"birth year extracted: {out['出生年份'].notna().sum()} / {len(out)}")
    print(f"mutation extracted:   {out['基因变异点位'].notna().sum()} / {len(out)}")
    print(f"  blank - source cell empty:        {len(empty_cell)}")
    print(f"  blank - no valid c. notation:     {len(invalid)}")
    print(f"  extracted but flagged:            {len(review)}")
    print(f"\nblanked (no c. notation):")
    for i in invalid:
        print(f"  {out.loc[i, '宝贝昵称']}: {src.mutation_raw[i]!r}")
    print(f"\nwrote {OUT_CSV}")
    print(f"wrote {OUT_MD}")


if __name__ == "__main__":
    main()
