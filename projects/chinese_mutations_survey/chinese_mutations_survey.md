# Chinese CDKL5 mutations survey — extraction

Source: `cdkl5_cn_survey (20240902).xlsx`, sheet `智能表1`.

Original brief:

> 1) firstly, both tabs might have the same patients, investigate,
> 2) we want all the patient names, their province/city, their year of birth, and mutations points.

Deliverable — `output/cdkl5_cn_patients.csv` (UTF-8 with BOM, so Excel renders the
Chinese correctly). Rerun `build_patient_table.py` to refresh.

| 宝贝昵称 | 所在地区（省市） | 出生年份 | 基因变异点位 |
|---|---|---|---|
| 郭暖暖 | 内蒙古锡盟 | 2023 | c.312delA |
| 桃桃 | 河南省卫辉市 | 2022 | c.2276+1G>A |
| 晗樾 | 山东省烟台市 | 2023 | c.577G>A |
| 小米 | 河南省商丘市 | 2024 | c.502de1 |
| 亦宝 | 四川省成都市 | 2022 | c.1259del |

225 rows, 4 columns.

## 1. The two tabs hold the same patients — so either works

| | `有效数据表` | `智能表1` |
|---|---|---|
| rows | 225 | 225 |
| distinct `(姓名, 地区, 出生, 变异)` | 225 | 225 |
| overlap | 225 common, 0 unique to either side | |
| row order | identical | identical |

Only 2 cells differ, both cosmetic (an extra space in `变异来源` for seq 86; `1月3日`
vs an Excel-coerced datetime in `发作持续时间` for seq 8).

`智能表1` is used because it additionally carries `外显子序列` and `备注`. Neither tab
stores the four requested fields in cleaned form — the year and the DNA mutation are
derived here either way. Those two extra columns are **not** used in this extract.

## 2. Structure gotcha: `序号` is not a unique key

225 rows but `序号` only reaches 182. The sheet is **two batches appended, each numbered
from 1**: batch A = rows 1–182 (mutation mostly filled), batch B = rows 183–225
(mutation mostly blank). Row position is therefore the key, and the stray cells the
smart-table export leaves below the data (`否`, `否`, `未控制发作`) are dropped by
requiring a numeric `序号`.

## 3. Rules applied

| column | rule |
|---|---|
| `宝贝昵称` | copied verbatim, leading/trailing whitespace trimmed (2 cells) |
| `所在地区（省市）` | copied verbatim (no province/city splitting) |
| `出生年份` | the 4-digit year from `出生年月`; blank if there is no unambiguous one |
| `基因变异点位` | valid `c.` notation only, protein annotation stripped; blank when there is none |

The DNA column keeps the variant only when it is written in `c.` notation —
`c.577G＞A(p.Asp193Asn)` → `c.577G>A`. Everything else is **left empty**, because it is
not a valid mutation description:

| raw cell | output |
|---|---|
| `X染色体缺失，包含CDKL5基因1-3号外显子` | *empty* |
| `16-21号外显子缺失` | *empty* |
| `Xp22.13杂合缺，失累及 CDKL5基因的上游调控区至3号外显子及其相邻内含子` | *empty* |
| `4号` | *empty* |
| `ChrX:18622719. exon12` | *empty* |
| `Cdkl5` / `CDKL5` / `cdkl5基因突变` | *empty* |
| `p.H939fs*14` (protein only) | *empty* |

Cosmetic normalisations only: full-width punctuation → ASCII, `C.` / `c·` → `c.`, and an
exon label wedged mid-token is dropped (`c.533( exon8)G>A` → `c.533G>A`).

## 4. Coverage and rows needing review

- `出生年份`: **223 / 225**
- `基因变异点位`: **164 / 225**
  - 26 blank because the source cell is empty (all in batch B)
  - 35 blank because the cell has text but no `c.` notation — the full list is at the bottom
    of `output/cdkl5_cn_patients.md`

**Two unusable birth dates** (left blank, not guessed):

- 凤宝 — `202.8.8` (truncated; almost certainly 2020, unverified)
- 董依心 — `23.4.17` (2-digit year; 2023 if 21st century)

**Three mutation cells where the extract is not clean** (also listed at the bottom of
`output/cdkl5_cn_patients.md`):

- 沫沫 `c.1854_1861d elCAAAGTG A(p.D618Efs*18）` → `c.1854_1861delCAAAGTGA`. OCR spacing
  splits the deleted bases, and only 7 bases are written for an 8-position deletion — the
  sequence needs checking against the lab report.
- 吴承励 `c.574_581del GTGGACAT` → `c.574_581delGTGGACAT`. Same OCR issue, though here the
  8 written bases do match the 8 deleted positions.
- 恬甜 — two variants in one cell (`c.1959delC` and `c.2816G>T`); only the first is kept.

