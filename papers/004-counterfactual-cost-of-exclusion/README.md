# ARIS4C004 · The Counterfactual Cost of Exclusion

**Full title:** *The Counterfactual Cost of Exclusion: Mental Health and Keystone Individuals in Human Knowledge Networks*

**Status:** feasibility / ARIS run

**ARIS provenance:** v0.4.26 · `951654847b015585385b2448c5667dcd04e7b56b`

## Canonical research question

> Among historically realized knowledge contributors, how would scientific, intellectual, or cultural development change if productive participation were reduced, after allowing realistic substitution, independent discovery, and network rewiring — and what does that imply for exclusion risks faced by people with well-documented mental-health conditions?

The project does **not** test whether mental illness causes genius or creativity. It studies the potential opportunity cost of exclusion while allowing the counterfactual effect to be positive, zero, or negative.

A crucial scope limit is explicit: people who were excluded before leaving observable historical traces are largely absent from the data. The primary study therefore estimates effects among **historically visible / realized contributors**, not the full societal cost of mental-health discrimination. Where appropriate, positive observed-node effects may be interpreted as a partial or lower-bound component of a broader opportunity cost, not as the total loss.

## Three estimands that must remain separate

1. **Structural position (descriptive):** do knowledge producers with strong surviving mental-health evidence occupy different network positions from appropriately matched comparison nodes?
2. **Counterfactual Participation Effect, CPE (simulation):** how does a network outcome change when a focal person's future productive participation is attenuated, after allowing realistic substitution, delays, and rewiring?
3. **Discrimination-scaled CPE (scenario analysis):** what network-level effect follows when externally defensible discrimination/participation-penalty distributions are applied? This is a scenario-based policy estimand unless the historical discrimination mechanism is directly identified.

These estimands must never be collapsed into a claim that a psychiatric condition itself produced a person's contribution.

## Sign-neutral primary quantity

For focal person `i`, attenuation level `a`, and intervention time `t0`:

`CPE_i(a,t0) = V(G_observed) - E[V(G_counterfactual | i, a, t0, adaptation)]`

Interpretation:

- `CPE > 0`: observed participation increased the chosen outcome; reducing participation would lower it;
- `CPE = 0`: replacement/recovery is effectively complete;
- `CPE < 0`: the modeled counterfactual adaptation improves that outcome, for example through outsider entry or alternative directions.

The phrase **cost of exclusion** is therefore an empirical interpretation of positive CPE components, not something assumed by definition.

## Frozen conceptual decisions before ARIS

1. The primary counterfactual is **participation reduction**, not "the person never existed."
2. Counterfactual interventions are temporal: work created before `t0` remains available unless a separate censorship/destruction scenario is explicitly modeled.
3. Mental-health history/evidence is not an explanation for creativity or achievement.
4. Historical examples such as John Nash, Friedrich Nietzsche, or Vincent van Gogh may motivate the question but must not define the sample.
5. Build and freeze the candidate sampling frame **before** mental-health evidence coding.
6. `Unknown` mental-health history is not equivalent to `no disorder` or "healthy."
7. Retrospective psychiatric evidence must be graded and uncertainty-aware; unsupported modern labels cannot enter confirmatory analyses.
8. Direct output, downstream propagation, independent precursor paths, substitution, and recovery must be modeled separately.
9. Network adaptation is mandatory. A naïve deletion model is only an upper-bound-like stress test.
10. Models must permit counterfactual gains as well as losses.
11. Cross-domain network scores cannot be compared raw. Domains require validated domain-specific outcomes and only later, if justified, standardized/hierarchical synthesis.
12. Documentation intensity must be measured because famous people are more likely to have surviving biographies, medical records, correspondence, and later diagnostic speculation.
13. The final confirmatory number of domains and people will be determined from the feasibility pilot, not chosen to maximize a preferred result.
14. Primary quantitative analyses use **deceased persons only**; the project will not infer psychiatric diagnoses of living people.
15. No paid LLM API is required. API-gated ARIS reviewer/research stages use GPTPage handoffs, with factual claims independently checked against primary literature or official data documentation.

