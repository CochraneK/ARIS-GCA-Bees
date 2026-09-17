# AUTO REVIEW — ARIS4C004

## Review stage

Pre-data adversarial review. Written before confirmatory outcome construction or large-scale exposure coding.

## Overall assessment

**Promising and potentially distinctive, but only if the paper is framed as a bounded counterfactual/network study rather than proof of the "mad genius" idea.**

The publishable contribution is strongest when it estimates what happens to a knowledge network under participation attenuation of evidence-supported historical contributors, explicitly allowing adaptation and uncertainty.

The project should continue, but several design issues are blocking before confirmatory analysis.

---

## Major concern 1 — survivorship makes invisible the people exclusion erased completely

The proposed data sources contain people who became visible enough to enter publications, biographies, archives, or cultural databases. The most severe form of exclusion creates the opposite outcome: a person never gets the training, job, platform, publication, patronage, or institutional access needed to leave a measurable contribution.

### Why this matters

ARIS4C004 cannot recover the true works/ideas of people who were historically excluded before producing observable traces. A simulation based on Nash, van Gogh, Nietzsche, or other realized contributors therefore cannot estimate the full social cost of mental-health discrimination.

### Required fix

Define the primary estimand as one of:

- **realized-contributor counterfactual effect**, or
- **lower-bound / observed-node opportunity cost**.

Any attempt to infer contributions of completely unseen people must be a separate latent-node model with very strong assumptions and should remain exploratory.

**Gate: GO after claim narrowing.**

---

## Major concern 2 — conditioning on fame/notability can create collider bias

Historical notability is affected by contribution, archival survival, institutional privilege, language, geography, gender, class, and potentially the very traits under study. Mental-health documentation is also strongly related to fame and archive richness.

### Why this matters

Within a famous-person sample, an observed association between mental-health evidence and network importance cannot be generalized to all people and may be induced by selection.

### Required fix

- build sampling frames independently of mental-health status;
- sample across impact strata where possible rather than only "geniuses";
- measure documentation intensity;
- treat E1 structural-position comparisons as descriptive;
- do not use E1 to argue that mental illness causes eminence.

**Gate: GO with descriptive-only interpretation of E1.**

---

## Major concern 3 — "no documented disorder" is not a healthy control

Historical medical records are incomplete and selective. A comparison person's biography may simply omit symptoms or treatment.

### Required fix

Use at least four states:

- Tier A evidence;
- Tier B evidence;
- weak/speculative Tier C;
- Unknown.

For comparison analyses, distinguish high-documentation unknown/negative-evidence cases from low-documentation unknowns. Use sensitivity analysis for exposure misclassification rather than a naive disorder/no-disorder binary.

**Gate: BLOCKING until coding manual is frozen.**

---

## Major concern 4 — the model currently presupposes "loss," but node removal can generate gains

Empirical star-death studies show collaborator losses but also increased entry by outsiders and new highly cited work in affected fields. A focal person's presence can simultaneously enable knowledge and inhibit entry or alternative directions.

### Required fix

The core mathematical quantity should be sign-neutral. Prefer:

`CPE_i(a) = V(G_observed) - E[V(G_counterfactual(i,a))]`

where **CPE = Counterfactual Participation Effect**.

- positive CPE: observed participation increases the chosen value metric;
- zero CPE: replacement is complete;
- negative CPE: counterfactual adaptation improves that metric.

The phrase "cost of exclusion" is an interpretation only when the relevant CPE is positive.

**Gate: BLOCKING terminology/model fix.**

---

## Major concern 5 — participation removal is time-dependent

Removing a person after their influential work already exists is not equivalent to preventing early-career participation. Past works do not vanish just because later participation stops.

### Required fix

Make interventions temporal:

- early-entry attenuation;
- career-wide attenuation from a defined start;
- episode-aligned exclusion where historical evidence exists;
- late-career attenuation.

At time `t`, only future outputs and future edges are directly intervened upon. Existing works remain available unless a separate censorship/destruction scenario is explicitly modeled.

**Gate: BLOCKING before simulator implementation.**

---

