# ARIS4C010 · Novelty audit

**Current verdict:** PROMISING BUT NOT FROZEN  
**Date:** 2026-09-18

## Claims that are already taken

ARIS4C010 must not claim novelty for any of the following:

- using binary questions to identify a hidden target;
- the (\log N) information lower bound;
- entropy / expected information gain as question utility;
- generalized binary search;
- optimal decision-tree formulations;
- query learning of concepts;
- teaching dimension;
- choosing a minimum feature/test set that uniquely identifies all items;
- concept lattices / Formal Concept Analysis;
- WordNet-like lexical sense organization;
- building semantic or commonsense knowledge graphs;
- letting LLMs play Twenty Questions;
- using Twenty Questions to evaluate world knowledge;
- adaptive natural-language elicitation via LLMs;
- the philosophical existence of vagueness, paradox, non-classical logics or ineffability.

## Surviving novelty wedge

A defensible contribution would combine four pieces that adjacent literatures usually separate.

### N1 · Semantic admissibility as an explicit restriction on query complexity

Define (Q_{sem}\subset Q_{all}), where questions must be meaningful for the target type, interpretable, answerable under an explicit context/oracle model, and compliant with a response protocol.

Measure the resulting **Semantic Query Overhead** rather than merely reporting game score.

### N2 · Typed coverage beyond ordinary concrete objects

Benchmark representation levels and ontological categories, then deliberately add logical composition, vague/contextual cases and open-world targets.

The goal is not "more words"; it is controlled **semantic coverage**.

### N3 · Non-classical response semantics

Separate at minimum:
- false;
- epistemically unknown;
- borderline/graded;
- undefined/not applicable/presupposition failure;
- inconsistent/both.

Then quantify what goes wrong when all of these are forced into binary YES/NO.

### N4 · Identification boundary

Distinguish:
- finite closed-world identifiability;
- infinite but unbounded identification;
- open-world ontology failure;
- empirical unknowns;
- computational undecidability;
- strong-ineffability as failure of target representability itself.

This provides a principled answer to when "universal Twenty Questions" is impossible rather than simply difficult.

## Why a single taxonomy is not the expected solution

A single `is-a` tree cannot naturally encode all of:

- polysemy and representation level;
- relations and roles;
- negation/complement relative to a universe;
- conjunction/disjunction;
- modality and counterfactuals;
- indexicals and context variables;
- vague predicates;
- empty/impossible descriptions;
- metalinguistic/self-referential targets.

The candidate architecture is therefore a typed semantic graph / factorized coordinate system plus compositional operators.

## Potential fatal collisions to audit

### A. Referring expression generation
This field asks how to generate properties that uniquely distinguish a referent from distractors. It may overlap strongly with static semantic separation and minimal descriptions.

**Action:** dedicated literature audit before claiming the "minimal semantic basis" as a new formulation.

### B. Description logics / ontology query answering
Knowledge-representation work may already study minimal distinguishing concepts or query sets over formal ontologies.

**Action:** search DL/OWL concept learning, distinguishing descriptions, query inseparability and ontology-mediated query literature.

### C. Active feature acquisition / diagnosis
Cost-sensitive test selection and abstention are mature in diagnosis and ML.

**Action:** novelty must reside in semantic breadth and formal cross-regime integration, not the optimization machinery.

### D. Pragmatics and reference games
RSA/pragmatic language games may model speaker/listener identification under rational communication.

**Action:** compare semantic-query overhead to pragmatic efficient communication and reference-game literature.

## Falsification of novelty

Downgrade or split 010 if a prior work is found that already does all or nearly all of:

1. broad concept ontology spanning lexical/abstract/compositional targets;
2. adaptive minimum-query identification;
3. explicit comparison to an unrestricted information lower bound;
4. non-binary semantic answer states;
5. open-world/OOS targets;
6. pathological cases such as vagueness, empty/impossible descriptions or paradox;
7. a unified benchmark with reproducible metrics.

Finding isolated versions of these components does **not** establish novelty of their combination, but it should narrow claims.

## Current recommendation

Proceed to Benchmark v0 and a dedicated referring-expression / description-logic audit in parallel. Do **not** yet write the manuscript title as "Universal" without the qualifier **relative to a specified representable concept universe and query language**.
