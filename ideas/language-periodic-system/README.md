# Candidate · Periodic System of Human Language

**Status:** novelty-test / pilot

**Working title:** *Is There a Periodic System of Human Language? A Data-Driven Test Across the World’s Languages*

## Core question

Does cross-linguistic structural diversity contain a recurrent organization strong enough to justify a **periodic-system** model, rather than merely a loose metaphor, clustering visualization, tree, graph, or generic low-dimensional embedding?

The project deliberately treats “periodic table” as a falsifiable hypothesis rather than a desired output.

## Prior art that constrains the claim

- Mark C. Baker’s *The Atoms of Language* (2001) explicitly proposed a “periodic table of languages” built from grammatical parameters and a parameter hierarchy. The broad metaphor and the idea of linguistic “atoms” are therefore **not novel**.
- Grambank (Skirgård et al., 2023) already tests the dimensionality of global grammatical diversity. Its PCA required 19 components to explain 49% of variation, arguing against an extremely small set of global grammatical axes. Its supplementary analyses also induced nine feature bundles and fitted Bayesian latent-class models, so ordinary clustering or bundle discovery alone is **not novel**.
- Graff et al. (2025) provide GBI/TLI datasets curated to reduce logical and very strong statistical dependencies. TLI combines grammar, phonology, and colexification data, making it a useful substrate for asking whether meaningful structure survives after obvious dependencies are removed.
- Verkerk et al. (2025) tested 191 proposed grammatical universals with phylogenetic and spatial controls and found robust support for a minority, showing that recurrent constraints exist but are much weaker than naive correlations suggest.

## Defensible novelty wedge

The candidate contribution is **not** to invent a language periodic table. It is to operationalize the analogy and ask whether a periodic geometry is empirically warranted.

A full paper would compare competing representations of cross-linguistic structural space on held-out data:

- periodic / circular / toroidal / lattice-like latent structure;
- ordinary Euclidean factor or embedding models;
- hierarchical/tree models;
- graph/manifold models;
- independence/null baselines.

A periodic interpretation only survives if it adds reproducible out-of-sample predictive value and recurrent ordering beyond these alternatives.

## Stage-0 pilot

Before fitting ambitious geometries, test two prerequisites on the statistically curated TLI data:

1. **Compression beyond a marginal-preserving null.** Does the observed one-hot language-feature matrix concentrate substantially more variance into its leading latent dimensions than matrices produced by independently shuffling each feature across languages?
2. **Residual association beyond curation.** Do reasonably well-covered feature pairs retain normalized mutual information substantially above a column-wise permutation null after the TLI statistical curation?

These tests are intentionally conservative. Passing them does **not** demonstrate periodicity; failing both would be evidence against spending a full ARIS run on the strong periodic-system hypothesis.

## Promotion criterion

Promote this candidate to the next stable Paper ID only if the pilot finds non-trivial residual organization **and** the follow-up novelty review does not uncover an existing study that already performs explicit periodic-vs-nonperiodic model comparison with held-out evaluation.

## Key sources

- Baker, M. C. (2001). *The Atoms of Language: The Mind’s Hidden Rules of Grammar*. Basic Books. Chapter 6: “Toward a Periodic Table of Languages.”
- Skirgård, H. et al. (2023). Grambank reveals the importance of genealogical constraints on linguistic diversity and highlights the impact of language loss. *Science Advances*, 9, eadg6175. https://doi.org/10.1126/sciadv.adg6175
- Graff, A. et al. (2025). Curating global datasets of structural linguistic features for independence. *Scientific Data*, 12, 106. https://doi.org/10.1038/s41597-024-04319-4
- Verkerk, A. et al. (2025). Enduring constraints on grammar revealed by Bayesian spatiophylogenetic analyses. *Nature Human Behaviour*. https://doi.org/10.1038/s41562-025-02325-z
