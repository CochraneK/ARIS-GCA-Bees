# Research Forensics at Scale: An Auditable Multi-Evidence Framework for Scientific Integrity Screening

**Methods and benchmark manuscript draft — ARIS4C011**  
**Status:** Methods frozen in principle; confirmatory benchmark results pending  
**Author:** Cunyi Kang

## Abstract

### Background

Scientific-integrity screening is fragmented across statistical consistency checks, image analysis, text-similarity and paper-mill classifiers, citation verification, post-publication notices, registration checks, and emerging generative-AI provenance methods. Publisher infrastructures increasingly orchestrate multiple tools, while structured trustworthiness instruments show the value of explicit human review. However, a central methodological problem remains: heterogeneous detectors have different applicability conditions, error modes, evidential meanings, and dependencies. Treating their outputs as interchangeable scores—or treating retraction status as a unitary misconduct label—can create leakage, shortcut learning, and false escalation.

### Objective

We propose Research Forensics, an open, auditable framework and benchmark for evaluating whether multiple integrity-relevant signals can improve issue detection and reviewer triage without converting anomalies into automated allegations of misconduct.

### Methods

The framework routes scientific artifacts to ten detector families: statistical-inference consistency; discrete-summary and numerical forensics; table and cross-section consistency; image forensics; citation integrity; text reuse and paper-mill similarity; generative-AI provenance; methods-results semantic coherence; registration and provenance checks; and corpus/network analysis. Each detector must first establish applicability and may return FLAG, PASS, ABSTAIN, or ERROR. Findings are represented using evidence classes and a dependency-aware evidence graph. The benchmark separates a time-safe content-only Track A from an open-world Track B. Ground truth is issue-level rather than binary retraction status, with separate strata for officially documented problems, documented corrections/errors, and matched papers with no known integrity concern. Primary evaluation is eligible issue-type recall at a fixed false-alert burden. Planned analyses include detector-family baselines, leave-one-family-out ablation, grouped and temporal leakage controls, shortcut stress tests, correction/error adversarial cases, calibration, fairness analyses, and human-review burden.

### Design validation

A live Crossref/Retraction Watch source audit identified two benchmark hazards before large-scale data collection. First, update-query records can represent a notice rather than the affected work and can contain multiple publisher and Retraction Watch assertions for the same event. Second, current metadata for affected works can explicitly contain later status information such as a RETRACTED title prefix. A three-record real-data seed also showed that the single status “retracted” can correspond to nonspecific validity concerns, gift authorship, or manipulated peer review, some of which need not be detectable from manuscript content.

### Conclusion

Research Forensics reframes automated integrity assessment as applicability-aware, evidence-preserving scientific auditing. The proposed benchmark is designed to measure which detector families provide independent forensic value, how much apparent predictive performance derives from shortcuts, and whether structured evidence improves human review. No claim of detector superiority is made before confirmatory evaluation.

## 1. Introduction

The integrity of the scientific record is challenged by both ordinary error and deliberate manipulation. The observable traces of these problems are heterogeneous. A paper may contain an arithmetically impossible mean, an inconsistent p value, a duplicated image, a citation that does not exist, a citation that fails to support the claim for which it is used, a registration timeline inconsistency, templated language associated with paper mills, or patterns that become visible only when many papers are viewed as a network. Conversely, some integrity problems—such as gift authorship or manipulated peer review—may leave little necessary trace in the scientific content itself.

The technical ecosystem reflects this heterogeneity. statcheck automates recomputation of common null-hypothesis significance tests from reported statistics and degrees of freedom [1]. GRIM tests whether rounded means of granular integer data are possible given sample size and scale structure [2]. GRIMMER extends granularity reasoning to measures of variability, while SPRITE reconstructs candidate distributions compatible with reported summary statistics [3,4]. DEBIT targets mutual consistency among the mean, standard deviation, and sample size of binary data [5]. These methods are powerful precisely because they are bounded: they answer specific mathematical questions under specific assumptions.

