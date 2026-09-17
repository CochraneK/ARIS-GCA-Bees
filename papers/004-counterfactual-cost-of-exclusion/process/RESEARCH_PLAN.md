# RESEARCH PLAN — ARIS4C004

## Title

**The Counterfactual Cost of Exclusion: Mental Health and Keystone Individuals in Human Knowledge Networks**

## Stage

Feasibility → preregistration design. No confirmatory outcome analysis yet.

---

# 1. Aim

Estimate how much observable scientific/knowledge-network development would change under counterfactual reductions in the productive participation of historically realized contributors with strong evidence of mental-health conditions, while explicitly allowing for:

- alternative contributors;
- network rewiring;
- independent precursor paths;
- delayed rather than permanently lost discoveries;
- uncertainty in historical mental-health evidence;
- documentation and selection bias.

The project does **not** estimate whether mental illness causes creativity and does **not** claim to recover the full societal loss from people who were excluded before leaving historical traces.

---

# 2. Target population and scope

## Primary quantitative paper

**Science / mathematics first.**

Primary target population:

> deceased, historically visible scientific/mathematical knowledge producers in a preregistered modern historical window who can be resolved to an adequate scholarly-network footprint.

The exact time window will be selected from pilot coverage, with **1900–2000** the preferred strict window and **1800–2000** a broader sensitivity window.

"Historically visible" is an explicit target-population restriction, not a claim to represent all potential contributors.

## Portability pilots

- philosophy / literature / intellectual history;
- visual arts / music.

These domains are not required to survive into the first confirmatory paper.

## Living persons

Primary analysis is **deceased persons only**. No psychiatric inference about living people.

---

# 3. Conceptual variables

Keep the following variables distinct:

- `MH`: underlying mental-health condition/history (partly latent historically);
- `E`: strength/type of surviving mental-health evidence;
- `D`: documentation intensity / archival richness;
- `X`: stigma, discrimination, or formal exclusion mechanism;
- `S`: symptom/condition burden;
- `T`: treatment/access effects;
- `P(t)`: productive participation over time;
- `N(t)`: knowledge-network position and links over time;
- `Y(t)`: knowledge outputs and downstream outcomes.

The policy story of interest is primarily:

`X -> P(t) -> network development / Y(t)`

but historical `X` is often not observed. Therefore most discrimination-scaled analyses are scenarios, not direct causal estimates.

A separate pathway exists:

`S/T -> P(t) -> Y(t)`

and must not be mislabeled discrimination.

Documentation is generated partly by fame/achievement and health history, so conditioning carelessly on `D` or historical notability can create collider bias.

---

# 4. Mental-health-independent sampling frame

## Pilot

Construct approximately **150–300 total candidates** across the three pilot domain families, sampled before mental-health evidence coding.

### Science candidate-frame options

Preferred:

1. identify eligible notable scientific/mathematical contributors from the Laouenan et al. cross-verified notable-person dataset;
2. resolve to OpenAlex/Wikidata identifiers;
3. stratify by field/subfield, cohort, geography where feasible, and baseline prominence/impact;
4. supplement with an OpenAlex-derived high-impact stratum to reduce dependence on Wikipedia notability alone.

The goal is not a population prevalence estimate. It is a reproducible universe of historically visible contributors suitable for counterfactual network analysis.

### Pilot strata

At minimum:

- cohort/era;
- field/subfield;
- baseline impact/prominence tier;
- region/language context where feasible;
- gender where source coverage permits.

Freeze the candidate list before exposure coding.

---

# 5. Mental-health evidence protocol

## Evidence classes

- **A1:** contemporaneous clinical diagnosis/record with clear provenance.
- **A2:** documented hospitalization/treating-clinician evidence with meaningful syndrome evidence but uncertain modern label.
- **B1:** multiple strong contemporaneous nonclinical sources documenting a clinically meaningful syndrome/impairment.
- **B2:** rigorous scholarly historical/medical reconstruction with primary-source trail and explicit uncertainty.
- **C:** later/speculative retrospective label without adequate primary support.
- **U:** insufficient evidence.

Primary exposed definition: **Tier A (A1+A2)** if N permits.  
Sensitivity: **Tier A+B**.

Do not create a literal "healthy control" variable.

## Coding fields

For every candidate:

