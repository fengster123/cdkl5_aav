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
workbook. It has **28 tabs, and 25 of them carry embedded lab reports: 1,718 images in total.**
Its own mutation column (col 66) is empty for every row, so the survey values were transcribed
by hand from these images. This section checks them against the images.

Which images are actually distinct:

| | images |
|---|---:|
| embedded in the workbook | 1,718 |
| **unique pictures** (after content-hash de-duplication) | **758** |
| on `希舞宝贝情况登记（收集结果）` (the consolidated tab) | 490 |
| on the 21 monthly tabs `20250101…20260930` | 268 |
| duplicate snapshots | 960 |

The 960 duplicates are not lost data: `希舞宝贝情况登记（收集结果）(副本)` (471 images) and
`20241201-20241231（收集结果）` (483) are earlier snapshots of the same submissions, and the
same photo reappears across monthly tabs. De-duplication is by bytes, with a 16×16 greyscale
fingerprint fallback for the 13 large PNGs the first export had re-encoded as JPEG.

One photo can belong to two form rows — a child who submitted once on the consolidated tab and
again on the monthly tab of their submission month — so the 758 pictures resolve to **301 child
rows**, and those collapse to **289 distinct children**. Two keys are used, unioned together:
real name + exact date of birth + province, and exact date of birth + exact district + identical
variant. The second key is needed because one submission typed the baby's nickname (`糖果`) into
the name field, so name-based grouping alone left 唐握瑜 listed three times
(`master:21`, `m202502:5`, `m202512:6` — father, grandfather, grandmother).
`blind_ocr/cdkl5_distinct_children.csv` is that collapsed list; the per-row tables keep the rows
separate so the merge stays auditable.

Method, and why it is trustworthy:

- the mutation column in the survey was **never opened** by the extractor — a separate,
  blind pass OCR'd the screenshots into `blind_ocr/blind_mutations_cdkl5.csv`
- OCR: `rapidocr_onnxruntime` in an isolated venv at `C:\temp\ocr_env` (zf.12 untouched)
- a token counted only when it sat on, or within ±5 lines of, a line naming CDKL5 — the
  gene name either literally, or as OCR leaves it (`CDKLS`, `COKLS`, `CDK`+`L5`), or via the
  CDKL5 transcript accessions (`NM_003159`, `NM_001323289`), or the disease name / MIM number.
  Positions beyond the 3,093 bp CDKL5 CDS, and any token printed beside a non-X chromosome
  (`chr8:`), were discarded — this is what stops the lab's whole multi-gene variant table
  from being read as the patient's variant
- linkage by **nickname → birth year → city**, scored rather than first-hit: every survey
  row whose nickname overlaps the child's real name or WeChat name is scored (exact name >
  name inside the WeChat name > a 2+ character shared run, which is what links `暖暖妈…郭萌`
  to `郭暖暖`), a birth-year disagreement is disqualifying, and two different provinces is a
  hard veto. Mutation agreement is used **only** to break an exact tie, and any pair chosen
  that way is labelled `(mutation tiebreak)` — choosing the pair by the mutation and then
  reporting the mutation as corroborated would be circular.

## 6.1 Result

**Step 1 — Picture-derived CDKL5 mutation list (`blind_ocr/cdkl5_distinct_children.csv`, 290 children):**

| | consolidated tab | monthly tabs | total |
|---|---:|---:|---:|
| distinct children | 191 | 98 | **289** |
| complete `c.` point mutation | 163 | 75 | **238** |
| CNV / exon del-dup only | 15 | 4 | **19** |
| fragment only (`partial_only`) | 0 | 1 | **1** |
| no readable variant | 13 | 18 | **31** |
| **with a CDKL5 call** | 178 | 80 | **258 (89.3%)** |

- **239** children carry a `c.` token, of which **238 are complete** point mutations; multi-line wrapped tokens inside narrow clinical report cells are stitched back together in place.
- **19** children have a CDKL5 **CNV / exon deletion or duplication** (`EX7-EX9del`, `exon2-3 del`, `exon14 del`, `exon12 del`, `exon6-20 del`, `exon1-3 del`, `exon1 del`, whole-gene del, `chrX:18636850_18640535dup`). These are rewritten to HGVS cDNA form (`c.2277_2376dup (exon16 dup)`), with the caveat that a CNV breakpoint sits in an intron, so the positions are exon-level rather than base-exact.
- **206 distinct variants** in total: 192 distinct `c.` calls + 14 distinct CNVs. Hotspots: `c.533G>A` ×9, `c.1648C>T` ×6, `c.587C>T` ×5, `c.532C>T` ×5.
- **31** children uploaded only a cover/conclusion summary page or a blurry photo with no variant table.
- **1** child (甘牵岚) has one remaining fragment: her report photo cuts off at `c.785d…` (see §6.5).

