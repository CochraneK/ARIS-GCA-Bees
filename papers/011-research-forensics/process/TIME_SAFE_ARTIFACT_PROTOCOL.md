# Time-safe artifact protocol — Track A

Updated: 2026-09-18

## Why this gate exists

A retrospective integrity benchmark can leak the future outcome even after obvious label columns are deleted.

Examples:
- current metadata can acquire update relations or status-prefixed titles after retraction;
- publishers may directly modify original HTML/PDF after a correction;
- current article pages can contain correction/retraction banners;
- benchmark filenames or directories can encode the class label;
- a corrected figure/table can silently replace the erroneous object a detector is supposed to find.

Therefore Track A is defined by artifact time and version provenance, not merely by which database columns are passed to a model.

## Three qualification states

### SAFE_EXACT

Eligible for the primary Track A benchmark.

Requirements:
- artifact version demonstrably predates the update/outcome;
- immutable version or independently verifiable historical snapshot;
- same published version, publisher-original snapshot, or equivalent preserved original;
- no post-publication status marker in title/banner/path;
- provenance source recorded.

### PROXY_ONLY

Not eligible for the primary confirmatory Track A, but eligible for a prespecified sensitivity analysis.

Examples:
- versioned preprint posted before the outcome;
- accepted author manuscript deposited before the outcome.

Reason: a proxy may differ from the final publication in exactly the statistic, figure, table, or wording under forensic review.

### BLOCKED

Not usable for Track A.

Examples:
- current publisher HTML/PDF known to have been corrected in place;
- artifact version is on/after the correction/retraction date;
- status marker such as RETRACTED or a correction banner is present;
- dataset path contains the outcome label;
- provenance/version date is unknown;
- historical equivalence cannot be established.

Blocked artifacts remain eligible for Track B when otherwise lawful and useful.

## Source-specific implications

### Nature portfolio

Nature-family correction policies state that, in the majority of corrections, original HTML and PDF versions are corrected and linked to the amendment. Therefore a current Nature article should not be presumed historical-equivalent after an amendment.

Policy example:
https://www.nature.com/commsbio/editorial-policies/correction-and-retraction-policy

### PLOS

PLOS states that corrections are generally linked as post-publication notices and that, in rare cases, a corrected version may replace the original online version. Therefore PLOS artifacts require case-level version verification rather than a publisher-wide assumption.

Policy:
https://journals.plos.org/plosone/s/corrections-and-retractions

### PubMed Central

PMC requires structured correction notices and explicitly preserves original articles when a work is corrected and republished. This makes PMC valuable for provenance, but ordinary correction handling still needs article-level verification.

Policy:
https://pmc.ncbi.nlm.nih.gov/about/guidelines/

### Versioned preprint servers

bioRxiv supports version-specific URLs and retains a citable version history. A pre-outcome version is useful as a proxy artifact, but it is not assumed to be identical to the final journal version.

Policy:
https://www.biorxiv.org/about-biorxiv

## Confirmatory rules

1. Primary Track A statistics are computed only on SAFE_EXACT artifacts.
2. PROXY_ONLY results are reported separately.
3. BLOCKED cases are not counted as detector false negatives.
4. Coverage reports the loss of benchmark scope caused by missing historical artifacts.
5. The reason for every exclusion is retained; attrition is itself a study result.
6. A detector may not see current update metadata in Track A even when a separate historical PDF is SAFE_EXACT.
7. Original artifact bytes or stable hashes should be frozen before confirmatory scoring whenever licensing permits.

## Planned attrition reporting

For each benchmark issue family report:
- labelled issues;
- full-text availability;
- historical version date known;
- exact historical equivalence established;
- proxy-only available;
- blocked due to contamination;
- blocked due to missing provenance;
- final SAFE_EXACT denominator.

This prevents an apparently strong detector result from hiding that only an easy subset of the labelled literature had usable historical artifacts.
