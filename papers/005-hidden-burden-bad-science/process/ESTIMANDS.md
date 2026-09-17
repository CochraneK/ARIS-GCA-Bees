# ESTIMANDS — ARIS4C005

## Design principle

ARIS4C005 does not have one estimand called “the amount of bad science.” It has a linked set of estimands with different units, observation processes, and levels of causal ambition.

All confirmatory estimands must state:

- exposure layer (`E1`, `E2`, `E3`);
- publication universe / target population;
- calendar period;
- unit of analysis;
- observed vs latent/modelled status;
- uncertainty interval;
- data release/version;
- causal vs descriptive interpretation.

Primary historical analysis window: **2000–2025**. Calendar year 2026 is incomplete and is not used for annual trend comparisons.

---

# 1. Publication-universe estimands

## U1 — annual global journal-output count

`N_articles(t)` = count of resolvable journal articles + reviews in calendar year `t`.

Primary source family: OpenAlex with Crossref DOI reconciliation.

Sensitivity universes:

- journal articles only;
- journal articles + reviews;
- journal + conference proceedings;
- Crossref journal DOI universe;
- OpenAlex core works (descriptive only, because work types are broader than papers).

## U2 — cumulative target universe

`N_articles(2000:2025)` under each frozen denominator definition.

No count from one metadata ecosystem is silently substituted for another.

---

# 2. Detected-integrity estimands

## D1 — detected severe-integrity count

`N_E1_detected(t)` = unique target-universe works with an E1 event attributable to a publication year / correction cohort under the project codebook.

Report both:

- publication-year cohorts;
- correction/retraction-year cohorts.

These answer different questions.

## D2 — detected rate

`r_E1_detected(t) = N_E1_detected(t) / N_articles(t)`

Interpretation: **detection/correction rate, not prevalence**.

## D3 — correction latency

`L_i = correction_date_i - publication_date_i`

Report median, IQR, survival curves, and right-censor-aware analyses.

---

# 3. Latent article-level prevalence estimands

## P1 — severe-integrity prevalence

Primary latent target:

`pi_severe(f,t) = P(Z_i = severe integrity failure | field=f, period=t, target universe)`

Initial confirmatory latent model is intentionally binary:

- `Z=1`: article contains a severe integrity failure sufficient to make a material scientific claim unreliable;
- `Z=0`: no such failure established in the audit/model.

The richer multi-state ontology is used descriptively and in sensitivity analyses because a 5-state latent model may be weakly identified.

### Evidence streams

Possible detectors `D_j`:

- formal retraction/editorial notice reason;
- independent high-confidence image anomaly;
- impossible/statistically inconsistent reporting;
- validated duplicated data/text beyond legitimate reuse;
- high-specificity paper-mill/tortured-phrase signal;
- post-publication integrity flag adjudicated by the manual audit.

### Model

For detector `j`:

`D_ij ~ Bernoulli(theta_{j,Z_i})`

with hierarchical priors for detector sensitivity/specificity informed by manual adjudication and external validation. Prevalence varies by field and publication period using partial pooling.

### Hard boundary

Researcher self-report prevalence (for example FFP self-admission) can inform contextual priors/sensitivity analysis but is **never treated as paper prevalence**.

## P2 — undetected severe-integrity burden

`N_undetected = sum_i P(Z_i=1 | D_i, X_i) - N_E1_detected`

Report posterior interval and detector/model sensitivity.

## P3 — multi-list capture-recapture sensitivity

Estimate hidden-case count from partially overlapping high-specificity detection lists with log-linear interaction terms.

Use only as a sensitivity model because list independence is implausible and capture probability is heterogeneous.

---

# 4. Human-time and production-cost estimands

## H1 — Researcher-Life-Years, direct production

`RLY_production = sum_i P(severe_i) * E(FTE_years_i attributable to invalidated component)`

Effort is sampled from study-type/field-specific distributions; a paper is never assumed to equal one researcher-year.

## H2 — downstream follow-up RLY

`RLY_followup = sum_k P(material_dependency_k) * attributable_followup_effort_k`

Only downstream work materially dependent on the unreliable result is included.

## H3 — correction RLY

Investigation, reanalysis, correction, retraction, evidence-review update, and avoidable replication effort attributable to E1/E2 events.

## H4 — Integrity Maintenance Debt

`IMD_hours` = incremental reviewer + editor + integrity-investigation + evidence-correction hours attributable to problematic submissions/outputs.

Ordinary peer review is not counted as waste.

---

# 5. Financial estimands

## F1 — attributable direct research cost

For linked grants/projects:

`Cost_direct = sum_g Award_g * allocation_weight(g -> problematic output)`

Allocation strategies are predeclared:

- publication-fraction allocation;
- project-period effort allocation where available;
- conservative lower bound using only explicitly attributable sub-awards/costs.

