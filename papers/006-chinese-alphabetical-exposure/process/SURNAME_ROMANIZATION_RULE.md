# ARIS4C006 · Frozen surname romanization and focal-form rule

Last updated: 2026-09-18

## Primary focal surname rule

A CN-affiliated authorship can be a focal Chinese-surname row only when its family name passes one of two high-confidence routes.

### Route H — direct Han

- family name is directly recoverable in Han characters under the reviewed compound-surname-first rule;
- exact Han surname exists in the pinned ChineseNames 2025.8 dictionary;
- ChineseNames supplies the authoritative initial and population frequency.

### Route P — exact canonical Hanyu Pinyin

- DOI-linked Crossref contributor metadata provides a structured `family` value;
- OpenAlex/Crossref author lists pass the frozen positional reconciliation rule;
- normalized structured family name exactly equals a frozen canonical Hanyu-Pinyin form generated from ChineseNames;
- no conflicting ORCID / canonical-author evidence exists.

Unreviewed historical/regional/legacy Romanizations are **not** primary-route matches.

Examples such as Lee, Chan, Wong, Cheung, Tsang, Hsü, or Wade–Giles-style spellings are not guessed into a ChineseNames surname merely because a mapping seems plausible.

## Canonical map

Engineering version:
- ChineseNames familyname rows: 1,806;
- `pypinyin == 0.55.0`;
- accepted high-confidence rows: 1,803;
- unresolved: 3;
- represented ChineseNames population: **99.9918%**;
- aggregated Hanyu-Pinyin bibliographic forms: **413**.

The three unresolved automated rows are:
- 尉;
- 朝;
- 万俟.

They are excluded from automated Romanized primary mapping until separately reviewed and frozen.

## Homophonous surnames

When multiple Chinese-character surnames map to the same Romanized Hanyu-Pinyin form, a Romanized bibliographic observation does not receive an invented exact Han surname.

Instead retain:
- the Romanized form;
- its initial;
- aggregate population count/ppm summed over all accepted ChineseNames surnames producing that form;
- ambiguity count / member list for provenance.

Direct-Han records may retain exact-character population counts as a sensitivity.

## Bibliographic coverage

Pilot 14:
- 1,153 CN-affiliated structured-family rows sampled across all 26 fields in 2024;
- 1,102 exact canonical-Pinyin matches;
- primary mapping coverage **95.58%**.

This is sufficient to prefer precision over speculative variant expansion.

## Non-primary variant dictionary

A reviewed variant dictionary may be created later only for sensitivity analysis.

Rules:
1. source each variant;
2. freeze the dictionary before focal results from that sensitivity are inspected;
3. report coverage gain and any change in initial/population assignment;
4. never let the variant-expanded sample replace the primary sample because it yields a stronger effect.

## Ordering of all coauthors

The primary focal-row rule above applies to **focal ChineseNames-mappable CN-affiliated authorships**.

To compute whole-team `RelAlphaRank`, non-focal coauthors need a reliable structured family-name ordering key but do not need to map to ChineseNames.

Thus:
- Chinese population attributes are attached only to focal mapped surname forms;
- all reliable coauthor family names can determine relative alphabetical position.

## Parser version

Frozen primary mapping label:

`aris4c006-surname-map-v1`

Components:
- ChineseNames 2025.8;
- Crossref structured-family reconciliation rule;
- pypinyin 0.55.0 canonical map;
- direct-Han compound-first rule;
- no unreviewed legacy/regional aliases.

Any later mapping change increments the version and is secondary unless required to correct a demonstrable bug.
