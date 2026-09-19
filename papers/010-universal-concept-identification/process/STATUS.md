# ARIS4C010 · STATUS

**Updated:** 2026-09-19  
**Stage:** HUMAN-CALIBRATION-READY · P2/P3/P6 mechanism design, source/calibration/forms/UI/analysis plumbing CI-verified  
**Current claim strength:** provisional integration gap; not manuscript-frozen

## Completed

- [x] canonical project folder and `paper.json`
- [x] 2025 proactive information-gathering and 2026 group-elicitation neighbors added to novelty boundary
- [x] 2026 nearest-neighbor re-audit: ICAART ontology-guided Bayesian active querying added as major structural collision
- [x] all Python tools compile successfully; full pipeline + power sensitivity verified in CI run #49
- [x] standalone no-backend three-protocol annotation UI implemented; current design contains 108 participant forms
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
- [x] figure/table plan with confirmatory-result placeholders
- [x] English + Chinese pre-results manuscript scaffolds
- [x] annotation adjudication policy + review triage tool
- [x] staged human precision/stopping plan
- [x] human-form validation, CSV export and synthetic analysis dry-run extended to P2/P3/P6 and verified in the current three-protocol chain
- [x] balanced human forms built: 108 forms (36 P2 + 36 P3 + 36 P6), 92 presented formal trials/form
- [x] complete calibration chain verified in ARIS4C010 CI run #30
- [x] mixed response-state packet built: 24 scenarios × 9 probes = 216 blank pairs, shared across P2/P3/P6
- [x] lexical human packet built: 1,440 full pairs + 720 answer-blind calibration pairs
- [x] Calibration60 built from pinned oewn:2025 and CI-verified: 60 targets, 10 lemma groups × 6 senses
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

**Engineering:** human-calibration pipeline complete and CI-verified.

**Theory:** baseline propositions and failure-mode distinctions are frozen enough for implementation; they remain revisable if a closer prior is found.

**Empirical evidence:** Pilot 2 is source-derived but still exploratory because semantic responses are not human calibrated. Pilots 0–1 remain synthetic/combinatorial.

**Next real evidence step:** complete the ethics/recruitment gate, collect Stage-A real human P2/P3/P6 calibration responses, test P2→P3 and especially P3→P6, then decide which response protocol survives before Benchmark v0 expansion.

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


## Human calibration gate

The repository is now **human-calibration-ready**.

### Verified lexical calibration artifacts

CI run #30 confirms:

- 60 pinned OEWN 2025 targets;
- 10 lemma groups × 6 noun senses;
- 1,440 blank full target-query pairs;
- 720 answer-blind lexical calibration pairs;
- generic query exposure 29–31 times in the 720-pair subset.

### Verified mixed response-state artifacts

CI run #30 confirms:

- 24 constructed stress scenarios;
- 18 generic probes;
- 216 blank target-query pairs;
- each probe exposed exactly 12 times.

### Verified participant forms

The **current three-protocol form artifact is locked to CI run #61** in `process/HUMAN_FORMS_LOCK.json`:

- 108 total forms;
- P2/P3/P6 = 36/36/36;
- 84 unique main trials + 8 retests = 92 presented formal trials/form;
- lexical pair main exposure = 3 per protocol per complete form cycle;
- mixed-stress pair main exposure = 4 per protocol per complete form cycle;
- 108 per-form CSVs + one index;
- synthetic analyzer dry-run covers P2/P3/P6.

An earlier two-protocol development run exposed a possible immediate main/retest adjacency. The ordering algorithm was changed to deterministic reshuffling until no adjacent duplicate remains; the current run-#61 artifact is the canonical form lock.

### What is genuinely blocked

No further code or ontology prose can substitute for the next evidence step:

1. ethics/exemption determination as appropriate;
2. recruitment/platform decision;
3. real P2/P3/P6 participant responses;
4. Stage-A reliability/category-use analysis;
5. only then promotion of selected response cells from `unannotated` toward `human_annotated` / adjudication.

Synthetic responses, LLM responses, and the exploratory Pilot 2 matrix must not be used to pretend that this gate has been passed.

