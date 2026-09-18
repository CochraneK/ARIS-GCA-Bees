# ARIS4C010 · Semantic Query Admissibility Protocol v0.1

## Purpose

ARIS4C010 is only interesting if "semantic query" is more constrained than an arbitrary binary partition of the candidate set.

This file defines the operational restriction used by future benchmarks.

## A query is admissible only if all applicable conditions hold

### A1 · Interpretable
A competent participant can understand what the question asks without seeing the hidden target label.

### A2 · Target-type compatible
The query is meaningful for the current target level.

Example:
- "Is it physically located in France?" may apply to a concrete referent;
- it is a category error for the orthographic string `bank`.

A type mismatch is not ordinary NO.

### A3 · Context-resolvable
Every context variable required for a determinate answer is either:
- frozen in the benchmark;
- recoverable from dialogue history;
- or explicitly requested as a context subquery.

### A4 · Non-leaking unless scored as a direct guess
A diagnostic semantic question should not contain a unique target name, synonym, gloss fragment or identifier that trivially reveals the answer.

Direct guesses are permitted, but must be labeled and assigned their own cost regime.

### A5 · Answerable under the stated oracle model
The benchmark must specify who/what is answering:
- human participant;
- lexical resource;
- knowledge base;
- formal solver;
- LLM;
- adjudicated consensus.

A question can be admissible for one oracle and inaccessible for another.

### A6 · Stable enough for reproducible evaluation
The intended interpretation should be sufficiently stable that repeated judgments are meaningful.

This does not require unanimity. Vague or theory-dependent questions may remain admissible if disagreement is itself modeled.

### A7 · Provenance-known
Every benchmark query records whether it is:
- human authored;
- resource derived;
- literature derived;
- LLM generated then validated;
- constructed stress query.

## Query classes

### Semantic class questions
Examples:
- Is it an organism?
- Is it a process?
- Is it a social role?

### Property questions
Examples:
- Is it physically extended?
- Is it typically perceptible by vision?

### Logical/compositional questions
Examples:
- Is the target defined using negation?
- Does the expression quantify over a class?

### Referential/modal questions
Examples:
- Does the description currently have a satisfier?
- Is the target fictional in the benchmark interpretation?

### Context questions
Examples:
- Does its interpretation depend on the speaker?
- Does the answer require a comparison class?

### Epistemic/computability questions
Examples:
- Is the proposition empirically unresolved?
- Is the relevant decision problem undecidable in general?

### Lexical/metalinguistic questions
Examples:
- Is the target a lexical sense rather than a referent?
- Does this surface form have another benchmarked sense?

### Direct identity guesses
Examples:
- Is it the financial-institution sense of "bank"?

These are legal game moves but analytically distinct from semantic partition questions.

## Invalid versus non-informative

A question can be:

- **valid + informative** — partitions remaining candidates;
- **valid + non-informative** — all remaining candidates receive the same response;
- **invalid by type/context** — should trigger UNDEFINED or CONTEXT_REQUEST rather than ordinary NO;
- **leaky** — direct identity reveal not allowed under the diagnostic-query condition.

This distinction matters because a policy that asks many type-invalid questions may still appear to gain information if the benchmark wrongly encodes all invalid cases as NO.

## Semantic cost model

Default unit cost is 1 question, but later analyses should consider:

[
cost(q)=
1
+ \lambda_{len} \cdot length(q)
+ \lambda_{ctx} \cdot context\_burden(q)
+ \lambda_{cog} \cdot cognitive\_difficulty(q).
]

The coefficients are not fixed yet. The publication-level benchmark should first report:
1. unit-question cost;
2. token/length cost;
3. empirically measured response-time cost where human data exist.

## Policy-level validity metrics

For each questioning policy report:

- invalid/type-error rate;
- missing-context rate;
- direct-guess rate;
- mean semantic cost;
- information gain per cost;
- repeated-question rate;
- oracle-disagreement rate.

Success@N alone is insufficient.

## Admissibility adjudication

For a calibration subset, two annotators independently judge:
- query type;
- target-level applicability;
- context requirements;
- leakage;
- answerability.

Disagreements are adjudicated and retained in the audit trail.

## Important boundary

"Semantically admissible" is always relative to a specified language, participant population, task framing and oracle.

ARIS4C010 should not claim a context-free universal set of admissible questions.
