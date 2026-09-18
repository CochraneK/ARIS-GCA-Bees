# UCID data layer

This directory contains **schemas and future benchmark artifacts** for ARIS4C010.

Current files:

- `ucid-target.schema.json` — target/concept record schema;
- `ucid-query.schema.json` — candidate question schema;
- `ucid-response.schema.json` — target × query judgment schema.

No file in this directory should be interpreted as semantic ground truth unless its provenance and adjudication status explicitly say so.

## Planned artifact layers

```text
raw-source/
normalized/
annotations/
adjudicated/
splits/
release/
```

Raw external resources should not be committed blindly. Preserve licensing, version and checksum metadata, and use retrieval/build scripts where redistribution is restricted or unnecessarily large.
