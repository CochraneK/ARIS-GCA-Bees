# ARIS4C006 · Pilot 7 — ORCID/OpenAlex identity consistency

Last updated: 2026-09-18

## Verdict

**Person-level identity gate: FAILS as a naive raw-ID join; canonicalization follow-up required.**

GitHub Actions run: `35298170831`  
Artifact: `aris4c006-identity-orcid-pilot`

This pilot directly compared:
- the OpenAlex author ID embedded in sampled work authorships; and
- the current OpenAlex author resolved from that authorship's ORCID using the official ORCID author lookup.

No focal surname-effect or career outcome was used.

## Design

- Years: 2020 and 2024
- Fields: Economics, Mathematics, Business, Psychology, Medicine, Engineering
- Reproducible OpenAlex random samples
- 25 multi-author works requested per field/year cell
- China-affiliated authorships with ORCID used for the identity check
- Crossref family name used only to stratify the diagnostic by early/middle/late alphabet bands when positional reconciliation was available
- Aggregate-only output

## Result

- unique ORCID lookups attempted/resolved: **968**
- resolved authorship checks: **977**
- raw authorship author-ID vs ORCID-resolved OpenAlex ID mismatches: **61**
- raw mismatch rate: **6.24%**
- OpenAlex author IDs observed with >1 ORCID in the sampled works: **0** (lower-bound diagnostic only)

## Alphabet-band diagnostic

Aggregating across field/year cells:

| Initial band | Resolved checks | Mismatches | Raw mismatch rate |
|---|---:|---:|---:|
| A–I | 198 | 10 | **5.05%** |
| J–R | 274 | 17 | **6.20%** |
| S–Z | 455 | 30 | **6.59%** |
| Unknown structured family | 50 | 4 | **8.00%** |

The late-initial band is not dramatically worse than the early/middle bands in this pilot, but the overall raw mismatch rate is far too large to ignore.

## Interpretation

A longitudinal pipeline must **not** assume that the author ID embedded in every work is already the current canonical OpenAlex person ID.

One plausible explanation is OpenAlex author merging / entity updates: historical or embedded work records may retain IDs that resolve to a newer canonical author entity. That hypothesis is now being tested in Pilot 8/9 by re-resolving each mismatched embedded author ID before classifying it as a substantive identity conflict.

## Immediate rule

Until the follow-up passes:

- raw work-level author IDs are acceptable for the work-local authorship observation itself;
- they are **not** trusted as the sole key for stitching long-horizon career histories;
- distal career models remain locked;
- ORCID-linked robustness cannot be treated as automatically clean without canonical author resolution.

## Differential-error interpretation

The observed band-level rates do not show a simple strong monotonic increase from early to late initials, which is mildly reassuring.

However:
- the pilot was not powered as an equivalence test;
- exact surname frequency was not available for every row;
- field/year composition differs by band.

Therefore the identity gate cannot be cleared from this comparison alone.

## Next gate

Re-run the deterministic sample and, for every raw mismatch:

1. fetch the embedded OpenAlex author ID directly;
2. record the canonical ID returned by OpenAlex;
3. compare that canonical ID / ORCID against the ORCID-resolved author;
4. classify mismatch as:
   - repaired by canonicalization,
   - unresolved identity conflict,
   - failed lookup.

The longitudinal identity rule will be frozen only after that reconciliation.
