# CITATION-EDGE AI ADJUDICATION HANDOFF — ARIS4C005

## Purpose

This is the operational handoff for the second AI task: deciding whether a post-retraction citation is merely exposure or represents material scientific dependence.

Canonical instructions:

- `process/CONTAMINATION_PROTOCOL.md`
- `process/CITATION_AI_ADJUDICATION_PROMPT_V1.md`
- semantic summary code: `code/citation_dependence.py`

## Real input package

The live pipeline contains:

- **486 unique post-retraction citation edges**
- **972 blinded AI assignments**
- `CIT_AI_A`: 486 assignments
- `CIT_AI_B`: 486 assignments
- batch size: 100
- total batches: **10**
- 200 edges with OpenAlex full-text signal
- 290 edges with OA signal

Full-text/OA are access variables, not evidence of contamination.

## Batch naming

- `CIT_AI_A_batch_001.csv` … `CIT_AI_A_batch_005.csv`
- `CIT_AI_B_batch_001.csv` … `CIT_AI_B_batch_005.csv`

The fifth batch contains 86 assignments for each adjudicator.

## Required semantic labels

Exactly one primary class:

- `BACKGROUND_MENTION`
- `METHOD_REUSE`
- `RESULT_DEPENDENCE`
- `EVIDENCE_SYNTHESIS_INCLUDE`
- `CRITIQUE_OR_CORRECTION`
- `CITATION_ONLY_OR_PERIPHERAL`
- `INDETERMINATE`

Secondary fields:

- `component_implicated`
- `material_to_downstream_claim`
- `source_retraction_known_in_text`
- `context_access`
- `review_confidence`

Do not classify from title alone when citation context is unavailable.

## Primary SCF rule

An adjudicated edge enters primary Scientific Contamination Footprint only when:

- semantic class is `RESULT_DEPENDENCE` or `EVIDENCE_SYNTHESIS_INCLUDE`, and
- `material_to_downstream_claim=YES`.

`METHOD_REUSE` is reported separately unless the reused component is itself implicated and materially affects the downstream work.

`CRITIQUE_OR_CORRECTION` is corrective propagation, not contamination.

## Batch-output integrity gate

Before semantic merging, name completed files:

- `CIT_AI_A_batch_001_output.csv` … `CIT_AI_A_batch_005_output.csv`
- `CIT_AI_B_batch_001_output.csv` … `CIT_AI_B_batch_005_output.csv`

Run:

`python code/collect_ai_batch_outputs.py data/pilot/citation_ai_batch_manifest.json <completed_output_dir> <collected_dir> <collection_summary.json> --mode citation`

The collector verifies exact edge assignments/checksums, row counts, adjudicator and prompt identity, controlled semantic vocabularies, duplicate assignments and abstention requirements before creating collected A/B outputs.

Successful collection is an integrity check on the files, not evidence that semantic labels are correct.

---

## After both AI passes

Preserve A/B outputs separately and build a disagreement/arbitration layer before calling `citation_dependence.py`.

The existing semantic summary must retain:

- raw citation exposure,
- material dependence,
- methodological contamination,
- corrective citations,
- indeterminate/context-missing cases

as separate quantities.

## Downstream result

Once semantic labels are calibrated, the project can upgrade:

`Citation Ghost Half-Life -> Dependence Ghost Half-Life`

and estimate SCF without equating every citation with contamination.