Other integrity problems require different evidence. Publishers increasingly use image-duplication screening together with expert verification; a 2025 report from the American Society for Microbiology described routine image screening as a human-in-the-loop process rather than an autonomous adjudicator [6]. Machine-learning approaches have been developed to screen for paper-mill-like text at large scale, including a 2026 BMJ study using a BERT-based classifier trained on known paper-mill publications [7]. BMMDetect goes further by combining metadata, semantic embeddings, and model-extracted manuscript attributes to classify retracted biomedical articles versus controls [8]. Generative-AI provenance methods span post-hoc classifiers and generator-side watermarking, such as SynthID-Text [9]. Yet recent evidence also shows that generic AI-text classifiers can be sensitive to editing, domain, and style and can be evaded through rewriting, making them unsuitable as standalone misconduct evidence [10].

Integration is no longer, by itself, a novel idea. The STM Integrity Hub provides a cloud environment in which publishers can configure multiple research-integrity screening tools, including third-party integrations, duplicate-submission checks, paper-mill signals, and post-publication resources [11]. INSPECT-SR similarly demonstrates the value of structured, multidomain trustworthiness assessment through up to 21 checks for randomized controlled trials [12]. These developments make the remaining methodological gap more precise: how should heterogeneous signals be represented, combined, benchmarked, and audited so that a system measures integrity-relevant evidence rather than artifacts of labels, publishers, geography, language, or post-publication metadata?

The problem is especially acute when “retracted” is used as a positive class. Retraction is an editorial status, not a single causal mechanism. A retraction can follow image manipulation, fabrication, plagiarism, authorship problems, peer-review manipulation, publisher error, or other circumstances. A classifier may therefore learn correlates of the retraction process rather than features of the issue one hopes to detect. Journal identity, publication year, venue prestige, language style, institution metadata, formatting, and known paper-mill template families can all become shortcuts. A high area under the curve on a random retracted-versus-control split does not by itself establish forensic utility.

We therefore propose Research Forensics, an auditable multi-evidence framework and benchmark with four commitments. First, the unit of evidence is an issue-specific finding, not an author-level misconduct label. Second, detector applicability and abstention are first-class outputs. Third, content-only detection is separated from open-world post-publication triage. Fourth, performance is evaluated in terms of issue coverage and review burden under leakage-aware, time-aware, and fairness-aware conditions.

## 2. Research questions

The study is organized around five confirmatory questions.

**RQ1. Integration.** At a fixed false-alert burden, does an integrated multi-evidence framework identify a larger fraction of eligible, independently documented issue types than the strongest eligible single-detector family?

**RQ2. Complementarity.** Which detector families contribute unique issue yield after accounting for correlated findings and shared evidence sources?

**RQ3. Shortcut learning.** How much performance in binary retraction classification survives strict matching, grouped family splits, removal of contextual metadata, and temporal holdout?

**RQ4. Abstention and false escalation.** Does explicit applicability/abstention reduce invalid checks and unsupported escalation, particularly for documented corrections and honest errors?

**RQ5. Human review.** Does a structured forensic report increase issue yield per unit reviewer time compared with manuscript-only review and an LLM-only review baseline?

The primary hypothesis is not that every detector improves performance. Some detector families may add little unique information, be applicable to only a small fraction of manuscripts, or create unacceptable false-alert burdens. Such negative findings are informative because they quantify which forensic methods are operationally useful.

## 3. Conceptual framework

### 3.1 Observation is not adjudication

Research Forensics separates four layers:

1. **Artifact:** the manuscript, tables, figures, references, supplement, metadata, code, data, registration, or related papers available to the screen.
2. **Observation:** an extracted statistic, image match, citation relation, metadata relation, or semantic inconsistency.
3. **Finding:** a detector-specific interpretation of an observation under stated assumptions.
4. **Adjudication:** a human or official conclusion about what happened and whether policy was violated.

The automated system operates at layers 1–3. It may quote an existing official adjudication in Track B, but it does not generate a new misconduct determination.

### 3.2 Evidence classes

Each finding is assigned an evidence class:

- **E0 — metadata observation:** a DOI resolves, a registration exists, or an update relation is present.
- **E1 — deterministic contradiction:** a mathematical or logical incompatibility under satisfied assumptions.
- **E2 — externally verifiable provenance fact:** an official notice exists, a cited identifier resolves to a different work, or a registration timestamp has a documented relation to study dates.
- **E3 — high-specificity forensic match:** for example, a verified cross-panel or cross-paper duplicate where the match itself is reproducible.
- **E4 — model-derived anomaly:** a calibrated image, semantic, paper-mill, or network model produces an anomalous score.
- **E5 — weak/context-dependent heuristic:** a generic AI-text detector score, unjustified digit anomaly, or other signal whose interpretation is highly assumption dependent.

Evidence class is not severity, culpability, or a guilt scale.

### 3.3 Applicability before execution

Every detector must answer whether it is applicable before its output can be interpreted. A detector may return:

- **FLAG:** the detector was validly applied and identified its target condition;
- **PASS:** the detector was validly applied and did not identify its target condition;
- **ABSTAIN:** the detector lacks required information or assumptions do not hold;
- **ERROR:** execution failed.

ABSTAIN and ERROR are not converted to PASS. This distinction matters because forensic coverage is inherently uneven. For example, GRIM is not a universal test of any reported mean; it requires granular integer-valued data and an interpretable denominator. A citation-context model cannot assess claims whose cited full text is inaccessible. An image duplication detector is irrelevant to a paper with no eligible images.

### 3.4 Detector families

Research Forensics defines ten families.

**F1 Statistical-inference consistency.** Recalculation of reported test statistics, p values, degrees of freedom, confidence intervals, effect estimates, and related algebraic relationships.

**F2 Discrete-summary and numerical forensics.** GRIM, GRIMMER, SPRITE, DEBIT, and distribution/digit checks where their assumptions are justified.

**F3 Table and cross-section consistency.** Denominators, percentages, participant flow, subgroup totals, SD/SE confusion, repeated sample sizes, and abstract-text-table contradictions.

**F4 Image and figure forensics.** Within-paper and cross-paper duplication, copy-move, crop/rotation/mirror matches, splicing or local inconsistencies, and figure provenance. Detection of similarity is separated from interpretation of whether reuse is legitimate.

**F5 Citation forensics.** Reference existence, DOI and bibliographic agreement, retraction/correction status, semantic support, and citation-network anomalies.

**F6 Text and paper-mill signals.** Exact and near-duplicate text, tortured phrases, templates, recurrent phrase families, and trained paper-mill similarity models.

**F7 Generative-AI provenance.** Generator-side watermark verification where technically possible, generic AI-text classifiers, token/probability-derived features, and disclosure consistency. AI assistance itself is not classified as misconduct.

**F8 Methods-results semantic coherence.** Outcomes absent from methods, unexplained analysis populations, contradictory directions or magnitudes, analyses that lack required inputs, and claims unsupported by reported results.

**F9 Registration, ethics, and provenance.** Registry existence and timing, protocol drift, ethics identifiers, ORCID/affiliation consistency, data/code statements, and impossible timelines.

**F10 Corpus and network forensics.** Cross-document text or image families, unusual reference-list overlap, reciprocal citation structures, repeated template fingerprints, and other graph-level anomalies.

## 4. Agent architecture

The reusable Research Forensics Agent implements a router rather than a monolithic judge.

### 4.1 Provenance and safety preflight

The agent first identifies artifact version and mode. In Track A, the artifact must be historically equivalent to what was available before the outcome being predicted. A current PDF containing a later retraction banner is not eligible, even if a retraction-reason database column is hidden. A current bibliographic title prefixed with “RETRACTED:” is likewise outcome-contaminated.

Track A therefore fails closed unless title and document time safety are established. Track B can use current metadata and post-publication evidence, provided their provenance is explicit.

### 4.2 Structured extraction

The paper is decomposed into source-linked objects: sections, claims, reported sample sizes, statistical tests, table cells, figure panels, references, citation contexts, outcomes, methods, registrations, and identifiers. Source locators are retained so that every finding can be checked against the original artifact.

### 4.3 Deterministic-first execution

