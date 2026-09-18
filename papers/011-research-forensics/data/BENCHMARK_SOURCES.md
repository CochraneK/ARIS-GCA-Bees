# Benchmark source registry

Status: source feasibility map; no confirmatory sample has been materialised.

| Source | Candidate role | Strength | Main caveat |
|---|---|---|---|
| Crossref Retraction Watch | official/post-publication outcome backbone | open, DOI-linked, updated frequently | retraction reasons are heterogeneous; corrections less comprehensive |
| Publisher notices | issue labels and chronology | primary source for stated reason | reason wording and detail vary |
| PubMed | biomedical metadata/full-text linking | stable identifiers and article types | domain-limited |
| Crossref | DOI metadata and update relations | broad coverage | metadata incompleteness |
| OpenAlex | field/corpus/comparator metadata | broad open graph | must freeze snapshot/version |
| PubPeer public pages | exploratory post-publication evidence | issue-specific observations | not an official misconduct label; bulk access/terms must be respected |
| Existing paper-mill datasets | text detector development/benchmark | direct prior-art comparison | template/family leakage risk |
| Public forensic case studies | deterministic unit tests | known examples | not population-representative |

## Benchmark v0 extraction fields

- paper_id
- DOI
- title
- year
- journal
- article_type
- field
- version/date
- OA/fulltext availability
- notice_type
- notice_date
- source_url
- raw_reason
- controlled_issue_codes
- ground_truth_tier
- known_cluster_id
- author_component_id (derived, optional)
- text_cluster_id
- image_cluster_id
- train/dev/test split
- track_A_eligible
- track_B_eligible

## Critical distinction

Crossref/Retraction Watch records are used to **construct and verify labels**. Their status fields and reason text are not exposed to content-only Track A detectors.
