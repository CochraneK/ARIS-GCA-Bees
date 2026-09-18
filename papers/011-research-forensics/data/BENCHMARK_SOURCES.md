# Benchmark source registry

Status: source anatomy validated against live Crossref production API; no confirmatory sample has yet been frozen.

| Source | Candidate role | Strength | Main caveat |
|---|---|---|---|
| Crossref Retraction Watch | update assertion / post-publication outcome backbone | open, DOI-linked, updated every working day | update query can return notice works; top-level DOI/title are not necessarily the affected article |
| Retraction Watch CSV | reason text / record-id enrichment | open linked record IDs and richer retraction details | retraction reasons are heterogeneous; correction coverage is less comprehensive |
| Publisher notices | issue labels and chronology | primary source for stated reason | wording/detail vary and notices can be incomplete |
| PubMed | biomedical metadata/full-text linking | stable identifiers and article types | domain-limited |
| Crossref | target DOI metadata and update relations | broad coverage | metadata incompleteness and inconsistent relation patterns |
| OpenAlex | field/corpus/comparator metadata | broad open graph | must freeze snapshot/version |
| PubPeer public pages | exploratory post-publication evidence | issue-specific observations | not an official misconduct label; bulk access/terms must be respected |
| Existing paper-mill datasets | text detector development/benchmark | direct prior-art comparison | template/family leakage risk |
| Public forensic case studies | deterministic unit tests | known examples | not population-representative |

## Source anatomy discovered in live production data

A Crossref query filtered by `update-type:retraction` returns works containing `update-to` relations.

The top-level work may be:
1. a separate retraction notice DOI whose `update-to[].DOI` is the affected article; or
2. the affected article itself with a self-relation.

The same event may be asserted by both `publisher` and `retraction-watch`.

Therefore Benchmark v0 stores **assertions** separately from **events**, and resolves target-paper metadata only from `target_doi`. Source-work title/year/journal are never silently copied onto the target paper.

## Stage A — update assertion fields

- assertion_key
- event_key
- crossref_source_work_doi
- notice_doi
- target_doi
- relation_type
- relation_label
- assertion_source
- update_date
- retraction_watch_record_id
- source_work_title
- source_work_journal
- source_work_published
- target_metadata_resolved

## Stage B — target paper / adjudication fields

- paper_id
- target_doi
- target_title
- target_year
- target_journal
- article_type
- field
- version/date
- OA/fulltext availability
- event_key
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

## Critical distinctions

Crossref/Retraction Watch records are used to **construct and verify labels**. Their status fields, record IDs, notice titles, dates, and reason text are not exposed to content-only Track A detectors.

A retraction is an update status, not automatically a misconduct label. Ground-truth issue coding remains separate from update ingestion.
