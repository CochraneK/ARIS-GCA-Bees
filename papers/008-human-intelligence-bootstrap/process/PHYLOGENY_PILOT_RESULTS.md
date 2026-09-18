# Phylogeny pilot · ARIS4C008

## Live resolution result

The 29 species in `data/pilot_taxa_v2.csv` were submitted to Open Tree of Life TNRS with:

- context: Animals;
- approximate matching: disabled;
- one exact match required per query.

**Result: 29 / 29 resolved, 0 unmatched, 0 approximate matches.**

All matches were species rank with score 1.0.

## Synonym reconciliation

One query requires explicit synonym handling:

- query: `Physeter macrocephalus`
- OpenTree matched taxon: `Physeter catodon`
- OTT id: 276851
- `is_synonym = true`

This mapping is retained rather than silently rewriting the canonical pilot name.

## OpenTree provenance

The live response reported Open Tree Taxonomy version **3.7** / source `ott3.7draft3`.

An induced subtree for all 29 OTT ids was successfully generated. The response reported **110 supporting studies** in the synthetic-tree provenance.

## Critical limitation

The OpenTree induced subtree solves the **taxonomic reconciliation + topology availability** problem. It does **not** by itself solve the branch-length problem.

The synthetic induced tree is not treated as a calibrated chronogram. Therefore:

- topology-aware sensitivity analyses can use it;
- confirmatory PGLS / evolutionary-rate analyses require a dated tree, justified branch-length transformation, or a model whose assumptions do not require calibrated divergence times;
- cross-kingdom breadth (vertebrates + mollusc + insects) makes a single high-quality dated species tree harder than within-clade analyses.

## Analysis strategy

Use a two-layer phylogenetic plan:

1. **Global topology layer:** OpenTree across all 29 taxa, mainly for non-independence diagnostics and topology-aware sensitivity.
2. **Dated within-clade layer:** use established dated phylogenies for sufficiently sampled clades (primates, birds, cetaceans/mammals) for formal comparative models.

This is preferable to assigning arbitrary equal branch lengths to the entire animal tree and pretending they represent evolutionary time.

## Files

- `data/opentree_taxonomy_v2.csv` — frozen TNRS mapping from the successful live run.
- `code/build_opentree_phylogeny.py` — reproducible resolver + induced-subtree builder.
- running the script also writes `data/opentree_v2_induced_subtree.tre` and metadata with supporting-study provenance.
