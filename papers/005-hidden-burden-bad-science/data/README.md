# Data — ARIS4C005

This directory stores **open, derived, or synthetic/scenario artifacts only** unless a source explicitly permits redistribution.

## Current files

### `numeric_evidence.csv`

Atomic numeric evidence ledger. Every row records:

- claim and value;
- unit;
- period and denominator/population;
- source + DOI/URL;
- PuddingSkill-style claim status (`VERIFIED`, `QUALIFIED`, etc.);
- confidence;
- observed vs modelled status;
- interpretation boundary.

This is the canonical starting point for factual numbers used in the project narrative.

### `scenario_parameters.example.json`

**Illustrative only.** Parameters exist to test the Fermi/scenario engine and vivid unit conversions. They are not empirical estimates and must never be merged into `numeric_evidence.csv`.

## Planned derived files

```text
openalex_universe_counts.csv
openalex_universe_provenance.json
crossref_coverage_audit.csv
retraction_events_derived.csv
retraction_reason_codebook.csv
universe_coverage.csv
correction_match_audit.csv
citation_context_gold.csv
```

Large Parquet/model files may live outside Git depending on size.

## Raw data policy

Do not commit:

- copyrighted full text;
- restricted publisher data;
- third-party annotations whose terms prohibit redistribution;
- personal/sensitive researcher investigation material;
- raw datasets whose license requires access through the original provider.

Instead commit:

- identifiers;
- source/version dates;
- exact query/filter recipes;
- checksums where useful;
- derived non-identifying features where allowed;
- scripts that can rehydrate the data lawfully.

## Current primary external data targets

- OpenAlex core works snapshot/API;
- Crossref metadata;
- Retraction Watch via Crossref/GitLab;
- NIH iCite/OCC biomedical subset;
- NIH RePORTER funding links;
- ClinicalTrials.gov / AACT clinical subset;
- Scite literature/citation-context evidence where permitted.

## Tool availability log

At project initialization (2026-09-18):

- Scite literature search/read tools: available;
- Scite Collection creation: attempted, returned payment-required (HTTP 402); nonessential;
- Elicit API: attempted, returned `api_access_denied` for current plan; nonessential;
- web access to official public documentation: available.

The pipeline must remain reproducible without paid optional research-assistant features.
