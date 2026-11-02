"""Score-based linking of form children to survey rows.

The v1 linkage took the *first* survey row whose nickname appeared in the child's
WeChat name and then either accepted or rejected that single candidate. That is
what went wrong for 郭萌 (nickname ``暖暖妈20230317郭萌``): the first ``暖暖`` hit
was 河北张家口 2017, the birth year disagreed, and the pair was dropped — the
correct row, ``郭暖暖`` 内蒙古锡盟 2023, was never tried.

Here every candidate is scored on the signals in the order they can be trusted:

1. **nickname** — exact real-name match beats "the survey nickname is inside the
   child's WeChat name" beats "the child's real name is inside the survey
   nickname";
2. **birth year** — agreement is required when both sides have one (a mismatch is
   disqualifying, not just a low score);
3. **city** — the survey writes places as free text (``内蒙古锡盟``) while the form
   gives ``自治区/盟/市``, so the comparison strips administrative suffixes and
   accepts common abbreviations (``锡盟`` = ``锡林郭勒盟``).

**Mutation agreement is only ever a tiebreak between candidates that already agree
on nickname, birth year and city, and any pair chosen that way is labelled.**
Choosing the pair *by* the mutation and then reporting the mutation as
corroborated would be circular — the comparison would agree with itself.
"""

from __future__ import annotations

import re

import pandas as pd

# administrative suffixes, longest first so 自治区 is removed before 区
_PLACE_SUFFIXES = (
    "维吾尔自治区", "回族自治区", "壮族自治区", "特别行政区", "自治区", "自治州",
    "自治县", "自治旗", "地区", "林区", "新区", "省", "市", "盟", "县", "区", "旗", "州",
)

_PROVINCES = (
    "内蒙古", "黑龙江", "河北", "山西", "辽宁", "吉林", "江苏", "浙江", "安徽", "福建",
    "江西", "山东", "河南", "湖北", "湖南", "广东", "广西", "海南", "四川", "贵州",
    "云南", "西藏", "陕西", "甘肃", "青海", "宁夏", "新疆", "北京", "天津", "上海",
    "重庆", "香港", "澳门", "台湾",
)

POSITIVE_BASIS = {
    "nickname",
    "nickname + birth date",
    "nickname + birth year",
    "nickname + birth year + city",
    "nickname + city",
    "nickname (fuzzy)",
    "nickname (fuzzy) + birth year",
    "nickname (fuzzy) + birth year + city",
    "nickname (fuzzy) + city",
    "birth year+month + city",
    "city + mutation",
    "duplicate form entry",
    "full birth date",
}
TIEBREAK_SUFFIX = " (mutation tiebreak)"

_NORM_CHARS = str.maketrans({"凱": "凯"})


def norm_nick_text(val) -> str:
    s = text(val).translate(_NORM_CHARS).replace("🍎", "苹果")
    return s


def row_key(nick, mut, birth) -> tuple[str, str, str]:
    """NaN-safe tuple key for claiming survey rows."""
    return (text(nick), text(mut), text(birth)[:4])


def survey_index_of(survey: pd.DataFrame, nick, mut, birth) -> int | None:
    """Position of the survey row matching a row key, or None when it is absent.

    The exact key includes the variant text, but that is the field the whole exercise
    disputes — a survey cell that has since been corrected ('c.64+2' -> 'c.64+2delT')
    would silently cost the pair its survey row. So the lookup falls back to
    nickname + birth year, and only when that identifies exactly one row.
    """
    key = row_key(nick, mut, birth)
    hits = [
        int(i)
        for i, r in survey.iterrows()
        if row_key(r["宝贝昵称"], r["基因变异点位"], r["出生年份"]) == key
    ]
    if hits:
        return hits[0]

    loose = (text(nick), text(birth)[:4])
    loose_hits = [
        int(i)
        for i, r in survey.iterrows()
        if (text(r["宝贝昵称"]), text(r["出生年份"])[:4]) == loose
    ]
    return loose_hits[0] if len(loose_hits) == 1 else None


