# Deep-coding queue · ARIS4C008 Pilot 8

The 50 new Tier-1 taxa are now converted into an execution queue.

## Rules

1. **Positive evidence and tested-negative evidence are separate searches.** No missing paper becomes a zero.
2. Every row receives explicit **O1–O7 outcome coding**; otherwise component presence cannot be used as an anti-sufficiency contrast.
3. Theory candidates start from the module evidence already in `theory_candidate_evidence_seed_v0.csv` and fill the complementary modules.
4. Underrepresented-clade and matched-family calibration taxa have the highest tested-negative priority because they are the main defense against spectacular-animal selection bias.
5. ACDB/ASNR presence reduces search cost but is never itself a biological score.

## Queue composition

- theory-discriminating: 14
- underrepresented-clade calibration: 15
- matched-family ordinary calibration: 10
- source candidates: 11

## First-pass stopping rule

A taxon completes first-pass deep coding when:
- each priority module has at least one of: positive, tested-negative, ambiguous-but-tested, or documented not-tested;
- exact-species scope is explicit;
- captive/wild/task context is retained;
- O1–O7 outcome evidence has been searched separately;
- sources are sufficient to distinguish “not observed” from “tested and failed”.

The queue is deliberately staged. Completing these 50 does not automatically unlock confirmatory modeling; recoverability is rerun after the empirical matrix is rebuilt.
