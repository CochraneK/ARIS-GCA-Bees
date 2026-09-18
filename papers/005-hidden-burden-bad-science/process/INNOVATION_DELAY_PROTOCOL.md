# INNOVATION DELAY PROTOCOL — ARIS4C005

## Purpose

Estimate whether a documented scientific-integrity shock changes the subsequent vitality and timing of nearby legitimate research.

This module is deliberately separate from article-level prevalence and Researcher-Life-Years.

Primary question:

> After an integrity shock, does a narrowly defined neighboring research topic receive fewer new papers, fewer new entrants, less funding, or slower emergence than a credible counterfactual topic trajectory?

---

## Empirical precedent

Azoulay, Furman, Krieger & Murray (2015, Review of Economics and Statistics, DOI 10.1162/REST_a_00469) studied more than 1,100 retractions. Relative to carefully selected controls, intellectually related papers experienced a lasting 5–10% citation decline after retraction, with larger penalties for fraud/misconduct than honest mistakes; the study also reported reduced arrival of new articles and funding flows into affected fields.

This is a design precedent, not a parameter to copy into ARIS4C005.

---

## Exposure

Primary treatment event:

- date/year at which a source work receives a formal retraction or another high-confidence scientific-integrity shock;
- exposure family recorded separately: E1-S, E1-M, E1-P, E3;
- the first confirmatory analysis should prioritize adjudicated E1-S sources.

Retraction date is an observation/governance event, not necessarily the date the underlying problem began.

---

## Unit

Primary unit: a **topic-neighborhood cluster**, not an individual author.

A treated cluster is constructed from legitimate works intellectually close to the source paper but not themselves the source paper.

Possible neighborhood definitions:

- pre-shock bibliographic coupling;
- pre-shock citation-network proximity;
- pre-shock semantic embedding similarity;
- shared concepts/keywords or field/subfield;
- combinations of the above.

All neighborhood features used for matching must be measured before the shock.

---

## Controls

Each treated topic cluster should be matched to one or more control clusters using only pre-shock information.

Match dimensions should include where available:

- pre-shock outcome trajectory;
- field/subfield;
- publication vintage;
- topic size;
- citation intensity;
- number of active authors;
- funding intensity;
- semantic novelty/interdisciplinarity;
- database coverage/access.

Do not match on post-retraction citations, post-retraction publication volume, later funding, or any variable affected by treatment.

---

## Outcomes

### Primary

1. **Article arrivals** — legitimate new works entering the topic per year.
2. **New-author entry** — authors publishing in the topic for the first time.
3. **Funding flow** — new/active grant value or count where a compatible funder dataset exists.

### Secondary

4. citations/attention to neighboring legitimate work;
5. collaboration-network entry/exit;
6. semantic novelty/diversity of new work;
7. milestone/rediscovery timing where a defensible milestone can be defined.

Do not define innovation loss from citation decline alone.

---

## Event-study estimand

For matched set m and event time k:

D_mk = treated outcome_mk − mean(control outcomes_mk)

Normalize each matched set by its own pre-shock difference:

E_mk = D_mk − mean(D_mk over frozen baseline years)

The aggregate event-study effect at k is the mean E_mk across matched sets.

Primary baseline window:

- event years −3, −2, −1

Primary post window:

- event years 0 through +5

Longer windows are secondary because database coverage and treatment contamination increase with time.

---

## Pre-trend requirement

Event-study estimates are not interpreted causally if treated and control clusters show material divergent pre-trends.

Report:

- each pre-period event-time effect;
- a pre-period slope/imbalance diagnostic;
- missing panel cells;
- number of matched sets contributing at each event time.

Do not hide failed pre-trends by dropping inconvenient pre-years after inspecting results.

---

## Output-equivalent delay

For count outcomes, an interpretable descriptive quantity is:

Cumulative Missing Output = sum over post years of max(0, −E_k)

Normalize by the pre-shock annual treated output:

Output-Equivalent Delay Years = Cumulative Missing Output / Baseline Annual Output

This has units of 'topic-years of baseline output'.

It is **not** automatically the number of calendar years a discovery was delayed.

Use labels:

- article-output-equivalent delay years;
- entrant-output-equivalent delay years;
- funding-output-equivalent delay years.

Do not combine units.

---

## Scientific Detour Years

`Scientific Detour Years (SDY)` is reserved for an explicitly normalized field-vitality measure.

Preferred first implementation:

SDY_articles = cumulative article-arrival deficit / pre-shock annual article arrivals

Interpretation:

> the amount of baseline topic output missing after the shock, expressed in annual-output equivalents.

This is a field-level opportunity-cost metric. It must not be added to RLY because that would mix topic-output time with researcher labor time.

---

## Stronger Innovation Delay

A true 'discovery delayed by X years' claim requires a milestone model:

- define a legitimate discovery/concept/method milestone;
- estimate its counterfactual arrival time absent the integrity shock;
- compare observed vs counterfactual milestone timing.

That is a later confirmatory layer. The first event-study module estimates field vitality and output-equivalent delay, not exact discovery dates.

---

## Heterogeneity

Pre-specified heterogeneity:

- misconduct/severe reliability failure vs honest major error;
- high vs low source centrality;
- field;
- pre-shock topic size;
- retraction lag;
- correction visibility;
- source citation/semantic centrality.

Country/institution may be descriptive covariates but not a suspicion prior.

---

## No-go rules

- Do not call every post-retraction decline 'lost good science'.
- Do not infer causality without credible controls and pre-trend diagnostics.
- Do not use post-treatment variables for matching.
- Do not equate citation penalties with publication displacement.
- Do not convert article-output-equivalent years into Researcher-Life-Years.
- Do not infer one bad paper displaced one good paper.
- Do not count retracted-source papers themselves as missing legitimate output.
