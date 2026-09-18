# Testing the Periodic-Table Hypothesis of Human Language: Predictive Evidence Favors Non-Circular Structure

**Paper 002 · ARIS4C**  
**Author:** Cunyi Kang  
**Manuscript status:** Draft v1 · exploratory/model-comparison study  
**Secondary ARIS review:** PASS (WorkBuddy / Tencent Hy3)  
**Last substantive evidence cutoff:** 2026-09-18

## Abstract

The idea that human languages might admit an organization analogous to a periodic table is scientifically attractive because it suggests that apparently diverse grammars could be generated from a recurrent, compact structural system. Yet a periodic-table metaphor is not itself a statistical model, and modern typological datasets make it possible to ask a sharper question: does a simple global periodic geometry predict structural relations among linguistic features better than non-periodic alternatives?

We operationalized one strong, deliberately bounded form of periodicity as a single circular geometry over structural features. Models were trained on feature–feature normalized mutual information (NMI) estimated from one set of languages and evaluated against independently estimated NMI in held-out languages. We compared circular models with low-rank, Euclidean, hierarchical-tree, graph and null representations, progressively adding top-level-family hold-outs, predefined structural domains, direct circular-Robinson-style diagnostics, geographic blocks, repeated split uncertainty, an alternative GBI curation, and a sparse external WALS replication.

Across 20 TLI family-held-out splits, the hierarchical-tree benchmark achieved mean Spearman correlation 0.182 versus 0.109 for the optimized circular model; the paired difference was 0.073 (split-bootstrap 95% CI 0.055–0.092), with the tree higher in all 20 splits. The same qualitative ordering appeared in GBI (0.122 vs 0.073) and WALS (0.603 vs 0.410). Direct circularity diagnostics also failed to show robust wrap-around closure: at 60 TLI features, the circular closure/internal-adjacency ratio was 0.037. No predefined TLI domain met the joint predictive-competitiveness and circular-stability criterion for local periodicity.

These analyses do not establish a universal tree geometry, nor do they exclude every possible form of linguistic periodicity. They instead constrain a specific global-circle formulation: reproducible structural order exists, but the tested periodic geometry is not the strongest held-out account of it. Geographic portability was representation-dependent, underscoring that conclusions about global linguistic geometry depend on dataset construction and sampling.

## 1. Introduction

Human languages vary extensively in word order, morphology, phonology, lexical structure and the ways in which grammatical categories are expressed. A long tradition in linguistic typology asks whether this diversity occupies a constrained design space rather than an unstructured collection of possibilities. Within the principles-and-parameters tradition, Baker (2001) made the analogy especially vivid by proposing that grammatical parameters might eventually support a "periodic table of languages": a compact organization of recurring structural choices that could summarize attested languages and perhaps delimit possible but unattested systems.

The analogy was generative, but it was not a single statistical hypothesis. Baker's own exposition culminated in a parameter hierarchy rather than a literal circular table. Subsequent quantitative work has established that linguistic structure is neither random nor independent across languages. Grambank documents broad morphosyntactic diversity across more than two thousand languages and shows strong genealogical structure (Skirgård et al., 2023). Curated GBI and TLI resources were subsequently designed to reduce logical and strong statistical dependencies among structural features, enabling large-scale multivariate analyses under clearer feature-independence assumptions (Graff et al., 2025). Bayesian spatiophylogenetic work further shows that some proposed grammatical universals remain supported after explicit controls for genealogy and geography, while many weaken substantially (Verkerk et al., 2026).

At the same time, several adjacent claims are already well explored and are not the novelty target here. Persistent topology, dimensionality and hierarchical clustering have been applied to syntactic parameter data (Port et al., 2018; Port, Karidi, & Marcolli, 2022). Probabilistic prediction of typological features is an established task in computational typology (e.g., Bjerva et al., 2019). Circular seriation itself has a formal mathematical literature built around circular Robinson dissimilarities (Armstrong, Guzmán, & Sing-Long, 2021). The scientific gap is therefore not whether language data can be clustered, embedded or predicted. The narrower question is whether a periodic interpretation can be turned into an explicit predictive competitor and survive out-of-sample comparison with non-periodic alternatives.

