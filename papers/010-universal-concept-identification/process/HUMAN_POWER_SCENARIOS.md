# ARIS4C010 · Human Power / Precision Sensitivity Scenarios

This is **not** the final registered power analysis. It documents how strongly sample-size conclusions depend on the effect size and within-participant clustering assumed for the 8 retest trials.

## Approximation

For a pairwise protocol contrast in retest consistency, the repository computes the usual two-proportion normal-approximation requirement and then applies the simple design effect:

`DE = 1 + (m - 1) × ρ`

where `m = 8` repeated retest judgments and `ρ` is a participant-level intra-class correlation sensitivity parameter.

This does not capture crossed item effects and therefore cannot replace the final hierarchical-model power analysis.

## Mechanism-specific scenarios

The design now includes three protocols:

- P2 = binary forcing;
- P3 = coarse MAYBE escape;
- P6 = fine-grained semantic states.

Therefore the key contrasts are P2→P3 and P3→P6.

## Illustrative P2→P3/P6-scale scenario

If P2 retest consistency is 0.80 and a coarse/rich protocol reaches 0.88:

- ignoring clustering requires roughly 329 effective retest observations per arm;
- with `ρ = 0.05`, `DE = 1.35`;
- this corresponds to roughly 56 participants per arm when each participant contributes 8 retests.

Therefore:

- one balanced form cycle: 36 participants/arm — primarily a feasibility stage;
- two cycles: 72 participants/arm — more plausible for detecting an ~0.08 pairwise reliability difference under this illustrative ICC;
- smaller true differences can require substantially more participants.

## Why the project uses staged recruitment

The first cycle estimates:
- baseline consistency;
- actual P6 category use;
- response-time burden;
- participant/item variance.

Those observed nuisance parameters can inform a properly frozen second-stage precision/power calculation without pretending that arbitrary assumptions are known in advance.

The code `power_retest_scenarios.py` prints sensitivity grids for:

- P2=.80 versus P3-like targets .85 / .88 / .90;
- P3=.85 versus P6 targets .88 / .90 / .92;
- participant-level ICC 0 / .05 / .10.

## Claim boundary

Do not cite the approximate numbers as a definitive required sample size.

The final confirmatory plan should simulate the intended hierarchical analysis using Stage-A nuisance estimates while keeping the effect-size target fixed independently of observed treatment/protocol differences.


## Fine-graining is likely harder

The scientifically distinctive comparison is P3→P6, not P2→P6.

If P3 already raises retest consistency to 0.85 and P6 only raises it to 0.88, the absolute difference is 0.03. Under the same simple clustered approximation, that can require far more participants than the 0.08 scenario.

Therefore a null P3→P6 result from one 36-person-per-arm cycle should not be interpreted as strong evidence that fine-grained states have no value. Stage A is primarily for nuisance-parameter estimation and feasibility.

The final power simulation should use the intended hierarchical model and a pre-specified minimum worthwhile P3→P6 effect.
