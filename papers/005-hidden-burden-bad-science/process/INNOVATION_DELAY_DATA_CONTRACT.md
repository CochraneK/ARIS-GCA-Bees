# INNOVATION DELAY DATA CONTRACT — ARIS4C005

## Purpose

Freeze the data boundary between source selection, pre-shock neighborhood construction, matching, panel construction, and event-study estimation.

## Source table

Required:

- source_id
- source_openalex_id
- source_doi if available
- event_date
- event_type
- exposure_family
- adjudication_provenance

Final confirmatory treated sources should come from adjudicated E1-S or another explicitly frozen exposure class.

## Pre-shock neighborhood candidates

Candidate neighbors may use only information available at or before the event date.

Allowed:

- source title/abstract;
- source topics/field metadata;
- candidate publication date before event;
- pre-event semantic similarity;
- pre-event citation/reference network structure;
- pre-event author/topic/funding history.

Forbidden for selecting neighbors or controls:

- post-event citation counts;
- post-event publication volume;
- post-event funding;
- later retraction status as a matching feature;
- post-event author entry/exit;
- outcomes the event study is trying to estimate.

OpenAlex semantic search is permitted as a candidate-discovery layer because the query is built from source text and candidates are filtered to pre-event publications. The embedding service/version must be recorded because semantic ranking can change over time.

## Matched-set table

Every final matched set needs:

- matched_set_id
- one treated topic-neighborhood unit or a frozen treated aggregate;
- one or more controls;
- event_year copied to controls as a pseudo-event year;
- matching feature snapshot date;
- matching algorithm/version;
- pre-shock balance diagnostics.

Controls must not be chosen using post-event outcomes.

## Panel table

One row per matched_set × unit × calendar year.

Required keys:

- matched_set_id
- unit_id
- treated
- event_year
- year
- event_time

Outcome columns can include:

- outcome_articles
- outcome_new_authors
- outcome_funding
- outcome_citations

## Missingness

Missing outcome cells are not zeros unless the upstream database query establishes a true zero count.

Missing funding coverage is especially likely to be informative and must be distinguished from zero funding.

## Current OpenAlex implementation note

OpenAlex currently exposes semantic search and algorithmically related works. For confirmatory matching, ARIS4C005 prefers pre-event semantic search constrained to pre-event candidate publications rather than current `related_works`, because current related-work ranking can encode changing corpus/algorithm behavior.

## Reproducibility

Persist:

- exact OpenAlex query;
- query/retrieval date;
- semantic query text hash;
- API corpus (`core` primary);
- candidate rank/relevance score;
- event cutoff date;
- source metadata snapshot used to create the query.
