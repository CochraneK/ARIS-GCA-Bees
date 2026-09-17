# IDEA REPORT · Testing a Periodic System of Human Language

**ARIS stage:** active candidate / idea-discovery in progress  
**Canonical brief:** `../RESEARCH_BRIEF.md`  
**Stage-0 evidence:** `../PILOT_REPORT.md`, `../pilot-results.json`

<a id="literature-landscape"></a>
## Literature landscape

### 1. The metaphor already exists

Baker (2001) explicitly proposed a “periodic table of languages” grounded in grammatical parameters. Therefore neither the periodic-table metaphor nor the idea that languages are assembled from a finite inventory of grammatical “atoms” can be claimed as novel.

### 2. Topology of syntactic parameter space already exists

Port et al. (2018) applied persistent homology to syntactic-parameter data and reported non-trivial topology within language families. Port, Karidi & Marcolli (2022) expanded this to dimensionality, hierarchical clustering, persistent H1 loops, and family-specific relations in SSWL/LanGeLin data. Therefore “use topological data analysis to find loops in linguistic feature space” is also not a defensible novelty claim.

### 3. Global typological latent structure is already studied

Grambank provides large-scale morphosyntactic data and has already been analyzed with PCA, feature bundling, and latent classes. Ordinary dimensionality reduction, clustering, or latent-type discovery alone is insufficiently novel.

### 4. Feature-dependency and universals are already studied with modern controls

Graff et al. (2025) explicitly curate GBI/TLI to reduce logical and very strong feature dependencies. Verkerk et al. (2025/2026) test proposed grammatical universals using Bayesian phylogenetic and spatial controls. Any analysis here must distinguish recurrent structural organization from genealogy, geography, and coding dependencies.

### 5. Typological feature prediction is already a field

SIGTYP shared tasks and related work predict WALS/Grambank features using correlations and language embeddings. A paper whose only claim is “we can predict missing typological features” would not be new; predictive evaluation matters here only as a discriminator between geometric hypotheses.

### Gap that remains defensible

The literature located so far does **not** establish an explicit, capacity-controlled, out-of-sample comparison in which a formal periodic/circular/toroidal model of cross-linguistic structural organization competes against non-periodic Euclidean factor, hierarchical/tree, graph/manifold, and null alternatives on modern curated global data.

The project should therefore be framed as a **test of the periodic-table hypothesis**, not construction of a periodic table.

<a id="ranked-ideas"></a>
## Ranked ideas

### 1. Predictive model competition for linguistic design-space geometry — SELECTED

**Question:** Does a formal periodic geometry generalize better than non-periodic alternatives when predicting held-out structural relationships or feature values?

**Core contribution:** Define periodicity operationally and compare periodic vs factor/tree/graph/manifold/null models under matched evaluation, including family/area extrapolation.

**Why selected:** It is the clearest point not already occupied by Baker, Port/Marcolli, Grambank latent-structure work, or SIGTYP feature prediction.

**Primary risk:** A periodic model may be underdefined or unfairly parameterized; the paper only works if model capacity and evaluation are explicit.

### 2. Modern TLI replication of persistent topology of syntax — PARKED

Apply persistent homology to TLI/GBI and compare topology across grammar, phonology, and colexification.

**Why parked:** modern data and cross-domain scope are useful, but the core method is too close to Port et al. 2018/2022 to carry the novelty by itself. It can serve as an analysis block or sanity check, not the headline contribution.

### 3. Predicting “missing cells” / unattested language configurations — CONDITIONAL

Use the best-performing structural model to identify high-probability but unattested feature configurations and evaluate them by historical hold-out or later database versions.

**Why conditional:** attractive and close to the Mendeleev analogy, but only defensible after a structural model first demonstrates real out-of-sample performance. Otherwise it becomes speculative table-filling.

<a id="novelty-verification"></a>
## Novelty verification

### Closest prior work and differentiation

| Prior work | Overlap | Remaining difference |
|---|---|---|
| Baker 2001 | periodic-table metaphor; grammatical atoms/parameters | theoretical proposal, not modern held-out geometric model competition |
| Port et al. 2018 | persistent topology of syntactic parameters | family-focused topology; not an explicit periodic-vs-nonperiodic predictive contest |
| Port, Karidi & Marcolli 2022 | dimensionality, clustering, H1 loops, syntax geometry | strongest methodological overlap; still does not make “periodic geometry” a predictive hypothesis against multiple alternatives on TLI/GBI |
| Grambank 2023 | PCA, feature bundles, latent classes over global morphosyntax | establishes latent structure but not the proposed periodic hypothesis test |
| Graff et al. 2025 | curated independent global structural datasets | enables cleaner testing; it is substrate, not equivalent research question |
| Verkerk et al. 2025/2026 | universals with phylogenetic/spatial controls | tests specific implicational universals, not the global geometry/model class |
| SIGTYP 2020+ | held-out typological feature prediction | establishes prediction task; here prediction is used for geometric model selection |

