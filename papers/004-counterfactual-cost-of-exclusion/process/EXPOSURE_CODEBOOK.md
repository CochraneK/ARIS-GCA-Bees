# EXPOSURE CODEBOOK — ARIS4C004

Date: 2026-09-18

## Purpose

This codebook defines how historical mental-health evidence is recorded for ARIS4C004 before confirmatory network outcomes are inspected. It is designed to prevent celebrity-driven case selection, retrospective overdiagnosis, and the false assumption that missing evidence means absence of a condition.

The coded object is **surviving evidence about mental-health history**, not an omniscient modern diagnosis.

---

## 1. Eligibility before exposure coding

A person may enter exposure coding only after appearing in the frozen mental-health-independent candidate frame.

Primary quantitative analysis is restricted to **deceased persons**.

Required identity fields:

- `person_id` — project-stable identifier;
- `canonical_name`;
- `birth_year`;
- `death_year`;
- `domain`;
- `subdomain`;
- `wikidata_qid` if resolved;
- `openalex_author_id` if resolved/applicable;
- candidate-frame source and row/record ID.

Exposure coders must not add people merely because a famous diagnosis is known.

---

## 2. Evidence-class variable

Canonical variable: `mh_evidence_class`

Allowed values:

### A1 — contemporaneous clinical diagnosis / medical record

Use when a surviving source contemporaneous with the person's life documents a clinical diagnosis or equivalent medical assessment with clear provenance.

Examples of acceptable source types:

- treating clinician's record;
- hospital case record;
- contemporaneous clinical report;
- authenticated medical correspondence with explicit clinical assessment.

Do not translate historical terminology into a modern DSM/ICD diagnosis in the primary field.

### A2 — strong contemporaneous clinical encounter without stable modern label

Use when there is strong evidence of psychiatric hospitalization, treatment, institutionalization, or treating-clinician documentation, but the exact diagnosis is unclear, contested, historically obsolete, or not transportable into modern nosology.

A2 is intended to preserve strong evidence without false diagnostic precision.

### B1 — strong contemporaneous nonclinical evidence

Use only when multiple independent contemporaneous sources document a sustained or severe mental-health syndrome/impairment and no adequate clinical record survives.

Possible sources:

- multiple letters/diaries from the person;
- close associates' contemporaneous accounts;
- institutional records documenting severe impairment;
- legally/administratively documented episodes.

B1 requires more than eccentricity, unconventional behavior, substance use alone, artistic themes, or a single anecdote.

### B2 — rigorous scholarly historical/medical reconstruction

Use when a high-quality scholarly source reconstructs a clinically meaningful syndrome from identifiable primary sources, explicitly discusses diagnostic uncertainty, and does not rely primarily on legend or circular citation.

B2 is still retrospective and remains outside the strict Tier-A primary exposure definition.

### C — speculative retrospective attribution

Use when a modern author/website/biography assigns a psychiatric label but the claim lacks sufficient contemporaneous evidence, source transparency, or historical diagnostic caution.

Tier C may be retained for descriptive audit but is excluded from confirmatory exposed definitions.

### U — unknown / insufficient evidence

Use when evidence is absent, too sparse, contradictory, or not adequately searched.

**U never means healthy.**

---

## 3. Collapsed analysis tiers

Derived variable `mh_tier`:

- `A` = A1 or A2;
- `B` = B1 or B2;
- `C` = C;
- `U` = U.

Default analysis definitions:

- strict confirmatory exposed set: Tier A;
- sensitivity exposed set: Tier A+B;
- Tier C excluded from exposed set;
- U retained as unknown and handled through comparison/common-support rules.

If pilot Tier-A yield is insufficient, the project must explicitly downgrade or redesign rather than silently redefine B as confirmed diagnosis after seeing outcomes.

---

## 4. Historical wording versus modern mapping

Store separately:

