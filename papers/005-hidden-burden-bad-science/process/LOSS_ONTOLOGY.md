# LOSS ONTOLOGY — ARIS4C005

## Purpose

This ontology prevents the project from treating every undesirable research outcome as the same phenomenon. It separates **exposure type**, **harm pathway**, **unit of loss**, and **identifiability**.

---

# A. Exposure ontology

## E1 — confirmed severe integrity failure

Examples:

- formal fabrication/falsification findings;
- retractions where the reason supports serious author-caused unreliability;
- independently verified serious data/image fabrication;
- organized publication fraud with strong evidence.

E1 is the cleanest exposure for causal event studies but is a detected subset, not prevalence.

## E2 — probable severe integrity failure

Examples:

- multiple convergent high-specificity anomaly detectors;
- high-confidence paper-mill signatures;
- impossible/internally inconsistent statistical structures confirmed by audit;
- high-confidence image or data reuse with no adequate explanation;
- unresolved integrity concerns with strong evidence but no formal finding.

E2 requires calibration against audited cases. A model probability is not a misconduct verdict about a named individual.

## E3 — broader research waste / distortion

Examples:

- nonpublication;
- severe honest error;
- irreproducibility not attributable to misconduct;
- avoidable low-value design/reporting;
- discontinued research that yields no usable knowledge;
- selective reporting where misconduct cannot be established.

E3 is scientifically and socially important but must not be labeled fraud.

---

# B. Loss layers

## L1 — production-resource loss

### L1.1 Direct financial cost

**Unit:** currency, price-year specified.

Includes attributable funding spent on severely flawed outputs, not whole grants by default.

Preferred estimator:

`attributable grant cost = grant award * allocation rule for target output`

Sensitivity: fractional attribution by publication count, staff effort, or project output share.

### L1.2 Researcher-Life-Years (RLY)

**Unit:** full-time-equivalent researcher-years.

Subcomponents:

- `RLY_production`: time spent producing a severely flawed work that loses scientific value;
- `RLY_followup`: time spent by downstream teams following unreliable findings;
- `RLY_replication`: avoidable replication/verification triggered by unreliable foundations;
- `RLY_correction`: time spent correcting, investigating, retracting, reanalyzing, or rebuilding evidence.

Do not equate a paper with one researcher-year. Estimate effort distributions by study type and field.

### L1.3 Participant sacrifice without knowledge gain

**Unit:** participant-hours, enrolled participants, participant-risk events, or burden-weighted participation.

Primary clinical definition:

> participant exposure to study burden/risk that fails to contribute usable public knowledge because of nonpublication, severe integrity failure, or invalidation.

E3 nonpublication and E1/E2 integrity failure must be reported separately.

### L1.4 Infrastructure/sample opportunity cost

**Unit:** instrument-hours, scarce samples, animal subjects, compute-hours, biobank aliquots, telescope/beamline time, etc.

Initially secondary because comparable global data are weak.

---

## L2 — labor and career-capital loss

### L2.1 Integrity Maintenance Debt (IMD)

**Unit:** person-hours.

Includes:

- peer-review hours spent on fraudulent/manufactured submissions;
- editorial triage/investigation time;
- institutional investigation time;
- correction/retraction production;
- systematic-review reanalysis;
- post-publication integrity screening.

IMD differs from ordinary quality-control labor: estimate the incremental burden attributable to problematic work.

### L2.2 Collateral Career Damage (CCD)

**Units:** citation loss, funding loss, promotion/job transitions, collaboration loss, or modeled career-capital change.

Target population: collaborators/students not implicated in the integrity failure.

Anchor evidence: Hussinger & Pellens (2019) estimated an 8–9% citation penalty among uninvolved prior collaborators after documented misconduct events.

### L2.3 Talent Misallocation

**Unit:** trainee/researcher-years spent in research trajectories that would likely have been avoided under reliable evidence.

Exploratory because assignment of the counterfactual career path is difficult.

---

## L3 — epistemic / knowledge-system loss

### L3.1 Scientific Contamination Footprint (SCF)

**Unit:** dependent downstream knowledge objects.

Layered counts:

- `SCF_1`: direct citing works materially relying on the problematic claim;
- `SCF_2`: second-order dependent works;
- `SCF_SR`: systematic reviews/meta-analyses containing the problematic evidence;
- `SCF_G`: guidelines/policy/HTA documents materially relying on contaminated synthesis;
- `SCF_P`: patents or translational outputs materially relying on problematic evidence.

A citation is not automatically contamination.

### L3.2 Epistemic Reproduction Number (R_E)

For a problematic knowledge node or claim cluster:

`R_E(t) = expected number of new materially dependent knowledge nodes generated per active contaminated node over a defined time interval.`

Interpretation:

- `R_E > 1`: contamination is expanding;
- `R_E < 1`: contamination is decaying.

This is a knowledge-propagation analogy, not a biological epidemic claim.

