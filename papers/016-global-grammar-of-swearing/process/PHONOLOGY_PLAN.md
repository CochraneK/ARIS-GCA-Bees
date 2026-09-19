# ARIS4C016 Phonology Feasibility and Replication Plan

Updated: 2026-09-19

## Phase-0 feasibility result

The Sulpizio et al. Study-1 `transcription` field is **not** a global
phonological representation.

Coverage by community:
- Cantonese (CN): 601 / 632 rows = 95.1%;
- Mandarin (CN): 301 / 302 rows = 99.7%;
- all other 16 community samples: essentially 0%.

Nearly all populated Chinese transcriptions contain digits, consistent with
tone-number romanization. The field therefore cannot be treated as a common
IPA layer across the 13 languages.

## Consequence

Do **not** run a cross-language phoneme analysis directly on the source
`transcription` column.

ARIS4C016 will build an independent pronunciation layer and keep the source
transcription only as language-specific provenance / validation data.

## Prior hypothesis to replicate

Lev-Ari & McKay's cross-linguistic work identified a candidate profanity sound
pattern: approximants were relatively under-represented in swear words, and
experimental participants were less likely to judge pseudowords containing
approximants as swear-like.

Their approximant coding covered:
- /l/ and lateral approximants such as /ʎ/;
- /w/;
- /j/;
- r-sounds in their ASJP-based coding.

This is a **prior hypothesis**, not an ARIS4C016 discovery.

## Pronunciation layer

### Primary route: Epitran where supported

Use language/script-specific G2P, freezing:
- Epitran version;
- language code;
- preprocessing options;
- dictionary dependencies;
- failures / out-of-vocabulary rate.

The currently documented Epitran support includes many relevant ARIS4C016
languages, including English, German, Finnish, French, Dutch, Italian,
Mandarin, Spanish, Serbian, Slovenian, Thai, Setswana and Cantonese/Yue.

Cautions:
- English requires an additional Flite-based backend;
- Chinese/Cantonese rely on dictionary resources for some modes;
- French and other ambiguous orthographies require extra caution;
- slang, deliberate misspelling, euphemism and code-switching may fail G2P
  non-randomly.

### Phonological feature reference: PHOIBLE

PHOIBLE provides:
- Unicode-IPA inventory representations;
- distinctive features;
- Glottolog/ISO-linked language inventories.

PHOIBLE is an inventory database, **not** a word-pronunciation lexicon. It
should be used to normalize/validate phoneme classes, not to invent
pronunciations for lexical items.

## Replication design

For each language:

1. generate/validate IPA for taboo items;
2. construct a neutral control pool from the same language;
3. match control words on at least:
   - segment length;
   - corpus frequency;
   - morphological complexity where feasible;
   - lexical class / part of speech where feasible;
4. calculate phoneme-class features;
5. test the preregistered approximant hypothesis;
6. treat other sound classes as exploratory unless separately preregistered.

## Primary phonological outcome

At item level:
- approximant present / absent;
- approximant count;
- approximant proportion among segments.

Model taboo/control status from phonological features with language-level
partial pooling.

## Essential controls

A raw comparison of taboo words against arbitrary dictionary words is
insufficient because profanity may differ systematically in:
- length;
- frequency;
- morphology;
- borrowings;
- part of speech;
- register;
- expressive spelling.

Use matched controls and within-language inference first, then meta-analyze
effects across languages.

## Genealogy

Cross-language effect estimates are not independent.

Report:
- language-specific effects;
- family-aware sensitivity;
- leave-family-out stress tests only after the expanded language set has
  enough families.

The current 13-language Phase-0 set is too Indo-European-heavy for a strong
claim of phonological universality.

## Quality gate

A language enters the confirmatory phonology analysis only if:
- pronunciation coverage is adequate;
- a native/source-language audit of a stratified sample shows acceptable G2P
  validity;
- control-word matching is feasible;
- slang/multiword/OOV exclusions are reported;
- results are robust to excluding automatically generated pronunciations with
  low confidence.

Otherwise that language remains descriptive/exploratory.


## Live Epitran technical audit · 2026-09-19

A live smoke test with Epitran 1.35.2 was run against the checksum-verified
Study-1 inventory.

- 5,103 rows in the ten currently dependency-free routes were attempted;
- 5,103 / 5,103 returned technically usable output;
- 3,087 English/Mandarin/Cantonese rows were deliberately dependency-blocked;
- 995 / 5,103 attempted rows (~19.5%) were multiword.

This upgrades the track from package-level feasibility to executable technical
feasibility, but does not pass the pronunciation-validity gate.

See `process/G2P_TECHNICAL_AUDIT.md`.