### 1.1 A bounded operationalization of periodicity

A periodic-table metaphor does not uniquely imply a circle. We use a single global circle as a **strong, minimal and falsifiable operationalization of recurrent wrap-around structure**, not as a claim that Baker literally proposed circular geometry or that all possible notions of periodicity reduce to one circle. A genuine circle should do more than yield a stable ordering: neighboring points should recur around the entire cycle, including across the wrap-around edge, and the learned ordering should exhibit held-out dissimilarity structure compatible with circular seriation.

This distinction matters because a stable ordering can be line-like or hierarchical without being periodic. Every linear Robinson-compatible structure is compatible with a weaker circular interpretation in a formal sense, so circular compatibility alone cannot establish genuine closure. We therefore combine predictive model comparison with direct diagnostics of row-wise circular-Robinson-style structure and explicit wrap-around closure.

### 1.2 Study question and claim boundary

The central question is:

> **Does a simple global circular geometry provide reproducible out-of-sample organization of cross-linguistic structural feature relations beyond non-periodic alternatives?**

The study is explicitly exploratory and screening-oriented. Analyses were developed sequentially from Stage 0 through Stage 1I, rather than preregistered as a single confirmatory protocol. Accordingly, we emphasize effect sizes, held-out replication, contradictions and claim boundaries rather than interpreting the full sequence as one confirmatory test family.

The strongest conclusion permitted by the design is also deliberately narrow:

> **The global-circle form of the language periodic-table hypothesis tested here is not supported by predictive and held-out circularity evidence; hierarchical/non-circular models provide stronger family-held-out benchmarks across TLI, GBI and WALS, without establishing one universal tree geometry.**

## 2. Materials and methods

### 2.1 Data sources

#### TLI

The primary analyses used the statistically curated TLI resource from Graff et al. (2025), specifically the densified-small full dataset used by the ARIS4C pipeline. TLI combines structural information derived from WALS, AUTOTYP, PHOIBLE and Lexibank and applies curation to reduce logical dependencies and strong statistical dependencies among features. Stage 0 used 644 languages and up to 120 features. Global predictive comparisons used the 60 best-covered eligible features unless otherwise stated; robustness analyses repeated selected comparisons at 40 features.

For Stage 1, a feature was eligible if it had at least 180 observed language values and between 2 and 15 observed states. Eligible features were ranked first by coverage and then by lower cardinality, reducing unstable NMI estimates from sparse, high-cardinality variables. The top 60 were used for the main global screen.

#### GBI

Stage 1H used the statistically curated GBI representation from Graff et al. (2025), derived from Grambank under an alternative feature-curation strategy. The analysis used 1,140 languages and 60 selected features. Because GBI and TLI are curated from partly related typological infrastructure and are not fully independent scientific data-generating processes, GBI is treated as a **curation/representation replication**, not as a fully external dataset.

#### WALS

Stage 1I used the CLDF WALS dataset as an external sparse sanity replication. The pivot contained 2,659 languages; the 30 best-covered categorical parameters meeting coverage/cardinality rules were selected. WALS is substantially sparser and is not dependency-curated in the same way as TLI/GBI, so WALS effect magnitudes are not interpreted as directly comparable to TLI/GBI. Its role is qualitative: to test whether the family-held-out tree-versus-circle ordering reverses under a distinct representation.

#### Family and geographic metadata

Top-level family assignments were mapped using Glottolog CLDF. Entries without a mapped family were treated as separate isolate groups rather than pooled into a single missing-family category. Geographic robustness used Glottolog macroareas and, separately, latitude/longitude clusters constructed without reference to linguistic outcomes.

