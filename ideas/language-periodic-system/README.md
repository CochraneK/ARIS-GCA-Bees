# Active Candidate · Beyond the Periodic Table

**Status:** ARIS active candidate · predictive-geometry reframe  
**Paper ID:** not assigned  
**Current working title:** *Beyond the Periodic Table: Predictive Geometry of Cross-Linguistic Structural Space*  
**Historical hypothesis:** *Testing the Periodic-Table Hypothesis of Human Language*

## Core question

Does cross-linguistic structural diversity contain a genuinely periodic organization, or is it better described by non-periodic geometry such as hierarchy, low-rank structure, or graphs/manifolds?

The project treats “periodic table” as a falsifiable historical hypothesis rather than a desired visualization.

## What is already taken by prior work

- **Baker (2001)** explicitly proposed a “periodic table of languages” and grammatical parameters as language-building atoms.
- **Port et al. (2018)** and **Port, Karidi & Marcolli (2022)** already applied topology/persistent-homology ideas to syntactic-parameter spaces.
- **Grambank (2023)** already studies global morphosyntactic latent structure using PCA, feature bundles, and latent classes.
- **Graff et al. (2025)** provide dependency-curated GBI/TLI structural datasets.
- **Verkerk et al. (2025/2026)** test grammatical universals with genealogical and geographical controls.
- **SIGTYP / computational typology** already establish held-out typological feature prediction.
- **Circular-seriation research** formalizes circular Robinson matrices; a serious circular-order claim should be checked against that methodology rather than only a custom circle.

## Surviving novelty wedge

The candidate contribution is the **predictive model competition itself**:

> operationalize the historical periodic-table hypothesis and test whether a periodic geometry generalizes better than non-periodic alternatives on modern curated global data, including language-family and later geographic controls.

## Evidence trajectory

### Stage 0 · prerequisite signal

`MIXED_SIGNAL`

- 644 languages;
- 20-component compression = **0.510** vs shuffled-null **0.362**;
- residual dependencies show a substantial upper tail.

Conclusion: there is real organization worth modeling, but this is not periodicity evidence.

### Stage 1 · global model competition

`REFRAME_NONPERIODIC_GEOMETRY`

Family-held-out Spearman on 60 features:

| Model | Spearman |
|---|---:|
| tree | **0.178** |
| graph | 0.163 |
| low-rank | 0.150 |
| Euclidean | 0.150 |
| circular | **0.109** |

Circular-order stability was 0.542 ± 0.139: the circle captured reproducible structure, but not as well as the best non-periodic models.

### Stage 1B · fairer circle

`MIXED_ROBUSTNESS`

After fixing affinity connectivity and directly optimizing angular positions:

- 40 features: circular 0.179, tree 0.178, Euclidean 0.217;
- 60 features: circular 0.105, tree 0.147, low-rank 0.153.

The periodic hypothesis therefore cannot be dismissed as a trivial strawman, but it is not robustly best either.

### Stage 1C · predefined subsystem test

`NO_PREDEFINED_LOCAL_PERIODIC_CANDIDATE`

Using TLI's official feature groupings rather than cherry-picking subsets:

| Domain | Optimized circle | Best relevant non-periodic signal | Circle stability | Verdict |
|---|---:|---:|---:|---|
| Grammar linear order | 0.401 | tree 0.494 | 0.811 | non-periodic |
| Grammar other | 0.253 | tree 0.313 | 0.274 | non-periodic |
| Grammatical categories | 0.252 | tree 0.229 | 0.373 | ambiguous |
| Lexical | 0.142 | tree 0.269 | 0.057 | non-periodic |
| Phonology | 0.151 | tree 0.229 | 0.550 | non-periodic |

No predefined domain passed the predeclared combination of predictive competitiveness and order stability needed to call it a local periodic candidate.

## Current interpretation

The evidence currently favors:

> **Human language has reproducible structural geometry, but a simple global or predefined-local periodic system is not the best description found so far.**

The strongest next paper direction is therefore not to draw a periodic table. It is to ask which geometry best predicts linguistic design space and to use Baker's periodic-table proposal as the historical hypothesis being tested.

## Remaining decisive checks

- standards-aligned circular-seriation / circular-Robinson sensitivity;
- more repeated family-held-out uncertainty and capacity accounting;
- geography-aware validation;
- second-dataset / independent-subset replication;
- formal identity-bearing ARIS secondary review.

## ARIS artifacts

- `RESEARCH_BRIEF.md` — canonical research brief
- `idea-stage/IDEA_REPORT.md` — prior art, idea ranking, novelty analysis
- `PILOT_REPORT.md` / `pilot-results.json` — Stage 0
- `STAGE1_REPORT.md` / `stage1-results.json` — global competition
- `STAGE1B_REPORT.md` / `stage1b-results.json` — periodic fairness robustness
- `STAGE1C_REPORT.md` / `stage1c-results.json` — predefined domain screen
- `refine-logs/FINAL_PROPOSAL.md` — current paper framing
- `refine-logs/EXPERIMENT_PLAN.md` / `EXPERIMENT_TRACKER.md` — next experiments
- `ARIS_STATUS.md` — durable state and review gate

## Formal review boundary

ARIS v0.4.26 requires identity-bearing secondary-review evidence for reviewer-bearing phases. The current ChatGPT-side pass has not fabricated a reviewer receipt. Promotion to a numbered paper remains blocked on that formal gate plus the remaining confirmatory controls.

## Promotion criterion

Do **not** create `papers/002-*` yet. Promote only after the final periodic baseline, spatial/replication controls, and formal ARIS review support a stable manuscript framing.
