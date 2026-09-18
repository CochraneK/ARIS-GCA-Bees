# ARIS4C010 · Figure and Table Plan

The final paper should contain real figures and tables. This file separates figures that can be finalized before confirmatory data from figures that must wait for human/Benchmark v0 results.

## Figures

### Figure 1 · From unrestricted Twenty Questions to semantic identification
**Status:** can be finalized pre-results.

Panels:
A. unrestricted binary partitions;
B. semantically admissible query family;
C. response-signature collisions;
D. Semantic Query Overhead.

Purpose: explain why `log2(N)` is a lower-bound/coding baseline rather than a realistic semantic questioning strategy.

### Figure 2 · UCID typed concept space
**Status:** can be finalized pre-results.

Visualize the 10 cross-cutting axes and show that one target can occupy coordinates across multiple axes rather than one leaf in a universal tree.

Example targets:
- dog;
- bank (financial sense);
- tall;
- unicorn;
- round square;
- here;
- halting predicate.

### Figure 3 · Evidence ladder and anti-overclaiming architecture
**Status:** can be finalized pre-results.

Pilot 0 → Pilot 1 → Pilot 2 → Calibration60 → mixed P6 → Benchmark v0.

Clearly label:
synthetic / source-derived / machine-mapped / human-calibrated / adjudicated.

### Figure 4 · Human calibration design
**Status:** can be finalized after human-form CI.

Show:
- 60 OEWN lexical targets;
- 24 stress scenarios;
- 36 base forms × P2/P6;
- main/retest structure;
- pair exposure balance.

### Figure 5 · Semantic Query Overhead by representation and stratum
**Status:** confirmatory only.

Potential axes:
- x: representation/query condition;
- y: expected questions minus unrestricted optimum;
- facets: lexical / abstract / compositional / vague-contextual / stress.

No values should be populated from synthetic pilots.

### Figure 6 · P2 versus P6 response validity
**Status:** confirmatory only.

Potential panels:
- retest consistency;
- response entropy;
- invalid forced-answer rate;
- response time;
- P6 category confusion.

### Figure 7 · Open-world failure and recovery
**Status:** Benchmark v0 only.

Compare forced closed-world guessing, OOS abstention, and ontology expansion on withheld targets.

## Tables

### Table 1 · Concept representation axes
Source: `CONCEPT_ONTOLOGY.md`.

### Table 2 · Prior-art boundary
Rows: exact query learning, Test Cover, REG, DL concept learning, RSA, active feature acquisition, LLM Twenty Questions, open-world learning, vagueness/non-classical logic.
Columns: existing contribution / overlap / what 010 does not claim / remaining gap.

### Table 3 · Formal propositions
Summarize finite-channel bound, separability, Test Cover reduction, response coarsening, context, OOS aliasing and ineffability boundary.

### Table 4 · Evidence ladder
Pilot 0–2 and calibration stages with source type, N, main result and claim ceiling.

### Table 5 · Calibration resources and licenses
OEWN, Wikidata, THINGS/THINGSplus, BFO, ConceptNet/external baseline.

### Table 6 · Confirmatory benchmark results
Reserved until frozen Benchmark v0.

## Bilingual requirement

English and Chinese manuscripts should use the same figure/table numbering and the same underlying generated result artifacts. Do not manually maintain two independent numerical result tables.
