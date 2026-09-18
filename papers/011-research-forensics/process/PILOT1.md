# Pilot 1 — deterministic detector adapters

Status: implementation committed; CI validation required before promotion.

## Scope

Pilot 1 deliberately excludes learned text/image/LLM detectors. Its purpose is to validate the forensic contract with checks that are reproducible from structured inputs.

Implemented adapters:

- F1: NHST p-value recomputation for t, z, chi-square and F tests.
- F2: conservative GRIM-style discrete item-mean feasibility.
- F2: conservative DEBIT-style binary mean/SD feasibility.
- F3: table percentage, sum and rank-sequence checks.
- F5: DOI/reference metadata verification from externally provenance-stamped resolver results.

## Non-goals

- This is not a full port of statcheck, GRIMMER, SPRITE, or scrutiny.
- The binary detector is DEBIT-style feasibility, not a claim of bit-for-bit equivalence with an external package.
- PDF extraction is not bundled into the detector logic.
- DOI network retrieval is outside the deterministic detector; resolver outcomes must include source and verification time.
- Pilot 1 contains no empirical sensitivity/specificity estimate.

## Input architecture

Extraction and verification produce structured records with source locators. Detectors consume only the records they are designed to assess.

This separation is intentional:

PDF/XML -> extraction -> structured record -> applicability gate -> deterministic detector -> Finding

It permits extraction errors and detector errors to be audited separately.

## Required Pilot 1 invariants

- record-level non-applicability remains ABSTAIN;
- an applicable detector may contain a mix of PASS/FLAG/ABSTAIN records;
- no finding may set misconduct_inference=true;
- all flags retain enough numbers to reproduce the check;
- every flag lists benign alternatives and a concrete reviewer next action.

## Honest-error link

The first correction seed includes a "Top 50" table with a missing rank 14. The Pilot 1 rank-sequence detector is intentionally capable of representing this kind of deterministic inconsistency. Correct detection should increase anomaly recall, while safe synthesis should **not** increase misconduct accusations.

## Next

After CI passes:
1. promote Pilot 1 to main;
2. build a small historical full-text extraction pilot;
3. run these adapters on time-safe real manuscripts;
4. measure extraction failure, detector applicability, flag yield, and reviewer verification time before adding learned models.