### 2.2 Pairwise structural target

For each train/test partition, the target was a feature-by-feature association matrix computed independently in the training and test languages. For each feature pair with sufficient joint observations, association was quantified using normalized mutual information (NMI; arithmetic normalization). In the main TLI screen, feature pairs required at least 60 jointly observed training/test observations where applicable.

A model therefore did not predict an individual language's feature value. Instead, it learned the **geometry of inter-feature association** from one set of languages and was evaluated on whether that geometry predicted the independently re-estimated association structure in held-out languages.

This choice makes held-out prediction a test of whether a learned structural organization transports across samples rather than merely fitting the pooled association matrix.

### 2.3 Model families

All candidate geometries were fit using training-language associations only.

#### Null model

The null prediction assigned every off-diagonal feature pair the mean observed training association.

#### Rank-2 low-rank model

The finite training affinity matrix was centered by its mean off-diagonal value and reconstructed using the two eigencomponents with largest absolute eigenvalues. This provided a simple non-periodic low-dimensional comparator.

#### Euclidean two-dimensional model

A two-dimensional spectral embedding was estimated from the training affinity matrix. Pairwise Euclidean distances were mapped back to predicted associations using a quadratic calibration fit on training feature pairs.

#### Hierarchical-tree benchmark

Training dissimilarity was defined as (1-mathrm{NMI}). Average-linkage hierarchical clustering produced a dendrogram, and cophenetic distances between features were converted to predicted association using a quadratic training-set calibration. This model is a predictive benchmark, not an assertion that linguistic structure is literally a phylogenetic tree.

#### Graph benchmark

A 6-nearest-neighbor graph was constructed from training dissimilarities. Shortest-path distances on the undirected weighted graph were quadratically calibrated to the training associations.

#### Circular models

The initial circular model projected a two-dimensional spectral embedding to angular coordinates and predicted association with a symmetric periodic regression using the first two cosine harmonics.

The stronger Stage 1B model directly optimized one angular coordinate per feature, fixing one feature at angle zero to remove rotational non-identifiability. At each optimization step the association prediction was fit as

[
hat{s}_{ij} = eta_0 + eta_1cos(Delta_{ij}) + eta_2cos(2Delta_{ij}),
]

where (Delta_{ij}) is circular angular distance. The (n-1) free angular coordinates were optimized by L-BFGS-B to minimize mean squared error in the training association matrix, with multiple starting points. This reduces the concern that a negative circular result is merely caused by inheriting poor spectral angles.

### 2.4 Train/test evaluation

The primary ranking metric was Spearman correlation between model-predicted feature associations and the independently estimated held-out association matrix. Pearson correlation, RMSE and MAE were also recorded.

Two basic split types were used in Stage 1:

1. random language hold-out; and
2. top-level-family hold-out, in which complete sampled Glottolog families were assigned to the test set.

Family hold-out reduces direct genealogical leakage, but it does **not** eliminate all phylogenetic or contact dependence. The study therefore does not interpret family hold-out as a complete solution to Galton's problem.

### 2.5 Sequential robustness analyses

The analyses evolved iteratively. They should be read as a robustness ladder rather than as independent preregistered confirmatory tests.

- **Stage 0:** test whether TLI contains non-random compressibility and residual feature association worth modeling.
- **Stage 1:** compare null, low-rank, Euclidean, tree, graph and initial circular models.
- **Stage 1B:** improve circular fairness with connected embeddings and direct angular optimization; repeat at 40 and 60 features.
- **Stage 1C:** test predefined TLI structural domains rather than selecting circular-looking domains post hoc.
- **Stage 1D:** test held-out circular-Robinson-style row unimodality and explicit wrap-around closure.
- **Stage 1E:** evaluate macroarea and coordinate-cluster hold-outs, with and without removing from training every family represented in the test block.
- **Stage 1F:** repeat family hold-out 20 times and bootstrap the paired split-level performance differences.
- **Stage 1G:** compare geographic blocks with matched-size random test samples to test whether geographic transfer loss is a trivial sample-size artifact.
- **Stage 1H:** replicate the family-held-out ranking in GBI.
- **Stage 1I:** perform an external sparse WALS sanity replication.

