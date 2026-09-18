# Sleeping Beauty Miner agent

This folder is the reusable agent/skill surface for ARIS4C015.

## Entry point

Read `SKILL.md`.

## What the bundled reference implementation can do now

- reconstruct zero-filled annual citation histories from citation-edge years;
- compute Beauty Coefficient B and awakening time;
- truncate histories at a historical cutoff;
- compute transparent prospective baselines;
- ingest bounded OpenAlex citation data;
- ingest local SciSciNet-v2 CSV/TSV/Parquet slices through a configurable schema adapter;
- adapt ARIS4C011 findings into CLEAR / CAUTION / QUARANTINE / ABSTAIN routing;
- generate Candidate Evidence Cards.

## What is intentionally not claimed yet

The repository does not yet contain a validated prospective model that can reliably predict future Sleeping Beauties.

That claim requires a historical-cutoff benchmark with out-of-time and cross-field testing.

## Relationship to 011

ARIS4C011 is reused as the integrity/provenance evidence layer. 015 does not duplicate all forensic detectors and does not treat "no flag" as evidence of scientific importance.
