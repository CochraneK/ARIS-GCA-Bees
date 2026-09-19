# ARIS4C010 · Literature / prior-art matrix

**Audit date:** 2026-09-19  
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
| Ontology-guided hierarchical elicitation | Agafonov, Ponomarev & Smirnov, *Ontology-Guided Hierarchical Preference Elicitation with Bayesian Active Querying*, ICAART 2026, DOI 10.5220/0014476800004052 | Starts from semantically retrieved candidates in a rooted product ontology, then asks binary subtree-relevance questions chosen with Bayesian active-query strategies under a turn budget | **Major structural collision:** ontology-guided active querying in a hierarchy is already published; 010 must not claim this. Difference must come from heterogeneous semantic regimes, admissibility/error states, open-world/pathological cases, and explicit overhead versus unrestricted partitions |
| Proactive information gathering | Huang et al., *Teaching Language Models To Gather Information Proactively*, Findings of EMNLP 2025, DOI 10.18653/v1/2025.findings-emnlp.843 | Trains LMs to identify missing task information and ask targeted clarification questions; includes human evaluation of question quality | Proactive clarification and elicitation of missing information are established; 010 is about hidden-target identifiability/query cost and semantic answer-state validity, not general assistant proactivity |
| Referential ambiguity + clarification | *Referential ambiguity and clarification requests: comparing human and LLM behaviour*, CRAC 2025, DOI 10.18653/v1/2025.crac-1.1 | Empirically studies when humans and LLMs issue clarification requests under referential ambiguity and finds weak human ambiguity→clarification linkage / low human–LLM correlation | Supports treating context requests as an empirical behavior rather than an axiom; useful comparator for P6+CONTEXT |
| Adaptive group elicitation | Ding et al., *Whom to Query for What: Adaptive Group Elicitation via Multi-Turn LLM Interactions*, ICML 2026 / arXiv:2602.14279 | Jointly selects what question to ask and which respondent to query under explicit query/participation budgets, using LLM information-gain scoring and graph propagation | Reinforces that adaptive natural-language elicitation is a mature area; not a hidden-concept semantic-identifiability benchmark, but blocks broad novelty claims about budgeted multi-turn elicitation |
| Current public LLM benchmark | Deep20Bench v1.1, Sept 2026 (non-peer-reviewed benchmark) | Multi-turn hidden-subject identification with graded YES/NO directions plus UNKNOWN | Confirms active current interest; not evidence for semantic universality |
| Separating systems / identifying codes | Katona (1966) and later separating-system/search literature | Pairwise separation by query sets is a classical combinatorial object; constrained query families such as metric balls have their own bounds | UCID's separability theorem is baseline mathematics, not novelty |
| Clarification question generation | White et al., EMNLP 2021, DOI 10.18653/v1/2021.emnlp-main.44 | Expected-information-gain polar clarification questions can resolve ambiguity in a goal-oriented 20-questions-style task | Clarification-by-EIG is an established baseline; UCID must differentiate semantic regime coverage and boundary handling |
| Active feature acquisition | Melville et al. (2004); Li & Oliva, ICML 2021; Rahbar et al., IJCAI 2023 | Sequentially acquire costly missing feature values to improve prediction/decision quality | Cost-aware query choice is established; semantic validity and concept-space coverage are the target contribution |
| Open-set / open-world active learning | Open-world recognition literature; e.g. Safaei et al., AAAI 2024 | Unknown classes can occur outside the known label set; query/rejection strategies explicitly model known versus unknown samples | OUT-OF-SUPPORT detection is not novel; UCID studies its interaction with semantic querying and ontology expansion |
| Open-world active learning | Xie et al., *Deep Active Learning in the Open World* (2024/2025 preprint lineage) and Hu et al., *Uncertainty-driven active developmental learning*, Pattern Recognition 2024 | Explicitly discover/annotate unknown classes under constrained labeling budgets | Unknown-class discovery and budgeted open-world active learning are established; 010 contribution can only be the coupling to semantic question languages/response semantics, not OOS itself |
| Vagueness / sorites | Formal semantics and philosophical logic | Borderline cases and competing semantics for vague predicates | Do not collapse borderline into ordinary false/unknown |
| Paraconsistency | Paraconsistent-logic literature | Contradictory information need not entail arbitrary conclusions (non-explosion) | Useful for inconsistent targets/knowledge states; theory itself is not new |
| Ineffability | Sebastian Gäb, *Ineffability: the Very Concept*, Philosophia 48 (2020), DOI 10.1007/s11406-020-00198-2 | Distinguishes weak from strong ineffability and linguistic from cognitive limits | Strong ineffability should be modeled as an outer boundary, not an ordinary target label |

## Closest technical neighbors after the expanded audit

There is no longer one single closest neighbor; after the 2026 re-audit, 010 sits at the intersection of at least six mature lines.

1. **Wang et al. (ICML 2025):** strongest general adaptive natural-language elicitation neighbor.
2. **Agafonov et al. (ICAART 2026):** strongest *tree ontology + active binary refinement* neighbor and the most important new collision found in the 2026 pass.
3. **Referring Expression Generation:** strongest static semantic-discrimination neighbor.
4. **Description-logic active learning:** strongest formal ontology + interactive-query-learning neighbor.
5. **RSA/reference games:** strongest efficient-communication/pragmatic neighbor.
6. **Huang et al. (EMNLP 2025) + clarification literature:** strongest proactive missing-information/clarification neighbor.

The project survives only if it does not repackage any one of these. In particular, **“ontology-guided active questioning” is no longer available as a novelty claim after ICAART 2026**.

## Current integration gap

The expanded audit, including 2025–2026 adaptive-elicitation work, has not yet found a work whose primary object is all of the following together:

> adaptive identification of a hidden target across deliberately heterogeneous concept regimes, with an explicit admissible semantic query language, response states that distinguish false/unknown/borderline/undefined/inconsistent, open-world withholding, pathological semantic cases, and query cost measured against an unrestricted information-theoretic baseline.

This is a **provisional gap**, not a final novelty claim.

## Search queue before manuscript freeze

- referring expression generation for abstract/non-visual meanings;
- discriminating descriptions in description logics;
- active feature acquisition with missing/abstaining/non-applicable values;
- open-world active concept learning;
- clarification-question generation optimized for disambiguation;
- diagnostic questioning over knowledge graphs;
- multi-valued interactive diagnosis and explicit not-applicable/undefined answer semantics;
- semantic query cost / constrained twenty-questions work using vague, contextual or contradictory targets;
- reference games with compositional or paradoxical meanings;
- minimum identifying codes / separating systems beyond binary Test Cover.

