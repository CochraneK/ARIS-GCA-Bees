# ARIS4C011 · Confirmatory issue-adjudication protocol v0

Status: **FROZEN FOR FIRST-PASS ADJUDICATION**  
Machine contract: `data/protocol/confirmatory_adjudication_protocol_v0.json`

## Purpose

This protocol governs the manager-side coding of the frozen 80-record feasibility frame **before detector scoring**. It determines what the official/public source actually documents, whether the labelled issue is content-assessable, and which historical artifact role would be required to test it.

Adjudication does **not** make a paper confirmatory-eligible. Eligibility is decided later, after time-safe artifact qualification and the remaining freeze gates.

## Evidence hierarchy

Use the strongest available primary source: official publisher notice first; then PubMed/PMC structured notice/preserved notice; then institutional/journal investigation statements; then other primary public records. Secondary commentary can point to a source but cannot by itself create GT-A/B/C ground truth.

Detector output, finding count, review priority, anomaly/model score, or whether a detector happened to succeed during development are prohibited inputs.

## Issue families

- **statistical_reporting** — statistical value/model/analysis/inference reporting error.
- **data_fabrication_falsification** — only when primary evidence specifically supports fabricated/falsified/manipulated data.
- **image_integrity** — figure/image duplication, manipulation, assembly, or image-content issue.
- **plagiarism_text_duplication** — plagiarism, text overlap, duplicate/redundant publication.
- **paper_mill** — only when primary evidence specifically identifies paper-mill/industrial fabrication.
- **authorship_peer_review** — authorship, gift/ghost authorship, peer-review or editorial-process manipulation.
- **citation_reference** — citation/reference existence, attribution, metadata, or manipulation issue.
- **registration_ethics_provenance** — protocol, registration, ethics, consent, provenance, identifier, or timeline issue.
- **methods_results_coherence** — methods/results/abstract/caption/scope mismatch not better captured above.
- **other_unclear** — official issue exists but is nonspecific or outside the frozen vocabulary.

Multiple codes are allowed when the source documents distinct sub-issues.

## Ground-truth tiers

- **GT-A:** official notice explicitly identifies the issue.
- **GT-B:** correction/corrigendum explicitly documents a concrete error.
- **GT-C:** primary-source institutional/journal investigation documents the issue.
- **GT-D:** reproducible public forensic finding without official adjudication; exploratory only.
- **GT-E:** suspicion/commentary only; not positive confirmatory ground truth.

Update type alone does not determine the tier.

## Content detectability and required artifact role

`CONTENT_ASSESSABLE` requires at least one concrete role such as body text, table, figure image, references, raw data, supplement, registration/protocol, metadata timeline, or cross-source reference.

`PROCESS_ONLY` uses `none_content_detectable`. It must not be scored as a Track-A false negative simply because a manuscript-content detector cannot observe a gift-authorship or peer-review-process issue.

`MIXED` is used when the same record documents both content-assessable and process-only sub-issues. `UNCLEAR` is used when the manager evidence is insufficient.

## Frozen safeguards

1. Generic retractions are not upgraded to fabrication/falsification, paper-mill activity, or intent without explicit primary evidence.
2. Current status-prefixed titles and update relations are manager-side provenance only and never Track-A features.
3. Coding must cite/record the manager evidence source; ambiguity is preserved rather than guessed away.
4. Adjudication cannot set confirmatory eligibility.
5. Any ontology change after first-pass coding begins requires a dated amendment and an explicit remap of old codes.

## Next step

Acquire the strongest available notice evidence for each of the 80 frozen rows, code a first-pass manager file under this protocol, retain uncertainty, and only then begin required-role historical artifact qualification.
