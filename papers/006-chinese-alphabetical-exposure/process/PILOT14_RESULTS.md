# ARIS4C006 · Pilot 14 — canonical Hanyu-Pinyin surname map

Last updated: 2026-09-18

## Verdict

**Canonical Chinese surname-form mapping gate: PASS.**

Primary focal surname forms may use a conservative direct-Han / exact-canonical-Hanyu-Pinyin rule without relying on unreviewed legacy or regional Romanizations.

GitHub Actions run: `35301818928`  
Artifact: `aris4c006-canonical-pinyin-map`

## Construction

Input:
- 1,806 ChineseNames `familyname` rows.

Romanization engine:
- `pypinyin == 0.55.0`.

Internal check:
- ChineseNames supplies the expected Latin initial for every surname;
- default Pinyin was accepted when its first letter matched the ChineseNames initial;
- default mismatches entered a heteronym search;
- only a **unique** initial-consistent repair was automatically accepted;
- unresolved rows were excluded rather than guessed.

## Dictionary result

- ChineseNames surname rows: **1,806**
- accepted canonical surname rows: **1,803**
- unresolved rows: **3**
- row coverage: **99.8339%**
- population coverage: **99.9918%**
- accepted compound surnames: **62 / 63**
- distinct canonical Romanized bibliographic forms after aggregation: **413**

## Unresolved surnames

The three automated unresolved rows were:

| Surname | Expected initial | Default | Initial-consistent candidates | Population n |
|---|---|---|---|---:|
| 尉 | Y | wei | yu; yun | 87,816 |
| 朝 | Z | chao | zhao; zhu | 8,817 |
| 万俟 | W | moqi | none | 3 |

These rows are excluded from automated confirmatory Romanized mapping unless separately reviewed and frozen before outcome analysis.

## Romanized-form aggregation

Multiple Chinese-character surnames can share the same Hanyu-Pinyin family form.

For Romanized bibliographic records, the population mapping therefore uses:

`PopulationN(romanized form) = sum population counts of all accepted ChineseNames surnames mapping to that form`.

The analysis does **not** pretend to know the exact Chinese character surname from an ambiguous Romanized form.

Direct-Han records can retain exact-character population frequency as a sensitivity.

## Bibliographic coverage pilot

Across reproducibly sampled 2024 works spanning all 26 primary-topic fields:

- CN-affiliated structured-family rows: **1,153**
- exact canonical-Pinyin matches: **1,102**
- exact mapping coverage: **95.58%**

The remaining ~4.4% are not automatically treated as non-Chinese people. They are simply outside the conservative confirmatory focal surname-form mapping.

## Frozen primary mapping rule

A focal authorship is ChineseNames-mappable for the primary mechanism frame only if:

1. direct validated Han surname maps to ChineseNames; or
2. Crossref structured family name, normalized for case/diacritics/separators, **exactly equals** one of the frozen canonical Hanyu-Pinyin forms.

Unreviewed variants such as legacy, Cantonese, or other regional spellings are not added adaptively.

They may enter a separately reviewed sensitivity dictionary only if frozen before focal outcomes are inspected.

## Gate consequence

**Focal surname-form mapping: PASS.**

The study can retain a high-precision primary sample with approximately 95.6% mapping coverage in the contemporary random bibliographic pilot while covering >99.99% of the ChineseNames population baseline.
