# ARIS4C006 · Frozen final convention-sampling rule

Last updated: 2026-09-19

## Purpose

Materialize the outcome-blind field-level alphabetical-authorship convention evidence used to construct the primary lagged LOAO exposure.

No focal surname rank, listed-position outcome, first-author outcome, or persistence outcome is read during this stage.

## Context

Primary convention context:

**OpenAlex `primary_topic.field.id` × calendar year**

Annual evidence is later aggregated into the frozen **prior 3 complete years** for each focal year 2011–2025.

Convention source years therefore span:

**2008–2024**

## Eligible works

A convention work must:

1. have at least one CN-affiliated authorship;
2. have the focal primary-topic field;
3. be OpenAlex type `article` or `conference-paper`;
4. have at least 2 listed authors;
5. have fewer than 100 OpenAlex authorships;
6. have a DOI resolving in Crossref;
7. have matching OpenAlex/Crossref contributor counts;
8. have a non-empty structured Crossref `family` value for every listed contributor.

Works with 100 OpenAlex authorships are excluded because the OpenAlex authorship component is capped at the first 100 authors and completeness cannot be guaranteed.

## Reproducible annual sampling

For each field/year:

- draw reproducible OpenAlex random blocks of up to **100 works**;
- block seeds are deterministic functions of paper ID, field ID, year, and block number;
- deduplicate by OpenAlex work ID across blocks;
- process blocks in numerical seed order;
- never inspect a surname-effect or career outcome while deciding to continue sampling.

## Prospective information target

For each valid convention work:

`num_w = I_alpha_w - p_chance_w`

`den_w = 1 - p_chance_w`

where:

`p_chance_w = prod_j(m_j!)/n_w!`

with family-name tie groups `m_j`.

Annual sampling stops after a completed random block when both hold:

- all multi-author effective information `D_year = sum den_w >= 35`;
- 3+ author effective information `D3_year >= 20`.

Maximum:
- **4 random blocks per field/year**.

Failure to meet the annual target is recorded; it does not trigger adaptive surname/outcome analysis.

## Rolling primary exposure

For focal year `t`:

- combine annual work contributions from `t-3, t-2, t-1`;
- calculate field-window `N_ct, D_ct`;
- full descriptive exposure `E_ct = N_ct/D_ct`.

The primary focal-author exposure later applies exact LOAO subtraction:

`E^{-i}_{ct} = (N_ct-N_ict)/(D_ct-D_ict)`

and requires:

`D_ct-D_ict >= 50`.

3+ author convention exposure is mandatory robustness and is constructed analogously.

## Author canonicalization

Each accepted convention work stores the canonical OpenAlex author IDs needed for later LOAO subtraction.

Engineering rule:

1. collect unique embedded author IDs;
2. use OpenAlex author-list OR batching with up to 100 IDs where supported;
3. raw IDs returned unchanged by the batch map to themselves;
4. raw IDs absent from the batch return are resolved by singleton `/authors/{raw_id}`;
5. preserve work-level author membership after canonicalization;
6. deduplicate an author within a work before later LOAO subtraction.

The batch contract was verified outcome-blind in `code/21_openalex_author_batch_contract.py`.

## Outputs

Per field:
- annual convention summary, 2008–2024;
- rolling field exposure summary, focal 2011–2025;
- work-level convention contributions with canonical author membership;
- measurement manifest.

Global aggregation:
- coverage/information summary across all 26 fields;
- no H1/H2/H3 coefficients.

## Stop / narrow rule

If a rolling field-year has `D_ct < 50`, it cannot supply primary exposure.

No unsupported context is rescued by:
- using source-level exposure;
- changing field assignment;
- adding reviews/preprints/books;
- lowering surname-validation rules;
- increasing sample blocks after observing focal effects.

Sampling targets may only be revised before focal outcomes if this outcome-blind materialization demonstrates widespread measurement failure and the revision is documented as a protocol amendment.