The router prioritizes low-inference checks when applicable. A p-value recomputation or impossible discrete mean is easier to reproduce than a generic anomaly score. Learned detectors are then applied to modalities for which they have valid inputs. This ordering does not assume deterministic findings are more consequential; it prioritizes auditability.

### 4.4 Critic pass

Every FLAG is subjected to an explicit critic step that checks extraction, detector assumptions, rounding, alternate denominators, legitimate reuse, and other benign explanations. Model-based findings also record calibration evidence when available.

### 4.5 Evidence graph

Findings become nodes connected by relations such as corroborates, contradicts, depends_on, same_source_as, same_claim_as, and cross_document_match. Detectors that react to the same underlying value are not counted as independent corroboration.

The default review-priority rule is intentionally transparent. Two independent detector families with reproducible E1–E3 findings may yield HIGH review priority; one such family yields MODERATE; multiple independent E4 families can yield MODERATE; E5-only evidence yields at most LOW. Review priority is explicitly not a probability of fraud.

## 5. Benchmark design

### 5.1 Why issue-level ground truth

A manuscript may contain multiple problems, and a single post-publication status may summarize very different mechanisms. Ground truth is therefore attached to issues rather than assigning every affected paper one positive binary label.

Ground-truth tiers are:

- **GT-A:** an official notice explicitly identifies the issue;
- **GT-B:** a correction or corrigendum explicitly documents the error;
- **GT-C:** an institutional or journal investigation documents the issue;
- **GT-D:** a reproducible public forensic finding without official adjudication, used exploratorily;
- **GT-E:** suspicion or commentary only, not treated as positive confirmatory ground truth.

### 5.2 Benchmark strata

The benchmark contains three major strata.

**P — officially documented problem cases.** Retractions, expressions of concern, or other primary records with issue-specific coding.

**E — known-error/correction cases.** Corrections, corrigenda, coding errors, and reporting mistakes. This stratum is essential because a useful forensic detector should be able to flag a real inconsistency without converting the existence of an error into a misconduct claim.

**C — no-known-integrity-concern comparators.** Papers matched on publication period, field, article type, venue where feasible, accessibility, and broad manuscript characteristics. These are never described as “confirmed clean.”

### 5.3 Track A: time-safe content-only evaluation

Track A asks a counterfactual operational question: what could have been detected from the manuscript and contemporaneously available scientific artifacts before the later integrity outcome?

Excluded from model-visible inputs are outcome-defining notice text, retraction status, Retraction Watch record identifiers, current status markers, and similar leakage. Current target-paper metadata is also not automatically trusted, because bibliographic services may update titles and metadata after retraction. Historical-equivalent content must pass a safety preflight.

A critical consequence follows: not every officially documented issue is eligible for Track A. Manipulated peer review, for example, may be established by editorial evidence but be invisible in manuscript content. This is not counted as a content-detector failure. Instead, detector eligibility is reported separately from overall coverage.

### 5.4 Track B: open-world triage

Track B evaluates practical integrity review. It can use Crossref/Retraction Watch updates, publisher notices, related-publication history, corpus networks, registration histories, and other public post-publication evidence. Track B is a workflow evaluation rather than a pure prediction problem and is not interpreted as directly comparable to Track A.

### 5.5 Data sources and provenance

Crossref acquired the Retraction Watch database in 2023 and exposes it through production services, including update relations with publisher or Retraction Watch sources [13]. The same retraction event can appear from more than one assertion source. Benchmark ingestion therefore preserves assertion provenance before collapsing records to event level.

Target-paper metadata is resolved independently from notice metadata. Retraction reason text is stored for adjudication but never exposed to Track A.

### 5.6 Leakage control

Random paper-level train/test splitting is insufficient for learned integrity detectors. Grouped splitting is required for:

- paper-mill template families;
- high-overlap text clusters;
- duplicated-image families;
- author/collaboration components when relevant;
- journal special-issue clusters;
- known batch retractions.

At least one temporal holdout is required. A learned detector trained on one member of a paper-mill template family must not be evaluated on a near-duplicate family member in a nominally independent test split.

### 5.7 Shortcut stress tests

