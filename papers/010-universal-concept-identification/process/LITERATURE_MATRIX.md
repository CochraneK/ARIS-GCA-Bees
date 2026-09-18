# ARIS4C010 · Literature / prior-art matrix

**Audit date:** 2026-09-18  
**Purpose:** prevent novelty inflation by separating already-solved subproblems from the integration gap.

| Strand | Representative source | What is already established | Consequence for 010 |
|---|---|---|---|
| Exact query learning | Dana Angluin, *Queries and Concept Learning*, Machine Learning 2, 319–342 (1988), DOI 10.1007/BF00116828 | Membership, equivalence, subset, superset, disjointness and exhaustiveness queries; query-learning lower bounds | Query-based concept learning is not novel |
| Teaching complexity | Goldman & Kearns, *On the Complexity of Teaching*, JCSS 50(1), 20–31 (1995), DOI 10.1006/jcss.1995.1003 | Teaching dimension formalizes examples sufficient to uniquely identify a target concept | "How much evidence identifies a concept?" is not novel by itself |
| Generalized binary search | Nowak, *The Geometry of Generalized Binary Search*, IEEE TIT 57(12), 7893–7906 (2011), DOI 10.1109/TIT.2011.2169298 | Greedy near-balanced splitting can achieve order-log-N query complexity under structural conditions; noisy variant included | Information-gain / balanced splitting is baseline, not contribution |
| Test Cover | de Bontridder et al.; Gutin et al., Test Cover literature; e.g. Gutin, Muciaccia & Yeo (2013), DOI 10.1016/j.ipl.2012.12.008 | Minimum subset of binary tests that separates every item pair; NP-hard | The user's "minimal taxonomy/features sufficient to identify everything" has a known combinatorial core |
| Formal Concept Analysis | Ganter & Wille, *Formal Concept Analysis: Mathematical Foundations*, 2nd ed. (2024) | Object–attribute formal contexts and concept lattices mathematically organize concepts/hierarchies | Concept lattices are candidate representations; not novelty |
| Lexical ontology | Miller, *WordNet: A Lexical Database for English*, CACM 38(11), 39–41 (1995), DOI 10.1145/219717.219748 | Synsets represent lexicalized senses linked by semantic relations | Use as lexical-sense backbone; WordNet alone is not universal concept space |
| Multilingual semantic networks | BabelNet; ConceptNet | Large graphs integrate lexical, encyclopedic and commonsense relations | Graph construction itself is not the contribution |
| Upper ontology | BFO / DOLCE / SUMO traditions | Typed high-level distinctions such as objects/processes/qualities/social or conceptual entities, with different philosophical commitments | 010 should compare/adapt rather than claim a metaphysically final ontology |
| Semantic feature norms | McRae et al. and later feature-norm resources | Human concepts can be represented by weighted produced features, especially concrete concepts | Useful query bank / human baseline; coverage is uneven for abstract/pathological concepts |
| Cognitive Twenty Questions | Experimental psychology using Twenty Questions/category questioning | Humans improve efficiency by asking broad category questions; semantic structure affects search behavior | Human strategy effects are established; 010 should quantify semantic coverage/overhead |
| BIG-bench Twenty Questions | BIG-bench `twenty_questions` task | Two model instances communicate a concept via yes/no turns; task authors explicitly note arbitrary categories and propose a more comprehensive ontology | Very close motivation; ontology completion remains open in that benchmark |
| 20Q world-knowledge benchmark | De Bruyn et al., GEM 2022 | Twenty Questions used to probe LM world knowledge with overlap controls | LLM 20Q benchmarking is established |
| Adaptive elicitation | Wang, Zollo, Zemel & Namkoong, ICML 2025, *Adaptive Elicitation of Latent Information Using Natural Language* | Natural-language question selection that actively reduces uncertainty; Twenty Questions dataset built around hundreds of concrete objects and a large question bank | Strategic next-question optimization is established and should be a strong baseline |
| Current public LLM benchmark | Deep20Bench v1.1, Sept 2026 (non-peer-reviewed benchmark) | Multi-turn hidden-subject identification with YES / RATHER YES / RATHER NO / NO / UNKNOWN | Confirms active current interest; not evidence for semantic universality |
| Vagueness / sorites | Formal semantics and philosophical logic | Borderline cases and multiple competing semantics for vague predicates | Do not collapse borderline into ordinary false/unknown |
| Paraconsistency | Paraconsistent-logic literature | Contradictory information need not entail arbitrary conclusions (non-explosion) | Useful for inconsistent targets/knowledge states; theory itself is not new |
| Ineffability | Sebastian Gäb, *Ineffability: the Very Concept*, Philosophia 48 (2020), DOI 10.1007/s11406-020-00198-2 | Distinguishes weak from strong ineffability and linguistic from cognitive limits | Strong ineffability should be modeled as an outer boundary, not simply another ordinary target label |

## Closest collision discovered in the live audit

The strongest current technical neighbor is **Wang et al. (ICML 2025)**: it directly optimizes adaptive natural-language elicitation and evaluates on Twenty Questions. Its object dataset is therefore a valuable bridge benchmark.

The strongest conceptual neighbor is the **BIG-bench Twenty Questions limitation note**, which explicitly says the communicated concepts/categories are arbitrary and suggests structuring them into a more comprehensive ontology.

Neither source, in the reviewed material, makes the central ARIS4C010 problem the primary object:

> characterize query-identifiability across lexical levels, ontological types, logical composition, open-world targets and non-classical semantic/epistemic cases, and measure the query cost of semantic admissibility relative to unrestricted partitions.

## High-priority searches still required before manuscript claims

- "semantic query complexity" + concept identification;
- ontology-based optimal question generation;
- diagnostic decision trees over description logics / knowledge graphs;
- active learning with abstention / undefined / multi-valued semantic responses;
- exact identification of compositional concepts;
- query learning under open-world ontologies;
- computational treatments of indexicals, empty descriptions and paradox in interactive identification;
- minimum distinguishing description / referring expression generation and its relationship to this task.

The last item is especially important: **referring-expression generation** may contain a closer formal analogue than ordinary Twenty Questions and must be audited before novelty is frozen.
