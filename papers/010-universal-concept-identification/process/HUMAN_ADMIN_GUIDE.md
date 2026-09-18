# ARIS4C010 · Human Calibration Administration Guide

## Scope

This guide covers the first **P2 versus P6 calibration**. It does not authorize or replace institutional ethics review.

## What participants judge

Participants are **not playing Twenty Questions** in this calibration phase.

For each trial they see:

1. a target sense/scenario;
2. its definition and any frozen context;
3. one semantic question.

They judge whether the question applies to the target under the supplied interpretation.

This calibration estimates whether the response matrix needed by the later identification benchmark can be obtained reproducibly.

## P2 instructions

Choose exactly one:

- **YES** — the question applies / is true under the supplied interpretation.
- **NO** — the question is meaningful and applicable, but does not apply / is false.

P2 intentionally forces binary judgment.

## P6 instructions

Choose exactly one:

- **YES** — applies / true.
- **NO** — meaningful and applicable, but false.
- **BORDERLINE** — genuinely graded or borderline, not merely unknown.
- **UNKNOWN** — there is an answer in principle, but it is not knowable from the allowed information.
- **UNDEFINED** — the question is not properly truth-evaluable as posed because of type mismatch, missing required context, failed presupposition, or another stated semantic failure.
- **BOTH** — under the supplied benchmark information and its explicitly non-explosive interpretation, positive and negative support are both present.

Participants should never use BOTH as “I am confused.”

## Display requirements

- Show source/target definition before the query.
- Show frozen context in a separate visually distinct panel.
- Do not show ontology labels, expected phenomenon tags, or any researcher/model prediction.
- Do not expose whether a trial is a retest.
- Keep response buttons in a stable order within one protocol.
- Record response time from query presentation to final response.

## Confidence

After the categorical response, collect confidence on a 0–100 or equivalent continuous scale.

Confidence is about the participant's judgment, not about how familiar the word looks.

## Retest

Eight trials per form are covert repeats.

Do not tell participants which items are repeated. It is acceptable to disclose generally that some items may recur.

## Data fields to retain

At minimum:

- participant ID (pseudonymous);
- form ID;
- protocol;
- pair ID;
- response;
- confidence;
- response time;
- trial order;
- whether the row is a retest;
- timestamp/session identifier where allowed.

Do not collect unnecessary identifying or sensitive information.

## Exclusion / quality flags

Predefine before data inspection:

- incomplete session;
- impossible response code;
- duplicate submission/session collision;
- implausibly short completion patterns if a threshold is justified;
- failed attention/comprehension checks if such checks are introduced.

Do not exclude participants merely because they use BORDERLINE/UNKNOWN/UNDEFINED often; that usage is itself part of the research question.

## Language boundary

Calibration60 is based on Open English WordNet and English query wording. Results are therefore about an English semantic interface.

A later multilingual extension should not translate the English gold matrix and call it universal; it requires language-specific calibration.