Whole-grant totals are reported as exposure/context, not automatically as waste.

## F2 — correction-system cost

Costs of formal investigations, journal corrections, reanalysis, replication, and evidence updates where directly measurable.

## F3 — opportunity-cost funding displacement

Counterfactual funding reallocation estimated only in designs with plausible matched/control trajectories. Never computed as “global R&D × misconduct rate.”

---

# 6. Participant estimands — clinical subset

## PT1 — participants without usable knowledge gain

Count of enrolled participants whose study contribution fails to enter usable public evidence because of:

- E1/E2 invalidation; or
- E3 nonpublication/discontinuation.

Report E1/E2 and E3 separately.

## PT2 — participant-hours

`sum participation burden time` where protocols/trial registries permit.

## PT3 — participant-risk burden

Use observed adverse events or protocol risk categories only when comparable. Avoid speculative DALY conversion in the primary analysis.

---

# 7. Scientific contamination estimands

## C1 — direct material-dependence footprint

`SCF_1` = number of unique downstream works whose claims/methods/evidence synthesis materially depend on an E1/E2 source.

Citation-context classifier labels:

- background mention;
- critique / retraction discussion;
- method reuse;
- data/result dependence;
- evidence-synthesis inclusion.

Primary contamination = data/result dependence + evidence-synthesis inclusion.

## C2 — higher-order footprint

`SCF_h` = unique materially dependent nodes at graph distance `h`, with path confidence retained.

## C3 — evidence-synthesis contamination

Counts of systematic reviews/meta-analyses containing problematic evidence, plus leave-problematic-evidence-out changes in pooled estimates.

## C4 — guideline/policy contamination

Guidelines/policy documents that rely on contaminated synthesis or directly on problematic studies. Language and database coverage restrictions are explicit.

---

# 8. Dynamic propagation estimands

## R1 — Epistemic Reproduction Number

Within time bin `t`:

`R_E(t) = new materially dependent nodes generated / active materially contaminated parent nodes`

Estimate by exposure cohort and correction status. This is an operational network statistic, not a biological parameter.

## R2 — Knowledge Ghost Half-Life

`KGH` = post-correction time at which new materially dependent use falls to 50% of the pre-correction reference/counterfactual rate.

Estimate using interrupted time-series / event-study survival or hazard models, stratified by citation type.

---

# 9. Innovation / opportunity estimands

## I1 — Innovation Delay Years

For a legitimate alternative/topic outcome `Y`:

`IDY = T_observed(Y) - T_counterfactual_no-integrity-shock(Y)`

Candidate outcomes:

- first validated alternative result;
- crossing a field-normalized uptake threshold;
- first major grant influx;
- first guideline adoption;
- first successful replication/translation.

Identification: matched topic clusters + event studies / synthetic controls with pre-trend diagnostics.

## I2 — crowding-out

Differences in publication entry, funding share, citation attention, or researcher entry for matched neighboring topics after an integrity shock.

Do not define crowding-out as one fake paper mechanically replacing one good paper.

## I3 — Scientific Detour Years

Cumulative excess time/resources in a trajectory later shown to rest materially on severe integrity failure relative to counterfactual trajectory.

Secondary because counterfactual definition is stronger.

---

# 10. Career spillover estimands

## CC1 — innocent-collaborator citation effect

Event-study / matched-control change in citations for prior collaborators not implicated in the misconduct.

## CC2 — funding/collaboration effect

Change in funding probability/amount and collaboration formation, conditional on available identifiers and pre-trends.

The perpetrator's sanction is not classified as social loss by default.

---

# 11. Sleeping Beauty estimands — exploratory

## SB1 — observed delayed-recognition model

Train on historical Sleeping Beauty/Prince pairs to estimate:

`P(awakening within h years | pre-awakening features)`.

## SB2 — Never-Woken Sleeping Beauties

`N_NWSB = sum_i [P_i(awakening | low-contamination counterfactual) - P_i(awakening | observed)]`

This is an **expected counterfactual count**, not identification of named “lost masterpieces.”

## SB3 — awakening delay

For papers that eventually awaken, estimate whether local integrity shocks are associated with longer sleep duration after matching/pre-trend adjustment.

SB3 is more identifiable than permanent non-awakening and should precede SB2.

---

# 12. Reporting hierarchy

### Confirmatory / primary

U1/U2, D1–D3, P1/P2, C1/C3, R2, H1–H4 where calibration permits, F1, I1, PT1 for the clinical subset.

### Secondary

P3, C2/C4, R1, F2/F3, I2/I3, CC1/CC2, PT2/PT3.

### Exploratory

SB1–SB3 (especially SB2), Talent Misallocation, global Trust Tax.

If feasibility fails for a primary model, downgrade it explicitly rather than filling the gap with an unvalidated number.
