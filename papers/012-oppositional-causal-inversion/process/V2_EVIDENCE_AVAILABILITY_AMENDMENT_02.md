# V2 evidence-availability Amendment 02 — deterministic replacements

Frozen decision: 2026-09-19  
Status: **PRE-CODING ONLY**

## Trigger

The first blind packet had 24/30 usable abstract excerpts and six bibliographic-only records. Amendment 01 attempted record-level DOI/landing-page metadata enrichment for exactly those six records and recovered **0/6**.

No A2/B2 coding has started. Therefore an outcome-blind evidence-availability replacement remains permissible.

## Scientific purpose

This 30-record set is an **instrument-reliability validation sample**, not a prevalence sample. Every coder should receive enough record-level evidence to distinguish schema reliability from missing-evidence noise.

Replacement is therefore allowed only for evidence availability and only before either coder starts.

## Frozen replacement rule

Affected sample IDs:

- V215 — conflict_security
- V216, V219 — economic_network_rebound
- V224, V225 — information_attention
- V227 — organization_measurement

For each affected ID, in ascending sample-ID order:

1. reconstruct the original fresh eligible pool by excluding Pilot 0B records exactly as in the frozen sample draw;
2. compute the same FNV-1a score using seed `ARIS4C012-V2-A2B2-20260919`;
3. remain inside the **same retrieval stratum**;
4. exclude all 30 records from the original frozen validation sample and any replacement already accepted;
5. scan remaining candidates in ascending frozen hash score (tie-break original `selection_rank`);
6. attempt the same evidence materialization stack (OpenAlex → Crossref → Semantic Scholar → record-level landing metadata);
7. accept the **first candidate with a non-empty record-level evidence excerpt**;
8. preserve the original sample ID (for example V215) but record old→new bibliographic identity in a non-coder replacement manifest;
9. continue until every affected slot has usable evidence.

The algorithm may not inspect OCI labels, Pilot-0 labels, A2/B2 labels, anticipated result direction, or manuscript usefulness.

## Audit requirements

Persist separately from the coder packet:

- every candidate attempted;
- its deterministic score;
- evidence-availability result;
- accepted/rejected status;
- exact old→new mapping;
- final provider/evidence-source coverage.

The coder packet must continue to hide stratum, query, draw score, provider selection metadata, and all previous labels.

## Gate

A2/B2 may start only if:

- all 30 final records have usable evidence;
- A2/B2 response forms are byte-identical;
- both coder input manifests point to the same final bundle SHA-256;
- the final freeze explicitly supersedes the first packet and Amendment 01;
- no coder labels existed before the replacement mapping was frozen.

Once either independent coder starts, **no further sample replacement is allowed**.
