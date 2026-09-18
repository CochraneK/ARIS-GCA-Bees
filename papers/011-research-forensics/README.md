# ARIS4C011 — Research Forensics

## Working title

**Research Forensics at Scale: An Auditable Multi-Evidence Framework for Scientific Integrity Screening**

## Core question

Can a modular, applicability-aware system combine independent statistical, numerical, textual, visual, citation, provenance, registration, metadata, and corpus-level signals to identify research-integrity concerns more comprehensively than single detectors, while preserving calibration, auditability, and a strict distinction between anomalies and allegations of misconduct?

## Why this is not "an AI fraud detector"

The project does **not** infer intent and does not classify authors as fraudulent. Its atomic output is an auditable finding:

- what was checked;
- whether the check was applicable;
- what evidence was observed;
- how reproducible the finding is;
- what alternative benign explanations remain;
- whether human review is required.

A mathematical inconsistency can be real while its cause is an honest reporting error. A model-derived anomaly can be useful for triage while being too weak for accusation. This distinction is a design invariant.

## Research gap

The ecosystem is rich in specialised checks: statcheck for NHST consistency; GRIM/GRIMMER/SPRITE/DEBIT and related numerical checks; image-duplication and manipulation screening; plagiarism and tortured-phrase/paper-mill signals; citation verification and citation-context checks; post-publication notices; trial registration and protocol consistency; and AI-origin/watermark signals.

Publisher infrastructures such as the STM Integrity Hub already demonstrate the value of orchestrating multiple screening tools. INSPECT-SR demonstrates the value of transparent, multi-domain trustworthiness checks for RCTs. The open research gap targeted here is a **cross-disciplinary, machine-executable, detector-applicability-aware, evidence-fusion framework with a benchmark designed to avoid label leakage and detector-family contamination**.

## Primary contributions

1. **Research-forensics taxonomy** spanning 10 detector families.
2. **Detector contract** that makes applicability and abstention first-class outputs.
3. **Evidence graph** that separates observations from interpretations and intent.
4. **Two-track benchmark**:
   - Track A: content-only blind screening;
   - Track B: open-world integrity triage.
5. **Issue-level evaluation** rather than only paper-level classification.
6. **Detector-family ablation** to estimate independent information contribution.
7. **Fairness and shortcut audit**, especially for language and geography proxies.
8. **Human-review burden analysis**: alerts per manuscript and minutes per true issue.

## Primary estimand

The primary outcome is **eligible issue-type recall at a fixed false-alert burden**, not "fraud accuracy".

For manuscript i with eligible issue set E_i and detected issue set D_i:

```
issue_recall_i = |E_i ∩ D_i| / |E_i|
```

Aggregate reporting will include micro and macro averages and confidence intervals.

## Strong design rules

- No country, nationality, language background, or institutional prestige is allowed as a direct suspicion feature.
- A detector that is not applicable must return **ABSTAIN / NOT_APPLICABLE**, not PASS.
- Post-publication notices cannot be used in the primary content-only benchmark when those notices define the labels.
- Papers without known integrity notices are **no-known-concern comparators**, never "confirmed clean".
- Retraction is not synonymous with misconduct; reasons are coded separately.
- AI-origin scores and Benford-like heuristics are weak/context-dependent evidence unless their assumptions are satisfied.
- No single detector output may be converted into an allegation of misconduct.

## Current state

**DESIGN / BENCHMARK SPECIFICATION LOCKED.**

The immediate next phase is Benchmark v0 construction and a deterministic Pilot 0 using statistics and metadata checks before any learned evidence-fusion model is trained.