Because this sequence was adaptive, no family-wise confirmatory error rate is claimed across Stage 1–1I.

### 2.6 Predefined local-domain criterion

Stage 1C used TLI's published feature grouping metadata to define five superdomains: Grammar linear order, Grammar other, Grammatical categories, Lexical and Phonology. A domain was considered a local periodic candidate only if the optimized circular model simultaneously achieved:

1. Spearman correlation at least 0.15;
2. performance within 0.03 of the best non-periodic comparator; and
3. circular-order stability at least 0.40.

The joint rule was chosen to avoid calling a subsystem periodic merely because a circular fit was non-zero.

### 2.7 Direct circularity diagnostics

Stage 1D implemented a noisy-data sensitivity inspired by circular Robinson structure (Armstrong et al., 2021). For an order learned from training languages, each held-out dissimilarity row was read around the cycle and scored for deviation from a single rise-then-fall unimodal sequence; lower values indicate closer compatibility.

This diagnostic is **not** an exact strict circular-Robinson recognition algorithm. It is a standards-inspired sensitivity analysis.

Because line-like Robinson order can also appear compatible with a cyclic ordering, we added a closure diagnostic:

[
	ext{closure ratio}=
rac{	ext{similarity of wrap-around pair}}
{	ext{median similarity of internal adjacent pairs}}.
]

A ratio near 1 would indicate that the final-to-first edge is supported similarly to ordinary internal adjacencies. The closure ratio is interpreted for the circular order; values for tree/random orders are not evidence for or against cyclic closure.

### 2.8 Geographic transfer and matched-size calibration

Stage 1E used outcome-blind geographic partitions based on Glottolog macroareas and five coordinate-derived spatial clusters. Stage 1G compared the correlation between training- and geographic-test association matrices against random test sets matched to each geographic block's size.

The calibration addresses one simple alternative explanation—smaller test sets—but does not identify causal areal transmission or separate geography from historically correlated population structure.

### 2.9 Repeated-split uncertainty

Stage 1F used 20 valid top-level-family-held-out splits. Paired differences in Spearman performance were computed for the same split (e.g., tree minus optimized circle), and a bootstrap over the **20 split-level differences** produced 95% intervals.

These intervals quantify sensitivity to the sampled family splits. They do **not** quantify uncertainty over languages as independent observations, phylogenetic-tree uncertainty, contact-network uncertainty or the full model-selection process.

## 3. Results

### 3.1 Structural signal exists, but Stage 0 does not imply periodicity

On the TLI Stage-0 screen, 20 principal components explained 0.510 of cumulative variance compared with 0.362 under a column-wise shuffled null, an excess of 0.148. Pairwise residual association was small for most feature pairs but showed a stronger upper tail: the observed 99th percentile of NMI was 0.119 compared with 0.039 under permutation.

These results justified explicit geometry tests. They were not interpreted as evidence for periodicity.

### 3.2 Initial held-out comparison favored non-periodic competitors

With 60 TLI features, the initial family-held-out Stage 1 comparison yielded mean Spearman correlations of 0.178 for the hierarchical tree, 0.163 for the graph, 0.150 for the rank-2 low-rank model, and 0.109 for the circular model. The circular ordering was not arbitrary—the mean order stability relative to the full-data reference was 0.542—but stability did not translate into best held-out prediction.

Under random-language splits the pattern was similar in direction: graph 0.205, tree 0.199, low-rank 0.172 and circular 0.122.

### 3.3 Direct circular optimization removed a simple strawman explanation

