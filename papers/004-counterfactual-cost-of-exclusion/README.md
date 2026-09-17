# ARIS4C004 · The Counterfactual Cost of Exclusion

**Full title:** *The Counterfactual Cost of Exclusion: Mental Health and Keystone Individuals in Human Knowledge Networks*

**Status:** feasibility / ARIS run

**ARIS provenance:** v0.4.26 · `951654847b015585385b2448c5667dcd04e7b56b`

## Canonical research question

> If people with well-documented mental-health conditions are prevented from participating fully in scientific, intellectual, or cultural production, how much direct and downstream knowledge-network value can be lost after allowing the system to adapt, substitute, and rewire?

The project does **not** test whether mental illness causes genius or creativity. It studies the potential opportunity cost of exclusion.

## Three estimands that must remain separate

1. **Structural importance (descriptive):** are knowledge producers with documented mental-health histories located in unusually consequential network positions relative to matched comparison nodes?
2. **Replacement-adjusted participation loss (simulation):** how much network value is lost when a focal person's productive participation is reduced, after allowing realistic substitution and rewiring?
3. **Discrimination-scaled loss (scenario analysis):** what network-level loss is implied when empirically grounded discrimination/participation penalties are applied to eligible nodes? This is a scenario-based policy estimand, not a direct historical causal estimate.

These estimands must never be collapsed into a claim that a psychiatric condition itself produced a person's contribution.

## Frozen conceptual decisions before ARIS

1. The primary counterfactual is **participation removal/reduction**, not "the person never existed."
2. Mental-health status is an exposure/evidence variable, not an explanation for creativity or achievement.
3. Historical examples such as John Nash, Friedrich Nietzsche, or Vincent van Gogh may motivate the question but must not define the sample.
4. Build the candidate sampling frame **before** examining mental-health evidence.
5. `Unknown` mental-health history is not equivalent to `no disorder`.
6. Retrospective psychiatric diagnosis must be evidence-graded and uncertainty-aware; unsupported modern labels cannot enter confirmatory analyses.
7. Direct output loss, downstream cascade loss, and substitution/recovery must be modeled separately.
8. Network adaptation is mandatory. A naïve deletion model may be reported only as an upper-bound stress test.
9. Cross-domain network scores cannot be compared raw. Domain-specific outcomes must be standardized or synthesized hierarchically.
10. Documentation intensity must be modeled because famous people are more likely to have surviving biographies, medical records, correspondence, and later diagnostic speculation.
11. The final confirmatory number of domains and people will be decided after a feasibility pilot, not chosen to maximize a preferred result.
12. No paid LLM API is required. API-gated ARIS reviewer/research stages use GPTPage handoffs with factual claims verified against primary literature or official data documentation.

## Mental-health evidence tiers

The exact coding manual will be frozen before outcome analysis, but the initial structure is:

- **Tier A:** contemporaneous clinical diagnosis, hospitalization, medical record, or comparably strong primary documentation.
- **Tier B:** strong contemporaneous biographical/medical evidence compatible with a clinically meaningful syndrome, but with diagnostic uncertainty.
- **Tier C:** later retrospective diagnostic speculation or weakly sourced secondary claims.
- **Unknown:** insufficient evidence either way.

Primary confirmatory analyses should preferentially use Tier A; Tier A+B may support sensitivity analyses. Tier C must not be silently treated as confirmed diagnosis.

## Candidate knowledge-network layers

The project treats knowledge production as a temporal multiplex network. Candidate layers include:

- person → work (authorship/creation)
- work → work (citation/reference)
- person ↔ person (coauthorship/collaboration)
- mentor → trainee / advisor → student
- person/work → concept/topic
- person/work → later person/work via explicitly documented influence
- movement/school/institution membership where historically meaningful

Each edge type must remain distinguishable; "citation", "coauthor", and "influenced by" are not interchangeable evidence.

## Counterfactual worlds

### W0 — Observed network
The best reconstructed historical network.

### W1 — Naïve removal
Remove or attenuate a focal person's productive contribution without compensation. This is an interpretable upper-bound stress test, not the preferred causal model.

### W2 — Adaptive replacement
Allow temporally eligible substitute nodes, collaborators, competitors, adjacent ideas, and outside entrants to rewire into the affected subnetwork.

### W3 — Discrimination-scaled participation reduction
Apply plausible participation penalties informed by external evidence on stigma/discrimination rather than assuming 100% disappearance.

Monte Carlo simulation should propagate uncertainty in evidence, edge existence, substitution probability, and participation intensity.

## Candidate primary quantity

A generic replacement-adjusted counterfactual contribution can be written as:

`CKC_i = V(G_observed) - E[V(G_counterfactual | participation of i reduced)]`

where `V(G)` is not a single fame score. Candidate components include:

- retained/reachable knowledge output
- field- and time-normalized downstream citation/usage
- diffusion/reachability
- brokerage between communities
- knowledge/topic diversity
- emergence or delay of later concepts/works

