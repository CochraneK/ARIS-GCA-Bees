# ARIS4C006 · Confirmatory unlock protocol

Last updated: 2026-09-19

## Principle

The preregistration lock freezes the design files listed in
`code/27_prereg_lock.py`.

**No file covered by the preregistration hash may be edited merely to unlock
confirmatory analysis.**

In particular, the locked values

- `ANALYSIS_SPEC.json -> confirmatory_outcomes_unlocked = false`
- `DESIGN_GATES.json -> confirmatory_outcomes_unlocked = false`

remain false permanently in the locked design snapshot. They record the state
at preregistration-lock creation.

## Separate mutable unlock record

After:
1. all frozen outcome-blind execution gates pass;
2. `PREREGISTRATION_LOCK.json` is created and committed;
3. repository status is promoted to `preregistered`;

a **separate repository change** may create:

`process/CONFIRMATORY_UNLOCK.json`

with exactly this semantic content:

- `schema_version = 1`;
- `paper_id = "006"`;
- `unlocked = true`;
- `prereg_lock_label` equals the committed lock label;
- `prereg_lock_sha256` equals the committed lock combined SHA-256;
- a short provenance note stating that all pre-outcome gates passed.

This unlock file is intentionally **not** part of the preregistration hash.

## Integrity check before every confirmatory execution

Before H1/H2/H3 code may read or estimate a scientific outcome:

1. load `PREREGISTRATION_LOCK.json`;
2. recompute SHA-256 for every file listed in `file_sha256`;
3. require byte-for-byte equality with every stored hash;
4. require the locked design/gate booleans to remain false;
5. load `CONFIRMATORY_UNLOCK.json`;
6. require `unlocked = true`;
7. require its lock label and combined SHA to match the committed lock;
8. require `paper.json` status to be `analysis` or `manuscript`.

If any locked file changed after preregistration, confirmatory execution stops.

## State transitions

Allowed sequence:

`research-design`
→ outcome-blind execution gates PASS
→ preregistration hash created while locked
→ `preregistered`
→ separate unlock record committed
→ `analysis`
→ confirmatory execution.

Forbidden:
- changing a locked design document in the same commit that unlocks analysis;
- regenerating a lock after inspecting H1/H2/H3;
- pointing the unlock record to a different or newly regenerated lock;
- setting analysis status without a valid unlock record;
- running confirmatory code against locked-file hashes that no longer match.

## Amendments after lock

A substantive design amendment after lock is not an “unlock”.

It requires:
- explicit amendment documentation;
- a new versioned preregistration record;
- preservation of the original lock and hashes;
- clear separation of analyses under the original versus amended specification.

No amendment may be used to retroactively redefine a confirmatory result after
the original outcome has been inspected.