Stage 1B gave the circular hypothesis a more favorable fit. At 40 features, the optimized circle achieved Spearman 0.179, almost equal to the tree benchmark at 0.178, while the connected Euclidean model reached 0.217. At 60 features, however, the optimized circle fell to 0.105, below tree (0.147) and low-rank (0.153).

The directly optimized circular order was reasonably stable at 60 features (0.628 ± 0.081). Thus the negative result cannot be reduced to a completely unstable or obviously misfit ordering. Rather, **stable circular order was not sufficient for robust predictive dominance**.

### 3.4 No predefined TLI domain satisfied the local-periodicity rule

None of the five predefined structural domains passed all three local-periodicity criteria.

The most informative case was Grammar linear order. Its optimized circular model reached Spearman 0.401 and high order stability (0.811), showing that a reproducible ordering exists. Yet tree and low-rank models both reached approximately 0.49. This provides a concrete example of the distinction central to the study: **stable order is not the same as a best-supported cycle**.

Grammatical categories was the only domain in which the optimized circular mean (0.252) exceeded the tree mean (0.229), but circular-order stability was 0.373, below the predeclared 0.40 threshold. Lexical, Grammar other and Phonology did not approach joint periodic competitiveness.

### 3.5 Held-out circularity diagnostics did not support global closure

In Stage 1D, lower row-unimodality deviation indicates closer circular-Robinson-style compatibility. At 40 features the circular order scored 0.222 ± 0.012, compared with 0.209 ± 0.011 for the tree leaf order and 0.237 ± 0.009 for random orders. At 60 features the corresponding values were 0.297 ± 0.009, 0.284 ± 0.010 and 0.307 ± 0.009.

More directly, the mean circular wrap-around closure/internal-adjacency ratio was 0.608 at 40 features but only **0.037** at 60 features. The 60-feature result provides little support for the key edge that distinguishes a closed cycle from a stable open ordering.

These diagnostics are noisy-data sensitivities, not formal rejection tests for all circular-Robinson structures. Their value is that the negative periodic interpretation no longer depends solely on a higher-capacity tree outperforming a circle.

### 3.6 Tree-over-circle ranking was stable across repeated TLI family hold-outs

Across 20 valid Stage 1F family-held-out splits, mean Spearman correlation was:

| Model | Spearman mean ± SD |
|---|---:|
| tree | **0.182 ± 0.047** |
| low-rank (rank 2) | 0.155 ± 0.034 |
| Euclidean connected | 0.110 ± 0.053 |
| circular optimized | **0.109 ± 0.030** |

The paired tree-minus-circle difference was **+0.073**, with split-bootstrap 95% CI **[0.055, 0.092]**; the tree was higher in all 20 splits. The low-rank-minus-circle difference was +0.046 [0.033, 0.061] and favored low-rank in 95% of splits. Euclidean-versus-circle was effectively tied (+0.001 [−0.020, 0.021]).

The bootstrap interval is a summary of split sensitivity, not phylogenetic uncertainty.

### 3.7 TLI geography blocks weakened all models, but the pattern was not universal

When complete TLI macroareas were held out, all models performed weakly. Under the stricter geography-plus-family condition, the best non-periodic Spearman was approximately 0.056 while the optimized circle was approximately 0.000. Spatial-cluster-plus-family splits produced a best non-periodic mean of 0.085 and circular mean of 0.039.

Matched-size calibration showed that the weak TLI geographic transfer was not simply caused by the smaller number of test languages. Across macroareas, the train–test association correlation averaged 0.088 for geographic blocks versus 0.363 for matched random test sets. Across coordinate clusters, the corresponding means were 0.106 versus 0.351. All ten geographic blocks had lower transfer than their matched random controls.

However, the external WALS replication later showed much stronger cross-macroarea transfer, so geographic collapse is **not** treated as a universal property of cross-linguistic structure.

### 3.8 Tree-over-circle ordering replicated under GBI curation

