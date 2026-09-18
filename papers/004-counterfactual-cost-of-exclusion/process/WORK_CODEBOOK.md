# WORK-LEVEL CODEBOOK — ARIS4C004

Date frozen for pilot: 2026-09-18

## Purpose

Identity verification answers **who the person is**. It does not guarantee that every work attached to an accepted OpenAlex Author ID belongs to that person or represents an independent historical knowledge contribution.

This codebook is frozen before work-level cleanup is used to change `network_observable` or any mental-health exposure is examined.

## Unit of analysis

The preferred network unit is an **intellectual work / historical publication event**, not every database manifestation.

One book split into frontmatter, contents, acknowledgments, and chapter records must not automatically become many independent contributions. Likewise, a modern reprint of an older work is not treated as a new original contribution merely because OpenAlex assigns the reprint's modern date.

Raw OpenAlex records are always retained separately from the cleaned analytical work layer.

## Mechanical pre-review rules

These operations are allowed before manual relevance review:

1. preserve `person_id`, accepted source Author ID, OpenAlex Work ID, DOI, title, publication year and topic;
2. flag whether publication year falls inside the candidate-specific permissive window `birth+15 ... death+5`;
3. deduplicate exact normalized DOI matches across author fragments;
4. if DOI is absent, deduplicate exact normalized title + publication-year matches;
5. never auto-promote a held person to `network_observable=true`.

Mechanical deduplication is not evidence that two semantically similar but differently titled works are the same work.

## Manual work-decision states

### KEEP_ORIGINAL
Evidence supports that the intended person authored/created the work and it represents an original intellectual output appropriate for the domain network.

### KEEP_POSTHUMOUS_ORIGINAL
First publication occurred shortly after death but the work is credibly attributable to research/manuscript activity completed during life. Keep the observed diffusion/publication date unless a separate historical-source rule justifies another date.

### EXCLUDE_NAME_COLLISION
The work belongs to a different same/similar-name person.

### EXCLUDE_CONTAINER_FRAGMENT
Database manifestations that are not independent intellectual outputs for the planned network, such as table of contents, front/back matter, acknowledgments, index, or duplicate chapter manifestations.

### EXCLUDE_MODERN_REPRINT
A modern edition/reprint/translation attached to the historical author that would create a false modern production event. A reliable original historical event may be represented separately, but its year must not be guessed.

### DUPLICATE_MANIFESTATION
Multiple database records represent the same historical intellectual work and mechanical DOI/title-year deduplication did not already collapse them.

### EXCLUDE_NON_SCHOLARLY_ARCHIVAL_RECORD
Administrative/archival objects rather than knowledge outputs, e.g. registration records.

### NEEDS_REVIEW
Evidence is insufficient. `NEEDS_REVIEW` cannot enter the confirmatory network.

## Chronology rules

- Before `birth+15`: presumptively incompatible and requires extraordinary evidence to retain.
- After `death+5`: not automatically a namesake, but normally excluded as a production event unless a documented original posthumous publication.
- Modern reprints can support **identity verification** while being excluded from historical production.

This is why a person may be identity-verified but still network-unobservable.

## Book / chapter policy

For the science-first pilot:

1. journal article / conference paper / original monograph = independent work;
2. substantive book chapter = independent only when bibliographically distinct and consistently modeled across the corpus;
3. frontmatter, contents, notes, acknowledgments, index = exclude;
4. book record plus chapter records from the same book = avoid double counting;
5. modern digitization/reissue chapters = exclude as modern manifestations when the historical work is already represented.

## Topic/field evidence

Topic disagreement alone must not delete a work: interdisciplinary careers exist and automated OpenAlex topics are noisy.

Topic mismatch can support `EXCLUDE_NAME_COLLISION` only with stronger evidence such as incompatible bibliography, institution/coauthor network, chronology, or a coherent alternative namesake career.

## Author-ID contamination

An accepted OpenAlex Author ID can be partially contaminated.

Therefore:

- identity may remain `VERIFIED_SINGLE` / `VERIFIED_CLUSTER`;
- only verified work rows enter the analytical network;
- a mixed Author ID does not force exclusion of the historical person;
- aggregate OpenAlex `works_count` is never enough to release a person.

## Network-release rule

A person can become `network_observable=true` only if:

1. identity is VERIFIED;
2. no unresolved work-level contamination threatens the included corpus;
3. at least the current pilot minimum of **5 unique KEEP works** remains;
4. cleaned works provide enough temporal/link information for planned network metrics;
5. provenance from clean work to source OpenAlex Work/Author IDs is preserved.

The >=5 rule is a feasibility gate, not a final sample-size criterion.

## Blinding

Work cleanup remains **pre-exposure**. Reviewers may use identity, dates, field, institutions, publications and network metadata, but not mental-health evidence or CPE outcomes.

## Audit table

Manual decisions should eventually store:

```text
person_id
openalex_work_id
dedup_key
work_decision
canonical_work_id
historical_publication_year
decision_evidence
reviewer
second_reviewer
adjudication_status
mh_blinded_at_work_lock
review_date
```

No confirmatory network should be built directly from raw OpenAlex author profiles once a work-level decision table exists.