**Malformed tokens left exactly as recorded** (not corrected): `c.502de1` (`de1` for `del`),
`c,1051deIGpV351X` (comma, `deI`, and a stray `pV351X`), `c.1855>T` and `c.532>T` (missing
base before `>`), `c.13070>G` (beyond the 3.2 kb CDKL5 CDS — almost certainly `c.1370…`),
`c.507_c.508delAG` (nested `c.`), `c.C338_340del` (stray `C.`).

## 5. Duplicate patient records (not removed — decide whether to keep both)

- 安安: rows 11 and 182 — both 福建厦门, 2018.09, `c.592G>T`. Same child entered twice.
- 汤圆: rows 62 and 98 — both 湖北随州, `c.2354del p.Lys785ArgfsTer18`; birth
  `2021.11.23` vs `202201`.

Other repeated nicknames (伊伊, 优优, 依依, 圆圆, 小米, 彤彤, 恬恬, 沐沐, 瑶瑶, 甜甜, 鑫鑫,
雯雯) are different children — different birth dates and mutations.

## 6. Screenshot audit of the mutation column

Source of the check: `C:\temp\希舞宝贝情况登记（收集结果）.xlsx` — the raw form-collection
workbook, which holds **490 lab-report screenshots** attached to **197 children** (2–6 pages
each). Its own mutation column (col 66) is empty for all 203 rows, so the survey values were
transcribed by hand from these images. This section checks them against the images.

Method, and why it is trustworthy:

- the mutation column in the survey was **never opened** by the extractor — a separate,
  blind pass OCR'd the screenshots into `blind_ocr/blind_mutations_cdkl5.csv`
- OCR: `rapidocr_onnxruntime` in an isolated venv at `C:\temp\ocr_env` (zf.12 untouched)
- a token counted only when it sat on, or within ±2 lines of, a line mentioning CDKL5;
  positions beyond the 3,219 bp CDKL5 CDS were discarded (this is what stops the lab's
  whole multi-gene variant table from being read as the patient's variant)
- linkage by **nickname → full birth date → birth year+month + city**. The mutation value
  was never used to link. Where the name collided or the birth year disagreed, the pair was
  left unmatched rather than guessed.

## 6.1 Result

152 child ↔ survey pairs were matched. Outcome of comparing the survey value with the report:

| outcome | n | meaning |
|---|---|---|
| `MATCH` | 65 | report shows exactly the recorded change |
| `MATCH_1_OF_SEVERAL` | 6 | several tokens on the pages; the recorded one is among them |
| `CONSISTENT_OCR_PARTIAL` | 8 | OCR caught only part (`c.602T>C` read as `c.602`) — no contradiction |
| **`MISMATCH`** | **2** | the report contradicts the survey |
| **`SURVEY_BLANK_OCR_HAS`** | **5** | survey cell empty, report shows a variant |
| `UNCLEAR` | 1 | OCR read a different position; needs a human eye |
| `NOT_VERIFIABLE` | 43 | matched, but the report pages produced no readable `c.` token |
| `UNMATCHED` | 22 | name collided or birth year disagreed — deliberately not guessed |

So **79 of 152 pairs corroborate** the recorded value, and **8 need action**.

Also note: **95 of the 225 survey rows have no screenshot in this workbook at all**, so they
were out of scope for this check. The two files are different snapshots.

## 6.2 The 2 disagreements

- **李洋** — survey `c.1195C>T`, report `c.1165C>T`. A single digit (1195 vs 1165); the two
  give different amino-acid changes, so one of them is wrong.
- **游奕可** (nickname 可可) — survey `c.1855>T`, report `c.1855A>T`. The survey cell is
  missing the 5′ base; the report supplies it. This is the malformed token already flagged
  in §4, now confirmed by the source: it should read **`c.1855A>T`**.

## 6.3 Five cells that are empty in the survey but have a variant in the report

- 罗诗皓 (皓皓) → `c.533G>T`
- 吴一锘 (胡沐橙) → `c.683G>A`
- 孟欣苇 (苇苇) → `c.212A>G`
- 李烨坤 (李烨坤) → `c.1934dup`
- 郭诗然 (郭诗然) → `c.1675C>T`

All five sit in batch B, the block where the mutation column is mostly blank (§2). Treat these
as candidates from OCR to be confirmed against the printed report — they are not yet verified
by eye.

## 6.4 One that needs a human

- **范牧荑** (牧牧) — survey `c.104A>G`, report reads `c.404A>G`. Same class of digit error as
  李洋. Worth noting the survey's own protein annotation is `p.Asp135Gly`, which corresponds
  to `c.404A>G`, not `c.104A>G` — so the DNA position is the suspect part.

## 6.5 Caveat

OCR is not an authority. It reads confidently (~0.99 on clean pages) but the characters it can
confuse — `1/I/l`, `0/O`, `>` — are precisely the ones that matter here. Everything above is a
flag for review against the printed reports, not a correction applied to the data.

Artefacts: `blind_ocr/blind_mutations_cdkl5.csv` (per-child OCR), `blind_ocr/ocr_text.jsonl`
(full text of all 490 pages, so any claim can be audited line by line),
`blind_ocr/comparison.csv` (the joined verdict per pair).
