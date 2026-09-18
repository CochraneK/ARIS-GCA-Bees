# Research plan — ARIS4C011

## 1. Research question

Does an auditable multi-evidence research-forensics framework improve coverage of known integrity-relevant issues and reduce reviewer burden relative to specialised single detectors or an LLM-only reviewer, while maintaining controlled false-alert rates and explicit abstention?

## 2. Conceptual target

The target is **trustworthiness-relevant anomaly screening**, not adjudication of misconduct.

The framework observes evidence O and produces a structured set of findings F. Human reviewers may use F to decide whether clarification or investigation is warranted. Intent is outside the automated target.

## 3. Detector families

F1. Statistical inference consistency  
F2. Discrete-summary feasibility and numerical forensics  
F3. Table / cross-section arithmetic and internal consistency  
F4. Image and figure forensics  
F5. Citation existence, metadata, context, and retraction status  
F6. Text reuse, tortured phrases, templates, and paper-mill similarity  
F7. Generative-AI provenance signals and watermark checks  
F8. Methods–results–abstract coherence  
F9. Registration, ethics, provenance, identifiers, and timeline consistency  
F10. Corpus/network anomalies across papers, authors, citations, figures, and templates

See DETECTOR_TAXONOMY.md.

## 4. Benchmark architecture

### Track A — content-only blind

Inputs:
- manuscript content;
- figures/tables;
- bibliographic references;
- registration/protocol only when it would have been available independently of later integrity findings.

Excluded:
- retraction/correction/Expression-of-Concern status if it supplies the target label;
- PubPeer/investigator commentary used to define the case;
- downstream author-history labels;
- explicit retraction reason text.

Purpose: estimate whether the paper itself contained detectable signals before/without the later integrity decision.

### Track B — open-world triage

Adds:
- Crossref/Retraction Watch notices;
- known corrections and Expressions of Concern;
- related-publication history;
- cross-paper/network evidence;
- public post-publication signals where legally and ethically usable.

Purpose: estimate practical review prioritisation.

Track B is **not** comparable to Track A as a pure predictive task; it is a workflow evaluation.

## 5. Case strata

### P — confirmed/official problem cases
Official notices or sufficiently documented public records. Each issue is coded rather than treating all retractions as equivalent.

Candidate issue codes:
- statistical/reporting inconsistency;
- data fabrication/falsification;
- image duplication/manipulation;
- plagiarism/text duplication;
- paper-mill/industrial fabrication;
- citation manipulation or fabricated references;
- authorship/peer-review manipulation;
- registration/ethics/provenance problem;
- other/unclear.

### E — known-error / correction cases
Corrections, corrigenda, and documented coding/reporting errors. These are critical negative controls for the inference "anomaly -> misconduct".

### C — no-known-integrity-concern comparators
Matched on publication year, field, article type, journal/venue where feasible, accessibility, and coarse manuscript characteristics.

The label explicitly means no known notice at extraction time, not verified absence of problems.

## 6. Splitting and leakage control

Ordinary random paper-level splits are prohibited for learned detectors.

Use grouped splitting by:
- known paper-mill family/template;
- high-overlap text cluster;
- duplicated-image cluster;
- author/collaboration component when relevant;
- journal special-issue cluster when relevant.

At least one temporal holdout is required.

A detector trained on known retracted paper-mill articles must not be evaluated on near-duplicate members of the same template family in a different split.

## 7. Baselines

B0. No automated screening / random review priority  
B1. statcheck-style statistical consistency  
B2. discrete-summary family (GRIM/GRIMMER/SPRITE/DEBIT where applicable)  
B3. citation verification only  
B4. text/paper-mill detector only  
B5. image detector only  
B6. LLM-only reviewer with manuscript text and a frozen prompt  
B7. simple unweighted alert count  
B8. full evidence-graph framework

Commercial systems can be described as prior art but are not required for a reproducible primary benchmark.

## 8. Primary outcome

**Eligible issue-type recall at fixed false-alert burden.**

A paper may contain multiple labelled issue types. Detector-family eligibility is recorded before scoring.

Primary operating point:
- freeze a maximum mean false-alert burden per comparator manuscript in the preregistration;
- compare issue recall at that burden.

Do not optimise the threshold separately on the confirmatory test set.

## 9. Secondary outcomes

- paper-level recall/precision as a descriptive secondary measure;
- macro-F1 across issue classes;
- calibration/Brier score for modules that emit probabilities;
- abstention rate;
- coverage = fraction of benchmark issues for which at least one detector is applicable;
- false alerts per manuscript;
- human minutes per manuscript;
- human minutes per true issue surfaced;
- proportion of alerts resolved without author contact;
- inter-rater agreement for human adjudication;
- severe false-positive rate.

## 10. Ablation

Run leave-one-family-out analyses:
- minus statistical;
- minus numerical/distributional;
- minus table consistency;
- minus image;
- minus citation;
- minus text/paper-mill;
- minus GenAI provenance;
- minus semantic coherence;
- minus provenance/registration;
- minus network.

Report Δ issue recall, Δ false-alert burden, and Δ reviewer time.

Pairwise overlap matrices and UpSet-style summaries will estimate complementarity among detector families.

## 11. Evidence fusion

Do not train a "fraud probability" target.

Each finding is a node carrying:
- detector ID and version;
- applicability;
- evidence class;
- exact evidence span/object;
- reproducibility status;
- confidence/calibration if relevant;
- plausible benign explanations;
- dependencies on other findings.

Edges encode:
- corroborates;
- contradicts;
- depends_on;
- same_source_as;
- same_claim_as;
- cross_document_match.

The system produces review priority plus an explanation.

## 12. Human evaluation

A stratified sample of manuscripts is independently reviewed by at least two reviewers using a frozen rubric informed by INSPECT-SR principles but extended beyond RCTs.

Reviewers see either:
A. manuscript only, or  
B. manuscript + structured forensic report.

Compare:
- time;
- issues found;
- false alerts accepted;
- confidence;
- agreement.

Order/randomisation should prevent learning carry-over.

## 13. Fairness / shortcut audit

Prohibited as suspicion predictors:
- nationality;
- country;
- author name origin;
- institutional prestige;
- English-proficiency proxy.

Required subgroup analyses where feasible:
- native vs non-native-English publication context using non-identifying aggregate proxies only if scientifically justified;
- translated vs non-translated text;
- field;
- publication year;
- manuscript length;
- journal type.

Text detectors must be audited for stylistic/language bias. A higher flag rate is not evidence of a higher misconduct rate.

## 14. Sample-size strategy

Pilot 0 is diagnostic and not powered for final claims.

Benchmark v1 should target enough labelled issues per major issue family to estimate recall with useful intervals. Rare issue families may remain descriptive.

The confirmatory sample size will be determined after a blinded feasibility pass using only:
- prevalence of eligible issue types;
- detector applicability;
- expected missingness;
- review-time variance.

No effect-size peeking from confirmatory outcomes.

## 15. Claims permitted before empirical run

Permitted:
- the detector ecosystem is fragmented;
- current publisher systems demonstrate practical orchestration needs;
- individual methods have heterogeneous applicability;
- a unified auditable benchmark/framework is methodologically motivated.

Not permitted:
- the integrated system detects misconduct better;
- any final sensitivity/specificity;
- prevalence of undetected misconduct;
- claims that a flagged paper is fraudulent.
