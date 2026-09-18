# Evidence model

## Principle

The system stores **observations**, **constraints**, and **relationships**. It does not store an automated conclusion that an author committed misconduct.

## Finding node

Required fields:

- finding_id
- paper_id
- detector_id
- detector_version
- family
- applicable
- applicability_reason
- status: FLAG / PASS / ABSTAIN / ERROR
- evidence_class: E0..E5
- source_locator: page/table/figure/reference/span
- claim
- machine_readable_evidence
- reproducible: yes/no/unknown
- confidence: optional
- calibration_reference: optional
- benign_explanations
- misconduct_inference: always false at detector level

## Evidence graph

Node types:
- paper
- claim
- statistic
- table cell
- figure/panel
- image fingerprint
- citation
- DOI/work
- author identifier
- registration
- protocol
- dataset/code object
- detector finding

Edge types:
- supports
- contradicts
- corroborates
- depends_on
- derived_from
- cites
- matches
- same_source_as
- same_cluster_as
- supersedes

## Independence

Evidence accumulation must discount duplicated information.

Examples:
- statcheck and an LLM both noticing the same wrong p value are not two independent findings;
- two image detectors using the same perceptual hash family may be correlated;
- a paper-mill classifier and tortured-phrase detector may share textual features.

Each finding therefore carries a dependency group.

## Review priority

Pilot rules may use transparent heuristics such as:
- deterministic contradiction + independent corroborating family -> high priority;
- >=2 independent E1–E3 families -> high priority;
- one E1/E2/E3 finding -> moderate priority;
- only E4/E5 findings -> low/moderate depending on calibration;
- E5 alone can never create high priority.

Final models, if learned, predict **review yield / issue discovery**, not fraud or intent.

## Why no naive sum

A simple sum assumes equal validity and independence, neither of which holds. The benchmark will test whether evidence-graph features improve triage over:
- count of flags;
- max detector score;
- single best detector;
- LLM-only synthesis.

## Human-facing report

Every alert must be answerable with:
1. What exactly triggered?
2. Was the detector applicable?
3. Can a reviewer reproduce it?
4. What benign explanations are plausible?
5. What source location should be inspected?
6. Does another independent family corroborate it?
7. What should the reviewer verify next?
