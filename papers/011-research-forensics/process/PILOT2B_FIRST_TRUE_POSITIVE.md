# Pilot 2B — first pre-outcome real true-positive

Updated: 2026-09-18

## Case

Target DOI: 10.1371/journal.pone.0258910  
Target publication: 2021-10-22  
Later correction DOI: 10.1371/journal.pone.0303714  
Correction publication: 2024-05-09

The documented correction concerns Table 1's summary of Harper & Rhodes (2021).

## Time-safe target artifact

The exact PLOS printable PDF was captured by the Wayback Machine on 2022-01-14, more than two years before the correction.

- archive timestamp: 20220114120313
- MIME type: application/pdf
- CDX digest: BLKICC3WUYN7GH4E7K63U5GD2NW2RYWY
- role: table
- qualification: SAFE_EXACT

The archived PDF contains Table 1 on PDF page 15. The historical Harper & Rhodes row reports N=322, RMSEA=0.080, CFI=0.77, and best fitting model=5 factors.

## Contemporaneously available comparison source

Harper & Rhodes, DOI 10.1111/bjso.12452, was first published on 2021-02-17, before the PLOS target paper. Its Study 2 confirmatory factor analysis reports N=322 and the improved three-factor model with CFI=0.87 and RMSEA=0.07.

The target paper therefore could have been checked against the cited source at publication time. No 2024 correction information is required for the detector.

## Detector result

The deterministic F5 adapter cross_source_field_consistency compares only prespecified source-verified fields.

- N: MATCH
- RMSEA: MISMATCH
- CFI: MISMATCH
- best fitting model: MISMATCH
- overall: FLAG
- evidence class: E2
- review priority: MODERATE
- misconduct inference: false

The later 2024 PLOS correction independently confirms that the model and CFI/RMSEA values in Table 1 were incorrect. The correction is ground truth only; it is not detector input.

## Significance

This is the first ARIS4C011 case that is content-eligible, has the exact historical artifact role, uses comparison evidence available before target publication, runs under Track A provenance rules, and flags the same discrepancy later documented by an official correction.

It is still only one case. It does not establish recall, precision, or superiority. It demonstrates that the full time-safe pipeline can produce a genuine pre-outcome true positive rather than only synthetic tests or post-outcome rediscovery.
