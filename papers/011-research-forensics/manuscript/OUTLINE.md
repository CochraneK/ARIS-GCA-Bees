# Manuscript outline

## Title
Research Forensics at Scale: An Auditable Multi-Evidence Framework for Scientific Integrity Screening

## Abstract structure
Background — integrity screening is fragmented across specialised methods and publisher workflows.  
Objective — test whether applicability-aware multi-evidence screening improves issue coverage and review efficiency.  
Methods — two-track benchmark, detector contracts, evidence graph, matched correction/problem/comparator strata, grouped/temporal splits, detector ablation, human review study.  
Results — reserved until Benchmark v1.  
Conclusion — reserved until confirmatory analysis.

## 1. Introduction

1. Scientific publishing now faces heterogeneous integrity threats and heterogeneous honest errors.
2. Specialised detectors are useful but narrow.
3. Publisher orchestration exists, so "combining tools" alone is not novel.
4. Existing trustworthiness frameworks demonstrate the importance of transparent checks and human judgement.
5. Missing methodological layer: open applicability-aware benchmarking and evidence fusion across detector families.
6. Research questions and hypotheses.

## 2. Related work

2.1 Statistical and numerical forensics  
2.2 Image integrity  
2.3 Text reuse, tortured phrases, paper mills  
2.4 Citation integrity  
2.5 Registration/provenance checks  
2.6 GenAI provenance and watermarking  
2.7 Publisher integrity hubs and trustworthiness checklists

## 3. Framework

3.1 Manuscript decomposition  
3.2 Detector router and applicability gate  
3.3 Detector contract  
3.4 Evidence classes  
3.5 Evidence graph  
3.6 Human-facing report  
3.7 Safety: anomaly != misconduct

## 4. Benchmark

4.1 Data sources  
4.2 Ground-truth tiers  
4.3 Problem/correction/comparator strata  
4.4 Track A and Track B  
4.5 Leakage control and temporal split  
4.6 Fairness audit  
4.7 Metrics

## 5. Experiments

E1: detector-family baseline tournament  
E2: integrated framework  
E3: leave-one-family-out ablation  
E4: evidence-overlap/complementarity analysis  
E5: LLM-only comparison  
E6: human review burden experiment  
E7: robustness/fairness tests  
E8: calibration and abstention

## 6. Results
Reserved.

## 7. Discussion

- Which families provide unique information?
- Where do deterministic checks outperform learned methods?
- Which issues remain inaccessible without raw data?
- How much review time is saved or added?
- What kinds of false alerts dominate?
- How should publishers/reviewers interpret weak AI-provenance signals?
- Generalisation limits.

## 8. Ethics and governance

- No automated misconduct accusations.
- Reproducible evidence traces.
- Care with public naming and false positives.
- Dataset rights and privacy.
- Bias and geography/language shortcut prohibition.

## 9. Reproducibility

- versioned benchmark manifests;
- detector versions/hashes;
- frozen splits;
- open schemas;
- deterministic unit tests;
- full provenance log.
