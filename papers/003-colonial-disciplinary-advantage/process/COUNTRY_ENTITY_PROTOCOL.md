# COUNTRY / ENTITY PROTOCOL — ARIS4C003

## Canonical modern key

Primary contemporary analyses use **ISO 3166-1 alpha-3 (`iso3c`) for current sovereign states** as the canonical country key.

The protocol separates three questions that must not be conflated:

1. Which modern state receives contemporary OpenAlex output?
2. Which modern state is represented by the COLDAT/CEPII historical exposure record?
3. How should historical/dissolved COW entities be represented in ICOW robustness analyses?

No historical predecessor is silently coerced into a modern successor merely to avoid missingness.

---

## Source-specific mapping

### OpenAlex

OpenAlex authorship country codes are converted to canonical ISO3 before aggregation. Any non-ISO/disputed code is retained in an unresolved audit table and excluded from the confirmatory sovereign-state model until reviewed.

Primary country attribution follows the preregistered distinct-country fractional rule; the crosswalk changes labels, not credit weights.

### COLDAT / Our World in Data

OWID provides a `Code` field for current entities. The `Code` is used directly when it is a valid ISO3 current-state code.

Rows without a valid current-state code (aggregates, regions, World, historical/non-country entities) are excluded from the primary state-level exposure table and logged.

This source is already defined over countries that are independent today; no attempt is made to reinterpret it as a complete dataset of continental/informal empire.

### CEPII Gravity

Use CEPII's ISO-style origin/destination identifiers and map both ends to canonical ISO3. Directional historical indicators are converted to an unordered dyadic key only after retaining the original directional fields for audit.

The raw CEPII file/version remains traceable through `data/manifests/source_manifest.json`.

### ICOW / Correlates of War

ICOW is a robustness/history source using COW codes. Mapping uses `code/build_country_crosswalk.py` and the `countrycode` country-year panel where a year is available.

Rules:

- prefer a country-year COW→ISO mapping;
- otherwise allow the package cross-sectional COW conversion only when it returns a unique modern ISO3;
- unresolved historical/dissolved entities remain unresolved;
- manual overrides require a row in `COUNTRY_CROSSWALK_OVERRIDES.csv` with a note, reviewer, and date;
- an override must describe the historical rationale, not merely state that two labels "look equivalent".

---

## Sovereignty / territory rule

Primary country-level analysis excludes current non-sovereign dependencies and territories because the historical exposure and modern publication attribution unit would otherwise be inconsistent.

A territory-inclusive sensitivity may be run only after:

- defining whether the territory or sovereign state owns the modern output;
- defining the historical exposure unit;
- documenting any parent-state aggregation.

No territory is reassigned ad hoc after observing outcomes.

---

## Historical succession rule

Potentially difficult cases include dissolved states, partitions, reunifications, and disputed recognition (e.g. historical German states, USSR successor states, Yugoslav successor states, Czechoslovakia, historical Vietnams, Kosovo/Taiwan-type coding differences).

Primary principle:

> A historical entity is not a modern state simply because one successor inherited its capital, name, or largest territory.

For the primary COLDAT/CEPII contemporary-state estimands, rely on the source's current-state coding. For ICOW robustness, keep unresolved predecessor rows separate unless a defensible country-year mapping exists.

---

## Required audit outputs

Before real confirmatory models:

1. `data/derived/COUNTRY_CROSSWALK.csv`
2. `data/derived/COUNTRY_CROSSWALK_UNRESOLVED.csv`
3. source-specific counts of mapped/unmapped rows;
4. list of manual overrides and rationale;
5. list of excluded aggregates/territories;
6. checksum/provenance for every source used.

The primary analysis cannot proceed if an unresolved entity contributes materially to the confirmatory sample.

---

## Freeze rule

This protocol is frozen before opening the contemporary country×discipline outcome matrix. Later mapping corrections are allowed only as documented data-quality amendments; they must not be chosen based on effect direction or significance.
