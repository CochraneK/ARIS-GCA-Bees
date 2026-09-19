# ARIS4C016 Chinese Romanization → IPA Pilot

Updated: 2026-09-19

## Motivation

The initial phonology plan treated Mandarin and Cantonese character G2P as
dictionary-dependent:
- Mandarin character mode requires CC-CEDict;
- Cantonese character mode requires CC-Canto.

However, the source Study-1 dataset already contains a high-coverage
`transcription` field for the Chinese samples. The better Phase-0 route is
therefore to test whether this **source-provided romanization** can be passed
through Epitran's romanization backends, avoiding character-level
pronunciation disambiguation.

## Source transcription audit

### Cantonese (CN)
- rows: 632;
- non-empty source transcription: 632 / 632;
- 600 / 632 contain digits consistent with tone-number romanization;
- 581 / 632 contain whitespace;
- no non-Latin letters detected in the transcription field.

### Mandarin (CN)
- rows: 302;
- non-empty source transcription: 301 / 302;
- all 301 non-empty values contain digits;
- 2 / 301 contain whitespace;
- no non-Latin letters detected.

The high Cantonese whitespace rate must **not** be interpreted as 581
multiword lexical expressions: in a romanization field, spaces may be syllable
or morpheme separators.

## Live technical conversion

Execution environment:
- Epitran 1.35.2;
- source Study-1 checksum verified.

Backends:
- Cantonese: `yue-Latn`, tones enabled;
- Mandarin: `cmn-Latn`, tones enabled.

Technical result:
- Cantonese: 632 / 632 returned non-empty letter-containing output;
- Mandarin: 301 / 301 non-empty source transcriptions returned output;
- no conversion exceptions in either sample.

No lexical forms or IPA strings were printed in the audit output.

## Consequence

For the existing Phase-0 dataset, Chinese pronunciation does **not** need to
start from character-level dictionary lookup.

Preferred route:

```
source expression
  ↓
source-provided Pinyin / Jyutping-like transcription
  ↓
Epitran cmn-Latn / yue-Latn
  ↓
IPA candidate
  ↓
native/source-language validation
```

This reduces one important source of polyphonic-character ambiguity and avoids
making the confirmatory pronunciation layer depend immediately on
CC-CEDict/CC-Canto.

## Combined technical feasibility

Using:
- the ten dependency-free orthography routes: 5,103 rows;
- Cantonese source-romanization route: 632 rows;
- Mandarin source-romanization route: 301 rows;

the current pipeline has a technical pronunciation route for:

**6,036 / 8,190 Study-1 rows = 73.7%.**

The remaining **2,153 rows (26.3%)** are the five English community samples,
for which the official Epitran English route requires Flite / `lex_lookup`.

This remains an engineering coverage estimate, not validated pronunciation
coverage.

## New quality questions

### Cantonese no-digit subset
32 Cantonese transcription rows lack tone digits. They must be audited rather
than silently treated as equivalent to the dominant tone-number format.

### Segmentation
The source romanization may contain syllable separators. The pipeline should
preserve a distinction between:
- lexical multiword status from `word_clean`;
- whitespace inside the pronunciation/transcription representation.

### Tone handling
The preregistered approximant hypothesis concerns segment classes rather than
tone. Primary approximant analyses can report tone-insensitive segment results,
but the raw tone-bearing representation should be preserved for future
exploratory work.

## Scientific status

This pilot upgrades Mandarin/Cantonese from
`BLOCKED_BY_DICTIONARY_DEPENDENCY` to
`TECHNICALLY_FEASIBLE_VIA_SOURCE_ROMANIZATION`.

Promotion to confirmatory phonology still requires:
- pronunciation audit;
- handling of the Cantonese no-digit subset;
- matched neutral controls;
- frozen segment-class coding.
