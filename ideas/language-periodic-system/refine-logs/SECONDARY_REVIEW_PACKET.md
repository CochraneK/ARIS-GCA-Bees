# Secondary ARIS Review Packet · Language Periodic-System Candidate

**Candidate:** `language-periodic-system`  
**Paper ID:** not assigned  
**Requested decision:** `PASS / REVISE / STOP`  
**Primary executor:** ChatGPT-side ARIS4C workflow  
**Required reviewer:** identity-bearing secondary ARIS reviewer, independent of the primary executor

## One-sentence claim to review

> **The simple global circular form of the language periodic-table hypothesis is not supported by held-out predictive or direct circularity evidence; hierarchical/non-circular models provide stronger family-held-out predictive benchmarks across TLI, GBI, and WALS, without establishing one universal tree geometry.**

## Why this is not a trivial negative result

The broad periodic-table metaphor is old (Baker 2001), and topology/latent-structure analyses already exist. The proposed contribution is the **explicit predictive operationalization and stress test** of that historical hypothesis against non-periodic alternatives, with family-held-out, area-aware, direct circularity, repeated-split, curation-replication, and external sparse-data checks.

A reviewer should reject the project if an existing study already performs an essentially equivalent periodic/circular-vs-tree/graph/factor held-out comparison on global typological structure.

## Closest prior art to inspect

1. Baker (2001), *The Atoms of Language*, chapter “Toward a Periodic Table of Languages”.
2. Port et al. (2018), *Persistent Topology of Syntax*.
3. Port, Karidi & Marcolli (2022), *Topological Analysis of Syntactic Structures*.
4. Skirgård et al. (2023), Grambank latent structure / genealogical constraints.
5. Graff et al. (2025), GBI/TLI dependency-curated structural datasets.
6. Verkerk et al. (2025/2026), spatiophylogenetic tests of grammatical universals.
7. SIGTYP/computational typology literature on held-out typological prediction.
8. Circular-seriation / circular-Robinson methodology (e.g. Armstrong, Guzmán & Sing-Long).

## Evidence table

| Stage | Question | Result | Reviewer-relevant interpretation |
|---|---|---|---|
| S0 | Is there non-random structure worth modeling? | `MIXED_SIGNAL` | yes; not periodic evidence |
| S1 | Does a simple global circle predict held-out structure? | circle < tree/graph under family hold-out | initial evidence against simple circle |
| S1B | Was the circle an obvious strawman? | directly optimized circle competitive at 40 features, loses again at 60 | fairness improved; result feature-count sensitive |
| S1C | Do predefined domains contain local periodicity? | none meet predeclared predictive+stability rule | no cherry-picked local cycle |
| S1D | Does the learned order satisfy held-out circularity / closure? | `CIRCULAR_ROBINSON_NOT_SUPPORTED`; 60-feature closure ratio 0.037 | direct evidence against global cycle |
| S1E | Does geometry survive geographic blocking? | all models weaken strongly in TLI | global portability questionable |
| S1F | Is tree > circle stable across family splits? | +0.073, 95% CI [0.055, 0.092], tree wins 20/20 | stable TLI ranking |
| S1G | Is TLI geographic collapse just small-test noise? | matched random ≈0.35–0.36 vs geographic ≈0.09–0.11 | no; but not necessarily causal geography |
| S1H | Does GBI curation reproduce ranking? | tree 0.122 vs circle 0.073; wins 12/12 | yes; curation robustness |
| S1I | Does WALS external sparse source reproduce ranking? | tree 0.603 vs circle 0.410; wins 8/8 | yes qualitatively; WALS geography differs |

## Important contradiction the reviewer must preserve

The geography result is **not** stable across representations:

- TLI/GBI show weak cross-Macroarea / geographic transfer;
- WALS shows strong cross-Macroarea association transfer (~0.634).

Therefore the manuscript must not promote “geographic heterogeneity explains language geometry” as a universal result. The robust cross-source result is the **tree/non-circular benchmark > simple circle under family hold-out**, not geographic collapse.

## Capacity/fairness issue

