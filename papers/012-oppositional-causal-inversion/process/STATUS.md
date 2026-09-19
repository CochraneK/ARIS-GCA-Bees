# STATUS — ARIS4C012

Updated: 2026-09-19

## State

**SCHEMA V2 TESTED AND FAILED · INSTRUMENT REVISION (v3) REQUIRED · 165-RECORD SCREEN STILL LOCKED**

## Canonical identity

**When Opposites Become Causes: An Indexed Cross-Domain Framework for Oppositional Causal Inversion**

ARIS4C012 tests a restricted indexed representation of functional-opposite-producing causal effects. It does not treat rhetorical paradoxes as empirical truths.

## Preserved v1 result

Pilot 0B remains an immutable failed instrument-validation result:

- opposition_valid κ = 0.466;
- OCI candidacy κ = 0.592;
- primary_mechanism κ = 0;
- 141 disagreement cells.

The 141 cells were exhaustively partitioned for diagnosis:
- lexical/token mismatch: 30;
- schema-category overlap: 24;
- source/metadata disagreement: 26;
- genuine conceptual disagreement: 61.

No post-hoc normalization has replaced the raw v1 statistics.

## Frozen Schema v2

`process/SCHEMA_V2_FROZEN.md` separates:
1. entry/opposition validity;
2. opposition relation vector;
3. index-switch vector;
4. generative mechanism vector;
5. evidence-mode vector and controlled evidence strength;
6. result direction;
7. normative valence.

There is no forced single `primary_mechanism`.

Frozen reliability gate:
- opposition_valid κ >= 0.70;
- each informative secondary axis: κ >= 0.60 and raw agreement >= 0.80;
- median κ across informative axes >= 0.70;
- undefined κ on sparse/degenerate axes is reported, not counted as a pass.

## Fresh validation sample and evidence packet

The original fresh draw used six retrieval strata × five records, excluded Pilot 0B, and used fixed seed `ARIS4C012-V2-A2B2-20260919`.

First immutable materialization:
- 24/30 abstract excerpts;
- 6/30 bibliographic-only;
- coding remained locked.

Amendment 01:
- attempted record-level public landing metadata for only the six missing slots;
- recovered 0/6;
- preserved the first packet.

Amendment 02 was frozen **before any A2/B2 labels existed**:
- same retrieval stratum;
- same original fixed-seed/FNV hash order;
- scan forward after original sampled records;
- accept the first candidate with materializable record-level evidence;
- no label, outcome, adjudication, or manuscript-utility information may influence replacement.

Final result:
- 6 deterministic replacements;
- 30/30 abstract excerpts;
- no remaining bibliographic-only slots;
- A2/B2 response forms are byte-identical.

Final hashes:
- evidence packet: `8eb9fd3782d480ce7412f378b422296047f5190e1208675e767ddcf7fc114ccf`
- Schema v2: `066f3e42aeda4fc5842abd2d44310a3da45588ecc41e466282b93af1e960f681`
- response form: `1e57bfb2c8e52e296eb6b6d938683780b84ce4250de19cd899a83d99ff7d6398`
- A2/B2 input bundle: `9f0d8b785b8f8f739cdd41cf7c6f9f6fc3f7fbdf2299587cbab6d732bdddfc51`

## Independence safeguards

`process/V2_INDEPENDENT_CODING_PROTOCOL.md` requires:
- truly separate A2 and B2 execution surfaces;
- identical frozen input bundle;
- no access to the other coder's labels;
- no Pilot-0 labels/adjudication during coding;
- a separate completion hash/freeze for each coder;
- comparison only after both freezes exist.

`.github/workflows/aris4c012-v2-agreement.yml` rejects partial one-coder integration on `main`.

An independent coding surface has since executed both A2 and B2 against this
frozen bundle, so the requirement for two independent judges is met; the gate
itself returned **REVISE_V2_INSTRUMENT** (see below).

## Current hard gate

### Gate B2 — Schema-v2 construct reliability

- Schema: **FROZEN**
- Fresh validation evidence: **READY (30/30)**
- A2/B2 input equality: **PASS** (identical `input_bundle_sha256` on both completion freezes)
- Independent A2 coding: **RUN** — 30/30, `data/v2_coding/A2_completed.csv`, frozen
- Independent B2 coding: **RUN** — 30/30, `data/v2_coding/B2_completed.csv`, frozen
- Reliability decision: **REVISE_V2_INSTRUMENT** (see `process/V2_AGREEMENT_DIAGNOSIS.md`)
- Full 165-record screen: **LOCKED**

## v2 executed result (2026-09-19)

Two coders were run against the same frozen bundle by one driver script
(`code/run_v2_coders.py`), at temperature 0, by explicit model id, from two
different provider families. Each coder's request contained only the frozen
schema and its batch of packet records; the two judges never received each
other's labels, and both files were frozen before any comparison. What is
independent is the *judge*; the prompt and the field list were deliberately held
constant, because in a reliability test the instrument must not vary. See
`process/V2_AGREEMENT_DIAGNOSIS.md` section 8 for the full provenance record.

| metric | value | threshold |
| --- | --- | --- |
| `opposition_valid` Cohen's kappa | 0.481 | >= 0.70 |
| median kappa across 33 informative axes | 0.372 | >= 0.70 |
| secondary axes passing | 1 / 32 | all |
| disagreement cells | 380 | — |

The primary gate failure is not a base-rate artifact: raw agreement 0.733 against
a Cohen chance expectation of 0.487 gives kappa 0.481 and nominal alpha 0.471.
68.2% of
all cells are a single `0` vs `uncertain` conflict created by schema precedence
rule 4, and `oci_candidate` duplicates `opposition_valid` on 30/30 records.
Diagnosis, root causes and the proposed v3 amendment are in
`process/V2_AGREEMENT_DIAGNOSIS.md`.

This is a failure of the instrument, not evidence about the phenomenon: v2
cannot yet measure oppositional causal inversion reliably, and nothing in this
result supports or refutes the framework's substantive claim.

## Next execution queue for this paper

1. Do not re-score or harmonize the v2 labels; the result is final.
2. Draft a v3 amendment against the four root causes in the diagnosis, the
   highest-value change being removal of `uncertain` from the vector axes.
3. Draw a fresh validation sample that does not overlap V201..V230.
4. Re-run independent A3/B3 coding, freeze both, then re-run the scorer.
5. Only a PASS unlocks the 165-record evidence-map screen.

## Handoff sentence

**ARIS4C012's v2 instrument has now been genuinely tested by two independent
coding surfaces and failed (primary kappa 0.481 against a 0.70 gate). The
remaining work is instrument revision under a v3 amendment plus a fresh,
non-overlapping validation sample — not more coding against the v2 form.**
