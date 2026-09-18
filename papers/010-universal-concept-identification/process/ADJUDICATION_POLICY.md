# ARIS4C010 · Annotation Adjudication Policy

Human semantic judgments may legitimately disagree. UCID therefore separates **measurement stability** from **gold adjudication**.

## Never use raw majority vote as automatic gold

A modal response is descriptive. It becomes a benchmark label only after the maturity gate appropriate to that item.

## Automatic triage

The repository includes `triage_human_annotations.py`.

Default review flags are deliberately provisional:

- fewer than 6 valid ratings for a protocol × pair cell;
- modal response proportion below 0.70;
- response entropy above 1.20 bits.

These thresholds are queueing rules, not scientific universal constants, and should be frozen before confirmatory calibration data are inspected.

## Stable-for-next-gate

A pair that passes automatic triage may advance to:
- provenance review;
- wording/context review;
- cross-protocol comparison;
- retest review.

It does **not** automatically become `adjudicated_gold`.

## Review queue

High-disagreement pairs can receive:

1. additional independent ratings;
2. wording repair followed by recollection, with version bump;
3. expert/theory review;
4. preservation as a probabilistic response distribution;
5. exclusion from crisp-label analyses while remaining in uncertainty analyses.

## Special treatment

Vagueness, semantic paradox, fiction, phenomenal access and inconsistent-information cases should not be penalized merely for having higher entropy. For these strata, disagreement may be part of the phenomenon.

The benchmark should therefore publish both:
- adjudicated operational labels where justified;
- empirical response distributions.
