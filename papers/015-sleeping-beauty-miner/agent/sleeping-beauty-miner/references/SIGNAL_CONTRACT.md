# ARIS4C015 Semantic and Network Signal Contract

## Purpose

Citation trajectories capture attention dynamics, but a prospective Sleeping Beauty miner needs independent evidence families if it is to do more than rediscover citation momentum.

This contract defines how semantic novelty, atypical combinations, reference diversity, graph structure, and Prince-related signals enter ARIS4C015 without being overinterpreted.

## Core rule

**No semantic or network score is scientific value by itself.**

Every signal must state:

- exact definition;
- unit of analysis;
- historical cutoff;
- corpus used to construct the feature;
- normalization;
- missingness / coverage;
- whether the feature is a transparent proxy or a published metric;
- whether it is used for ranking, explanation, sensitivity analysis, or audit.

## S1 — Transparent combination novelty proxy

Bundled implementation:
`code/evidence_features.py::pair_novelty_features`

Definition:

Among the unordered category pairs attached to a target paper, compute the share that have zero occurrences in a supplied pre-cutoff corpus.

This is useful because it is:

- simple;
- auditable;
- cutoff-safe when the prior table is cutoff-safe;
- easy to ablate.

It is **not** the Uzzi et al. atypical-combination z-score and must not be labeled as such.

Failure modes:

- ontology granularity changes the score;
- rare/poorly indexed labels can look artificially novel;
- field differences alter the opportunity set;
- missing references or labels inflate uncertainty;
- novelty may proxy interdisciplinarity rather than discovery potential.

## S2 — Published novelty / atypicality metrics

Published metrics may be implemented later as separate named signals.

Examples include:

- atypical combinations of journal/reference categories;
- novelty measures based on new combinations;
- embedding-distance novelty.

Each implementation must preserve its original formula and null model rather than being approximated and given the same name.

Do not replace a published metric with the transparent proxy and then compare results as if they were identical.

## S3 — Semantic embeddings

Embedding-based novelty is exploratory until historical leakage is addressed.

A present-day embedding model can be used for:

- semantic retrieval;
- explanatory clustering;
- exploratory discovery.

For confirmatory historical backtests, document why the representation does not leak future corpus/network outcomes, or reconstruct the representation using an appropriate historical state.

At minimum perform sensitivity analysis against transparent lexical/category proxies.

## N1 — Reference-field diversity

Bundled implementation:

- Shannon entropy;
- normalized entropy;
- Hill-number effective categories;
- cross-field reference share.

Interpretation:

These describe breadth of the paper's reference context, not quality and not interdisciplinarity in every substantive sense.

Required controls:

- field;
- publication year;
- reference count;
- indexing coverage.

## N2 — Citing-community diversity

Bundled implementation:
`citing_community_features`

Input community labels must come from a graph available at or before the cutoff.

Do not:

1. cluster the full 2026 citation graph;
2. assign those future-informed communities to a 1990 cutoff;
3. present the result as historically available.

If historical community reconstruction is unavailable, return ABSTAIN for confirmatory backtests.

## N3 — Bridge / brokerage features

Candidate graph features may include:

- betweenness-like brokerage;
- participation across communities;
- cross-community citation share;
- bibliographic-coupling bridge position.

These should be computed on cutoff-safe graphs and compared with cheaper diversity baselines.

High centrality is not automatically desirable. A Sleeping Beauty can be peripheral before awakening.

## P1 — Prince evidence

A Prince candidate is a paper/event associated with later awakening.

Candidate evidence may include:

- temporal position near the awakening;
- direct citation to the Sleeping Beauty;
- later co-citation growth;
- semantic relation;
- diffusion into a new community.

A Prince score is descriptive. It does not establish causal awakening.

Multiple Princes and gradual awakening must remain valid outputs.

## Track M temporal phases

Mechanism analysis must label evidence by when it exists relative to the
Sleeping Beauty trajectory.

### M0 — Publication-state evidence

Available at or immediately after publication:

- reference combinations;
- author/network position;
- journal/source/indexing context;
- contemporaneous semantic distance;
- document type and reference count.

Use to study initial visibility and field readiness.

### M1 — Sleep-period evidence

Observed after publication but before the case-specific awakening boundary:

- cumulative citation rate during the sleep window;
- changes in semantic-neighborhood size;
- emergence of related methods/technologies;
- changes in bibliographic-coupling neighborhood;
- weak diffusion into adjacent communities.

Use to study persistence of neglect and latent field development.

### M2 — Awakening-window evidence

Observed near the identified awakening:

- candidate Prince papers;
- sudden co-citation growth;
- new citing communities;
- technology/patent/application events;
- review/guideline events where timestamped.

Use to study awakening triggers.

### M3 — Post-awakening evidence

Observed only after awakening.

This may describe consequences of awakening but must not be used to explain
why the paper was initially neglected. It is forbidden as a prospective
feature before the corresponding historical cutoff.

### Anti-time-reversal rule

A later event cannot be used as evidence for the cause of initial neglect
without an explicit longitudinal/causal design.

For example:

- a 2005 Prince paper may help explain a 2005 awakening;
- it cannot be used as a feature claiming why a 1958 paper was overlooked at
  publication.

Track M may use later evidence to study awakening mechanisms. Track B may use
only evidence available by its historical cutoff.

## Feature-family separation

For ablation, keep at least these families distinct:

1. citation trajectory;
2. semantic / concept-combination novelty;
3. reference diversity;
4. citation-network structure;
5. citing-community diversity;
6. technology / patent linkage;
7. reuse (method/data/software);
8. integrity/provenance routing from 011.

Do not train one opaque "novelty" embedding containing all of them and then claim independent contribution.

## Normalization

Before cross-field modeling, candidate normalizations include:

- publication-cohort percentile;
- field × cohort z-score / robust z-score;
- matched controls;
- empirical CDF.

Any normalization choice is part of the model specification and must be frozen before evaluating the final test cohort.

## Missingness

Missing semantic/network evidence is not zero.

Represent as:

- applicable + value;
- ABSTAIN / insufficient coverage;
- BLOCKED if historical reconstruction is impossible.

Coverage itself may correlate with language, geography, age, journal, and open-access status. Audit those channels separately.

## Evidence Card language

Recommended:

- "high reference-field diversity at the 1995 cutoff";
- "two of three concept pairs were unseen in the pre-cutoff corpus";
- "citing-community diversity unavailable";
- "semantic novelty proxy is supportive but source-sensitive."

Avoid:

- "this is a revolutionary idea";
- "novelty proves future impact";
- "cross-disciplinary means better science".
