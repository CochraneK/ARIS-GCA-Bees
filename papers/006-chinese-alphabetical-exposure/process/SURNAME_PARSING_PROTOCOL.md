# ARIS4C006 · Chinese surname parsing protocol

Last updated: 2026-09-18

## Objective

Recover a scholar's family-name initial with quantified confidence from bibliographic name strings without equating name form with nationality or ethnicity.

This is a measurement protocol for the focal predictor. Parser decisions must be frozen before confirmatory outcomes are opened.

## 1. Canonical surname dictionary

Base dictionary: all 1,806 `familyname` rows in ChineseNames 2025.8.

For every surname retain:
- Chinese characters;
- single vs compound surname;
- official `initial` and `initial.rank` supplied by ChineseNames;
- population count / ppm;
- uniqueness.

Build an auxiliary Romanization table containing:
- canonical Hanyu Pinyin surname form;
- surname-specific pronunciation for polyphonic characters;
- common alternative/legacy Romanizations with documented mappings;
- normalized ASCII ordering key;
- ambiguity flag where one Latin form maps to multiple Chinese surnames.

The ChineseNames-provided initial remains the population-baseline authority when a Chinese-character surname is directly identified.

## 2. Name-source hierarchy

For an OpenAlex authorship, preserve rather than overwrite:

1. `raw_author_name` from each work;
2. resolved OpenAlex `author.display_name`;
3. ORCID identifier where present;
4. repeated raw-name variants across the author's works;
5. structured external family-name evidence only when reproducibly linked.

A normalized final name must never erase the raw evidence used to derive it.

## 3. Parsing tiers

### Tier 1A — direct Chinese-character match

If raw name contains Han characters:
- strip punctuation/whitespace honorifics;
- longest-match against compound surnames first, then single surnames;
- require surname to appear in a plausible family-name position under a frozen rule;
- use ChineseNames `initial` directly.

### Tier 1B — structured family-name evidence

Use when a linked structured source explicitly supplies family name and identity linkage is high confidence (for example ORCID-linked metadata with consistent work/affiliation evidence).

### Tier 2A — repeated Romanized consistency

Requirements:
- one candidate token maps to the surname Romanization dictionary;
- repeated records support the same token as family name;
- no competing token has comparable evidence;
- observed Chinese/Western name order can vary, but family-token identity remains stable.

### Tier 2B — Romanized + independent corroboration

A single/limited raw-name pattern plus an independent structured source supports the same family-name token.

### Tier 3 — heuristic

Examples:
- always use last token;
- always use first token;
- choose whichever token is a common Chinese surname without corroboration.

Tier 3 is **engineering-only** and excluded from confirmatory models.

## 4. Compound surnames

Match compound surnames before single surnames in Chinese-character strings.

For Romanized forms, normalize common separator variants:
- space;
- hyphen;
- concatenation where documented.

Do not split a known compound surname merely to increase matching coverage.

## 5. Polyphonic surname exceptions

Chinese characters whose surname pronunciation differs from the common lexical pronunciation require an explicit reviewed exception table. Examples should be verified from authoritative linguistic/name sources before release; do not rely on a generic character-to-Pinyin converter alone.

Each exception row should contain:
- Chinese surname;
- surname pronunciation;
- expected initial;
- source/citation;
- alternative Romanizations;
- notes.

## 6. Romanization ambiguity

Potential ambiguity sources:
- Wade–Giles / historical spellings;
- Cantonese and other regional Romanizations;
- spacing/hyphen differences;
- initials-only records;
- Western given names inserted before/after Chinese names;
- name changes;
- compound given names.

Do not force an assignment when two plausible surname tokens remain.

Output `parse_status = ambiguous` and exclude from the confirmatory sample.

## 7. Record-level output schema

For each authorship/name observation record:

- `work_id`
- `author_id`
- `raw_author_name`
- `display_name`
- `surname_chinese` when known
- `surname_romanized`
- `surname_initial`
- `surname_initial_rank`
- `surname_population_n` when exact surname known
- `surname_population_ppm`
- `parse_tier`
- `parse_confidence`
- `parse_rule_id`
- `evidence_count`
- `ambiguity_reason`
- `parser_version`

At author level, retain discordance across works; do not silently majority-vote without recording disagreement.

