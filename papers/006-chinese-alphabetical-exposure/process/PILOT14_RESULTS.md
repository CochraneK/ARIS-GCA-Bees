# ARIS4C006 · Pilot 14 — generic pypinyin mapping diagnostic

Last updated: 2026-09-18

## Verdict

**Engineering coverage diagnostic only. Superseded as the confirmatory surname-pronunciation map.**

GitHub Actions run: `35301818928`  
Artifact: `aris4c006-canonical-pinyin-map`

## What the pilot showed

Using `pypinyin == 0.55.0` and ChineseNames' supplied initial as a repair constraint:

- ChineseNames rows: **1,806**
- auto-accepted: **1,803**
- unresolved: **3**
- row coverage: **99.834%**
- population coverage: **99.9918%**
- sampled 2024 CN-affiliated structured-family rows: **1,153**
- exact mapped rows: **1,102**
- bibliographic coverage: **95.58%**

These results show that a conservative Hanyu-Pinyin-style focal sample can retain high coverage.

## Why the mapping rule is rejected as confirmatory truth

The algorithm implicitly treated ChineseNames `initial` as the authority for choosing among polyphonic readings.

The ChineseNames documentation describes SNI as alphabetical order of a surname's Pinyin initial, but it does not document a surname-pronunciation lexicon or algorithm.

Known polyphonic surnames expose the risk:
- 单 is surname-specific **Shan**;
- 解 is surname-specific **Xie**;
while generic character pronunciation tools may select `dan` / `jie`.

Therefore a generic character-to-Pinyin library plus ChineseNames initial cannot serve as the final pronunciation truth.

## Corrected separation of roles

- **ChineseNames:** population counts/frequencies.
- **Surname-specific lexicon:** canonical Hanyu-Pinyin surname form.
- **Crossref structured family:** actual bibliographic family string/order key.
- **pypinyin:** QA/fallback diagnostic only.

The corrected pronunciation layer is being built from CCNC's Romanized Chinese Last Names Dictionary, which explicitly maps surname forms to Pinyin.

## Population aggregation rule retained

When multiple Han surnames share the same validated Romanized bibliographic form, population mass is aggregated across those surnames.

A Romanized record is not assigned a specific Han character surname unless that character form is independently observed.

## Gate consequence

**Generic pypinyin map: superseded.**  
**Surname population weights remain valid; surname-specific Romanization gate remains OPEN until the corrected lexicon audit passes.**
