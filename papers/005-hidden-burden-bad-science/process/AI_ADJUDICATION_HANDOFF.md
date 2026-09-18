# AI ADJUDICATION HANDOFF — ARIS4C005

## Purpose

This file is the operational handoff for the external/other model that will replace most manual article-level adjudication.

The model is an **AI adjudicator**, not an oracle. Outputs remain noisy measurements and must follow the frozen ontology and prompt.

Canonical instructions:

- `process/AI_ADJUDICATION_PROTOCOL.md`
- `process/AI_ADJUDICATION_PROMPT_V1.md`
- output schema: `data/ai_adjudication_output_template.csv`

---

## Input package

Canonical scaled-audit artifact:

- workflow run ID: `35301945169`
- artifact ID: `10529404069`
- artifact name: `aris4c005-scaled-ai-audit`
- artifact SHA-256 digest: `065230382d1f69f98ebb4ce189158c93a5b00f5e3ac2f46aa877bd51587af699`

The artifact contains:

1. `aris4c005_scaled_random_audit.csv` — 10,000 sampled works with sampling metadata.
2. `aris4c005_scaled_ai_reviewer_packet.csv` — 20,000 blinded assignments.
3. `aris4c005_scaled_ai_manager_linkage.csv` — manager-only linkage/sampling metadata.
4. `aris4c005_ai_batches/` — 80 deterministic model-input batches.

Do not expose manager linkage to the adjudicating model.

---

## Execution rule

AI_A and AI_B must be independent.

Preferred:

- different strong model families/providers;
- fresh context for every batch;
- fixed prompt `AI-ADJ-V1`;
- no sharing of AI_A results with AI_B;
- deterministic batch bookkeeping;
- model/version/run metadata returned for every row.

If only one model family is available, run two fresh independent passes and explicitly report correlated-error risk.

---

## Batch naming

Input batches are already named:

- `AI_A_batch_001.csv` … `AI_A_batch_040.csv`
- `AI_B_batch_001.csv` … `AI_B_batch_040.csv`

Recommended completed-output names:

- `AI_A_batch_001_output.csv` …
- `AI_B_batch_001_output.csv` …

Do not reorder or regenerate assignment IDs.

---

## Per-row required outputs

Return:

- assignment_id
- paper_id
- adjudicator_id
- model_name
- model_version_or_snapshot
- prompt_version = `AI-ADJ-V1`
- run_id
- scientific_state
- materiality
- misconduct_evidence
- publication_process_state
- review_confidence
- fulltext_seen
- notice_seen
- formal_finding_seen
- evidence_locator
- brief_evidence_rationale
- abstain_reason

`brief_evidence_rationale` is a short evidence summary, not hidden chain-of-thought.

---

## Mandatory abstention behavior

The model must not force a binary verdict.

Use:

- `SERIOUS_UNRESOLVED` when serious evidence exists but material unreliability is not established;
- `INDETERMINATE` when source access/evidence is too incomplete or contradictory.

Missing DOI is **not** an integrity signal.

---

## After both model passes

Concatenate AI_A outputs and AI_B outputs separately, then run:

`code/merge_ai_adjudications.py`

This produces:

- automatic dual-AI agreement records;
- an arbitration queue;
- agreement/QA summary.

Automatic dual agreement is labelled:

`AI_DUAL_AGREEMENT_NOT_GOLD_STANDARD`

Cases route to arbitration when scientific state/materiality disagrees, confidence is LOW, either pass is INDETERMINATE, or formal-finding evidence conflicts.

---

## Calibration requirement

Before weighted prevalence inference:

1. measure dual-model agreement/abstention;
2. evaluate high-confidence anchor cases;
3. estimate or sensitivity-test AI sensitivity/specificity;
4. preserve field/year/access missingness;
5. fit the final measurement-error / latent model.

Do not calculate:

`AI positive rows / 10,000 = global fraud prevalence`

That shortcut is explicitly invalid.

---

## Why specificity is critical

For a hypothetical true prevalence of 0.5% and sensitivity 90%, design analysis shows approximately:

- specificity 99.0% -> PPV ~31%
- specificity 99.5% -> PPV ~47%
- specificity 99.9% -> PPV ~82%
- specificity ~99.95% -> PPV ~90%

So rare-event estimation can be dominated by false positives even when a model appears highly accurate overall.

---

## Completion criterion

The AI-adjudication stage is complete only when:

- all 20,000 assignments are accounted for;
- no assignment ID duplicates/mismatches;
- A/B independence preserved;
- arbitration completed under a frozen rule;
- model/version/prompt provenance complete;
- calibration/sensitivity analysis available.
