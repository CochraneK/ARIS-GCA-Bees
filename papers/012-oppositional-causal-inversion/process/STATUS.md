# STATUS — ARIS4C012

Updated: 2026-09-19

## State

**SCHEMA V2 FROZEN · FINAL 30-RECORD BLIND BUNDLE READY · GENUINELY INDEPENDENT A2/B2 REQUIRED**

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

The current controller does not have a genuinely independent second coding surface, so **ARIS4C012 is Blocked at this gate rather than simulating independence**.

## Current hard gate

### Gate B2 — Schema-v2 construct reliability

- Schema: **FROZEN**
- Fresh validation evidence: **READY (30/30)**
- A2/B2 input equality: **PASS**
- Independent A2 coding: **NOT YET RUN**
- Independent B2 coding: **NOT YET RUN**
- Reliability decision: **LOCKED**
- Full 165-record screen: **LOCKED**

## Next execution queue for this paper

1. Execute A2 and B2 in genuinely independent isolated contexts.
2. Freeze each completed response with `code/freeze_v2_coder.py`.
3. Only after both freezes exist, integrate both completed files.
4. Run `code/score_v2_agreement.py`.
5. If PASS, unlock the 165-record evidence-map screen.
6. If FAIL, revise only failing v2 axes under an explicit new amendment and validate again on a fresh sample.

## Handoff sentence

**ARIS4C012 has finished everything the current controller can validly do before independent coding. Resume only with genuinely independent A2/B2 execution; do not duplicate the same controller as two coders.**
