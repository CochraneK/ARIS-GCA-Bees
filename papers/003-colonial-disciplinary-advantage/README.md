# ARIS4C003 · Colonial Legacies and the Global Geography of Disciplinary Advantage

**Status:** design locked / outcome locked · executable pipeline ready

**ARIS provenance:** v0.4.26 · `951654847b015585385b2448c5667dcd04e7b56b`

## Canonical research question

> Do colonial and imperial histories predict persistent, discipline-specific advantages or specializations in contemporary science and scholarship, and if so are those legacies expressed through research capacity, citation impact, institutional prestige, or persistent international knowledge networks?

## Core idea

The study does **not** reduce the question to Sociology + Anthropology or to a single university ranking. Anthropology and Sociology are anchor cases inside a cross-disciplinary, multi-outcome design.

The theoretical object is **historical knowledge capital**: durable stocks of institutions, expertise, collections, archives, field sites, language systems, professional societies, journals, training pipelines, and prestige that may have accumulated through imperial/colonial systems and persisted after formal empire ended.

This is a hypothesis to test, not a claim that colonialism "improved" science.

## Frozen design decisions

1. Separate **imperial/colonizer exposure** from **colonized/dependency exposure**; never collapse them into one dummy.
2. Keep COLDAT-style European overseas-colonial duration measures conceptually separate from broader ICOW-style dependency histories.
3. Treat the imperial-center analysis as **small-N**: repeated discipline observations do not turn a handful of empire states into a large independent treatment sample.
4. Make former-colony/dependency and dyadic former-colonial analyses the main scalable inferential layers.
5. Use a **country × discipline × year × outcome** structure for specialization and a **country-pair × discipline × year** structure for network persistence.
6. Estimate **relative disciplinary advantage/specialization**, not merely raw national research strength.
7. Use multiple outcome families: scientific output, field-normalized impact, elite-paper share, collaboration/network structure, and prestige/ranking.
8. Keep ranking products secondary; they must not be the sole measure of "strength."
9. Separate a preregistered confirmatory discipline set from an exploratory all-discipline scan.
10. Treat effects among formerly colonized states as heterogeneous and not signed universally positive or negative.
11. Scientist migration/war shocks (for example German scientists moving to the United States) are a related **historical knowledge capital** mechanism but are outside the primary colonial exposure definition for 003.
12. No paid LLM API is required: API-gated ARIS reviewer/research stages use the GPTPage handoff in `process/GPTPAGE_HANDOFF.md`.

## Inferential hierarchy

### Tier 1A · Former-colony disciplinary profile

Main question:

> Does historical colonial/dependency exposure predict the modern *shape* of disciplinary specialization as a function of independently coded imperial/colonial knowledge entanglement?

The primary test is a cross-disciplinary gradient, not isolated significance in one or two fields.

### Tier 1B · Dyadic network persistence

Main question:

> Are former colonizer–colony pairs disproportionately connected in modern scientific collaboration, especially in more historically entangled disciplines, after geographic/scientific-size controls?

Common language is treated both as a possible persistence channel and as a robustness adjustment, not automatically as a nuisance variable.

### Tier 2 · Imperial-center disciplinary profile

Theory-critical but small-N.

Historical imperial centers are compared across disciplines using effect sizes, profile similarity, leave-one-empire-out analysis, and exact/permutation-style inference where appropriate. Do not rely on naive large-N panel asymptotics.

### Tier 3 · Prestige persistence

Test whether ranking/reputation outcomes remain unusually high relative to contemporary bibliometric performance in historically entangled disciplines.

## Confirmatory conceptual disciplines

The conceptual set and primary OpenAlex crosswalk are frozen before outcome inspection:

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

These fields will receive an outcome-blinded **Imperial/Colonial Knowledge Entanglement Score (IKES)** using the protocol in `process/ENTANGLEMENT_PROTOCOL.md`.

## Outcome families

### Knowledge production
- fractional publication count
- national share of world output
- relative specialization / scientific RCA and alternative transforms

### Scientific impact
- field/year-normalized citation impact
- top-10% and top-1% paper share
- citation-based specialization

### Knowledge networks
- international collaboration share
- normalized dyadic coauthorship intensity
- selected network measures when stable

### Institutional / prestige layer
- QS subject indicators where legally/publicly obtainable
- THE subject rankings
- Shanghai GRAS
- Leiden Open Edition as independent/open bibliometric robustness

