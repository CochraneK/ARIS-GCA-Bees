# ARIS4C010 · Novelty audit

**Current verdict:** PROMISING, NARROWED, NOT YET FROZEN  
**Date:** 2026-09-18

## Claims that are already taken

ARIS4C010 must not claim novelty for any of the following:

- using binary questions to identify a hidden target;
- the \(\log N\) information lower bound;
- entropy / expected information gain as question utility;
- generalized binary search;
- optimal decision-tree formulations;
- query learning of concepts;
- teaching dimension;
- choosing a minimum feature/test set that uniquely identifies all items;
- minimal distinguishing descriptions for known referents;
- active concept learning relative to formal ontologies;
- concept lattices / Formal Concept Analysis;
- WordNet-like lexical sense organization;
- building semantic or commonsense knowledge graphs;
- rational/pragmatic reference games that trade off informativeness and utterance cost;
- letting LLMs play Twenty Questions;
- using Twenty Questions to evaluate world knowledge;
- adaptive natural-language elicitation via LLMs;
- the philosophical existence of vagueness, paradox, non-classical logics or ineffability.

## Completed collision audit

### A. Referring Expression Generation — close static analogue, not fatal

Classical REG formalizes a target referent, a contrast set of distractors, and a set of properties that should apply to the target while excluding every distractor. Full-brevity/minimal distinguishing descriptions therefore overlap strongly with the **static semantic separation** part of 010.

Consequence:

> 010 cannot claim that selecting a smallest set of semantic properties that uniquely identifies a target is new.

Difference that remains:

- REG normally assumes the speaker already knows the target and **emits a description**;
- 010 studies a guesser who does **not** know the target and adaptively chooses questions from response history;
- 010's candidate universe includes senses, abstract/compositional concepts, vague/contextual cases, open-world targets and pathological cases rather than only contextual referents.

REG is therefore a required baseline and conceptual ancestor.

### B. Description-logic active concept learning — close formal analogue, not fatal

Funk, Jung & Lutz (IJCAI 2021) explicitly learn concepts and conjunctive queries in the presence of an ontology using Angluin-style membership and equivalence queries, with polynomial learnability results for selected description-logic classes.

Consequence:

> 010 cannot claim that "interactive query learning of concepts under an ontology" is new.

Difference that remains:

- their target is a formal concept/query in a specified description language;
- 010 asks how **semantic admissibility, natural-language answerability and heterogeneous concept types** alter identification complexity;
- 010 explicitly compares classical binary forcing with non-binary semantic states and includes open-world/pathological boundaries.

### C. Ontology inseparability — adjacent but different object

Description-logic work studies whether ontologies are indistinguishable with respect to classes of concepts/queries. This is useful formal language for "what can a query language distinguish?" but generally concerns equivalence/replacement of knowledge bases, not a Twenty-Questions-style hidden target policy.

### D. Rational Speech Acts / pragmatic reference games — efficiency baseline

RSA and related reference-game models already formalize speakers selecting informative utterances under cost and listeners inferring referents.

Consequence:

> "informativity minus communication cost" is not a novel principle.

010 should compare its semantic-query cost to pragmatic efficient-communication baselines, while keeping the distinction between **speaker-chosen messages** and **listener-chosen diagnostic questions** explicit.

## Surviving novelty wedge

A defensible contribution is now narrower and stronger.

### N1 · Semantic admissibility as a restriction on adaptive query complexity

Define \(Q_{sem}\subset Q_{all}\), where questions must be meaningful for the target type, interpretable, answerable under an explicit context/oracle model, and compliant with a response protocol.

Measure **Semantic Query Overhead** relative to unrestricted partitions.

This is more specific than generic information gain, Test Cover, REG or description-logic query learning.

### N2 · Controlled semantic breadth

Benchmark target levels and ontological categories, then deliberately add:

- lexical ambiguity;
- logical composition;
- vague predicates;
- indexicals/context;
- empty and impossible descriptions;
- self-reference/paradox;
- empirical unknowns;
- undecidable cases;
- ostensive / weakly ineffable cases;
- open-world withheld targets.

The contribution is not sheer vocabulary size but **coverage of qualitatively different identification regimes**.

### N3 · Non-classical response semantics as an experimental variable

Separate at minimum:
- false;
- epistemically unknown;
- borderline/graded;
- undefined/not-applicable/presupposition failure;
- inconsistent/both.

Then measure the cost and error introduced when these are forcibly collapsed to YES/NO.

### N4 · A unified boundary theorem/benchmark story

Distinguish:
- finite closed-world identifiability;
- infinite candidate sets with no uniform finite worst-case bound;
- open-world ontology failure;
- empirical unknowns;
- computational undecidability;
- strong ineffability as failure of target representability itself.

The project is strongest when these are treated as **different failure modes**, not one miscellaneous "hard concepts" bucket.

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

The candidate architecture is a typed semantic graph / factorized coordinate system plus compositional operators.

## Remaining high-risk prior-art audits

The following could still narrow the contribution:

1. minimal distinguishing description / REG work beyond concrete visual domains;
2. description-logic concept learning with richer query/answer protocols;
3. active feature acquisition with abstention and missing/not-applicable values;
4. interactive clarification-question generation;
5. diagnostic questioning over knowledge graphs;
6. pragmatic efficient communication with abstract/compositional meanings;
7. open-world active learning / novelty detection;
8. multi-valued logic in interactive diagnosis.

## Falsification of novelty

Downgrade or split 010 if a prior work is found that already combines most of:

1. broad concept ontology spanning lexical, abstract and compositional targets;
2. adaptive minimum-query identification;
3. explicit comparison to an unrestricted information lower bound;
4. non-binary semantic answer states;
5. open-world/OOS targets;
6. pathological cases such as vagueness, empty/impossible descriptions or paradox;
7. a unified reproducible benchmark.

Finding isolated versions of these components does not establish novelty of their integration, but every such finding must narrow individual claims.

## Current recommendation

Proceed to Benchmark v0.

Use **"Universal Concept Identification" only as a working program name**. In formal claims, always qualify universality as:

> relative to an explicit representable concept universe, admissible query language, response protocol, context model and oracle.

