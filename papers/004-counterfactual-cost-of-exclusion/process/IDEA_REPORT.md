# IDEA REPORT — ARIS4C004

## Project

**The Counterfactual Cost of Exclusion: Mental Health and Keystone Individuals in Human Knowledge Networks**

Date: 2026-09-18  
ARIS: v0.4.26 (`951654847b015585385b2448c5667dcd04e7b56b`)

## Executive judgement

**GO to feasibility, not yet GO to confirmatory data collection.**

The motivating observation — that some highly influential historical figures had serious mental-health problems — is not novel and is vulnerable to the long-running "mad genius" stereotype. The defensible research contribution is different:

> quantify the **replacement-adjusted network opportunity cost of exclusion or reduced participation**, while treating mental-health evidence, network contribution, discrimination, and historical substitution as separate constructs.

A preliminary search found substantial neighboring literatures but no exact predecessor combining:

1. a mental-health-independent sampling frame;
2. evidence-graded historical mental-health status;
3. temporal multiplex knowledge networks;
4. participation-removal counterfactuals;
5. adaptive substitution/rewiring;
6. discrimination-scaled scenario analysis.

This novelty judgement is provisional and must survive a dedicated closest-prior-work search.

---

## 1. Original intuition and why it needed reframing

The seed idea was that people such as John Nash, Friedrich Nietzsche, Vincent van Gogh, and other major historical figures are often discussed in connection with serious mental-health problems; if society had excluded such people completely, their disappearance might have damaged not just their own output but downstream fields and later people inspired by them.

Three problems arise if this is left in its intuitive form:

- **selection on memorable examples:** choosing famous diagnosed people first nearly guarantees a compelling story;
- **causal slippage:** observing psychopathology and achievement does not show that psychopathology caused achievement;
- **naïve historical deletion:** assuming all downstream work disappears ignores independent discovery, competitors, collaborators, and field adaptation.

The project therefore shifts from a claim about "mad genius" to a counterfactual opportunity-cost problem.

---

## 2. Canonical question

> If people with well-documented mental-health conditions are prevented from participating fully in scientific, intellectual, or cultural production, how much direct and downstream knowledge-network value can be lost after allowing the system to adapt, substitute, and rewire?

The word **prevented** is essential. The policy-relevant object is participation/exclusion, not whether a person exists and not whether a disorder makes someone creative.

---

## 3. Estimands

### E1 — Structural-position contrast

Descriptive quantity:

`E[network importance | MH evidence] - E[network importance | matched comparison]`

Purpose: test whether documented-MH nodes occupy unusual positions after matching/adjustment.

This estimand is strongly vulnerable to documentation and survivor selection and must be interpreted descriptively.

### E2 — Replacement-adjusted participation loss

For focal node `i` and participation attenuation `a`:

`CKC_i(a) = V(G_observed) - E[V(G_counterfactual(i, a, adaptive rewiring))]`

where `a` may represent 25%, 50%, 75%, or 100% loss of productive participation.

This is the central computational estimand.

### E3 — Discrimination-scaled network loss

Apply externally supported distributions of participation penalties associated with discrimination/stigma to eligible nodes and propagate them through the network.

This is a **scenario estimand** unless a historically credible causal discrimination mechanism can be directly identified.

---

## 4. Neighboring literatures and overlap

### 4.1 Creativity / psychopathology historiometry

This literature already demonstrates why the project must not sell itself as "many geniuses were mentally ill."

- Ludwig (1992), *Creative achievement and psychopathology: comparison among professions*, examined **1,005** biographical subjects across 18 professions (DOI `10.1176/appi.psychotherapy.1992.46.3.330`).
- Post (1994), *Creativity and psychopathology. A study of 291 world-famous men*, studied **291** famous men across science, thought, politics, and art (DOI `10.1192/bjp.165.1.22`).
- Andreasen & Canter (1974) compared creative writers with controls (DOI `10.1016/0010-440X(74)90028-5`).
- Acar, Chen & Cayirdag (2018) meta-analyzed schizophrenia and creativity and reported an overall negative association that varied with severity and measurement (DOI `10.1016/j.schres.2017.08.036`).
- Baas et al. (2016) reviewed the "mad genius" controversy and emphasized heterogeneous psychopathology-creativity relationships (DOI `10.1037/bul0000049`).

