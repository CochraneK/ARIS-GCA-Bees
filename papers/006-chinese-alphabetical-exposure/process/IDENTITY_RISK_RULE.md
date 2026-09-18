# ARIS4C006 · Frozen longitudinal identity-risk QA rule

Last updated: 2026-09-19

## Scope

This rule applies only to the longitudinal secondary analysis.

The primary work-level H1 uses work-local authorship rows and does not require a complete career reconstruction.

## Hard identity exclusions

A longitudinal author is excluded only for a directly observed identity-integrity failure:

1. embedded OpenAlex author ID cannot be resolved to a current canonical OpenAlex author;
2. available ORCID evidence conflicts with the resolved canonical author and cannot be reconciled;
3. two distinct focal authorships on the same work collapse to the same canonical author ID;
4. longitudinal retrieval returns an internally contradictory entity record that cannot be deterministically reconciled under the frozen rules.

No person is excluded merely because their name is common.

## Required provenance

For every longitudinal author retain:

- canonical OpenAlex author ID;
- original embedded IDs encountered;
- ORCID when available;
- canonicalization status;
- raw authorship-level ORCID consistency status where available.

Names are not used to merge two separate canonical author entities.

## Deterministic diagnostic flags

The following are **risk flags, not primary exclusions**:

### R1 — no ORCID anchor
No ORCID is available on the canonical author record or eligible authorships.

### R2 — extreme annual eligible output
More than **100 eligible article/conference-paper works in any calendar year**.

### R3 — very high annual institutional spread
More than **12 distinct resolved focal-author institution IDs in any calendar year**.

### R4 — very high annual country spread
More than **4 distinct countries among the focal author's own resolved affiliations in any calendar year**.

### R5 — canonical-ID alias history
The author was observed under >=2 embedded OpenAlex author IDs that resolve to the same canonical ID.

This is not itself an error; Pilot 9 showed it is a real OpenAlex merge/alias pattern. It is retained as a sensitivity marker.

### R6 — sparse early identity evidence
Fewer than 2 eligible works in the first 3 observed publication years after cohort entry.

This flag matters for early-exposure measurement and identity confidence but does not redefine cohort entry.

## Low-risk sensitivity subset

The preregistered low-risk longitudinal sensitivity requires:

- no hard identity exclusion;
- R2 = false;
- R3 = false;
- R4 = false.

A stricter ORCID-anchored sensitivity additionally requires:
- R1 = false.

R5 is reported separately rather than automatically excluded because canonicalization explicitly resolves these aliases.

## Outcome-blind QA report before unlock

Before H3 is estimated, report only:

- longitudinal candidates;
- hard exclusions by reason;
- prevalence of R1–R6;
- overlap of flags;
- retained low-risk subset size;
- retained ORCID-anchored subset size;
- counts by entry cohort year.

Do **not** report persistence rates by flag, surname rank, or exposure before preregistration unlock.

## Sensitivity hierarchy after unlock

H3 must be reported for:

1. frozen primary entry cohort after hard identity exclusions;
2. low-risk subset;
3. ORCID-anchored subset where adequately powered.

If H3 appears only in high-risk records, the distal claim is downgraded regardless of nominal significance.

## Interpretation

These flags identify bibliographic entity-resolution risk.

They do not diagnose misconduct, implausible human productivity, nationality, or employment status.
