"""Shared cDNA-token scanner for the Chinese CDKL5 survey.

One implementation, three callers:

* ``build_patient_table.py``      — survey side, one cell at a time
* ``extract_blind_mutations.py``  — screenshot side, a whole OCR page at a time
* ``build_cdkl5_blind_table.py``  — re-derives the blind tables from ``ocr_text.jsonl``

Rules (they must be identical on both sides, otherwise a "mismatch" is just a
tokenisation difference):

* a token starts at ``c`` + optional separator + position, and the letter ``c``
  must not be part of a word (rejects ``grch37``, ``nc-000001``);
* it ends at a protein annotation (``p.`` — even a malformed one), Chinese text,
  a slash/pipe/comma/bracket, or a second base change;
* an exon/intron label wedged inside a token is dropped, so the base change
  stays contiguous (``c.533( exon8)G>A`` → ``c.533G>A``);
* missing bases are never invented.
"""

from __future__ import annotations

import re

# A cDNA token starts at 'c' followed by an optional separator and a position.
# The lookbehind rejects look-alikes such as 'grch37' and 'nc-000001'.
CDNA_START_RE = re.compile(r"(?<![A-Za-z])[cC]\s*[.,:·\-]?\s*[A-Za-z]?\s*[\*\-]?\s*\d+")
TOKEN_STOP_CHARS = set("/｜|()【】[]{}") | {",", "，", ":", "："}
# '(' ... ')' holding only an exon/intron label, e.g. '( exon8)', '(IVS5)', '(1VS16)'.
PAREN_ANNOT_RE = re.compile(r"(?i)^\s*(?:exon|ex0n|ex|ivs|1vs|intron|e)?\s*[0-9ivs]{1,8}\s*$")
PAREN_ANNOT_SPAN_RE = re.compile(r"\(\s*(?:(?:exon|ex0n|ex|ivs|1vs|intron|e)?\s*[0-9ivs]{1,8})\s*\)", re.IGNORECASE)
# Each separate cDNA variant; 'c.507_c.508delAG' is one variant, not two.
MULTI_VARIANT_RE = re.compile(r"(?<![_\w])[cC]\.")
# Chinese text or full-width punctuation glued to a token ('c.502del杂合突变',
# 'c.463+2T>C；') is prose, not part of the variant, and ends it.
CJK_RE = re.compile(r"[\u4e00-\u9fff\u3000-\u303f\uff01-\uff5e]")

# A token that was written without the HGVS dot ('C1', 'C2' — sample/control IDs in
# '样本26HB29546...、C1/C2/C3为3个正常对照') carries no information unless it also
# states the change; 'c123A>G' is still accepted.
SEP_AFTER_C_RE = re.compile(r"^[cC]\s*[.,:·]")
OPERATION_RE = re.compile(r">|[Dd][Ee][Ll]|[Dd][Uu][Pp]|[Ii][Nn][Ss]")
# A substitution is finished once the alternative base has been read ('c.643A>C').
SUB_DONE_RE = re.compile(r"[ACGT]\s*>\s*[ACGT]$", re.IGNORECASE)
# A three-letter amino-acid code is a protein annotation, never part of a cDNA token.
AA_RE = re.compile(
    r"(?i)^(?:ala|arg|asn|asp|cys|gln|glu|gly|his|ile|leu|lys|met|phe|pro|ser|thr|trp|tyr|val)\s*\d+"
)


def is_usable(raw: str, token: str) -> bool:
    """False for a bare ``C1``-style token: no 'c.' separator and no change stated."""
    if SEP_AFTER_C_RE.match(raw):
        return True
    return bool(OPERATION_RE.search(token))


def norm_width(text: str) -> str:
    """Full-width punctuation -> ASCII. Nothing else."""
    return (
        text.replace("＞", ">").replace("＜", "<").replace("（", "(").replace("）", ")")
        .replace("：", ":").replace("，", ",").replace("ｃ", "c").replace("．", ".")
        .replace("〉", ">").replace("〈", "<")
        .replace("\u3000", " ")
    )


