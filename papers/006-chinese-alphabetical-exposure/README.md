# ARIS4C006 · Alphabetical Exposure and Academic Careers in Chinese Science

**Status:** feasibility / novelty-gated ARIS run

**ARIS provenance:** v0.4.26 · `951654847b015585385b2448c5667dcd04e7b56b`

## Canonical research question

> Among Chinese scholars, does surname alphabetical position predict academic visibility or career outcomes specifically when scholars are exposed to fields, journals, and collaborations that use alphabetical author ordering, after calibrating against the highly non-uniform population distribution of Chinese surnames?

## Why this is not a simple “A beats Z” paper

Chinese surnames are extremely uneven across Pinyin initials: common surnames such as Wang, Li, Zhang, Liu, Chen, Yang, Huang, Zhao, Wu, and Zhou concentrate population mass in particular letters. Therefore raw counts of successful scholars by surname initial are not interpretable without a population denominator.

The focal exposure is not the letter itself. It is the interaction between:

1. **alphabetical vulnerability** — where a surname falls in A–Z Pinyin order; and
2. **alphabetical exposure** — how strongly the scholar's field/journal/coauthorship environment actually orders authors alphabetically.

The design therefore treats surname position as a stable inherited attribute and alphabetization as the institutional mechanism that may convert it into differential visibility or credit.

## Novelty gate

Two close precedents materially constrain the paper:

- Einav & Yariv (2006) established alphabetical discrimination in economics and used psychology as a non-alphabetical comparison.
- Li & Yi (2021) already studied Chinese economists relative to Chinese physicists/statisticians and found surname-position differences in US-versus-China job placement.
- D'Angelo (2026) tested surname-initial bias in inclusion in the global top-2% scientist list/c-score using expected national surname distributions.

Therefore ARIS4C006 must **not** claim novelty for merely showing that early surname initials correlate with academic success, nor for merely adding a Chinese sample.

The intended contribution is the joint combination of:

- a near-population Chinese surname denominator (`ChineseNames`);
- all/large-scale Chinese science rather than only economics;
- directly measured field/journal/year alphabetization intensity;
- longitudinal author-level exposure rather than a field label alone;
- mechanism tests on authorship visibility and collaboration;
- multiple career outcomes with negative-control fields and specifications.

## Primary estimand

A generic specification is:

`Outcome(i,t) ~ SurnameRank(i) × AlphabetizationExposure(i,t) + controls + FE`

where `AlphabetizationExposure` is estimated from observed multi-author publication order in the scholar's field/journal/year environment rather than assigned by stereotype.

The coefficient on the interaction is the main object. A standalone coefficient on `SurnameRank` is descriptive and secondary.

## Population calibration

Canonical baseline: `ChineseNames` version 2025.8, whose underlying surname database covers 1,806 surnames and about 1.2 billion Han Chinese household-registered people born 1930–2008 and alive in 2008.

Required baseline quantities:

- surname frequency;
- Pinyin initial;
- alphabetical rank 1–26;
- population share by initial;
- surname uniqueness;
- compound-surname indicator.

Observed scholar distributions must be compared with expected distributions under this population baseline. Equal 1/26 letter probabilities are prohibited.

## Main outcome families

### Mechanism-proximal
- first-listed-author frequency conditional on team structure;
- visibility under first-author/`et al.` citation conventions;
- single- vs multi-authorship;
- coauthor choice and team size;
- deviation from alphabetical order;
- corresponding-author probability where available.

### Scientific impact
- field/year-normalized citation impact;
- top-10% and top-1% cited-paper shares;
- author-level citation trajectories;
- h-index or analogous cumulative metrics as secondary outcomes.

### Career / mobility
- affiliation trajectory;
- transition into/out of high-prestige institutions;
- international mobility, especially China ↔ overseas;
- persistence/exit from publishing;
- elite-list inclusion only as a secondary validation outcome.

## Main data stack

1. **ChineseNames 2025.8** — population surname denominator and name covariates.
2. **Ministry of Public Security national name reports** — contemporary validation of common surnames and geographic concentration; not a bulk individual-level source.
3. **OpenAlex** — works, author order, raw author names, affiliations, country, topics/fields, citations, corresponding-author flag, and longitudinal publication histories.
4. **Optional validation lists** — CAS academicians and other transparent public elite rosters, used only as secondary outcomes.

## Major confounding threats

- Chinese surnames correlate with geography and ancestry/clan history; surname rank is not automatically randomized.
- Pinyin romanization can create parsing ambiguities and variant spellings.
- OpenAlex author disambiguation can split or merge common Chinese names.
- affiliation country is not nationality; “Chinese scholar” must have a frozen operational definition.
- alphabetical ordering can occur by chance, especially in two-author papers.
- field choice and international publishing exposure are endogenous.
- cumulative metrics create survivorship and career-age bias.

## Required negative controls / falsification

The institutional-mechanism account weakens if:

- surname rank predicts outcomes equally in low-alphabetization and high-alphabetization environments;
- effects appear in single-authored output where author ordering cannot operate;
- effects do not scale with empirically measured alphabetization intensity;
- results disappear after population calibration and career-age/field controls;
- results are entirely generated by author-disambiguation failures among common surnames;
- replacing true surname rank with randomized ranks yields similar effects.

## Hard pre-analysis gates

- [ ] freeze the operational definition of “Chinese scholar”;
- [ ] freeze surname parsing/romanization rules;
- [ ] build and validate the Chinese surname initial population baseline;
- [ ] define excess-alphabetization above random chance (`1/n!`) by team size;
- [ ] freeze field/journal/year exposure construction without using focal career outcomes;
- [ ] run author-disambiguation stress tests stratified by surname frequency/name commonness;
- [ ] complete closest-prior-work map;
- [ ] preregister primary outcomes and model hierarchy before confirmatory outcome inspection.

## Interpretation boundary

A positive interaction would support an institutional authorship-order mechanism under the measured publication regime. It would **not** establish that alphabetically earlier surnames intrinsically cause ability, personality, intelligence, or scientific quality.