## Major concern 6 — disorder burden, treatment, stigma, and institutional discrimination are different mechanisms

A mental-health condition can affect participation through symptoms; treatment may help or harm participation; discrimination may operate through hiring, dismissal, disclosure penalties, social isolation, or institutionalization; historical legal regimes may create direct exclusion.

### Required fix

Do not use observed productivity differences as a proxy for discrimination.

Separate:

1. `condition burden`;
2. `treatment/access`;
3. `stigma/discrimination`;
4. `formal institutional exclusion`;
5. `counterfactual participation attenuation`.

The policy-facing discrimination scenario must be calibrated from external discrimination evidence or historically documented exclusion events.

**Gate: GO only with mechanism separation.**

---

## Major concern 7 — retrospective psychiatric diagnosis is an unstable exposure

Modern nosology cannot be projected backward without uncertainty. Biographies are not standardized clinical assessments and diagnostic speculation is especially common for famous creators.

### Required fix

- primary analyses: Tier A, or narrowly justified A+B;
- retain historical wording/syndromic evidence rather than forcing precise DSM labels;
- record source dates and source type;
- two-coder adjudication for ambiguous cases where feasible;
- blinded exposure coding to network-loss outcomes where feasible;
- sensitivity analyses dropping all retrospective-only diagnoses.

**Gate: BLOCKING until exposure manual exists.**

---

## Major concern 8 — privacy/ethics for living people

Mental-health information is sensitive, even when some material is public. The project does not need living people to answer its historical counterfactual question.

### Required fix

**Default primary sample: deceased persons only.**

If living persons are ever included, require a separate ethics/data-governance review and restrict exposure evidence to appropriately public/self-disclosed or ethically usable material. Do not infer psychiatric diagnoses of living people from behavior or creative works.

**Gate: GO after deceased-only rule is frozen for primary analysis.**

---

## Major concern 9 — simple rewiring may not represent independent discovery

Knowledge substitution can occur without replacing a social edge. A theorem, technique, style, or concept may be rediscovered by a competitor with a delay; several independent precursor paths may exist.

### Required fix

Use at least two counterfactual families:

1. **network rewiring model:** replace collaborations/knowledge paths using temporally eligible neighbors and outsiders;
2. **alternative-precursor / delay model:** where evidence permits, model whether downstream concepts have independent precursor paths and estimate delays rather than total disappearance.

Do not claim one simulated graph is "the" alternative history.

**Gate: GO; second family may be exploratory if data are insufficient.**

---

## Major concern 10 — downstream attribution can double count contribution

If later work `C` cites/inherits from A, B, and D, deleting A and assigning all of C to A exaggerates A's contribution.

### Required fix

Possible approaches:

- path redundancy / alternative-path analysis;
- marginal-contribution simulation;
- cooperative-game/Shapley approximation on bounded local subgraphs;
- proportional or probabilistic attribution with preregistered rules.

Shapley value is a potential attribution tool, not mandatory for the entire network and not a substitute for causal identification.

**Gate: GO with anti-double-counting rule required.**

---

## Major concern 11 — cross-domain pooling can become meaningless

A citation in physics, a philosophical lineage, and artistic influence are different relations with different measurement error.

### Required fix

- analyze domains separately;
- preserve edge types;
- define domain-specific value functions;
- standardize only after domain-specific validation;
- synthesize effects hierarchically/meta-analytically only if constructs are sufficiently aligned.

If humanities/arts fail feasibility, publish science as the primary quantitative paper rather than force a universal score.

**Gate: GO with domain separation.**

---

## Major concern 12 — network value function can hide arbitrary researcher choices

`V(G)` could include citations, output, reachability, brokerage, topic diversity, prestige, and many other quantities. A flexible weighted composite would create a specification garden.

### Required fix

Use a small primary outcome set. Recommended minimal science-domain core:

1. future field-normalized output attributable to the affected local knowledge area;
2. future high-impact output / citation-weighted production;
3. outsider entry / diversity;
4. collaborator productivity;
5. recovery time / fraction recovered.

Structural metrics are mechanisms/secondary outcomes unless justified as welfare-relevant network value.

