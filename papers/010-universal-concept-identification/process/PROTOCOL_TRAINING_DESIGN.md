# ARIS4C010 · Protocol Training Design

## Purpose

The training layer teaches how to use the assigned response alphabet before the 92 formal trials.

It is not a semantic benchmark and is not evidence for the study hypotheses.

## Separation from formal outcomes

Training items are:

- researcher-constructed;
- outside Calibration60;
- outside the 24 mixed-stress scenarios;
- given explicit corrective feedback;
- excluded from the formal target-query response matrix.

Their expected labels are instructional keys, not claims about natural semantic ground truth.

## Protocol-specific goals

### P2
Teach only the forced binary interface.

P2 training does not provide an uncertainty escape label.

### P3
Teach YES / NO / MAYBE.

MAYBE is deliberately coarse and may cover multiple reasons a confident binary response is inappropriate.

Participants are not trained to diagnose those reasons in P3.

### P6
Teach the distinction among:

- YES
- NO
- BORDERLINE
- UNKNOWN
- UNDEFINED
- BOTH

The practice set contains at least one constructed example of each P6 response state.

## Corrective learning rule

A participant cannot advance past a practice item until the canonical practice answer is selected.

After an incorrect attempt:

1. explanatory feedback is shown;
2. the participant must select again;
3. all attempts are retained in the raw response export.

Formal trials do not provide correctness feedback.

## Training-error variable

Researcher-side ingestion reconstructs correctness from the canonical training key rather than trusting the browser's `correct` field.

For each session it stores:

- number of practice items;
- total training attempts;
- training error count;
- completed-training flag.

## Default analysis policy

Training errors are initially a **quality / comprehension covariate**, not an automatic exclusion rule.

Before real outcome data are inspected, the study must freeze one of:

- no exclusion based on training errors;
- a specific maximum-error threshold;
- a sensitivity analysis comparing inclusion/exclusion.

Do not choose the threshold after seeing which rule makes P6 look better.

## Why training is necessary but not sufficient

If P6 reliability is poor after training, at least three explanations remain:

1. the distinctions are intrinsically difficult or unstable;
2. the operational definitions/instructions are inadequate;
3. the specific target-query items do not support clean distinction.

The mixed-stress item analysis and error/confusion structure should be used to distinguish these possibilities.

## Versioning rule

If a material training definition changes after recruitment begins:

- stop recruitment;
- version the training material;
- document which sessions used each version;
- do not silently pool across materially different training versions.
