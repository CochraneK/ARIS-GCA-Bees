# ACDB cultural-group context · ARIS4C008

The current ACDB group table was joined to the 29-species v2 panel using exact species names plus explicit nested-subspecies mappings.

## Coverage
- matched cultural-group rows: **65**
- represented panel species: **16**
- species with at least one numeric group size: **12**

## Interpretation rule

These sizes describe the **grouping unit used in a cultural-behaviour source**. They are not a standardized social-group-size trait.

Depending on the source, a row may refer to:
- a troop or local group;
- an acoustic clan;
- a population;
- a colony;
- a metapopulation.

Therefore this file is a J-module **cultural-context layer**. It is not merged numerically with PanTHERIA social group size or ASNR network size without an explicit measurement model.

Nested subspecies (for example *Pan troglodytes verus* under *Pan troglodytes*) are flagged `subspecies_nested`, not silently treated as species-level measurements.
