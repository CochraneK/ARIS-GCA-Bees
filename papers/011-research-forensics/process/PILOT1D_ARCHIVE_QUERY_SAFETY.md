# Pilot 1D — archive-query safety and identity collision control

Updated: 2026-09-18

## Trigger

Scaling historical-artifact discovery exposed two retrieval-layer failure modes.

### 1. Event-day leakage in the CDX request

The first implementation described itself as ending the archive query on the day before the outcome, but set the CDX to date to the event date itself. A second-stage filter removed same-day captures, so previously retained records were still pre-event, but the request was not fail-closed by construction.

The builder now sets the CDX upper bound to event_date minus one day and still retains the independent strict capture_date earlier than event_date check.

### 2. Wildcard identity collisions

A J-STAGE prefix search around article identifier 54_1_1 returned the target article but also neighbouring objects such as 54_1_101, 54_1_107, and 54_1_13.

This is a subtle corpus-construction hazard: a prefix wildcard can silently bind an archive capture from another paper to the target case.

The discovery layer now supports an identity_marker. For the J-STAGE target the marker is /54_1_1/, so neighbouring article IDs fail identity filtering before time filtering or qualification.

## Search-manifest architecture

The six-seed pilot is now represented as source candidates with:

- target DOI;
- event date;
- issue code;
- required artifact role;
- candidate URL;
- archive query pattern;
- identity marker;
- source kind;
- intended equivalence class;
- current discovery state;
- notes.

artifact_search_manifest.py turns these candidates into auditable CDX query rows. Every generated row begins as DISCOVERY_ONLY; generation never promotes an object to SAFE_EXACT.

## Current source-anatomy result

The candidate registry currently contains publisher, repository, and mirror routes for all six original seed targets. It explicitly records known outcomes such as:

- PLOS historical HTML: SAFE_EXACT found;
- PLOS Figure 1 image: no pre-correction capture found;
- J-STAGE 2005 article: SAFE_EXACT HTML/PDF found;
- Nature correction: no pre-correction capture in the first wildcard pass;
- Springer retraction: no pre-retraction capture in the first canonical pass;
- SAGE/PMC correction article: current HTML corrected; exact old table still unresolved;
- SAGE/PMC 2019 retraction article: PMCID located, but first canonical archive pass found no pre-retraction capture.

These are acquisition states, not detector-performance results.

## Consequence for the manuscript

Historical-artifact availability is a measurable selection process. Archive discovery therefore has its own error taxonomy:

- no capture;
- wrong time;
- wrong object identity;
- current/outcome contamination;
- proxy-only version;
- equivalence unknown;
- SAFE_EXACT.

The benchmark will report this attrition before any detector metric.
