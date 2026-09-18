# ARIS4C010 · Concept-space specification v0.1

## Purpose

This document answers the project's first design question: **what must be represented before "ask as few questions as possible to identify any concept" becomes well-defined?**

It deliberately avoids claiming that concepts form one globally MECE tree. Semantic phenomena cross-cut one another. The design goal is therefore:

- local mutual exclusivity where scientifically defensible;
- cross-axis orthogonality where possible;
- explicit multi-labeling where reality is genuinely overlapping;
- typed relations instead of forcing all structure into `is-a`.

A taxonomy is one projection of the representation, not the representation itself.

---

## Axis A · Target / representation level

Before asking semantic questions, identify what kind of target the game treats as the answer.

- **A1 string / orthographic form** — e.g. the character sequence "bank";
- **A2 word token** — one occurrence in an utterance;
- **A3 lexeme** — BANK as a vocabulary item;
- **A4 sense / synset-like meaning** — financial-bank vs river-bank;
- **A5 concept / intension** — the abstract meaning or rule of application;
- **A6 referent / extension member** — a particular bank branch, person, event;
- **A7 proposition** — something truth-evaluable;
- **A8 rule / operation / procedure** — algorithm, game rule, transformation;
- **A9 metalinguistic target** — a word, sentence, concept or category as an object of discourse.

A benchmark must not silently switch levels. "Is it located in Europe?" may be legitimate for a referent and category error for an orthographic string.

---

## Axis B · Ontological kind

This axis should be aligned where useful with upper-ontology distinctions but remain language-friendly.

### B1 continuant-like entities
- material object;
- organism / agent;
- substance / mass;
- part / boundary / region;
- artifact;
- biological structure.

### B2 occurrent-like entities
- event;
- process;
- action;
- change / transition;
- state / condition.

### B3 dependent / predicative entities
- quality / property;
- disposition / capacity;
- relation;
- role;
- function.

### B4 abstract / formal entities
- number;
- set / class;
- geometric object;
- logical object;
- algorithm / formal structure;
- measure / unit.

### B5 informational entities
- text;
- image;
- melody;
- code;
- theory/model;
- data structure.

### B6 mental / phenomenal entities
- belief;
- desire;
- memory;
- emotion;
- sensation / qualia-like experience.

### B7 social / institutional / normative entities
- organization;
- office/status;
- law/rule;
- money-like institution;
- right/obligation;
- social category.

### B8 fictional / represented entities
- fictional individual;
- fictional kind;
- mythic entity;
- stipulated thought-experiment entity.

A target may occupy more than one branch at different representation levels. That is expected, not an ontology failure.

---

## Axis C · Logical / compositional form

"All concepts" cannot be approximated by listing nouns. The representation needs operators.

- **C0 primitive relative to current vocabulary**;
- **C1 conjunction** (A \land B);
- **C2 disjunction** (A \lor B);
- **C3 negation / complement** (\neg A);
- **C4 set difference / exclusion** (A \land \neg B);
- **C5 relation-defined** (R(x,y));
- **C6 quantified** (all / some / exactly n / most / none);
- **C7 comparative / superlative**;
- **C8 modal** (possible / necessary / permitted / required);
- **C9 temporal** (was / will / until / during);
- **C10 counterfactual**;
- **C11 recursive / inductive**;
- **C12 higher-order** (properties of properties, concepts of concepts);
- **C13 quotation / metalinguistic construction**.

Negation always requires an explicit universe (U):

[
\neg A = U \setminus A.
]

"Not a mammal" over animals is not the same extension as "not a mammal" over all representable entities.

---

## Axis D · Referential / existence / modal status

Do not collapse all non-actual targets into "fictional."

- **D1 presently actual**;
- **D2 past actual**;
- **D3 future / contingent anticipated**;
- **D4 possible but non-actual**;
- **D5 fictional / story-internal**;
- **D6 hypothetical / stipulated**;
- **D7 currently empty description** — meaningful intension with no current satisfier;
- **D8 impossible / necessarily empty** — inconsistent constraints under the adopted logic;
- **D9 existence status itself unknown/contested**.

This axis lets the system distinguish "unicorn", "the current king of France", and "round square."

---

## Axis E · Boundary and gradedness

- **E1 crisp / classical**;
- **E2 scalar with explicit threshold**;
- **E3 scalar with context-sensitive threshold**;
- **E4 prototype / family-resemblance category**;
- **E5 vague / borderline / sorites-prone**;
- **E6 probabilistic / dispositional**;
- **E7 convention-dependent boundary**.

A benchmark should store both category labels and confidence/inter-annotator distributions when boundaries are not crisp.

---

