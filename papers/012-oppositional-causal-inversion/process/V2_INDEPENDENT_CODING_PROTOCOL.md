# V2 independent A2/B2 coding protocol — ARIS4C012

Frozen operational rule: 2026-09-19

## Purpose

Validate `SCHEMA_V2_FROZEN.md` on the fresh V201–V230 sample without repeating the Pilot-0 independence failure mode.

## Independence boundary

A2 and B2 must be **genuinely separate coding executions**. One model/session may not be duplicated and presented as two independent coders.

Both coders receive exactly the bundle named by their input-freeze manifest:

- the same `common_evidence_packet.jsonl`;
- the same frozen Schema v2;
- byte-identical blank response forms.

A2 must not read B2 labels; B2 must not read A2 labels. Neither may read Pilot-0 labels, Pilot-0 disagreement diagnosis, or any v2 adjudication while coding.

## Git / execution isolation

Preferred workflow:

1. start both coders from the same packet-freeze commit;
2. A2 works on an isolated branch or execution surface and edits only its own copy of the response file;
3. B2 works on a separate isolated branch or execution surface and edits only its own copy;
4. each coder runs `freeze_v2_coder.py` after all 30 rows are complete;
5. preserve each completed-response SHA-256 and completion freeze;
6. only **after both freezes exist** may the two completed files be brought into one integration state for agreement scoring.

Do not merge A2 labels into `main` while B2 is still coding, or vice versa.

## Coder task

For every V201–V230 record:

- use only the supplied evidence packet;
- code exact controlled tokens from `SCHEMA_V2_FROZEN.md`;
- use `uncertain` when the supplied packet cannot resolve a relevant judgment;
- do not invent new synonyms/tokens;
- multi-label relation/mechanism/evidence-mode fields are coded independently as `0`, `1`, or `uncertain`;
- free-text `coder_note` is optional and is not scored.

## Pre-comparison freeze

Each independent coder must run, with its own input freeze:

```bash
python code/freeze_v2_coder.py \
  --coder A2 \
  --response data/v2_coding/A2_completed.csv \
  --input-freeze process/A2_INPUT_FREEZE.json \
  --schema process/SCHEMA_V2_FROZEN.md \
  --output process/A2_COMPLETED_FREEZE.json
```

B2 uses the analogous B2 paths.

The helper rejects blanks, invalid vocabulary, duplicate IDs, missing rows, and schema/input mismatches. It creates a hash-only freeze and does not inspect the other coder.

## Reliability scoring

After both completed files and completion freezes are integrated:

```bash
python code/score_v2_agreement.py \
  --a2 data/v2_coding/A2_completed.csv \
  --b2 data/v2_coding/B2_completed.csv \
  --a2-freeze process/A2_COMPLETED_FREEZE.json \
  --b2-freeze process/B2_COMPLETED_FREEZE.json \
  --summary data/reliability/v2_reliability_summary.json \
  --disagreements data/reliability/v2_disagreements.csv
```

The scorer verifies that both coders received the same frozen input-bundle hash before calculating agreement.

## Gate

Full 165-record screening remains locked unless the scorer returns `PASS_V2_RELIABILITY`.

No disagreement adjudication is allowed to modify the pre-comparison A2/B2 files or their completion hashes.