**Overlap:** mental health + achievement.  
**Gap for 004:** these studies do not estimate counterfactual downstream network loss under exclusion with adaptive substitution.

### 4.2 Star loss / knowledge spillovers

This is the strongest methodological anchor.

- Azoulay, Graff Zivin & Wang (2010), *Superstar Extinction*, used 112 premature deaths of academic superstars and found persistent quality-adjusted publication declines among collaborators (QJE; working-paper DOI `10.3386/w14577`).
- Azoulay, Fons-Rosen & Graff Zivin (2019), *Does Science Advance One Funeral at a Time?*, studied subfields associated with **452** prematurely deceased life-science stars. Collaborator output fell, while non-collaborator entry increased, demonstrating both loss and adaptive replacement (DOI `10.1257/aer.20161574`).
- Mohnen (2022), *Stars and Brokers: Knowledge Spillovers Among Medical Scientists*, showed that the network brokerage position of deceased stars predicts heterogeneous coauthor productivity losses (DOI `10.1287/mnsc.2021.4032`).
- Khanna (2021), *Aftermath of a tragedy*, found coauthor-network structure moderated productivity effects after star death (DOI `10.1016/j.respol.2020.104159`).
- Work on evolving scientific collaboration networks has found substantial robustness after removal of eminent hub scientists, supporting latent-network/rewiring mechanisms rather than stationary-network deletion assumptions.

**Overlap:** counterfactual-like node loss + downstream knowledge effects + adaptation.  
**Gap for 004:** not focused on mental-health-related participation/exclusion, evidence uncertainty, or cross-domain cultural networks.

### 4.3 Network robustness / cooperative-game centrality

Targeted node removal, robustness envelopes, and game-theoretic centrality provide mathematical tools for measuring node contribution without assigning all downstream output to a single predecessor. Shapley-value approaches can estimate average marginal contribution across coalitions, but they are computational tools rather than a causal solution by themselves.

Candidate anchor: Gómez et al. (2003), *Centrality and power in social networks: a game theoretic approach*, DOI `10.1016/S0165-4896(03)00028-3`.

### 4.4 Mental-health stigma / participation

Systematic reviews show that mental-health stigma and discrimination are associated with barriers to employment, income, disclosure, social inclusion, and workplace opportunity. A 2025 scoping review synthesized 448 studies and emphasized that adverse outcomes are widespread while direct causal evidence for some stigma → outcome pathways remains limited. Therefore ARIS4C004 must not mechanically translate stigma prevalence into a historical participation effect.

Relevant anchors include:

- Brohan et al. (2012), workplace disclosure systematic review (BMC Psychiatry 12:11).
- van Beukering et al. (2022), systematic review of health-related stigma, sustainable employment and well-being (DOI `10.1007/s10926-021-09998-z`).
- Sharac et al. (2010), systematic review of economic impact of mental-health stigma/discrimination (DOI `10.1017/S1121189X00001159`).

### 4.5 Retrospective diagnosis / historical epistemology

- Karenberg (2009), *Retrospective diagnosis: use and abuse in medical historiography* (PMID `19591388`).
- Muramoto (2014), *Retrospective diagnosis of a famous historical figure: ontological, epistemic, and ethical considerations* (DOI `10.1186/1747-5341-9-10`).

These works justify evidence grading, historical contextualization, and explicit uncertainty rather than binary modern diagnosis labels.

---

## 5. Provisional novelty claim

A defensible novelty statement is:

