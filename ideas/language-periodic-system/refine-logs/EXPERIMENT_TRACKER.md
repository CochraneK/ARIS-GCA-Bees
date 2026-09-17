# Experiment Tracker · Language Periodic System

| ID | Experiment | Status | Decision role | Artifact |
|---|---|---|---|---|
| S0-A | Compression vs marginal-preserving shuffle | DONE | prerequisite structural signal | `../PILOT_REPORT.md` |
| S0-B | Residual pairwise NMI vs permutation null | DONE | prerequisite residual dependency | `../PILOT_REPORT.md` |
| S1-A | Random-split geometric model competition | DONE | optimistic held-out screen | `../STAGE1_REPORT.md` |
| S1-B | Glottolog family-held-out model competition | DONE | genealogy-aware screen | `../STAGE1_REPORT.md` |
| R1 | Connected-affinity sensitivity | DONE | remove spectral disconnect artifact | `../STAGE1B_REPORT.md` |
| R2 | Directly optimized circular model | DONE | rule out obvious circular strawman | `../STAGE1B_REPORT.md` |
| R3 | 40/60 feature-count sensitivity | DONE | robustness to feature count | `../STAGE1B_REPORT.md` |
| R4 | Predefined TLI-domain local periodicity screen | DONE | test local periodicity without cherry-picking | `../STAGE1C_REPORT.md` |
| R5 | Standards-aligned circular seriation / circular-Robinson test | TODO | final fair periodicity sensitivity | — |
| R6 | More repeated family-held-out splits + uncertainty / capacity accounting | TODO | quantify model differences | — |
| R7 | Geographic blocking / areal sensitivity | TODO | reduce contact/geographic leakage | — |
| R8 | Second dataset or independent structural replication | TODO | external robustness | — |
| ARIS-REV | Identity-bearing secondary novelty/research review | BLOCKED/PENDING | formal ARIS review gate | — |

## Evidence trajectory

### Stage 0
`MIXED_SIGNAL`: substantial non-random compressibility and a tail of residual associations justified direct geometry tests.

### Stage 1
`REFRAME_NONPERIODIC_GEOMETRY`: the simple circular model predicted held-out feature associations worse than tree/graph alternatives, especially under top-level-family hold-out.

### Stage 1B
`MIXED_ROBUSTNESS`: direct angular optimization and connected affinity showed that the original circle was not purely a strawman. At 40 features the optimized circle roughly matched tree, but at 60 features it again lagged tree/low-rank models.

### Stage 1C
`NO_PREDEFINED_LOCAL_PERIODIC_CANDIDATE`: five TLI-defined structural domains were screened with four valid family-held-out replicates each. None met the predeclared combination of predictive competitiveness and circular-order stability required for a local periodic candidate.

The strongest circular-looking subsystem was **Grammar linear order**, where the optimized circle had Spearman 0.401 and high order stability 0.811, but tree and low-rank models were both about 0.49. This looks more like stable structured ordering than a uniquely circular geometry.

`Grammatical categories` remained ambiguous: optimized circle 0.252 vs tree 0.229, but circular stability 0.373 missed the predeclared 0.40 threshold.

## Current branch decision

The candidate should now be **reframed rather than promoted as a periodic-table discovery**. The primary research question becomes which geometry best characterizes and predicts cross-linguistic structural space, with the historical periodic-table proposal retained as the falsified-or-constrained hypothesis under test.

R5 is still required because circular seriation has a formal methodology based on circular Robinson matrices; the project should not claim a fair rejection after testing only custom/spectral circular models.

## Promotion gate

A numbered paper is not created until:

- R5 establishes a standards-aligned final periodic baseline;
- R6-R8 provide enough uncertainty, geography, and replication control for manuscript wording;
- ARIS-REV is completed honestly with a real reviewer identity/trace;
- the final framing is frozen as predictive non-periodic geometry, a narrower mixed result, or parked.