Rankings are explicitly not interchangeable with bibliometric performance.

## Main model logic

For scalable former-colony analyses, the target is a cross-disciplinary interaction such as:

`Y(c,d,t) ~ HistoricalExposure(c) × IKES(d) + country-year FE + discipline-year FE + error`

This asks whether historical exposure is associated with the **shape** of a country's contemporary research portfolio. It does not make historical exposure exogenous and should be interpreted as evidence of persistent path dependence, not automatic causal proof.

A complementary dyadic model tests:

`Collaboration(i,j,d,t) ~ FormerColonialTie(i,j) × IKES(d) + gravity/network controls + FE`

## Falsification logic

The broad theory weakens if:

- effects are similar across nearly all disciplines;
- the IKES gradient fails;
- results are driven only by Anglophone/database coverage;
- results vanish under fractional counting or reasonable specialization measures;
- one empire/region drives the pattern;
- field-taxonomy changes reverse the result;
- only reputation-heavy rankings show an association.

The last outcome would not make the project empty; it would narrow the conclusion to **prestige persistence** rather than scientific-capacity persistence.

## ARIS progress

Completed and stored under `process/`:

- canonical idea report;
- executable research plan;
- first adversarial auto-review;
- verified literature seed;
- GPTPage fallback workflow;
- first GPTPage novelty review;
- causal/DAG review;
- discipline-entanglement coding protocol;
- colonial/imperial exposure protocol with small-N correction.

## Remaining pre-outcome gate

Most design and engineering gates are now closed. Contemporary confirmatory
country×discipline outcomes remain intentionally unopened.

Completed:

- [x] closest-prior-work review narrowed the defensible novelty claim;
- [x] 21-discipline conceptual set and OpenAlex crosswalk frozen;
- [x] bibliometric windows, counting rules, zero-cell policy, PPML estimator,
      clustering, permutation, leave-one-field-out, and volume sensitivities frozen;
- [x] preregistration draft plus dated implementation/estimator amendments;
- [x] Coder A historical-entanglement pass;
- [x] COLDAT historical exposure build and 159/159 country crosswalk audit;
- [x] OpenAlex public-Parquet nested schema probe;
- [x] local/public-S3 OpenAlex materialization code and synthetic model CI;
- [x] CEPII Gravity V202211 extraction/audit code; compact dyad artifact is
      generated by the dedicated historical workflow.

Still integrity-gated:

- [ ] independent blinded Coder B in a genuinely fresh GPTPage/model context;
- [ ] outcome-blind A/B adjudication and `IKES_FROZEN.csv`;
- [ ] final CEPII compact dyad artifact/manifest present in the canonical branch.

Only after these pass may `preoutcome_gate.py --strict` return
`OUTCOME_UNLOCKED` and allow contemporary OpenAlex outcome materialization.


## Current execution gate

The project now enforces a machine-readable pre-outcome lock.

**Completed before contemporary confirmatory outcomes:**

- 21 conceptual disciplines frozen as D01–D21;
- OpenAlex primary-topic crosswalk frozen;
- Coder A IKES pass complete and machine-readable;
- independent Coder B packet frozen for a fresh GPTPage/model context;
- country attribution, multilateral dyad weighting, work types, time windows, and zero-cell rules frozen;
- COLDAT / CEPII / OpenAlex acquisition and transformation scripts implemented;
- PPML model family frozen in `process/MODEL_SPEC_LOCK.json`;
- `code/run_confirmatory_models.py` implements the three headline 2019–2022 tests plus persistence, 999 IKES-label permutations, leave-one-discipline-out, volume, and median-IKES sensitivities;
- outcome-blind PyFixest model-engine smoke tests pass in GitHub Actions;
- imperial-center evidence is explicitly small-N and has its own frozen corroboration protocol.

**Still required before `OUTCOME_UNLOCKED`:**

1. independent blinded Coder B in a fresh context;
2. outcome-blind adjudication and `IKES_FROZEN.csv`;
3. CEPII compact historical dyads and checksum manifest committed;
4. OpenAlex public-S3/local source remains schema-compatible (already probed PASS).

Run `python code/preoutcome_gate.py --require-design-locked` to assert the design gate.
Run `python code/preoutcome_gate.py --strict` only when attempting to unlock contemporary confirmatory outcomes.

The intended state before those external/local gates close is **DESIGN_LOCKED / OUTCOME_LOCKED**. This is an integrity feature, not an unfinished hypothesis.