A dedicated series of stress tests evaluates whether retraction classification depends on contextual proxies rather than issue evidence.

1. **Metadata-only ceiling:** estimate how much a binary label is predictable from year, field, venue, article type, length, references, figures, and similar context without integrity evidence.
2. **Strict matching:** re-evaluate after matching problem/error/comparator manuscripts on nuisance structure.
3. **Correction adversarial set:** test whether real errors are surfaced without unsupported misconduct language.
4. **Family-grouped split:** prevent template, image, author, and batch leakage.
5. **Temporal holdout:** train only on evidence available before a cutoff and test later outcomes.
6. **Style perturbation:** normalize formatting and test meaning-preserving edits for text-model stability.
7. **Evidence-only versus context-rich models:** compare direct evidence features with multimodal contextual classifiers.
8. **Reason-stratified evaluation:** measure which retraction reasons a model actually detects.
9. **Leave-context-out tests:** remove venue, affiliation, author strings, references, funding, or layout in planned diagnostic experiments.
10. **Negative controls:** permutation tests within matched strata.

Nationality, country, author-name origin, and institutional prestige are prohibited as operational suspicion features.

## 6. Outcomes and analysis

### 6.1 Primary outcome

The primary outcome is eligible issue-type recall at a prespecified mean false-alert burden.

For manuscript i, let E_i be its set of benchmark issues for which at least one preregistered detector is eligible, and D_i the corresponding detected issue set. Then issue recall for i is |E_i ∩ D_i| / |E_i|.

Both micro- and macro-averaged estimates will be reported with uncertainty intervals. Coverage is reported separately as the fraction of benchmark issue types for which at least one detector family can validly operate.

### 6.2 Secondary outcomes

Secondary measures include:

- false alerts per manuscript;
- precision and F1 as descriptive outcomes;
- calibration and Brier score for probabilistic modules;
- abstention rate;
- severe false-positive rate;
- human minutes per manuscript;
- human minutes per true issue surfaced;
- proportion of alerts resolved without author contact;
- inter-rater agreement;
- issue yield unique to each detector family.

A single ROC-AUC is not sufficient for the primary question because detectors differ in applicability, issue families differ, and workflow burden matters.

### 6.3 Baselines

Planned baselines include:

- statcheck-like inference consistency;
- GRIM/GRIMMER/SPRITE/DEBIT family where applicable;
- citation verification alone;
- text/paper-mill model alone;
- image screening alone;
- LLM-only manuscript review with a frozen prompt;
- simple unweighted flag count;
- BMMDetect-like binary retraction classification;
- the full dependency-aware Research Forensics framework.

The purpose of the BMMDetect-like baseline is not to reproduce a proprietary or unavailable implementation exactly, but to test the general retracted-versus-control paradigm under the same leakage controls.

### 6.4 Ablation and complementarity

For each detector family f, leave-one-family-out analysis estimates:

Delta_f = Metric(full framework) − Metric(full framework without f).

We will report changes in issue recall, false-alert burden, review time, and unique issue yield. Pairwise overlap and UpSet-style analyses will show whether families provide independent evidence or repeatedly flag the same cases.

### 6.5 Human-review experiment

A stratified sample will be independently reviewed under conditions such as:

- manuscript only;
- manuscript plus structured Research Forensics report;
- manuscript plus LLM-only review, where feasible.

Reviewers will record issues found, time, accepted/rejected alerts, confidence, and next actions. Order will be randomized or counterbalanced to limit learning carry-over. At least two reviewers will independently code a subset, with disagreements preserved for agreement statistics before adjudication.

## 7. Design-validation audit

Before scaling the benchmark, we ran a small source-anatomy audit against live Crossref production metadata and three official retraction records. This phase was intended to test data architecture, not detector performance.

### 7.1 Assertion versus target-work ambiguity

Crossref update queries can return a separate retraction-notice work whose update relation points to the affected article. Other records use a self-relation. The same event can also contain publisher and Retraction Watch assertions. This required a two-level ingestion model: assertion provenance is preserved, while event identity is represented separately.

### 7.2 Current metadata is not necessarily time-safe