- canonical person IDs;
- evidence class;
- historical wording;
- any modern mapped label in a separate field;
- evidence date;
- source type;
- source identifier/DOI/archive citation;
- direct/secondary source flag;
- coder;
- adjudication note;
- blinded-to-network-outcome flag;
- documentation-intensity vector.

## Reliability

Pilot at least 20–30 ambiguous cases with two independent coders if resources permit. Report agreement on evidence class and resolve disagreements by written adjudication rules.

---

# 6. Knowledge-network construction — science core

Construct a temporal multiplex graph with explicit edge types.

## Node types

- person/author;
- work/publication;
- topic/subfield;
- institution (secondary);
- concept/idea where reliably mapped (exploratory).

## Edge types

- author → work;
- work → cited work;
- author ↔ coauthor;
- work → topic;
- author → institution over time;
- advisor → trainee where source quality permits.

OpenAlex is the preferred core graph source. Crossref/Wikidata/domain genealogy sources may supplement.

## Temporal rule

No counterfactual decision at time `t` may use information that first becomes available after `t` to choose substitutes, except in explicitly labeled oracle/upper-bound sensitivity analyses.

This avoids look-ahead bias.

---

# 7. Intervention definition

The intervention is **participation attenuation**, not erasure from existence.

For focal person `i`, intervention begins at `t0` and attenuates future participation by intensity `a`.

Candidate intensities:

- 25%;
- 50%;
- 75%;
- 100%.

## Timing families

### Primary candidate

**Early-career gate:** `t0` immediately before first stable entry into the observable knowledge-production network.

This represents denial of entry/opportunity rather than retroactive destruction of existing work.

### Secondary

- career-wide attenuation from first observed work;
- historically documented exclusion episode;
- late-career attenuation.

Any work created before `t0` remains in the network unless a separate censorship/destruction model is explicitly declared.

---

# 8. Sign-neutral estimand

Replace directionally loaded "loss" notation with:

`CPE_i(a,t0) = V(G_observed) - E[V(G_cf | i, a, t0, adaptation model)]`

**CPE = Counterfactual Participation Effect.**

Interpretation:

- `CPE > 0`: observed participation increased the value metric; exclusion would reduce it;
- `CPE = 0`: substitution/recovery is complete;
- `CPE < 0`: the counterfactual adaptation improves that value metric.

The phrase "cost of exclusion" applies to positive components/effects, not by definition.

---

# 9. Counterfactual model families

Do not rely on one rewiring rule.

## M0 — Naïve deletion / upper-bound stress test

Remove the attenuated fraction of focal future output and dependent focal edges with no compensation.

Purpose: transparent upper-bound-like baseline. Not preferred historical model.

## M1 — Observed-alternative-path recovery

For each affected downstream work/path, ask whether non-focal, temporally prior alternative sources/precursors already provide redundant access to similar knowledge/topics.

Use citation-path redundancy, topic proximity, and non-focal precursor availability.

This model is relatively conservative because it only uses alternatives visible in the observed graph.

## M2 — Dynamic network rewiring

Allow collaborators/nearby authors and outside entrants to create replacement links/outputs according to pre-`t` information:

- prior productivity/capacity;
- topic similarity based only on prior work;
- network distance;
- institutional/geographic opportunity;
- field entry rates;
- latent/redundant tie evidence.

Replacement can be delayed.

## M3 — Alternative-precursor / discovery-delay model

Where possible, represent a downstream innovation as having multiple precursor paths. Removal of one precursor changes hazard/timing of later appearance rather than necessarily deleting it forever.

This may be exploratory if concept-level data are insufficient.

## Calibration / plausibility bounds

Use empirical star-loss studies to bound plausible collaborator decline, outsider entry, and recovery dynamics. Do not import one published coefficient as a universal structural parameter.

---

# 10. Structural dependency measures

To avoid assigning all descendants to one predecessor, compute redundancy-aware quantities.

Candidate measures:

- number/proportion of alternative temporal citation paths after focal removal;
- edge-/node-disjoint path counts;
- temporal dominator-like dependence: downstream nodes for which focal works are unavoidable under the chosen path definition;
- local brokerage and community bridging;
- sampled marginal contribution / Shapley approximation on bounded local subgraphs;
- delay to first alternative path/source.

Shapley calculations are secondary unless computational and interpretive validation is strong.

---

# 11. Primary science-domain outcome set

Avoid one opaque greatness/network-value score.

## Primary outcomes

