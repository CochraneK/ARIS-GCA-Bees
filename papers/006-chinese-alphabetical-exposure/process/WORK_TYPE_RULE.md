# ARIS4C006 · Frozen work-type rule

Last updated: 2026-09-18

## Primary work types

The primary author-order mechanism frame and the primary convention-exposure estimator include only OpenAlex works with:

- `type = article`
- `type = conference-paper`

This rule is frozen before focal surname × outcome estimation.

## Rationale

The primary question concerns scholarly byline credit on substantive research papers.

- `article` captures journal research articles.
- `conference-paper` preserves fields such as Computer Science and Engineering where full conference papers are a major scholarly output form.

The two types share a paper-level coauthorship/byline structure sufficiently close to support the common mechanism.

## Excluded from primary

Do not include in the primary convention or focal work frame:

- preprint;
- review;
- data-paper;
- software-paper;
- book;
- book-chapter;
- book-review;
- conference-abstract;
- dissertation;
- editorial;
- erratum;
- letter;
- dataset;
- software;
- report;
- retraction;
- peer-review;
- reference-entry;
- standard;
- supplementary-materials;
- paratext;
- libguides;
- other.

## Secondary sensitivity types

Outcome-blind secondary analyses may separately add:

- `review`;
- `data-paper`;
- `software-paper`.

They must be labeled as sensitivity/extension analyses and cannot replace the frozen primary sample because they produce a stronger surname interaction.

## Duplicate/version rule

Preprints are excluded from primary analysis to avoid mixing a manuscript version with its later published work and to avoid attributing a preprint-repository ordering convention to the final publication context.

Where OpenAlex identifies a published DOI/version relationship, the published primary work is preferred.

## Exposure matching

The prior-3-year primary field convention exposure must be estimated from the **same primary work-type set** used in the focal mechanism frame.

A convention estimate mixing reviews/books/preprints into the primary article/conference-paper exposure is not allowed.

## Work-type drift

OpenAlex may improve type classification over time. The extraction manifest must record:

- extraction date;
- OpenAlex API/schema context;
- observed counts by work type;
- the frozen allowed-type set.

If a future OpenAlex type taxonomy changes, the analysis does not silently substitute new types; it records the change and maps it explicitly.