### Current novelty verdict

**PROCEED WITH CAUTION (primary-executor assessment, not an ARIS reviewer receipt).**

The initial novelty claim was too broad. After adding the Port/Marcolli line of work, the surviving wedge is narrower but still potentially publishable: formalize periodicity and ask whether it yields reproducible predictive structure beyond established non-periodic alternatives, using modern curated data and explicit genealogy/geography-aware evaluation.

### Kill conditions

Abandon or substantially reframe if any of the following is found:

1. an existing paper already conducts essentially the same periodic/circular/toroidal vs tree/graph/factor held-out comparison on cross-linguistic structural data;
2. “periodic” cannot be specified without arbitrary post-hoc choices that give it more capacity than competitors;
3. any apparent periodic advantage disappears under family-held-out and area-aware evaluation;
4. the result reduces to persistent H1 loops already covered by the Port/Marcolli program.

<a id="external-critical-review"></a>
## External critical review

**Formal ARIS secondary-review status: PENDING.**

This section currently contains a primary-executor stress test only. It must **not** be treated as the identity-bearing external review required by ARIS's reviewer-bearing phase.

### Strongest case for the paper

The hypothesis has an unusually clear historical origin (Baker), modern data now make it testable, and both positive and negative outcomes can answer a concrete structural question if the competing models are fair. TLI additionally lets the work go beyond syntax-only datasets.

### Main reviewer risks

1. **Definition risk:** “periodicity” may remain metaphorical unless represented by an explicit model family with fixed degrees of freedom.
2. **Prior-art risk:** persistent loops are already known in syntax; topology itself is not enough.
3. **Confounding risk:** genetic inheritance, contact, database construction, and missingness can manufacture apparent recurrence.
4. **Evaluation risk:** random language splits leak family/area similarity and can dramatically overstate generalization.
5. **Model-comparison risk:** graph/manifold models are flexible; an unfairly simple periodic model losing is uninformative, while an over-flexible periodic model winning is equally uninformative.
6. **Negative-result risk:** a null result is only interesting if the test has adequate power and the periodic model is a faithful formalization of the historical hypothesis.

### Cheapest discriminating next experiment

Construct train/test feature-association matrices and compare a low-capacity circular model against constant/null, Euclidean low-rank, hierarchical/tree, and graph-distance baselines on **held-out associations**. Repeat with language-family-held-out splits. If circular structure cannot outperform or match alternatives even in this favorable screening setting, do not invest in toroidal or richer periodic models.

## Current decision

Continue to Stage 1. Do not assign Paper 002 yet. The candidate is alive because Stage-0 found non-trivial structure and the novelty search left a narrow but meaningful gap; it remains vulnerable to both stronger prior art and a negative capacity-controlled model comparison.

## Key references

- Baker, M. C. (2001). *The Atoms of Language: The Mind’s Hidden Rules of Grammar*.
- Port, A. et al. (2018). Persistent Topology of Syntax. *Mathematics in Computer Science*, 12, 33–50. https://doi.org/10.1007/s11786-017-0329-x
- Port, A., Karidi, T., & Marcolli, M. (2022). Topological Analysis of Syntactic Structures. *Mathematics in Computer Science*, 16, 2. https://doi.org/10.1007/s11786-021-00520-5
- Skirgård, H. et al. (2023). Grambank reveals the importance of genealogical constraints on linguistic diversity and highlights the impact of language loss. *Science Advances*, 9, eadg6175.
- Graff, A. et al. (2025). Curating global datasets of structural linguistic features for independence. *Scientific Data*, 12, 106.
- Verkerk, A. et al. (2025/2026). Enduring constraints on grammar revealed by Bayesian spatiophylogenetic analyses. *Nature Human Behaviour*, 10, 126–136.
- Bjerva, J. et al. (2020). SIGTYP 2020 Shared Task: Prediction of Typological Features.
- Bjerva, J. (2024). The Role of Typological Feature Prediction in NLP and Linguistics. *Computational Linguistics*, 50(2), 781–794.
