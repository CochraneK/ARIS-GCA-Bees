# ADJUDICATION PROTOCOL — ARIS4C005 Pilot B

## Purpose

Create an article-level reference standard for **scientific reliability/materiality**, not a public accusation list of researchers.

The adjudication layer exists to calibrate detectors and estimate article-level severe-failure prevalence. It must remain conceptually separate from person-level intent, guilt, sanctions, or reputation.

---

## Unit of adjudication

Primary unit: one target-universe scholarly work.

Where a formal notice exists, the reviewer may inspect:

- original article;
- correction/retraction/expression-of-concern notice;
- linked investigation/finding when public and authoritative;
- supplementary material;
- registry/protocol where directly relevant;
- post-publication evidence used only as documented evidence, not as automatic truth.

A citation, comment, or detector flag alone is never sufficient to infer misconduct.

---

## Blinding

Reviewers should not see:

- composite model risk score;
- latent-model posterior;
- the sampling stratum label when avoidable;
- other reviewers' labels before independent coding.

A reviewer may see a formal notice when that notice is required to assess the scientific state.

---

## Primary scientific-state label

Exactly one:

1. **SEVERE_SUPPORTED** — Strong evidence that at least one material scientific claim is unreliable because of fabrication/falsification, invalid data/results, or another severe integrity failure.
2. **SERIOUS_UNRESOLVED** — Serious concern exists, but available evidence is insufficient to conclude that a material scientific claim is unreliable.
3. **HONEST_MAJOR_ERROR** — A major scientific error materially undermines the work, with no evidence sufficient to classify it as misconduct. This is E3, not E1-M.
4. **MINOR_OR_IMMATERIAL** — Confirmed issue exists but does not materially affect the scientific claim used for the primary prevalence estimand.
5. **NO_MATERIAL_PROBLEM_FOUND** — No material scientific reliability problem established from the reviewed evidence.
6. **INDETERMINATE** — Evidence/access is too incomplete or contradictory to adjudicate.

The confirmatory binary reference standard uses `SEVERE_SUPPORTED` as positive; `HONEST_MAJOR_ERROR`, `MINOR_OR_IMMATERIAL`, and `NO_MATERIAL_PROBLEM_FOUND` as negative; and retains `SERIOUS_UNRESOLVED`/`INDETERMINATE` outside the binary detector-metric denominator.

This binary coding is for the **severe integrity failure estimand**, not a moral judgment.

---

## Separate intent / process fields

Scientific reliability and misconduct intent are different axes.

### misconduct_evidence

One of:

- `FORMAL_FINDING`
- `STRONG_DOCUMENTED_EVIDENCE`
- `SUSPECTED_NOT_ESTABLISHED`
- `NO_EVIDENCE_OF_MISCONDUCT`
- `NOT_ASSESSABLE`

### publication_process_state

One or more:

- `PAPER_MILL_SIGNAL`
- `COMPROMISED_PEER_REVIEW`
- `AUTHORSHIP_AFFILIATION_MANIPULATION`
- `PLAGIARISM_DUPLICATION`
- `OTHER_PROCESS_FAILURE`
- `NO_PROCESS_FAILURE_ESTABLISHED`
- `NOT_ASSESSABLE`

A paper can have publication-process misconduct without the adjudicator being able to show that its substantive scientific result is false.

---

## Materiality test

A problem is material when a reasonable downstream user would need to change at least one of:

- whether the main result should be believed;
- the estimated magnitude/direction of a key effect;
- whether the method/data can be reused;
- whether the work should enter evidence synthesis;
- a major conclusion derived from the work.

Record materiality separately as `MATERIAL`, `POTENTIALLY_MATERIAL`, `IMMATERIAL`, or `NOT_ASSESSABLE`.

---

## Evidence hierarchy for adjudication

Highest weight:

1. formal institutional/ORI-equivalent finding;
2. publisher correction/retraction notice with explicit evidence;
3. raw/supplementary evidence that independently demonstrates the problem;
4. validated specialist forensic assessment with reproducible evidence;
5. replicated statistical/technical impossibility check.

Context only unless independently verified:

- anonymous allegation;
- social-media claim;
- detector score;
- country/journal/researcher reputation;
- citation count;
- language/writing style.

---

## Reviewer workflow

1. Confirm work identity/DOI and version.
2. Record accessible evidence sources.
3. Describe the alleged/observed issue without assigning intent.
4. Decide whether a material scientific claim is affected.
5. Assign `scientific_state`.
6. Separately assign `misconduct_evidence`.
7. Separately assign `publication_process_state`.
8. Record confidence: `HIGH`, `MEDIUM`, `LOW`.
9. Record a short evidence rationale and exact locator where possible.
10. Submit independently.

---

## Double coding / adjudication

Mandatory double coding:

- every candidate initially labelled `SEVERE_SUPPORTED`;
- every disagreement on `scientific_state`;
- every case with `FORMAL_FINDING`;
- all cases used to validate a new detector family;
- random >=20% of the remaining sample where resources permit.

Adjudication by a third reviewer or consensus panel must preserve both original labels.

Report raw agreement, confusion matrix, Cohen's kappa for the six-state label where informative, binary severe/not-severe agreement, and frequency of unresolved/indeterminate cases. Kappa is descriptive and must not replace substantive disagreement review.

---

## Missingness

Do not silently drop inaccessible papers. Record full-text availability, notice availability, supplementary-data availability, detector applicability, and reason for non-adjudication.

`INDETERMINATE` and access failure are analysis variables because missingness may be informative.

---

## Safety / fairness constraints

Do not:

- infer misconduct from nationality, institution, language, journal, or coauthor network alone;
- publicly name unretracted authors based only on model flags;
- translate article-level severe-failure probability into person-level guilt;
- use region as a detector feature in the primary model;
- let known Retraction Watch reason labels leak into a supposedly blinded detector validation unless that detector is the object being calibrated.

Country/region may be used later for heterogeneity analysis with detection/governance adjustment, not as a suspicion prior.

---

## Pilot B gate

Proceed to the latent prevalence model only when:

- at least 100 resolved adjudications come from the population-random component for the engineering dry-run gate;
- at least one detector has estimable sensitivity and specificity;
- unresolved/indeterminate share is reported;
- design weights/inclusion probabilities pass audit;
- the population-random estimate and detector-enriched calibration do not show obvious irreconcilable spectrum bias.

The final publication gate is stricter than this engineering threshold.
