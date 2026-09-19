# ARIS4C016 G2P Technical Coverage Audit

Updated: 2026-09-19

## Scope

This audit asks only whether the current Study-1 lexical inventory can be
passed through the planned Epitran pronunciation backends without technical
failure.

It is **not** a pronunciation-accuracy validation.

Environment used for the live smoke:
- Epitran 1.35.2;
- public Study-1 CSV checksum verified before execution;
- English / Mandarin / Cantonese intentionally pre-blocked because their
  documented external dependencies were not frozen into the ARIS4C pipeline;
- no lexical forms or IPA strings were emitted.

Reproducible script:
`code/g2p_coverage_audit.py`

## Overall result

Study 1 contains 8,190 lexical rows.

- **5,103 rows** belonged to the ten language routes that do not require the
  special English/Chinese dependency layer in the current audit.
- All **5,103 / 5,103** returned technically non-empty, letter-containing
  Epitran output.
- **3,087 rows** were deliberately marked `BLOCKED_BY_DEPENDENCY` rather than
  silently processed:
  - five English samples;
  - Mandarin;
  - Cantonese.

This is a strong engineering-feasibility result, but not evidence that 100% of
those 5,103 pronunciations are linguistically correct.

## Technical success by community

| Community | Rows | Attempted | Technical success |
|---|---:|---:|---:|
| Dutch (BE) | 704 | 704 | 100% |
| Finnish (FI) | 432 | 432 | 100% |
| French (FR) | 179 | 179 | 100% |
| German (DE) | 863 | 863 | 100% |
| Italian (IT) | 441 | 441 | 100% |
| Serbian (RS) | 975 | 975 | 100% |
| Setswana (BW) | 275 | 275 | 100% |
| Slovenian (SI) | 351 | 351 | 100% |
| Spanish (CL) | 216 | 216 | 100% |
| Spanish (ES) | 413 | 413 | 100% |
| Thai (TH) | 254 | 254 | 100% |

Dependency-blocked:
- Cantonese (CN): 632 rows;
- Mandarin (CN): 302 rows;
- English AU/CA/GB/SG/US: 2,153 rows total.

## Multiword warning

Among the 5,103 technically attempted rows, **995 (~19.5%)** contain
whitespace/multiword forms.

This is a major validity warning.

A G2P backend can return IPA for a multiword expression while:
- token boundaries are linguistically non-trivial;
- slang spelling may be non-standard;
- the expression may contain borrowed/code-switched material;
- morphosyntactic context may change pronunciation.

Therefore technical success is an upper bound on usable phonological coverage.

Across all 8,190 Study-1 rows, 1,677 were flagged as multiword.

## Dependency strategy

### English
Do not install/use a generic English Flite layer and then claim
AU/CA/GB/SG/US community phonology differences.

Primary use:
- generic lexical-form replication of the prior approximant hypothesis.

Community phonology requires a dialect-sensitive pronunciation source.

### Mandarin / Cantonese
The dictionaries must be separately frozen with:
- version / retrieval date;
- license;
- checksum;
- backend settings.

Only then should technical coverage be rerun.

## Interpretation

The phonology track is **technically feasible** for the ten currently
dependency-free routes. This substantially reduces the risk that the project
would need to abandon cross-language pronunciation analysis altogether.

However, the next scientific gate is pronunciation validity, not additional
G2P throughput.

A stratified native/source-language pronunciation audit must deliberately
oversample:
- multiword expressions;
- creative spellings;
- low-frequency slang;
- code-switching / borrowing;
- source rows where automated IPA contains unusual segments.

## Next gate

1. Freeze external English/Chinese pronunciation dependencies.
2. Generate a de-identified pronunciation-audit sample.
3. Compare automated pronunciation against source/native judgement.
4. Establish per-language validated-success rates.
5. Only then construct matched neutral controls and test the preregistered
   approximant hypothesis.