## Axis F · Context dependence

- **F1 context-invariant for benchmark purposes**;
- **F2 speaker-relative / indexical** (I, you);
- **F3 spatial/deictic** (here, nearby);
- **F4 temporal/deictic** (today, recently);
- **F5 comparison-class dependent** (tall, expensive);
- **F6 discourse/anaphoric** (the former, that one);
- **F7 social/institutional-context dependent**;
- **F8 possible-world / counterfactual-context dependent**;
- **F9 perspective/evaluator dependent**.

Context variables should be frozen or explicitly queried. "CONTEXT REQUIRED" is not the same as "UNKNOWN."

---

## Axis G · Grounding / access mode

How can an answerer know or discriminate the target?

- lexical / definitional;
- encyclopedic / factual;
- perceptual;
- spatial;
- motor / embodied;
- interoceptive / phenomenal;
- social / normative;
- mathematical / formal proof;
- testimonial / source-dependent;
- multimodal / exemplar-based;
- ostensive only or primarily ostensive.

This axis is essential for concepts such as odors, pains and colors, which may be discriminable without compact verbal definitions.

---

## Axis H · Epistemic and computability status

- **H1 directly decidable from stored representation**;
- **H2 decidable with finite external lookup/measurement**;
- **H3 empirically uncertain / not currently known**;
- **H4 observer-limited / inaccessible to this oracle**;
- **H5 probabilistic / stochastic answer**;
- **H6 underdetermined by available context**;
- **H7 undecidable in general for the relevant problem class**;
- **H8 computationally decidable but practically intractable**.

False, unknown, inaccessible and undecidable are different states.

---

## Axis I · Reflexivity and semantic pathology

- **I1 ordinary/non-reflexive**;
- **I2 metalinguistic**;
- **I3 self-referential but non-paradoxical**;
- **I4 circular definition**;
- **I5 inconsistent description**;
- **I6 liar-like / truth-semantic paradox**;
- **I7 set-theoretic / membership paradox pattern**;
- **I8 category error / type violation**;
- **I9 presupposition failure**.

For inconsistent information, the benchmark must not silently adopt explosion. A paraconsistent response layer is one candidate design.

---

## Axis J · Lexicalization and expressibility

- **J1 conventional lexical item exists**;
- **J2 conventional multiword expression exists**;
- **J3 readily paraphrasable but unlexicalized**;
- **J4 constructible compositionally only in context**;
- **J5 primarily ostensive / exemplar-grounded**;
- **J6 weakly ineffable relative to a language or expressive resource**;
- **J7 strong-ineffability boundary condition**.

J7 is not treated as an ordinary benchmark class. If a participant cannot form or preserve the target representation, ordinary question answering about it is not defined.

---

# Response-state ontology

Strict binary Twenty Questions assumes

[
A(c,q)\in\{YES,NO\}.
]

ARIS4C010 will evaluate at least two protocols.

## Protocol P2 · strict binary
- YES
- NO

Ambiguous cases must be resolved by a frozen interpretation policy. This protocol measures the cost of forcing semantic phenomena through a one-bit channel.

## Protocol P6 · semantically explicit
- YES
- NO
- BORDERLINE / DEGREE-DEPENDENT
- UNKNOWN / EPISTEMICALLY UNRESOLVED
- UNDEFINED / NOT-APPLICABLE / PRESUPPOSITION-FAILURE
- BOTH / INCONSISTENT under represented information

Context dependence should ideally trigger a context subquery before scoring rather than be merged with UNKNOWN.

The six labels are not claimed to be metaphysically exhaustive. They are an engineering interface to prevent predictable category errors.

---

# Formal identifiability

Let (C) be a candidate set, (Q) an admissible query family, (R) a response alphabet, and

[
A:C\times Q\rightarrow R
]

the idealized oracle.

Define a signature

[
\sigma_Q(c)=(A(c,q))_{q\in Q}.
]

For a finite closed world, exact identification is possible iff (sigma_Q) is injective.

Two candidates with identical signatures are **query-equivalent** under (Q). No adaptive strategy using only (Q) can distinguish them.

This makes ontology evaluation quantitative:

- number and size of collision classes;
- pairwise separation rate;
- minimum separating query subset;
- adaptive expected/worst-case depth;
- robustness when answers are noisy or non-binary.

---

# What "MECE" means here

The project should not advertise the entire concept universe as globally MECE.

A better claim is:

> ARIS4C010 uses a **typed factorization** designed to minimize accidental overlap between semantic dimensions while preserving genuine cross-classification.

Local fields can be MECE (e.g. target level in a frozen task, benchmark response protocol). Global semantic reality often cannot.
