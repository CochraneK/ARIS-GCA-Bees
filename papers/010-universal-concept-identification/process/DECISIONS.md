# ARIS4C010 · Decisions Log

## 2026-09-18 · D001 — Do not build one "perfect tree of all concepts"
**Decision:** use a typed multi-axis semantic representation plus compositional operators.

**Reason:** polysemy, relations, negation, modality, context, vagueness, empty descriptions and self-reference are cross-cutting and do not fit one inheritance tree without distortion.

## D002 — Separate static coverage from adaptive efficiency
**Decision:** always report both minimum/approximate separating bases and adaptive decision-tree/path cost.

**Reason:** Pilot 0 demonstrates that a large static basis can still support shorter adaptive paths.

## D003 — Treat Test Cover, generalized binary search and information gain as baselines
**Decision:** no novelty claim for the core optimization machinery.

**Reason:** these are mature literatures.

## D004 — Treat REG and description-logic concept learning as direct ancestors
**Decision:** cite and compare rather than rediscover.

**Reason:** REG covers minimal distinguishing descriptions; DL work covers active concept learning under ontologies.

## D005 — Define Semantic Query Overhead relative to unrestricted partitions
**Decision:** central quantitative target is the cost imposed by semantic admissibility.

**Reason:** this directly links information theory to ontology/language restrictions.

## D006 — Keep P2 and richer semantic protocols separate
**Decision:** benchmark strict binary and P6/P6+context rather than assuming richer labels are better.

**Reason:** richer answers transmit more information but may impose reliability/cognitive costs.

## D007 — Strong ineffability is outside ordinary target rows
**Decision:** model it as a boundary condition.

**Reason:** if an oracle cannot form/maintain the target representation, the ordinary response function is undefined.

## D008 — Preserve open-world/OOS explicitly
**Decision:** allow withheld targets and ontology expansion; never force every target into the known list.

## D009 — Synthetic semantic pilots are not empirical evidence
**Decision:** `constructed_seed` and `adjudicated_gold` are distinct schema states.

## D010 — External ontologies are evidence layers, not canonical metaphysics
**Decision:** retain source-native assertions and provenance; adjudicate UCID mappings separately.

## D011 — Avoid license contamination
**Decision:** keep reciprocal-license resources such as ConceptNet isolated as baselines/lookup until redistribution architecture is explicit.

## D012 — Canonical source of truth is the numbered paper folder
**Decision:** `paper.json`, `process/STATUS.md`, schemas and code are authoritative. Public portfolio pages are generated views and may temporarily lag during concurrent ARIS4C updates.


## 2026-09-19 · D013 — Add P3 as the mechanism baseline
**Decision:** compare P2 = YES/NO, P3 = YES/NO/MAYBE, and P6 = YES/NO/BORDERLINE/UNKNOWN/UNDEFINED/BOTH.

**Reason:** 2025–2026 prior art already uses coarse non-binary answers in adaptive elicitation/Twenty Questions. Therefore "allow non-binary answers" is not a defensible novelty claim.

**Mechanistic interpretation:**
- P2→P3 estimates the value of any coarse escape from binary forcing;
- P3→P6 estimates the incremental value of distinguishing *why* a binary answer fails;
- P2→P6 is the total protocol effect but cannot isolate the mechanism.

## 2026-09-19 · D014 — Do not substitute models for the human calibration gate
**Decision:** LLM, synthetic, or researcher-generated answers may be used only as separate oracle/baseline classes and engineering dry-runs.

**Reason:** the next scientific claim depends on whether humans can reproducibly use the P3/P6 response semantics. Model-generated labels cannot establish that.

## 2026-09-19 · D015 — Stop expanding ontology prose before Stage A
**Decision:** further ontology elaboration is not the default next step.

**Reason:** the engineering and conceptual framework is sufficiently mature; the current bottleneck is empirical response-protocol validation and ethics/recruitment setup. Resume ontology changes only if human calibration or new prior art forces revision.
