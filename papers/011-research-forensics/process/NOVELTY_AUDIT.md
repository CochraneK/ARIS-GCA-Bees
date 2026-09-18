# Novelty audit — ARIS4C011

Updated: 2026-09-18

## Bottom line

ARIS4C011 must **not** claim to be:
- the first system to combine research-integrity tools;
- the first multimodal misconduct detector;
- the first automated paper-mill screening system;
- the first trustworthiness checklist.

Those claims are already occupied by publisher infrastructure and prior research.

The defensible research contribution is a **benchmark-and-evidence architecture** that asks whether integrity-relevant evidence can be detected, combined, audited, and used for human review without collapsing heterogeneous errors/retractions into a binary misconduct label.

## Nearest neighbours

### STM Integrity Hub
What it already does:
- publisher-facing orchestration;
- multiple screening tools/workflows;
- duplicate-submission and paper-mill-oriented checks;
- integration of third-party integrity resources.

What remains open for 011:
- open detector contract;
- issue-level ground truth;
- explicit detector applicability/abstention;
- reproducible benchmark and split leakage rules;
- detector-family ablation;
- evidence dependency graph;
- human false-alert burden.

### Elsevier Check Integrity
What it already does:
- large-scale automated manuscript integrity screening embedded in editorial workflows;
- human integrity-analyst oversight.

Implication:
Operational scale and human-in-the-loop screening are not themselves novel claims.

### INSPECT-SR
What it already does:
- structured trustworthiness assessment;
- up to 21 checks across four domains for RCTs;
- explicitly avoids treating concerns as proof of fraud.

What remains open for 011:
- cross-disciplinary machine-executable checks;
- unified detector schemas;
- empirical complementarity/ablation;
- benchmarking of review efficiency.

### BMMDetect / BioMCD
Nearest methodological threat to a generic "multimodal detector" novelty claim.

Reported design:
- biomedical retracted-vs-control classification;
- 13,160 retracted articles and 53,411 controls;
- journal/institution metadata;
- PubMedBERT semantic embeddings;
- GPT-4o-derived textual/methodological attributes;
- reported ROC-AUC 74.33%.

Why it changes 011:
A binary retraction target can mix many causes: fabrication, falsification, plagiarism, paper mills, peer-review manipulation, honest errors, publisher problems, and other reasons. Predictive performance can also be inflated by stable correlates of retraction rather than content evidence of a specific problem.

Therefore 011 treats BMMDetect-like classification as a **baseline and stress-test target**, not as the target architecture.

### ResAIKit / AntiAI
Current web project presenting a broad catalogue of text, image, and statistical integrity indicators with evidence-first review framing.

Implication:
"Many checks in one interface" is not sufficient novelty. 011 must contribute benchmark science, evidence semantics, and controlled comparisons.

### Scancar et al. paper-mill screening
Demonstrates that learned text classifiers can detect recurring paper-mill patterns at scale.

Implication:
- paper-mill text detection is one detector family, not the whole project;
- paper-mill/template families must not cross train/test boundaries;
- language/style shortcut audits are mandatory.

### Citation-integrity agents / Cite Lens
Reference verification and semantic citation-context screening already exist as specialised systems.

Implication:
Citation checking is a module/baseline, not a standalone novelty claim.

## Locked novelty statement

Subject to final systematic prior-art review, ARIS4C011 targets the following combination:

1. **Issue-level truth rather than binary retraction labels.**
2. **Applicability-aware detector routing with explicit abstention.**
3. **Two-track evaluation separating content-only detection from post-publication/open-world triage.**
4. **Evidence classes plus a dependency-aware evidence graph.**
5. **Grouped and temporal leakage control for paper-mill, text, image, author, and article families.**
6. **Detector-family complementarity and leave-one-family-out ablation.**
7. **Alert burden and human review time as primary workflow outcomes.**
8. **Shortcut/fairness audits that prohibit geography, author-name origin, or institutional prestige as suspicion signals.**
9. **Correction/honest-error cases as an explicit stress set against the inference anomaly -> misconduct.**
10. **No automated author-level misconduct or intent classification.**

## Falsifiable novelty test

The project should be considered insufficiently novel if a prior peer-reviewed/open system is found that already combines all of the following:
- issue-level labelled benchmark across multiple integrity domains;
- detector applicability/abstention;
- leakage-aware grouped/temporal evaluation;
- evidence dependency modelling;
- human alert-burden evaluation;
- correction/error controls;
- explicit shortcut/fairness testing.

If such a system is found, 011 should pivot to the benchmark/shortcut study alone rather than preserve an inflated framework claim.
