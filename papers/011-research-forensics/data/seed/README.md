# Benchmark v0 real-data seed

Date captured: 2026-09-18.

This seed is deliberately tiny. Its purpose is schema validation, not prevalence estimation or model evaluation.

## Included target works

1. **10.1177/1758835919874651** — current Crossref title contains a `RETRACTED:` prefix. The official retraction notice describes concerns about scientific accuracy and legitimacy but does not establish a specific fabrication/falsification subtype.
2. **10.1538/expanim.54.1** — official retraction notice states that the editorial board investigated an illegal gift-authorship case.
3. **10.1007/s11277-021-09072-0** — current Crossref title contains `RETRACTED ARTICLE:`; publisher notice attributes retraction to a compromised guest-edited process and manipulated peer review.

## Why these three are useful

They expose three separate benchmark hazards with only three records:

- **label heterogeneity**: all are "retracted", but the stated problems differ;
- **metadata leakage**: current titles can explicitly contain the outcome;
- **detectability mismatch**: authorship/peer-review manipulation may leave little or no signal in manuscript content.

Therefore a content-only detector cannot reasonably be scored as if every official retraction reason were observable from the article itself. Detector eligibility/abstention must be issue-specific.

## Provenance

Bibliographic/update relations were checked against the Crossref production REST API on 2026-09-18. Retraction reasons were checked against publisher/PMC/J-STAGE records.

This seed must never be interpreted as representative of all retractions.