> Prior work has separately studied psychopathology among eminent creators, the consequences of losing star scientists, network robustness to node removal, and employment/social costs of mental-health stigma. ARIS4C004 connects these literatures by estimating the **replacement-adjusted network-level opportunity cost of reduced participation among people with evidence-supported mental-health histories**, with explicit uncertainty in diagnosis/evidence and substitution.

Do **not** claim novelty merely because no identical title appears in search results. A dedicated novelty packet must search scientometrics, innovation economics, historiometry, cultural analytics, disability studies, and mental-health stigma literatures.

---

## 6. Sampling logic

### Forbidden design

Hand-curate Nash + Nietzsche + van Gogh + other famous diagnosed people, then calculate that they were important.

### Preferred design

1. Define a mental-health-independent candidate sampling frame.
2. Freeze inclusion/time/domain rules.
3. Resolve identities.
4. Independently code mental-health evidence and documentation intensity.
5. Build domain networks and baseline impact variables.
6. Match/weight comparison nodes without labeling missing mental-health information as healthy.
7. Run counterfactual simulations.

### Pilot domains

- **Science / mathematics:** high feasibility; citation, coauthor, topic and institution layers.
- **Philosophy / literature / intellectual history:** intermediate feasibility; explicit influence and bibliographic evidence needed.
- **Visual arts / music:** low-structure but theoretically important portability test.

Pilot target: **150–300 total candidates**, not 150–300 confirmed diagnoses.

This intentionally corrects a dangerous quota-based formulation. The number of Tier-A/Tier-B exposed cases is measured after the frame is frozen.

---

## 7. Candidate sampling frames

### Cross-domain frame

Laouenan et al. (2022), *A cross-verified database of notable people, 3500BC–2018AD* (Scientific Data, DOI `10.1038/s41597-022-01369-4`) provides a large cross-verified notable-person universe built from Wikipedia/Wikidata. It is a useful candidate generator but still inherits notability/coverage biases and cannot be treated as a population census.

### Science frame

OpenAlex provides author/work/reference/topic/institution metadata with stable identifiers and large-scale open access to the scholarly graph. A science-specific pilot can draw from predeclared field/time/impact strata rather than only globally famous scientists.

### Humanities/arts frame

Use the cross-verified notable-person dataset plus domain-specific authority sources/curated catalogues. Wikidata can support entity resolution and candidate relationship discovery, but unverified `medical condition` or `influenced by` claims cannot by themselves define confirmatory exposure or causal influence.

---

## 8. Exposure coding principles

Mental-health history must be represented as **evidence**, not timeless diagnostic truth.

Required fields per candidate:

- person ID(s)
- evidence tier A/B/C/Unknown
- historical source date
- source type (clinical record, hospitalization, contemporaneous physician, correspondence, biography, later diagnostic paper, etc.)
- syndrome/condition wording exactly as supported
- modern mapping, if used, separated from historical wording
- confidence/uncertainty notes
- evidence provenance
- coder
- blinded-to-network-outcome flag where feasible
- documentation-intensity metrics

A candidate with no surviving record remains `Unknown`; do not use `no evidence` as a clean negative control.

---

## 9. Network model

Use a temporal multiplex graph rather than one undifferentiated network.

Possible layers:

- authorship/creation
- coauthorship/collaboration
- citation/reference
- mentorship/advising
- topic/concept participation
- explicit intellectual/artistic influence
- institution/movement/school membership

Edges carry:

- type
- direction
- start/end time
- provenance
- confidence/evidence class

Counterfactual rewiring may use:

- temporal eligibility
- domain/topic similarity
- collaborator proximity
- institutional/geographic opportunity
- independent-predecessor availability
- observed historical entry rates after analogous node loss

---

## 10. Outcome families

Avoid a single opaque "greatness" score.

### Direct production
- works / publications / creations
- field-normalized impact or reception where defensible

### Downstream propagation
- later citations/references
- descendants in mentorship or collaboration networks
- topic/concept diffusion

### Structural role
- brokerage
- community bridging
- reachability
- redundancy / alternative path availability

