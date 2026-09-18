# Data source map · ARIS4C008

## Immediately useful open comparative sources

### Animal Culture Database (ACDB)
2025 Scientific Data resource. Initial version documents 128 culturally transmitted behaviours across 61 nonhuman species and provides species, groups, behaviours and sources tables.

Use:
- presence and breadth of putative cultural behaviours;
- behavioural domains;
- transmission modes;
- social-structure metadata;
- source-level evidence tracing.

Caveat: strong research-effort and taxonomic bias; absence is not evidence of no culture.

Paper: https://www.nature.com/articles/s41597-025-05315-y  
Repository: https://github.com/datadiversitylab/ACDB

### EVApeCognition
Open database of great-ape cognition studies from the Wolfgang Köhler Primate Research Center.

Use:
- within-great-ape cognitive task data;
- domain-level performance;
- development / social relationship analyses where available.

Source: https://www.eva.mpg.de/comparative-cultural-psychology/studying-non-human-primates/evapecognition-database/

### AnimalTraits
Curated body mass, metabolic rate and brain-size observations across almost 2,000 terrestrial species.

Use:
- brain/body scaling;
- energetic covariates;
- allometric correction.

Paper: https://www.nature.com/articles/s41597-022-01364-9

### PanTHERIA
Mammalian species-level life-history, ecological and geographical trait data; commonly distributed form has 5,426 observations and 55 variables.

Use:
- lifespan;
- reproductive / developmental traits;
- body size;
- group and ecological covariates.

### AVONET
All-bird functional trait resource: 11 continuous morphological traits and six ecological variables for 11,009 extant species, based on 90,020 individuals.

Use:
- bird morphology / ecology;
- body-size correction;
- integration with bird phylogenies.

Paper: https://onlinelibrary.wiley.com/doi/10.1111/ele.13898

### Amniote life-history database
Open life-history dataset with at least one of 29 life-history parameters for 21,322 birds, mammals and reptiles.

Use:
- age at maturity;
- generation time;
- reproductive investment;
- life-history comparisons.

Overview: https://www.weecology.org/data-projects/life-history/

### AnAge
Curated animal ageing and longevity resource, with thousands of animal entries and life-history fields.

Use:
- maximum longevity;
- ageing-related life-history variables.

Source: https://genomics.senescence.info/species/

### MoveTraits
2026 proof-of-concept standardized movement-trait database based on biologging, currently covering 97 bird and 52 mammal species in v0.1.

Use:
- comparable movement / space-use variables;
- behavioural ecology covariates.

Paper: https://onlinelibrary.wiley.com/doi/full/10.1111/ele.70297

## Additional sources to build or curate

### Neural architecture
Need a harmonized table distinguishing:
- brain mass / volume;
- relative brain measures;
- total neuron count;
- pallial / cortical neuron count where comparable;
- metabolic cost.

Likely requires synthesis from primary comparative neuroscience datasets rather than one universal source.

### Tool use and manipulation
Need a source-level database of:
- habitual versus facultative tool use;
- tool manufacture;
- sequential / compound tool use;
- transport;
- manipulator morphology;
- persistent constructions.

Do not collapse one-off captive demonstrations with habitual wild behaviour.

### Communication
Need comparable coding for:
- vocal production learning;
- referentiality;
- combinatoriality;
- compositionality;
- repertoire size;
- audience sensitivity.

### Teaching
Create a source-level evidence table with operational criteria rather than a species-level yes/no label.

### Hominin archaeology
Create a separate uncertainty-aware evidence table. Each proxy gets:
- date range;
- taxonomic attribution confidence;
- site count;
- preservation bias;
- behavioural interpretation alternatives.

## Merge keys and taxonomy

Canonical taxon key should be a current scientific species name plus a stable external taxonomy identifier where possible. Maintain synonym tables because cognition and culture literatures often use historical taxonomic names.

## Missingness policy

Missing behavioural data are not coded as zero.

For each trait store:
- observed positive;
- experimentally tested negative / failed;
- not tested;
- ambiguous;
- evidence disputed.

A research-effort covariate is mandatory for literature-derived behavioural variables.
