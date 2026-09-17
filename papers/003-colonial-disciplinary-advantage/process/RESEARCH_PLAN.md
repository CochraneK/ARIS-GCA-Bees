# RESEARCH PLAN — ARIS4C003

## 0. Status

**ARIS conditional GO · pre-data design.**

Primary principle: **historical theory first, contemporary outcomes second.** Historical exposure definitions, discipline coding, primary outcomes, and inference rules are frozen before the full contemporary country-by-field outcome matrix is inspected.

The design has three inferential layers rather than one omnibus regression:

1. **Former-colony/dependency disciplinary specialization** — scalable primary analysis.
2. **Former colonial dyad collaboration persistence** — scalable primary network analysis.
3. **Imperial-center disciplinary profiles** — theory-critical but small-N; use comparative/exact-style inference rather than pretending repeated fields create many independent empire observations.

Ranking/prestige analyses are secondary triangulation.

---

## 1. Units of analysis

### A. Country × discipline × year/window

Primary unit for former-colony/dependency specialization and bibliometric impact.

Core fields:
- country
- conceptual discipline + database taxonomy id
- year/window
- fractional publication output
- normalized citation impact
- elite-paper share
- international collaboration measures
- historical exposure variables
- source/coverage diagnostics

### B. Country-pair × discipline × year/window

Primary unit for network persistence.

Core fields:
- country_i
- country_j
- discipline
- coauthorship intensity
- direct former-colonial tie
- common colonizer
- common language
- distance/contiguity
- bilateral scientific mass
- other prespecified dyadic controls

### C. Imperial center × discipline × year/window

Small-N comparative layer. Repeated discipline observations are useful for profile comparisons but do **not** increase the number of independent imperial histories.

### D. University × discipline × ranking year

Secondary prestige/institutional layer using rankings and Leiden/OpenAlex-linked indicators where legally and publicly obtainable.

Do not collapse these datasets into one opaque score.

---

## 2. Historical exposures

Use the definitions in `EXPOSURE_PROTOCOL.md`.

### 2.1 Former-colony/dependency exposure — primary scalable country-level family

Candidate variables to freeze after source audit:
- total years under external colonial/dependency rule;
- ever formally colonized/dependent;
- primary/last colonizer;
- number of distinct colonizers;
- independence/end-of-rule year or cohort.

The primary duration measure should come from one documented source family rather than averaging incompatible datasets.

Do not prespecify a universally positive or negative coefficient. Colonizer identity, duration, institutional path, and independence period may generate heterogeneous effects.

### 2.2 Dyadic former-colonial exposure — primary scalable network family

Candidate variables:
- `direct_former_colonial_tie_ij`
- `common_colonizer_ij`
- `common_official_or_colonial_language_ij`
- end year/duration where available

Common language is both a potential persistence mechanism and a robustness adjustment. Models should be shown before and after language adjustment.

### 2.3 Imperial-center exposure — small-N secondary family

Candidate summaries:
- cumulative colony-years ruled;
- duration as overseas colonial ruler;
- number/peak number of dependencies;
- empire scale measures where historically defensible.

For a COLDAT-style European overseas-colonial definition there are only a handful of imperial centers. Therefore:
- emphasize profile effect sizes;
- use leave-one-empire-out analysis;
- use permutation/exact-style comparisons where meaningful;
- avoid naive large-sample clustered inference.

### 2.4 Out-of-scope primary mechanisms

Scientist migration, war-driven human-capital transfer, Cold War investment, and similar shocks are related **historical knowledge capital** mechanisms but are not part of the primary colonial exposure definition for ARIS4C003.

---

## 3. Discipline construct

### 3.1 Frozen conceptual confirmatory set

The following 21 conceptual fields were frozen before contemporary outcome inspection:

1. Anthropology
2. Archaeology
3. Geography
4. Development Studies
5. Linguistics
6. Tropical Medicine / colonial-health-related Public Health
7. Agriculture & Forestry
8. Geology / Earth-resource sciences
9. Sociology
10. Political Science / International Relations
11. Law
12. Economics
13. Public Administration / Social Policy
14. Education
15. History
16. Demography / Population Studies
17. Mathematics
18. Physics
19. Chemistry
20. Computer Science
21. Materials / modern engineering comparator

### 3.2 Imperial/Colonial Knowledge Entanglement Score (IKES)

Use `ENTANGLEMENT_PROTOCOL.md`.

IKES is coded outcome-blind across 11 dimensions covering administration, mapping, population/language classification, overseas fieldwork, extraction, colonial health, agriculture/forestry transfer, institutional transplantation, collections/archives, missionary/linguistic networks, and postwar development continuity.

Primary score: equal-weight mean after evidence review/adjudication. No contemporary performance data may be used in scoring or weighting.

