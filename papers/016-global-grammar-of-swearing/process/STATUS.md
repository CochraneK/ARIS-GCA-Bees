# ARIS4C016 Status

Updated: 2026-09-19

## Stage

**Phase 0 bilingual working paper · semantic reliability gate frozen · pronunciation route technically complete.**

Portfolio maturity: **68% · block**.

The project is empirically active at Phase 0, but confirmatory semantic
fingerprints remain blocked on genuinely independent Coder A/B plus
native-language review. The phonology track has separately passed its
engineering-feasibility gate and is now blocked on pronunciation validity,
matched controls, and confirmatory freezing rather than tool coverage.

## Completed

### Scientific framing
- canonical research question defined;
- novelty reframed away from a simple swear-word dictionary;
- falsification-first hypothesis hierarchy drafted;
- language/community/country/genealogy separation specified;
- phylogenetic pseudoreplication recognized as a primary design threat;
- public-output ethics for slurs and identity-targeting language specified.

### Data / provenance
- Sulpizio et al. Study-1/Study-2 public OSF sources identified;
- source GUIDs and SHA-256 provenance frozen;
- raw third-party data intentionally not vendored because no project-level OSF
  license is displayed;
- reproducible checksum-verified download/audit scripts added.

### Measurement / ontology
- Study-1/Study-2 structure audited directly;
- elicitation-yield, missingness and multi-label heterogeneity quantified;
- original flat category field shown to mix semantic, pragmatic and
  social-indexical levels;
- orthogonal multi-axis taboo ontology v0 + machine-readable schema added;
- conservative harmonization v0 quantified;
- naïve semantic fingerprint attempted and rejected as measurement-biased.

### Genealogy / repeated-language identification
- 18 community samples linked to 13 Glottolog language IDs / 5 top-level
  families;
- English and Spanish repeated-language structure separated from language-level
  evidence;
- English repeated-item community-variation diagnostic completed;
- item-fixed-effects FWL model completed;
- all-five-English balanced sensitivity completed;
- sparse filler negative control completed, showing current community effects
  are not demonstrably taboo-specific.

### Reliability gate
- deterministic 300-row multilingual ontology audit sample frozen;
- frozen manifest SHA-256:
  `48c58f91901e8c2a1aab01958e95ea28afaf0f33e7a98677f98e58b8a412c9b4`;
- independent-coder protocol and handoff implemented;
- protected private coding-sheet exporter implemented;
- aggregate reliability scorer implemented;
- scorer enforces identity of the frozen manifest before computing agreement.

**2026-09-19 defect found: the frozen manifest digest is not reproducible from
the committed sampler.** Re-running
`code/build_audit_sample.py` against the checksum-verified OSF source is
deterministic across fresh runs and reproduces the frozen *structure* exactly
(300 rows; 16 × 15 + Setswana 30 + Spanish 30; strata 42 / 116 / 61 / 81), but
yields
`910a47c353a7ebbe0ccbe48c0001fea536c9f24e9cb6242dcec46d9e3e541751`, and none of 86
tested serialisations gives `48c58f91…`. The private-sheet exporter and the
reliability scorer therefore fail closed, so the Coder A/B gate cannot start. This
is a record/tooling defect, not evidence about the phenomenon, and no coding may
begin on the unreproducible draw. See
`process/MANIFEST_DIGEST_MISMATCH.md` and
`data/manifest_digest_diagnosis.json` for the ranked explanations (recover the
original artifact, or supersede the freeze with a new versioned manifest hash under
the freeze document's own replacement rule) and the cross-check digests.

### Manuscript / figures
- English working manuscript established;
- Chinese working manuscript established;
- three public-safe SVG figures added;
- public command center links both manuscripts.

### Phonology / pronunciation engineering
- source `transcription` field shown not to be a common global IPA layer;
- pronunciation backend matrix frozen for all 13 languages;
- Epitran 1.35.2 live technical audit executed;
- Flite `lex_lookup` compiled from official Flite source for English G2P;
- Flite source commit frozen:
  `6c9f20dc915b17f5619340069889db0aa007fcdc`;
- Cantonese and Mandarin upgraded to source-romanization → IPA routes rather
  than character-level dictionary guessing;
- full-route technical pronunciation audit completed:
  **8,187 / 8,190 rows = 99.9634% technical success**;
- remaining three non-success rows are 2 English (SG) empty/non-letter outputs
  and 1 Mandarin row lacking source transcription;
- runtime provenance frozen in `data/phonology_runtime_lock.json`.

Technical G2P success is explicitly **not** treated as pronunciation validity.

## Immediate next gates

### Semantic / ontology gate — external and independent
0. Resolve the frozen-manifest digest mismatch (recover `48c58f91…` or record a
   superseding versioned manifest). Until then no private sheet can be exported.
1. Generate private Coder A and Coder B sheets from the frozen sample.
2. Complete genuinely independent coding; neither coder sees the other's
   output before freezing.
3. Run axis/label reliability and community-stratified disagreement analyses.
4. Adjudicate only after raw A/B labels are frozen.
5. Promote ontology version only after reliability diagnostics.
6. Build the first measurement-corrected semantic fingerprints only on axes
   that pass the reliability gate.

### Phonology gate — validation, not coverage
1. Freeze a stratified pronunciation-validation sample.
2. Oversample slang, creative spelling, multiword forms, borrowing/code-switching
   and unusual automated segments.
3. Obtain native/source-language pronunciation review.
4. Quantify validated success by language and error stratum.
5. Freeze segment normalization / approximant coding.
6. Build matched neutral controls.
7. Run the preregistered Lev-Ari & McKay approximant replication.

### Later expansion
- ontology-domain × community repeated-item models;
- purpose-designed matched taboo/neutral interaction test;
- missing/unresolved-content sensitivity bounds;
- genealogy-aware cross-language tests;
- crossed language × country expansion with broader family diversity.

## Current blockers

- the frozen 300-row manifest digest cannot be reproduced from the committed
  sampler, so the private coder sheets cannot be exported and the Coder A/B gate
  cannot start (maintainer decision required, see
  `process/MANIFEST_DIGEST_MISMATCH.md`);
- genuinely independent/native-speaker ontology coding has not yet been
  executed;
- pronunciation technical coverage is high, but pronunciation validity has not
  been independently/native-language audited;
- 17 countries are too few for aggressive country-level cultural regression;
- most language and country effects remain confounded outside repeated-language
  subsets;
- language-family coverage remains Indo-European-heavy;
- expansion sampling and ethics review are not yet frozen.

## Current claim boundary

Allowed now:
- annotation protocols differ substantially across samples;
- raw semantic category profiles are not directly comparable;
- lexical identity strongly structures English taboo ratings;
- modest community-associated variation remains after lexical-item fixed
  effects;
- current community effects are not shown to be taboo-specific;
- all 13 project languages now have an engineering-feasible pronunciation
  route, with 99.9634% technical row coverage in the current pipeline.

Still blocked:
- country/community semantic-domain fingerprints as confirmatory results;
- causal cultural explanations;
- strong global universality claims;
- a claim that 99.9634% G2P technical success means pronunciation accuracy;
- a claim that ARIS4C016 independently replicated the approximant hypothesis.

## Promotion rule

The earlier reproduction/variance-decomposition promotion gate has been
passed. The next promotion requires **independent measurement reliability**:
semantic claims require the frozen Coder A/B gate, and phonological claims
require native/source-language pronunciation validation plus matched controls.
