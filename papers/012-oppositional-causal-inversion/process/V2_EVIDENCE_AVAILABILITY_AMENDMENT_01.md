# V2 evidence-availability Amendment 01 — ARIS4C012

Frozen decision: 2026-09-19

## Why an amendment is needed

The first immutable blind-packet materialization successfully preserved blinding and byte-identical A2/B2 inputs, but it produced:

- 24 records with abstract excerpts;
- 6 records with bibliographic metadata only;
- `ready_for_independent_coding = false`.

Starting A2/B2 on that packet would confound construct reliability with unequal evidence availability.

## Allowed amendment

Before either independent coder starts, enrich **only** the six records whose packet state is `BIBLIOGRAPHIC_ONLY`:

- V215
- V216
- V219
- V224
- V225
- V227

Allowed sources are public DOI/record landing-page metadata fields such as:

- `citation_abstract`;
- Dublin Core description/abstract;
- JSON-LD `abstract` / record description;
- equivalent record-level HTML metadata.

Evidence is capped at the same 180-word ceiling as the first packet.

## What is forbidden

This amendment must not:

- inspect A2/B2 labels (none exist yet);
- inspect Pilot-0 coder labels for these records;
- inspect Pilot-0 disagreement/adjudication material to choose evidence;
- change Schema v2;
- change the 30-record sample;
- expose retrieval stratum/query/draw metadata;
- overwrite the first packet or its hashes.

The amended bundle must have its own new hash and explicitly reference the superseded bundle hash.

## Decision rule

If all six records gain usable record-level evidence, Amendment 01 may become the operative A2/B2 input bundle.

If any remain bibliographic-only, **do not start coding**. The next permissible action is a separately frozen, outcome-blind deterministic replacement rule using the next evidence-materializable candidate(s) from the same retrieval stratum. Replacement must be driven by evidence availability only, before any new labels exist.
