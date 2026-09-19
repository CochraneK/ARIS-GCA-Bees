# Paper 002 · Chat / Agent History Summary

**Purpose:** durable summary of the ChatGPT-led Paper 002 thread for recovery after chat deletion, account/computer changes, or agent handoff.  
**Canonical scientific state:** use `STATUS.md`, `HANDOFF.md`, and `paper.json` if any historical note conflicts with newer Git state.

## Origin

The project began as an unnumbered idea:

**“Is There a Periodic System of Human Language? A Data-Driven Test Across the World’s Languages”**

The central discipline adopted early was:

> “periodic table” is a falsifiable hypothesis, not a desired visualization.

The candidate remained under:

`ideas/language-periodic-system/`

until an independent cross-family ARIS secondary review authorized promotion.

## Prior-art constraints established

The thread explicitly determined that the following are not novel by themselves:

- Baker (2001): periodic-table metaphor / parameter atoms;
- Grambank: large-scale morphosyntactic structure;
- Graff et al.: dependency-curated GBI/TLI datasets;
- Verkerk et al.: explicit spatiophylogenetic testing of grammatical universals;
- Port et al. / Port, Karidi & Marcolli: topology, dimensionality, persistent homology and clustering in syntactic parameter data;
- SIGTYP / computational typology: held-out typological feature prediction;
- circular seriation / circular-Robinson methods.

This forced the novelty wedge toward **explicit out-of-sample geometry competition** rather than “discovering structure”.

## Empirical ladder developed in chat

### Stage 0

Purpose:
test whether the structural data contain enough non-random organization to justify geometry modeling.

Result:
`MIXED_SIGNAL`.

Key methodological correction later preserved:
Stage 0 uses mode imputation → one-hot encoding → TruncatedSVD for compression, plus a separate pairwise NMI within-pair permutation screen. It is not ordinary PCA and not residualized NMI.

### Stage 1

Compared:
- null;
- rank-2 low-rank;
- Euclidean 2D;
- hierarchical tree;
- graph shortest path;
- circular model.

Family-held-out results favored tree/graph over the initial circle.

### Stage 1B

Added direct circular-angle optimization so the periodic model would not be dismissed as a weak spectral strawman.

Result:
40 features gave near tree/circle parity, while 60 features again favored non-periodic baselines.

### Stage 1C

Tested predefined structural domains rather than selecting “good-looking” circular domains post hoc.

No domain passed the joint local-periodicity gate.

Important conceptual example:
Grammar linear order had highly stable ordering but tree/low-rank prediction remained stronger.

### Stage 1D

Added direct circular-Robinson-style row-unimodality sensitivity and wrap-around closure.

Result:
`CIRCULAR_ROBINSON_NOT_SUPPORTED`.

Important:
60-feature closure ratio ≈0.037.

Later manuscript boundary:
40-feature closure 0.608 ± 0.764 is highly unstable and should not be interpreted as positive evidence.

### Stage 1E / 1G

Geographic hold-out initially caused strong transfer collapse in TLI.

Stage 1G matched-size controls showed this was not explained solely by smaller geographic test samples.

However this never became the headline because WALS later contradicted the geographic-collapse pattern.

### Stage 1F

20 repeated TLI top-level-family hold-outs.

Key result:
- tree 0.182;
- circle 0.109;
- paired +0.073;
- split-bootstrap 95% CI [0.055, 0.092];
- tree wins 20/20.

Important reporting boundary:
bootstrap interval measures sampled-split sensitivity, not phylogenetic uncertainty.

### Stage 1H

GBI curation/representation robustness:
- tree 0.122;
- circle 0.073;
- tree wins 12/12.

### Stage 1I

Separately processed WALS sanity representation:
- tree 0.603;
- circle 0.410;
- tree wins 8/8.

Critical correction later made:
WALS contributes source data to TLI, so WALS is not a statistically independent replication of TLI. It is a separately processed representation/sanity check.

WALS also showed strong macroarea transfer, contradicting TLI/GBI geographic-transfer weakness. Geography therefore remains a secondary representation-dependent result.

## Scientific reframe

The project moved away from:

“build a periodic table of language”

toward:

