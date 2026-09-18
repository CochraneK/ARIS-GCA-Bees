# ARIS4C010 · Pilot 1 — synthetic semantic seed

**Status:** complete as a constructed sanity test  
**Evidence class:** synthetic / design validation only  
**Date:** 2026-09-18

## Purpose

Pilot 0 verified the generic combinatorics. Pilot 1 asks a narrower design question:

> If the target set deliberately contains ordinary objects, properties, social roles, lexical senses, fiction, empty descriptions, impossible descriptions, indexicals, logical operators, paradox-like sentences and undecidable formal objects, does a single ontology-kind projection remain separating?

This pilot is **not** human-annotated and must not be cited as empirical evidence that the proposed ontology is correct.

## Constructed target set

16 seed targets:

- dog
- water
- running
- red
- teacher
- justice
- unicorn
- current king of France
- round square
- bank — financial sense
- bank — river-bank sense
- tall
- here
- and
- liar-like sentence
- halting set

The script encodes only a small subset of the UCID axes needed for this sanity test.

## Result 1 · taxonomy-only is non-separating

Using only coarse ontology-kind membership, three collision classes remain:

```text
red ↔ tall
teacher ↔ current king of France
justice ↔ bank (financial sense)
```

Interpretation:

- `red` and `tall` need boundary/context information beyond "property";
- `teacher` and the empty current-king description need existence/target-level information beyond "role/social";
- `justice` and the financial sense of `bank` need representation/boundary distinctions beyond "social/institutional".

This does **not** prove that every possible single taxonomy fails. It shows that this ordinary `is-a` projection loses distinctions the benchmark explicitly cares about.

## Result 2 · multi-axis questions remove the seed collisions

A greedy Test-Cover-style procedure over the constructed cross-axis question bank found a 14-question separating basis for all 16 targets.

The unrestricted binary information lower bound is only:

[
\lceil \log_2 16 \rceil=4.
]

The gap is intentional and illustrates the project's central quantity: semantic questions may be substantially less flexible than arbitrary mathematical partitions.

This 14-query set is only a **greedy** static basis and is not claimed to be globally minimal.

## Result 3 · adaptive querying is much cheaper than asking the whole basis

On the same constructed basis, greedy information gain gives:

- mean query cost: **4.5625**
- worst-case query cost: **7**

for the 16 uniformly weighted targets.

This is close to the 4-bit information lower bound in expectation despite the static basis containing 14 questions.

Interpretation:

> static ontology coverage and adaptive dialogue efficiency are distinct quantities.

## Result 4 · response coarsening can destroy distinctions

A toy P6 fragment uses four distinct responses:

```text
YES
NO
UNKNOWN
UNDEFINED
```

If UNKNOWN and UNDEFINED are forcibly mapped to NO, four response states collapse to two.

This is merely an executable illustration of the data-processing argument in `FORMAL_CORE.md`. The real question is whether human raters can use richer states consistently enough to justify their interaction cost.

## Reproducibility

```bash
cd papers/010-universal-concept-identification/code
python pilot1_semantic_seed.py
```

The script imports the shared `query_complexity.py` baseline core.

## What Pilot 1 establishes

Only:

1. the planned code can expose query-equivalence collisions;
2. a taxonomy-only projection can be intentionally stress-tested;
3. cross-axis queries can restore separability in the constructed example;
4. adaptive versus static query costs can be reported separately;
5. richer response states can be analyzed without assuming binary semantics.

## What Pilot 1 does NOT establish

It does not establish:

- that the UCID axes are complete;
- that 14 is the true minimal semantic basis;
- that real humans would assign the encoded labels;
- that multi-axis ontology representations will outperform lexical graphs or embeddings on real data;
- that pathological concepts have one uncontested semantic analysis;
- that the final paper's empirical hypotheses are supported.

Those require Benchmark v0 + human/resource calibration.
