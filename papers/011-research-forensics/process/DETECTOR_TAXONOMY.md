# Detector taxonomy and evidence semantics

## Evidence classes

### E0 — metadata observation
Example: DOI resolves; registration exists; a correction is attached.

### E1 — deterministic contradiction
Reproducible mathematical/logical incompatibility under satisfied assumptions.
Examples: impossible discrete mean; incompatible p-value/test statistic; percentages cannot sum under stated denominator.

### E2 — externally verifiable provenance fact
Examples: a cited DOI does not correspond to the reference; an official retraction notice exists; registration date is later than the claimed prospective date.

### E3 — high-specificity forensic match
Examples: verified image duplication across ostensibly independent panels; high-confidence exact/near-exact text reuse after legitimate boilerplate exclusions.

### E4 — model-derived anomaly
Examples: paper-mill classifier score; semantic citation mismatch; learned image manipulation score; cross-document anomaly.

### E5 — weak/context-dependent heuristic
Examples: Benford deviation without a strong generative justification; generic AI-text classifier score; stylometric oddity.

Evidence classes are not guilt levels.

## Required detector contract

Every module MUST emit:

```json
{
  "detector_id": "grim",
  "detector_version": "...",
  "family": "numerical_forensics",
  "applicable": true,
  "applicability_reason": "...",
  "status": "FLAG | PASS | ABSTAIN | ERROR",
  "evidence_class": "E0-E5",
  "claim": "...",
  "evidence": {},
  "confidence": null,
  "calibration_reference": null,
  "benign_explanations": [],
  "misconduct_inference": false
}
```

PASS means the check was applicable and did not flag. ABSTAIN means it was not valid/applicable or evidence was insufficient.

## F1 — Statistical inference consistency

Candidate checks:
- statcheck-compatible t/F/chi-square/Z/r/Q patterns;
- recomputed p values;
- df vs stated N bounds;
- CI/effect-estimate consistency;
- effect/SE/z/p algebra;
- multiple-testing annotation.

Primary strength: deterministic and auditable when reporting pattern is parseable.

Main risks:
- corrections not stated in text;
- one- vs two-tailed assumptions;
- rounding;
- nonstandard tests;
- extraction errors.

## F2 — Discrete-summary and distributional forensics

Candidate checks:
- GRIM;
- GRIMMER;
- SPRITE;
- DEBIT;
- RIVETS / related integer-feasibility checks where validated;
- terminal-digit/heaping tests;
- Benford/Newcomb only when the data-generating process plausibly satisfies assumptions;
- variance/effect-size anomaly screens.

Rule: distributional heuristics cannot be upgraded to deterministic evidence.

## F3 — Table and arithmetic consistency

Candidate checks:
- percentages vs denominator;
- row/column totals;
- participant flow;
- repeated N inconsistencies;
- SD/SE confusion;
- duplicated impossible cells;
- subgroup totals exceeding parent group;
- abstract/table/text mismatch.

## F4 — Image/figure forensics

Candidate checks:
- within-paper duplicate panels;
- cross-paper duplicate figures;
- crop/rotation/mirror matches;
- copy-move;
- splicing/local inconsistency;
- western blot lane reuse;
- microscopy reuse;
- figure provenance and metadata where available.

Separate:
- duplication detection;
- manipulation classification;
- interpretation of whether reuse is legitimate.

## F5 — Citation forensics

Candidate checks:
- DOI/reference existence;
- metadata agreement (title/authors/year/journal);
- retracted/corrected cited work;
- citation-context semantic support;
- out-of-scope citations;
- suspicious citation concentration;
- citation-cartel/network patterns;
- fabricated references.

Do not infer misconduct merely because a cited paper was later retracted.

## F6 — Text / paper-mill signals

Candidate checks:
- exact/near duplicate passages;
- tortured phrases;
- template reuse;
- machine-learned paper-mill similarity;
- implausibly repeated title/abstract structures;
- phrase-family clustering across corpus.

Critical leakage rule: template relatives must be grouped across train/test splits.

## F7 — GenAI provenance

Candidate checks:
- model-specific watermark verification when technically available;
- generic AI-text classifiers;
- token/probability-derived provenance features;
- disclosure consistency.

Default evidence class: E5 for generic post-hoc detectors.

Watermark detection can be stronger only when:
- the generator supports the watermark;
- detector/version is known;
- text length/transformation assumptions are satisfied.

AI assistance is not itself research misconduct; the module only addresses provenance/disclosure questions defined by venue policy.

## F8 — Methods–results semantic coherence

Candidate checks:
- outcomes in Results absent from Methods;
- sample-size mismatches;
- analysis claimed without required inputs;
- abstract claims unsupported by Results;
- direction/magnitude contradictions;
- inconsistent variable labels.

Use LLMs as extractors/reasoners with source spans, not untraceable judges.

## F9 — Registration / ethics / provenance / identity consistency

Candidate checks:
- registry existence and date;
- prospective vs retrospective registration;
- outcome/protocol drift;
- ethics identifier existence/format where verifiable;
- ORCID/affiliation/email consistency;
- data/code availability statements;
- timeline impossibilities.

Identity mismatch is not misconduct by itself.

## F10 — Corpus/network forensics

Candidate graph entities:
- paper;
- author identifier;
- institution;
- journal/issue;
- editor/reviewer if legitimately available;
- citation;
- figure/image fingerprint;
- text-template fingerprint;
- reagent/material identifier;
- registration.

Candidate graph signals:
- dense reciprocal citation clusters;
- shared unusual reference lists;
- recurring template/image families;
- improbable author-paper structures;
- bursty cross-journal submission patterns where lawful data exist.

Network methods require especially careful confounding control: normal collaboration can resemble suspicious clustering.
