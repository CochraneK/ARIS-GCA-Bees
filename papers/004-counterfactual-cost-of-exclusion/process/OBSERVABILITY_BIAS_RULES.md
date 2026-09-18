# OBSERVABILITY BIAS RULES — ARIS4C004

Date frozen: 2026-09-18

## Purpose

Separate three quantities that must never be conflated:

1. historical contribution;
2. surviving documentation/notability;
3. observability in modern scholarly databases such as OpenAlex.

ARIS4C004 samples from an already historically visible contributor database and then applies a modern bibliographic observability gate. Both stages can be selective.

## Descriptive meaning only

A group-level quantity such as:

`network_observable_rate(region = Europe) > network_observable_rate(region = Asia)`

means only:

> Within this frozen candidate frame and the current identity/network protocol, a larger fraction of the European candidates yielded an analyzable graph.

It does **not** establish:

- Europeans contributed more knowledge;
- European scholarship was intrinsically more important;
- people outside Europe were less productive;
- the historical population had the same regional composition as the candidate frame.

## Required observability audit

Before mental-health exposure coding, report identity/network outcomes by at least:

- birth cohort;
- cohort × candidate visibility stratum;
- region;
- gender;
- source level-2 occupation;
- source level-3 occupation/subdomain.

For each group report:

- candidate N;
- verified-identity N/rate;
- network-observable N/rate;
- no-graph N/rate;
- collision/error N;
- remaining provisional N.

Small cells must be presented as descriptive diagnostics, not stable rate estimates.

## No outcome-driven frame repair

If one region/era/subdomain is poorly observed, permitted responses include:

- characterize the missingness;
- use stratified/matched analysis;
- use domain-appropriate alternative influence layers;
- create a separately versioned sensitivity frame using pre-exposure rules.

Forbidden response:

> lower identity/work thresholds for the under-covered group until rates look balanced.

Coverage equality is not worth identity error.

## Candidate-frame Europe weighting

The current 100-person frame inherited strong European weighting from the upstream historical-notability source.

That fact must be visible in the manuscript/limitations. It cannot be repaired after exposure coding by selectively adding people based on known psychiatric history or known importance.

If a region-balanced sensitivity frame is later created, it must:

1. be generated from the original eligible source pool;
2. use only pre-exposure covariates;
3. be versioned separately from the canonical seed-20260918 frame;
4. be analyzed as a sensitivity/generalizability exercise rather than silently replacing the primary frame.

## Citation-rich vs citation-sparse

Citation-layer observability is another selection dimension.

The frozen pilot definitions are:

- citation-rich: >=10 downstream unique works under the fixed anchor/horizon protocol;
- citation-sparse: 1–9;
- no-downstream: 0.

These are database/network-observability labels, not importance labels.

A citation-sparse person may remain scientifically important but be represented poorly because of publication era, books, language, geography, or indexing.

## Exposure-stage firewall

When mental-health evidence is eventually coded, analysts must be able to reconstruct:

- who was in the frozen candidate frame;
- who was identity-verifiable;
- who was network-observable;
- who was citation-rich/sparse;
- why each exclusion occurred,

**without using the exposure column**.

Any post-exposure change to identity/network inclusion requires explicit versioning and sensitivity analysis.

## Statistical implication

Primary exposed/comparison contrasts should condition or match on relevant pre-exposure opportunity/observability variables rather than interpreting raw group differences.

Candidate variables include:

- era/cohort;
- subdomain;
- candidate visibility;
- geography/language context;
- baseline output;
- documentation/authority availability;
- baseline network observability/quality.

Documentation intensity may itself be downstream of fame/achievement, so it should be used transparently for common-support/ascertainment sensitivity rather than described as a universal confounder control.

## Claim language

Preferred:

> Network observability differed across historical strata in the frozen contributor frame; analyses therefore characterize and adjust for differential database coverage.

Avoid:

> Some demographic groups had lower knowledge impact because fewer individuals were found in OpenAlex.