Crossref recommends reflecting retracted status in the original DOI metadata, including adding “RETRACTED:” to the article title [14]. Consequently, resolving an original DOI today can reveal a future outcome that would not have been visible when the paper was published. Track A therefore cannot use current metadata wholesale.

This is a general lesson for retrospective machine-learning studies: hiding a retraction-reason column does not make a data set leakage-free if the title, abstract, PDF, file path, update relations, or publisher banners have already been modified by the outcome.

### 7.3 Label heterogeneity in a three-record seed

The initial seed contains three intentionally heterogeneous records. One official notice described concerns about scientific accuracy and legitimacy without establishing a more specific issue type. A second explicitly described an illegal gift-authorship case [15]. A third attributed retraction to a compromised guest-edited editorial process and manipulated peer review.

The point is not the prevalence of these categories; three records cannot estimate prevalence. The point is structural: one binary “retracted” label collapses content-validity concerns, authorship problems, and editorial-process manipulation into a single target. It also mixes issues that may be visible in manuscript content with issues that may not be.

## 8. Detector versioning and defect governance

An integrated system inherits the failure modes of its components. Detector version and known defects are therefore part of evidence provenance.

This requirement is not hypothetical. At the time of this draft, the documentation for the scrutiny implementation of GRIMMER warns that one of its tests can generate false-positive results and advises users to interpret that component with care [16]. A framework that simply executes every available method and counts alerts would amplify such defects. Research Forensics therefore maintains a detector registry containing implementation version, evidence target, applicability constraints, known defects, calibration references, and whether a module is eligible for confirmatory use.

Detector updates after the confirmatory freeze require a new benchmark version or a prespecified bug-fix policy; they cannot silently alter test-set behavior.

## 9. Ethics, fairness, and governance

Integrity screening is a high-consequence setting because false accusations can harm researchers, while missed problems can contaminate the literature. The framework therefore adopts conservative language and evidence handling.

First, a flagged anomaly is reported as an anomaly. The system does not infer motive or mental state and does not label authors fraudulent. Second, nationality, country, name origin, and institutional prestige are not used as operational suspicion features. Third, learned text models are stress-tested for stylistic and language shortcuts. Fourth, publicly documented corrections are treated as a crucial control group because they demonstrate that genuine inconsistencies do not imply intent.

The distinction between detection and adjudication is also consistent with real editorial practice. In image screening, for example, the ASM pilot combined automated image-duplication tools with specialist human inspection, and most detected concerns were resolved rather than treated as automatic evidence of misconduct [6].

GenAI provenance requires additional caution. Watermarking can provide generator-specific provenance when assumptions hold [9], whereas generic post-hoc classifiers may react to academic style, editing, or domain and can be evaded by rewriting [10]. Moreover, AI assistance is governed by venue policy and disclosure expectations; its presence is not synonymous with research misconduct.

## 10. Reproducibility and open implementation

ARIS4C011 is implemented as both a research protocol and a reusable Agent Skills-compatible skill. The skill contains:

- a safety and provenance preflight;
- a detector contract with applicability and abstention;
- machine-readable finding and report schemas;
- a dependency-aware reference orchestrator;
- a detector version/defect registry;
- benchmark source and leakage documentation.

Benchmark releases will record extraction date, data-source version, inclusion and exclusion logic, label-schema version, split manifest hash, detector versions, and eligibility rules. The confirmatory test set will not be repeatedly optimized against.

## 11. Limitations

Several limitations are anticipated.

First, issue-level ground truth remains imperfect. Official notices vary in specificity, and absence of a notice does not prove absence of a problem. Second, some detector families require raw data, source images, registration records, or full text that may be unavailable. Third, even a time-safe historical manuscript may be difficult to reconstruct reliably for older literature. Fourth, dependency modeling among detectors is only an approximation; two nominally different models can share training data or latent features. Fifth, domain-specific checks may not transfer cleanly across fields. Sixth, corpus/network analysis can mistake normal collaboration or field-specific citation structure for suspicious clustering if confounding is poorly controlled.

Finally, this framework cannot automate institutional investigation. It is designed to improve triage, reproducibility of checks, and the quality of evidence handed to human reviewers.