def text(value) -> str:
    """str() that maps NaN/None to '', so a missing value never reads as 'nan'."""
    return "" if value is None or (isinstance(value, float) and value != value) or pd.isna(value) else str(value).strip()


def key_of(rec) -> str:
    """Globally unique child id: ``child_key`` when present, else ``master:{form_row}``.

    An Excel row number is only unique inside its own tab, and the workbook has 25
    tabs with screenshots, so every identity decision uses ``child_key``.
    """
    ck = text(rec.get("child_key"))
    return ck or f"master:{int(rec['form_row'])}"


def keys_column(children: pd.DataFrame) -> pd.Series:
    """The ``child_key`` series for a children frame, filled in when it is missing."""
    if "child_key" in children.columns:
        return children["child_key"].fillna("")
    return children["form_row"].map(lambda r: f"master:{int(r)}")


def provinces_conflict(survey_area, child_area) -> bool:
    """True when both sides name a province and they differ (one child, one province)."""
    s, c = province_of(survey_area), province_of(child_area)
    return bool(s and c and s != c)


def strip_place(text_val: str, drop_prov: str = "") -> str:
    """Drop province prefix and administrative suffixes from every component of a place string."""
    parts = re.split(r"[/、,，\s]+", str(text_val))
    out = []
    for part in parts:
        p = part.strip()
        if drop_prov and p.startswith(drop_prov):
            p = p[len(drop_prov):].strip()
        for suf in _PLACE_SUFFIXES:
            if p.endswith(suf) and len(p) > len(suf):
                p = p[: -len(suf)]
                break
        if drop_prov and p == drop_prov:
            continue
        if p:
            out.append(p)
    return "/".join(out)


def province_of(text_val: str) -> str:
    """The province-level name in a free-text location, '' when absent."""
    flat = re.sub(r"[/、,，\s]+", "", str(text_val))
    for prov in sorted(_PROVINCES, key=len, reverse=True):
        if flat.startswith(prov) or prov in flat:
            return prov
    return ""


def city_matches(survey_area, child_area) -> int:
    """2 = same city/county, 1 = same province only, 0 = nothing in common."""
    if pd.isna(survey_area) or pd.isna(child_area):
        return 0
    s_prov, c_prov = province_of(survey_area), province_of(child_area)
    if not s_prov or s_prov != c_prov:
        return 0
    if s_prov in {"北京", "天津", "上海", "重庆", "香港", "澳门"}:
        return 2

    child_parts = [p for p in strip_place(child_area, drop_prov=c_prov).split("/") if p]
    s_parts = [p for p in strip_place(survey_area, drop_prov=s_prov).split("/") if p]
    for s in s_parts:
        for c in child_parts:
            if s == c:
                return 2
            if len(s) >= 2 and (s in c or c in s):
                return 2
            # 锡盟 -> 锡 | 锡林郭勒 : abbreviations keep the first character
            if len(s) <= 2 and c.startswith(s[:1]) and s[-1] == c[:1]:
                return 2
    return 1


def longest_common_substring(a: str, b: str) -> int:
    """Length of the longest run of characters shared by two nicknames."""
    if not a or not b:
        return 0
    best = 0
    prev = [0] * (len(b) + 1)
    for ca in a:
        cur = [0] * (len(b) + 1)
        for j, cb in enumerate(b, 1):
            if ca == cb:
                cur[j] = prev[j - 1] + 1
                best = max(best, cur[j])
        prev = cur
    return best


