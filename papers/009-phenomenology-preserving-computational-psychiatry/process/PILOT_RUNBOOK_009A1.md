# ARIS4C009A1 · Pilot-0 runbook using DAIS-C

## Objective

Test whether the 009A1 measurement system is operational on real schizophrenia interview material before seeking a richer phenomenological cohort.

Pilot-0 is a **methods calibration**, not a clinical inference study.

## Stage 0 · Source integrity

Record:

- source repository;
- DOI;
- retrieval date;
- archive SHA-256;
- file count;
- extension/type distribution;
- transcript-like file count;
- aggregate text volume.

Do not commit raw source text.

## Stage 1 · Corpus eligibility

A candidate interview enters the pilot only if:

- participant/interviewer turns are recoverable;
- the transcript contains enough natural-language material for source-grounded questions;
- provenance can be mapped to a stable file/span;
- severe formatting damage does not prevent interpretation.

Do not exclude clinically unusual speech because it is difficult.

## Stage 2 · Episode segmentation

The unit of analysis is not automatically the entire interview.

Create focal episodes using a frozen procedure.

Candidate episode boundary:

- one interviewer prompt/topic initiation;
- the participant's connected response;
- directly relevant interviewer clarification;
- participant clarification/continuation.

An episode ends when the topic clearly changes or a preregistered maximum context window is reached.

### Pilot comparison

Test at least two segmentation strategies on calibration-only material:

1. interaction-turn episode;
2. fixed-context-window episode.

Choose the rule before confirmatory Pilot-0 scoring.

## Stage 3 · Source adjudication

Two independent source raters create:

- entities;
- relations;
- temporal/context qualifiers;
- uncertainty;
- literal/metaphoric status where inferable;
- admissible answers to benchmark queries.

Every claim retains provenance.

Disagreement states:

- agreement;
- resolvable disagreement;
- legitimate ambiguity;
- not answerable.

Legitimate ambiguity is not forced into consensus.

## Stage 4 · Query construction

Panel A sees source only.

Build a balanced query bank across:

- domain-general semantics;
- relations;
- context;
- temporal structure;
- clinically conventional information;
- phenomenology-informed distinctions where the source actually supports them.

Because DAIS-C was not designed as an EASE interview, do not manufacture self-disorder questions when the source does not support them.

## Stage 5 · Representation construction

From the same source episode generate:

### R0 · source reference

Full eligible episode.

### R1 · episode graph

Structured entities/relations/modifiers with provenance removed from evaluator view but retained internally.

### R2-lite · phenomenology-informed structured code

For Pilot-0 only, use the subset of the relation ontology supportable from DAIS-C.

Do **not** call this an EASE score.

### R3P · questionnaire-format projection

Map source evidence to a frozen fixed-response format.

This is a projection, not participant self-report.

### R4P · conventional symptom-style projection

Map source evidence to a frozen coarse clinical description where justified.

This is not a diagnosis.

### R5 · compact representation

Apply a frozen representation budget/summary rule.

## Stage 6 · Blinded reconstruction

Panel C:

- sees one representation only;
- never sees another representation of the same episode;
- answers frozen questions;
- may abstain;
- reports confidence.

Use balanced incomplete-block assignment.

## Stage 7 · Pilot metrics

Primary engineering outputs:

- answerable-query yield per episode;
- source-adjudication agreement;
- relation-rater F1;
- query redundancy;
- evaluator variance;
- semantic reconstruction fidelity;
- relation F1;
- context/temporal recovery where available;
- representation rate;
- coder/evaluator time.

## Stage 8 · Anti-overclaim gate

Pilot-0 may support:

> The benchmark can/cannot be applied reliably to naturalistic schizophrenia interview material.

It may not support:

> EASE is superior/inferior.

> schizophrenia phenomenology is fully captured.

> this representation predicts clinical outcome.

> the method reconstructs the participant's true inner state.

## Stage 9 · Go/no-go criteria

### GO to larger Pilot-1 if

- source material yields a useful number of adjudicable episodes;
- query-bank construction is feasible;
- core annotation reliability is acceptable after calibration;
- representation conditions can be generated without systematic source leakage;
- evaluator blinding works;
- rate/burden metrics are measurable.

### REVISE if

- relation ontology cannot be applied reliably;
- query bank is dominated by one theoretical vocabulary;
- most candidate queries are unanswerable;
- transcript format prevents stable provenance;
- R3P/R4P rules require uncontrolled subjective invention.

### STOP DAIS-C as A1 substrate if

- its interview content is too far from the intended phenomenological constructs for meaningful reconstruction testing.

Stopping DAIS-C does not falsify 009; it means the corpus is unsuitable.

## Stage 10 · Privacy/publication

Only publish:

- aggregate corpus inventory;
- aggregate reliability/fidelity results;
- source identifiers already intended for public scholarly use when necessary;
- analysis code.

Do not publish raw transcript passages in generated artifacts by default.
