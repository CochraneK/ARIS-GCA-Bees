# Pilot 1C result — first SAFE_EXACT real manuscript

Updated: 2026-09-18

## Artifact

Target DOI: `10.1538/expanim.54.1`  
Retraction event: 2022-08-01  
Document: *Effect of Treadmill Exercise on Bone Mass in Female Rats*  
Article type: Review

Wayback/CDX discovered the exact J-STAGE publisher endpoints before the retraction:

- HTML capture: 2018-06-11, digest `YZQHEJFRYGMRELLFBDCNGMLNPXZSWV33`
- PDF capture: 2018-07-25, `application/pdf`, digest `BVVVDATHFQQOSOD4UX6KKPS7YDZJF3H3`

The PDF is therefore promoted to **SAFE_EXACT** for body-text/reference-list roles.

Source verification of the PDF header gives:

- *Experimental Animals*
- volume 54
- issue 1
- pages 1–6
- year 2005
- Review

## Pilot 1 deterministic result

The historical review contains no eligible structured records for the currently implemented deterministic adapters:

- F1 NHST recomputation: ABSTAIN
- F2 GRIM discrete mean: ABSTAIN
- F2 binary mean/SD feasibility: ABSTAIN
- F3 table arithmetic/completeness: ABSTAIN
- F5 DOI metadata: ABSTAIN in this first smoke fixture because reference-resolution records have not yet been generated

Overall review priority: **NONE**.

This is not a detector success/failure against gift authorship. The official issue label is process/authorship-level and the current deterministic content checks are not expected to detect it. The result is a valid **coverage and applicability** observation.

## Extraction-layer failure discovered

A separate automated extraction of the archived PDF correctly identified the title but returned the bibliographic year as 2004 and pages as 1–8.

The source PDF header is 54(1), 1–6, 2005. The 2004 dates are submission/acceptance dates, not publication year.

This provides a real example of **extractor error before detector execution**.

ARIS4C011 therefore now treats extraction as an auditable stage:

`historical object -> extraction -> source verification -> detector input`

For Track A, every non-empty structured detector record must now retain a `source_locator` and set `provenance_verified=true`; otherwise the entire confirmatory run fails closed before any detector executes.

## Interpretation

The first SAFE_EXACT real-manuscript run demonstrates three distinct states that must not be collapsed:

1. the historical artifact can be valid;
2. automated extraction can still be wrong;
3. a detector family can be genuinely non-applicable.

That separation is central to the paper's benchmark design.
