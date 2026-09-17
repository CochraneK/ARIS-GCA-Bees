# ARIS4C006 · First real-data feasibility pilot

Last updated: 2026-09-18

## Status

**Pilot completed successfully. These outputs validate the data path; they are not confirmatory surname-effect estimates.**

GitHub Actions run: `35275257207`

Artifact: `aris4c006-data-feasibility-pilot`

The workflow successfully:

1. downloaded a public plain-CSV engineering mirror of the ChineseNames `familyname` table;
2. verified the expected 1,806 surname rows;
3. generated a 26-initial population baseline;
4. queried a bounded sample of 1,000 OpenAlex works with mainland-China (`CN`) institutional authorships in 2024;
5. retained 993 eligible multi-author works;
6. generated field × team-size author-order summaries;
7. uploaded a public-safe pilot artifact.

The canonical confirmatory surname baseline must still be reproduced from the pinned `ChineseNames == 2025.8` R package via `code/00_export_chinesenames.R`.

## 1. Chinese surname population baseline

Total population count represented by the `familyname` table:

**1,181,719,774**

The distribution across Latin/Pinyin initials is extremely non-uniform.

Largest initial groups:

| Initial | Population | Share |
|---|---:|---:|
| L | 224,001,885 | 18.96% |
| Z | 183,810,656 | 15.55% |
| W | 138,390,660 | 11.71% |
| Y | 91,844,031 | 7.77% |
| C | 85,553,439 | 7.24% |
| H | 76,521,203 | 6.48% |
| X | 59,106,538 | 5.00% |
| S | 56,385,505 | 4.77% |
| G | 41,799,694 | 3.54% |
| D | 35,218,158 | 2.98% |

Derived facts:

- `L + Z + W` = **46.22%** of the population baseline.
- The five largest initials = **61.23%**.
- Population-weighted mean initial rank = **16.21**, compared with 13.5 under a uniform A–Z distribution.
- A–M contains **48.15%** and N–Z **51.85%**; this near-half split hides strong internal concentration.
- A–F = **13.41%**; G–M = **34.74%**; N–T = **11.81%**; U–Z = **40.04%**.
- I, U, and V contain no surnames in this 1,806-surname table; E is extremely rare.

### Interpretation

This directly confirms a central design decision: a uniform 1/26 surname-initial null is scientifically inappropriate for Chinese names.

It also reveals a potentially stronger mechanism than originally emphasized: Chinese surname mass is shifted toward later Latin initials, particularly W/X/Y/Z. In an internationally mixed team that uses strict alphabetical authorship, this population composition may create a **group-level expected author-position burden** for China-affiliated authors relative to collaborators drawn from countries with earlier surname distributions.

That international-composition mechanism requires its own novelty and feasibility audit before becoming the canonical paper question.

## 2. OpenAlex extraction pilot

Parameters:

- publication year: 2024;
- requested works: 1,000;
- eligible multi-author works: **993**;
- API key: none required for this bounded pilot;
- field × team-size summary cells: **273**.

The extraction path successfully retained:

- listed author order;
- raw/display names;
- field assignment;
- journal/source metadata;
- team size;
- China-affiliation filter.

### Important limitation

The pilot deliberately used `HEURISTIC_ONLY_LAST_LATIN_TOKEN` to verify engineering mechanics. This is **not a valid confirmatory Chinese surname parser**.

Therefore the pilot's observed alphabetical-order rates are not substantive scientific results.

The unstratified first 1,000-work pull was also dominated by large natural-science fields (e.g. Engineering, Medicine, Computer Science) and contained very few Economics or Psychology papers. It cannot estimate cross-field convention differences reliably.

## 3. What the pilot established

### Passed

- [x] ChineseNames surname table can be transformed into a reproducible 26-initial population baseline.
- [x] The Chinese surname-initial distribution is sufficiently non-uniform to make population calibration essential.
- [x] OpenAlex can provide a bounded China-affiliated multi-author work sample with ordered authorships and relevant context metadata.
- [x] Team-size-adjusted chance-ordering calculations are technically feasible.
- [x] CI can produce public-safe derived outputs without retaining the raw mirror.

### Not yet passed

- [ ] validated surname extraction from Chinese/Romanized OpenAlex names;
- [ ] differential parser-error audit by surname rank and internationalization;
- [ ] OpenAlex author split/merge audit;
- [ ] stratified high- vs low-alphabetization field pilot;
- [ ] longitudinal author-year reconstruction;
- [ ] cross-fitted context exposure construction;
- [ ] confirmatory career outcomes.

## 4. Immediate design consequence

The next pilot should **not** simply increase the random sample size.

It should deliberately sample:

- known high-alphabetization fields (e.g. Economics, Mathematics, selected business/social-science contexts);
- low-alphabetization comparison fields;
- all-China vs internationally mixed teams;
- 2-author vs 3+ author teams;
- records with Chinese-character name evidence vs Romanized-only names.

The goal is to establish whether local alphabetization exposure and international-team composition provide enough independent variation for the proposed mechanism.

## 5. Current verdict

**Data-path GO; inferential GO remains conditional.**

The first pilot strengthens feasibility but does not clear the two critical scientific gates: surname parsing and author identity resolution.
