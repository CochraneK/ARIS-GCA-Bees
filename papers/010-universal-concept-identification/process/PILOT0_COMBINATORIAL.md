# ARIS4C010 · Pilot 0 — combinatorial plumbing

**Status:** complete  
**Nature:** mathematical / software sanity check only; no semantic or empirical claim

## Purpose

Before building a concept ontology or collecting judgments, verify that the code distinguishes three different objects correctly:

1. information-channel lower bounds;
2. a static separating query basis;
3. an adaptive decision tree.

These are easy to conflate.

## Executed sanity case

`code/query_complexity.py` was run on 2026-09-18 with a synthetic 12-candidate deterministic binary matrix. Four columns contain the candidate code; two additional columns are redundant transformations.

Observed output:

```text
20 binary questions: 1,048,576 leaves
21 binary questions: 2,097,152 leaves
12-candidate binary lower bound: 4 questions
minimum static separating queries: (0, 1, 2, 3)
optimal worst-case tree: (4.0, 0)
optimal expected tree: (3.6666666666666665, 0)
collisions if one essential bit is omitted: [[0, 8], [1, 9], [2, 10], [3, 11]]
```

## Interpretation

- The 20/21-question leaf counts reproduce the finite-channel bound.
- A **static basis** needs all four information-bearing binary columns to assign unique signatures to all 12 candidates.
- An **adaptive tree** can have lower expected depth than the static basis length because some leaves terminate early, while its worst-case depth still meets the 4-question lower bound.
- Omitting an essential axis creates explicit query-equivalence classes: no policy restricted to the remaining questions can distinguish those pairs.

## Why this matters for the semantic study

The future empirical pipeline should report at least four separate quantities:

- theoretical lower bound;
- minimum static semantic basis;
- optimal/approximate adaptive query cost;
- unresolved collision classes.

A visually elegant ontology can still have poor separation; a large ontology can still admit a shallow adaptive policy.

## Reproducibility

Standard-library Python only:

```bash
python papers/010-universal-concept-identification/code/query_complexity.py
```

No external data or generated semantic labels are used in Pilot 0.
