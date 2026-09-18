# ARIS4C010 · STATUS

**Updated:** 2026-09-19  
**Stage:** source-derived Pilot 2 complete · pinned 60-target OEWN calibration build configured  
**Current claim strength:** provisional integration gap; not manuscript-frozen

## Completed

- [x] canonical project folder and `paper.json`
- [x] finite/infinite/open-world problem separation
- [x] formal separability criterion
- [x] static Test-Cover connection
- [x] adaptive decision-tree distinction
- [x] Semantic Query Overhead metric family
- [x] multi-axis concept ontology v0.1
- [x] binary vs semantically explicit response protocols
- [x] benchmark ladder ordinary → compositional → adversarial → open-world
- [x] live audit of query learning / GBS / Test Cover / FCA / WordNet / LLM Twenty Questions
- [x] live audit of ICML 2025 adaptive elicitation
- [x] live audit of Referring Expression Generation
- [x] live audit of description-logic active concept learning / ontology inseparability
- [x] pragmatic/RSA neighbor identified
- [x] standard-library combinatorial engine
- [x] Pilot 0 executed and recorded
- [x] Pilot 1 synthetic semantic seed executed and recorded (taxonomy collisions → multi-axis separation; synthetic only)
- [x] machine-readable UCID target schema v0
- [x] calibration60 builder + validator + artifact upload configured
- [x] pinned dependency/resource path: wn==1.1.1 + oewn:2025
- [x] calibration60 sampling frozen: 10 polysemous lemmas × 6 noun senses
- [x] raw OEWN source-record layer separated from UCID semantic annotation layer
- [x] first CI run completed successfully
- [x] persistent GitHub Actions CI for unit tests + Pilots 0–2
- [x] unrestricted expected-cost baseline upgraded from entropy-only to exact Huffman prefix-code optimum
- [x] Pilot 2 exact semantic-query overhead: expected +0.3333 questions; worst-case +2 (exploratory, uncalibrated)
- [x] source-derived OEWN Pilot 2: 15 real senses (bank + spring)

## Main correction made during audit

The early formulation risked claiming that the project would discover a "minimal taxonomy that can identify anything."

That is too broad and partly already solved in adjacent forms:

- Test Cover: minimum separating test set;
- REG: minimum distinguishing properties for a known referent;
- description-logic active learning: query-learning formal concepts under ontologies.

The canonical 010 question is therefore now:

> **How much query complexity is added by semantic admissibility across heterogeneous and non-classical concept regimes, and where does exact identification become undefined or impossible?**

## Current novelty wedge

Four-part integration:

1. semantically admissible adaptive query complexity relative to unrestricted partitions;
2. typed semantic coverage across representation levels and logical composition;
3. explicit false/unknown/borderline/undefined/inconsistent response distinctions;
4. open-world + pathological identification boundaries in one reproducible benchmark.

## Pilot 0 result

Synthetic 12-candidate sanity matrix:

- information lower bound: 4 binary questions worst case;
- minimum static separating basis: 4 informative queries;
- exact optimal adaptive worst-case depth: 4;
- exact optimal expected depth: 3.6667;
- removal of one essential dimension creates four indistinguishable pairs.

This is code validation only, not semantic evidence.

## Next implementation gate

### Benchmark v0
Target: ~300 records across ordinary, abstract, lexical, compositional, contextual and stress strata.

Before large-scale population:
- settle resource licenses;
- define sampling quotas;
- build question-record schema;
- add source and adjudication ledgers;
- pilot human calibration on a small mixed stratum.

### Remaining novelty searches
- abstract/nonvisual REG;
- clarification-question generation for disambiguation;
- active feature acquisition with abstention / not-applicable;
- open-world concept learning;
- multi-valued diagnosis;
- identifying/separating codes literature.

## Stop conditions

Pause or split the project if:
- a close prior already integrates broad semantic coverage + adaptive hidden-target identification + nonclassical answers + open-world/pathological regimes;
- human calibration shows the proposed response states cannot be made reproducible;
- ontology-axis complexity adds no held-out separation benefit beyond simpler graph/embedding baselines.

## Canonical files

- `README.md`
- `paper.json`
- `process/RESEARCH_PLAN.md`
- `process/CONCEPT_ONTOLOGY.md`
- `process/BENCHMARK_SPEC.md`
- `process/LITERATURE_MATRIX.md`
- `process/NOVELTY_AUDIT.md`
- `process/PILOT0_COMBINATORIAL.md`
- `data/ucid-target.schema.json`
- `code/query_complexity.py`


## Current readiness

**Engineering:** pinned lexical source ingestion implemented; calibration60 CI build is the current hard gate.

**Theory:** baseline propositions and failure-mode distinctions are frozen enough for implementation; they remain revisable if a closer prior is found.

**Empirical evidence:** Pilot 2 is source-derived but still exploratory because semantic responses are not human calibrated. Pilots 0–1 remain synthetic/combinatorial.

**Next real evidence step:** freeze the generated 60-target OEWN source pool, create its P2/P6 human annotation packet, and calibrate semantic responses before expanding toward the ~320-target mixed Benchmark v0.

The project should not spend more time expanding ontology prose before that evidence step unless a literature collision forces redesign.


## Pilot 2 result

Pilot 2 uses 15 source-derived OEWN senses: 9 noun senses of `bank` and 6 noun senses of `spring`.

Source-native `lexname` alone leaves 5 collision groups, with pairwise separation coverage 0.9143. An exploratory 18-query semantic bank gives unique signatures for all 15 targets; the exact minimum static separating subset contains 12 questions.

Under a uniform prior and unit question cost:

- unrestricted Huffman-optimal expected binary cost: **3.9333**;
- semantic exact-optimal expected cost: **4.2667**;
- expected Semantic Query Overhead: **+0.3333 questions**;
- unrestricted worst-case lower bound: **4**;
- semantic exact-optimal worst case: **6**;
- worst-case overhead: **+2 questions**.

These are **exploratory engineering results** because the semantic response matrix is `machine_mapped_unreviewed`.

## Calibration60

The next lexical calibration set is generated from pinned `oewn:2025` through `wn==1.1.1`.

Design:

- 10 polysemous lemmas;
- 6 noun senses per lemma;
- 60 total source-derived targets;
- grouped by lemma to prevent surface-form leakage;
- source layer stores only OEWN-supported sense/synset/lexname/gloss/example data;
- UCID semantic labels are added only after mapping/calibration.

The builder intentionally fails if any selected lemma has fewer than six noun senses; it never silently replaces the sampling plan.

## CI

`.github/workflows/aris4c010-ci.yml` now runs:

- query-complexity unit tests;
- seed validation;
- leakage split checks;
- Pilots 0–2;
- pinned OEWN calibration60 build/validation;
- calibration60 artifact upload.

The first pre-calibration60 CI run completed successfully. The new pinned-resource build is being validated by the updated workflow.
