# ACDB pilot extraction · ARIS4C008

**Source:** Animal Culture Database v0.1 published data release (Scientific Data, 2025).

## Extraction result

- ACDB species in release: 61
- ACDB groups: 116
- ACDB behaviours: 129
- ARIS4C008 pilot taxa directly matched by canonical species name: **13**
- Matched ACDB groups: **32**
- Matched cultural-behaviour records: **42**

## Coverage lesson

Coverage is strongly incomplete for the 008 pilot. A missing species or behaviour in ACDB is therefore coded as **not covered / not tested**, never as behavioural absence.

The most behaviour-rich direct matches in this extraction are:

- **Orcinus orca** — 10 behaviours across 4 coded domains (foraging; play; social; vocal communication).
- **Corvus moneduloides** — 5 behaviours across 3 coded domains (antipredation; foraging; vocal communication).
- **Pan paniscus** — 4 behaviours across 2 coded domains (architecture; foraging).
- **Megaptera novaeangliae** — 3 behaviours across 3 coded domains (foraging; mating; vocal communication).
- **Physeter macrocephalus** — 3 behaviours across 3 coded domains (foraging; social; vocal communication).
- **Pongo abelii** — 3 behaviours across 2 coded domains (architecture; foraging).
- **Sapajus libidinosus** — 3 behaviours across 1 coded domains (foraging).
- **Tursiops aduncus** — 3 behaviours across 1 coded domains (foraging).

## Design consequence

ACDB is useful as a standardized culture layer and source index, but cannot serve as the sole outcome database. The 008 matrix must supplement it with targeted comparative-cognition literature, and must carry a research-effort variable.

## Files

- `data/acdb_pilot_species.csv` — species-level extraction summary.
- `data/acdb_pilot_behaviors.csv` — source-traceable behaviour rows for directly matched pilot taxa.
