# Object-level historical artifact safety

Updated: 2026-09-18

## New finding

Historical safety cannot be represented by one Boolean per paper.

The first successful archival search found a Wayback snapshot of the PLOS ONE target article 10.1371/journal.pone.0161231 from 2022-05-20, almost two years before the 2024 correction. The archived page identifies the original article, DOI and 2016 publication date, exposes the Figure 1 link, and does not display an article-specific correction/retraction status notice.

The Wayback CDX record for that HTML snapshot reports digest:

`SJBUQU4QEVTKRFABLY56LDCTDJJ6B3EL`

However, separate CDX queries for the Figure 1 image endpoints (inline, medium, and original-download forms) returned no pre-correction capture.

## Consequence

The same paper currently has different Track-A status by modality:

| Role | Historical evidence | Status |
|---|---|---|
| body_text | 2022 archived publisher HTML | SAFE_EXACT |
| figure_caption/link | 2022 archived publisher HTML | SAFE_EXACT |
| figure_image | no independently verified pre-correction image object found | BLOCKED |

Therefore the documented Figure-1 panel-switch correction is **not yet eligible for a primary F4 image-forensics test**, even though the article text itself has a valid historical snapshot.

## Benchmark rule

Eligibility is computed at:

**paper × issue × required artifact role**

not simply paper.

Examples:
- a p-value inconsistency may require body_text/table;
- GRIM may require table or textual summary statistics;
- an image-duplication case requires the relevant historical figure-image object;
- a citation-existence check requires the historical reference list;
- a text/paper-mill detector requires the exact historical text version.

If every required role has SAFE_EXACT evidence, the issue is primary Track-A eligible.

If no role is blocked but at least one is available only as a preprint/accepted-manuscript proxy, the issue is PROXY_ONLY.

If any required role lacks an exact/proxy object, the issue is BLOCKED.

## Why this matters

Without object-level qualification, a benchmark can accidentally score an image detector on a corrected image while believing that an old HTML snapshot made the paper historical. The resulting false positive/false negative accounting would be invalid.

## Sources checked

Historical article:
https://web.archive.org/web/20220520171120id_/https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0161231

Wayback CDX searches were performed on 2026-09-18 for:
- the article HTML;
- Figure 1 inline image endpoint;
- Figure 1 medium image endpoint;
- Figure 1 original-download endpoint.

The correction itself is:
https://pmc.ncbi.nlm.nih.gov/articles/PMC10956798/
