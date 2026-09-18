# ARIS4C006 · Pilot 3 — Crossref structured-family validation

Last updated: 2026-09-18

## Verdict

**PASS as a structured surname-evidence route; NOT a pass for the last-token heuristic.**

GitHub Actions run: `35276216696`  
Artifact: `aris4c006-crossref-family-pilot`

This pilot tested whether DOI-linked Crossref contributor metadata can provide structured family-name evidence for OpenAlex authorships. It did **not** estimate any surname effect.

## Design

- Year: 2024
- Fields: Economics, Mathematics, Business, Psychology, Medicine, Engineering
- Requested DOI-containing multi-author works: 30 per field, 180 total
- Join: OpenAlex work DOI -> Crossref work record
- Positional comparison was attempted only when OpenAlex and Crossref reported the same author count.
- Only aggregate outputs were retained.

## Results

### Work-level coverage within the DOI-selected pilot

- Crossref records found: **180 / 180 (100%)**
- Same OpenAlex/Crossref author count: **172 / 180 (95.56%)**
- Crossref family name present for all contributors: **99.44%** of found records
- Aligned author rows from same-count works: **1,305**
- Aligned China-affiliated author rows: **787**

Important: because this pilot deliberately sampled works that already had DOI values, **100% Crossref retrieval is not an estimate of DOI coverage in the underlying OpenAlex population**. Pilot 4 measures that denominator.

### China-affiliated author rows

Across 787 positionally aligned China-affiliated author rows:

- Crossref family matched some token in the OpenAlex raw/display name: **99.87%**
- Crossref family matched the last token: **99.87%**
- Crossref family matched the first token: **0.38%**

This shows that, in this bounded modern DOI sample, OpenAlex name strings overwhelmingly used a Western-style given-name/family-name order.

### Non-China-affiliated author rows

Across 518 aligned non-CN rows:

- Crossref family matched some OpenAlex name token: **96.53%**
- Crossref family matched the last token: **96.53%**
- first-token family matches were rare.

## Interpretation

The result materially reduces the surname-measurement problem, but only in the correct direction:

1. **Crossref `author[].family` is promoted to a high-confidence structured surname evidence source** when the work DOI resolves, author lists can be positionally reconciled, and no independent identity evidence conflicts.
2. **The final-token heuristic remains Tier 3 / engineering-only.** Its high agreement here is conditional on modern DOI-bearing works and on Crossref-aligned records.
3. OpenAlex and Crossref author-list disagreement is non-negligible (~4.4% by author count), so positional reconciliation is mandatory rather than assuming index equivalence.
4. The pilot does not address DOI missingness, historical coverage, or OpenAlex person-level split/merge errors.

## Confirmatory evidence rule proposed from Pilot 3

A Crossref-backed surname observation may enter Tier 1B only if:

- OpenAlex work has a DOI that resolves in Crossref;
- OpenAlex and Crossref author counts agree;
- Crossref supplies a non-empty family name for the focal contributor;
- the structured family token is compatible with the OpenAlex raw/display-name evidence at the same list position;
- any available ORCID evidence does not conflict;
- compound/alternative Romanization rules do not create unresolved ambiguity.

Records failing these conditions fall to a lower parser tier or are excluded; they are never silently repaired by assuming the last token is the surname.

## Remaining gate

Pilot 4 must estimate, over multi-author China-affiliated works **without preselecting DOI presence**:

- DOI coverage by field and year;
- Crossref retrieval conditional on DOI;
- strict position-by-position alignment;
- ORCID agreement when both systems supply ORCID;
- lower-bound ORCID-to-OpenAlex ID split/merge inconsistencies.

## Current decision

**Surname evidence route: GO. Population-wide parser gate: still conditional.**
