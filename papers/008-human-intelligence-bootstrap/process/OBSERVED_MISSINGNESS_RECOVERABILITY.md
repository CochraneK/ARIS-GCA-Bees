# Observed-missingness recoverability · ARIS4C008 Pilot 7

## Input

The simulation now uses the actual **29 taxa × 10 module** measurement/evidence mask from `module_evidence_state_v2.csv`.

Observed module coverage is:

- A 4/29
- B 11/29
- C 8/29
- D 7/29
- E 7/29
- F 9/29
- G 24/29
- H 18/29
- I 26/29
- J 19/29

Overall observed-cell coverage is about **45.9%**.

## Current-panel diagnostic

Across 500 simulated datasets using the fixed observed mask:

- additive recovery: **0.660**
- weakest-link recovery: **0.346**
- threshold recovery: **0.162**

The current matrix is therefore **not adequate** for confirmatory architecture selection.

## Missingness is not the only problem

With all ten modules hypothetically complete for 29 randomly configured taxa, recovery remains:

- additive: **0.750**
- weakest-link: **0.430**
- threshold: **0.255**

So merely filling the present 29 × 10 table is insufficient.

## Configuration-aware sampling matters

An upper-bound “model-discriminating” selection procedure chooses taxa whose latent configurations maximally separate mean, minimum and threshold signatures.

At 29 complete taxa:

- additive: **0.795**
- weakest-link: **0.645**
- threshold: **0.665**

At 80 complete taxa:

- additive: **0.835**
- weakest-link: **0.535**
- threshold: **0.680**

By contrast, 80 randomly configured complete taxa recover threshold only **0.335** in this diagnostic.

## Interpretation

The exact percentages are not biological power estimates. The models are deliberately simplified and the model-discriminating selection is an oracle upper bound.

The robust design lesson is:

> **The study needs both targeted gap filling and configuration-diverse taxon selection. More taxa alone do not solve identifiability.**

This also explains why a “smartest animals” sample is dangerous: taxa clustered in the same high-cognition corner do not provide the counterexamples needed to distinguish additive from bottleneck/threshold systems.

## Gate decision

The `model_recoverability` gate should now be marked **blocked for confirmatory modeling**.

To unblock:
1. substantially increase A/C/D/E/F exact-species coverage;
2. add deliberately ordinary and dissociative taxa, not only famous cognitive specialists;
3. use provisional low-cost traits to approximate model-discriminating sampling;
4. re-run recoverability using the resulting empirical distributions and missingness;
5. supplement winner-take-all model selection with direct necessary-condition/counterexample tests rather than relying on one global architecture winner.