- `historical_description_verbatim_short` — <=25 words only when necessary and legally permissible;
- `historical_term_normalized` — concise historical descriptor;
- `modern_mapping_family` — optional broad family such as psychotic-spectrum, mood-spectrum, anxiety/trauma-related, substance-related, neurodevelopmental, other/uncertain;
- `modern_mapping_confidence` — none / low / moderate / high;
- `modern_mapping_basis`.

The primary exposure is evidence tier, not a precise modern diagnosis.

Do not infer a modern condition solely from:

- artistic or literary content;
- political/religious beliefs;
- nonconformity;
- sexual orientation/gender expression;
- unusual personality;
- one episode of intoxication;
- rumors or unsourced lists of "famous people with X".

---

## 5. Clinical significance and duration

Record where evidence permits:

- `episode_pattern`: single / recurrent / chronic / unclear;
- `functional_impairment`: none documented / mild / moderate / severe / unclear;
- `hospitalization_or_institutionalization`: yes / no / unknown;
- `treatment_documented`: yes / no / unknown;
- `first_evidence_year`;
- `last_evidence_year`;
- `active_career_overlap`: before career / during career / after main career / spans periods / unclear.

These are descriptive evidence fields, not causal interpretations.

---

## 6. Discrimination / exclusion coding is separate

Canonical variable family: `exclusion_*`

Mental-health evidence does not automatically imply discrimination.

Possible evidence categories:

- `formal_legal_or_institutional_exclusion`;
- `employment_or_appointment_denial`;
- `dismissal_or_forced_leave`;
- `training_or_education_barrier`;
- `publication/patronage/platform barrier`;
- `involuntary_institutionalization_affecting_participation`;
- `documented_stigma/social_exclusion`;
- `none_documented`;
- `unknown`.

For every affirmative exclusion code record:

- event date/range;
- source;
- whether the source explicitly links the action to mental-health status;
- evidence strength;
- estimated participation consequence only if directly supported.

Do not infer discrimination merely from lower productivity during illness.

---

## 7. Source hierarchy

For each evidence claim, record `source_class`:

1. `primary_clinical` — medical/hospital/treating-clinician record;
2. `primary_nonclinical` — contemporaneous personal/institutional record;
3. `scholarly_history` — peer-reviewed historical/medical scholarship with primary-source trail;
4. `authoritative_biography` — scholarly/major biography with citations;
5. `reference_work` — curated reference database/encyclopedia;
6. `general_secondary` — reputable but non-scholarly secondary source;
7. `unsourced_or_weak` — websites/lists/repeated claims without traceable evidence.

Tier A requires class 1 evidence. Tier B normally requires classes 2–4 with adequate triangulation. Classes 5–7 can generate search leads but cannot alone establish Tier A/B.

---

## 8. Source independence

Multiple sources that repeat the same biography or unsourced claim are not independent confirmation.

Record:

- `source_family_id` — common upstream source where known;
- `independent_primary_sources_n`;
- `independent_scholarly_reconstructions_n`.

Coders should trace important claims backward to the earliest identifiable evidence whenever feasible.

---

## 9. Contradictory evidence

Record:

- `contradiction_flag`;
- `contradiction_summary`;
- `alternative_interpretation`;
- `adjudication_status`.

If serious contradictory evidence exists, choose the weaker/more uncertain evidence tier unless a written adjudication justifies otherwise.

A famous or repeated diagnosis does not override source conflict.

---

## 10. Documentation intensity

Exposure ascertainment depends strongly on how much documentation survives.

Required candidate-level fields where feasible:

- `biographies_n`;
- `scholarly_biographies_n`;
- `archive_or_correspondence_available`;
- `authority_records_n`;
- `languages_with_substantial_biography_n`;
- `medical_historical_sources_n`;
- `cross_verified_notability_group` where available;
- `documentation_notes`.

Derived `documentation_intensity` may be constructed later, but raw components must remain available.

The score must not be tuned to improve exposed/control balance after outcome inspection.

---

## 11. Search-completeness field

Because `U` can mean either genuinely little evidence or inadequate searching, record:

- `search_status`: not_started / basic / expanded / adjudicated;
- `databases_or_catalogues_searched`;
- `search_date`;
- `languages_searched`;
- `searcher`;
- `stopping_rule_met`: yes/no.

### Proposed stopping rule for a candidate used as a primary comparison

At least:

1. one authoritative biographical/reference source;
2. targeted searches for psychiatric/mental-health/medical history using name variants;
3. inspection of any identified medical/biographical scholarly lead;
4. documentation-intensity fields completed sufficiently for common-support assessment.

A low-documentation candidate who cannot meet the rule remains U-low-information and should not be described as a negative case.

---

## 12. Blinding

Preferred workflow:

1. candidate frame frozen;
2. basic identity/domain metadata available to exposure coder;
3. coder does **not** see focal CPE simulations or downstream network-loss estimates;
4. evidence tier locked;
5. network outcome analysis proceeds.

Perfect blinding to fame is impossible, but blinding to calculated outcomes reduces motivated coding.

Record `outcome_blinded_at_lock = true/false`.

---

## 13. Reliability / adjudication

Pilot a double-coded subset before scaling.

Recommended minimum:

- 20–30 cases enriched for ambiguous A/B/C boundaries;
- two independent coders;
- agreement reported for collapsed A/B/C/U and source-class decisions;
- Cohen's kappa or weighted kappa where meaningful, alongside raw agreement;
- written adjudication for disagreements.

If reliability is poor, simplify categories rather than forcing precision.

---

## 14. Machine-readable schema

Minimum CSV/Parquet columns:

```text
person_id
canonical_name
birth_year
death_year
domain
subdomain
wikidata_qid
openalex_author_id
candidate_frame_source
candidate_frame_record_id
mh_evidence_class
mh_tier
historical_term_normalized
modern_mapping_family
modern_mapping_confidence
episode_pattern
functional_impairment
hospitalization_or_institutionalization
treatment_documented
first_evidence_year
last_evidence_year
active_career_overlap
source_class_best
source_primary_identifier
source_secondary_identifiers
independent_primary_sources_n
independent_scholarly_reconstructions_n
contradiction_flag
adjudication_status
search_status
search_date
languages_searched
outcome_blinded_at_lock
documentation_intensity
coder
notes
```

Exclusion/discrimination events should live in a separate one-to-many table keyed by `person_id`.

---

## 15. Quality-control rules

Automatic validation should flag:

- living person in primary dataset;
- Tier A without clinical-source provenance;
- Tier B with only weak/general-secondary sources;
- modern diagnosis filled while historical/source evidence is empty;
- U coded as `healthy` or `control_negative`;
- exclusion/discrimination field inferred only from productivity change;
- exposure lock date later than first confirmatory outcome inspection;
- duplicate people / conflicting IDs;
- evidence dates outside plausible lifespan;
- missing provenance for an affirmative Tier A/B classification.

---

## 16. Analysis restrictions

### Confirmatory

- Tier A exposed definition if precision permits;
- Tier A+B sensitivity;
- deceased only;
- exposure locked before confirmatory CPE outcome review;
- documentation common support required.

### Exploratory only

- diagnosis-family comparisons;
- Tier C inclusion;
- probabilistic modern-diagnosis mapping;
- symptom-specific hypotheses;
- fine-grained disorder labels.

The project should not become a post hoc search for which psychiatric diagnosis appears most "important."

---

## 17. Language standard

Preferred language:

- "people/persons with documented mental-health histories/conditions";
- "evidence-supported historical mental-health condition";
- "retrospective attribution" where appropriate;
- "participation attenuation/exclusion scenario."

Avoid:

- "mad genius" except when naming/critiquing the historical stereotype;
- "crazy" or sensational labels;
- implying that suffering is beneficial or necessary for creativity;
- presenting contested historical diagnoses as settled facts.

---

## 18. Freeze rule

This codebook may be improved during the **pilot before confirmatory outcome inspection**. Every substantive change must be logged with date and reason.

Once the exposure coding pilot and reliability review are accepted, create a version tag/hash and use that frozen version for the confirmatory focal sample.
