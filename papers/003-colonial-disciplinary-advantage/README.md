# ARIS4C003 · Colonial Legacies and the Global Geography of Disciplinary Advantage

**Status:** research design / ARIS entry

**ARIS provenance:** v0.4.26 · `951654847b015585385b2448c5667dcd04e7b56b`

## Canonical research question

> Do colonial and imperial histories predict persistent, discipline-specific advantages in contemporary science and scholarship, and if so are those legacies expressed through research capacity, citation impact, institutional prestige, or persistent international knowledge networks?

## Why this is not a two-discipline ranking paper

The study does **not** reduce the question to Sociology + Anthropology or to a single university ranking. Anthropology and Sociology are theory-motivated anchor cases, but the main design is cross-disciplinary and multi-outcome.

The key theoretical object is **historical knowledge capital**: durable stocks of institutions, expertise, collections, administrative knowledge, language networks, field sites, learned societies, journals, university chairs, and prestige that may have accumulated through imperial/colonial systems and persisted after formal empire ended.

## Frozen design decisions before ARIS

1. Separate **imperial/colonizer exposure** from **colonized/dependency exposure**; do not collapse them into one dummy.
2. Treat colonial exposure intensity, duration, ruler identity, and dyadic former-colonial ties as distinct variables where data permit.
3. Use a **country × discipline × year × outcome** framework rather than a single cross-sectional ranking.
4. Estimate **relative disciplinary advantage/specialization**, not merely raw national research strength.
5. Use multiple outcome families: scientific output, field-normalized impact, elite-paper share, collaboration/network structure, and prestige/ranking.
6. Keep ranking products secondary/robustness evidence; they must not be the sole outcome.
7. Separate a preregistered confirmatory discipline set from an exploratory all-discipline scan.
8. Treat the direction of effects for formerly colonized states as theoretically ambiguous and heterogeneous rather than automatically positive.
9. Explicitly test whether any apparent effect is merely GDP, population, language, university age, general science capacity, region, or English-language database coverage.
10. No paid LLM API is required for this project. API-gated ARIS reviewer/research steps use the GPTPage handoff in `process/GPTPAGE_HANDOFF.md`.

## Primary theoretical predictions

- **H1 Imperial specialization:** stronger historical imperial exposure predicts greater contemporary relative advantage in disciplines historically entangled with imperial knowledge production.
- **H2 Gradient:** the imperial-exposure association increases with a preregistered measure of colonial/imperial knowledge entanglement across disciplines.
- **H3 Specificity:** the association is weaker or absent in comparison disciplines whose modern formation was less directly tied to colonial administration, territorial knowledge, extraction, or overseas field systems.
- **H4 Colonized heterogeneity:** former-colonial exposure has heterogeneous effects that depend on ruler, duration, educational/institutional investment, independence period, language, and postcolonial development.
- **H5 Network persistence:** former colonizer–colony dyads retain excess coauthorship/knowledge-network ties after standard geographic, linguistic, economic, and scientific-size controls.
- **H6 Prestige persistence:** historical imperial exposure predicts a larger prestige signal than would be expected from contemporary bibliometric performance alone.

## Candidate confirmatory discipline families

The exact set must be frozen before outcome inspection.

**High prior entanglement candidates:** Anthropology; Archaeology; Geography; Development Studies; Linguistics; Tropical Medicine / selected Public Health fields; Agriculture & Forestry; Geology / Earth-resource sciences.

**Medium candidates:** Sociology; Political Science / International Relations; Law; Economics; Public Administration / Social Policy; Education; History; Demography / Population Studies.

**Comparison candidates:** Mathematics; Physics; Chemistry; Computer Science; selected modern engineering/materials fields.

The project should prefer a **continuous, independently coded entanglement score** over a hand-picked high/low binary whenever feasible.

## Outcome families

### 1. Knowledge production
- fractional publication count
- national share of world output
- revealed scientific comparative advantage / relative specialization

### 2. Scientific impact
- field/year-normalized citation impact
- top-10% and top-1% paper share
- citation-based comparative advantage

### 3. Knowledge networks
- international coauthorship share
- dyadic former-colonial tie excess
- network centrality / brokerage where feasible

### 4. Institutional/prestige layer
- QS subject indicators where legally/publicly obtainable
- THE subject indicators
- Shanghai GRAS
- Leiden Open Edition as independent bibliometric robustness

Rankings are not interchangeable with research performance and should be modeled separately.

## Main empirical idea

A core specification is an interaction design in which country fixed effects absorb time-invariant national capacity and the quantity of interest is whether historically imperial countries show unusually high specialization in historically empire-entangled disciplines:

`Outcome(c,d,t) ~ ImperialExposure(c) × Entanglement(d) + country FE + discipline FE + year FE + controls/interactions`

Because time-invariant `ImperialExposure(c)` is absorbed by country fixed effects, inference focuses on its interaction with discipline-level entanglement.

A complementary dyadic design tests whether former colonial links predict present-day collaboration above and beyond distance, language, scientific size, GDP, and regional ties.

## Non-negotiable falsification logic

The preferred theory weakens substantially if:

- effects are similar across nearly all disciplines;
- effects disappear after accounting for general research specialization/capacity;
- only reputation-heavy rankings show an association and bibliometric/network outcomes do not (this would support a narrower prestige-persistence story instead);
- results are driven only by Anglophone database coverage;
- effects vanish under fractional counting, alternative field taxonomies, or leave-one-empire-out tests;
- the apparent gradient is created by selecting disciplines after seeing outcomes.

## Current next gate

ARIS should now shrink and stress-test the design before data collection:

1. novelty review;
2. causal/DAG review;
3. construct and measurement review;
4. freeze confirmatory discipline set and entanglement coding procedure;
5. freeze primary outcomes and transformations;
6. build a source/licensing-aware data acquisition plan;
7. draft a preregistration-style analysis specification;
8. only then begin large-scale data acquisition and modeling.
