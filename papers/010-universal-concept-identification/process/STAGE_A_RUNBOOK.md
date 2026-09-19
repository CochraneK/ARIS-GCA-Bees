# ARIS4C010 · Stage-A Human Calibration Runbook

**Status:** execution-ready protocol shell; institution/platform-specific ethics and recruitment fields remain to be completed before real data collection.

## Scientific purpose

Stage A is a **measurement-feasibility study**, not the final confirmatory test of the ontology.

It asks whether the three response protocols can generate reproducible semantic judgments:

- P2 — YES / NO
- P3 — YES / NO / MAYBE
- P6 — YES / NO / BORDERLINE / UNKNOWN / UNDEFINED / BOTH

The key mechanistic contrast is P3 → P6.

## Before any participant is run

Complete and freeze:

- ethics approval / exemption / institutional determination as applicable;
- participant-information and consent wording;
- eligibility criteria;
- English-language proficiency criterion;
- recruitment platform or laboratory procedure;
- compensation;
- expected session duration;
- device/browser requirements;
- approved data-transfer/storage path;
- pre-specified exclusion/quality rules;
- Stage-A stopping/precision plan;
- form-assignment ledger.

Do not infer approval from the fact that the software is ready.

## Form assignment

One balanced cycle contains:

- P2: 36 forms
- P3: 36 forms
- P6: 36 forms
- total: 108 forms

Each base-form number has parallel P2/P3/P6 versions.

### Assignment rule

Within a complete cycle:

1. allocate each form once before reuse;
2. randomize participant-to-form assignment subject to remaining-form balance;
3. one participant receives exactly one protocol arm;
4. never move a participant to another protocol because of their answers;
5. if a session must be replaced after a pre-specified exclusion, replace the same form/protocol slot.

The form cycle is a balancing device, not a power guarantee.

## Participant flow

### 1. Information / consent
Use the institutionally approved procedure.

### 2. Pseudonymous ID
Assign or enter a study ID that does not encode unnecessary personal information.

### 3. Protocol instruction
Participant receives only the instructions for their assigned protocol.

### 4. Constructed training
Practice items teach the response alphabet.

Training items are not benchmark trials and are not included in the main semantic outcome matrix.

### 5. Formal calibration
Each form contains:

- 60 lexical trials;
- 24 mixed response-state trials;
- 84 unique main trials total;
- 8 covert retests;
- 92 presented formal trials.

### 6. Local export / approved submission
The standalone interface downloads one JSON response file.

For a remote study, replace local handoff with an approved secure collection route rather than inventing ad-hoc email/file sharing.

## Training policy

P6 training explicitly distinguishes:

- BORDERLINE — genuine graded/boundary case;
- UNKNOWN — determinate in principle but unavailable to the oracle;
- UNDEFINED — question not properly truth-evaluable/applicable as posed;
- BOTH — explicit positive and negative support under a non-explosive benchmark representation.

P3 intentionally teaches only one MAYBE state and does not ask participants to diagnose the reason.

P2 intentionally provides no escape state.

Training performance may be retained as a quality variable, but any exclusion based on training errors must be frozen before outcome inspection.

## Response handling

Raw browser exports must pass through:

`ingest_standalone_responses.py`

before analysis.

The ingestion step validates canonical form identity and reconstructs hidden design metadata such as `is_retest`.

Never manually add retest labels to participant files.

## Minimum data-integrity checks

Before analysis:

- every included session has one known form ID;
- protocol matches canonical form;
- exactly 92 formal rows are present;
- target/query/pair IDs match the frozen trial order;
- responses belong to the assigned alphabet;
- no duplicate participant/form session is present;
- a participant does not appear in multiple protocol arms;
- negative response times and impossible confidence values are rejected.

## Stage-A analyses

### Protocol usability
- completion rate;
- missing/invalid response rate;
- response time;
- confidence.

### Reliability
- within-rater retest consistency;
- pairwise inter-rater agreement;
- pair-level response entropy.

### Mechanism
- P2 → P3 coarse-escape effect;
- P3 vs coarsened-P6 distribution divergence;
- P6 fine-state utilization;
- P6 fine-state reliability.

### Semantic calibration
- pair-level distributions;
- lexical versus mixed-stress differences;
- review/adjudication queue.

## Stage-A decision gate

### Continue P6 if
- fine states are actually used;
- use is semantically patterned;
- reliability is acceptable;
- P6 provides measurable value beyond P3 after considering response time/cost.

### Prefer P3 if
- P3 captures nearly all benefit over P2;
- P6 subdivisions are unreliable or rarely used;
- P6 substantially increases burden without downstream benefit.

### Rework protocol if
- participants systematically confuse UNKNOWN / UNDEFINED / BORDERLINE / BOTH;
- training failure is widespread;
- wording creates high entropy across ordinary items;
- ingestion or identity integrity checks fail.

## What Stage A cannot establish

Stage A alone does not prove:

- UCID's multi-axis representation is superior;
- P6 is globally optimal;
- the benchmark is universal across languages/cultures;
- 108 participants are sufficient for a small P3→P6 effect;
- response majority equals semantic truth.

## Handoff after Stage A

Only after the response-protocol gate is resolved:

1. freeze the retained protocol(s);
2. adjudicate or probabilistically retain calibrated pair responses;
3. expand to Benchmark v0 strata;
4. simulate/freeze confirmatory hierarchical power and analysis;
5. run representation/query-policy comparisons.