### L3.3 Knowledge Ghost Half-Life (KGH)

**Unit:** years after correction/retraction.

Definition:

> time from a visible correction event until the rate of new materially dependent uses of the unreliable claim falls to 50% of the pre-correction counterfactual/reference rate.

Estimate separately for ordinary citations, evidence syntheses, guidelines, and policy/translational use.

### L3.4 Evidence distortion

**Units:** change in pooled effect, change in direction/significance, recommendation changes, certainty-of-evidence changes.

VITALITY-style leave-retracted-evidence-out analysis is a primary template.

---

## L4 — innovation/opportunity loss

### L4.1 Innovation Delay Years (IDY)

**Unit:** years.

Definition:

> counterfactual delay in the arrival, uptake, funding, or recognition of a legitimate alternative caused by an unreliable research trajectory or integrity shock.

Preferred identification:

- matched topic clusters;
- event study / difference-in-differences;
- synthetic control;
- pre-trend diagnostics;
- negative-control topics.

This is the primary innovation estimand because delay is more identifiable than permanent disappearance.

### L4.2 Scientific Detour Years (SDY)

**Unit:** field-years or cumulative researcher-years.

Definition:

> time during which a topic cluster devotes excess attention/resources to a trajectory later shown to rely on severely unreliable foundations.

Requires an explicit counterfactual benchmark, not retrospective storytelling.

### L4.3 Research crowding-out

**Units:** displaced funding, displaced publications, delayed topic entrants, attention share.

Do not assume fixed journal capacity. Measure observed displacement mechanisms.

### L4.4 Never-Woken Sleeping Beauties (NWSB)

**Unit:** model-estimated expected count, never a directly observed count.

Target estimand:

`sum_i [P(awake_i | low-contamination counterfactual) - P(awake_i | observed environment)]`

Candidate predictors:

- pre-awakening citation trajectory;
- semantic novelty;
- cross-field distance;
- topic growth;
- later independent rediscovery similarity;
- network position;
- availability of plausible Prince papers;
- funding/attention shocks.

The result must be labeled **counterfactual opportunity loss**.

---

## L5 — societal / translational loss

### L5.1 Clinical-decision distortion

**Units:** changed recommendations, changed treatment exposure, modeled patient outcomes where defensible.

Only pursue after evidence-synthesis contamination is established.

### L5.2 Policy distortion

**Units:** policy documents, decisions, program expenditure, or implementation delay linked to unreliable evidence.

Initially exploratory because policy citation semantics are heterogeneous.

### L5.3 Industrial/translational misallocation

**Units:** patents, R&D spend, failed follow-up development, time-to-translation.

Use only when linkage is concrete.

### L5.4 Trust Tax

**Units:** extra verification/monitoring/investigation time or cost; survey trust outcomes are secondary.

Avoid treating generic public distrust as causally attributable to misconduct without design-based evidence.

---

# C. Identifiability tiers

## Tier A — directly measurable or strongly design-identifiable

- detected/retracted counts and rates under explicit denominators;
- time-to-retraction;
- post-retraction citation/dependence persistence;
- retracted-evidence effect on meta-analysis results;
- attributable direct grant cost under declared allocation rules;
- specific participant counts in invalid/nonpublished trial subsets;
- documented collaborator citation/funding spillovers.

## Tier B — model-assisted but calibratable

- latent E2 article prevalence;
- Researcher-Life-Years;
- Integrity Maintenance Debt;
- SCF higher-order propagation;
- R_E and KGH;
- Innovation Delay Years.

## Tier C — exploratory counterfactual

- permanent publication/discovery displacement;
- Scientific Detour Years at global scale;
- Never-Woken Sleeping Beauties;
- Talent Misallocation;
- Trust Tax at global scale.

The manuscript must never present Tier C outcomes with the rhetorical certainty of Tier A outcomes.

---

# D. Anti-double-counting rules

1. A researcher-hour can belong to only one direct labor component in the accounting table; overlapping causal pathways are shown separately.
2. Direct grant cost and researcher salary time are not summed unless the grant-cost accounting explicitly excludes/partitions salary.
3. A downstream paper is counted once per SCF layer even if it cites multiple problematic sources; source-level and unique-work counts are both reported.
4. Participant burden is not converted into researcher time or dollars in the primary dashboard.
5. Career penalties to perpetrators are not automatically treated as societal loss; sanctions may be intended correction mechanisms. Collateral harm to uninvolved people is a distinct outcome.
6. Honest error and misconduct are never merged in the primary exposure label.

---

# E. Dashboard vector

The project reports a vector, not a score:

`Burden = (USD, RLY, participant burden, IMD hours, SCF, R_E, KGH, IDY, CCD, exploratory NWSB)`

Every component carries:

- exposure layer (E1/E2/E3);
- population and time window;
- observed vs modeled status;
- uncertainty interval;
- data version;
- assumptions/sensitivity range.
