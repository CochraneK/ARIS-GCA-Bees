# AUTO REVIEW — ARIS4C003

## Review stage

Pre-data adversarial review. This review is intentionally written before full contemporary outcome inspection.

## Overall assessment

**Promising, but the publishable contribution depends on disciplined scope control and a credible preregistered mapping from historical mechanism to modern discipline-level outcomes.**

The project is stronger as a science-of-science/historical-sociology study of **disciplinary path dependence** than as a generic claim that "colonial countries have better rankings."

The design should proceed, but only after the confirmatory discipline-entanglement construct and primary exposure/outcome definitions are frozen.

---

## Major concern 1 — empire is confounded with prior state/scientific capacity

States that built large empires were not historically random. They often had naval capacity, fiscal institutions, universities, printing/publishing networks, industrialization, scientific societies, and high state capacity before or during imperial expansion.

### Why this matters

A cross-sectional regression such as:

`Anthropology strength ~ empire + GDP`

would not identify a colonial mechanism.

### Current mitigation

Use within-country cross-disciplinary specialization and country or country-year fixed effects. The key estimand becomes whether countries with stronger imperial histories are **disproportionately specialized in fields with stronger historical imperial entanglement**, not whether those countries are generally scientifically stronger.

### Remaining weakness

The entanglement of disciplines may itself correlate with other features such as field age, publication culture, or humanities/social-science orientation. Discipline-year fixed effects and carefully chosen comparison fields help but do not fully solve historical selection.

**Gate:** GO with strong wording discipline; causal claims must remain limited unless further quasi-experimental leverage is found.

---

## Major concern 2 — discipline selection can manufacture the result

If investigators choose Anthropology, Geography, Archaeology, Development Studies, and Tropical Medicine because these are obviously linked to empire and then compare them with Mathematics/Physics after seeing outcomes, the design has substantial researcher degrees of freedom.

### Required fix

- preregister confirmatory disciplines before full outcome inspection;
- create a transparent historical entanglement rubric;
- code that rubric blind to contemporary outcome values;
- use independent coders/evidence summaries;
- retain a separate exploratory all-field scan.

**Gate:** BLOCKING until the coding protocol is frozen.

---

## Major concern 3 — ranking products may reproduce prestige rather than capability

QS/THE/Shanghai measure different composites; some subject products include substantial reputation components and institutional eligibility filters. Treating rank as ground truth would conflate historical reputation with current knowledge production.

### Required fix

The primary outcomes must be bibliometric/network measures. Rankings become a separate prestige/institution layer.

A particularly interesting result would be divergence:

- historical exposure predicts QS/reputation but not bibliometrics → prestige persistence;
- predicts bibliometrics too → broader capability/institutional persistence;
- predicts dyadic collaboration most strongly → network persistence.

**Gate:** GO; current plan already separates outcomes.

---

## Major concern 4 — English-language and database coverage bias

OpenAlex and citation-based systems have broader coverage than older databases but are still not culturally neutral. Leiden Open Edition core-publication indicators explicitly impose English/core-journal restrictions for some normalized metrics, while its broader core+non-core set differs in eligibility.

### Required fix

- report country/field/language coverage;
- run non-core/broader-coverage sensitivity where possible;
- compare Anglophone and non-Anglophone subsets;
- avoid interpreting absent indexed output as absent scholarship;
- consider national/regional publication systems in limitations.

**Gate:** GO with mandatory sensitivity analyses.

---

## Major concern 5 — colonial exposure is not one construct

"Colonial history" mixes:

- metropole/ruler status;
- duration and scale of rule;
- settlement vs extractive rule;
- land vs overseas empire;
- multiple successive rulers;
- postwar mandates/trusteeships;
- informal empire;
- independence timing;
- language/institutional inheritance.

### Required fix

Do not create an arbitrary one-number empire index too early. Define a small primary exposure plus secondary variants. Separate imperial-center and former-colony models.

The project should state explicitly whether continental empires (Russian, Ottoman, Qing/Chinese, etc.) are inside the main estimand or a separate robustness family; modern colonial datasets often encode these differently.

**Gate:** PARTIAL BLOCK until scope of "empire" is specified.

---

## Major concern 6 — RCA is useful but not literal causal comparative advantage

