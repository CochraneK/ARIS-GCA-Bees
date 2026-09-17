# ARIS4C006 · Executable research plan

Last updated: 2026-09-18

## 1. Target question

> In the mainland-China scholarly system, does later Pinyin surname position lead to worse authorship visibility or downstream career outcomes specifically when scholars are exposed to publication environments that empirically use alphabetical author ordering more often?

The primary mechanism is institutional author-order exposure, not implicit egotism and not intrinsic properties of names.

## 2. Unit structure

The project uses several linked levels rather than forcing one regression to answer everything.

### Level A — surname population
One row per Chinese surname / initial using `ChineseNames`.

### Level B — work/authorship
One row per authorship on an eligible scholarly work.

### Level C — context
Journal × field × year (or a coarser field × year cell when sparse), used to estimate the local convention for alphabetical ordering.

### Level D — author-year
One row per resolved OpenAlex author per year, containing cumulative/pre-period alphabetization exposure, collaboration history, affiliation, and outcomes.

## 3. Frozen conceptual variables

### Surname position
Primary continuous exposure:

`SurnameInitialRank ∈ {1,...,26}`

where A=1 and Z=26 according to Pinyin surname initial.

Secondary specifications:
- population-weighted surname percentile;
- initial groups/quintiles for visualization only;
- exact surname fixed/stratified comparisons where sample size permits.

### Population frequency
Use surname/initial frequencies from `ChineseNames`.

A uniform A–Z probability is never a valid null for Chinese surnames.

### Institutional alphabetization exposure
The focal moderator is not a discipline label. It is the empirically estimated tendency of a publication environment to order coauthors alphabetically beyond chance.

For each context `c,t`:

`ObservedAlphaRate(c,t)` = share of eligible multi-author works whose parsed surnames are in lexicographically ascending order.

`ExpectedChance(c,t)` = team-size-weighted expected alphabetical share under random ordering, with tie adjustment.

Candidate normalized measure:

`ExcessAlpha(c,t) = (ObservedAlphaRate - ExpectedChance) / (1 - ExpectedChance)`

Context estimates must be cross-fitted, leave-one-work-out, lagged, or otherwise constructed so a focal paper does not mechanically determine its own exposure.

## 4. Primary population

Primary frame:

> authorships linked by OpenAlex to at least one mainland-China (`CN`) institution, subsequently aggregated to author-year panels when the author satisfies the frozen longitudinal inclusion criteria.

The study describes this as the **China-based scholarly system**. It does not infer citizenship, nationality, or ethnicity from names.

Only records with sufficiently high surname-parsing confidence enter confirmatory surname-effect models.

## 5. Surname parser protocol

### Phase 5A — direct-character cases
If `raw_author_name` contains Chinese characters, detect single and compound surnames using a longest-match dictionary built from `ChineseNames`.

### Phase 5B — Romanized names
Build a validated surname-romanization dictionary with:
- standard Hanyu Pinyin;
- surname-specific pronunciations for polyphonic characters;
- common legacy/regional romanizations where evidence supports them;
- compound surnames.

Use raw-name variants, ORCID-linked records, and consistency across works to infer which token is the family name.

### Phase 5C — confidence
Assign `surname_parse_tier` and `surname_parse_confidence`.

Tier-3 heuristic-only parses cannot enter the confirmatory sample.

### Phase 5D — blinded validation
Validate a stratified sample before focal career outcomes are inspected. Freeze minimum precision/coverage requirements in the preregistration.

## 6. OpenAlex extraction

### Work query
Collect eligible works with at least one authorship affiliated with a `CN` institution.

Retain:
- OpenAlex work ID;
- DOI where available;
- publication year/date;
- source/journal ID;
- primary topic/field hierarchy;
- citations and normalized citation information where available;
- ordered authorships;
- each `raw_author_name`;
- resolved author ID/display name/ORCID;
- raw affiliation strings;
- resolved institution IDs/country codes;
- `is_corresponding`.

### Time window
Do not freeze the final confirmatory window until the pilot establishes coverage. Candidate main window: 2010–2025, allowing lagged convention estimates and career follow-up.

The final window must be frozen before confirmatory focal-outcome analysis.

## 7. Alphabetization classifier

For each paper with >=2 reliably parsed surnames:

1. convert each surname to a canonical Romanized ordering key;
2. preserve the actual listed author sequence;
3. flag exact non-decreasing alphabetical order;
4. record team size;
5. calculate chance probability under random permutation;
6. separately flag ties and ambiguous parsing;
7. estimate observed-minus-expected alphabetization by context.

### Team-size rule
Two-author alphabetical order occurs by chance about half the time if surnames differ, so it is weak convention evidence. Primary convention estimation should either:
- model chance explicitly for every team size; and/or
- emphasize teams of 3+ as a robustness specification.

## 8. Outcomes and hierarchy

### Tier 1 — mechanism-proximal confirmatory outcomes

1. listed-author position among multi-author works;
2. probability of being first listed, conditional on team composition/context;
3. corresponding-author status, where coverage is adequate;
4. collaboration/team-size behavior;
5. departures from alphabetical ordering in high-exposure contexts.

### Tier 2 — longitudinal scientific outcomes

