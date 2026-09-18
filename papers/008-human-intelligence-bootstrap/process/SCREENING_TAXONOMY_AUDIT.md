# Screening-pool taxonomy audit · ARIS4C008 Pilot 8

## Pool

The expanded screening pool contains **209 operational taxa**:
- 155 species-level names normalized from the current 29 + ACDB + ASNR source union;
- 54 same-family, body-mass-matched database-unrepresented bird/mammal calibration taxa.

“Database-unrepresented calibration” means absent from the current ACDB/ASNR union. It is **not** a biological negative label.

## OpenTree 3.7 live audit

With approximate matching disabled:

- **195 / 209** queries have a clean non-synonym self species match;
- **13** require explicit synonym / taxonomy handling;
- **3** queries return multiple matches but have a unique non-synonym self species match and are therefore resolvable;
- **1** query is unmatched: `Serracutisoma proximum`.

The 3 multiple/self-resolvable taxa are:
- *Balaenoptera musculus*;
- *Gopherus agassizii*;
- *Gryllus campestris*.

## Important operational-taxon exceptions

### Domestic dog

`Canis familiaris` maps to OpenTree `Canis lupus familiaris` at subspecies rank.

The domestic dog remains useful as a screening/calibration operational taxon, but it must not be treated as an independent species terminal in species-level phylogenetic models.

### Domestic chicken

`Gallus domesticus` maps to the same species/OTT as `Gallus gallus`.

They may be retained as separate ecological/experimental operational forms during screening, but share one species cluster for phylogenetic independence.

### Equus quagga

OpenTree currently resolves the query to a below-species taxon (`Equus burchellii quagga`). This is flagged for manual taxonomy review before confirmatory inclusion rather than silently accepted.

### Serracutisoma proximum

OpenTree 3.7 does not match the current combination. External systematic-taxonomy literature recognizes *Serracutisoma proximum* and documents its older combination/synonym history. OpenTree's approximate search finds legacy `Acutisoma proximum` (OTT 5097765).

Paper 008 therefore uses an explicit **manual legacy OTT crosswalk** for screening/tree placement and preserves `Serracutisoma proximum` as the analysis name. This is not an automatic approximate-name acceptance.

## Policy

Taxonomy resolution is separate from biological evidence coding. A synonym, database lag, or below-species operational unit must never create a fake behavioral difference.
