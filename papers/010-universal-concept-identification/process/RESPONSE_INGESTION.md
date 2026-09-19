# ARIS4C010 · Response Ingestion Contract

Participant-visible files are **not** trusted as authoritative trial metadata.

The standalone HTML intentionally hides internal design fields such as `is_retest`. Therefore raw participant JSON cannot be analyzed directly.

## Canonical ingestion step

Use:

```bash
python ingest_standalone_responses.py response1.json response2.json -o combined.json
```

The ingest tool joins every submitted row against the frozen `forms.generated.json` using:

- form ID;
- protocol;
- trial position;
- pair ID;
- target ID;
- query ID.

It reconstructs:

- `is_retest`;
- base form;
- target/query metadata required for analysis.

## Integrity checks

A response file is rejected if:

- form ID is unknown;
- protocol does not match the form;
- row count differs from the canonical form;
- trial order is altered;
- pair/target/query IDs differ from the canonical form;
- a response is outside that protocol's allowed alphabet;
- confidence is outside [0,1];
- response time is negative;
- the same participant/form session is submitted twice in one ingest batch;
- one participant appears in multiple protocol arms in the same batch.

## Why this is preferable to embedding internal labels in the UI

The participant should not be told which trials are retests or which semantic phenomenon motivated a stress item.

The researcher's canonical form, not the browser payload, is the source of truth for design metadata.

## Analysis path

```text
participant HTML
    ↓ local JSON export
ingest_standalone_responses.py
    ↓ validated combined JSON
analyze_human_calibration.py
    ↓ descriptive calibration summary
triage_human_annotations.py
    ↓ review / additional-rating queue
```

A synthetic end-to-end CI test additionally tampers with a pair ID and verifies that ingestion rejects the modified file.