### Adaptive recovery
- time to replacement
- fraction of downstream value recovered
- entry of outside nodes
- diversity of replacement knowledge

### Cultural domains
Domain-specific measures must be justified separately and standardized before synthesis.

---

## 11. Hypotheses and non-hypotheses

### Not a hypothesis

`Mental illness causes creativity/genius.`

This is explicitly outside the confirmatory claim set.

### Candidate H1 — nonzero exclusion cost

After adaptive replacement, reducing participation of evidence-supported focal nodes produces nonzero downstream network loss on average.

### Candidate H2 — heterogeneity by network position

Replacement-adjusted loss is larger for low-redundancy brokers/bridges than for equally productive but structurally redundant nodes.

### Candidate H3 — adaptation matters

Naïve node deletion materially overstates loss relative to adaptive substitution models.

### Candidate H4 — discrimination-scaled cost

Under externally plausible participation-penalty distributions, expected network loss remains nontrivial relative to matched random-subset interventions.

### Exploratory H5 — domain heterogeneity

The balance of direct loss, cascade loss, and adaptive recovery differs across scientific, intellectual, and artistic network types.

---

## 12. Strong nulls / falsification

The study must include null interventions strong enough to defeat a story-driven result.

1. **Matched random-node null:** remove/attenuate equally prominent nodes with comparable baseline network position and documentation intensity.
2. **Label permutation null:** permute mental-health evidence labels within tight strata when logically valid.
3. **Equal-size arbitrary-subset null:** compare aggregate losses to random subsets of identical size.
4. **Rewiring-strength sensitivity:** allow weak, moderate, and strong substitution.
5. **Edge-confidence restriction:** rerun on high-confidence edges only.
6. **Tier restriction:** Tier A only versus A+B.
7. **Celebrity exclusion:** leave out the most famous named cases.
8. **Domain leave-one-out:** test whether any broad conclusion is one-domain driven.
9. **Documentation matching:** test whether apparent structural importance disappears when archive/biography richness is balanced.

---

## 13. Main threats

### Selection / collider bias

Conditioning on fame or availability of biographies can induce an association between mental-health documentation and achievement even if none exists in the underlying population.

Mitigation: prospective sampling frame, impact-stratified sampling, explicit documentation model, and no causal interpretation of E1.

### Differential survival of records

Archival richness differs by era, language, country, gender, class, profession, institutional affiliation, and fame.

Mitigation: measure documentation intensity; restrict time windows; use sensitivity bounds.

### Exposure misclassification

Retrospective labels are uncertain and historically unstable.

Mitigation: evidence tiers and probabilistic/sensitivity representation.

### Influence-edge subjectivity

An art-historical "influence" is not equivalent to a scientific citation.

Mitigation: preserve edge types; domain-specific validation; no raw pooled centrality.

### Historical counterfactual underdetermination

Many alternative histories are possible.

Mitigation: estimate distributions under transparent families of substitution rules instead of claiming one true alternative history.

---

## 14. Feasibility decision rule

A domain proceeds to confirmatory analysis only if a preregistered pilot clears thresholds for:

- candidate-frame coverage;
- entity-resolution success;
- sufficient Tier-A/Tier-B evidence yield;
- adequate high-confidence network edges;
- matched-comparison availability;
- tolerable documentation imbalance;
- computationally stable counterfactual simulation.

If only science clears the gate, the project should **shrink to a science-of-science primary paper** and retain philosophy/art as qualitative or exploratory extensions rather than forcing a cross-domain claim.

---

## 15. Current conclusion

**Conceptual novelty: promising.**  
**Data feasibility: plausible for science, uncertain for philosophy/literature, high-risk for arts.**  
**Causal identification of historical discrimination: weak unless separately anchored; use scenario language.**  
**Best next action: continue ARIS feasibility, build data/licensing matrix, formalize evidence coding and adaptive counterfactual model before collecting outcome data.**