If a composite CPE is retained, publish every component and freeze weights before confirmatory simulation.

**Gate: BLOCKING before preregistration.**

---

## Major concern 13 — mental-health-specific relevance can vanish if any key node produces the same loss

If removing any prominent broker produces the same distribution of counterfactual effects, the study may reduce to a generic paper about star nodes with a mental-health label added afterward.

### Required fix

Use strong benchmarks:

- matched nodes with comparable era/domain/baseline impact;
- matched nodes with comparable network position;
- arbitrary equal-size subsets;
- label permutations under valid strata;
- documentation-intensity matched subsets.

The policy interpretation should then be:

> if a stigmatized group faces elevated exclusion risk, the cost depends on the distribution of network roles among people subjected to that risk.

It does not require claiming that the group is inherently more central.

**Gate: GO with matched/random benchmarks mandatory.**

---

## Major concern 14 — discrimination parameters may not transport historically

Modern workplace stigma estimates cannot simply be applied to nineteenth-century artists or early-twentieth-century mathematicians. Legal institutions, treatment systems, occupations, and disclosure norms differ.

### Required fix

Create parameter families:

- contemporaneous/historical documented exclusion where available;
- modern empirical discrimination bounds used only as policy scenarios;
- purely hypothetical 25/50/75/100% attenuation stress tests.

Clearly label which are historical reconstructions versus modern-policy scenarios.

**Gate: GO with transportability caveat.**

---

## Major concern 15 — the paper can drift into stigmatizing language

Framing influential people as "mentally ill geniuses" can romanticize severe illness, erase disability burden, and reinforce stereotypes.

### Required fix

Use person-first or context-appropriate neutral terminology, avoid sensational case lists, and explicitly state:

- mental-health conditions are neither necessary nor sufficient for creativity;
- the study concerns inclusion/exclusion and network consequences;
- disability burden and social discrimination can coexist;
- historical labels are uncertain.

**Gate: GO with language review.**

---

# Recommended minimal first paper

The full cross-cultural-history idea is ambitious. The most defensible first quantitative paper is likely **science-first**, with humanities/arts retained as predeclared portability pilots.

## Primary population

Deceased scientific/mathematical knowledge producers in a preregistered twentieth-century window, sampled independently of mental-health status and with adequate OpenAlex/auxiliary coverage.

## Primary exposure

Tier-A documented mental-health condition/history; Tier A+B sensitivity.

## Primary intervention

Early-career or career-wide future participation attenuation at several intensities, preserving contributions already produced before intervention time.

## Primary counterfactual

Adaptive model with collaborator and outsider replacement, calibrated/plausibility-bounded using star-loss literature and observed network redundancy.

## Primary outcomes

- future production/impact in affected local topic/subfield;
- collaborator production;
- outsider entry/diversity;
- recovery fraction/time.

## Primary benchmark

Matched non-exposed/unknown-high-documentation or arbitrary nodes with comparable pre-intervention domain, era, output, and network position; report both importance-matched and less-conditioned benchmarks because matching on network position changes the question.

## Cross-domain extension

Proceed only after explicit data/edge gates are cleared.

---

# Current gate summary

| Component | Gate |
|---|---|
| Core research question | **GO** |
| Novelty | **PROVISIONAL GO — dedicated search still required** |
| Science data | **GO** |
| Humanities data | **CONDITIONAL** |
| Arts data | **HIGH RISK** |
| Exposure coding | **BLOCKING until manual frozen** |
| Counterfactual timing | **BLOCKING until frozen** |
| Sign-neutral outcome / CPE terminology | **BLOCKING fix required** |
| Network value outcomes | **BLOCKING until bounded** |
| Living-person ethics | **RESOLVED by deceased-only primary rule** |
| Adaptive replacement | **MANDATORY** |
| Full historical social cost claim | **NOT IDENTIFIED — must remain out of scope** |

## Reviewer verdict

**Continue ARIS.** The study remains interesting after adversarial review, but its strongest form is narrower and more credible than the original intuition. The next deliverables should formalize the sign-neutral CPE estimand, deceased-only exposure protocol, temporal intervention, and science-first pilot before large-scale coding.