**Step 2 — Cross-check against the survey Excel (`blind_ocr/comparison.csv`, 301 rows):**

Every child row is scored — one row each, so an unlinked child is visible rather than missing.
The survey (`cdkl5_cn_survey (20240902).xlsx`) predates 2025, so the monthly tabs are almost
entirely absent from it:

| outcome | all 301 | consolidated (197) | monthly (104) |
|---|---:|---:|---:|
| `MATCH` | 136 | 129 | 7 |
| `MATCH_1_OF_SEVERAL` | 1 | 1 | 0 |
| `CONSISTENT_OCR_PARTIAL` | 1 | 1 | 0 |
| **`MISMATCH`** | **5** | **5** | **0** |
| **`SURVEY_BLANK_OCR_HAS`** | **14** | **12** | **2** |
| `NOT_VERIFIABLE` | 14 | 12 | 2 |
| `UNLINKED` | 130 | 37 | 93 |

The consolidated column is the same set of pairs as the single-tab run — the survey row each
child was paired with did not move when the sweep widened to 25 tabs. All 5 disagreements remain
the same five, all in the consolidated tab. Two verdicts did improve, both because the survey
extract was finally regenerated (it had been locked open in Excel, so the file still held the
pre-refactor values): 武艺雯 is a `MATCH` now that `c.64+2（IVS2）de1T` is read whole instead of
truncated to `c.64+2`, and the comparison now re-reads the survey row it points at instead of
reusing the copy stored in the v1 pair.

The 7 monthly children that do link are real: they appear on the consolidated tab too, but with
a different set of photographs, so the monthly tab adds pages rather than a new child. Because
some of those extra pages carry the variant the consolidated row lacks (陈梦雅 becomes
`c.464_554del (exon8 loss)`), collapsing the pair improves coverage instead of double-counting.

## 6.2 The 5 disagreements

- **李洋** — survey `c.1195C>T`, report `c.1165C>T`. A single digit (1195 vs 1165); the two
  give different amino-acid changes, so one of them is wrong.
- **游奕可** (nickname 可可) — survey `c.1855>T`, report `c.1855A>T`. The survey cell is
  missing the 5′ base; the report supplies it. This is the malformed token already flagged
  in §4, now confirmed by the source: it should read **`c.1855A>T`**.
- **范牧荑** (牧牧) — survey `c.104A>G`, report `c.404A>G`. Same class of digit error as
  李洋. The survey's own protein annotation is `p.Asp135Gly`, which corresponds to
  `c.404A>G`, not `c.104A>G` — so the DNA position is the suspect part.
- **王以彤** (王以彤) — survey `c.553G>T`, report `c.533G>T` (`p.Arg178Leu`). Single-digit
  transcription slip in the survey (`553` vs `533`).
- **程钰琪** (程钰琪) — survey `c.282+3A>C`, report `c.282-3A>C` (intron 5 acceptor vs donor
  sign `+3` vs `-3`).

One remaining case where the survey truncated the deletion and the report supplies the missing
suffix:
- **陈怡霖** (怡霖) — survey `c.103_104(p.His36Ter)`, report **`c.103_104del`**

## 6.3 Thirteen cells that are empty in the survey `c.` column but have a `c.` variant in the report

- 孟欣苇 (苇苇) → `c.212A>G`
- 杨诗悦 (悦悦) → `c.2814delG` (survey raw cell had only `p.H939fs*14`)
- 李烨坤 (李烨坤) → `c.1934dup`
- 张语馨 (张语馨) → `c.428T>A`
- 罗诗皓 (皓皓) → `c.533G>T`
- 白舒诺 (小丸子) → `c.533G>A` (survey raw cell had only `chrX:18602452`)
- 韩雨萱 (韩雨萱) → `c.250C>T` (survey raw cell had `IVS9-1G>A`)
- 郭诗然 (郭诗然) → `c.1675C>T` (survey raw cell had only `ChrX:18622719. exon12`)
- 周泽宇 (乐乐) → `c.211A>G` (survey raw cell had only `4号`)
- 李芮安 (安子) → `c.931G>A`
- 吴一锘 (胡沐橙) → `c.683G>A` (survey raw cell had only `ChrX:18598085`)
- 江凤怡 (江凤怡) → `c.2635_2636del` (survey raw cell had only `cdkl5基因突变`)
- 江羽言 (小言) → `c.1996G>T` (survey raw cell had only `CDKL5`)

