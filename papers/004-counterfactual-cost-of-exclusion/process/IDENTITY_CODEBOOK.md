# IDENTITY CODEBOOK — ARIS4C004

Date: 2026-09-18

## Purpose

Define how a historical person in the frozen mental-health-independent candidate frame becomes a verified science-network entity.

The mapping target is not necessarily one OpenAlex Author ID:

`historical person -> {one or more verified OpenAlex Author IDs}`

OpenAlex author fragmentation is expected. The analytic object is therefore an **audited person-level author cluster**.

Mental-health information must not be used to resolve identity.

---

## 1. Identity states

Canonical variable: `identity_status`

Allowed values:

- `VERIFIED_SINGLE` — one OpenAlex Author ID is adequately verified as the intended person and no material additional fragment has been identified.
- `VERIFIED_CLUSTER` — two or more OpenAlex Author IDs are adequately verified as fragments of the same historical person.
- `PROVISIONAL_SINGLE` — one plausible record exists but evidence is insufficient for confirmatory inclusion.
- `PROVISIONAL_CLUSTER` — multiple plausible fragments exist but the merge is not yet sufficiently verified.
- `AMBIGUOUS_COLLISION` — records may belong to different people with the same/similar name and cannot be safely separated/merged.
- `NO_GRAPH_RECORD` — no usable OpenAlex author/work record is found under the current search protocol.
- `EXCLUDED_IDENTITY_ERROR` — an earlier automated match was shown to be wrong.

Only `VERIFIED_SINGLE` and `VERIFIED_CLUSTER` can enter the confirmatory network analytic frame.

---

## 2. Evidence signals

Every verified decision must use more than a bare name match unless a unique strong external identifier is available.

### Strong external identity signals

- exact ORCID linked to the intended person;
- authoritative identity crosswalk from a curated authority source;
- exact DOI/work identity linking the historical person to an OpenAlex author record;
- institutional or archival authority record that directly cross-links the person and scholarly works.

### Bibliographic concordance signals

- known work title appears in the candidate OpenAlex record;
- publication dates are plausible for the person's career, allowing reprints/posthumous records to be labeled separately;
- known institution/affiliation agrees;
- known coauthor/collaborator agrees;
- subject/topic profile agrees with the documented field;
- initials/full-name/alias pattern agrees;
- language/geography agrees where informative.

### Fragment-linking signals

Two OpenAlex Author IDs may be merged into one person-level cluster when independent evidence supports common identity, such as:

- duplicate/overlapping works;
- same distinctive coauthors;
- same institution in overlapping periods;
- complementary name variants/initials plus matching bibliographic content;
- same ORCID or authoritative external identifier;
- explicit known publications split across the records.

Name equality alone is **not** enough for a confirmatory cluster merge.

---

## 3. Conflict signals

The following block automatic merging and normally require `AMBIGUOUS_COLLISION` until resolved:

- different non-empty ORCIDs;
- incompatible career periods that cannot be explained by reprints/indexing artifacts;
- incompatible disciplines plus distinct coauthor/institution communities;
- distinct external authority identities;
- publication evidence showing two contemporaneous people with the same name.

A larger `works_count` is not proof that the larger record is the intended person.

---

## 4. Minimum rules for VERIFIED_SINGLE

A single record can be verified by either:

### Route S1 — strong identifier

At least one strong external identity signal and no material contradiction.

### Route S2 — convergent bibliographic evidence

At least **two independent bibliographic concordance signals beyond name**, with no material contradiction.

Examples:

- name/alias + known paper title + institution;
- name/alias + known work + distinctive coauthor;
- name/alias + institution + field/topic + career dates, when the name is uncommon and search results do not indicate a collision.

The reviewer must also inspect whether additional plausible OpenAlex fragments exist.

---

## 5. Minimum rules for VERIFIED_CLUSTER

For every included fragment:

1. the fragment must independently be plausible for the historical person;
2. at least one fragment-linking signal beyond name must connect it to the verified person/cluster;
3. no unresolved strong conflict signal may remain;
4. the cluster decision must list every included OpenAlex Author ID and the evidence used;
5. obvious duplicate works across fragments must be deduplicated at work-ID/DOI/title-year level before analysis.

A cluster can be incomplete. Reviewers should explicitly record `cluster_completeness = high / moderate / low`.

Primary confirmatory analysis should prefer high/moderate completeness; low-completeness clusters are sensitivity/exploratory unless otherwise justified.

---

## 6. Network observability is separate from identity validity

Record both:

- `network_observable`: enough verified graph data exist for planned baseline/downstream metrics;
- `identity_status`: whether the graph actually belongs to the intended person.

Possible combinations include:

- high apparent coverage + ambiguous identity;
- verified identity + too few works for network analysis;
- verified cluster + strong network coverage;
- no OpenAlex graph record.

Do not collapse these into one `resolved` variable.

---

## 7. Required identity-review fields

Person-level decision table:

```text
person_id
canonical_name
wikidata_qid
birth_year
death_year
identity_status
verified_openalex_ids
cluster_completeness
network_observable
strong_identifier_evidence
known_work_match_n
institution_match
coauthor_match
topic_field_match
career_timing_match
conflicting_orcid
collision_evidence
reviewer
second_reviewer
adjudication_status
review_date
mh_blinded_at_identity_lock
notes
```

A separate evidence table may store one row per evidence item.

---

## 8. Blinding rule

Identity review happens **before mental-health exposure coding** whenever feasible.

Reviewers may use:

- candidate-frame identity metadata;
- authority records;
- bibliographic works;
- institutions/coauthors/topics;
- general biographical dates needed for identity.

Reviewers must not use psychiatric history to decide which OpenAlex record "looks right."

Record `mh_blinded_at_identity_lock=true/false`.

---

## 9. Precision audit

Before expanding the science pilot:

1. review all automatically accepted records among the first 30;
2. independently double-review at least a substantial subset, enriched for fragment/collision cases;
3. estimate false-positive and missed-fragment rates of the automated resolver;
4. revise automated search/review prioritization if precision is inadequate;
5. never lower verification rules merely to increase coverage.

Desired confirmatory property:

> near-100% auditable identity precision among final included analytic persons, even if broad-frame coverage is much lower.

This is not the same as demanding 95–100% OpenAlex coverage of the historical candidate universe.

---

## 10. Pre-exposure analytic-frame lock

The science network analytic frame can be frozen only after:

- identity review is complete for all included candidates;
- all included candidates are `VERIFIED_SINGLE` or `VERIFIED_CLUSTER`;
- network observability criteria are satisfied;
- exclusions and missingness reasons are recorded;
- distribution of inclusion/exclusion is audited across cohort, visibility, geography, gender, and subdomain;
- mental-health evidence has not been used as an inclusion criterion.

Only after this lock may `EXPOSURE_CODEBOOK.md` be applied to determine the mental-health focal set.

---

## 11. Automatic quality-control failures

The identity validator should reject or flag:

- confirmatory inclusion with a `PROVISIONAL_*`, `AMBIGUOUS_COLLISION`, `NO_GRAPH_RECORD`, or error state;
- `VERIFIED_CLUSTER` with fewer than 2 OpenAlex IDs;
- `VERIFIED_SINGLE` with more than 1 OpenAlex ID;
- any verified state with zero evidence beyond name unless a strong external identifier is recorded;
- conflicting ORCID marked true in a verified cluster;
- network-observable true with no verified OpenAlex ID;
- duplicate OpenAlex ID listed twice;
- mental-health blinding field missing at identity lock;
- living person in the primary historical analytic frame.

---

## 12. Freeze rule

This codebook can change during the pre-exposure identity pilot. Every substantive revision must be logged.

Once the first science analytic frame is frozen, identity rules used for confirmatory inclusion must be versioned and cannot be loosened after mental-health exposure yield or CPE outcomes are seen.
