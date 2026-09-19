#!/usr/bin/env python3
"""Deterministic date-only traditional-calendar features for ARIS4C013.

Scope is deliberately narrow. No hour pillar, Ten Gods, hidden stems, Na Yin,
luck pillars, or auspiciousness rules are exposed.
"""
from __future__ import annotations

from datetime import date
from importlib.metadata import version as package_version
from typing import Any

from lunar_python import Lunar, Solar

PINNED_LUNAR_PYTHON = "1.4.8"

INSTALLED_LUNAR_PYTHON = package_version("lunar_python")
if INSTALLED_LUNAR_PYTHON != PINNED_LUNAR_PYTHON:
    raise RuntimeError(
        f"lunar_python {PINNED_LUNAR_PYTHON} required; "
        f"found {INSTALLED_LUNAR_PYTHON}"
    )

STEMS = ("甲","乙","丙","丁","戊","己","庚","辛","壬","癸")
BRANCHES = ("子","丑","寅","卯","辰","巳","午","未","申","酉","戌","亥")
ANIMALS = ("鼠","牛","虎","兔","龙","蛇","马","羊","猴","鸡","狗","猪")
ELEMENTS = ("Wood","Fire","Earth","Metal","Water")

STEM_ELEMENT = {
    "甲":"Wood","乙":"Wood",
    "丙":"Fire","丁":"Fire",
    "戊":"Earth","己":"Earth",
    "庚":"Metal","辛":"Metal",
    "壬":"Water","癸":"Water",
}
STEM_POLARITY = {
    "甲":"Yang","乙":"Yin",
    "丙":"Yang","丁":"Yin",
    "戊":"Yang","己":"Yin",
    "庚":"Yang","辛":"Yin",
    "壬":"Yang","癸":"Yin",
}
JIA_ZI = tuple(
    STEMS[i % 10] + BRANCHES[i % 12]
    for i in range(60)
)
JIA_ZI_INDEX = {gz:i for i,gz in enumerate(JIA_ZI)}
BRANCH_INDEX = {z:i for i,z in enumerate(BRANCHES)}
STEM_INDEX = {g:i for i,g in enumerate(STEMS)}

SOLAR_TERMS = (
    "立春","雨水","惊蛰","春分","清明","谷雨",
    "立夏","小满","芒种","夏至","小暑","大暑",
    "立秋","处暑","白露","秋分","寒露","霜降",
    "立冬","小雪","大雪","冬至","小寒","大寒",
)
SOLAR_TERM_INDEX = {name:i for i,name in enumerate(SOLAR_TERMS)}

JIE_TERMS = (
    "立春","惊蛰","清明","立夏","芒种","小暑",
    "立秋","白露","寒露","立冬","大雪","小寒",
)


def split_ganzhi(gz: str) -> tuple[str, str]:
    if len(gz) != 2 or gz[0] not in STEM_INDEX or gz[1] not in BRANCH_INDEX:
        raise ValueError(f"unexpected Gan-Zhi value: {gz!r}")
    return gz[0], gz[1]


def ganzhi_payload(gz: str | None) -> dict[str, Any] | None:
    if gz is None:
        return None
    gan, zhi = split_ganzhi(gz)
    return {
        "ganzhi": gz,
        "cycle_index": JIA_ZI_INDEX[gz],
        "stem": gan,
        "stem_index": STEM_INDEX[gan],
        "branch": zhi,
        "branch_index": BRANCH_INDEX[zhi],
        "animal": ANIMALS[BRANCH_INDEX[zhi]],
        "stem_element": STEM_ELEMENT[gan],
        "stem_polarity": STEM_POLARITY[gan],
    }


def _normal_term_table(lunar) -> dict[str, Any]:
    table = lunar.getJieQiTable()
    return {name:table[name] for name in SOLAR_TERMS if name in table}


def _terms_on_date(lunar, ymd: str) -> list[str]:
    table = _normal_term_table(lunar)
    return [
        name for name in SOLAR_TERMS
        if name in table and table[name].toYmd() == ymd
    ]


def _preceding_solar_term(lunar, solar_noon) -> str | None:
    table = _normal_term_table(lunar)
    current_jd = solar_noon.getJulianDay()
    candidates = [
        (term_solar.getJulianDay(), name)
        for name, term_solar in table.items()
        if term_solar.getJulianDay() < current_jd
    ]
    if not candidates:
        return None
    return max(candidates)[1]


def date_only_features(d: date) -> dict[str, Any]:
    """Return only features supportable from a civil birth date.

    Noon is used as a neutral representative time. Any date containing a
    relevant astronomical transition is explicitly flagged ambiguous before a
    Bazi-style year/month feature is returned.
    """
    solar = Solar.fromYmdHms(d.year, d.month, d.day, 12, 0, 0)
    lunar = solar.getLunar()
    ymd = solar.toYmd()
    terms_today = _terms_on_date(lunar, ymd)
    on_li_chun = "立春" in terms_today
    on_jie = any(name in JIE_TERMS for name in terms_today)
    on_any_term = bool(terms_today)

    official_year_gz = lunar.getYearInGanZhi()

    # Bazi-style year is ambiguous for date-only records on Li Chun itself.
    bazi_year_gz = (
        None if on_li_chun else lunar.getYearInGanZhiByLiChun()
    )

    # Month branch changes at Jie. Without birth time, the transition date is
    # unresolved; do not guess which side of the boundary applies.
    bazi_month_gz = (
        None if on_jie else lunar.getMonthInGanZhiExact()
    )

    # Civil-date sexagenary day: deterministic at noon, deliberately not
    # labeled a personal Bazi day pillar.
    civil_day_gz = lunar.getDayInGanZhi()

    preceding_term = None if on_any_term else _preceding_solar_term(lunar, solar)

    lunar_month = int(lunar.getMonth())
    lunar_day = int(lunar.getDay())

    return {
        "source_date": d.isoformat(),
        "implementation": {
            "library": "lunar_python",
            "version": PINNED_LUNAR_PYTHON,
            "representative_time": "12:00:00",
        },
        "boundary_flags": {
            "solar_terms_on_date": terms_today,
            "on_any_solar_term_date": on_any_term,
            "on_li_chun_date": on_li_chun,
            "on_jie_date": on_jie,
        },
        "official_chinese_calendar": {
            "lunar_month": abs(lunar_month),
            "lunar_day": lunar_day,
            "is_leap_month": lunar_month < 0,
            "year": ganzhi_payload(official_year_gz),
        },
        "bazi_style_date_only": {
            "year": ganzhi_payload(bazi_year_gz),
            "year_ambiguous_without_birth_time": on_li_chun,
            "month": ganzhi_payload(bazi_month_gz),
            "month_ambiguous_without_birth_time": on_jie,
        },
        "solar_term_phase": {
            "preceding_term": preceding_term,
            "preceding_term_index": (
                None if preceding_term is None
                else SOLAR_TERM_INDEX[preceding_term]
            ),
            "ambiguous_without_birth_time": on_any_term,
        },
        "civil_date_sexagenary_day": ganzhi_payload(civil_day_gz),
        "scope_warning": (
            "Date-only encoding; not a complete Four-Pillars/Bazi chart."
        ),
    }