In GBI, using 1,140 languages and 60 selected features, family-held-out mean Spearman was 0.122 ± 0.038 for the tree and 0.073 ± 0.036 for the optimized circle; the tree-minus-circle mean difference was +0.049 and the tree was higher in every evaluated split. Rank-2 low-rank performance was 0.098 ± 0.034.

Mean cross-macroarea association transfer was 0.144 ± 0.043, qualitatively similar to the weak geographic transfer observed in TLI. Because GBI and TLI are alternative curations rather than fully independent sources, this result is interpreted as robustness to representation/curation rather than a fully independent replication.

### 3.9 WALS reproduced the model ranking but contradicted the geography pattern

The WALS sanity replication used 2,659 languages and 30 best-covered parameters. Across eight valid family-held-out splits, mean Spearman was 0.603 ± 0.026 for the tree, 0.468 ± 0.034 for rank-2 low-rank, and 0.410 ± 0.050 for the optimized circle. The tree-minus-circle mean difference was +0.193, and the tree was higher in all eight splits.

Unlike TLI/GBI, WALS exhibited high cross-macroarea association transfer: **0.634 ± 0.075** across six macroareas. This contradiction narrows the robust cross-source conclusion. The stable finding is the family-held-out advantage of non-circular/tree-like benchmarks over the tested circle; the apparent geographic portability of the full association geometry is dataset-dependent.

### 3.10 Cross-dataset synthesis

| Dataset / representation | Languages | Features | Tree Spearman | Circular Spearman | Tree > circle |
|---|---:|---:|---:|---:|---:|
| TLI repeated family hold-out | 644 | 60 | **0.182** | 0.109 | 20/20 |
| GBI curation replication | 1,140 | 60 | **0.122** | 0.073 | all evaluated splits |
| WALS sparse external sanity replication | 2,659 | 30 | **0.603** | 0.410 | 8/8 |

Absolute Spearman magnitudes should not be compared directly across datasets because coverage, sparsity, feature definitions, feature selection and curation differ. The relevant replication is qualitative: in each representation, the optimized circle did not reverse the tree benchmark under family hold-out.

## 4. Discussion

### 4.1 What the study constrains

The motivating periodic-table idea survives as a useful scientific question, but the specific global-circle model tested here does not survive the evidence ladder as the strongest predictive geometry.

The result is not merely "a tree fits better than a circle." That comparison is potentially capacity-confounded: hierarchical and graph representations can be more flexible than a single circle. The stronger inference comes from the conjunction of several observations:

1. direct optimization gave the circle (n-1) angular parameters rather than inheriting a fixed spectral order;
2. low-rank structure also outperformed the circle on average in the repeated TLI family splits;
3. no predefined TLI domain passed the joint local-periodicity rule;
4. direct held-out circular-Robinson-style diagnostics did not favor the circular order over a tree leaf order;
5. wrap-around closure was especially weak in the 60-feature TLI analysis;
6. the family-held-out tree-over-circle ranking replicated qualitatively in GBI and WALS.

Together, these results make a simple global cycle a weak summary of the observed association geometry.

### 4.2 What the study does not establish

First, the study does **not** establish that language is universally "tree-shaped." The hierarchical model is used as a predictive benchmark. Its better performance does not identify a unique ontological geometry, and the model-capacity comparison is not exact.

Second, the study does **not** falsify all possible notions of linguistic periodicity. Baker's original discussion was parameter-hierarchical and the periodic-table metaphor could, in principle, be formalized using multiple cycles, products of spaces, lattices, conditional parameter systems or generative constraints that are not captured by a single circle. Testing such models would constitute new hypotheses and should be preregistered rather than introduced post hoc to rescue the original prediction.

Third, the study does **not** claim that typological features are natural kinds analogous to chemical elements. The objects organized here are database features, whose definitions and dependencies are partly consequences of linguistic theory, coding practice and curation.

### 4.3 Stable order without periodic closure

