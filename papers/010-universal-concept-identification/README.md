# ARIS4C010 · Beyond Twenty Questions

**Status:** design + live literature audit complete; implementation/pilot next

## Canonical question

> What is the minimal semantic structure necessary for finite-query identification of arbitrary human-representable concepts, and how much additional query cost is introduced when questions must be semantically meaningful, answerable, and robust to vagueness, context, nonexistence, contradiction, self-reference, undecidability, and limits of expressibility?

This is not primarily a project about getting an LLM to become better at a parlour game. The scientific target is the boundary between **information-theoretic identifiability** and **semantic identifiability**.

## The key correction to the original intuition

A complete tree-shaped taxonomy of everything is **not** a mathematical prerequisite.

For a target set (C) and admissible query family (Q), exact identification requires the query family to be **separating**:

[
\forall c_i \neq c_j,\; \exists q \in Q: A(c_i,q) \neq A(c_j,q).
]

Equivalently, the response signature induced by all admissible questions must be injective over the candidate set.

The static problem of finding the smallest subset of binary questions that still separates every pair is the classical **Test Cover** problem. Therefore the scientifically useful question is not "Can we write the perfect taxonomy?" but:

> **What is the smallest semantically admissible separating basis for a target concept universe, and what adaptive query policy minimizes identification cost?**

## Three regimes that must not be conflated

### 1. Finite closed world
If there are (N) known candidates and arbitrary noiseless binary partitions are allowed, the worst-case information lower bound is

[
\lceil \log_2 N \rceil.
]

Twenty binary answers can encode at most 1,048,576 leaves; twenty-one encode at most 2,097,152.

### 2. Infinite but enumerable world
With a finite response alphabet there is no **uniform finite worst-case** question bound for infinitely many candidates. Individual targets may still have finite but unbounded code lengths, and a non-uniform prior can permit finite expected length when its entropy is finite.

### 3. Open semantic world
New words, senses, compositional concepts and context-created referents can enter after the ontology is built. A universal system therefore needs an explicit **out-of-support/open-world state**, not forced guessing.

## Main object of study: Semantic Query Overhead

Let (L^*_{all}) be the optimal expected number of unrestricted information-theoretic questions and (L^*_{sem}) the optimum under a specified family of human-interpretable semantic questions.

Define:

[
\Delta_{sem}=L^*_{sem}-L^*_{all}
]

and the normalized semantic overhead

[
\rho_{sem}=\frac{L^*_{sem}}{\max(H(C),\epsilon)}
]

for binary questions when entropy (H(C)) is measured in bits.

The core empirical question becomes: **which kinds of concepts incur the largest semantic overhead, and why?**

## Working hypotheses

- **H1 · A single inheritance taxonomy is insufficient.** A typed multi-axis concept representation will produce fewer unresolved collisions than a single is-a tree at matched query budget.
- **H2 · Semantic constraints have measurable cost.** Natural, answerable questions require more queries than arbitrary partitions, with especially large overhead for vague, context-dependent and compositional targets.
- **H3 · Binary forcing is sometimes the wrong channel.** Allowing carefully defined states such as UNKNOWN, BORDERLINE, UNDEFINED/NOT-APPLICABLE and BOTH/INCONSISTENT will reduce oracle inconsistency even when it does not always reduce bit cost.
- **H4 · Logical closure matters.** Negation, conjunction, disjunction, relations, quantification, modality and counterfactual composition cannot be represented reliably by a noun taxonomy alone.
- **H5 · Open-world detection is necessary.** A system allowed to declare OUT-OF-SUPPORT will make fewer confident false identifications when the target is absent from its current ontology.
- **H6 · Pathological cases expose the boundary.** Empty reference, impossible descriptions, self-reference, paradox and undecidability require distinct handling rather than one generic "unknown" bucket.
- **H7 · Strong ineffability is a boundary condition, not an ordinary class.** If an answerer can stably represent a target and judge arbitrary admissible questions about it, the target is representable enough to participate in the game; genuinely strong-ineffable content therefore lies outside the normal candidate universe.

## Concept representation

The project uses an **orthogonal typed coordinate system / hypergraph**, not a claim that one universal MECE tree already exists.

Core axes:

1. target/representation level;
2. ontological kind;
3. logical/compositional form;
4. referential and modal status;
5. boundary/gradedness;
6. context dependence;
7. grounding and access mode;
8. epistemic/computability status;
9. reflexivity/pathology;
10. lexicalization/expressibility.

See `process/CONCEPT_ONTOLOGY.md`.

## Prior-art boundary

Existing work already covers major pieces:

- Rényi–Ulam / generalized binary search / exact query learning: query complexity and optimal splitting;
- Test Cover: minimum static separating attributes;
- teaching dimension: examples sufficient to identify concepts;
- Formal Concept Analysis and lexical/upper ontologies: organization of concepts;
- BIG-bench Twenty Questions, 20Q, ICML 2025 adaptive elicitation, and current LLM benchmarks: machine performance at the game;
- philosophical and logical work: vagueness, paraconsistency, reference and ineffability.

The novelty claim must therefore **not** be "we apply information gain to Twenty Questions" or "we build an ontology."

The defensible wedge is the **formal integration of semantic admissibility, ontology coverage, open-world support, non-classical answer states and adversarial concept classes into one query-complexity benchmark**, with semantic overhead measured relative to unrestricted identification.

## Relationship to the existing Language Periodic System project

They are distinct.

- **Language Periodic System** asks whether cross-linguistic structural diversity has periodic/circular geometry.
- **ARIS4C010** asks what concept/query structure is sufficient for efficient concept identification.

The former studies geometry among languages; the latter studies identifiability in semantic/concept space.

## Next hard gate

Before strong novelty language is permitted:

1. complete the closest-prior-work matrix;
2. freeze the formal response protocol and open-world semantics;
3. build Benchmark v0 with ordinary + adversarial concept strata;
4. run a small exact/greedy decision-tree pilot;
5. compare single-tree, multi-axis and unrestricted baselines;
6. conduct human/LLM answer-consistency checks before treating any generated concept-question matrix as ground truth.