## 6.4 What the v2 pass fixed

The first OCR pass (kept as `blind_ocr/v1_*.csv`) had six defects, and the four-tab sweep and the
fragment review added four more; all are now corrected by `build_cdkl5_blind_table.py` and the
shared scanner in `cdna_tokens.py`:

| defect | effect |
|---|---|
| multi-line table cell wrapping not stitched | 18 children had only a truncated prefix (`C.1142`, `C.18`, `C.53`, `C.2814`, `C.507; C.508`, `C.5`) because `(exon12) delC` or `57del(p.Val620*)` wrapped onto the next line in the table |
| CDKL5 required the literal string within ±2 lines | 17 children lost their real variant — the gene name sat 3–5 lines away, or next to `chrX:185/186...`, or OCR wrote `COKLS` / `NMLS` / split `CDK`+`L5` across lines |
| CNV / exon deletions ignored | 14 children with exon/CNV deletions (`EX7-EX9del`, `exon14 del`, `exon12 del`, `exon6-20 del`, `exon1-3 del`, `exon1 del`, `whole-gene del`, `3.69kb dup`) were left blank |
| literature citations treated as patient variants | ACMG PM5/PS1 sentences citing other mutations at the same codon (`同一位置的变异c.533G>A...文献报道`, `[c.532C>T] [c.533G>C]`) polluted rows 114 and 163 |
| tokens de-duplicated case-sensitively & regex ran into `p.` | duplicate tokens (`C.2578C>T; c.2578C>T`) for 33 children and junk like `C.107A>CP.HIS36PRO` |
| `protein_tokens` was never filtered | 40+ proteins from other genes inside a file named *_cdkl5* |
| prose glued onto a finished token | `c.643A>Cinexon9oftheCDKL5gene` stayed unparsed (Lydia chen), and `c.532(exon8)C Arg178Trp` swallowed the protein name into the token |
| bare sample IDs read as cDNA | `C1/C2/C3` in `…、C1/C2/C3为3个正常对照` became `C.1; C.2; C.3` (王若汐), hiding the fact that her real finding is a CNV |
| exon-range shorthand not recognised | `ex.2_3del` (王若汐) matched no rule; the coordinate interval next to it is split by the cell layout, so the CNV was reported as “no call” |
| base change only stated in prose | 牛宸溪's table cell lost its `>T`; the narrative line carries the full change and is now used as a last-resort candidate |

Net effect on the consolidated tab alone: children with a complete CDKL5 variant from the
screenshots **124 → 182 / 197** (167 complete `c.` + 15 CNVs; 0 `partial_only`), linked pairs
**130 → 160**, corroborated pairs **79 → 128** (`MATCH` **65 → 128**), `NOT_VERIFIABLE`
**43 → 12**. Every per-child change is listed in `blind_ocr/blind_cdkl5_v2_changes.csv`, every
verdict change in `blind_ocr/comparison_changes.csv`.

One matching detail is worth recording: a v1 pair stores the survey row it was linked to, but
that row key includes the *variant text*, which is the very field under review. When a survey
cell was later corrected (`c.64+2` → `c.64+2delT`), the stale key no longer resolved and the pair
quietly lost its survey row. `survey_index_of` now falls back to nickname + birth year, and only
when that identifies exactly one row.

## 6.5 Caveat

OCR is not an authority. It reads confidently (~0.99 on clean pages) but the characters it can
confuse — `1/I/l`, `0/O`, `>` — are precisely the ones that matter here. Everything above is a
flag for review against the printed reports, not a correction applied to the data.

One child could not be resolved and is left flagged rather than guessed:

- **甘牵岚** (`m202501:10`, 2024-10-02) — the report print reads
  `NM_001323289.2:c.785d…` and the photo ends mid-token, so the deleted bases are not in any of
  the three uploaded pages (confirmed by re-OCR'ing a 4× upscaled crop of that cell). The
  protein annotation is `p.(Tyr262Ter)`, which is consistent with a deletion at codon 262 but
  does not pin down how many bases are lost. She stays `partial_only` until the next page of the
  report is photographed.

Three other children needed the same look and *were* resolvable from their own pages:

| child | was | now | how |
|---|---|---|---|
| Lydia chen (`m202501:12`) | `C.643A>CINEXON9OFTHECDKL5GENE` | **`c.643A>C`** (`p.Ser215Arg`) | OCR glued the prose `in exon 9 of the CDKL5 gene` onto the token |
| 牛宸溪 (`m202607:16`) | `C.532CARG178TRP` | **`c.532C>T`** (`p.Arg178Trp`, rs26760849) | the table cell lost its `>T`, but the report's own narrative states “编码序列第532位核苷酸由胞嘧啶核苷酸(C)替换为胸腺嘧啶核苷酸(T)” |
| 王若汐 (`m202606:4`) | `C.1; C.2; C.3` (sample IDs from the appendix page) | **`c.-162_99del (exon2-3 loss)`** | the report is a CNV: `CDKL5 NM_003159.3:ex.2_3del`, chrX:18,525,217-18,528,975, pathogenic |

Two further limits are worth stating plainly:

- **coverage, not completeness.** 758 unique pictures is the whole of this workbook, but the
  survey lists 225 patients and only 167 of those rows are claimed by any child here. The
  workbook is one snapshot of a submission form, not a registry.
- **the monthly tabs store their screenshots in columns 32–37**, the consolidated tab in
  110–115. Screenshots are therefore always located by their anchor, never by a hard-coded
  column, or 21 tabs would silently yield nothing.

Artefacts: `blind_ocr/cdkl5_distinct_children.csv` (one row per child — the authoritative
list), `blind_ocr/blind_mutations_cdkl5.csv` (one row per form row, with `child_key` and
`source_sheet`), `blind_ocr/blind_mutations.csv` (every token, all genes),
`blind_ocr/ocr_text.jsonl` + `blind_ocr/ocr_text_extra.jsonl` (full text of all 758 pages, so
any claim can be audited line by line), `blind_ocr/image_manifest.csv` (all 1,718 embedded
images with the dedupe decision for each), `blind_ocr/comparison.csv` (the verdict per child),
`blind_ocr/comparison_all_join.csv` (full outer join with the survey: 359 rows), plus the
`v1_*` backups.

Rebuild with:

```
cd cdkl5_aav
python -m projects.chinese_mutations_survey.export_screenshots
C:\temp\ocr_env\Scripts\python.exe -m projects.chinese_mutations_survey.extract_blind_mutations \
    --shots projects/chinese_mutations_survey/screenshots_extra \
    --out-jsonl projects/chinese_mutations_survey/blind_ocr/ocr_text_extra.jsonl \
    --out-csv   projects/chinese_mutations_survey/blind_ocr/blind_mutations_extra.csv
python -m projects.chinese_mutations_survey.build_cdkl5_blind_table
python -m projects.chinese_mutations_survey.rescore_blind_comparison
python -m projects.chinese_mutations_survey.build_all_join
python -m projects.chinese_mutations_survey.build_distinct_children
```

The first `extract_blind_mutations` pass (consolidated tab) is unchanged and its output
`blind_ocr/ocr_text.jsonl` is reused; only the extra tabs are OCR'd again. Budget ~51 s per
page: RapidOCR does not downscale, so every phone photo is detected at full resolution.

## 6.6 Tab-coverage audit — what the first pass never opened

The first extraction hard-coded `MASTER = "希舞宝贝情况登记（收集结果）"` and globbed
`screenshots/row*`, so it processed **490 of the workbook's 1,718 images (28.5%) and one of 25
image-bearing tabs**. Nothing flagged it, because a single-tab extraction looks complete from
the inside.

| tab | images | used by the first pass |
|---|---:|---|
| `希舞宝贝情况登记（收集结果）` (consolidated) | 490 | yes |
| `希舞宝贝情况登记（收集结果）(副本)` | 471 | no — earlier snapshot, all images already present |
| `20241201-20241231（收集结果）` | 483 | no — 470 duplicates, 13 unique |
| `20250101…20260930（收集结果)` (21 tabs) | 268 | no |
| `工作表1/2`, `智能表1/2` | 0 | n/a |

The omission cost real children: the monthly tabs hold **98 distinct children who appear
nowhere on the consolidated tab**, **80 of whom have a CDKL5 call** (75 complete `c.` + 4 CNV +
1 fragment). Those same children do not exist in the 2024 survey either, which is why 93 of the
104 monthly rows come out `UNLINKED` — that is the expected answer, not a linking failure.

Two guards now prevent a repeat of the blind spot: `export_screenshots.py` enumerates tabs from
the workbook instead of naming one, and it reports `duplicate` counts per tab, so a tab that
silently yields nothing is visible in the manifest.
