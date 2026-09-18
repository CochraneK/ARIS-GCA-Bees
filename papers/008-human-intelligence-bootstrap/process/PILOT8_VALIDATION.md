# Pilot 8 structural validation

Validated against branch commit `2565fe7b14902a975cb5d18729240f647de847ad`.

The zero-network validator `code/validate_pilot8.py` completed with `VALIDATION_OK`.

Checks passed:

- screening pool = 238 unique operational taxa;
- exactly 29 retained Pilot-7 taxa;
- next wave = 50 unique taxa and excludes retained 29;
- next-wave role allocation = 14 theory-discriminating + 15 underrepresented-clade + 10 matched-family + 11 source candidates;
- screening feature matrix covers exactly the 238-taxon pool;
- taxonomy table covers exactly 238 operational taxa;
- one manual legacy OTT crosswalk is preserved;
- deep-coding queue exactly equals the 50-taxon next wave;
- all 14 theory candidates have source-traceable evidence-seed coverage;
- Tier-1 module matrix = 79 taxa × 10 modules = 790 unique cells;
- canonical observed A–J counts = 9, 16, 11, 8, 10, 21, 60, 55, 53, 41;
- architecture-balanced recoverability output includes empirical, complete and oracle-geometry scenarios;
- model-recoverability design gate remains blocked.

This validation checks structural consistency, not truth of every source-level biological claim. Source-level evidence remains subject to ongoing deep coding and later confirmatory review.
