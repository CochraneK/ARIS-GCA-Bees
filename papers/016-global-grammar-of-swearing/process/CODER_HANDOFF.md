# ARIS4C016 Independent Coder Handoff

Updated: 2026-09-19

## Task

Independently code the deterministic ARIS4C016 ontology audit sample.

**Do not read another coder's output before completing your own.**

Canonical documents:
- `process/ONTOLOGY_V0.md`
- `process/RELIABILITY_PROTOCOL.md`
- `data/ontology_v0.schema.json`

Sampler:
- `code/build_audit_sample.py`

Private review-sheet generator:
- `code/export_private_coding_sheet.py`

## Scientific purpose

The task is not to maximize the number of labels assigned.

The purpose is to estimate whether different coders can apply the multi-axis
ontology consistently across languages and to identify where native/context
knowledge is required.

Use `UNRESOLVED`, `UNKNOWN_TARGET`, or `CONTEXT_REQUIRED` whenever the
available evidence does not justify a stronger label.

## Input

The private coding sheet contains:
- stable row ID/hash;
- community sample;
- original lexical expression;
- English translation when available;
- source category labels;
- source production frequency.

The sheet must remain private because it can contain identity slurs and other
highly offensive lexical material.

## Coding rules

### Semantic source
Code what semantic domain supplies the taboo/derogatory material.

Do not code a semantic domain merely because the original source says
`insult` or `slur`.

### Target
Code who/what is targeted only when lexically/contextually supported.

### Pragmatic function
If isolated lexical form is insufficient to distinguish direct insult,
expletive, intensifier, teasing, etc., use `CONTEXT_REQUIRED`.

### Social-indexical basis
Do not infer a protected/social identity solely from an English translation
if the source-language usage is ambiguous.

### Mechanism
This is interpretive. Prefer `UNKNOWN_MECHANISM` over speculative
psychological interpretation.

### Confidence
- HIGH: native/context evidence directly supports label;
- MEDIUM: strong source annotation + defensible translation/context;
- LOW: translation-heavy inference;
- UNRESOLVED: insufficient evidence.

## Native-language escalation

Flag `native_review_required=true` when:
- translation is absent/ambiguous;
- local political/historical meaning matters;
- morphology changes target/intensity;
- expression is slang/code-switching;
- identity/slur interpretation is uncertain;
- pragmatic meaning depends on register.

Do not silently use web snippets as a substitute for native-language
verification.

## Required output

One JSONL or CSV row per sampled item containing:
- row_hash;
- semantic_source[];
- target[];
- pragmatic_function[];
- social_indexical_basis[];
- taboo_mechanism[];
- confidence;
- native_review_required;
- short evidence note.

Do **not** change ontology labels during coding.

If an ontology problem is found, record it in a separate
`ontology_change_requests` section after coding.

## Independence rule

Coder output becomes frozen evidence once submitted.

Ontology changes are discussed only after:
1. Coder A frozen;
2. Coder B frozen;
3. agreement statistics computed.

This prevents the ontology from being tuned to make coders agree.

## Acceptance

A coder run is acceptable when:
- every sampled row has an output;
- unresolved cases are retained;
- no other coder output was consulted;
- any external/native evidence used is noted;
- no raw offensive lexical dataset is committed to the public repository.

## After both coders finish

Run:
1. exact-set agreement;
2. per-axis Jaccard;
3. labelwise prevalence/raw agreement;
4. kappa / Gwet AC1 where appropriate;
5. community-stratified disagreement;
6. native-review queue.

Only then adjudicate.


## Executable handoff

Generate Coder A's private sheet **outside the repository**:

```bash
python code/export_private_coding_sheet.py \
  --output /PRIVATE/PATH/aris4c016_coder_a.csv \
  --coder-id A
```

Generate Coder B independently with a different private output path and
`--coder-id B`.

The exporter:
- regenerates the frozen deterministic sample;
- verifies the Study-1 source SHA-256;
- verifies the frozen 300-row manifest SHA-256;
- refuses by default to write raw taboo/slur content anywhere inside the
  ARIS4C repository.

After both frozen outputs are returned, calculate aggregate reliability:

```bash
python code/score_coder_reliability.py \
  /PRIVATE/PATH/aris4c016_coder_a.csv \
  /PRIVATE/PATH/aris4c016_coder_b.csv \
  --output /PRIVATE/PATH/aris4c016_reliability.json
```

The reliability output contains aggregate statistics and disagreement row
hashes only; it does not emit raw lexical expressions.

Canonical frozen-sample identity:
`48c58f91901e8c2a1aab01958e95ea28afaf0f33e7a98677f98e58b8a412c9b4`.