### 3.3 Database crosswalk

Before outcome extraction, freeze `DISCIPLINE_CROSSWALK.csv` containing:
- conceptual field;
- OpenAlex field/subfield/topic ids;
- inclusion/exclusion rationale;
- ranking-category crosswalk where applicable;
- primary vs sensitivity mapping.

Use at least one alternative taxonomy/mapping as robustness where feasible.

---

## 4. Primary outcomes

### 4.1 Output specialization

Country c, discipline d, period t:

`RCA_output = (fractional_output_cdt / total_fractional_output_ct) / (world_output_dt / world_output_t)`

Primary analysis should use a bounded/symmetric or log-type transformation chosen **before** viewing historical-exposure associations.

Also report absolute fractional output so that high specialization based on tiny denominators is visible.

### 4.2 Scientific impact

Candidate primary/secondary metrics:
- field/year-normalized citation impact;
- PP(top 10%);
- PP(top 1%) as secondary because of denominator instability;
- citation-based specialization.

### 4.3 Collaboration/network outcomes

Country-level:
- international collaboration share;
- partner diversity/strength where stable.

Dyadic primary candidate:
- fractional coauthored output normalized by expected collaboration from bilateral field size.

Network centrality/brokerage is secondary because it is mechanically sensitive to network size and coverage.

### 4.4 Prestige/institutional outcomes

Secondary only:
- QS subject scores/components where publicly obtainable;
- THE subject indicators/ranks;
- Shanghai GRAS;
- Leiden Open Edition as open bibliometric institutional robustness.

Do not use naive OLS on ordinal rank values. Prefer component scores, top-N presence, bins, or ordinal/censored approaches when only ranks are available.

---

## 5. Confirmatory hypotheses and models

### H1 — former-colony/dependency disciplinary gradient

> Historical colonial/dependency exposure is associated with the contemporary shape of national disciplinary specialization as a function of outcome-blind IKES.

Primary repeated-window specification candidate:

`Y_cdt = beta * HistoricalExposure_c × IKES_d + alpha_ct + gamma_dt + error_cdt`

where:
- `alpha_ct` = country × time fixed effects, absorbing contemporary aggregate national scientific capacity in each period;
- `gamma_dt` = discipline × time fixed effects, absorbing global field-specific trends.

The estimand is cross-disciplinary covariance within country-periods. It is an association/path-dependence test, **not** proof that colonial exposure was exogenous.

If duration/colonizer identity are modeled, prespecify whether they enter continuously, categorically, or hierarchically.

### H2 — specificity

The historical-exposure association should vary monotonically with IKES rather than appearing uniformly across fields. Field-specific coefficients are secondary to the preregistered gradient test.

### H3 — heterogeneity among former colonies

Secondary prespecified analyses may stratify/hierarchically model:
- primary colonizer;
- duration;
- independence cohort;
- language;
- documented institutional/educational legacy proxies.

No universal signed effect is assumed.

### H4 — dyadic network persistence

`Collaboration_ijdt ~ DirectColonialTie_ij × IKES_d + gravity controls + FE`

Candidate controls:
- geographic distance;
- contiguity;
- bilateral scientific mass;
- region;
- common language (shown both excluded and included);
- other prespecified dyadic variables.

For count outcomes, PPML with appropriate high-dimensional fixed effects is a leading candidate; distribution and zero structure must be checked before freezing.

### H5 — imperial-center profile consistency

For the small set of imperial centers, test whether stronger historical empire exposure corresponds to greater specialization in high-IKES fields using:
- profile correlations/slopes;
- exact/permutation inference where defensible;
- leave-one-empire-out stability;
- effect-size visualization.

This is theory-critical corroboration, not the main large-sample causal estimate.

### H6 — prestige persistence

Estimate whether prestige/ranking outcomes are unusually high relative to contemporary bibliometric performance in historically entangled disciplines.

Use the label **prestige persistence/residual signal**, not causal "premium," unless a stronger design emerges.

---

## 6. Causal estimands and controls

Use `process/gptpage/2026-09-18_dag-review.md`.

Keep three estimands separate:

1. **Total long-run historical association** — do not automatically control away modern mediators such as R&D, university stock, English use, or collaboration.
2. **Association net of present-day aggregate capacity** — country-year fixed effects and/or explicitly labeled contemporary-capacity adjustments.
3. **Mechanism-specific persistence** — prestige, network, language, institutional pathways modeled separately.

Modern GDP/R&D/university size may be descendants of historical processes and therefore cannot be treated mechanically as baseline confounders.

---

## 7. Time design

Use fixed multi-year windows, preferably 4–5 years, from the earliest period with acceptable cross-national/field coverage through the latest complete period.

