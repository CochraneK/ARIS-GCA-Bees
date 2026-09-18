# STATUS · ARIS4C008

Updated: 2026-09-18

## Current state

ARIS4C008 has moved from research-design scaffolding into **pilot evidence integration and design stress-testing**.

The original "animal skill-point allocation" intuition is now operationalized as a test of additive, threshold, weakest-link and feedback architectures for open-ended cumulative intelligence.

## Completed

- [x] canonical research question frozen at design level;
- [x] multidimensional O1–O7 outcome codebook;
- [x] candidate-condition ontology;
- [x] initial 25-taxon comparative scaffold;
- [x] source-level evidence schema with explicit missingness states;
- [x] Animal Culture Database v0.1 pilot extraction;
- [x] 13 direct ACDB pilot-species matches, 32 groups and 42 cultural-behaviour records extracted;
- [x] scope-aware literature evidence seed expanded to 24 source-traceable rows;
- [x] exact-species versus genus/family/clade exemplar evidence separated;
- [x] scope-aware coverage matrix;
- [x] first 25-taxon pilot evidence matrix;
- [x] toy model-recoverability simulation;
- [x] model-discriminating panel-v2 sampling principle;
- [x] AnimalTraits v1.0.7 ingestion code prepared.

## Pilot coverage

Current scope-aware seed coverage:

- **14 / 25** taxa have exact-species literature seed evidence;
- **5 / 25** additional taxa have exact-species ACDB coverage without a separate literature-seed row;
- **5 / 25** currently rely on genus-level exemplar evidence;
- **1 / 25** currently relies on family-level exemplar evidence.

Thus **19 / 25** pilot taxa currently have at least one exact-species evidence route suitable for expansion into the primary matrix. The remaining six require exact-species resolution or must remain sensitivity-analysis taxa.

No missing database record is interpreted as absence of an ability.

## Model-recoverability lesson

A toy simulation with eight latent modules showed that small, famous-"intelligent"-animal panels can make additive, threshold and weakest-link mechanisms difficult to distinguish, especially with 20–40% missing behavioural data.

At 25 taxa / 20% missingness, selecting taxa for disagreement among candidate models increased mean exact architecture recovery from about **0.45 to 0.59** in the toy setup. Gains were largest for threshold and weakest-link models.

This is a **design diagnostic, not a biological power analysis**.

## Key design change

The first 25 taxa are now treated as a seed panel, not the final sample.

Panel v2 will deliberately seek:
- high-average / one-severe-bottleneck configurations;
- balanced moderate configurations;
- threshold-straddling configurations;
- cognition-matched but embodiment-different pairs;
- social-learning-matched but life-history/network-different pairs;
- ordinary negative/calibration taxa.

## Pilot 2 additions

- [x] parsed frozen AnimalTraits v1.0.7 and generated pilot body/brain/metabolic summaries;
- [x] parsed AnAge bulk life-history data and generated a normalized pilot extract;
- [x] joined culture/cognition evidence with energetic and life-history coverage in `pilot_matrix_v1.csv`;
- [x] resolved the seed panel to 29 species-level taxa in `pilot_taxa_v2.csv`;
- [x] added reproducible ingestion scripts for AnimalTraits and AnAge;

Current integrated coverage in the 25-label v1 matrix includes longevity for 22 labels, AnimalTraits brain-size records for 10, and at least one metabolic-rate source for 6. Scope flags distinguish exact species from exemplars.

## In progress

- [ ] rebuild all downstream matrices on the 29-taxon species-level v2 panel;
- [ ] quantify research effort per taxon and module;
- [ ] harmonize neural measures beyond raw brain mass (relative brain measures, neuron counts where comparable);
- [ ] expand each core module beyond one or two flagship papers;
- [ ] choose compatible phylogenetic trees and taxonomic reconciliation rules;
- [ ] build hominin archaeological time-slice layer;
- [ ] complete closest-prior-work novelty map for explicit necessary/sufficient-configuration claims;
- [ ] simulate recoverability using the **observed** missingness structure rather than toy missingness;
- [ ] freeze exact ARIS engine version/commit and begin formal full ARIS run.

## Current assessment

**Scientific framing: strong. Data integration: underway. Confirmatory analysis: not yet ready.**

The project should not advance to a headline "minimal sufficient set" until the exact-species panel, research-effort correction and phylogenetic layer pass their gates.
