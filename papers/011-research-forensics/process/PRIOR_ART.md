# Prior-art map — live audit 2026-09-18

This file records the initial landscape used to position ARIS4C011. It is not yet a systematic review.

## Integrated publishing infrastructure

### STM Integrity Hub
A publisher-facing cloud environment that can combine multiple integrity checks and third-party tools. Its public materials describe on-demand and ambient screening, duplicate-submission checking, Papermill Alarm integration, PubPeer integration, and broader tool orchestration.

Relevance:
- proves practical demand for orchestration;
- establishes that integration itself is not novel;
- pushes ARIS4C011 toward open auditability, benchmark science, applicability semantics, issue-level evaluation, and evidence fusion.

Sources:
- https://stm-assoc.org/what-we-do/strategic-areas/research-integrity/integrity-hub/
- https://stm-assoc.org/what-we-do/strategic-areas/research-integrity/integrity-hub/stm-integrity-hub-pilot-program/

## Trustworthiness checklists

### INSPECT-SR
A consensus-developed tool for RCT trustworthiness assessment with up to 21 checks across four domains: post-publication notices; conduct/governance/transparency; text/figures; and results.

Key positioning:
- it explicitly distinguishes trustworthiness concerns from fraud diagnosis;
- it is RCT-focused and reviewer-guided;
- ARIS4C011 generalises the principle to cross-disciplinary machine-executable checks and detector evidence contracts.

Source:
- https://pmc.ncbi.nlm.nih.gov/articles/PMC12424918/

## Statistical consistency

### statcheck
Automatically extracts common APA-style NHST results, recomputes p values, and flags inconsistencies/gross inconsistencies.

Source:
- Nuijten MB, Polanin JR. Research Synthesis Methods. 2020. doi:10.1002/jrsm.1408
- https://pmc.ncbi.nlm.nih.gov/articles/PMC7540394/

### GRIM
Checks whether rounded means for integer-valued data are mathematically possible given N.

Source:
- Brown NJL, Heathers JAJ. Social Psychological and Personality Science. 2017. doi:10.1177/1948550616673876

### GRIMMER
Extends granularity reasoning to reported variability / standard deviations under relevant assumptions.

Source:
- Anaya J. PeerJ Preprints. 2016. doi:10.7287/peerj.preprints.2400v1

### SPRITE
Reconstructs sample distributions compatible with reported summary constraints; useful as a forensic reconstruction tool but heuristic/non-unique.

### DEBIT
Checks mutual consistency of binary-data mean, standard deviation and sample size.

Reference implementation/documentation:
- https://lhdjung.github.io/scrutiny/reference/debit.html

### Review of statistical forensics
A recent review covers raw-data and reported-summary approaches including Newcomb-Benford, variance methods, effect-size anomalies, p-value analyses, GRIM/GRIMMER/SPRITE, and warns against treating anomaly detection as proof of fraud.

Source:
- https://pmc.ncbi.nlm.nih.gov/articles/PMC12121900/

## Paper mills and text

### Tortured phrases
Cabanac, Labbé and Magazinov documented tortured phrases, suspicious text generation/rewrite patterns, nonexistent citations, and other cross-paper signals.

Source:
- https://arxiv.org/abs/2107.06751

### Machine-learning paper-mill screening
Scancar et al. trained a BERT-based classifier using known/retracted paper-mill papers and independently collected validation data, then screened a large cancer-research corpus.

Source:
- BMJ 2026;392:e087581
- https://www.bmj.com/content/392/bmj-2025-087581

Methodological implication:
- learned paper-mill detectors are a serious baseline;
- cluster/template leakage and language/style bias require explicit testing.

## Citation forensics

### Retraction status
Crossref now exposes the Retraction Watch database via production services and a downloadable dataset.

Source:
- https://www.crossref.org/documentation/retrieve-metadata/retraction-watch/

### Citation-context relevance
Cite Lens is an example of embedding-based analysis of article-reference and context-reference similarity to surface out-of-scope/out-of-context citations.

Source:
- https://link.springer.com/chapter/10.1007/978-3-032-06136-2_3

### Fabricated bibliographic citations
LLMs can generate plausible but nonexistent or bibliographically incorrect references, motivating deterministic reference existence/metadata checks.

Source:
- Walters WH, Wilder EI. Scientific Reports. 2023;13:14045.
- https://www.nature.com/articles/s41598-023-41032-5

## Image integrity

STM maintains an Image Integrity Working Group concerned with requirements, quality measurement, issue classification, and deployment of automated image alteration/duplication screening.

Source:
- https://stm-assoc.org/what-we-do/strategic-areas/research-integrity/image-integrity/

ARIS4C011 should treat duplicate detection and manipulation inference as separate tasks.

## AI provenance / watermarking

### Generic post-hoc AI detectors
Current evidence indicates substantial false positives, domain/language/style sensitivity, and easy evasion under rewriting. Generic detector scores therefore default to weak evidence.

Recent source:
- Karr JA et al. Why AI Detection Fails for Academic Integrity. arXiv:2608.11256 (2026).

### Watermarking
SynthID-Text demonstrates scalable model-side text watermarking, but the authors emphasise that generative watermarks are not a complete detection solution and can be weakened by edits/paraphrasing.

Source:
- Nature 2024;634:818–823.
- https://www.nature.com/articles/s41586-024-08025-4

## Novelty statement after initial audit

The defensible novelty is **not** "the first system to combine research-integrity tools." Publisher systems already do that.

The target novelty is the combination of:
1. open/reproducible detector contracts;
2. applicability-aware routing and abstention;
3. issue-level, two-track benchmark with leakage controls;
4. evidence-class semantics and evidence graph;
5. detector-family complementarity/ablation;
6. explicit human review burden;
7. fairness/shortcut audit;
8. no automated misconduct/intent classification.

This claim must be re-audited before submission.
