---
name: research-forensics
description: Audits scientific manuscripts for research-integrity-relevant anomalies using applicability-aware statistical, numerical, table, image, citation, text, AI-provenance, methods-results, registration/provenance, and corpus/network checks. Use when reviewing a paper, DOI, manuscript, preprint, submission package, or corpus for reproducible integrity concerns. Produces evidence and review priorities, never an automated accusation of misconduct.
compatibility: Python 3.10+ for bundled reference orchestrator. Network access is optional but required for live DOI, registry, retraction, or citation verification.
metadata:
  author: CochraneK
  project: ARIS4C011
  version: "0.1.0"
---

# Research Forensics

## Purpose

Use this skill to perform an auditable research-integrity screen of a scientific manuscript or corpus.

The skill is designed for triage and evidence gathering. It does not determine author intent, guilt, fraud, or misconduct. A reproducible anomaly can arise from honest error, reporting conventions, extraction mistakes, legitimate reuse, or misconduct. Keep those possibilities separate.

## Core invariants

1. Never output a binary fraud/not-fraud verdict.
2. Never infer intent from an anomaly.
3. Every detector must decide applicability before interpreting an output.
4. NOT_APPLICABLE or insufficient evidence becomes ABSTAIN, not PASS.
5. Prefer deterministic/reproducible checks before learned or stylistic heuristics.
6. A weak AI-text detector, Benford deviation, stylometric anomaly, or generic LLM suspicion is not strong evidence by itself.
7. Preserve exact source locations and enough values to reproduce every flag.
8. Distinguish independent corroboration from repeated detection of the same underlying signal.
9. State plausible benign explanations for each flag.
10. Human review is required before any consequential conclusion.

## Modes

### Track A: time-safe content-only screening

Use when evaluating whether issues could have been detected from the manuscript itself before a later correction, expression of concern, or retraction.

Before any detector runs, verify that the artifact is time-safe:
- no retraction/correction banner added later;
- no title prefix such as RETRACTED, WITHDRAWN, or Expression of Concern;
- no outcome-defining status/reason metadata visible to detectors;
- no label-bearing file paths or filenames;
- no later corrected version substituted for the intended historical version.

If time safety cannot be established, mark Track A BLOCKED. The same item may still be eligible for Track B.

### Track B: open-world integrity triage

Use for practical review. Public post-publication notices, DOI relations, registration histories, related-paper evidence, and corpus/network information may be used if provenance is recorded.

### Ad hoc review

Use when the user wants an exploratory audit rather than benchmark-compatible evaluation. Apply the same evidence semantics and safety rules, but clearly mark unavailable checks.

## Workflow

### 1. Establish provenance and artifact safety

Record:
- artifact ID and version;
- DOI or other persistent identifier when available;
- source and retrieval date;
- whether the artifact is pre-outcome, current, corrected, or unknown;
- available modalities: body text, tables, figures, references, supplement, raw data, code, registration/protocol.

Do not silently mix versions.

### 2. Decompose the manuscript

Create structured objects for:
- sections and claims;
- sample sizes and analysis populations;
- reported test statistics, degrees of freedom, p values, confidence intervals, effect estimates;
- table cells and totals;
- figures/panels;
- references and in-text citation contexts;
- outcomes, exposures, variables, models, and methods;
- registration/ethics/data/code identifiers.

Keep source spans or page/table/figure locators.

### 3. Route only applicable detectors

Detector families:

F1 statistical-inference consistency  
F2 discrete-summary and numerical/distributional forensics  
F3 table and cross-section consistency  
F4 image/figure forensics  
F5 citation integrity  
F6 text reuse, tortured phrases, and paper-mill similarity  
F7 generative-AI provenance and watermark signals  
F8 methods-results-abstract coherence  
F9 registration, ethics, identifiers, provenance, and timeline consistency  
F10 corpus/network anomalies

Read references/DETECTOR_CONTRACT.md before implementing or wrapping a new detector.

### 4. Run deterministic checks first

Examples include:
- recomputing reported p values from test statistics and degrees of freedom;
- GRIM-family feasibility checks when data are integer-valued and assumptions hold;
- table denominator and percentage arithmetic;
- sample-size consistency;
- DOI existence and reference metadata matching;
- registry date and identifier validation.

A deterministic contradiction should still include rounding and scope caveats.

### 5. Run higher-inference checks second

Examples include:
- image-duplication or manipulation classifiers;
- semantic citation-support models;
- paper-mill/text-template classifiers;
- LLM-based methods-results consistency extraction;
- generic AI-text classifiers;
- cross-paper graph anomaly detection.

Record calibration evidence when a detector emits a probability.

### 6. Critic pass

For every FLAG:
- verify extraction against the source;
- test the detector's assumptions;
- list benign explanations;
- identify dependency on other findings;
- downgrade or withdraw findings that cannot be reproduced.

Do not count two detectors as independent evidence if they are reacting to the same extracted value or model feature.

### 7. Build the evidence graph

Use finding nodes plus relationships such as:
- corroborates;
- contradicts;
- depends_on;
- derived_from;
- same_claim_as;
- same_source_as;
- cross_document_match.

Do not naively sum all scores.

### 8. Assign review priority

Default transparent rule:
- HIGH: at least two independent detector families with reproducible E1-E3 flags;
- MODERATE: one E1-E3 family, or multiple independent calibrated E4 families;
- LOW: only weak/model-derived signals;
- NONE: no applicable flags;
- BLOCKED: required artifact/provenance safety failed for the requested mode.

E5 evidence alone must never produce HIGH priority.

Review priority is a triage priority, not a probability of misconduct.

### 9. Report coverage and abstention

Report:
- registered detector families;
- applicable families;
- executed families;
- abstained families and reasons;
- errors;
- artifact modalities that were unavailable.

"No issue found" must never imply "paper verified clean" when coverage is limited.

## Evidence classes

E0: metadata observation  
E1: deterministic contradiction under satisfied assumptions  
E2: externally verifiable provenance fact  
E3: high-specificity forensic match  
E4: model-derived anomaly  
E5: weak/context-dependent heuristic

Evidence class is not severity and is not a guilt scale.

## GenAI-specific rule

AI assistance is not itself research misconduct. Generic post-hoc AI detectors are usually weak provenance evidence and should default to E5 unless a specific detector has strong, task-relevant calibration. A verifiable generator-side watermark may be stronger only when generator, detector version, text length, and transformation assumptions are satisfied. Interpret any disclosure issue against the relevant journal/institution policy.

## Distribution-forensics rule

Do not run Benford/Newcomb or terminal-digit tests merely because a table contains numbers. First justify the expected data-generating distribution. If assumptions are weak, mark the detector NOT_APPLICABLE or E5.

## Output

Return a structured report compatible with assets/report.schema.json. Each finding should be compatible with assets/finding.schema.json.

The human-readable summary should answer:
- What exactly triggered?
- Where is it in the source?
- Was the check applicable?
- Can it be reproduced?
- What benign explanations remain?
- Is there independent corroboration?
- What should a reviewer verify next?
- What could not be checked?

## Bundled resources

- references/DETECTOR_CONTRACT.md — detector interface, applicability, evidence semantics, and failure modes.
- assets/finding.schema.json — machine-readable finding schema.
- assets/report.schema.json — machine-readable report schema.
- scripts/orchestrator.py — dependency-free reference orchestrator and priority logic.
