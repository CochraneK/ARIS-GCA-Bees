# ARIS4C006 · Literature seed and novelty map

Last searched: 2026-09-18

## Purpose

This file is a **novelty gate**, not a narrative literature review. ARIS4C006 should proceed only if its confirmatory design is materially distinguishable from the closest prior work below.

## 1. Separate two literatures that are easy to conflate

### 1A. Name-letter effect / implicit egotism

This literature asks whether people prefer letters in their own names or make choices associated with name similarity.

- Nuttin, J. M. (1985). *Narcissism beyond Gestalt and awareness: The name letter effect*. European Journal of Social Psychology, 15, 353–361. DOI: `10.1002/ejsp.2420150309`.
- Pelham, B. W., Mirenberg, M. C., & Jones, J. T. (2002). *Why Susie sells seashells by the seashore: Implicit egotism and major life decisions*. Journal of Personality and Social Psychology, 82(4), 469–487. DOI: `10.1037/0022-3514.82.4.469`.
- Simonsohn, U. (2011). *Spurious? Name similarity effects (implicit egotism) in marriage, job, and moving decisions*. Journal of Personality and Social Psychology, 101(1), 1–24. DOI: `10.1037/a0021990`.

The current paper does **not** use implicit egotism as its primary mechanism. It focuses on institutional author-order rules that can mechanically convert surname position into visibility/credit.

### 1B. Alphabetical authorship / surname-order effects

This is the primary literature for ARIS4C006.

## 2. Closest prior work

### Einav & Yariv (2006) — foundational institutional mechanism

Einav, L., & Yariv, L. (2006). *What's in a Surname? The Effects of Surname Initials on Academic Success*. Journal of Economic Perspectives, 20(1), 175–187. DOI: `10.1257/089533006776526085`.

Key contribution:
- studied faculty in top U.S. economics departments;
- earlier surname initials were associated with several academic-success outcomes;
- psychology was used as a comparison field where coauthors are not normatively alphabetized;
- authors explicitly linked the pattern to economics' alphabetical-author-order convention.

**Implication for 006:** cross-field heterogeneity in alphabetization is already an established identification idea. Our novelty cannot be “compare an alphabetical field with a non-alphabetical field.”

### Li & Yi (2021) — direct Chinese predecessor

Li, W., & Yi, J. (2021). *Alphabetical Author Order, Intellectual Collaboration and High-Skilled Migration*. The Economic Journal, 131(635), 1250–1268. DOI: `10.1093/ej/ueaa049` (online publication 2020).

Key contribution:
- Chinese economists are compared with Chinese physicists/statisticians;
- later surname initials among Chinese economists are associated with lower probability of staying in the United States and greater probability of working in China;
- the Chinese context is used to isolate alphabetical authorship because names are rarely alphabetized in other Chinese social contexts.

**Implication for 006:** neither “Chinese academics” nor “China/US mobility” is novel by itself. This is the closest predecessor and must be foregrounded in any manuscript.

### Wohlrabe & Bornmann (2022) — large-scale null/qualification on citations

Wohlrabe, K., & Bornmann, L. (2022). *Alphabetized co-authorship in economics reconsidered*. Scientometrics, 127, 2173–2193. DOI: `10.1007/s11192-022-04322-9`.

Key contribution:
- >120,000 multi-authored economics papers;
- alphabetization declined over time;
- after extensive controls, alphabetical coauthorship had little or no general citation relationship;
- team size strongly affected the probability of alphabetization.

**Implication for 006:** do not equate alphabetical ordering with higher citations. Estimate mechanisms and heterogeneity directly, and correct for chance ordering by team size.

### Öz (2024) — recent multi-field comparison

Öz, A. B. (2024). *Overcoming alphabetical disadvantage: factors influencing the use of surname initial techniques and their impact on citation rates in the four major disciplines of social sciences*. Scientometrics, 129, 4885–4908. DOI: `10.1007/s11192-024-05100-5`.

Key contribution:
- 70,377 publications from 2,278 academics, 2011–2020;
- Economics, Psychology, Political Science, Sociology;
- alphabetical ordering was more prevalent in Economics and Political Science;
- investigated behavioral responses to alphabetical disadvantage and citation outcomes.

