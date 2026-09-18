# ARIS4C015 Data Contract

## Purpose

This contract prevents a Sleeping Beauty discovery system from silently using incomplete citation histories or future information.

## Required identifiers

Each paper record should preserve, where available:

- source-native paper ID;
- OpenAlex ID;
- DOI;
- PMID;
- publication year;
- source snapshot/version;
- retrieval date.

Do not merge records solely on title similarity when a persistent identifier is available.

## Citation history

A complete annual history is defined as a zero-filled vector indexed by paper age.

For target paper p published in year y0:

```text
c_t = number of citing works published in year y0 + t
```

Requirements:

1. derive incoming citations from citation edges or a source with equivalent complete annual coverage;
2. join citing works to publication year;
3. insert years with zero citations;
4. preserve pre-publication citation anomalies separately;
5. record the observation endpoint;
6. document whether the history is complete, bounded, or sampled.

A bounded OpenAlex retrieval may be used for plumbing tests but not as a complete confirmatory trajectory if the cap truncates incoming citations.

## Historical-cutoff safety

For prospective cutoff T, every feature requires an availability claim.

Possible states:

- SAFE — demonstrably available <= T;
- PROXY — reconstructed approximation with explicit assumptions;
- BLOCKED — known future contamination or impossible historical reconstruction;
- UNKNOWN — availability cannot be established.

Default rule:

**UNKNOWN is excluded from the prospective model when it could leak outcome information.**

## Semantic features

A semantic embedding can leak future structure if trained or normalized against a corpus that contains post-cutoff literature.

For confirmatory historical backtests, one of these is required:

1. embeddings generated from text alone with a frozen model whose representation does not encode post-cutoff graph outcomes; or
2. embeddings/models reconstructed for the historical corpus state; or
3. a prespecified sensitivity analysis showing that the modern embedding does not materially encode the target future outcome.

Modern embeddings may be used for exploratory discovery but must be labeled as such.

## Network features

At cutoff T:

- citation edges must have citing-work date <= T;
- co-citation and bibliographic coupling must use only edges visible by T;
- community assignments should be rebuilt from the cutoff graph when they affect prediction;
- future centrality cannot be backfilled into old papers.

## Patent and technology linkage

A patent citation is available only from its historically appropriate date.

Later patent linkages are outcomes, not prospective features.

## Integrity data from ARIS4C011

Each imported finding should preserve:

- finding_id;
- detector_id/version;
- family;
- applicability;
- status;
- evidence_class;
- dependency_group when available;
- reproducibility;
- provenance/source locator;
- benign explanations;
- timestamp or availability year.

If availability time is unknown in a prospective benchmark, do not expose the finding to the model.

## Prestige and identity variables

The following must not be used as intrinsic-value predictors:

- institution prestige;
- author fame;
- country/nationality;
- journal prestige;
- language background.

They may be retained in a protected audit table for bias/shortcut diagnosis.

## Source-specific notes

### OpenAlex

Use for IDs, live metadata, references, topics, and bounded citation retrieval.

Do not assume `counts_by_year` is a complete lifetime history. For long-lived papers reconstruct yearly citations from incoming citation edges and citing-paper years.

### SciSciNet-v2

Preferred large-scale backbone when access and storage permit.

The adapter in ARIS4C015 intentionally accepts local slices and configurable column mappings rather than hard-coding unverified column names.

Record:

- dataset release/snapshot;
- exact source file/table;
- query/export used to create the slice;
- row counts before/after filters;
- column mapping;
- checksums where feasible.

## Minimum provenance record

Every empirical artifact should include:

```text
source_name
source_release_or_snapshot
retrieval_date
source_table_or_endpoint
query_or_filter
identifier_mapping
cutoff_year
field_stratum
coverage_limitations
code_commit
```

## Synthetic fixtures

Synthetic data may be used for tests and demos only.

It must be labeled SYNTHETIC and cannot be presented as evidence that the prospective miner works empirically.
