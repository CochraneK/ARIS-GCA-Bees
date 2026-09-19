# ARIS4C016 Full-Route Pronunciation Technical Audit

Updated: 2026-09-19

## Result

A complete technical pronunciation route was executed across all 8,190
Study-1 lexical rows.

Runtime:
- Epitran 1.35.2;
- Flite source commit
  `6c9f20dc915b17f5619340069889db0aa007fcdc`;
- `lex_lookup` compiled according to Epitran's official installation
  instructions;
- Study-1 source checksum verified.

Routing:
- ordinary orthography → language/script-specific Epitran;
- English orthography → `eng-Latn` / Flite `lex_lookup`;
- Cantonese source transcription → `yue-Latn`, tones enabled;
- Mandarin source transcription → `cmn-Latn`, tones enabled;
- Serbian chooses Latin vs Cyrillic backend from observed script.

## Overall engineering coverage

- total rows: **8,190**
- technical success: **8,187**
- technical success rate: **99.9634%**
- empty/non-letter output: 2
- missing route input: 1
- backend exceptions: 0

The three non-success rows consist of:
- 2 English (SG) rows with empty/non-letter output;
- 1 Mandarin row with no source transcription.

No lexical form or generated IPA string was emitted by the audit.

## Route counts

- orthography route: **7,256 rows**
- Chinese source-romanization route: **934 rows**

Among the orthography-route rows:
- **1,668** are lexical multiword expressions.

Among the Chinese romanization rows:
- **583** contain whitespace in the transcription representation.

These are different phenomena and must not be conflated. Chinese transcription
whitespace can represent syllable/morpheme segmentation rather than multiple
lexical words.

## Community-level technical results

All rows returned technical output in:
- Cantonese (CN)
- Dutch (BE)
- English (AU)
- English (CA)
- English (GB)
- English (US)
- Finnish (FI)
- French (FR)
- German (DE)
- Italian (IT)
- Serbian (RS)
- Setswana (BW)
- Slovenian (SI)
- Spanish (CL)
- Spanish (ES)
- Thai (TH)

Exceptions:
- English (SG): 375 / 377 = 99.47%
- Mandarin (CN): 301 / 302 = 99.67%

## What this establishes

The Phase-0 phonology program is no longer blocked by broad technical language
coverage.

A common computational pronunciation layer is **engineering-feasible** for all
13 project languages.

## What this does not establish

It does **not** establish 99.96% pronunciation accuracy.

Potential non-random errors remain especially important for:
- slang;
- creative/phonetic spellings;
- abbreviations;
- compounds and multiword expressions;
- borrowed/code-switched forms;
- orthographically ambiguous French/English items;
- dialect-sensitive English pronunciation;
- tone/segmentation conventions in source Chinese romanization.

A backend returning IPA is not sufficient evidence that the IPA is correct.

## Consequence for the approximant hypothesis

The next step is no longer "find a G2P tool."

It is:

1. freeze a pronunciation-validation sample;
2. independently/source-language audit automated pronunciation;
3. quantify validated success by language and error stratum;
4. define segment normalization / approximant coding;
5. build matched neutral controls;
6. only then test the preregistered Lev-Ari & McKay approximant hypothesis.

## Reproducibility

- backend metadata:
  `data/pronunciation_backend_matrix.json`
- runtime lock:
  `data/phonology_runtime_lock.json`
- full-route audit:
  `code/g2p_full_route_audit.py`
- initial dependency-aware audit:
  `code/g2p_coverage_audit.py`
- Chinese route pilot:
  `process/CHINESE_ROMANIZATION_PILOT.md`