Time is used to ask whether persistence is weakening, stable, or strengthening:

`HistoricalExposure × IKES × Time`

Do not describe this as a historical difference-in-differences design unless genuine pre/post identification is separately established.

---

## 8. Data-quality rules

1. Fractional country attribution is primary.
2. Freeze a minimum country-field publication threshold before specialization analysis.
3. Report missingness/coverage by country, field, language, region, and time.
4. Conduct Anglophone/indexing sensitivity analyses.
5. Store raw immutable source files only when licensing permits; otherwise commit acquisition scripts/instructions.
6. Record source version, retrieval date, and checksums where practical.
7. Never redistribute ICOW or proprietary ranking tables contrary to source terms.
8. Keep ranking data secondary even if easier to obtain than bibliometric data.
9. Report absolute counts alongside relative specialization metrics.
10. Flag modern country-boundary/historical-entity crosswalk decisions explicitly.

---

## 9. Data source hierarchy

### Historical exposure
- COLDAT/Our World in Data processing for European overseas-colonial duration/intensity where appropriate;
- ICOW Colonial History for broader dependency/colonizer history and dyads;
- CEPII Gravity/GeoDist for colonial ties, common colonizer/language, distance and gravity controls.

Do not merge source concepts silently.

### Bibliometrics
- OpenAlex as primary scalable works/institution/country/field source;
- Leiden Ranking Open Edition for independent/open institutional robustness.

### Prestige/rankings
- QS, THE, Shanghai GRAS only through legally/publicly obtainable routes and with methodology differences preserved.

### Contemporary controls
- World Bank/UNESCO/OECD or other documented public sources as needed for explicitly defined secondary estimands.

A detailed license/acquisition ledger is maintained separately.

---

## 10. Robustness/falsification set

Bounded minimum set:

- fractional vs full counting;
- primary specialization transform vs one prespecified alternative;
- output vs impact/top-10% outcomes;
- alternative field crosswalk/taxonomy;
- alternative historical exposure source/definition;
- minimum-volume threshold sensitivity;
- exclude smallest states;
- leave-one-region-out;
- leave-one-colonizer/empire-out where sample permits;
- Anglophone vs non-Anglophone sensitivity;
- broader vs English/core publication coverage where measurable;
- recent vs earlier modern bibliometric windows;
- comparison fields;
- permuted/random IKES falsification;
- blinded historical scoring before outcomes.

If the headline appears only under one specification, downgrade the claim.

---

## 11. Multiple testing

Confirmatory inference centers on a small number of preregistered interaction/gradient tests.

For exploratory field-by-field scans:
- show every field;
- label exploratory analyses;
- use FDR when emphasizing p-values;
- visualize the complete coefficient distribution and uncertainty;
- never select only supportive fields for the manuscript narrative.

---

## 12. Small-N imperial-center safeguards

Because major imperial-center exposure is shared by only a small number of states:

- the country is the relevant historical treatment cluster;
- discipline repetitions do not justify conventional large-N confidence claims;
- report exact sample composition;
- use leave-one-center-out diagnostics;
- prioritize effect size/profile concordance;
- use exact/permutation approaches only when exchangeability assumptions are defensible;
- keep conclusions comparative and theory-supporting rather than causal.

This safeguard is non-negotiable.

---

## 13. GPTPage / no-paid-LLM-API policy

ARIS reasoning/reviewer stages that would normally require unavailable paid LLM APIs are replaced by reproducible prompt packets in `GPTPAGE_HANDOFF.md`.

Returned GPTPage/web outputs are saved under `process/gptpage/` with date/stage metadata and remain advisory until factual claims are independently checked.

This policy concerns **LLM/reviewer calls**. Scientific data should use documented bulk downloads, public snapshots, or legitimate public endpoints as appropriate; GPTPage is not a substitute for reproducible numerical datasets.

---

## 14. Pre-outcome gate

Already frozen:
- [x] canonical research question
- [x] colonizer vs colonized conceptual separation
- [x] inferential hierarchy / small-N imperial-center treatment
- [x] 21-field conceptual confirmatory set
- [x] 11-dimension IKES rubric
- [x] ranking-vs-bibliometric separation
- [x] causal-language / estimand distinction

Still required before the full outcome matrix:
- [ ] complete closest-prior-work search
- [ ] first historical IKES evidence coding
- [ ] independent second coding/adjudication
- [ ] database discipline crosswalk
- [ ] exact primary historical exposure variable/source
- [ ] primary bibliometric window
- [ ] minimum publication threshold
- [ ] primary specialization transformation
- [ ] clustering/exact-inference rules
- [ ] source license/acquisition ledger
- [ ] preregistration-style locked analysis specification

Only after this gate should the confirmatory outcome matrix be opened; all-field scans remain exploratory.