## 8. Validation sampling

Create an outcome-blinded validation set stratified by:

- surname frequency quintile/decile;
- initial rank (early/middle/late);
- field;
- domestic-only vs internationally affiliated career history;
- two-token vs multi-token names;
- Chinese-character evidence present/absent;
- compound surname candidates;
- ORCID present/absent.

Oversample rare/high-risk strata for diagnostic precision, then report both stratified metrics and prevalence-weighted overall performance.

## 9. Validation metrics

At minimum:
- surname-token precision;
- surname-token recall/coverage;
- initial-letter precision;
- exact-initial-rank precision;
- ambiguity rate;
- error rate by surname-frequency and alphabet-rank strata.

The confirmatory acceptance threshold must be frozen **before** focal outcomes are inspected. A candidate starting standard is >=98% initial-letter precision in included Tier 1/2 records, but the final threshold should be justified after a blind engineering pilot rather than selected to preserve sample size.

## 10. Differential-error test

Parser error itself becomes an outcome in validation:

`ParserError ~ InitialRank + SurnameFrequency + Field + Mobility + Year + NameForm`

A meaningful monotonic relationship with `InitialRank` is a serious threat even when average accuracy looks high.

## 11. Versioning

Every parser change increments `parser_version` and records:
- rule change;
- reason;
- validation impact;
- whether focal outcomes had been seen at the time.

Post-outcome rule changes cannot silently replace preregistered confirmatory parsing; they are sensitivity analyses unless independently required to fix a clear bug.

## 12. Stop rule

If high-confidence parsing cannot achieve adequate precision and broad-enough coverage without differential error by surname rank, ARIS4C006 should narrow to a direct-Chinese-character subset or stop rather than substitute a convenient last-token heuristic.


## 13. Crossref structured-family rule after Pilot 3

Pilot 3 (`process/PILOT3_RESULTS.md`) establishes Crossref contributor metadata as the preferred structured family-name evidence for DOI-bearing works, subject to positional reconciliation.

### Tier 1B operational rule

A work-level Crossref family name is Tier 1B only when all applicable checks pass:

1. OpenAlex DOI resolves to a Crossref work record.
2. OpenAlex and Crossref contributor counts agree.
3. Crossref supplies a non-empty `family` value for the focal list position.
4. The normalized Crossref family token is compatible with the OpenAlex raw/display-name evidence at that same position.
5. If both sources provide ORCID, the identifiers must agree.
6. Compound-surname / alternative-Romanization logic does not leave two plausible family-name assignments.

Failure of any item does not imply a different surname; it downgrades the observation to a lower evidence tier or exclusion.

### Pilot 3 empirical evidence

In 180 DOI-selected 2024 multi-author works across six fields:

- Crossref record retrieval: 180/180;
- same author count: 172/180 = 95.56%;
- all Crossref family values present: 99.44% of found works;
- aligned CN-affiliated author rows: 787;
- structured Crossref family matched an OpenAlex name token: 99.87%;
- structured family matched the last OpenAlex token: 99.87%.

The last figure is **not** permission to promote the final-token heuristic. The pilot preselected DOI-bearing modern records and therefore does not quantify error in older/no-DOI/format-anomalous records.

### Freeze rule

Confirmatory code must preserve the distinction between:

- `surname_source = crossref_structured`
- `surname_source = direct_han`
- `surname_source = repeated_corroborated`
- `surname_source = heuristic`

The last category remains excluded from confirmatory inference.

## 14. Measurement-gate thresholds to freeze before outcome analysis

The final thresholds will be frozen from measurement-only Pilot 4, before focal surname-by-exposure outcome estimates are opened.

Candidate minimums:

- >=98% surname-initial precision among included Tier 1/2 validation records;
- >=95% strict positional support for Crossref/OpenAlex same-count work matches;
- ORCID disagreement sufficiently rare that it does not indicate positional misalignment;
- no material monotonic parser-error gradient by surname rank;
- field/year DOI coverage documented, with no silent complete-case interpretation if coverage is strongly selected.

If the Crossref-backed path is precise but selectively incomplete, the primary analysis may use the high-confidence subset while population generalization is explicitly bounded and no-DOI records enter only through independently validated Tier 1A/2 evidence.