**Implication for 006:** merely expanding from two to more disciplines is insufficient novelty. The exposure should be empirically continuous/granular and longitudinal rather than a discipline dummy.

### D'Angelo (2026) — most recent overlap

D'Angelo, C. A. (2026). *Testing for alphabetical bias in the c-score: Implications for evaluating scientific excellence*. Journal of Informetrics, 20(3), 101841. DOI: `10.1016/j.joi.2026.101841`.

Key contribution:
- compares observed vs expected surname-initial distributions across countries;
- expected distributions are derived from national Scopus-indexed author populations;
- later alphabetical position predicts lower inclusion in the Ioannidis Top Scientists List/c-score framework;
- effects vary strongly by macro-field and are strongest in humanities/economics/social sciences, while negligible or reversed in engineering/computing.

**Implication for 006:** population/expected-distribution calibration alone is no longer a novel contribution in 2026. Elite-list inclusion alone would substantially duplicate this work.

## 3. Additional relevant literature to map before preregistration

Priority search clusters:

1. strategic coauthor choice in response to alphabetical rules;
2. credit perception when alphabetical order conflicts with contribution order;
3. first-author visibility / `et al.` citation practices;
4. field-specific authorship conventions;
5. surname-initial effects in grant, hiring, tenure, conference, editorial, and ranking contexts;
6. author-order convention changes over time;
7. Chinese scholar name disambiguation / bibliometric identity errors;
8. geographic/clan structure of Chinese surnames;
9. surname romanization variants and family-name parsing.

Known anchor:
- Kadel, A., & Walter, A. (2015). *Do scholars in Economics and Finance react to alphabetical discrimination?* Finance Research Letters. DOI: `10.1016/j.frl.2015.05.015`.

## 4. Chinese-name data literature

### ChineseNames

Canonical software/data source:
- Bao, H.-W.-S. `ChineseNames`: Chinese Name Database 1930–2008, current package version 2025.8.
- Dataset contains 1,806 surnames and 2,614 given-name characters, covering about 1.2 billion Han Chinese household-registration records represented in the source database.
- `familyname` supplies Chinese surname, compound-surname indicator, Pinyin initial, rank 1–26, counts, ppm, and surname uniqueness.

The package version date must not be mistaken for the underlying population year: the database remains 1930–2008.

## 5. Novelty decision

### Ideas already occupied

ARIS4C006 must **not** claim novelty for:

- surname-initial effects on academic success;
- economics-vs-non-economics field comparisons;
- a Chinese-academic sample;
- China/US academic mobility as an outcome;
- expected vs observed surname-initial distributions;
- field heterogeneity in alphabetical bias;
- elite-scientist-list inclusion as the main endpoint.

### Remaining defensible contribution

The project remains a **conditional GO** if it successfully combines all of the following:

1. a Chinese population surname denominator rather than equal A–Z probabilities;
2. a large China-based scholarly population across many fields;
3. **observed journal/field/year/team-size-adjusted alphabetization intensity**, not a categorical assumption about disciplines;
4. author-level longitudinal cumulative exposure to those regimes;
5. mechanism-proximal outcomes (author position, collaboration behavior, visibility) before distal career outcomes;
6. negative-control settings in which author order cannot or rarely should matter;
7. explicit stress tests for Chinese-name parsing and OpenAlex author disambiguation;
8. longitudinal career outcomes beyond the already-studied China/US placement comparison.

The manuscript should describe this as an **institutional exposure study**, not as evidence of a psychological “name-letter effect.”

## 6. Search provenance / current tool constraints

- Public web search: active, used for current publisher records and documentation.
- Elicit MCP: attempted 2026-09-18; connected account does not include API access.
- Consensus MCP: attempted 2026-09-18; monthly search quota exhausted (reset reported as 2026-10-01).
- These failures are not treated as evidence gaps; GPTPage/public academic search is the fallback for the pre-registration closest-prior-work sweep.

## 7. Gate

**Verdict: CONDITIONAL GO.**

Do not open confirmatory career outcomes until the remaining closest-prior-work sweep and the exposure/name-parsing feasibility pilot are completed.