Any composite must be preregistered and accompanied by its components.

## Sampling strategy

Do **not** start from a hand-built list of "mentally ill geniuses."

The pilot should first build mental-health-independent candidate frames in three deliberately different data environments:

1. **Science / mathematics** — high-structure bibliometric and collaboration data.
2. **Philosophy / literature / intellectual history** — intermediate structure, requiring curated influence evidence.
3. **Visual arts / music** — difficult cultural-network setting, useful as a portability stress test.

Initial pilot target: roughly **150–300 total candidate people across the three domains**, stratified by time and baseline prominence/impact. Mental-health evidence is coded only after the frame is frozen. The number of exposed focal cases is therefore an outcome of evidence verification, not a quota.

A domain advances to confirmatory analysis only if it clears predefined thresholds for candidate coverage, identity resolution, exposure evidence, network-edge verification, and matched-control quality.

The main-study N will be set using pilot-observed prevalence, missingness, effect variance, matching success, and simulation-based power/precision analysis. No fixed target such as "300 diagnosed famous people" is assumed in advance.

## Time window

The default feasibility window is **1800–2000**, with a stricter **1900–2000** analysis considered where mental-health documentation and network data are substantially more reliable. Earlier figures may be used in qualitative or robustness extensions rather than forced into the same confirmatory model.

## Candidate data sources

- **OpenAlex** for scientific works, authors, topics, institutions, references, and citation relationships.
- **Wikidata** for cross-domain entity resolution and candidate relationship discovery; machine-readable claims are leads, not automatically trusted clinical evidence.
- **Cross-verified notable-people database (Laouenan et al., 2022)** as one possible mental-health-independent historical sampling frame.
- **Crossref** and domain bibliographies as supplementary publication metadata.
- **Curated biographies, archival/medical sources, scholarly histories, and authority records** for mental-health evidence and non-bibliometric influence edges.
- **Semantic Scholar** only if its current API/data license is compatible with the intended public outputs; OpenAlex is preferred where redistribution simplicity matters.

Raw copyrighted biographies or restricted API data should not be redistributed. Store derived codes, provenance, identifiers, and reproducible acquisition instructions instead.

## Closest methodological anchors identified so far

- Azoulay, Fons-Rosen & Graff Zivin (2019), *American Economic Review*, "Does Science Advance One Funeral at a Time?" (DOI `10.1257/aer.20161574`) demonstrates that removing eminent scientists can produce both collaborator losses and adaptive entry by outsiders, directly motivating a substitution-aware counterfactual rather than naïve deletion.
- Acar, Chen & Cayirdag (2018), *Schizophrenia Research*, "Schizophrenia and creativity: A meta-analytic review" (DOI `10.1016/j.schres.2017.08.036`) cautions against treating severe mental disorder as a simple positive cause of creativity.
- Muramoto (2014), *Philosophy, Ethics, and Humanities in Medicine*, "Retrospective diagnosis of a famous historical figure" (DOI `10.1186/1747-5341-9-10`) motivates uncertainty-aware and historically contextualized retrospective evidence.
- Karenberg (2009), "Retrospective diagnosis: use and abuse in medical historiography" (PMID `19591388`) highlights the risk of speculative modern labels and changing nosology.
- Recent systematic reviews of mental-health stigma report adverse employment/social-inclusion consequences while also noting that causal evidence for some stigma pathways remains limited; therefore the discrimination-to-participation link must be separately evidenced rather than assumed.

## Major threats to validity

- fame/documentation bias
- survivorship and collider bias from conditioning on historical prominence
- retrospective-diagnosis error
- differential archival survival across countries, genders, classes, and eras
- domain-dependent meaning of an "influence" edge
- bibliometric coverage bias
- multiple plausible substitute histories
- conflating disease burden with discrimination burden
- over-crediting a predecessor for downstream work that had multiple independent precursors
- interpreting simulated counterfactuals as observed historical facts

## Falsification / downgrade logic

The preferred broad claim weakens substantially if:

- apparent effects disappear after matching on baseline network position and documentation intensity;
- only naïve deletion shows large loss while adaptive replacement nearly eliminates it;
- results are driven by a small number of preselected celebrity cases;
- exposure coding is too uncertain for most of the sampling frame;
- cultural domains cannot support reproducible influence edges;
- the same network losses occur for arbitrary matched subsets of people, implying no mental-health-specific exclusion relevance;
- the discrimination-scaled results require implausibly large participation penalties;
- conclusions change qualitatively under reasonable alternative edge definitions or substitution models.

## Current ARIS gate

ARIS should now execute, in order:

1. closest-prior-work / novelty review;
2. estimand and causal-claim audit;
3. sampling-frame and documentation-bias audit;
4. mental-health evidence coding protocol;
5. three-domain data-feasibility pilot design;
6. substitution/rewiring model design;
7. simulation-based sample-size/precision plan;
8. data licensing and reproducibility plan;
9. preregistration-style confirmatory/exploratory split;
10. red-team review before any large-scale outcome analysis.
