# Active Candidate · Periodic System of Human Language

**Status:** ARIS active candidate · Stage 1 model competition  
**Paper ID:** not assigned  
**Working title:** *Testing the Periodic-Table Hypothesis of Human Language*  
**Subtitle:** *A Predictive Comparison of Periodic and Non-Periodic Models of Cross-Linguistic Structure*

## Core question

Does cross-linguistic structural diversity contain a recurrent organization strong enough to justify a **periodic-system** model, rather than merely a loose metaphor, clustering visualization, tree, graph, or generic low-dimensional embedding?

The project deliberately treats “periodic table” as a falsifiable hypothesis rather than a desired output.

## What is already taken by prior work

- **Baker (2001)** explicitly proposed a “periodic table of languages” and grammatical parameters as language-building atoms. The broad metaphor is not novel.
- **Port et al. (2018)** applied persistent homology to syntactic-parameter data and found non-trivial topology within language families.
- **Port, Karidi & Marcolli (2022)** analyzed dimensionality, hierarchical clustering, and persistent H1 loops in world-language syntactic data. Therefore “use TDA to find loops” is not novel either.
- **Grambank (2023)** already studies large-scale morphosyntactic latent structure with PCA, feature bundles, and latent classes.
- **Graff et al. (2025)** provide dependency-curated GBI/TLI datasets spanning structural domains.
- **Verkerk et al. (2025/2026)** test 191 grammatical universals with genealogical and geographical controls.
- **SIGTYP and computational typology** already make typological feature prediction an established task.

## Surviving novelty wedge

The candidate contribution is to turn the historical periodic-table analogy into a **capacity-controlled predictive hypothesis**:

> Does an explicitly periodic geometry generalize better than Euclidean factor, hierarchical/tree, graph/manifold, and null alternatives when predicting structural relations in held-out languages and held-out language families?

A periodic interpretation survives only if it adds reproducible out-of-sample value and stable recurrent ordering beyond these alternatives.

## Evidence so far

### Stage 0 · prerequisite screen

`MIXED_SIGNAL` on TLI-statistical densified-small:

- 644 languages;
- observed 20-component compression = **0.510** vs shuffled-null mean **0.362**;
- residual feature association is weak for most pairs but has a substantial upper tail.

This establishes non-random organization worth testing, **not periodicity**.

### Stage 1 · running

The current branch runs the first direct model competition:

- null;
- rank-2 low-rank structure;
- 2-D Euclidean geometry;
- hierarchical/tree geometry;
- graph shortest-path geometry;
- circular periodic geometry.

Each model is trained on feature associations in one set of languages and predicts associations in held-out languages. Evaluation includes ordinary random splits and harder **Glottolog top-level family-held-out splits**.

## ARIS artifacts

- `RESEARCH_BRIEF.md` — formal input brief
- `idea-stage/IDEA_REPORT.md` — literature landscape, ranked variants, novelty verification, review status
- `PILOT_REPORT.md` / `pilot-results.json` — Stage-0 evidence
- `refine-logs/EXPERIMENT_PLAN.md` — claim-driven experiment roadmap
- `ARIS_STATUS.md` — durable pipeline state and gate status
- `stage1.py` — executable model competition

## Formal review boundary

ARIS v0.4.26 requires identity-bearing secondary-review evidence for reviewer-bearing phases. The current ChatGPT-side pass has performed literature search and a primary-agent stress test, but **has not fabricated a formal external reviewer receipt**. Promotion to a numbered paper remains blocked on that review gate plus Stage-1 evidence.

## Promotion criterion

Promote to the next stable Paper ID only if:

1. Stage 1 yields a useful GO or defensible REFRAME result;
2. the periodic model has a precise, fair capacity definition;
3. genealogy/geography-aware validation is included;
4. novelty search still finds no equivalent predictive periodic-vs-nonperiodic comparison;
5. formal ARIS secondary review survives.

## Key sources

- Baker, M. C. (2001). *The Atoms of Language: The Mind’s Hidden Rules of Grammar*. Chapter 6: “Toward a Periodic Table of Languages.”
- Port, A. et al. (2018). Persistent Topology of Syntax. *Mathematics in Computer Science*, 12, 33–50. https://doi.org/10.1007/s11786-017-0329-x
- Port, A., Karidi, T., & Marcolli, M. (2022). Topological Analysis of Syntactic Structures. *Mathematics in Computer Science*, 16, 2. https://doi.org/10.1007/s11786-021-00520-5
- Skirgård, H. et al. (2023). Grambank reveals the importance of genealogical constraints on linguistic diversity and highlights the impact of language loss. *Science Advances*, 9, eadg6175. https://doi.org/10.1126/sciadv.adg6175
- Graff, A. et al. (2025). Curating global datasets of structural linguistic features for independence. *Scientific Data*, 12, 106. https://doi.org/10.1038/s41597-024-04319-4
- Verkerk, A. et al. (2025/2026). Enduring constraints on grammar revealed by Bayesian spatiophylogenetic analyses. *Nature Human Behaviour*, 10, 126–136. https://doi.org/10.1038/s41562-025-02325-z
