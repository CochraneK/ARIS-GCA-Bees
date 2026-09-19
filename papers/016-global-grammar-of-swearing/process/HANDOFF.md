# ARIS4C016 Cross-Agent Handoff

Updated: 2026-09-19

## Canonical project

- ID: ARIS4C016
- Slug: `global-grammar-of-swearing`
- Working title: **The Global Grammar of Swearing: A Cross-Linguistic Atlas of Taboo, Insult, and Profanity**
- ARIS route: ARIS4C guided design / Phase 0 empirical audit
- ARIS version: v0.4.26
- Current portfolio state: **68% · block**
- Block reason: genuinely independent Coder A/B plus native-language review is required for the frozen ontology-reliability gate.

Git is the canonical source of truth. Do not reconstruct state from chat memory when these files are available.

## Current scientific position

The project is no longer a “world swear-word dictionary”.

Main question:

> Which parts of taboo-language structure are stable across communities, and
> which remain context-sensitive once measurement non-equivalence, lexical
> identity and language genealogy are made explicit?

Current theory:
**stable lexical core + contextual modulation**, with a major measurement
warning that community/site effects are not yet demonstrably taboo-specific.

## Data already audited

Sulpizio et al. (2024) public OSF project:
- Study 1: 8,190 lexical rows;
- Study 2: 4,240 item-rating rows;
- 18 community samples;
- 17 countries;
- 13 languages;
- 1,046 Study-1 participants.

Raw third-party files are not vendored because the OSF project page reports no
project-level license. The repository stores source GUIDs, SHA-256 values and
reproducible download code.

Canonical provenance:
`data/source_manifest.json`.

## Main findings already frozen

### Measurement heterogeneity

Study-1 source annotations differ sharply across sites:
- large variation in elicitation yield;
- extreme differences in category missingness;
- extreme differences in multi-label usage;
- original flat category field mixes semantic, pragmatic and social-indexical levels.

Therefore raw category prevalence is not a valid cross-cultural outcome.

### Ontology

Ontology v0 separates:
1. semantic taboo source;
2. target;
3. pragmatic function;
4. social-indexical basis;
5. taboo/derogation mechanism;
6. linguistic form.

Preserve raw labels; unresolved is preferable to speculative mapping.

### Harmonisation

High-confidence rules map about 80.4% of non-empty source label occurrences,
but row-level semantic-source coverage varies strongly by community. The naïve
semantic Taboo Fingerprint therefore failed its comparability gate.

### Genealogy

The 18 samples correspond to 13 languages / 5 top-level Glottolog families.
Eight of 13 languages are Indo-European.

Repeated-language structure:
- English: AU, CA, GB, SG, US;
- Spanish: CL, ES.

Do not treat 18 community samples as 18 independent languages.

### Repeated English items

Primary item-fixed-effects FWL model:
- 139 taboo lexical items shared by ≥2 English communities;
- 417 item × community observations;
- tabooness community partial R² = .0265;
- offensiveness = .0361.

Balanced all-five subset:
- 23 items;
- tabooness R² = .0537;
- offensiveness R² = .0532;
- uncertainty is wider.

Sparse filler negative control:
- 35 shared filler items / 73 observations;
- tabooness rating R² = .2965;
- offensiveness = .1583.

Interpretation:
community-associated rating differences exist, but current data do **not**
establish a taboo-specific cultural effect. General site/sample/rating
calibration differences may contribute substantially.

## Frozen independent-coder gate

Audit sample:
- exactly 300 Study-1 rows;
- 15 per ordinary community;
- 30 Setswana (BW);
- 30 Spanish (ES);
- missing stratum: 42;
- unresolved: 116;
- multi-label: 61;
- random/backfill: 81.

Frozen manifest SHA-256:

`48c58f91901e8c2a1aab01958e95ea28afaf0f33e7a98677f98e58b8a412c9b4`

Do not replace difficult rows after coding begins.

Key files:
- `process/AUDIT_SAMPLE_FREEZE.md`
- `process/CODER_HANDOFF.md`
- `code/build_audit_sample.py`
- `code/export_private_coding_sheet.py`
- `code/score_coder_reliability.py`

The generated private sheet contains raw taboo/slur text and must not be committed.

## Manuscripts / figures

English working manuscript:
`manuscript/DRAFT.md`

Chinese working manuscript:
`manuscript/DRAFT.zh-CN.md`

Current public-safe figures:
- Figure 1 measurement pipeline;
- Figure 2 semantic-source annotation coverage;
- Figure 3 taboo-vs-filler repeated-item negative control.

See `figures/README.md`.

## Phonology track

The source `transcription` field is not a common global IPA layer, but the
pronunciation-engineering track has now been executed end-to-end.

Frozen runtime:
- Epitran 1.35.2;
- Flite source commit
  `6c9f20dc915b17f5619340069889db0aa007fcdc`;
- English via `eng-Latn` + compiled `lex_lookup`;
- Cantonese via source transcription → `yue-Latn`;
- Mandarin via source transcription → `cmn-Latn`;
- remaining languages via language/script-specific Epitran routes.

Full-route result:
- **8,187 / 8,190 rows = 99.9634% technical success**;
- 2 English (SG) rows returned empty/non-letter output;
- 1 Mandarin row lacked source transcription;
- no backend exceptions in the full-route audit.

This establishes engineering feasibility only. It does **not** establish
pronunciation accuracy. The next phonology gate is a stratified
native/source-language pronunciation-validity audit, followed by matched
neutral controls and frozen segment/approximant coding.

Primary prior hypothesis:
replicate Lev-Ari & McKay’s approximant effect. Do not claim it as a new 016
discovery.

Canonical files:
- `process/G2P_FULL_ROUTE_AUDIT.md`
- `process/CHINESE_ROMANIZATION_PILOT.md`
- `data/phonology_runtime_lock.json`
- `code/g2p_full_route_audit.py`.

## Immediate TODO after handoff

### External / independent gate
1. Generate private Coder A sheet.
2. Generate private Coder B sheet independently.
3. Freeze both outputs before either coder sees the other.
4. Run `score_coder_reliability.py`.
5. Review community-stratified disagreement and native-review queue.
6. Adjudicate only after raw A/B are frozen.
7. Version ontology only after agreement diagnostics.

### After reliability passes
1. Build measurement-corrected semantic fingerprints.
2. Run type-weighted and production-weighted versions.
3. Add missing/unresolved sensitivity bounds.
4. Run ontology-domain × community repeated-item models.
5. Build a purpose-designed matched taboo/neutral interaction test.
6. Freeze and run pronunciation-validity audit; technical G2P coverage is already complete.
7. Build matched neutral controls and continue the preregistered approximant replication.
8. Design a crossed language × country expansion with broader family diversity.

## Claims that are currently allowed

- annotation protocols differ substantially across samples;
- naïve raw category profiles are not directly comparable;
- lexical identity dominates English taboo ratings;
- modest community-associated variation remains after item fixed effects;
- current community effects are not shown to be taboo-specific;
- current language coverage is genealogically imbalanced.

## Claims that are currently blocked

Until independent reliability:
- country/community semantic-domain fingerprints;
- domain-specific cultural comparisons.

Until broader family coverage:
- strong cross-linguistic universals;
- language-family effects as general laws.

Until stronger identification:
- causal claims about religion, kinship, collectivism, censorship or other cultural variables.

## Public-safety / data rule

Do not turn the repository or atlas into a browsable identity-slur list.
Prefer aggregate statistics, hashes, censored examples, uncertainty and
provenance in public artifacts.
