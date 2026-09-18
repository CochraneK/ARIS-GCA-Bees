# Pilot 1B — real-world table semantics and archive discovery

Updated: 2026-09-18

## What changed

The first correction stress case exposed a detector-design error.

The official erratum for DOI `10.1177/1758573221989669` states that the **article information for number 14** in Table 1 was missing. The problem is therefore not necessarily a missing rank label. A simple rank-sequence check can pass while a scientifically meaningful table cell is empty.

ARIS4C011 now distinguishes:

- **rank_sequence** — are expected row keys present and unique?
- **row_completeness** — does every row contain all prespecified required fields?

This distinction was derived from a real correction case rather than invented from a synthetic taxonomy.

## Retrieval audit

### Current PMC HTML

The current PMC representation of the article explicitly states that the article has been corrected, and Table 1 now contains information for rank 14. It is therefore **BLOCKED_CURRENT** for primary Track A.

### Current PMC PDF

The current PMC PDF is a separate object. It does not itself display a correction banner in the parsed PDF, but it was retrieved after the erratum and has not yet been proven byte- or content-equivalent to the pre-erratum PDF. It therefore remains **BLOCKED_UNTIL_EQUIVALENCE_VERIFIED**.

### Wayback

No pre-erratum capture was found with the first canonical PMC URL query. This is a negative discovery result only, not evidence that no historical copy exists anywhere.

## PLOS SAFE_EXACT smoke-test consequence

The verified 2022 Wayback HTML for DOI `10.1371/journal.pone.0161231` is SAFE_EXACT for body text. A targeted extraction found no t/F/chi-square/z result containing enough statistic + degrees-of-freedom information for deterministic F1 recomputation, and no fully specified integer-scale mean eligible for GRIM.

Correct behavior is therefore **ABSTAIN / not applicable**, not forced scoring.

## New archive utility

`code/wayback_discovery.py` builds CDX queries, parses returned capture records, and filters strictly to status-200 captures before the outcome date.

Important: CDX discovery is not qualification. Every discovered object must still pass content/version verification and the artifact-safety gate.

## Scientific implication

Pilot progress is now reported as a funnel:

1. labelled issue exists;
2. candidate historical object discovered;
3. object verified as SAFE_EXACT / PROXY_ONLY / BLOCKED;
4. detector applicable;
5. detector emits PASS / FLAG / ABSTAIN;
6. human verification adjudicates any flag.

This prevents archive failure, extraction failure, and detector failure from being collapsed into one false-negative count.