Tree/graph models are not exactly capacity-matched to a single circle. The project therefore does **not** infer “language is a tree” merely from predictive ranking.

The negative circular result also rests on:

- direct `n-1` angular optimization;
- predefined-domain tests;
- circular-Robinson-style row-unimodality diagnostics;
- explicit wrap-around closure support;
- low-rank comparisons;
- repeated family-held-out paired uncertainty;
- qualitative replication in GBI and WALS.

See `MODEL_CAPACITY_NOTE.md`.

## Claims the reviewer should reject if they appear

- “We discovered the first periodic table of language.”
- “No form of linguistic periodicity exists.”
- “Language is proven to be tree-shaped.”
- “Geography is the primary cause of linguistic structural geometry.”
- “Family-held-out validation removes all phylogenetic/contact dependence.”
- “Features are linguistic atoms/natural kinds because the models organize them.”

## Claims that are currently supportable

- The tested simple global circular/periodic model is not supported as the best predictive organization of cross-linguistic feature associations.
- Hierarchical/non-circular representations provide stronger family-held-out predictive benchmarks in TLI, GBI, and WALS.
- A directly learned circular order can be reproducible without exhibiting robust wrap-around closure or best-in-class prediction.
- Dataset representation materially affects the apparent portability of the full association geometry across regions.

## Reviewer questions

The secondary reviewer should answer all of the following explicitly:

1. **Novelty collision:** Is there a prior paper that already performs essentially this full predictive test of Baker-like periodic geometry against non-periodic alternatives?
2. **Faithfulness:** Is a directly optimized single-circle model plus circular-Robinson/closure testing a fair operationalization of the *simple global* periodic-table hypothesis?
3. **Capacity:** Does the claim boundary adequately avoid overinterpreting tree superiority?
4. **Validation:** Are top-level-family hold-outs, geography blocks, matched-size controls, GBI curation replication, and WALS sanity replication sufficient for a paper-level negative/mixed claim, or is a full phylogenetic model indispensable before submission?
5. **Statistics:** Is the repeated-split bootstrap treatment adequate as a robustness summary, and what uncertainty analysis should replace/supplement it in the manuscript?
6. **Data dependence:** Does WALS' contradictory geography result require a narrower framing than currently proposed?
7. **Publication value:** Is the resulting falsification/constraint of the periodic-table hypothesis sufficiently informative to warrant a paper, given Baker/Port/Grambank prior art?
8. **Decision:** `PASS`, `REVISE`, or `STOP`, with concrete reasons and mandatory changes.

## Kill conditions for reviewer

Return `STOP` if any is true:

- a direct prior-art collision removes the central novelty;
- the simple-circle operationalization is judged too unfaithful to support even the bounded negative claim;
- the data/evaluation design has a fatal leakage problem that cannot be repaired without changing the core study;
- the remaining contribution collapses to already-known “genealogy/geography matters” observations.

Return `REVISE` if the central test remains novel/useful but needs additional phylogenetic modeling, uncertainty treatment, capacity calibration, or claim narrowing.

Return `PASS` only if the reviewer independently accepts the novelty wedge, bounded negative conclusion, and evidence ladder as sufficient to promote the candidate to a numbered ARIS4C paper.

## Canonical artifacts to inspect

- `../RESEARCH_BRIEF.md`
- `../idea-stage/IDEA_REPORT.md`
- `../PILOT_REPORT.md`
- `../STAGE1_REPORT.md`
- `../STAGE1B_REPORT.md`
- `../STAGE1C_REPORT.md`
- `../STAGE1D_REPORT.md`
- `../STAGE1E_REPORT.md`
- `../STAGE1F_REPORT.md`
- `../STAGE1G_REPORT.md`
- `../STAGE1H_REPORT.md`
- `../STAGE1I_REPORT.md`
- `FINAL_PROPOSAL.md`
- `MODEL_CAPACITY_NOTE.md`
- `EXPERIMENT_TRACKER.md`

## Receipt requirement

The review is not complete until the repository contains an identity-bearing reviewer receipt/trace with reviewer identity, timestamp, verdict, and required changes. A primary-executor summary, this packet, or an unsigned self-review must not be treated as that receipt.
