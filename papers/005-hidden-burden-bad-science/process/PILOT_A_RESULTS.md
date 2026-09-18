# PILOT A RESULTS — ARIS4C005

**Date:** 2026-09-18  
**Classification:** empirical public-data pilot; **not latent prevalence**

## Question

Can the project construct a versioned scholarly denominator and a formal-correction lower bound without conflating database records, correction events, unique papers, and misconduct?

## A1. OpenAlex target universe

Frozen API target:

- corpus: `core`
- types: `article|review`
- publication years: `2000–2025`

Observed metadata count:

**137,445,874 works**

The annual series is committed in:

`data/pilot/openalex_universe_counts.csv`

and the exact query/retrieval metadata in:

`data/pilot/openalex_universe_provenance.json`

### Interpretation

This is the primary ARIS4C005 bibliographic target-universe definition, not a claim that exactly 137.4 million scientific papers exist in reality.

Coverage, type assignment, indexing change, duplicate/merged records, DOI coverage, and database-version effects remain denominator sensitivities.

---

## A2. Retraction Watch correction-event snapshot

Pinned source repository commit:

`448a0ed262c6348dd6f06ac03f5602bae4ef2d01`

Observed snapshot:

- **72,577** correction/event rows;
- **63,434** unique resolvable original-paper DOIs;
- **6,110** rows without a resolvable original DOI;
- **3,033** duplicate original-DOI event rows after normalization.

Nature at event-row level:

- Retraction: 67,013
- Expression of concern: 3,718
- Correction: 1,522
- Reinstatement: 160
- Unknown: 164

Unique original DOIs with at least one nature label:

- Retraction: **60,971**
- Expression of concern: **3,378**
- Correction: **1,436**
- Reinstatement: **155**

The categories overlap when one work has multiple events/natures.

---

## A3. Conservative reason screening

Unique-original-DOI screening counts:

| screen | unique DOIs |
|---|---:|
| narrow E1-S auto | 2,020 |
| strong E1-M auto | 18,863 |
| strong E1-P auto | 20,417 |
| paper-mill signal | 11,706 |
| major-error E3 signal | 6,459 |
| manual scientific review | 31,113 |
| manual process review | 26,239 |
| manual review required | 47,869 |

These columns overlap and **must not be summed**.

They are screening features, not adjudicated article states.

---

## A4. What Pilot A falsified

Pilot A directly falsifies several tempting shortcuts.

### Shortcut 1

`Retraction Watch rows = retracted papers`

False: event rows exceed unique resolvable original-paper DOIs, and the data contain corrections, expressions of concern and reinstatements.

### Shortcut 2

`Retraction = fraud`

False by ontology and reason heterogeneity. Major error, process failure, plagiarism, formal misconduct, unreliable results and limited-information notices require different interpretation.

### Shortcut 3

`one reason label = one scientific state`

False: reasons are multi-label and many are context/process labels rather than evidence that a material scientific claim is false.

### Shortcut 4

`detected rate = prevalence`

False: detection is conditioned on scrutiny, governance, publisher/institution behavior, time to discovery, field, access and available detectors.

---

## A5. Engineering findings

The live run exposed and corrected three implementation hazards:

1. **case/label drift** in Retraction Watch reason vocabulary;
2. **event-row vs unique-work duplication**;
3. **lexical date ordering** incorrectly treating date strings as chronological values.

The production summary now:

- uses case-insensitive/current reason handling;
- reports both event-row and unique-DOI counts;
- parses dates chronologically.

Observed parsed correction-date range in the current snapshot:

**1927-04-01 to 2026-09-11**

---

## A6. Gate decision

**GO → Pilot B**

Reason:

- target denominator can be reproduced;
- correction snapshot can be pinned;
- reason data can be conservatively transformed into screening variables;
- detected events can be separated from unique works;
- the remaining scientific question is genuinely a measurement/calibration problem rather than a metadata-feasibility problem.

Pilot A does **not** authorize a global hidden-failure estimate.

---

## A7. Next valid inference

Pilot B must combine:

1. a population-random sample from the frozen target universe;
2. detector/signal-enriched sampling;
3. exact inclusion probabilities;
4. blinded manual adjudication;
5. detector sensitivity/specificity and missingness calibration.

Only then can Pilot C test whether a latent severe-failure prevalence is identifiable.