## 12. Expected contribution

The project will be informative under more than one empirical outcome.

If the integrated framework substantially improves eligible issue recall at the same alert burden, it will quantify the value of combining genuinely complementary evidence. If most performance is captured by a small subset of deterministic checks, that would argue for simpler screening systems. If binary retraction classifiers collapse under strict matching and temporal/grouped evaluation while issue-level methods remain stable, the study will demonstrate the cost of shortcut-prone labels. If neither integrated nor single methods perform well, the result will establish empirical limits on automated research forensics and clarify where raw data or human investigation remain indispensable.

The intended contribution is therefore not a universal misconduct detector. It is a reproducible method for asking a more defensible question: given the artifacts legitimately available at a particular time, which integrity-relevant observations can be detected, how strong and independent are they, and how can they be presented so that a human reviewer can verify them without confusing anomaly with accusation?

## References

1. Nuijten MB, Polanin JR. “statcheck”: Automatically detect statistical reporting inconsistencies to increase reproducibility of meta-analyses. Research Synthesis Methods. 2020;11(5):574–579. doi:10.1002/jrsm.1408.
2. Brown NJL, Heathers JAJ. The GRIM Test: A Simple Technique Detects Numerous Anomalies in the Reporting of Results in Psychology. Social Psychological and Personality Science. 2017;8(4):363–369. doi:10.1177/1948550616673876.
3. Anaya J. The GRIMMER test: A method for testing the validity of reported measures of variability. PeerJ Preprints. 2016. doi:10.7287/peerj.preprints.2400v1.
4. Heathers JAJ, Anaya J, van der Zee T, Brown NJL. Recovering data from summary statistics: Sample Parameter Reconstruction via Iterative TEchniques (SPRITE). PeerJ Preprints. 2018. doi:10.7287/peerj.preprints.26968v1.
5. Heathers JAJ, Brown NJL. DEBIT: A Simple Consistency Test for Binary Data. OSF Preprints. 2019. https://osf.io/5vb3u/
6. Chaturvedi AP, Hibbard A, Nelson C, Casadevall A, Kullas AL. ASM incorporates Imagetwin to address image duplication and preserve scientific accuracy. mBio. 2025;16(10):e01990-25. doi:10.1128/mbio.01990-25.
7. Scancar B, Byrne JA, Causeur D, Barnett AG. Machine learning based screening of potential paper mill publications in cancer research: methodological and cross sectional study. BMJ. 2026;392:e087581. doi:10.1136/bmj-2025-087581.
8. Zhou Y, Zhang J, Wang M, Yu L. BMMDetect: A Multimodal Deep Learning Framework for Comprehensive Biomedical Misconduct Detection. arXiv:2505.05763. 2025.
9. Dathathri S, See A, Ghaisas S, et al. Scalable watermarking for identifying large language model outputs. Nature. 2024;634:818–823. doi:10.1038/s41586-024-08025-4.
10. Karr JA, Khvatskii G, Hua T, Chawla NV. Why AI Detection Fails for Academic Integrity. arXiv:2608.11256. 2026.
11. International Association of Scientific, Technical and Medical Publishers. STM Integrity Hub. https://stm-assoc.org/what-we-do/strategic-areas/research-integrity/integrity-hub/
12. INSPECT-SR: a tool for assessing trustworthiness of randomised controlled trials. PMC12424918. 2025/2026 version accessed 2026-09-18.
13. Crossref. Retraction Watch documentation. https://www.crossref.org/documentation/retrieve-metadata/retraction-watch/
14. Crossref. Version control, corrections, and retractions: best practices for post-publication updates. https://www.crossref.org/documentation/principles-practices/best-practices/versioning/
15. Iwamoto J, Takeda T, Sato Y. Retraction: Effect of Treadmill Exercise on Bone Mass in Female Rats. Experimental Animals. 2022;71(3):414. doi:10.1538/expanim.54.1.r1.
16. scrutiny documentation. GRIMMER test implementation and current false-positive warning. https://lhdjung.github.io/scrutiny/reference/grimmer.html
