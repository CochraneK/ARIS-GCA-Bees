# Initial public-data source catalogue

Snapshot: 2026-09-18.

This file records source roles and caveats. It is not a claim that every source can be redistributed under the same licence.

## 1. Open Contracting Data Standard (OCDS)

Role:
- canonical procurement lifecycle schema;
- planning, tender, award, contract, implementation fields;
- cross-jurisdiction normalization.

Reference:
https://standard.open-contracting.org/latest/en/

Open Contracting Partnership reports implementations by more than 50 governments and publishes a 2024 red-flags guide with 73 procurement-risk indicators.

Reference:
https://www.open-contracting.org/resources/red-flags-in-public-procurement-a-guide-to-using-data-to-detect-and-mitigate-risks/

Use in 014:
make OCDS-like records the preferred canonical contract interface even when national adapters are required.

## 2. USAspending

Role:
- US federal awards/contracts/grants and recipient/agency information.

API:
https://api.usaspending.gov/

Caveat:
federal spending transparency is not identical to a full tender/bidding record. Applicability routing must know which procurement-process fields are absent.

## 3. EU TED

Role:
- EU procurement notices;
- published notice search and bulk reuse;
- linked open data / SPARQL.

API:
https://docs.ted.europa.eu/api/latest/
https://data.ted.europa.eu/

Current TED Search API allows retrieval of published notices for analysis and reuse and does not require authentication for published-notice search.

## 4. UK Companies House Public Data API

Role:
- companies;
- officers;
- persons with significant control (PSC);
- corporate/legal-person beneficial owner endpoints.

Reference:
https://developer-specs.company-information.service.gov.uk/companies-house-public-data-api/reference

Use:
entity resolution and ownership/control graph.

Caveat:
protective/redaction regimes and historical validity must be respected. Current PSC state cannot automatically stand in for historical ownership.

## 5. Open Ownership / BODS

Role:
- standardized beneficial-ownership data model;
- cross-source ownership analysis;
- downloadable analysis datasets where available.

References:
https://www.openownership.org/en/topics/beneficial-ownership-data-standard/
https://www.openownership.org/en/publications/beneficial-ownership-data-analysis-tools/user-guidance/

The analysis tools currently document national data including Denmark, Slovakia, and the UK among available datasets.

## 6. World Bank ineligible firms and individuals

Role:
- externally verifiable debarment / cross-debarment facts.

Reference:
https://www.worldbank.org/en/Projects-operations/procurement/debarred-firms

The World Bank page reports that its list is updated every three hours.

Leakage rule:
for Track A, a sanction imposed after the target cutoff is outcome-side information, not a feature.

## 7. ICIJ Offshore Leaks Database

Role:
- offshore entity/person/company relationship graph from major leak investigations.

References:
https://offshoreleaks.icij.org/
https://offshoreleaks.icij.org/pages/database

ICIJ makes downloadable node/relationship CSVs and Neo4j exports available and states that the database covers more than 810,000 offshore entities.

Critical caveat:
ICIJ explicitly warns that offshore entities can have legitimate uses and that same/similar names require identity confirmation. OpenIntegrity adopts this as a hard design rule.

## 8. OpenSanctions

Role:
- PEP/public-office, sanctions, related entities, identifiers, relationship enrichment.

References:
https://www.opensanctions.org/docs/
https://www.opensanctions.org/datasets/peps/

Licence/access note:
OpenSanctions documentation states free use for non-commercial users and requires a licence for commercial use. Do not assume unrestricted redistribution.

Design note:
PEP status is context, not adverse evidence. Prefer exact identifiers and occupancy dates; name-only candidate matches should abstain from high-priority inference.

## 9. OCCRP Aleph Pro — optional investigator source

Reference:
https://aleph.occrp.org/

Role:
- investigative research archive aggregating government records, databases, documents, and leaks.

Access caveat:
Aleph Pro requires an application/approval process. Therefore it cannot be a required dependency for the open core or benchmark reproducibility.

## Source-adapter contract

Each adapter should emit:

- source_name;
- source_record_id;
- source_url;
- retrieved_at;
- published_at if known;
- valid_from / valid_to if known;
- jurisdiction;
- licence/access note;
- raw checksum or immutable snapshot reference;
- canonical entities/relations produced;
- parser version.

## Source hierarchy

Prefer:
1. official structured record;
2. official unstructured record;
3. reputable public-interest structured dataset with provenance;
4. investigative reporting with cited documents;
5. unsourced web claims — excluded from evidence graph.

A lower-tier source can guide search but should not silently overwrite a higher-tier record.