def nick_score(survey_nick, child) -> int:
    """3 exact real-name, 2 survey nickname inside the WeChat name, 1 partial.

    The partial tier exists because the survey stores the full nickname
    (``郭暖暖``) while the WeChat name only carries the short form
    (``暖暖妈20230317郭萌``); a 2+ character shared run (or a reduplicated /
    diminutive root like ``笙笙`` -> ``笙``, ``刘小玥`` -> ``刘``+``玥``) puts the
    row on the shortlist, and birth year + city then decide.
    """
    nick = norm_nick_text(survey_nick)
    if len(nick) < 2:
        return 0
    real = norm_nick_text(child.get("real_name"))
    wx = norm_nick_text(child.get("wx_nickname"))
    if real and (nick == real or nick in wx and len(nick) >= 3):
        return 3
    if nick in real or nick in wx:
        return 2
    if real and len(real) >= 2 and real in nick:
        return 1
    if longest_common_substring(nick, wx) >= 2 or longest_common_substring(nick, real) >= 2:
        return 1
    # Reduplicated nickname '笙笙' -> '笙' in both real name ('封笙') and wx ('笙妈')
    if len(nick) == 2 and nick[0] == nick[1] and nick[0] in real and nick[0] in wx:
        return 1
    # Surname + diminutive '刘小玥' -> surname '刘' + given char '玥' in '刘玥言'
    if len(nick) == 3 and nick[1] == "小" and real.startswith(nick[0]) and nick[2] in real:
        return 1
    return 0


def birth_year(value) -> str:
    if pd.isna(value):
        return ""
    m = re.search(r"(19|20)\d{2}", str(value))
    return m.group(0) if m else ""


def child_years(child) -> set[str]:
    """Birth years recorded in either birth_raw or wx_nickname (parents often type YYYYMMDD in wx)."""
    yrs = set()
    for field in ("birth_raw", "wx_nickname"):
        y = birth_year(child.get(field))
        if y:
            yrs.add(y)
    return yrs


def mut_agrees(child, row) -> bool:
    blind_val = re.sub(r"\s+", "", text(child.get("cdna_cdkl5"))).upper().replace("DE1", "DEL").replace("DEI", "DEL")
    surv_val = re.sub(r"\s+", "", text(row.get("基因变异点位"))).upper().replace("DE1", "DEL").replace("DEI", "DEL")
    if not blind_val or not surv_val:
        return False
    return blind_val in surv_val or surv_val in blind_val


def score_candidate(child, row) -> dict:
    """All signals for one child/survey-row pair."""
    sy = birth_year(row.get("出生年份"))
    c_years = child_years(child)
    n = nick_score(row.get("宝贝昵称"), child)
    c = city_matches(row.get("所在地区（省市）"), child.get("area"))
    if sy and c_years:
        if sy in c_years:
            y = 2
        elif n == 3 and c == 2 and any(abs(int(sy) - int(cy)) == 1 for cy in c_years):
            # Exact 3-char real name + exact city, 1-year typo between form and survey (e.g. 刘思妍)
            y = 1
        else:
            y = -5
    else:
        y = 0
    return {"nick": n, "year": y, "city": c, "total": n + y + c}


