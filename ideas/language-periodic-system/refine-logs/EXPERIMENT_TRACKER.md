# Experiment Tracker · Language Periodic System

| ID | Experiment | Status | Decision role | Artifact |
|---|---|---|---|---|
| S0-A | Compression vs marginal-preserving shuffle | DONE | prerequisite structural signal | `../PILOT_REPORT.md` |
| S0-B | Residual pairwise NMI vs permutation null | DONE | prerequisite residual dependency | `../PILOT_REPORT.md` |
| S1-A | Random-split geometric model competition | DONE / publishing | optimistic held-out screen | `../STAGE1_REPORT.md` |
| S1-B | Glottolog family-held-out model competition | DONE / publishing | genealogy-aware screen | `../STAGE1_REPORT.md` |
| R1 | Connected-affinity sensitivity | TODO | rule out spectral disconnect artifact | — |
| R2 | Directly optimized circular model | TODO | rule out circular strawman | — |
| R3 | Feature-count / feature-selection sensitivity | TODO | robustness to coding choices | — |
| R4 | More repeated family-held-out splits + uncertainty | TODO | quantify model-difference stability | — |
| R5 | Geographic blocking / areal sensitivity | TODO | reduce contact/geographic leakage | — |
| R6 | Second dataset/domain replication | TODO | external robustness | — |
| ARIS-REV | Identity-bearing secondary novelty/research review | BLOCKED/PENDING | formal ARIS review gate | — |

## Current branch decision

`REFRAME_NONPERIODIC_GEOMETRY` is the **Stage-1 screening verdict**, not the final paper verdict.

The simple circular representation retains some predictive signal and moderate ordering stability, but currently underperforms the best non-periodic competitor under family-held-out validation. Robustness tests R1–R6 decide whether this is a fair rejection of global periodicity or an artifact of the initial implementation.

## Promotion gate

A numbered paper is not created until:

- R1/R2 establish a fair periodic baseline;
- at least R4 is complete;
- the main result survives enough genealogy/geography control to support its wording;
- ARIS-REV is completed honestly with a real reviewer identity/trace;
- final framing is frozen as positive periodic, local periodic, non-periodic geometry, or parked.
