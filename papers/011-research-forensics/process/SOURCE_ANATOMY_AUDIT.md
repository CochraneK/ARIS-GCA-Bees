# Source-anatomy audit — Benchmark v0

Updated: 2026-09-18

## Finding 1 — update-query work != target work

Crossref update queries can return a retraction-notice work whose `update-to[].DOI` points to the affected paper. Some records instead use a self-relation.

Consequence:
Never treat the top-level DOI/title from an update query as target-paper metadata without resolving `target_doi`.

## Finding 2 — one event can have multiple assertions

The same target/update event may be asserted independently in Crossref metadata by:
- `publisher`;
- `retraction-watch`.

Consequence:
Keep assertion provenance rows and event rows separately. Event deduplication must not erase source provenance.

## Finding 3 — current target metadata can leak future outcomes

Live Crossref target records can contain titles such as:
- `RETRACTED: ...`
- `RETRACTED ARTICLE: ...`

They also contain `updated-by` relations describing retraction status.

Consequence:
"Resolve the target DOI" is not sufficient for Track A. Current metadata is post-outcome metadata.

Track A therefore requires:
1. an explicit field allow-list;
2. removal of post-publication status text;
3. historical validation when a title had to be sanitised;
4. a clean manuscript/document artifact without publisher-added retraction banners/notices;
5. no raw DOI, journal, year, author, affiliation, notice, or outcome metadata as primary model features.

## Finding 4 — retraction is not an issue taxonomy

The first three real seed cases already include:
- nonspecific scientific-accuracy/legitimacy concerns;
- illegal gift authorship;
- compromised editorial process / manipulated peer review.

These are not interchangeable ground-truth labels.

Consequence:
Retraction status is an **outcome/source event**, not the target forensic issue class.

## Finding 5 — some official issues are not content-detectable

Gift authorship or peer-review manipulation can be established by editorial/institutional evidence while leaving no necessary textual/statistical/image signature in the published manuscript.

Consequence:
Primary scoring conditions on detector eligibility. Overall coverage is reported separately so the framework is still penalised for narrow applicability without pretending that an impossible content-only task is a false negative.

## Track A contamination preflight

Before a paper enters Track A, fail closed if any of the following occurs:
- title contains explicit retraction/withdrawal/EoC markers;
- extracted PDF/HTML contains a retraction notice or publisher banner that postdates publication;
- metadata includes outcome labels in model-visible fields;
- a later corrected/retracted version is supplied where a pre-outcome version was intended;
- filename/path contains class labels such as `retracted`, `fraud`, or issue type;
- document retrieval happened after outcome and historical equivalence cannot be established.

Such papers remain valid for Track B and for source-adjudication analyses.
