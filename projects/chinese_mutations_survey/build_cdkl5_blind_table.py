"""Rebuild the BLIND screenshot tables from every ``blind_ocr/ocr_text*.jsonl``.

``ocr_text.jsonl`` holds the consolidated tab's pages and ``ocr_text_extra.jsonl``
the pages of the other 24 image-bearing tabs; both are read and merged. Children are
keyed by ``child_key`` = ``"{sheet_slug}:{excel_row}"`` because the workbook's 25
screenshot tabs reuse the same row numbers, and ``source_sheet`` records the tab.

Blindness: the only variant input is the OCR text written by
``extract_blind_mutations.py``. Child identity (name / nickname / birth / area)
comes from the raw form workbook, whose mutation column is never read. This module
never opens the survey workbook or ``output/cdkl5_cn_patients.csv``, and refuses to
run if such a path is passed on the command line.

Fixes versus the v1 tables (kept as ``blind_ocr/v1_*.csv`` on first run):

1. tokens are de-duplicated case- and space-insensitively — v1 listed
   ``C.2578C>T; c.2578C>T`` and ``c. 1142; c.1142`` as two variants (33 children);
2. tokenisation uses the shared scanner in ``cdna_tokens.py``, so a token stops at
   the protein annotation (v1 produced ``C.107A>CP.HIS36PRO``) and stays on the
   same line instead of swallowing the next cell;
3. CDKL5 attribution accepts the gene when OCR mangles or splits it
   (``CDKLS``, ``COKLS``, ``CDK``+``L5`` on separate lines, ``NMLS``) and when the
   CDKL5 disease name or MIM number (300672 / 300203) is on the line; the line
   window is configurable. v1 required the literal string ``CDKL5`` within ±2
   lines, which silently dropped 11 children's real variant;
4. ``protein_cdkl5`` is filtered like the cDNA tokens instead of dumping the whole
   multi-gene panel's protein list into a file named *_cdkl5*;
5. fragments of one allele (``C.1``, ``C.1257D``, ``C.1257DEIT``, ``C.1257DEL``)
   are reported as ``n_partial`` rather than counted as separate variants;
   complete tokens win when both exist;
6. positions outside the CDKL5 coding sequence (c.1..3093) are dropped, at any
   line distance.

Run from the ``cdkl5_aav`` folder:

    python -m projects.chinese_mutations_survey.build_cdkl5_blind_table --window 5

Outputs
-------
``blind_ocr/blind_mutations.csv``         every cDNA token per child (all genes)
``blind_ocr/blind_mutations_cdkl5.csv``   CDKL5-attributed tokens per child
``blind_ocr/blind_cdkl5_v2_changes.csv``  per-child v1 -> v2 diff, for review
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

import pandas as pd

from projects.chinese_mutations_survey.cdna_tokens import iter_cdna_tokens, norm_width
from projects.chinese_mutations_survey.workbook_sheets import load_all_children, slug_map

BASE = Path(__file__).resolve().parent
BLIND_DIR = BASE / "blind_ocr"
ALL_CSV = BLIND_DIR / "blind_mutations.csv"
CDKL5_CSV = BLIND_DIR / "blind_mutations_cdkl5.csv"
CHANGES_CSV = BLIND_DIR / "blind_cdkl5_v2_changes.csv"

FORBIDDEN_DIR = (BASE / "output").resolve()

# NM_003159.3 coding sequence is c.1..3093 (1030 aa). Anything beyond that cannot
# be a CDKL5 coding change; intronic offsets are kept because c.825+1 etc. are real.
CDS_MAX = 3093

# Strong evidence: the gene name as OCR leaves it (CDKL5, CDKLS, COKLS, CDK L5 with
# junk between, NMLS), a CDKL5 transcript accession, or the CDKL5 genomic locus on
# chrX (18.5M-18.67M). A token near one of these beats a token that is only near the
# disease name — the reports put several genes in one column-major table, so the
# neighbouring block's variant is often one line closer to a disease-name cell than
# the gene's own variant is.
STRONG_RE = re.compile(
    r"CDKL5|CDKLS|COKLS|COKL5|CDK\.5|CDKI5|CDK[^A-Z0-9]{0,4}L5|NMLS"
    r"|NM_00315\d*|NM_00132\d*|NM_0031(?!\d)|NM_0013(?!\d)|CHRX:18[3456]\d"
)
# ACMG PM5/PS1 literature citations mention other variants at the same codon
# ('[c. 532C>T/p. R178W, NM_001323289] [c. 533G>C...]', '同一位置的变异c.533G>A...文献报道');
# never treat a literature citation line as the patient's own variant row.
PM5_LIT_RE = re.compile(r"\[C\..*NM_.*\]\s*\[C\.|文献报道|同一位置的变异", re.I)
# Weak evidence: the CDKL5 disease name / MIM numbers. Needed when the gene name
# itself is unreadable, but never enough to outrank a strong hit.
STRONG_CJK = ("300203",)
WEAK_RE = re.compile(r"300672|300203")
WEAK_CJK = ("癫痫性脑病2型", "癫痫性脑病2", "癫痫性脑病")
# CDKL5 is at chrX:18.5M-18.67M, so a token printed beside 'chr8:' or beside another
# X-chromosome locus ('chrX:153' L1CAM, 'chrX:532' MRX1) is a different gene.
CHR_OTHER_RE = re.compile(
    r"CHR(?:OMOSOME)?(?:[1-9]|1[0-9]|2[0-2]|Y)(?![0-9X])|CHRX:(?!18[3456])\d{3}"
)

PROTEIN_RE = re.compile(r"[pP]\s*\.\s*[A-Za-z]{1,3}\d+[0-9A-Za-z_*>]*")
# A CDKL5 transcript accession (also when OCR truncates the tail of the number).
CDKL5_TX_RE = re.compile(r"NM_00(?:3159|13232\d*)|NM_0031(?!\d)|NM_0013232")
# Any accession on the token's own line that is NOT CDKL5 means the row belongs to
# another gene in the panel table ('NM_02... c.931G>A ... 发育性和癫痫性脑病3型,AR' is
# DEE3/SLC25A22, not CDKL5), however close a CDKL5 mention happens to be.
OTHER_TX_RE = re.compile(r"NM_?0")
# CDKL5 is DEE2 / X-linked dominant. A row annotated with another DEE subtype (and no
# DEE2) is a neighbouring gene in the same panel table.
DEE_OTHER_RE = re.compile(r"癫痫性脑病(?:[3-9]|1[0-9])型|DEE(?:[3-9]|1[0-9])(?![0-9])")
DEE2_RE = re.compile(r"癫痫性脑病2型|DEE2(?![0-9])")
POS_RE = re.compile(r"^C\.-?(\d+)")
COMPLETE_RE = re.compile(r">[ACGT]$|^C\.-?\d+[ACGT]>[ACGT]$|DEL|DUP|INS")


def norm_token(tok: str) -> str:
    """One canonical spelling, folding common OCR look-alikes in HGVS tokens."""
    t = re.sub(r"\s+", "", norm_width(tok)).upper()
    t = re.sub(r"^C[.,·\-]?(?=-?\d)", "C.", t)
    t = re.sub(r"^C\.C(?=\d)", "C.", t)
    t = re.sub(r"([-+])([IL])", r"\g<1>1", t)
    t = re.sub(r"DE[1I]", "DEL", t)
    t = re.sub(r"DU[FP]", "DUP", t)
    t = re.sub(r"IN[5S]", "INS", t)
    # Strip trailing OCR punctuation misread as letters after DEL/DUP/INS ('c.1257delTo' where 'o' is '。')
    t = re.sub(r"((?:DELINS|DEL|DUP|INS)[ACGT]*)[B-FH-SU-Z]+$", r"\1", t)
    t = re.sub(r"^C\.(\d+)([ACGT])-([ACGT])$", r"C.\1\2>\3", t)      # C.682G-A -> C.682G>A
    t = re.sub(r"^C\.(\d+[ACGT])S([ACGT])$", r"C.\1>\2", t)          # C.619GST -> C.619G>T
    t = re.sub(r"^C\.(\d+)([ACGT])([ACGT])$", r"C.\1\2>\3", t)       # C.70TG   -> C.70T>G
    m0 = re.match(r"^C\.(\d{3,4})0>([ACGT])$", t)                    # C.27160>T -> C.2716G>T
    if m0 and int(m0.group(1) + "0") > CDS_MAX >= int(m0.group(1)):
        t = f"C.{m0.group(1)}G>{m0.group(2)}"
    return t


def dna_pos(tok: str) -> int | None:
    canon = norm_token(tok)
    if re.match(r"^C\.0\d", canon):  # reject sample-ID fragments such as C.004
        return None
    if re.match(r"^C\.\d{4,}[A-Z]{2,}$", canon) and not re.search(r"DEL|DUP|INS", canon):
        return None
    m = POS_RE.match(canon)
    return int(m.group(1)) if m else None


def is_complete(tok: str) -> bool:
    """A token carrying an actual allele or operation, not just a position."""
    return bool(COMPLETE_RE.search(norm_token(tok)))


def in_cds(tok: str) -> bool:
    pos = dna_pos(tok)
    return pos is not None and 1 <= pos <= CDS_MAX


def stitch_wrapped_lines(lines: list[str]) -> list[str]:
    """Stitch cDNA tokens that wrap across 2-12 lines inside narrow report table cells.

    Each reconstructed token is appended to its opening line ``i`` so line indices,
    marker distances, and chromosome guards on line ``i`` are preserved verbatim.
    """
    out = list(lines)
    open_re = re.compile(
        r"([cC]\s*\.\s*\d+(?:[_+-]\d+)?)\s*[\(（]\s*(?:ex(?:on|0n)?|ivs|1vs|1v)[0-9A-Za-z\s]*[\)）]?"
        r"(?!\s*(?:[ACGT]>|de[l1i]|dup|ins))",
        re.I,
    )
    close_re = re.compile(
        r"^(?:\d{4,6}\s+)?(?:on\d*|n\d*|\d+|s\d+)?\s*[\)）]\s*"
        r"([ACGT]\s*>\s*[ACGT]|[ACGT]{2}\b|de[l1i][A-Za-z0-9]*|dup[A-Za-z0-9]*|ins[A-Za-z0-9]*)",
        re.I,
    )
    bare_sub_re = re.compile(r"^\s*([ACGT]\s*>\s*[ACGT]|de[l1i][A-Za-z0-9]*)\s*$", re.I)

    nm_open_re = re.compile(
        r"(?:NM_00(?:3159|1323289)|(?:59|89)\.[23])\s*:\s*([cC]\s*\.\s*(?:\d{1,3}|\d+[ACGT]>))\s*(?:疑似)?$"
    )
    nm_cont_re = re.compile(
        r"^(\d{0,3}(?:[ACGT]>[ACGT]|de[l1i][A-Za-z0-9]*|dup[A-Za-z0-9]*|ins[A-Za-z0-9]*)|[ACGT])"
        r"\s*(?:[\(（]\s*[pP]\.|[\u4e00-\u9fff]|$)"
    )

    for i, ln in enumerate(lines):
        m = open_re.search(ln)
        if m:
            prefix = re.sub(r"\s+", "", m.group(1))
            has_close = ")" in ln[m.start():] or "）" in ln[m.start():]
            for j in range(i + 1, min(len(lines), i + 13)):
                mc = close_re.search(lines[j].strip())
                if mc:
                    op = re.sub(r"\s+", "", mc.group(1))
                    if re.fullmatch(r"[ACGT]{2}", op, re.I):
                        op = f"{op[0]}>{op[1]}"
                    out[i] = f"{out[i]} {prefix}{op}"
                    break
                if has_close:
                    mb = bare_sub_re.match(lines[j].strip())
                    if mb:
                        out[i] = f"{out[i]} {prefix}{re.sub(r'\\s+', '', mb.group(1))}"
                        break

        m2 = nm_open_re.search(ln.strip())
        if m2:
            prefix = re.sub(r"\s+", "", m2.group(1))
            for j in range(i + 1, min(len(lines), i + 10)):
                mc = nm_cont_re.match(lines[j].strip())
                if mc:
                    cand = f"{prefix}{re.sub(r'\\s+', '', mc.group(1))}"
                    if in_cds(cand):
                        out[i] = f"{out[i]} {cand}"
                        break
    return out


# NM_003159.3 exon structure on hg19/GRCh37 (UCSC ncbiRefSeq), used to express a
# genomic CNV call in cDNA terms. Columns: genomic start, genomic end, c.start, c.end.
# Anchored at cdsStart 18,525,216 (0-based) = the A of the ATG; exon 1 and part of
# exon 21 are non-coding, so their c. numbering is negative / runs past c.3093.
CDKL5_EXONS_HG19: dict[int, tuple[int, int, int, int]] = {
    1: (18443728, 18443815, -250, -163),
    2: (18525055, 18525280, -162, 64),
    3: (18528940, 18528974, 65, 99),
    4: (18582597, 18582642, 100, 145),
    5: (18593474, 18593610, 146, 282),
    6: (18597968, 18598088, 283, 403),
    7: (18600011, 18600070, 404, 463),
    8: (18602383, 18602473, 464, 554),
    9: (18606074, 18606263, 555, 744),
    10: (18613468, 18613548, 745, 825),
    11: (18616582, 18616733, 826, 977),
    12: (18622022, 18622988, 978, 1944),
    13: (18626931, 18627032, 1945, 2046),
    14: (18627585, 18627690, 2047, 2152),
    15: (18631272, 18631395, 2153, 2276),
    16: (18637987, 18638086, 2277, 2376),
    17: (18643248, 18643367, 2377, 2496),
    18: (18646491, 18646707, 2497, 2713),
    19: (18664127, 18664210, 2714, 2797),
    20: (18668530, 18668712, 2798, 2980),
    21: (18671552, 18671749, 2981, 3178),
}


def exons_to_cdna(lo: int | None = None, hi: int | None = None,
                  g_start: int | None = None, g_end: int | None = None) -> str:
    """c. span for an exon range, or for a genomic interval, on NM_003159.3.

    Exon-level calls (``exon6-20 del``) become ``c.283_2980``; a genomic interval
    (``chrX:18636850_18640535dup``) becomes the c. span of the exons it covers. The
    breakpoints of a CNV sit in introns, so this is the exon-level approximation —
    callers must not treat it as a base-exact HGVS position.
    """
    if g_start is not None and g_end is not None:
        covered = [n for n, (gs, ge, _, _) in CDKL5_EXONS_HG19.items() if gs <= g_end and ge >= g_start]
        if not covered:
            return ""
        lo, hi = min(covered), max(covered)
    if lo is None:
        return ""
    hi = hi if hi is not None else lo
    return f"c.{CDKL5_EXONS_HG19[lo][2]}_{CDKL5_EXONS_HG19[hi][3]}"


def cnv_to_cdna(descr: str) -> str:
    """Rewrite a descriptive CNV call in cDNA terms when the exon span is known."""
    if not descr:
        return ""
    m = re.match(r"^exon(\d+)-(\d+) del", descr)
    if m:
        span = exons_to_cdna(int(m.group(1)), int(m.group(2)))
        return f"{span}del (exon{m.group(1)}-{m.group(2)} loss)" if span else descr
    m = re.match(r"^exon(\d+) del", descr)
    if m:
        span = exons_to_cdna(int(m.group(1)))
        return f"{span}del (exon{m.group(1)} loss)" if span else descr
    m = re.match(r"^EX(\d+)-EX(\d+)del", descr, re.I)
    if m:
        span = exons_to_cdna(int(m.group(1)), int(m.group(2)))
        return f"{span}del (exon{m.group(1)}-{m.group(2)} loss)" if span else descr
    m = re.search(r"chrX:(\d+)_(\d+)dup", descr, re.I)
    if m:
        span = exons_to_cdna(g_start=int(m.group(1)), g_end=int(m.group(2)))
        covered = [n for n, (gs, ge, _, _) in CDKL5_EXONS_HG19.items()
                   if gs <= int(m.group(2)) and ge >= int(m.group(1))]
        ex = f" (exon{covered[0]} dup)" if len(covered) == 1 else ""
        return f"{span}dup{ex}" if span else descr
    if "whole-gene" in descr or "incl. CDKL5" in descr:
        return "c.-250_3178del (whole CDKL5 locus)"
    return descr


def exon_from_coord(text: str) -> int | None:
    """Exon whose boundary a printed chrX:18.6x coordinate sits on, ±3 bp."""
    for m in re.finditer(r"186[0-9]{5}", text):
        g = int(m.group(0))
        for n, (gs, ge, _, _) in CDKL5_EXONS_HG19.items():
            if abs(g - gs) <= 3 or abs(g - ge) <= 3:
                return n
    return None


def extract_cnv_cdkl5(pages_i: list[dict]) -> str:
    """Extract CDKL5 exon/CNV deletion or duplication calls when present on the report."""
    joined = "\n".join(pg["text"] for pg in pages_i)
    if not re.search(r"CDKL5|CDKLS|COKLS|300672|300203", joined, re.I):
        return ""
    # Table cells wrap mid-phrase ('该缺失包' / '含RS1、PHKA2、CDKL5'), so match on a
    # whitespace-free copy.
    flat = re.sub(r"\s+", "", joined)

    # 'ex.2_3del' / 'ex2-3del' — an exon range written with the laboratory's own
    # shorthand ('NM_003159.3:ex.2_3de1（p.？）', 王若汐). Checked before the generic
    # rules because the coordinate interval next to it is often split by the cell
    # layout and cannot be read as a pair.
    m = re.search(r"(?:EX|ex)\.?\s*(\d{1,2})\s*[-_–]\s*(\d{1,2})\s*de[l1i]", flat)
    if m and 1 <= int(m.group(1)) <= int(m.group(2)) <= 21:
        return f"exon{int(m.group(1))}-{int(m.group(2))} del"

    if re.search(r"EX7-EX9Del", joined, re.I):
        return "EX7-EX9del"
    if re.search(r"18636850[_-]18640535dup", joined, re.I):
        return "chrX:18636850_18640535dup (3.69kb)"

    m = re.search(r"(\d+)[-–](\d+)号外显子[^。]{0,8}缺", flat)
    if m:
        return f"exon{int(m.group(1))}-{int(m.group(2))} del"
    if re.search(r"上游调控区至3号外显子", flat):
        return "exon1-3 del (Xp22.13)"
    if re.search(r"CDKL5基因exon14半合子缺失", flat, re.I):
        return "exon14 del"
    if re.search(r"CDKL5的第12外显子|loss1\(EX[0O]N:12\)", flat, re.I):
        return "exon12 del"

    m = re.search(r"loss1\(EX[0O]N:(\d+)", flat, re.I)
    if m:
        return f"exon{m.group(1)} del"

    # 'loss1(EXON:' with the exon number lost to OCR — fall back to the coordinate
    # printed next to it (an exon boundary on hg19).
    if re.search(r"loss1\(EX[0O]N:", flat, re.I):
        ex = exon_from_coord(flat)
        return f"exon{ex} del" if ex else "exon del (loss1)"

    # A printed genomic interval that lies inside CDKL5: report the exons it removes.
    for gm in re.finditer(r"CHRX[:：]?(\d{7,9})[-_](\d{7,9})", flat, re.I):
        start, end = int(gm.group(1)), int(gm.group(2))
        inside = [n for n, (gs, ge, _, _) in CDKL5_EXONS_HG19.items() if gs >= start and ge <= end]
        if len(inside) >= 2:
            ex = f" (exon{min(inside)}-{max(inside)} loss)"
            return f"{exons_to_cdna(min(inside), max(inside))}del{ex}"

    # Only an explicit "the deletion covers CDKL5 exon 1" counts; a bare mention of
    # 外显子1 in an MLPA probe list is not a variant.
    if re.search(r"(?:包含|涉及|覆盖)[^。]{0,12}CDKL5[^。]{0,12}1号外显子", flat):
        return "exon1 del (Xp22.13)"
    if re.search(r"CDKL5全基因的拷贝数杂合缺失|(?:完全覆盖|全要盖)单[倍信]剂量不足基因CDKL5", flat):
        return "whole-gene del (Xp22.13)"
    if re.search(r"包含[^。]{0,30}CDKL5|CDKL5[^。]{0,30}包含基因", flat):
        return "Xp22.13 del (incl. CDKL5)"
    return ""


def marker_lines(lines: list[str]) -> tuple[list[int], list[int]]:
    """Line indices carrying strong (gene/transcript) and weak (disease/MIM) evidence."""
    strong: list[int] = []
    weak: list[int] = []
    for i, line in enumerate(lines):
        compact = re.sub(r"\s+", "", line).upper()
        if PM5_LIT_RE.search(compact):
            continue
        if STRONG_RE.search(compact) or any(k in line for k in STRONG_CJK):
            strong.append(i)
        elif WEAK_RE.search(compact) or any(k in line for k in WEAK_CJK):
            weak.append(i)
    return strong, weak


def attribute(text: str, window: int) -> tuple[list[tuple[str, tuple[int, int, int], str]], list[str]]:
    """Tokens within ``window`` lines of a CDKL5 marker, each with its rank key.

    The key is ``(is_partial, near_strong_marker, distance)``, so a complete token
    beside the gene name beats an equally close one beside only the disease name,
    which beats a fragment. Returns ``(candidates, proteins)`` where each candidate
    is ``(token, key, evidence)`` so any pick can be rechecked in ocr_text.jsonl.
    """
    raw_lines = text.split("\n")
    lines = stitch_wrapped_lines(raw_lines)
    strong, weak = marker_lines(lines)
    marks = strong + weak
    if not marks:
        return [], []

    cands: list[tuple[str, tuple[int, int, int], str]] = []
    proteins: list[str] = []
    for i, line in enumerate(lines):
        compact = re.sub(r"\s+", "", line).upper()
        if PM5_LIT_RE.search(compact) or CHR_OTHER_RE.search(compact):
            continue
        # A different DEE subtype in this table block means the row belongs to that
        # gene: CDKL5 is DEE2 (XD), so 'c.931G>A .. 发育性和癫痫性脑病3型，AR' is
        # DEE3/SLC25A22 next door in the same panel table, not CDKL5.
        block = "".join(re.sub(r"\s+", "", x).upper() for x in lines[max(0, i - 6): i + 7])
        if DEE_OTHER_RE.search(block) and not DEE2_RE.search(block):
            continue
        near = [(abs(i - m), m) for m in marks]
        distance, nearest = min(near)
        if distance > window:
            continue
        d_strong = min((abs(i - s) for s in strong), default=window + 1)
        for tok in iter_cdna_tokens(norm_width(line)):
            if not in_cds(tok):
                continue
            canon = norm_token(tok)
            key = (0 if is_complete(canon) else 1, 0 if d_strong <= window else 1, distance)
            cands.append((canon, key, f"{canon} L{i}{i - nearest:+d}"))
        proteins.extend(m.group(0).strip() for m in PROTEIN_RE.finditer(line))
    return cands, proteins


def _uniq(values) -> list[str]:
    return list(dict.fromkeys(values))


# Some reports state the substitution in prose instead of trusting the table cell:
# '该变异使CDKL5基因编码序列第532位核苷酸由胞嘧啶核苷酸(C)替换为胸腺嘧啶核苷酸(T)'.
# The table entry for the same variant is often unreadable (牛宸溪: 'c.532(exon8)C
# Arg178Trp)]' with the base change lost), so this sentence is used as a fallback.
NARRATIVE_RE = re.compile(
    r"第\s*(\d+)\s*位核苷酸(?:由)?\s*.{0,4}?核苷酸\s*[（(]\s*([ACGTU])\s*[）)]\s*"
    r"替换为\s*.{0,4}?核苷酸\s*[（(]\s*([ACGTU])\s*[）)]"
)


def recover_from_narrative(pages_i: list[dict]) -> tuple[str, str]:
    """Recover a substitution stated in Chinese prose; returns (token, evidence)."""
    for pg in pages_i:
        for i, line in enumerate(pg["text"].split("\n")):
            if not re.search(r"CDKL5|CDKLS|COKLS", line, re.I):
                continue
            m = NARRATIVE_RE.search(re.sub(r"\s+", "", line))
            if not m:
                continue
            pos, ref, alt = int(m.group(1)), m.group(2).upper(), m.group(3).upper()
            if not (1 <= pos <= CDS_MAX) or ref == alt:
                continue
            tok = f"C.{pos}{ref}>{alt}"
            return tok, f"{tok} narrative {pg['file']} L{i}"
    return "", ""


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--window", type=int, default=5, help="CDKL5 line window (default 5)")
    ap.add_argument("--dry-run", action="store_true", help="print the summary, write nothing")
    args, _ = ap.parse_known_args()

    if any(str(FORBIDDEN_DIR) in a for a in sys.argv):
        raise SystemExit("refusing to run: this builder must stay blind to the survey output")
    jsonls = sorted(BLIND_DIR.glob("ocr_text*.jsonl"))
    if not jsonls:
        raise SystemExit(f"no ocr_text*.jsonl in {BLIND_DIR}; run extract_blind_mutations.py first")

    pages: list[dict] = []
    for path in jsonls:
        pages.extend(json.loads(x) for x in path.read_text(encoding="utf-8").splitlines() if x.strip())
    if not pages:
        raise SystemExit(f"{jsonls} are empty")
    for pg in pages:
        pg.setdefault("slug", "master")  # the first pass wrote no sheet field

    sheets = slug_map()
    children = load_all_children(list(sheets.values()))
    by_key: dict[str, list[dict]] = {}
    for pg in pages:
        by_key.setdefault(f"{pg['slug']}:{int(pg['form_row'])}", []).append(pg)

    all_rows: list[dict] = []
    cdkl5_rows: list[dict] = []
    for key in sorted(by_key, key=lambda k: (k.split(":")[0] != "master", k.split(":")[0], int(k.split(":")[1]))):
        pages_i = sorted(by_key[key], key=lambda p: p["col"])
        meta = children.get(key, {})
        ident = {
            "child_key": key,
            "source_sheet": meta.get("source_sheet", sheets.get(key.split(":")[0])),
            "form_row": int(key.split(":")[1]),
            "real_name": meta.get("real_name"),
            "wx_nickname": meta.get("wx_nickname"),
            "birth_raw": meta.get("birth_raw"),
            "area": meta.get("area"),
            "n_images": len(pages_i),
        }

        page_tokens = [iter_cdna_tokens(norm_width(pg["text"])) for pg in pages_i]
        all_tokens = _uniq(norm_token(t) for toks in page_tokens for t in toks)
        all_proteins = _uniq(
            m.group(0).strip() for pg in pages_i for m in PROTEIN_RE.finditer(pg["text"])
        )

        all_rows.append(
            {
                **ident,
                "cdna_tokens": "; ".join(all_tokens),
                "n_tokens": len(all_tokens),
                "protein_tokens": "; ".join(all_proteins),
                "n_pages_without_token": sum(1 for toks in page_tokens if not toks),
                "ocr_seconds": round(sum(pg["seconds"] for pg in pages_i), 1),
                "min_page_score": min(pg["min_score"] for pg in pages_i),
            }
        )

        cands: list[tuple[str, tuple[int, int, int], str]] = []
        made_prot: list[str] = []
        for pg in pages_i:
            c, p = attribute(pg["text"], args.window)
            cands.extend(c)
            made_prot.extend(p)

        # Companion-page fallback: if one page names CDKL5 as the target gene and
        # another page prints '核酸突变：c....' (e.g. Sanger slip split across 2 photos).
        if not cands and any(re.search(r"CDKL5|CDKLS|COKLS", pg["text"], re.I) for pg in pages_i):
            for pg in pages_i:
                for i, ln in enumerate(pg["text"].split("\n")):
                    if "核酸突变" in ln or "核苷酸" in ln:
                        for tok in iter_cdna_tokens(norm_width(ln)):
                            if in_cds(tok):
                                canon = norm_token(tok)
                                cands.append((canon, (0 if is_complete(canon) else 1, 0, 1), f"{canon} L{i}@companion"))

        # Last resort: the report may state the change in prose when the table entry
        # itself is unreadable. Appended before the ranking so it is scored like any
        # other candidate.
        if not any(is_complete(t) for t, _, _ in cands):
            narr_token, narr_evidence = recover_from_narrative(pages_i)
            if narr_token:
                cands.append((narr_token, (0, 0, 1), narr_evidence))

        tokens = _uniq(t for t, _, _ in cands)
        complete = [t for t in tokens if is_complete(t)]
        partial = [t for t in tokens if not is_complete(t)]

        # Keep the best-ranked row of the gene table: complete before fragment,
        # beside the gene name before beside only the disease name, then nearest.
        best = min((k for _, k, _ in cands), default=None)
        kept_raw = _uniq(t for t, k, _ in cands if k == best)
        # Drop any token that is a strict prefix of another kept token on the same
        # child (e.g. 'C.1257DEL' when 'C.1257DELT' is also read).
        kept = [t for t in kept_raw if not any(o != t and o.startswith(t) for o in kept_raw)]
        evidence = _uniq(ev for t, k, ev in cands if k == best and t in kept)
        cnv = cnv_to_cdna(extract_cnv_cdkl5(pages_i))

        status = (
            "complete" if (kept and complete)
            else ("partial_only" if kept else ("cnv" if cnv else "none"))
        )
        cdkl5_rows.append(
            {
                **ident,
                "cdna_cdkl5": "; ".join(kept),
                "cnv_cdkl5": cnv,
                "n_tokens": len(kept),
                "token_status": status,
                "n_partial": len([t for t in partial if t not in kept]),
                "protein_cdkl5": "; ".join(_uniq(made_prot)),
                "gene_evidence": "; ".join(evidence[:8]),
            }
        )

    df_all = pd.DataFrame(all_rows)
    df_cdkl5 = pd.DataFrame(cdkl5_rows)

    # ------------------------------------------------------------- v1 -> v2 diff
    # The v1 tables only cover the consolidated tab, so the diff is limited to
    # children that tab contains; a child added by a monthly tab is not a "change".
    changes: list[dict] = []
    baseline = CDKL5_CSV.with_name(f"v1_{CDKL5_CSV.name}")
    if baseline.exists():
        old = pd.read_csv(baseline, encoding="utf-8-sig", dtype=object)
        if "cdna_cdkl5" in old.columns:
            old_map = {
                f"master:{int(r['form_row'])}": ("" if pd.isna(r["cdna_cdkl5"]) else str(r["cdna_cdkl5"]))
                for _, r in old.iterrows()
            }
            for _, r in df_cdkl5.iterrows():
                if r["child_key"] not in old_map:
                    continue
                before_s = old_map[r["child_key"]]
                if before_s.upper() != r["cdna_cdkl5"].upper():
                    changes.append(
                        {
                            "child_key": r["child_key"],
                            "form_row": r["form_row"],
                            "real_name": r["real_name"],
                            "v1": before_s,
                            "v2": r["cdna_cdkl5"],
                            "gene_evidence": r["gene_evidence"],
                        }
                    )

    n_with = int((df_cdkl5["cdna_cdkl5"] != "").sum())
    n_cnv = int(((df_cdkl5["cdna_cdkl5"] == "") & (df_cdkl5["cnv_cdkl5"] != "")).sum())
    print(f"pages OCR'd:                   {len(pages)}  from {len(jsonls)} pass(es)")
    print(f"children with >=1 image:       {len(df_all)}")
    print(f"children with >=1 CDKL5 token: {n_with}  (window +/-{args.window} lines)")
    print(f"children with CNV only:        {n_cnv}")
    print(f"children with >1 kept token:   {int(df_cdkl5['cdna_cdkl5'].str.contains(';').sum())}")
    print(f"children changed vs v1:        {len(changes)}")
    print()
    print("by tab:")
    print(
        df_cdkl5.groupby("source_sheet")
        .agg(children=("child_key", "size"), with_token=("cdna_cdkl5", lambda s: int((s != "").sum())))
        .to_string()
    )

    if args.dry_run:
        print("\ndry run - nothing written")
        for c in changes:
            print(f"  row={c['form_row']:>4} {c['real_name']}: {c['v1']!r} -> {c['v2']!r}  [{c['gene_evidence']}]")
        return

    for path in (ALL_CSV, CDKL5_CSV):  # keep the v1 tables for audit
        backup = path.with_name(f"v1_{path.name}")
        if path.exists() and not backup.exists():
            backup.write_bytes(path.read_bytes())

    BLIND_DIR.mkdir(parents=True, exist_ok=True)
    df_all.to_csv(ALL_CSV, index=False, encoding="utf-8-sig")
    df_cdkl5.to_csv(CDKL5_CSV, index=False, encoding="utf-8-sig")
    pd.DataFrame(changes).to_csv(CHANGES_CSV, index=False, encoding="utf-8-sig")

    print(f"\nwrote {ALL_CSV}")
    print(f"wrote {CDKL5_CSV}")
    print(f"wrote {CHANGES_CSV}")


if __name__ == "__main__":
    main()