1. field/year-normalized citation trajectory;
2. top-10%/top-1% paper share;
3. publication persistence / observed career length;
4. entry into higher-prestige institutional strata, after prestige metric is frozen;
5. observed international affiliation transitions.

### Tier 3 — secondary descriptive outcomes

- h-index and other cumulative metrics;
- public elite-roster inclusion;
- overall publication counts.

Tier 3 cannot carry the headline result alone.

## 9. Primary model family

At author-year level, a generic model is:

`Y(i,t) = β1 Rank(i) + β2 AlphaExposure(i,t-1) + β3 Rank(i)×AlphaExposure(i,t-1) + controls + FE + ε(i,t)`

The focal coefficient is `β3`.

Potential fixed effects depending on outcome:
- field × year;
- institution × year or institution strata;
- career-age bins;
- publication cohort;
- journal/context effects in work-level models.

Controls may include:
- surname population frequency/uniqueness;
- team size;
- career age;
- prior output/impact when temporally appropriate;
- collaboration/internationalization history.

Do not add post-treatment variables as routine controls.

## 10. Descriptive population-calibration layer

Before regression, report for each initial:

- population expected share from ChineseNames;
- observed share among China-affiliated authorships/authors;
- observed/expected ratio;
- uncertainty intervals.

This is descriptive quality control and context, not the causal test.

Large deviations may reveal selection, romanization, database coverage, or disambiguation problems and must be investigated before interpreting them as career effects.

## 11. Identification strategy

The strongest internal evidence is a **dose-response interaction**:

- surname rank should matter more where measured alphabetization exposure is high;
- it should weaken toward zero in low-exposure contexts;
- mechanism-proximal author-position outcomes should move first;
- distal career outcomes, if present, should be downstream and smaller.

This is stronger than a raw cross-sectional surname-success correlation but is still not automatically causal because field/context selection can be endogenous.

### Strengthening designs

1. **Within-author change in environment**: scholars moving between contexts with different prior alphabetization intensities.
2. **Journal convention changes over time**: event-study-style analyses if stable discontinuities can be identified independently of focal outcomes.
3. **Matched/coarsened comparisons**: similar career stage/field/institution authors with different surname ranks.
4. **Cross-fitted exposure**: estimate convention from other papers/authors.
5. **Field × year fixed effects**: absorb broad disciplinary trends.

Any quasi-experimental claim requires a separate assumptions audit.

## 12. Negative controls and falsification

Mandatory:

- single-authored works: no coauthor-order channel exists;
- low-alphabetization contexts;
- randomized surname ranks preserving the empirical surname distribution;
- placebo exposure based on future convention intensity;
- high-confidence name subset;
- ORCID-linked subset where feasible;
- uncommon-name subset to reduce author-identity collision risk;
- 3+ author teams separately from two-author teams.

The institutional mechanism is weakened if surname rank predicts outcomes similarly where author order cannot matter.

## 13. Error / bias audits

### Name parsing
Report coverage and precision by surname frequency, field, institution, international mobility, and decade.

### OpenAlex identity resolution
Stress-test split/merge errors and check whether diagnostics correlate with surname rank/frequency.

### Database coverage
Compare field/year/journal coverage against independent counts where feasible.

### Geography / surname ancestry
Chinese surnames are geographically structured. Because birthplace/province-of-origin is not directly observed, do not claim surname rank is randomized. Use institution/geographic fixed effects where meaningful and interpret residual rank effects cautiously.

## 14. Analysis order to prevent researcher degrees of freedom

### Stage 0 — no focal outcomes
- literature novelty sweep;
- data/license check;
- surname baseline construction;
- name-parser validation;
- author-disambiguation audit;
- alphabetization convention estimator.

### Stage 1 — mechanism pilot
- only author-order/context outcomes needed to validate exposure;
- do not optimize specifications against citations/career endpoints.

### Stage 2 — freeze
- final sample;
- window;
- parser threshold;
- exposure estimator;
- primary outcomes;
- model hierarchy;
- exclusion rules;
- multiplicity strategy.

### Stage 3 — confirmatory outcomes
Run frozen models once, then clearly separate confirmatory from exploratory extensions.

## 15. Minimum pilot acceptance criteria

Before promoting from feasibility to confirmatory-ready:

1. sufficient OpenAlex authorship coverage in multiple high/low alphabetization fields;
2. clear between-context variation in excess alphabetization;
3. surname parser reaches a pre-specified high precision on validation sample;
4. author-disambiguation diagnostics are not strongly monotonic with surname rank after restrictions;
5. ChineseNames-derived expected initial shares can be reproduced from pinned source data;
6. convention estimates are stable to excluding two-author papers and ambiguous names;
7. no closest prior paper is found that already combines population-calibrated Chinese surnames, continuous measured convention exposure, and longitudinal all-field career outcomes.

If these fail, narrow or stop the paper rather than forcing a result.

## 16. Deliverables

- frozen surname-population baseline;
- surname parser + validation report;
- OpenAlex extraction manifest;
- alphabetization exposure table;
- author-year panel;
- preregistration-style specification;
- analysis scripts;
- robustness/falsification suite;
- manuscript with an explicit novelty and limitations section.

## 17. Current decision

**ARIS conditional GO to pilot/data-feasibility stage.**

No confirmatory career-effect result should be generated before Stage 2 freeze.