1. **Recovered future output:** fraction of affected future topic/subfield production retained under adaptation.
2. **Recovered impact:** fraction of field/year-normalized downstream impact retained.
3. **Collaborator trajectory:** change in simulated/empirically calibrated collaborator production.
4. **Outsider entry/diversity:** change in new entrant share and topic/source diversity.
5. **Recovery time:** time required for output/impact to return to a prespecified fraction of observed or counterfactual benchmark trajectory.

## Secondary structural outcomes

- reachability;
- brokerage loss;
- community fragmentation;
- path redundancy;
- topic diversity.

## Composite

Only create a composite CPE if:

- component directions/scales are preregistered;
- weights are justified before results;
- all components remain separately reported.

---

# 12. Comparison and null benchmarks

Mental-health specificity must survive strong nulls.

For each exposed focal person, construct a pool of comparison nodes within:

- era/cohort;
- field/subfield;
- geography/language where feasible;
- baseline productivity/impact;
- documentation intensity.

Use two benchmark families because network-position matching changes the scientific question.

## Benchmark A — contribution-context matched

Match on baseline output/impact/documentation but **not tightly on network centrality**. Tests whether exposed focal nodes generate unusual counterfactual effects relative to broadly comparable contributors.

## Benchmark B — role matched

Additionally match on pre-intervention network role/centrality. Tests whether any difference remains beyond occupying a similar structural position.

Other nulls:

- equal-size random subsets;
- stratified label permutation where defensible;
- celebrity-excluded analyses;
- Tier A only;
- high-confidence-edge only.

Comparison nodes should be called `non-exposed-by-primary-evidence` or `comparison`, not "healthy," unless unusually strong negative evidence supports that label.

---

# 13. Documentation-bias model

Construct `D_i`, a documentation-intensity vector or score.

Candidate features:

- number of independent biographies/reference entries;
- number of language editions / cross-verification group;
- archive/correspondence availability;
- scholarly biography count;
- medical/pathography literature count;
- institutional/authority records;
- proxy measures such as biography length only as noisy secondary indicators.

Use `D_i` in:

- matching/weighting;
- missingness models;
- sensitivity analyses;
- exposure-yield reporting.

Do not simply regress it away if it is a collider for a causal question; use it primarily to define common support and characterize ascertainment.

---

# 14. Pilot acceptance rules

Use `DATA_FEASIBILITY.md` as canonical gate definitions.

Critical science-domain goals include:

- >=95% identity resolution;
- >=80% sufficient network data;
- >=15 Tier-A/B exposed cases in pilot to justify expansion;
- >=3 plausible comparison candidates per exposed focal;
- adequate overlap in documentation intensity;
- stable counterfactual results across repeated seeds/parameter ranges.

These are feasibility gates, not final sample-size targets.

---

# 15. Final N / precision design

Do not use a conventional one-line power calculation before observing pilot network dependence.

After pilot, estimate:

- exposed evidence yield;
- CPE variance;
- within-field clustering;
- match quality;
- dependence among focal subnetworks;
- missingness;
- simulation Monte Carlo variance.

Run a simulation grid over candidate exposed N values (e.g. 20, 30, 50, 75, 100, 150+) and choose a target based primarily on **precision and robustness**:

- width of the 95% interval for mean/median standardized CPE;
- power/coverage for comparison-vs-null contrasts;
- stability across adaptation models.

A useful planning target is to avoid promising a main effect unless the interval is meaningfully narrower than the differences among plausible counterfactual models.

---

# 16. Statistical analysis

## Focal-level estimation

For every focal node, produce a distribution of CPE under:

- intervention intensity;
- timing;
- adaptation model;
- evidence uncertainty;
- edge uncertainty;
- simulation seed.

## Aggregate summaries

Within domain:

- mean/median CPE with cluster/bootstrap intervals;
- quantiles and heavy-tail behavior;
- proportion positive/near-zero/negative;
- heterogeneity by brokerage/redundancy, not by diagnosis label as a creativity mechanism.

## Comparison analyses

Use matched/weighted contrasts with uncertainty propagated from simulation. Account for repeated use of comparison nodes and overlapping network neighborhoods.

## Cross-domain synthesis

If multiple domains survive:

- report each domain separately;
- standardized effect summaries only after construct alignment;
- hierarchical/meta-analytic synthesis as secondary;
- do not rank individuals or disciplines on a universal "importance" scale.

---

# 17. Mental-health discrimination scenario layer

This layer comes **after** the structural counterfactual model works.

