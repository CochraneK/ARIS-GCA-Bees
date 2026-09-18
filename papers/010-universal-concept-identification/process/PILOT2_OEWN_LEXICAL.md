# ARIS4C010 · Pilot 2 — OEWN lexical-sense identification

**Status:** source-derived exploratory pilot complete  
**Date:** 2026-09-18  
**Targets:** 15 Open English WordNet noun senses  
**Human calibration:** not yet performed

## Why this is different from Pilots 0–1

Pilot 0 was purely combinatorial. Pilot 1 used constructed semantic targets.

Pilot 2 introduces **real lexical sense identities from Open English WordNet**:

- 9 noun senses of **bank**;
- 6 noun senses of **spring**.

Every target preserves:
- OEWN synset ID;
- OEWN sense key;
- lexname;
- source gloss;
- source URL;
- license/provenance.

The added UCID semantic-query labels remain `machine_mapped_unreviewed`. Therefore this is the first source-derived pilot, but not publication-grade semantic gold.

## Source-only baseline: OEWN lexname

Using only source-native lexname categories leaves five collision classes:

```text
noun.object:
  bank — river slope
  bank — ridge/pile
  spring — groundwater flow

noun.group:
  bank — financial institution
  bank — arrangement of similar objects

noun.possession:
  bank — reserve stock
  bank — gambling funds

noun.artifact:
  bank — money container
  bank — bank building
  spring — elastic device

noun.act:
  bank — flight maneuver
  spring — leap/movement
```

Across 15 targets there are 105 target pairs. Nine pairs remain unresolved, so lexname pairwise separation coverage is:

[
96/105 = 0.9143.
]

This is not a criticism of WordNet. Lexnames were never designed to uniquely encode every sense.

## Added semantic-query family

Pilot 2 adds 18 broad YES/NO questions audited against the OEWN glosses, including:

- natural feature/phenomenon;
- water-related;
- institution/organization;
- money/banking-related;
- resource/stock;
- gambling;
- artifact/device;
- container;
- building;
- action/maneuver;
- aircraft motion;
- upward/forward movement;
- elasticity;
- abstract property;
- location/point;
- material flow;
- time/season;
- arrangement of similar objects.

All 15 source-derived targets have unique signatures under the full 18-query family.

**Pairwise separation coverage: 1.000.**

Again, this is engineering evidence only because the semantic labels have not yet been independently annotated.

## Static semantic basis

Exact subset search finds that **12 of the 18 questions are sufficient** to separate all 15 senses:

```text
natural
water
money
resource
artifact
container
action
aircraft
elastic
location
flow
time
```

The other six questions are redundant for this particular target sample, though they may matter in a broader benchmark.

This is a direct demonstration that:
- a full semantic feature bank;
- a minimum static separating basis; and
- an optimal adaptive questioning policy

are different objects.

## Adaptive query complexity

With a uniform prior and unit-cost deterministic questions, the exact optimal adaptive tree over the 18 semantic questions has:

- **expected cost: 4.2667 questions**
- **worst-case cost: 6 questions**

The greedy information-gain policy reaches the same expected/worst cost on this pilot.

For 15 equiprobable targets, an unrestricted binary decision tree can do better because it may use arbitrary partitions:

- **optimal expected unrestricted cost: 3.9333**
- **optimal unrestricted worst case: 4**

The unrestricted expected number is the Huffman-optimal prefix-code length, not merely the Shannon entropy lower bound.

## First source-derived Semantic Query Overhead estimate

Within this small exploratory sample:

[
\Delta_{sem}^{expected}
=4.2667-3.9333
=0.3333
]

questions on average.

Worst case:

[
\Delta_{sem}^{worst}
=6-4
=2.
]

This is the first concrete estimate of the project's central quantity.

It must **not** yet be generalized beyond this pilot because:
- only two polysemous lemmas are included;
- the semantic query bank was constructed after inspecting glosses;
- labels are not human calibrated;
- target prior is uniform;
- all query costs are fixed at one;
- direct natural-language answer reliability is not measured.

## Interpretation

The result already demonstrates a useful decomposition.

### Source taxonomy alone
Provides high but incomplete separation.

### Cross-cutting semantic questions
Can remove the observed collisions.

### Semantic restrictions
Still impose measurable overhead relative to arbitrary mathematical partitions.

That three-part pattern is exactly what Benchmark v0 is designed to test at larger scale.

## Reproducibility

Data:
- `data/pilot2/oewn_senses.v0.json`
- `data/pilot2/semantic_queries.v0.json`

Code:

```bash
cd papers/010-universal-concept-identification/code
python pilot2_oewn_lexical.py
```

## Next gate

Pilot 3 should **not** simply add more hand-labeled WordNet senses.

Next evidence should be:

1. automated pinned-release OEWN ingestion;
2. a stratified 60-target lexical calibration subset;
3. human judgments for semantic-query responses;
4. comparison of P2 versus P6 response protocols;
5. then expansion toward the ~320-target Benchmark v0.