**“Testing the periodic-table hypothesis of human language”**

and ultimately the title was tightened to:

**“Testing the periodic-table hypothesis of human language: predictive evidence does not support a global circular organization”**

The final bounded interpretation became:

> human language shows reproducible structural organization, but the tested simple global circle is not the strongest held-out predictive description.

The thread explicitly rejected stronger claims such as:
- language is a tree;
- all periodicity is impossible;
- geography universally determines structural geometry.

## ARIS promotion review

A WorkBuddy handoff was created because the primary executor was OpenAI GPT family and ARIS required a different-family identity-bearing reviewer.

The user ran WorkBuddy / Tencent Hy3.

Reviewer result:
- PASS;
- promotion authorized.

Paper 002 was then formally created at:

`papers/002-language-geometry/`

The old `002-REVIEW-CANDIDATE` pointer was retired.

## Manuscript construction

ChatGPT produced Draft v1 with:

- Abstract;
- Introduction;
- Materials and Methods;
- Stage 0–1I Results;
- Discussion;
- Limitations;
- Conclusion;
- References.

Additional manuscript infrastructure added:

- tables;
- figures;
- claims–evidence matrix;
- data provenance;
- bibliography audit;
- manuscript checklist;
- reproducibility workflows;
- model-capacity note / claim-boundary discipline.

## Literature rescan

A 2026 rescan found Kemp (2026), showing real circular/symmetry structure in specific semantic domains.

This was treated as important adjacent work, not a fatal collision.

Resulting conceptual boundary:

> domain-grounded circularity can be real while a single global heterogeneous-feature circle is unsupported.

General circular-arrangement prior art was also expanded with Evangelopoulos et al.

## Manuscript-stage WorkBuddy review

A second, fresh WorkBuddy manuscript-stage review was requested after Draft v1.

Verdict:

`PASS_SUBMISSION_PREP`

Authorization:
AUTHORIZED.

No blocking scientific changes.
No blocking manuscript changes.

Reviewer optional suggestions were implemented:
- narrower title;
- explicit Stage-1 0.35 vs Stage-1C 0.40 threshold distinction;
- stronger warning that 40-feature closure estimate is unstable.

## Journal choice

Primary target chosen:

**Linguistic Typology**

Reason:
Paper 002 is primarily a cross-linguistic typology / structural-variation / methodology paper.

Backup:
**Journal of Language Evolution**

A journal-specific package was created with:
- blinded manuscript;
- title-page template;
- cover letter;
- declarations;
- AI disclosure;
- data statement;
- metadata checklist;
- anonymised supplement;
- figure legends / alt text;
- pinned reproducibility environment;
- submission-build workflow.

## Historical 3-figure submission QA

The journal package was built and visually inspected page by page.

Historical reviewed build:
- workflow run `35412714647`;
- artifact `10575195098`;
- 31-page DOCX/PDF;
- technical verdict: PASS;
- anonymisation clean;
- Table 6 pagination fixed.

This artifact is now **historical only** because the canonical manuscripts were subsequently expanded to six figures.

## Later canonical visual expansion

Other concurrent ARIS4C work advanced Paper 002 after the original 3-figure QA:

- English manuscript complete;
- Chinese manuscript complete;
- canonical figures: 6;
- tables: 6;
- public EN/ZH HTML/PDF outputs completed;
- current paper status became `submission-ready-author-metadata-pending`.

Therefore the 3-figure journal artifact cannot be treated as final.

## Current state at chat deletion handoff

The science and reviews are complete.

The remaining technical work is:

1. refresh the Linguistic Typology blinded manuscript to the six-figure canonical version;
2. refresh six submission figure files / legends / alt text;
3. rebuild the journal package;
4. repeat full visual, text-parity, metadata and anonymisation QA;
5. update `SUBMISSION_QA.md` and `paper.json` to the new build;
6. obtain author-only metadata/declarations;
7. upload/submit via ScholarOne.

No new scientific analysis is presently required.

## Recovery entry point

Read first:

`HANDOFF.md`

Then:
- `STATUS.md`
- `../paper.json`
- `../submission/linguistic-typology/SUBMISSION_QA.md`

