# ARIS4C006 · Causal model and estimands

Last updated: 2026-09-18

## 1. What is treatment-like, and what is not

`SurnameInitialRank` is a stable pre-career attribute, but it is **not assumed randomized**. Chinese surnames have geographic, historical, clan, and demographic structure.

The institutional mechanism of interest is exposure to environments where coauthor credits are alphabetically ordered.

Define:
- `R_i`: surname Pinyin initial rank for scholar `i`;
- `A_ct`: independently estimated excess alphabetization intensity in context `c` at time `t`;
- `E_it`: scholar `i`'s lagged/cumulative exposure to `A` up to time `t`;
- `M_it`: mechanism-proximal outcomes such as listed position/visibility/collaboration;
- `Y_it`: downstream scholarly/career outcomes.

The primary object is effect modification by institutional exposure, operationalized through the interaction `R_i × E_it`.

## 2. Conceptual DAG

```text
Surname ancestry/geography ──► R_i
         │                    │
         ├──► education ──────┼──────────────► Y_it
         ├──► region ─────────┤
         └──► socioeconomic ──┘

ability/interests ─► field/journal/team choice ─► E_it
       │                         │                 │
       └─────────────────────────┴──────────────► Y_it

R_i × E_it ─► listed-position / visibility mechanisms M_it ─► Y_it

name commonness ─► OpenAlex disambiguation error ─► measured Y_it
       │
       └────────────────────────► measurement of R_i / career history
```

The design does not claim every path is observed. The DAG primarily prevents incorrect claims of surname randomization and highlights measurement bias.

## 3. Main estimand hierarchy

### Estimand 1 — institutional author-position interaction

Among eligible multi-author works in comparable field/year contexts:

> How does the association between surname rank and listed author position change as independently estimated alphabetization intensity increases?

This is the most mechanism-proximal estimand.

### Estimand 2 — cumulative visibility interaction

Among China-based author-years:

> Does prior cumulative alphabetization exposure modify the relationship between surname rank and subsequent visibility/credit outcomes?

Exposure must be lagged/cross-fitted.

### Estimand 3 — downstream career interaction

> Does prior cumulative alphabetization exposure modify the relationship between surname rank and later field-normalized impact, persistence, institutional transition, or observed geographic mobility?

This is weaker causally and should follow Estimands 1–2.

## 4. What population calibration does

ChineseNames provides expected surname/initial frequency in the underlying population database.

It helps answer:
- whether scholar initials are grossly over/underrepresented relative to population;
- whether database/parser problems are plausible;
- how misleading a uniform A–Z null would be.

It does **not** make surname rank randomly assigned among potential academics and does not by itself identify a career effect.

## 5. Exposure construction rules

`A_ct` must be estimated without the focal paper's outcome and preferably without the focal author's papers.

Preferred approaches:
1. leave-one-author-out context rate;
2. lagged journal/field convention rate;
3. cross-fitting by randomly partitioned papers/authors;
4. hierarchical/shrunken context rates for sparse cells.

Chance alphabetization is removed using team-size-specific random-order probabilities.

## 6. Primary work-level model

A generic specification:

`Position_ijct ~ R_i × A_ct + team-size + field×year FE + context controls + error`

Possible outcomes:
- `first_listed`;
- normalized list position;
- deviation from contribution-order proxies when independently available.

Inference should cluster at a level reflecting repeated scholars/context dependence; exact level will be frozen after the pilot structure is known.

## 7. Primary author-year model

`Y_it ~ R_i × E_i,t-1 + prior_Y + career_age + field×year FE + institution/context FE + error`

The coefficient on `R × E` is focal.

The standalone `R` coefficient is not interpreted as a clean causal effect.

## 8. Within-author strengthening design

Surname rank is time-invariant, but exposure can change when authors:
- change fields/subfields;
- move between journals/conference cultures;
- move institutions/countries;
- experience temporal changes in local authorship conventions.

A within-author design can ask whether outcomes change differentially for early- vs late-surname scholars when exposure changes.

Conceptually:

`Y_it ~ RankGroup_i × Exposure_it + author FE + field/year/context controls`

Because `RankGroup` itself is absorbed by author FE, identification comes from the interaction with time-varying exposure.

This is stronger than a cross-sectional surname comparison but still requires scrutiny of endogenous moves.

## 9. Potential quasi-experimental opportunities

Search prospectively for:
- journal policy/convention changes affecting author-order presentation;
- field-level shifts from alphabetical to contribution ordering;
- standardized contribution-taxonomy adoption;
- exogenous formatting/indexing changes that alter displayed order without changing contribution.

Do not manufacture a discontinuity after seeing outcomes. Each candidate event needs an independent date/source and parallel-trends/anticipation audit.

## 10. Controls: pre-treatment vs post-treatment

### Plausible baseline/pre-period adjustments
- field/year;
- career age/cohort;
- prior output/impact;
- institution/context before outcome window;
- surname frequency/uniqueness;
- parser/disambiguation-risk indicators for sensitivity.

### Variables that may be mediators
- team size;
- coauthor selection;
- journal choice;
- international collaboration;
- field switching.

When these are part of the mechanism, do not automatically control them away. Analyze total vs direct/mediated relationships explicitly.

## 11. Measurement-bias DAG

A major alternative explanation is:

`Surname frequency -> name collision -> author merge/split -> apparent publications/citations/career length`

and possibly:

`international mobility -> Westernized name order -> parser accuracy`

`international mobility -> outcomes`

This can generate spurious interaction patterns if high-alphabetization fields are also more international.

Therefore parser accuracy and author-disambiguation risk are part of the identification audit, not merely data cleaning.

## 12. Negative-control logic

### Negative-control exposure contexts
- very low measured alphabetization fields/journals;
- contribution-order environments.

### Negative-control outcomes
- outcomes on single-author works where coauthor order cannot operate;
- pre-exposure outcomes when temporally defined.

### Placebos
- future alphabetization intensity predicting earlier outcomes;
- randomized surname ranks preserving the empirical distribution;
- shuffled context exposure within field/year.

A robust institutional mechanism should fail these placebos.

## 13. Main competing explanations

1. **surname geography/ancestry** — rank correlates with unobserved background;
2. **field self-selection** — scholars choose high/low alphabetization environments;
3. **strategic coauthoring** — late-surname scholars adapt collaboration behavior;
4. **internationalization** — both name-order formatting and career outcomes differ;
5. **identity-resolution bias** — common names distort author-level metrics;
6. **database coverage** — fields/journals differ in OpenAlex completeness;
7. **pure chance ordering** — especially severe with two-author papers.

The analysis must distinguish these from the proposed visibility/credit mechanism where possible, or state them as unresolved alternatives.

## 14. Causal-language rule

Before a credible source of quasi-exogenous variation is found, use:
- “association”;
- “exposure gradient”;
- “consistent/inconsistent with the institutional mechanism”;
- “effect modification” descriptively where appropriate.

Reserve “causes” / “causal effect” for analyses whose identification assumptions have been separately defended.

## 15. Current DAG verdict

The project has a plausible mechanism and strong falsification structure, but **raw surname rank is not a natural experiment**. The most defensible strategy is triangulation across exposure gradients, negative controls, within-author exposure changes, and measurement-error audits.
