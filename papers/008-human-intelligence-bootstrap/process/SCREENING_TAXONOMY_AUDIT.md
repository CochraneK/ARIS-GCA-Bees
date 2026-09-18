# Screening-pool taxonomy audit · ARIS4C008 Pilot 8

## Canonical pool

The current screening pool contains **238 operational taxa**:
- 29 retained deep-panel taxa;
- ACDB/ASNR-derived candidates;
- 54 same-family body-mass-matched bird/mammal calibration taxa;
- 15 data-rich underrepresented-clade calibration taxa;
- 14 theory-discriminating candidates.

Database-unrepresented calibration means absent from the current ACDB/ASNR union. It is **not** a biological negative label.

## OpenTree 3.7 live audit

With approximate matching disabled across all 238 operational taxa:

- **222 / 238** have a clean non-synonym self species match;
- **15** require explicit synonym / operational-taxonomy handling;
- **3** queries return multiple candidates but have a unique non-synonym self species match;
- **1** query is unmatched by exact TNRS: `Serracutisoma proximum`.

The three multiple/self-resolvable taxa remain:
- *Balaenoptera musculus*;
- *Gopherus agassizii*;
- *Gryllus campestris*.

New Pilot-8 synonym crosswalks created by the expanded calibration pool include:
- *Hyla versicolor* → *Dryophytes versicolor* (OTT 386095);
- *Nephila clavipes* → *Trichonephila clavipes* (OTT 201922).

## Operational-taxon exceptions

### Domestic dog
`Canis familiaris` resolves to `Canis lupus familiaris` at subspecies rank. It may be retained for screening, but not as an independent species-level phylogenetic terminal without special treatment.

### Domestic chicken
`Gallus domesticus` resolves to the same OpenTree species/OTT as `Gallus gallus`. They may be treated as distinct experimental/ecological forms during screening, but not independent species in phylogenetic inference.

### Equus quagga
OpenTree currently resolves the supplied name below species. It remains flagged for manual taxonomic reconciliation before confirmatory tree construction.

### Serracutisoma proximum
OpenTree 3.7 lacks the current combination. The project preserves *Serracutisoma proximum* as the analysis name and uses the documented legacy `Acutisoma proximum` OTT 5097765 crosswalk for screening/tree placement. This is **not** automatic approximate-name acceptance.

## Policy

Taxonomic reconciliation is a measurement/provenance operation, not biological evidence. Synonyms, domestic forms, database lag and rank differences must never create artificial behavioral differences.

The builder now reads the canonical `screening_pool_expanded_v1.csv`, so future reruns audit all 238 taxa rather than the earlier 209-taxon intermediate pool.
