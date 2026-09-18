# ARIS4C010 · Human Power / Precision Sensitivity Scenarios

This is **not** the final registered power analysis. It documents how strongly sample-size conclusions depend on the effect size and within-participant clustering assumed for the 8 retest trials.

## Approximation

For a protocol-level contrast in retest consistency, the repository computes the usual two-proportion normal-approximation requirement and then applies the simple design effect:

[
DE = 1 + (m-1)\rho,
]

where (m=8) repeated retest judgments and (ho) is a participant-level intra-class correlation sensitivity parameter.

This does not capture crossed item effects and therefore cannot replace the final hierarchical-model power analysis.

## Illustrative scenario

If P2 retest consistency is 0.80 and the scientifically meaningful P6 level is 0.88:

- ignoring clustering requires roughly 329 effective retest observations per arm;
- with (ho=0.05), (DE=1.35);
- this corresponds to roughly 56 participants per arm when each participant contributes 8 retests.

Therefore:

- one balanced form cycle: 36 participants/arm — primarily a feasibility stage;
- two cycles: 72 participants/arm — more plausible for detecting an ~0.08 reliability difference under this illustrative ICC;
- smaller true differences can require substantially more participants.

## Why the project uses staged recruitment

The first cycle estimates:
- baseline consistency;
- actual P6 category use;
- response-time burden;
- participant/item variance.

Those observed nuisance parameters can inform a properly frozen second-stage precision/power calculation without pretending that arbitrary assumptions are known in advance.

The code `power_retest_scenarios.py` prints a sensitivity grid for:
- P6 consistency 0.85 / 0.88 / 0.90 versus P2 = 0.80;
- participant-level ICC 0 / .05 / .10.

## Claim boundary

Do not cite the approximate numbers as a definitive required sample size.

The final confirmatory plan should simulate the intended hierarchical analysis using Stage-A nuisance estimates while keeping the effect-size target fixed independently of observed treatment/protocol differences.
