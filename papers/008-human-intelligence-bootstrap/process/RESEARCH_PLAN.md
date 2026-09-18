# Research plan · ARIS4C008

## Aim

Identify combinations of traits that best explain transitions toward broad, recombinable and open-ended cumulative intelligence while distinguishing:

- correlation from candidate mechanism;
- single-trait effects from conjunctions;
- enabling conditions from bottlenecks;
- phylogenetic inheritance from convergent evolution;
- ability demonstrated in captivity from naturally expressed culture.

## Phase 1 · Measurement architecture

### Outcomes

O1. individual innovation / flexible problem solving  
O2. stable socially transmitted traditions  
O3. cumulative improvement or supra-individual acquisition  
O4. cultural repertoire breadth across domains  
O5. recombination / specialization / distributed knowledge  
O6. persistent external information or artifact dependence  
O7. open-ended expansion of inherited solution space

The outcomes are not assumed to be a strict ladder. O7 is not defined as "being human"; explicit coding criteria are in `OUTCOME_CODEBOOK.md`.

### Predictors

Use the frozen condition ontology:
cognition, social transmission, communication, manipulation, externalization, social architecture, life history, energetics, ecology and demography/network structure.

## Phase 2 · Evidence matrix

Build a species × trait × evidence table.

Every cell can carry:
- value;
- uncertainty;
- evidence state;
- evidence type;
- wild/captive context;
- number of studies;
- source;
- evidence strength;
- research-effort metadata;
- last update.

A literature "not found" must never be converted silently to trait absence.

## Phase 3 · Candidate-condition falsification

For every proposed condition X and outcome Y:

1. search for **X-high / Y-low** taxa — attacks sufficiency;
2. search for **X-low / Y-high** taxa — attacks necessity;
3. find phylogenetically distant **X-high / Y-high** cases — tests convergent replication;
4. find close relatives differing in Y — reduces broad phylogenetic confounding;
5. inspect whether X precedes Y in hominin time slices.

This condition audit happens before any headline model.

## Phase 4 · Comparative models

### Baseline
- phylogenetic generalized models for continuous outcomes;
- phylogenetic logistic / ordinal models where state counts justify them;
- clade random effects and measurement-error terms;
- body-size/allometric correction;
- explicit research-effort adjustment.

### Competing architecture models

Compare at least:

1. additive / weighted-sum model;
2. sparse interaction model;
3. multiplicative / geometric-mean model;
4. weakest-link / minimum-module model;
5. threshold model with learned change points.

The scientific question is whether advanced cultural outcomes behave more like total "skill points" or like a system that stalls when one critical module remains below threshold.

### Phylogenetic transition analysis

For traits with enough independent origins:
- correlated-evolution models;
- stochastic character mapping;
- transition-order analysis.

Do not force transition models when state counts are sparse.

### Set-theoretic exploratory analysis

Fuzzy-set QCA / necessary-condition analysis can be useful for configuration discovery, but remains secondary because standard forms do not automatically handle phylogenetic dependence, measurement error or strong missingness.

## Phase 5 · Hominin temporal triangulation

Create a separate archaeological evidence matrix.

Ask:
- which candidate conditions clearly precede later cultural acceleration?
- which arise approximately with it?
- which could be consequences of already-expanded culture?
- are there long intervals in which a proposed "sufficient" condition existed without open-ended growth?

Use date ranges and sensitivity analysis rather than false point precision.

## Phase 6 · Bootstrap proximity

Only after model validation, calculate descriptive module profiles for living taxa.

Outputs may include:
- uncertainty-aware module profiles;
- trait-space projections;
- distance to candidate bootstrap regions;
- missing-module explanations.

Do **not** publish a deterministic "next species to become human" forecast.

## Competing models

### Model A · Additive skill-points
High values in some modules can compensate for weaknesses elsewhere.

### Model B · Bottleneck / weakest link
Advanced accumulation is constrained by the lowest critical module.

### Model C · Network memory
Distributed cognition across connected individuals and generations is the central transition.

### Model D · Embodied externalization
Cognition becomes technologically cumulative when organisms can manipulate the world and leave persistent information-rich traces.

### Model E · Feedback loop
Once several modules co-occur, culture changes ecology, energy access, development and selection, creating a self-reinforcing gene-culture loop.

## Major threats

- publication bias toward famous "smart" taxa;
- task incomparability across sensory/motor systems;
- anthropocentric outcome definitions;
- species-level pseudo-replication;
- phylogenetic non-independence;
- ecological opportunity masquerading as cognitive absence;
- brain size used as a circular intelligence proxy;
- missing-not-at-random behavioural evidence;
- captive performance generalized to wild culture;
- archaeological preservation bias;
- reverse causality from culture to life history, energetics and social organization.

## Pre-registered falsification logic

A candidate **necessary** condition is weakened by a well-supported independent origin of the target outcome without it.

A candidate **sufficient** condition is weakened when it repeatedly occurs at high levels without the target outcome.

The bootstrap model is weakened if additive models predict held-out clades and transitions consistently better than interaction, threshold or weakest-link models.

The embodiment hypothesis is weakened if broad cumulative technology appears in taxa with very limited manipulation and persistent externalization.

The network-memory hypothesis is weakened if cultural breadth is unrelated to accessible network structure after research effort, phylogeny and individual cognition are controlled.

## Deliverable sequence

1. outcome codebook + condition ontology;
2. closest-prior-work / novelty map;
3. seed data integration;
4. 20–40 species contrast-maximizing pilot matrix;
5. missingness and research-bias audit;
6. model-recoverability simulation;
7. full literature expansion;
8. preregistration;
9. confirmatory comparative analysis;
10. manuscript + public Animal Bootstrap Atlas.