Parameterize participation attenuation from three source families:

1. historically documented formal exclusion/discrimination episodes where available;
2. modern empirical stigma/discrimination literature, clearly marked as modern-policy scenarios;
3. hypothetical stress tests (25/50/75/100%).

Output:

`Expected network effect = integrate CPE(a,t0) over a plausible attenuation distribution`

Do not call this an observed historical causal effect unless the participation parameter is historically identified.

---

# 18. Sensitivity analyses

Mandatory:

- Tier A only vs Tier A+B;
- strict 1900–2000 vs broader 1800–2000 where feasible;
- alternate documentation common-support rules;
- high-confidence edges only;
- M0/M1/M2 counterfactual families;
- weak/moderate/strong replacement;
- no future-information substitution rule;
- role-matched vs contribution-context matched benchmarks;
- leave-most-famous-cases-out;
- field leave-one-out;
- alternate OpenAlex author-resolution confidence filters;
- intervention timing alternatives;
- outcome-component-by-component reporting.

---

# 19. Negative controls / falsification

The broad exclusion-cost interpretation weakens if:

- adaptive models recover nearly all outcomes for almost every focal node;
- apparent effects vanish under high-confidence edges;
- results depend on celebrity cases chosen in advance;
- comparison/random subsets yield indistinguishable or larger effects under the same intervention distribution;
- exposure evidence is too sparse/uncertain to define the focal set;
- documentation common support fails;
- plausible replacement parameters reverse conclusions routinely;
- the result exists only for one arbitrary composite weighting.

A negative or near-zero result remains scientifically useful: it would demonstrate greater historical network redundancy than the motivating intuition assumed.

---

# 20. Ethics and language

- deceased-only primary sample;
- no remote diagnosis of living people;
- distinguish historical evidence from modern labels;
- do not romanticize severe illness;
- do not describe a condition as a source of genius unless independently demonstrated, which this design is not intended to do;
- emphasize social inclusion and opportunity-cost modeling rather than voyeuristic pathology of famous people;
- avoid unnecessary details of self-harm, hospitalization, or private medical history when not needed for coding.

---

# 21. Data/repository architecture

Proposed paper folder:

```text
004-counterfactual-cost-of-exclusion/
├── paper.json
├── README.md
├── code/
│   ├── config/
│   ├── acquire/
│   ├── resolve/
│   ├── exposure/
│   ├── network/
│   ├── simulate/
│   └── analysis/
├── data/
│   ├── README.md
│   ├── raw/          # gitignored/reconstructable
│   ├── interim/
│   └── derived/
├── figures/
├── manuscript/
└── process/
    ├── STATUS.md
    ├── IDEA_REPORT.md
    ├── AUTO_REVIEW.md
    ├── DATA_FEASIBILITY.md
    ├── EXPOSURE_CODEBOOK.md
    ├── RESEARCH_PLAN.md
    └── GPTPAGE_HANDOFF.md
```

Raw restricted/large data are reconstructed, not committed.

---

# 22. Execution sequence

## Gate A — novelty and causal framing

- exact prior-work search;
- DAG/estimand adversary;
- freeze lower-bound/realized-contributor interpretation.

## Gate B — exposure protocol

- finalize evidence codebook;
- pilot coder agreement;
- freeze deceased-only and negative/comparison terminology.

## Gate C — science data pilot

- candidate-frame acquisition;
- OpenAlex resolution;
- network-coverage audit;
- documentation-intensity variables;
- exposure-yield audit.

## Gate D — simulator validation

- implement M0 and M1;
- implement bounded M2;
- test recovery behavior on known star-loss-like cases or synthetic benchmarks;
- ensure no look-ahead substitution.

## Gate E — N/precision

- use pilot variance/dependence to set expansion N;
- preregister primary outcomes and robustness family.

## Gate F — humanities/arts portability

- run edge-audit;
- promote only if data gates pass.

## Gate G — confirmatory run

- freeze code/config;
- run exposure-defined focal and comparison simulations;
- report all preregistered outcomes including null/negative results.

---

# 23. Current decision

**Proceed continuously through feasibility.**

The immediate next blocking deliverables are:

1. `EXPOSURE_CODEBOOK.md`;
2. `GPTPAGE_HANDOFF.md`;
3. executable science-pilot schemas/acquisition scripts;
4. pilot candidate-frame test;
5. sign-neutral simulator skeleton.
