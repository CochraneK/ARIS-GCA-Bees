# SCHEMA V2 FROZEN — ARIS4C012

Frozen: 2026-09-19  
Status: **FROZEN FOR FRESH A2/B2 VALIDATION**  
Supersedes for new validation only: `CONCEPT_SCHEMA.md` v1 and the non-frozen `SCHEMA_V2_PROPOSAL.md`.

> This freeze does **not** recode Pilot 0B. The raw v1 reliability result remains an immutable failed instrument-validation result.

## 1. Unit of coding

One row = one retrieved scholarly record. Coders must code only the evidence available in the blinded packet supplied for the fresh validation sample. Free-text notes are allowed for audit but are excluded from nominal reliability calculations.

Missing information is **not** coded as `no`. Use `uncertain` when the construct is relevant but cannot be resolved from the supplied material.

## 2. Canonical tokens

All categorical tokens below are lowercase ASCII with underscores. Coders must use exactly these tokens.

### Axis A — entry gate

`opposition_valid ∈ {yes, no, uncertain}`

Definition: whether the focal causal claim contains a functional opposite/reversal after the relevant indices are made explicit.

`oci_candidate ∈ {yes, no, uncertain}`

Definition: whether the record is a candidate for the restricted OCI evidence map, conditional on the construct definition rather than rhetorical use of “paradox”.

### Axis B — opposition relation vector

Each field uses `{0, 1, uncertain}` and is independently coded:

- `rel_same_construct_reversal`
- `rel_target_reversal`
- `rel_functional_reversal`
- `rel_relational_reversal`
- `rel_proxy_reversal`

Multiple 1s are allowed.

### Axis C — index-switch vector

Each field uses `{0, 1, uncertain}`:

- `idx_actor_switch`
- `idx_level_switch`
- `idx_time_switch`
- `idx_construct_switch`
- `idx_environment_switch`

These are **not mechanisms**.

### Axis D — generative-mechanism vector

Each field uses `{0, 1, uncertain}`:

- `mech_strategic_adaptive_feedback`
- `mech_capacity_overload`
- `mech_nonlinear_ecological_dynamics`
- `mech_information_filtering`
- `mech_norm_motivational_reactance`
- `mech_exposure_induced_adaptation`
- `mech_intervention_toxicity`
- `mech_coordination_externality`

Multiple mechanisms may be coded 1. No `primary_mechanism` field exists in v2.

### Axis E — evidence mode vector

Each field uses `{0, 1, uncertain}`:

- `ev_randomized_experiment`
- `ev_quasi_experiment`
- `ev_longitudinal_observational`
- `ev_cross_sectional_observational`
- `ev_formal_model`
- `ev_simulation`
- `ev_qualitative_process`
- `ev_systematic_review`
- `ev_meta_analysis`
- `ev_conceptual_theory`

Multiple evidence modes are allowed because a single paper may combine them.

`evidence_strength ∈ {none, weak, moderate, strong, uncertain}`

Strength refers to support for the focal causal/reversal claim **within the supplied evidence**, not overall paper quality.

### Axis F — result direction

`result_direction ∈ {supports_reversal, null, opposes_reversal, mixed, formal_only, not_tested, uncertain}`

This is distinct from candidacy. A paper can be an OCI candidate and report `opposes_reversal` or `null`.

### Axis G — normative valence

`normative_valence ∈ {beneficial, harmful, mixed, actor_dependent, not_normatively_classified, uncertain}`

Normative valence is descriptive only and never determines OCI candidacy.

## 3. Coding precedence rules

1. **Code the claim, not the title word.** “Paradox”, “backfire”, “counterfinality”, etc. are not automatic OCI labels.
2. **Separate indices from mechanisms.** A time/actor/level/construct/environment switch is never entered as a mechanism.
3. **Do not force exclusivity.** Relation, mechanism, and evidence-mode vectors are multi-label.
4. **Do not infer absent evidence.** Use `uncertain` rather than `0` when the packet does not resolve a relevant axis.
5. **No synonym invention.** If the exact concept is not represented, use the closest defined field only when its definition is satisfied; otherwise leave all candidate fields 0/uncertain and explain in `coder_note`.
6. **No retrospective harmonization during blind coding.** Coders cannot see each other's labels before both files are frozen.

## 4. Reliability gate for fresh A2/B2 validation

The fresh validation sample must be independent of Pilot 0B.

Primary gate:
- `opposition_valid`: Cohen's κ >= **0.70**.

Secondary gate:
- for each informative categorical/binary axis with at least two categories used by both coders and >=20 pairwise-complete rows: κ >= **0.60** and raw agreement >= **0.80**;
- median κ across informative v2 axes >= **0.70**;
- any axis failing the secondary gate must be explicitly revised or demoted from confirmatory use before full screening.

Degenerate/sparse axes:
- if κ is undefined because one/both coders use only one category, report prevalence and raw agreement; do not count undefined κ as evidence of reliability.

The 165-record evidence-map frame remains gated until the fresh v2 pilot passes.

## 5. Blinding and provenance

- A2 and B2 receive the same frozen coding instructions and blinded records.
- Neither coder may inspect Pilot 0B adjudication materials while coding the fresh sample.
- Each completed coder file must be frozen by content hash before comparison.
- Adjudication begins only after both coder files are frozen.

## 6. Required output columns

The canonical blank form is `data/v2_validation_coding_template.csv`.

Excluded from reliability metrics:
- `title`
- `coder_note`
- provenance columns.

## 7. Why this freeze follows the diagnostic

Pilot 0B produced 141 disagreement cells. Diagnostic partitioning found:
- 30 lexical/token-vocabulary mismatches;
- 24 schema-category overlaps;
- 26 source/metadata disagreements;
- 61 genuine conceptual disagreements.

v2 removes the avoidable forced-category and token-vocabulary failure modes while preserving the need to test genuine conceptual reliability on a fresh sample.