One of the most useful findings is conceptual rather than simply negative. Grammar linear order showed high circular-order stability (0.811) and substantial circular prediction (0.401), yet tree/low-rank prediction was stronger (about 0.49). The 60-feature global optimized circle likewise had fairly stable order while showing almost no wrap-around closure.

This suggests a general warning for studies that infer periodicity from circular embeddings or stable orderings alone. Reproducible order may reflect a gradient, hierarchy or manifold that can be drawn around a circle without possessing the defining closure expected of a genuine periodic system.

### 4.4 Geography is a representation-dependent secondary result

TLI and GBI suggested poor transport of the full association geometry across large geographic blocks. Matched-size controls make it unlikely that TLI's collapse is solely a small-test-set artifact. Yet WALS shows the opposite qualitative pattern, with strong macroarea transfer.

This disagreement may reflect feature definitions, missingness, domain composition, curation, language sampling, or how association matrices behave under sparse coding. The present analyses do not identify which explanation is correct. The contradiction is therefore evidence **against** elevating geographic heterogeneity into a universal headline conclusion.

This caution aligns with recent spatiophylogenetic work showing that raw cross-linguistic associations can change substantially when genealogical and spatial dependence are modeled directly (Verkerk et al., 2026).

### 4.5 Relation to previous work

Baker (2001) supplied the motivating analogy and a parameter-hierarchical organization, not the predictive circular test used here. Port and colleagues demonstrated that syntactic-parameter datasets can exhibit non-trivial topology, clustering and loops (Port et al., 2018; Port et al., 2022), making it inappropriate to claim novelty for simply finding low-dimensional or topological structure. Grambank established the scale of global morphosyntactic structure and the importance of genealogy (Skirgård et al., 2023). Graff et al. (2025) provided the dependency-curated GBI/TLI substrates that make a multifeature geometry comparison more defensible. Computational typology already treats held-out prediction as a useful probe of structural information (Bjerva et al., 2019).

The contribution here is therefore methodological and diagnostic: **turning one strong form of the periodic-table metaphor into an explicit held-out competitor, then attempting to falsify it using predictive, domain, circularity, family, geographic and cross-representation tests.**

## 5. Limitations

### 5.1 Exploratory multiplicity

Stage 1 through Stage 1I were developed iteratively. The sequence contains multiple feature counts, domains, partitions, metrics and datasets. The paper therefore does not interpret nominal comparisons across stages as one preregistered confirmatory family. The repeated-split paired intervals in Stage 1F are robustness summaries for a focal contrast after the model family had already been explored.

### 5.2 Residual genealogy and contact

Holding out top-level families reduces direct leakage but does not model phylogenetic covariance within and between historical lineages, uncertainty in language trees, or contact networks. Full Bayesian spatiophylogenetic analysis would strengthen claims about universality and independence from inheritance/contact but is not required for the bounded descriptive conclusion that the tested circle is not the strongest held-out benchmark.

### 5.3 Capacity mismatch

A hierarchical tree, graph and single global circle do not have identical effective capacity. The paper therefore avoids interpreting tree superiority as evidence that a universal tree is the true geometry. Direct circular diagnostics and low-rank comparisons partly reduce, but do not eliminate, this limitation.

### 5.4 Association metric and sparse data

NMI depends on sample size, missingness and category structure. Feature pairs require minimum support, but uncertainty in the association matrix is not propagated through every model fit. WALS is especially sparse, and its larger correlation values should not be compared numerically with TLI/GBI as though they were measured on the same scale under the same sampling process.

### 5.5 Feature ontology

The geometry is a geometry of encoded typological variables, not necessarily of psychologically or historically primitive "linguistic atoms." Database feature definitions, curation choices and state coding shape the space being modeled.

### 5.6 Circular-Robinson sensitivity is approximate

