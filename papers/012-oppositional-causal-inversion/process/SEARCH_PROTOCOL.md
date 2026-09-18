# SEARCH PROTOCOL — ARIS4C012

Updated: 2026-09-18
State: Pilot 0 protocol frozen before full evidence-map screening

## 1. Purpose

The search is designed to test, not illustrate, the proposed Oppositional Causal Inversion (OCI) framework.

The primary retrieval strategy therefore does **not** search only for Orwell's three slogans and does not preferentially select famous paradoxes. It searches broad families of opposite-direction, backfire, feedback, overload, and cross-level effects and then asks whether the OCI coding scheme applies.

## 2. Core review question

> Across scientific domains, how often do empirically or formally supported causal claims show that increasing a construct produces a prespecified functional opposite after an explicit change in actor, level, time, construct, environment, feedback state, or capacity regime?

## 3. Source hierarchy

Primary discovery:
- OpenAlex;
- Crossref;
- PubMed for biomedical/psychological families;
- publisher and journal searches for exact known traditions.

Validation/extension when legitimately accessible:
- Web of Science;
- Scopus;
- domain bibliographies and backward/forward citation chasing.

Every included record should preserve DOI or other stable identifier when available.

## 4. Search families

Search families are intentionally broader than OCI terminology.

### A. General reversal language
- paradox*
- backfire
- boomerang
- counterproductive
- self-defeating
- perverse consequence
- unintended consequence
- reversal
- opposite effect
- iatrogenic
- counterfinal*

### B. Capacity and information
- less-is-more
- information overload
- choice overload
- rational inattention
- deliberate ignorance
- information avoidance
- bounded rationality
- overfitting
- signal-to-noise

### C. Strategic / equilibrium feedback
- security dilemma
- deterrence paradox
- risk compensation
- rebound effect
- Jevons paradox
- Braess paradox
- moral hazard
- Goodhart law
- Campbell law

### D. Autonomy / control
- autonomy paradox
- flexibility paradox
- control paradox
- choice autonomy
- algorithmic dependence
- delegation dependence

### E. Cross-group / cross-level conflict
- intergroup competition intragroup cooperation
- external threat internal cohesion
- rally around the flag
- diversionary conflict
- common enemy cooperation

## 5. Causal-evidence modifiers

Where database syntax permits, combine discovery families with at least one of:

- experiment*
- randomized
- longitudinal
- quasi-experiment*
- natural experiment*
- instrumental variable
- difference-in-differences
- regression discontinuity
- meta-analysis
- systematic review
- causal model
- equilibrium model

A paper is not excluded merely because these words are absent; this block is for high-specificity supplementary retrieval.

## 6. Screening stages

### Stage 1 — title/abstract relevance
Include if the abstract plausibly contains:
1. an identifiable exposure/intervention/state X;
2. an outcome that could be opposite to X or opposite to X's intended function;
3. a mechanism, moderator, or design capable of supporting a causal interpretation.

### Stage 2 — opposition validity
Before coding the observed direction, define the claimed opposite.

Admissible opposition must be supported by:
- an established bipolar construct;
- a formal complement;
- domain theory identifying incompatible functional states; or
- independent coder agreement with written rationale.

Lexical antonymy alone is insufficient.

### Stage 3 — indexed causal representation
Attempt to encode:

`do(X_i ↑) -> M/feedback -> O(X)_j ↑`

or

`do(X_i ↑) -> X_j ↓`

with actor, level, time, construct and environment indices recorded explicitly.

### Stage 4 — evidence classification
Code evidence tier E0-E5 using `CONCEPT_SCHEMA.md`.

## 7. Exclusion rules

Exclude from OCI-positive coding:
- literary/rhetorical paradox without empirical or formal causal mechanism;
- ordinary harmful side effects unrelated to the focal construct/function;
- reverse causality described as "causal inversion";
- post-hoc antonyms invented after outcome inspection;
- correlational sign changes with no plausible causal identification;
- measurement artifacts, mathematical coupling, or regression-to-the-mean presented as substantive reversal;
- same-index simultaneous `X = not-X` claims with no dynamic/nonlinear interpretation.

Excluded papers may remain in the corpus as negative examples for classifier development.

## 8. Pilot 0 sampling

Pilot 0 target: **30 records**.

To reduce cherry-picking:
1. use six prespecified search strata;
2. take five eligible records per stratum after deduplication;
3. within each stratum prioritize search rank/relevance before knowledge of whether OCI coding succeeds;
4. include both supportive and null/counterexample records;
5. do not replace a difficult-to-code paper merely to improve agreement.

Planned strata:
1. conflict/security;
2. autonomy/choice;
3. information/attention;
4. intervention backfire/iatrogenic;
5. economic/network rebound;
6. organizational/measurement paradox.

The existing seed file is **not** automatically the Pilot 0 sample; it is a prior-art seed.

## 9. Independent coding

Each Pilot 0 record receives at least two independent coding passes for:

- opposition validity;
- actor switch;
- level switch;
- time switch;
- construct switch;
- environment/regime switch;
- feedback/nonlinearity;
- primary mechanism family;
- evidence tier;
- causal-claim strength.

Coders should not see the other coder's labels before submission.

## 10. Reliability gate

Report raw agreement plus chance-corrected agreement (Cohen's kappa for suitable categorical fields; Krippendorff's alpha where missing/multicategory coding makes it preferable), with uncertainty where feasible.

Precommitted gate:
- if opposition-validity or primary-mechanism agreement is below 0.70, revise the construct definitions and repeat Pilot 0 on a fresh sample before full screening;
- >=0.80 is the preferred operational target for those key fields.

These are workflow thresholds, not claims about universal psychometric standards.

## 11. Primary evidence-map outputs

Do **not** estimate one grand OCI effect.

Primary outputs:
- proportion of screened candidate papers that survive opposition validation;
- distribution of index-switch types;
- distribution of mechanism families;
- evidence-tier distribution;
- domain x mechanism matrix;
- fraction that collapse into rhetoric/ordinary side effect after index restoration;
- counterevidence frequency;
- moderator/threshold frequency;
- cross-domain portability of the taxonomy.

## 12. Novelty test

After full closest-prior-work review, OCI may be presented as a new framework only if:

1. no existing umbrella theory already supplies the same indexed causal representation;
2. the coding scheme is reliable;
3. the framework organizes cases across multiple domains;
4. it distinguishes genuine reversals from negative examples better than domain labels or generic "paradox" terminology;
5. at least one out-of-domain validation demonstrates predictive/classification value.

Otherwise the project is reframed as a systematic taxonomy/evidence map without claiming a new general theory.
