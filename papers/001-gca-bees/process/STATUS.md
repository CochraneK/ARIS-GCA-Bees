# STATUS · ARIS4C001

**Canonical status:** research-design  
**Reconstructed:** 2026-09-18  
**ARIS:** v0.4.26 @ 951654847b015585385b2448c5667dcd04e7b56b  
**Replacement policy:** legacy Paper 001 removed from current main; Git history is the only archive.

## What is established

- Honey bees can alter opt-out behavior with task difficulty; the 2013 study explicitly discusses both uncertainty-monitoring and associative explanations.
- Honey-bee learning performance shows nonzero individual covariation across several tasks.
- A 2024 secondary factor analysis reported candidate GCA factors for visual and olfactory learning batteries.
- Current evidence does **not** establish that the opt-out phenotype and learning/GCA phenotype share a common mechanism.
- Current evidence does **not** justify a numerical precision optimum, a fixed negative metacognition–GCA correlation, or a central-complex predictive-coding mechanism.

## Gate table

| Gate | Requirement | Status |
|---|---|---|
| G0 | Correct core literature identities and claims | PASS |
| G1 | Retire circular simulation evidence | PASS |
| G2 | Lock competing confirmatory models before outcome analysis | PASS |
| G3 | Obtain individual-level learning data or reproduce published covariance inputs | OPEN |
| G4 | Obtain same-individual uncertainty + learning battery, or collect it | OPEN |
| G5 | Trial-level associative-vs-latent model comparison | OPEN |
| G6 | Independent adversarial review before strong mechanistic language | OPEN |
| G7 | Empirical manuscript/results | BLOCKED by G3–G6 |

## Immediate next empirical target

The most informative new dataset would measure, in the same identified bees, at least three learning indicators and at least three uncertainty/control indicators, with colony identity, order, motivation/reward sensitivity and attrition recorded. A planned-missingness design is acceptable if the overlap graph identifies all latent covariances.

## Synthetic feasibility note

A deterministic model-recovery simulation is included to test whether a one-factor versus two-factor distinction is statistically recoverable under a hypothetical two-factor data-generating process. It is explicitly labeled synthetic. In the current default scenario (loading 0.65, factor correlation 0.35), the one-factor model is rarely selected even at N=60, but distinguishing correlated from independent two-factor structures improves substantially with larger N. This informs design planning only and does not estimate any bee parameter.
