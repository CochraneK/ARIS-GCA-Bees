# Detector contract

## Goal

A detector is a bounded scientific check, not an accusation engine.

Each detector must expose two logically separate operations:

1. applicability(context): determine whether the method is valid for this artifact and claim;
2. run(context): execute only after applicability succeeds.

## Required finding fields

- finding_id
- detector_id
- detector_version
- family
- applicable
- applicability_reason
- status: FLAG, PASS, ABSTAIN, or ERROR
- evidence_class: E0 through E5
- claim
- source_locator
- evidence
- reproducible
- confidence, optional
- calibration_reference, optional
- benign_explanations
- dependency_group
- misconduct_inference, always false at detector level

## Applicability examples

### GRIM-like checks

Applicable only when:
- the reported statistic is a mean of integer-valued observations or an explicitly supported discrete score;
- the relevant denominator N is known;
- rounding precision is known or conservatively modeled.

Composite scale averages, weighted scores, imputed values, or uncertain denominators can invalidate a naive GRIM application.

### statcheck-like checks

Applicable only when enough elements of a supported NHST result are reported. Account for:
- one- vs two-sided tests;
- corrected p values;
- Greenhouse-Geisser/Huynh-Feldt or other df adjustments;
- rounding;
- nonstandard distributions.

### Benford / digit tests

Applicable only when the generative conditions make the proposed reference distribution plausible. Do not use as a universal fraud screen.

### Citation checks

Separate:
- reference existence;
- bibliographic metadata mismatch;
- cited work retraction/correction status;
- whether a citation context semantically supports a claim;
- citation-network anomalies.

A later retraction of a cited work does not by itself imply wrongdoing by the citing paper.

### Image checks

Separate:
- duplicate-region detection;
- cross-paper reuse;
- transformations such as rotation/mirror/crop;
- splice/manipulation inference;
- whether reuse was disclosed or legitimate.

### AI provenance

A generic classifier score is not proof of AI use. AI use is not itself misconduct. Venue policy, disclosure requirements, calibration, and transformation robustness all matter.

## Dependency groups

Findings must identify shared underlying evidence where possible.

Examples:
- an LLM and statcheck both notice the same p-value mismatch: one dependency group;
- two perceptual-hash algorithms flag the same image pair: probably correlated;
- an image duplication and an independent impossible sample-size arithmetic check: separate groups.

Review-priority logic must count independent families/dependency groups, not raw flag count.

## Failure handling

Use:
- ABSTAIN when required information or assumptions are missing;
- ERROR when execution fails;
- PASS only when a valid applicable check was actually executed and did not flag.

Never convert ABSTAIN or ERROR into PASS.

## Human review handoff

For a FLAG include a concrete next action, such as:
- recalculate from the original table;
- inspect a named figure pair;
- retrieve the cited DOI;
- compare registry timestamp with enrollment date;
- request raw/source image;
- clarify analysis population N.

The detector should make verification easier, not replace adjudication.
