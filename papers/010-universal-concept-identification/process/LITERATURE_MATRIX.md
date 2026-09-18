# ARIS4C010 · Literature / prior-art matrix

**Audit date:** 2026-09-18  
**Purpose:** prevent novelty inflation by separating already-solved subproblems from the integration gap.

| Strand | Representative source | What is already established | Consequence for 010 |
|---|---|---|---|
| Exact query learning | Dana Angluin, *Queries and Concept Learning*, Machine Learning 2, 319–342 (1988), DOI 10.1007/BF00116828 | Membership, equivalence, subset, superset, disjointness and exhaustiveness queries; query-learning lower bounds | Query-based concept learning is not novel |
| Teaching complexity | Goldman & Kearns, *On the Complexity of Teaching*, JCSS 50(1), 20–31 (1995), DOI 10.1006/jcss.1995.1003 | Teaching dimension formalizes examples sufficient to uniquely identify a target concept | "How much evidence identifies a concept?" is not novel by itself |
| Generalized binary search | Nowak, *The Geometry of Generalized Binary Search*, IEEE TIT 57(12), 7893–7906 (2011), DOI 10.1109/TIT.2011.2169298 | Greedy near-balanced splitting can achieve order-log-N query complexity under structural conditions; noisy variant included | Information-gain / balanced splitting is baseline, not contribution |
| Test Cover | Gutin, Muciaccia & Yeo (2013), *Information Processing Letters*, DOI 10.1016/j.ipl.2012.12.008, plus earlier Test Cover work | Minimum subset of binary tests that separates every item pair; NP-hard | "Smallest set of attributes sufficient to distinguish all candidates" has a known combinatorial core |
| Referring Expression Generation | Dale & Reiter tradition; modern overview/reanalysis e.g. *Rethinking symbolic and visual context in Referring Expression Generation* (2023) | A distinguishing description contains properties true of a known target and sufficient to exclude every distractor; minimal descriptions and heuristics are longstanding | Static target-description minimization is not novel; 010 must focus on hidden-target adaptive questioning and broader semantic regimes |
| Description-logic active learning | Funk, Jung & Lutz, *Actively Learning Concepts and Conjunctive Queries under ELr-Ontologies*, IJCAI 2021, DOI 10.24963/ijcai.2021/260 | Concepts/queries can be actively learned relative to ontologies with membership/equivalence queries for selected DL classes | "Active concept learning under an ontology" is not novel |
| Ontology inseparability | Botoeva et al., *Inseparability and Conservative Extensions of Description Logic Ontologies: A Survey* (2017/2018) | Formal notions of concept/query inseparability characterize when ontologies cannot be distinguished by query languages | Useful formal neighbor for expressive limits; different target from hidden-concept identification |
| Formal Concept Analysis | Ganter & Wille, *Formal Concept Analysis: Mathematical Foundations*, 2nd ed. (2024) | Object–attribute formal contexts and concept lattices mathematically organize concepts/hierarchies | Concept lattices are candidate representations; not novelty |
| Lexical ontology | Miller, *WordNet: A Lexical Database for English*, CACM 38(11), 39–41 (1995), DOI 10.1145/219717.219748 | Synsets represent lexicalized senses linked by semantic relations | Use as lexical-sense backbone; WordNet alone is not universal concept space |
| Multilingual/common-sense networks | BabelNet; ConceptNet | Large graphs integrate lexical, encyclopedic and commonsense relations | Graph construction itself is not the contribution |
| Upper ontology | BFO / DOLCE / SUMO traditions | Typed high-level distinctions such as objects/processes/qualities/social or conceptual entities, with different philosophical commitments | 010 should compare/adapt rather than claim a metaphysically final ontology |
| Semantic feature norms | McRae et al. and later feature-norm resources | Human concepts can be represented by weighted produced features, especially concrete concepts | Useful query bank / human baseline; coverage is uneven for abstract/pathological concepts |
| Pragmatic reference games | Rational Speech Acts and related work | Speakers/listeners optimize or infer informative referring expressions under priors and utterance costs | Informativity-cost tradeoff and efficient reference are established baselines |
| Cognitive Twenty Questions | Experimental psychology using Twenty Questions/category questioning | Human search efficiency depends on broad category questions and semantic structure | Human strategy effects are established; 010 should quantify semantic coverage/overhead |
| BIG-bench Twenty Questions | BIG-bench `twenty_questions` task | Two model instances communicate a concept via yes/no turns; authors explicitly note arbitrary categories and suggest a more comprehensive ontology | Very close motivation; ontology completion remains open in that benchmark |
| 20Q world-knowledge benchmark | De Bruyn et al., GEM 2022 | Twenty Questions used to probe LM world knowledge with overlap controls | LLM 20Q benchmarking is established |
| Adaptive elicitation | Wang, Zollo, Zemel & Namkoong, ICML 2025, *Adaptive Elicitation of Latent Information Using Natural Language* | Natural-language question selection that actively reduces uncertainty; Twenty Questions benchmark uses hundreds of concrete objects and a large question bank | Strategic next-question optimization is established and should be a strong baseline |
| Current public LLM benchmark | Deep20Bench v1.1, Sept 2026 (non-peer-reviewed benchmark) | Multi-turn hidden-subject identification with graded YES/NO directions plus UNKNOWN | Confirms active current interest; not evidence for semantic universality |
| Vagueness / sorites | Formal semantics and philosophical logic | Borderline cases and competing semantics for vague predicates | Do not collapse borderline into ordinary false/unknown |
| Paraconsistency | Paraconsistent-logic literature | Contradictory information need not entail arbitrary conclusions (non-explosion) | Useful for inconsistent targets/knowledge states; theory itself is not new |
| Ineffability | Sebastian Gäb, *Ineffability: the Very Concept*, Philosophia 48 (2020), DOI 10.1007/s11406-020-00198-2 | Distinguishes weak from strong ineffability and linguistic from cognitive limits | Strong ineffability should be modeled as an outer boundary, not an ordinary target label |

## Closest technical neighbors after the expanded audit

There is no longer one single closest neighbor; 010 sits at the intersection of four mature lines.

1. **Wang et al. (ICML 2025):** strongest adaptive natural-language elicitation neighbor.
2. **Referring Expression Generation:** strongest static semantic-discrimination neighbor.
3. **Description-logic active learning:** strongest formal ontology + interactive-query neighbor.
4. **RSA/reference games:** strongest efficient-communication/pragmatic neighbor.

The project survives only if it does not repackage any one of these.

## Current integration gap

The live audit has not yet found a work whose primary object is all of the following together:

> adaptive identification of a hidden target across deliberately heterogeneous concept regimes, with an explicit admissible semantic query language, response states that distinguish false/unknown/borderline/undefined/inconsistent, open-world withholding, pathological semantic cases, and query cost measured against an unrestricted information-theoretic baseline.

This is a **provisional gap**, not a final novelty claim.

## Search queue before manuscript freeze

- referring expression generation for abstract/non-visual meanings;
- discriminating descriptions in description logics;
- active feature acquisition with missing/abstaining/non-applicable values;
- open-world active concept learning;
- clarification-question generation optimized for disambiguation;
- diagnostic questioning over knowledge graphs;
- multi-valued interactive diagnosis;
- reference games with compositional or paradoxical meanings;
- minimum identifying codes / separating systems beyond binary Test Cover.