def scan_token(norm: str, start: int, after_prefix: int) -> tuple[int, str, list[str]]:
    """Walk one cDNA token from ``start`` (``after_prefix`` = end of the ``c.<pos>`` part).

    Returns ``(end_index, token, notes)``; ``token`` is ``""`` when nothing usable
    remains. Shared by :func:`extract_cdna` (first token of a cell) and
    :func:`iter_cdna_tokens` (every token on a page) so both stop identically.
    """
    notes: list[str] = []
    out = list(norm[start:after_prefix])
    j = after_prefix
    while j < len(norm):
        ch = norm[j]

        if CJK_RE.match(ch):
            break

        # Once the base change is complete, a following letter starts a new word —
        # prose glued on by the OCR ('c.643A>Cinexon9oftheCDKL5gene') or the
        # protein annotation without its 'p.' ('c.532C Arg178Trp').
        if ch.isalpha() and SUB_DONE_RE.search("".join(out)):
            notes.append("stopped at prose glued to the base change")
            break

        # An exon/intron annotation wedged inside the token ('c.533( exon8)G>A',
        # 'c.282+3(IVS5)A>C', 'c.1142(exon12) delC', 'c.507(exon8)_c.508(exon8)delAG')
        # is skipped when the base change or range resumes after it.
        if ch == "(":
            close = norm.find(")", j + 1)
            inner = norm[j + 1: close] if close != -1 else ""
            after = norm[close + 1:].lstrip()[:1] if close != -1 else ""
            if PAREN_ANNOT_RE.match(inner) and after.upper() in {"A", "C", "G", "T", "U", "D", "I", "_"}:
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
            if AA_RE.match(nxt):
                break
            if re.match(r"[\u4e00-\u9fff]", nxt):
                break
            if re.match(r"(?i)(splice|intron|ivs|exon)", nxt):
                break
            # a second cDNA variant starts here ('c.577G>A c.1207A>G')
            if re.match(r"[cC]\s*[.\-·]\s*\d", nxt):
                break
            # a position range split by OCR ('c.1493 1494del') is one token
            if out and out[-1].isdigit() and re.match(r"\d", nxt):
                out.append("_")
                notes.append("OCR split the position range; joined with '_'")
                j += 1
                continue
            if norm[j - 1].isalpha() and nxt[:1].isalpha():
                notes.append("OCR spacing merged two letter runs; bases need checking")
        out.append(ch)
        j += 1

    token = "".join(out)
    # drop the exon/intron label that was skipped over inside the token
    token = PAREN_ANNOT_SPAN_RE.sub("", token)
    token = re.sub(r"\s+", "", token).rstrip("/-.,，:：")
    return j, token, notes


def extract_cdna(norm: str) -> tuple[str | None, list[str]]:
    """Pull the cDNA token out of a single cell, plus any review notes."""
    m = CDNA_START_RE.search(norm)
    if not m:
        return None, []

    _, token, notes = scan_token(norm, m.start(), m.end())
    if not token or not is_usable(norm[m.start():m.end()], token):
        return None, notes

    if len(MULTI_VARIANT_RE.findall(norm)) > 1:
        notes.append("cell lists more than one variant; only the first was kept")

    # HGVS writes the prefix lowercase and a dot separator; the rest is untouched.
    if len(token) > 1 and token[0] == "C":
        token = "c" + token[1:]
    token = re.sub(r"^([cC])[·]", r"\1.", token)
    return token, list(dict.fromkeys(notes))


def iter_cdna_tokens(norm: str) -> list[str]:
    """Every cDNA token in a block of text, in order — same walking rules as a cell.

    Used by the blind OCR pass, which reads a whole report page rather than a
    single survey cell but must stop each token in the same way, so the two sides
    stay directly comparable.
    """
    tokens: list[str] = []
    pos = 0
    while True:
        m = CDNA_START_RE.search(norm, pos)
        if not m:
            return tokens
        end, token, _ = scan_token(norm, m.start(), m.end())
        if token and is_usable(norm[m.start():m.end()], token):
            tokens.append(token)
        pos = max(end, m.end())
