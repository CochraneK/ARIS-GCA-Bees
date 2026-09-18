# WORKBUDDY HANDOFF — ARIS4C012 ONLY

## Task identity

**Project:** ARIS4C012  
**Paper:** *When Opposites Become Causes: An Indexed Cross-Domain Framework for Oppositional Causal Inversion*

This is **NOT ARIS4C003**.  
Do not code IKES, disciplines, colonial history, D01–D21, or any 003 artifact.

## Independent Coder B task

Complete the 30-record blind coding packet:

`papers/012-oppositional-causal-inversion/data/pilot0_coderB_blind.csv`

Records are:

`P01 ... P30`

The core fields include:

- `opposition_valid`
- `oci_candidate`
- `primary_mechanism`

and the remaining index/mechanism/evidence fields already present in the CSV.

## Allowed inputs

Read only:

1. `papers/012-oppositional-causal-inversion/process/CONCEPT_SCHEMA.md`
2. `papers/012-oppositional-causal-inversion/process/SEARCH_PROTOCOL.md`
3. `papers/012-oppositional-causal-inversion/process/CODER_B_HANDOFF.md`
4. `papers/012-oppositional-causal-inversion/data/pilot0_coderB_blind.csv`
5. original publications/abstracts/full text required to judge P01–P30.

The exact pre-B freeze hashes are recorded in:

`papers/012-oppositional-causal-inversion/process/CODER_B_FREEZE.json`

## Forbidden inputs

Do **not** read:

- `data/pilot0_coderA_feasibility.csv`
- `process/PILOT0A_AUDIT.md`
- `data/reliability/`
- any file containing Coder A labels or A/B comparison;
- `process/SCHEMA_V2_PROPOSAL.md` — this was created after v1 freeze and is intentionally not part of Pilot 0B;
- ARIS4C003 Coder B / IKES materials;
- any prior summary stating which P records A called OCI-positive/negative.

## Required output

Overwrite only:

`papers/012-oppositional-causal-inversion/data/pilot0_coderB_blind.csv`

with all 30 records independently coded.

Do not adjudicate against Coder A.

Do not compute agreement.

Do not modify the frozen v1 schema.

## Completion test

The task is complete only when all P01–P30 have nonblank values for:

- `opposition_valid`
- `oci_candidate`
- `primary_mechanism`

After commit, the repository workflow:

`.github/workflows/aris4c012-coder-agreement.yml`

will automatically detect completion and calculate raw agreement, Cohen's kappa, Krippendorff nominal alpha, and a disagreement packet.

## Independence declaration

At completion, the commit message should state:

`ARIS4C012: independent blind Coder B complete`

and the WorkBuddy report should state whether any forbidden Coder A material was viewed. If contamination occurred, disclose it rather than claiming independence.
