# ARIS4C016 G2P Feasibility Matrix

Updated: 2026-09-19

## Question

Can the Phase-0 taboo dataset receive a reproducible pronunciation layer without
pretending that the sparse source `transcription` field is a global IPA resource?

## Result

The official Epitran repository provides a plausible orthography-to-IPA route
for **all 13 project languages**, but package support is not evidence of
validated pronunciation coverage.

Classic-map candidates:
- Dutch — `nld-Latn`
- Finnish — `fin-Latn`
- French — `fra-Latn`
- German — `deu-Latn`
- Italian — `ita-Latn`
- Serbian — `srp-Latn` / `srp-Cyrl`
- Setswana — `tsn-Latn`
- Slovenian — `slv-Latn`
- Spanish — `spa-Latn` (Iberian sensitivity: `spa-Latn-eu`)
- Thai — `tha-Thai`

Special-dependency routes:
- English — `eng-Latn`, requiring **Flite + lex_lookup**;
- Mandarin — `cmn-Hans` / `cmn-Hant`, requiring **CC-CEDict**;
- Cantonese — `yue-Hant`, requiring **CC-Canto**; `yue-Latn` supports Jyutping.

## Caveats

### English
One generic G2P does not encode AU/CA/GB/SG/US dialectal pronunciation
differences. Generic English IPA can support a lexical-form sensitivity
analysis, not community-specific phonology claims.

### Mandarin / Cantonese
Character G2P is dictionary-backed. Cantonese also has lexical ambiguity; the
official Epitran documentation warns that isolated characters can have multiple
pronunciations. Quality must therefore be audited on the actual inventory.

### Serbian
Backend selection must be script-aware rather than forcing all rows through
Latin or Cyrillic.

### Spanish
Use generic `spa-Latn` for the primary CL/ES comparison so backend selection
is not confounded with community. Treat `spa-Latn-eu` as a Spain sensitivity.

### Slang / multiword / code-switching
Taboo inventories contain creative spelling, slang, abbreviations,
code-switching, masking and multiword expressions. A backend can technically
return IPA while still being linguistically wrong.

Coverage therefore has two levels:
1. **technical success** — usable IPA returned;
2. **validated success** — pronunciation passes source-language audit.

## Confirmatory phonology gate

Before testing the approximant hypothesis:
1. report G2P success/failure by community;
2. report exclusion reasons;
3. compare taboo and matched-neutral coverage;
4. audit a stratified pronunciation sample;
5. freeze the analyzable language set;
6. then run the preregistered phonological test.

## Canonical metadata

See `data/pronunciation_backend_matrix.json`.

## Next executable step

Run `code/g2p_coverage_audit.py` in an environment with Epitran installed.

The audit must checksum-verify Study 1, never print raw taboo forms, emit only
aggregate success/failure counts, distinguish dependency failures from G2P
failures, and separately flag multiword and mixed-script inputs.
