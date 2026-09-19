# ARIS4C010 · Preregistration Skeleton v0.1

**Status:** internal design draft — not registered  
**Date:** 2026-09-19

This file exists to prevent outcome-dependent rewriting once human-calibrated Benchmark v0 data are available.

## Primary research question

Relative to unrestricted information-theoretic partitions, what query cost is induced when identification questions must be semantically interpretable, target-type appropriate, context-resolved and answerable across heterogeneous concept regimes?

## Primary hypotheses

### H1 · multi-axis separation
At matched query-bank complexity, the UCID multi-axis representation will have higher held-out pairwise separation coverage and fewer unresolved collision classes than a single `is-a` taxonomy.

**Primary outcomes**
- pairwise separation coverage;
- number/size of collision classes.

### H2 · semantic query overhead
Semantically admissible questions will require more interaction cost than unrestricted optimal partitions.

[
\Delta_{sem}=E[L^*_{sem}]-E[L^*_{all}] > 0.
]

**Primary outcomes**
- expected questions;
- entropy-normalized efficiency;
- cost-sensitive expected path length.

The trivial mathematical non-negativity of the restriction is not the empirical claim. The empirical target is the magnitude and its semantic predictors.

### H3 · heterogeneous-regime penalty
Vague, context-dependent, compositional and semantic-stress targets will have higher semantic overhead and/or oracle disagreement than matched ordinary targets.

**Primary outcomes**
- query cost;
- invalid/type-error question rate;
- response entropy/disagreement;
- retest inconsistency.

### H4 · response-protocol mechanism

The response experiment separates two mechanisms:

- **H4a · coarse escape effect:** P3 (YES/NO/MAYBE) will reduce forced binary invalidity relative to P2.
- **H4b · semantic differentiation effect:** P6 will improve reliability, interpretability, or downstream identification relative to P3 by distinguishing BORDERLINE / UNKNOWN / UNDEFINED / BOTH rather than collapsing them into MAYBE.

P6+context is a later extension testing explicit context requests.

**Primary outcomes**
- invalid forced-answer rate;
- rate of MAYBE in P3 versus fine-grained non-binary states in P6;
- retest disagreement;
- category confusion / response entropy;
- total interaction time/cost;
- successful identification per cost.

No claim that "more response labels are automatically more informative in practice" is permitted. A P6 advantage over P2 is not sufficient by itself; the key mechanistic comparison is P6 versus P3.

### H5 · open-world calibration
Explicit OOS handling will reduce confidently wrong in-support identifications on withheld targets relative to forced closed-world guessing.

**Primary outcomes**
- OOS precision/recall;
- calibration;
- false in-support match rate;
- ontology-expansion success where enabled.

## Main representation conditions

1. single taxonomy;
2. lexical-semantic graph;
3. UCID typed multi-axis graph;
4. dense embedding baseline;
5. hybrid graph + embedding;
6. unrestricted partition lower/upper baseline where computationally feasible.

## Main query policies

1. random admissible;
2. fixed hierarchy;
3. greedy information gain;
4. cost-sensitive greedy information gain;
5. generalized-binary-search-style split;
6. planning/MCTS if computationally justified;
7. exact optimal tree on small subsets.

Policy optimization is a baseline comparison, not the novelty claim.

## Primary analysis set

Publication claims should use targets that are:
- provenance-complete;
- in a frozen release;
- human calibrated where semantic judgment is required;
- grouped to prevent synonym/base-concept leakage.

Constructed Pilot 1 seeds are excluded from confirmatory inference unless independently re-annotated and promoted.

## Statistical model skeleton

For target-level query cost:

[
cost_i \sim
\beta_0
+\beta_1 representation
+\beta_2 semantic\_stratum
+\beta_3 composition\_depth
+\beta_4 familiarity
+\beta_5 context\_dependence
+\beta_6 vagueness
+ u_{concept}
+ u_{query}
+ \epsilon.
]

Exact family/model will be selected before confirmatory data are inspected and adapted to outcome distribution.

## Multiplicity

Predefine:
- H1 and H2 as primary;
- H3–H5 as key secondary;
- all individual pathology subclasses as exploratory unless separately powered.

Report effect sizes and uncertainty rather than only thresholded p-values.

## Exclusion criteria

Before test-set analysis exclude/quarantine:
- source/license unresolved;
- duplicate/alias leakage;
- target identity not independently specifiable;
- query interpretation irreparably ambiguous;
- missing required context;
- adjudication failure;
- accidental direct-answer leakage.

## Negative-result interpretation

The project remains informative if:
- a simple lexical graph equals the multi-axis ontology;
- P6 adds cost without reliability benefit;
- pathology strata are too annotation-unstable;
- semantic overhead is small for most ordinary concepts;
- open-world recovery is poor.

These outcomes should narrow, not be hidden from, the manuscript.

## Freeze requirements before real preregistration

- [ ] Benchmark v0 source versions fixed
- [ ] Stage-A P2/P3/P6 human calibration completed
- [ ] power/precision plan
- [ ] exact primary statistical models
- [ ] response-time cost definition
- [ ] query-bank complexity matching procedure
- [ ] split hashes
- [ ] analysis code dry-run on synthetic data