## Mental-health evidence tiers

The canonical details live in `process/EXPOSURE_CODEBOOK.md`. The current structure is:

- **A1:** contemporaneous clinical diagnosis/record with clear provenance.
- **A2:** strong contemporaneous clinical encounter/hospitalization/treating-clinician evidence where a modern label is uncertain.
- **B1:** multiple strong contemporaneous nonclinical sources documenting meaningful syndrome/impairment.
- **B2:** rigorous scholarly historical/medical reconstruction with primary-source trail and explicit uncertainty.
- **C:** later/speculative retrospective attribution without adequate evidence.
- **U:** unknown / insufficient evidence.

Strict confirmatory exposure should use Tier A if precision permits; Tier A+B is a prespecified sensitivity family. Tier C cannot silently become confirmed diagnosis.

## Candidate knowledge-network layers

The project treats knowledge production as a temporal multiplex network. Candidate layers include:

- person → work (authorship/creation)
- work → work (citation/reference)
- person ↔ person (coauthorship/collaboration)
- mentor → trainee / advisor → student
- person/work → concept/topic
- person/work → later person/work via explicitly documented influence
- movement/school/institution membership where historically meaningful

Each edge type remains distinguishable; a citation, coauthorship tie, teacher-student relation, and art-historical influence claim are not interchangeable evidence.

## Counterfactual model families

### M0 — Naïve attenuation / removal
Reduce focal future participation with no compensation. Transparent stress test only.

### M1 — Observed alternative-path recovery
Allow recovery through alternative paths and precursors that are already observable using information available before the intervention time.

### M2 — Dynamic adaptive rewiring
Allow temporally eligible collaborators, competitors, neighboring researchers, and outsiders to enter or rewire using only pre-intervention information. Replacement may be delayed.

### M3 — Alternative-precursor / discovery-delay model
Where data allow, treat later ideas/results as having multiple precursor paths so the absence of one person can delay rather than permanently erase an outcome.

No single simulated graph is presented as "the" true alternative history. Results are distributions across explicit counterfactual families and parameter ranges.

## Sampling strategy

Do **not** begin with a hand-built list of "mentally ill geniuses."

The pilot first builds mental-health-independent candidate frames in three deliberately different data environments:

1. **Science / mathematics** — high-structure bibliometric and collaboration data; primary quantitative route.
2. **Philosophy / literature / intellectual history** — intermediate structure; conditional portability pilot.
3. **Visual arts / music** — difficult cultural-network setting; high-risk portability stress test.

Initial pilot target: roughly **150–300 total candidate people across the three domain families**, stratified by time and baseline prominence/impact. This is **not** a quota for diagnosed/exposed cases. The number of Tier-A/Tier-B cases is discovered after the candidate frame is frozen.

A domain advances only if it clears prospective identity, network-coverage, exposure-yield, comparison-support, documentation-balance, edge-provenance, and simulation-stability gates. If only science passes, the first paper becomes science-of-science rather than forcing a weak cross-domain result.

The main-study N will be chosen from pilot-observed evidence yield, missingness, CPE variance, dependence among subnetworks, match quality, and simulation-based precision/power. There is no fixed promise such as "300 diagnosed famous people."

## Time window

The preferred strict quantitative window is **1900–2000**, subject to pilot coverage. **1800–2000** is a broader sensitivity/extension window. Earlier figures need not be forced into the same confirmatory model.

## Candidate data sources