## Current canonical claim ceiling

Allowed now:

> ARIS4C010 provides a formal theory, source-locked benchmark architecture, exploratory source-derived query-complexity pilot, and CI-verified human calibration protocol for measuring Semantic Query Overhead.

Not yet allowed:

> the proposed multi-axis ontology is empirically superior across human semantic judgments;

or:

> P6 is more reliable/valid than binary answering;

or:

> the final Benchmark v0 semantic response matrix has been validated.

Those require real human data.


## 2026 novelty re-audit

A September 2026 nearest-neighbor pass found a particularly important published collision:

- **Agafonov, Ponomarev & Smirnov, ICAART 2026** already combine a rooted ontology, semantic retrieval, binary relevance questions, Bayesian belief tracking and budgeted active refinement.

Therefore 010 must **not** claim “ontology-guided active questioning” as novel.

Additional current neighbors:

- **Wang et al., ICML 2025:** adaptive natural-language elicitation of latent information;
- **Huang et al., Findings of EMNLP 2025:** proactive clarification / information gathering;
- **Ding et al., ICML 2026:** adaptive group elicitation choosing both questions and respondents;
- **CRAC 2025 referential ambiguity work:** clarification behavior is empirically variable across humans and LLMs.

The surviving candidate contribution is narrower:

> quantify the cost and failure modes introduced by **semantic admissibility** across heterogeneous concept regimes, including non-classical response states and open-world/pathological boundaries, relative to unrestricted identification.

This remains a provisional integration gap, not a frozen novelty claim.

## Engineering verification history

CI run **#49** was a successful **pre-P3 engineering baseline**: all then-current Python tools compiled and the source/calibration/forms/UI/power plumbing executed. It is retained as history but is superseded for the current three-protocol design.

For the current design:

- **run #61** verifies the P2/P3/P6 chain and locks the 108-form artifact;
- **run #62** verifies the updated power-sensitivity calculator.

Illustrative retest sensitivity from the earlier binary-to-rich protocol calculation, assuming P2 consistency 0.80, 8 retests/person, two-sided alpha=.05, power=.80:

- target P6=.85, ICC=.05 → ~153 participants/arm;
- target P6=.88, ICC=.05 → ~56 participants/arm;
- target P6=.90, ICC=.05 → ~34 participants/arm.

These are crude design-effect approximations, not final sample-size requirements.


## P3 mechanism baseline

The 2026 prior-art pass showed that coarse non-binary answers such as YES/MAYBE/NO are already used in adaptive Twenty Questions research. Therefore “non-binary answering” itself is not a 010 novelty.

The human calibration now uses three protocols:

- **P2:** YES / NO;
- **P3:** YES / NO / MAYBE;
- **P6:** YES / NO / BORDERLINE / UNKNOWN / UNDEFINED / BOTH.

Interpretation:

- P2→P3 = value of allowing any coarse escape from binary forcing;
- P3→P6 = incremental value of distinguishing why binary judgment fails;
- P2→P6 = total protocol effect, but is not sufficient for the mechanism claim.

CI run **#61** verifies the complete three-protocol chain:

- 108 forms = 36 P2 + 36 P3 + 36 P6;
- 84 unique main trials + 8 retests per form;
- lexical pair exposure = 3 per protocol per complete cycle;
- mixed-stress pair exposure = 4 per protocol per complete cycle;
- 108 CSV forms and 108 standalone participant HTML pages;
- synthetic analysis dry-run covers all three protocols.

CI run **#62** verifies the updated power-sensitivity calculator.

Illustrative retest-consistency sensitivity with 8 retests/person and ICC=.05:

- P2 .80 → P3 .88: ~56 participants/arm;
- P3 .85 → P6 .88: ~344 participants/arm;
- P3 .85 → P6 .90: ~116 participants/arm;
- P3 .85 → P6 .92: ~55 participants/arm.

These are simple approximations, not final sample-size requirements. They show that a small P3→P6 effect can be much harder to detect than the broader P2→P6 contrast.