Stage 1D uses a continuous row-unimodality violation score inspired by circular-Robinson characterization, not the exact strict-recognition algorithm of Armstrong et al. (2021). The closure diagnostic was added because circular compatibility can include line-like structure. Exact noisy circular-seriation model comparison remains a useful methodological extension.

## 6. Conclusion

A periodic-table metaphor becomes scientifically informative only when it can lose.

Across progressively stricter screens, a directly optimized global circle captured reproducible linguistic structure but did not provide the strongest held-out account of that structure. Tree/non-circular benchmarks performed better under family hold-out in TLI, GBI and WALS; predefined domains did not yield a robust local-periodic candidate; and direct held-out diagnostics provided little evidence for the wrap-around closure expected of a global cycle.

The result is not that language has no periodic organization and not that language is a tree. The narrower conclusion is more useful: **stable cross-linguistic structure does not, by itself, imply periodicity, and the tested global-circle version of the language periodic-table hypothesis is not supported as the best predictive geometry.**

Future work can now ask a sharper question: which explicitly specified non-circular, modular or higher-dimensional geometries generalize across linguistic domains and populations, and what new evidence would be required before a stronger form of periodicity deserves to be revived?

## 7. Data and code availability

All analysis code, machine-readable results and stage reports are archived in the ARIS4C repository under:

- `ideas/language-periodic-system/` — full pre-promotion analysis provenance;
- `papers/002-language-geometry/` — manuscript-stage canonical paper;
- `papers/002-language-geometry/process/DATA_PROVENANCE.md` — upstream snapshots and source boundaries.

The original analysis scripts downloaded public upstream data at runtime. For manuscript reproducibility, the upstream repository commit identifiers observed at manuscript freeze are recorded separately. These identifiers document the current reproducibility target but do not retroactively prove that every historical run used byte-identical upstream files; this distinction is retained explicitly.

## References

Armstrong, S., Guzmán, C., & Sing-Long, C. A. (2021). An optimal algorithm for strict circular seriation. *SIAM Journal on Mathematics of Data Science, 3*(4), 1223–1250. https://doi.org/10.1137/21M139356X

Baker, M. C. (2001). *The Atoms of Language: The Mind's Hidden Rules of Grammar*. Basic Books.

Bjerva, J., Kementchedjhieva, Y., Cotterell, R., & Augenstein, I. (2019). A probabilistic generative model of linguistic typology. In *Proceedings of NAACL-HLT 2019* (pp. 1529–1540). https://doi.org/10.18653/v1/N19-1156

Dryer, M. S., & Haspelmath, M. (Eds.). (2013). *The World Atlas of Language Structures Online*. Max Planck Institute for Evolutionary Anthropology.

Graff, A., Chousou-Polydouri, N., Inman, D., et al. (2025). Curating global datasets of structural linguistic features for independence. *Scientific Data, 12*, 106. https://doi.org/10.1038/s41597-024-04319-4

Port, A., Gheorghita, I., Guth, D., Clark, J. M., Liang, C., Dasu, S., & Marcolli, M. (2018). Persistent topology of syntax. *Mathematics in Computer Science, 12*(1), 33–50. https://doi.org/10.1007/s11786-017-0329-x

Port, A., Karidi, T., & Marcolli, M. (2022). Topological analysis of syntactic structures. *Mathematics in Computer Science, 16*, Article 2. https://doi.org/10.1007/s11786-021-00520-5

Skirgård, H., Haynie, H. J., Blasi, D. E., et al. (2023). Grambank reveals the importance of genealogical constraints on linguistic diversity and highlights the impact of language loss. *Science Advances, 9*(16), eadg6175. https://doi.org/10.1126/sciadv.adg6175

Verkerk, A., Shcherbakova, O., Haynie, H. J., et al. (2026). Enduring constraints on grammar revealed by Bayesian spatiophylogenetic analyses. *Nature Human Behaviour, 10*, 126–136. https://doi.org/10.1038/s41562-025-02325-z
