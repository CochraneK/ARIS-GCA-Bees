# ARIS4C006 · Pilot 15 — CCNC surname-specific Romanization audit

Last updated: 2026-09-19

## Verdict

**PASS for a high-precision surname-specific Romanization layer.**

ChineseNames remains the population-weight source. The pinned CCNC Romanized Chinese Last Names Dictionary supplies the surname-specific Hanyu-Pinyin form used for primary alphabetic ordering.

GitHub Actions run: `35324885259`  
Artifact: `aris4c006-ccnc-romanization-audit`

## Inputs

- ChineseNames family-name table: 1,806 surname rows.
- CCNC surname dictionary pinned at commit `a14520b9cc8bd6b251aeb4a7453ab1a45f23aa15`.
- 2024 all-field random OpenAlex/Crossref sample for outcome-blind bibliographic coverage.

## Dictionary intersection

- ChineseNames rows: **1,806**
- CCNC dictionary rows: **1,606**
- exact Han-surname intersection: **1,166**
- intersection by row count: **64.56%**
- represented ChineseNames population: **99.9671%**
- ChineseNames surnames not represented in the CCNC intersection: **640**

The row-count gap is concentrated in extremely rare surnames: those 640 rows represent only about **0.0329%** of the ChineseNames population mass.

## Initial discrepancies

CCNC surname-specific pronunciation and ChineseNames' supplied `initial` disagree for **31 surnames**, representing approximately **0.4383%** of the ChineseNames population baseline.

Important examples:

- 覃: CCNC **Tan**, ChineseNames initial q
- 单: **Shan**, ChineseNames initial d
- 解: **Xie**, ChineseNames initial j
- 褚: **Zhu**, ChineseNames initial c
- 仇: **Qiu**, ChineseNames initial c
- 查: **Zha**, ChineseNames initial c
- 区: **Ou**, ChineseNames initial q
- 万俟: **Moqi**, ChineseNames initial w

This validates the concern raised by Pilot 14: generic character pronunciation or unreviewed initials are insufficient for polyphonic surnames.

## Bibliographic mapping coverage

Across the 2024 all-26-field random sample:

- CN-affiliated structured-family rows: **1,292**
- exact CCNC canonical-Pinyin matches: **1,241**
- exact primary mapping coverage: **96.05%**

## Frozen separation of roles

- **ChineseNames**: population counts/frequencies, surname inventory, compound-surname flag.
- **CCNC**: surname-specific canonical Romanized form and primary alphabetic ordering key.
- **Crossref**: observed structured bibliographic family string.
- **OpenAlex**: work/authorship order, affiliation, primary-topic field, canonical author entity and longitudinal histories.
- **pypinyin**: QA/engineering diagnostic only, not confirmatory pronunciation authority.

## Homophone rule

When multiple Han surnames share one canonical Romanized form:

- aggregate ChineseNames population mass over those surnames;
- retain the shared Romanized ordering key;
- do not impute a specific Han surname unless independently observed.

## Primary focal rule after Pilot 15

A Romanized focal surname is primary-eligible only when:

1. structured Crossref family passes the frozen positional reconciliation;
2. normalized family exactly equals a frozen CCNC canonical surname form intersecting ChineseNames;
3. any available ORCID/canonical-author evidence does not conflict.

A direct-Han focal surname is primary-eligible only when the Han surname occurs in **both** ChineseNames and the frozen CCNC surname lexicon.

This sacrifices roughly 0.033% of population mass rather than use an unvalidated pronunciation for rare names.

## Gate consequence

**Surname-specific Romanization gate: PASS.**

The pypinyin-based mapping in Pilot 14 is superseded for confirmatory surname pronunciation/order.