- **OpenAlex** — primary science graph: works, authors, topics, institutions, references/citations.
- **Wikidata** — cross-domain entity resolution and relationship leads; machine-readable `medical condition` or `influenced by` claims are not confirmatory evidence by themselves.
- **Laouenan et al. cross-verified notable-people database** — candidate cross-domain historical sampling frame, with its notability/coverage biases explicitly modeled.
- **Crossref** and domain bibliographies — supplementary publication/reference metadata.
- **Curated biographies, archival/medical sources, scholarly histories, and authority records** — mental-health evidence and non-bibliometric influence verification.
- **Semantic Scholar** — optional enrichment only if licensing/use terms fit the reproducible public pipeline; OpenAlex is preferred where sufficient.

Raw copyrighted biographies, clinical documents, or restricted API dumps should not be redistributed. Store source identifiers, derived codes, provenance, and reconstruction instructions.

## Closest methodological anchors identified so far

- **Azoulay, Fons-Rosen & Graff Zivin (2019), AER**, "Does Science Advance One Funeral at a Time?" (`10.1257/aer.20161574`): 452 premature star deaths; collaborator losses coexist with increased outsider entry, motivating sign-neutral adaptive counterfactuals.
- **Azoulay, Graff Zivin & Wang (2010), QJE**, "Superstar Extinction": star deaths and persistent collaborator productivity effects.
- **Mohnen (2022), Management Science**, "Stars and Brokers" (`10.1287/mnsc.2021.4032`): brokerage structure predicts spillover losses.
- **Ludwig (1992)** and **Post (1994)**: large historiometric samples show that "famous people + psychopathology" is old territory, so that observation is not the novelty claim.
- **Acar, Chen & Cayirdag (2018), Schizophrenia Research** (`10.1016/j.schres.2017.08.036`): cautions against a simple positive disorder→creativity assumption.
- **Muramoto (2014)** (`10.1186/1747-5341-9-10`) and **Karenberg (2009)** (PMID `19591388`): motivate uncertainty-aware, historically contextualized retrospective evidence.

## Major threats to validity

- invisible people excluded before producing observable traces
- fame/notability selection and collider bias
- documentation/archival-density bias
- retrospective-diagnosis error
- differential record survival across countries, languages, genders, classes, and eras
- domain-dependent meaning of an "influence" edge
- bibliometric coverage and author-disambiguation bias
- multiple plausible alternative histories
- conflating condition burden, treatment effects, stigma, and formal discrimination
- over-crediting one predecessor when downstream outcomes have several precursors
- look-ahead bias in choosing substitutes
- interpreting simulated counterfactuals as observed historical facts

## Falsification / downgrade logic

The preferred broad interpretation weakens substantially if:

- adaptive replacement recovers nearly all outcomes across focal nodes;
- high-confidence-edge analyses eliminate apparent effects;
- results are driven by a few famous examples;
- exposure evidence is too uncertain or sparse;
- comparison/random subsets show similar or larger CPE under the same intervention;
- documentation common support fails;
- plausible rewiring/substitution settings routinely reverse conclusions;
- humanities/arts cannot support reproducible influence edges;
- conclusions exist only for one arbitrary composite weighting;
- discrimination-scaled results require implausible participation penalties.

A null or negative result is informative: it would imply more redundancy/adaptive capacity than the motivating intuition assumed.

## Current ARIS gate

Canonical process files now include:

- `process/IDEA_REPORT.md`
- `process/AUTO_REVIEW.md`
- `process/DATA_FEASIBILITY.md`
- `process/EXPOSURE_CODEBOOK.md`
- `process/RESEARCH_PLAN.md`
- `process/GPTPAGE_HANDOFF.md`
- `process/STATUS.md`

The next gate is executable feasibility:

1. implement candidate/network/exposure schemas and validation;
2. build a reproducible science-pilot acquisition/resolution path;
3. implement M0/M1 and a bounded M2 simulator skeleton;
4. test synthetic invariants and no-look-ahead behavior;
5. obtain pilot coverage/evidence-yield metrics;
6. use those metrics to set final N and decide whether humanities/arts graduate beyond portability pilots.
