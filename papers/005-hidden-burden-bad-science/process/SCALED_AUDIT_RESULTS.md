# SCALED RANDOM AUDIT RESULTS — ARIS4C005

**Date:** 2026-09-18
**Classification:** probability-traceable confirmatory sampling infrastructure; **not adjudication results**

## Confirmatory target universe

Live OpenAlex definition:

`core + article|review + publication years 2000–2025`

Current live partitioned denominator:

**137,436,109 works**

Earlier Pilot A whole-window query returned **137,445,874** under the same semantic definition. The difference is **-9,765 works (-0.0071%)**, consistent with a live bibliographic database changing between retrievals.

### Rule

Do not overwrite one count with the other or pretend the denominator is immutable. Every final result must pin:

- query semantics;
- retrieval timestamp;
- OpenAlex corpus mode;
- API/source version when exposed;
- the exact denominator used for weighting.

Database snapshot drift is part of denominator uncertainty/provenance.

---

## Realized random audit

Target sample: **10,000 works**

Realized unique sample: **10,000 works**

Sampling is stratified by publication period. Each row stores its exact first-order inclusion probability and design weight.

| stratum | population N | sample n | inclusion probability | design weight |
|---|---:|---:|---:|---:|
| 2000–2004 | 15,767,429 | 1,459 | 0.0000925325 | 10,807.01 |
| 2005–2009 | 22,538,013 | 1,656 | 0.0000734759 | 13,609.91 |
| 2010–2014 | 29,906,848 | 1,871 | 0.0000625609 | 15,984.42 |
| 2015–2019 | 31,791,658 | 1,925 | 0.0000605505 | 16,515.15 |
| 2020–2024 | 30,282,727 | 1,881 | 0.0000621146 | 16,099.27 |
| 2025 | 7,149,434 | 1,208 | 0.0001689644 | 5,918.41 |

The 2025 stratum is deliberately oversampled relative to population size so the most recent complete publication year is not swamped by earlier years. Weighted inference is therefore mandatory.

---

## Realized broad-domain composition

- Physical Sciences: **3,862**
- Social Sciences: **2,692**
- Health Sciences: **2,140**
- Life Sciences: **1,208**
- OpenAlex primary-domain missing: **98**

These are realized sample counts, not target-universe shares and not integrity rates.

---

## DOI coverage

Among 10,000 randomly sampled target-universe works:

**3,747 lack a DOI in the sampled OpenAlex metadata.**

Therefore **37.47%** of this realized random audit would be lost under a DOI-required inclusion rule.

This reinforces the Pilot B finding that OpenAlex ID must remain a first-class identifier and that detector applicability/missingness must be modeled rather than treating no-DOI works as negative integrity cases.

---

## Dual-AI adjudication packet

Every sampled work is assigned independently to:

- `AI_A` — 10,000 assignments
- `AI_B` — 10,000 assignments

Total:

**20,000 blinded AI assignments**

Batch size: **250 assignments**

Total batches: **80**

- 40 batches for AI_A
- 40 batches for AI_B

Reviewer-facing packets do not contain detector enrichment, model risk scores, or another adjudicator's answer.

---

## Workflow provenance

Main workflow run:

`ARIS4C005 scaled AI audit`

Run ID: `35301945169`

Main merge commit: `d3c113752a6b395b8ecd0cf3ec4c0ea4c052d290`

Private row-level artifact:

- artifact name: `aris4c005-scaled-ai-audit`
- artifact ID: `10529404069`
- digest: `sha256:065230382d1f69f98ebb4ce189158c93a5b00f5e3ac2f46aa877bd51587af699`
- workflow retention expiry: 2026-10-18

The public repository stores only aggregate summaries and the batch manifest. Row-level random works, manager linkage and AI input batches remain workflow artifacts.

---

## What is now ready

The project no longer needs to design a future random audit. The confirmatory sampling frame already exists.

Next empirical transformation:

`10,000 sampled works -> dual AI labels -> disagreement arbitration -> calibrated measurement-error model -> weighted latent prevalence`

No prevalence number is authorized before those downstream stages.