def build_pairs(children: pd.DataFrame, survey: pd.DataFrame, anchors: list[dict]) -> tuple[list[dict], list[dict]]:
    """Return ``(pairs, link_log)``.

    ``anchors`` are the pairs an earlier pass already established; they are kept
    exactly as they are. Every other child is matched against the survey rows no
    anchor claimed, best score first, one-to-one.
    """
    claimed = {row_key(a["survey_nick"], a["survey_mutation"], a["survey_birth"]) for a in anchors}
    pairs = [dict(a) for a in anchors]
    for p in pairs:
        idx = p.get("survey_idx")
        if idx is None or pd.isna(idx):  # NaN arrives from the CSV baseline, not None
            p["survey_idx"] = survey_index_of(survey, p["survey_nick"], p["survey_mutation"], p["survey_birth"])
    log: list[dict] = []

    anchor_keys = {key_of(a) for a in anchors}
    child_keys = keys_column(children)
    pending = children[~child_keys.isin(anchor_keys)]

    scored: list[tuple[int, int, dict, dict]] = []
    for _, child in pending.iterrows():
        best: list[tuple[int, dict, dict]] = []
        for _, row in survey.iterrows():
            key = row_key(row["宝贝昵称"], row["基因变异点位"], row["出生年份"])
            if key in claimed:
                continue
            s = score_candidate(child, row)
            if s["nick"] == 0 or s["year"] < 0:
                continue
            # a partial-nickname match alone is too weak to carry a pair
            if s["nick"] == 1 and s["city"] == 0:
                continue
            if provinces_conflict(row.get("所在地区（省市）"), child.get("area")):
                # Only allow cross-province when exact 3-char real name + birth year + mutation
                # agree (e.g. 汪子涵 treated in another province), or nickname + exact YYYYMMDD + mutation.
                wx_digits = re.sub(r"\D+", "", text(child.get("wx_nickname")))
                b_digits = re.sub(r"\D+", "", text(child.get("birth_raw")))
                exact_ymd_in_wx = bool(b_digits and len(b_digits) == 8 and (b_digits in wx_digits or b_digits[:4] + b_digits[5:8] in wx_digits))
                if not (s["year"] == 2 and mut_agrees(child, row) and (s["nick"] == 3 or (s["nick"] >= 2 and exact_ymd_in_wx))):
                    continue
            best.append((s["total"], s, row))
        if not best:
            continue
        top = max(t for t, _, _ in best)
        winners = [(s, r) for t, s, r in best if t == top]
        # Deduplicate identical survey entries (e.g. 安安 福建厦门 2018 c.592G>T entered twice in the survey)
        uniq_winners: list[tuple[dict, dict]] = []
        seen_keys: set[tuple[str, str, str]] = set()
        for s, r in winners:
            rk = row_key(r["宝贝昵称"], r["基因变异点位"], r["出生年份"])
            if rk not in seen_keys:
                seen_keys.add(rk)
                uniq_winners.append((s, r))
        winners = uniq_winners

        if len(winners) > 1:
            # mutation may only break an exact tie between otherwise equal candidates
            agree = [(s, r) for s, r in winners if mut_agrees(child, r)]
            if len(agree) == 1:
                winners = agree
                tier = "tiebreak"
            else:
                log.append(
                    {
                        "child_key": key_of(child),
                        "form_row": int(child["form_row"]),
                        "real_name": child["real_name"],
                        "reason": "ambiguous after nickname + year + city",
                        "candidates": " | ".join(f"{r['宝贝昵称']}({r['所在地区（省市）']},{r['出生年份']})" for _, r in winners),
                    }
                )
                continue
        else:
            tier = ""
        scored.append((top, key_of(child), winners[0][0], {"child": child, "tier": tier, "row": winners[0][1]}))

    # highest score first; a survey row can only be claimed once
    for total, child_key_, s, extra in sorted(scored, key=lambda x: (-x[0], x[1])):
        child, tier, row = extra["child"], extra["tier"], extra["row"]
        rk = row_key(row["宝贝昵称"], row["基因变异点位"], row["出生年份"])
        if rk in claimed:
            continue
        claimed.add(rk)

        basis = "nickname" if s["nick"] >= 2 else "nickname (fuzzy)"
        if s["year"] > 0:
            basis += " + birth year"
        if s["city"] == 2:
            basis += " + city"
        elif provinces_conflict(row.get("所在地区（省市）"), child.get("area")):
            tier = "tiebreak"
        if tier == "tiebreak":
            basis += TIEBREAK_SUFFIX

        pairs.append(
            {
                "child_key": child_key_,
                "source_sheet": child.get("source_sheet"),
                "form_row": int(child["form_row"]),
                "real_name": child["real_name"],
                "wx_nickname": child["wx_nickname"],
                "survey_idx": int(row.name),
                "survey_nick": row["宝贝昵称"],
                "match_basis": basis,
                "survey_mutation": row["基因变异点位"],
                "survey_birth": row["出生年份"],
                "survey_area": row["所在地区（省市）"],
                "blind_birth": child["birth_raw"],
                "blind_area": child["area"],
            }
        )
        log.append(
            {
                "child_key": child_key_,
                "form_row": int(child["form_row"]),
                "real_name": child["real_name"],
                "reason": f"linked ({basis})",
                "candidates": f"{row['宝贝昵称']} | {row['出生年份']} | {row['所在地区（省市）']}",
            }
        )

    # Pass 2: for children still unlinked (survey used a baby nickname not in real_name/wx_nickname),
    # link when (city == 2 + birth year within 1 yr + exact mutation) uniquely identifies an unclaimed row,
    # OR when the child is a duplicate form submission of an already-linked child (same name + birth + variant).
    linked_ids = {key_of(p) for p in pairs}
    still_pending = children[~keys_column(children).isin(linked_ids)]
    for _, child in still_pending.iterrows():
        child_k = key_of(child)
        c_years = child_years(child)
        # Check duplicate form entry first (e.g. row 17 & row 18 陈玥彤 submitted by both parents)
        dup_hit = next(
            (
                p for p in pairs
                if text(p["real_name"]) == text(child.get("real_name"))
                and text(p["blind_birth"]) == text(child.get("birth_raw"))
                and text(p["real_name"])
            ),
            None,
        )
        if dup_hit is not None:
            pairs.append(
                {
                    "child_key": child_k,
                    "source_sheet": child.get("source_sheet"),
                    "form_row": int(child["form_row"]),
                    "real_name": child["real_name"],
                    "wx_nickname": child["wx_nickname"],
                    "survey_idx": dup_hit.get("survey_idx"),
                    "survey_nick": dup_hit["survey_nick"],
                    "match_basis": "duplicate form entry",
                    "survey_mutation": dup_hit["survey_mutation"],
                    "survey_birth": dup_hit["survey_birth"],
                    "survey_area": dup_hit["survey_area"],
                    "blind_birth": child["birth_raw"],
                    "blind_area": child["area"],
                }
            )
            continue

        cands_cm = []
        for _, row in survey.iterrows():
            rk = row_key(row["宝贝昵称"], row["基因变异点位"], row["出生年份"])
            if rk in claimed:
                continue
            sy = birth_year(row.get("出生年份"))
            if city_matches(row.get("所在地区（省市）"), child.get("area")) == 2 and mut_agrees(child, row):
                if not sy or not c_years or any(abs(int(sy) - int(cy)) <= 1 for cy in c_years):
                    cands_cm.append(row)
        # Deduplicate identical survey entries (e.g. 汤圆 湖北随州 c.2354del)
        uniq_cm = []
        seen_cm: set[tuple[str, str]] = set()
        for r in cands_cm:
            k2 = (text(r["宝贝昵称"]), text(r["基因变异点位"]))
            if k2 not in seen_cm:
                seen_cm.add(k2)
                uniq_cm.append(r)
        if len(uniq_cm) == 1:
            row = uniq_cm[0]
            claimed.add(row_key(row["宝贝昵称"], row["基因变异点位"], row["出生年份"]))
            pairs.append(
                {
                    "child_key": child_k,
                    "source_sheet": child.get("source_sheet"),
                    "form_row": int(child["form_row"]),
                    "real_name": child["real_name"],
                    "wx_nickname": child["wx_nickname"],
                    "survey_idx": int(row.name),
                    "survey_nick": row["宝贝昵称"],
                    "match_basis": "city + mutation" + TIEBREAK_SUFFIX,
                    "survey_mutation": row["基因变异点位"],
                    "survey_birth": row["出生年份"],
                    "survey_area": row["所在地区（省市）"],
                    "blind_birth": child["birth_raw"],
                    "blind_area": child["area"],
                }
            )
    return pairs, log
