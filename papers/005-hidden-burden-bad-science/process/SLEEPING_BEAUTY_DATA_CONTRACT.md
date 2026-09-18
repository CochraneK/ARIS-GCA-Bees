# SLEEPING BEAUTY DATA CONTRACT — ARIS4C005

## Purpose

Freeze the distinction between historical delayed-recognition measurement, prospective awakening prediction, and causal suppression analysis.

## SB0 historical citation-history table

One row per paper × calendar year.

Required:

- paper_id
- openalex_id
- publication_year
- citation_year
- citations

Rules:

- citation_year >= publication_year;
- missing years inside the observation window are explicit zeros only when the bibliographic query establishes complete year coverage;
- observation end year must be stored or reconstructable;
- annual citation counts are database-version dependent and need retrieval provenance.

## SB0 derived metrics

Required derived fields:

- Beauty Coefficient B
- citation peak age t_m
- awakening age t_a
- awakening year
- total observed citations
- observation-window length

Primary variable is continuous B. Any top-percentile flag is dataset-relative.

## SB1 landmark dataset

One row per paper at a frozen landmark age L.

Required keys:

- paper_id
- publication_year
- landmark_age
- landmark_calendar_year
- followup_end_year

Allowed features use information observed by landmark only:

- cumulative citations through L;
- annual citation trajectory through L;
- semantic novelty from title/abstract/publications available by L;
- topic growth through L;
- interdisciplinarity/cognitive-distance features through L;
- author/network position through L;
- OA/access features through L.

Targets are defined after landmark:

- awakening within H years;
- awakening time with right censoring;
- future B or B percentile only as an outcome, never as an input.

## Censoring

A paper without observed awakening is not a negative unless it has sufficient mature follow-up for the pre-specified horizon.

Record:

- event observed yes/no;
- event time if observed;
- censor time;
- reason for missing citation history.

## SB2 integrity-exposure table

Exposure variables must be temporally aligned to or before the recognition-risk period.

Possible fields:

- semantic distance to adjudicated E1-S sources;
- materially dependent contamination-path exposure;
- topic-level integrity shock date;
- attention/funding displacement exposure;
- source-centrality-weighted contamination exposure.

Exposure construction may not use future awakening information.

## SB3 suppressed-opportunity output

Only after SB1 prediction calibration and SB2 causal/exposure identification pass:

- observed awakening probability;
- counterfactual low/no-exposure awakening probability;
- individual probability difference;
- summed estimated delayed-recognition opportunities suppressed;
- uncertainty interval.

Do not publish a point count without uncertainty and calibration diagnostics.

## Provenance

Persist database, retrieval date, query, citation-count method, corpus mode, and code version for every citation-history batch.


## OpenAlex historical-citation rule

Do **not** use the nested Work `counts_by_year` field to reconstruct mature historical citation trajectories: current OpenAlex documentation states that Work-level `counts_by_year` contains only roughly the last ten years and omits older citation years.

For SB0 historical Beauty Coefficient estimation, reconstruct annual incoming-citation counts using a live Works query for each source:

`filter=cites:<WORK_ID>&group_by=publication_year`

Then fill unreturned calendar years inside the frozen observation window as zero only after the live query establishes the grouped history.

The live-citation query, retrieval date, and final complete observation year must be stored because citation matching and OpenAlex graph coverage can change over time.