Scientific RCA is a relative specialization measure. It can be unstable for small countries, mechanically depends on denominator composition, and should not be interpreted as an economic structural parameter.

### Required fix

- minimum publication thresholds;
- symmetric/log transformations;
- alternative specialization index;
- fractional counting;
- small-state sensitivity;
- report absolute output alongside relative specialization.

**Gate:** GO.

---

## Major concern 7 — the strongest fixed-effect model may absorb too much or change the estimand

Country-year fixed effects are attractive because they absorb contemporary national capacity. But the historical exposure is time-invariant and only identified through discipline interactions. If the entanglement score is also time-invariant, the interaction is identified from cross-disciplinary differences, not from historical temporal variation.

This is valid for an associational path-dependence test, but it is not a conventional panel treatment design.

### Required fix

State the estimand correctly:

> whether national historical exposure covaries with the *shape* of contemporary disciplinary specialization in the theoretically predicted direction.

Avoid presenting the FE panel as if it made empire exogenous.

**Gate:** GO with careful interpretation.

---

## Major concern 8 — former colonies are likely too heterogeneous for one coefficient

Colonial educational systems, institutional investments, languages, extractive structures, settlement patterns, and independence paths vary dramatically.

### Required fix

For formerly colonized states, a single pooled coefficient should be descriptive at most. Prioritize hierarchical/stratified analyses and dyadic former-colonizer ties. Do not state a universal "colonization improves/harms discipline X" hypothesis.

**Gate:** GO; current theory already treats sign as ambiguous.

---

## Major concern 9 — post-treatment controls can erase the mechanism

Modern GDP, R&D, university stock, English use, and international collaboration may be channels through which historical institutions persist.

### Required fix

Define three estimands:

1. total long-run historical association;
2. association net of contemporary capacity;
3. mediated/network/prestige pathway.

A DAG review must classify candidate controls rather than throwing all of them into one regression.

**Gate:** BLOCKING before final models.

---

## Major concern 10 — novelty may be narrower than it first appears

There is substantial literature on colonial science, decolonizing disciplines, colonial knowledge institutions, global scientific inequality, specialization, and former-colonial collaboration. There are also empirical studies linking colonial history to present knowledge-production geography in specific fields such as palaeontology.

### What appears potentially distinctive

The strongest novelty target is the **cross-disciplinary interaction/gradient**:

> historical imperial exposure × independently coded discipline entanglement → contemporary relative disciplinary specialization, impact, network structure, and prestige.

The novelty claim must be phrased at this level only after a targeted closest-prior-work search.

**Gate:** GO TO NOVELTY REVIEW; no broad novelty claim yet.

---

## Statistical concerns

- Clustered dependence across country×field cells must be handled explicitly.
- Rank outcomes are ordinal/censored and should not be used in naive OLS on rank numbers.
- Top-paper proportions require adequate denominators.
- Network centrality metrics are endogenous to network size; normalized dyadic collaboration is more interpretable as a primary network outcome.
- Missingness in historical exposure and bibliometric data can be geographically structured.
- Field taxonomies can create artificial discontinuities; crosswalk uncertainty must be documented.
- Multiple alternative empire definitions can become a hidden specification search; one primary definition should be frozen.

---

## Recommended minimal confirmatory core

A bounded first paper is preferable to an everything-at-once mega-project.

### Primary exposure
One transparent imperial-center historical exposure measure, plus a separately defined former-colony exposure.

### Primary discipline construct
Pre-outcome historical entanglement score for ~15–25 fields.

### Primary outcomes
1. fractional-output specialization;
2. field-normalized impact/top-10% specialization;
3. normalized international collaboration.

### Primary model
Country-year FE + discipline-year FE interaction model where feasible.

### Secondary analyses
- former-colony heterogeneity;
- dyadic colonial-tie collaboration model;
- rankings/prestige residual;
- full all-field exploratory scan.

This ordering protects the paper from becoming a collection of loosely related significant results.

---

## Decision

**ARIS gate: CONDITIONAL GO.**

Proceed to literature/construct/preregistration stages. Do **not** open the full outcome scan until the following are frozen:

- historical exposure definition;
- inclusion/exclusion of continental empires;
- discipline-entanglement coding protocol;
- confirmatory discipline set;
- primary outcomes and thresholds;
- DAG/control strategy;
- primary statistical specification.
