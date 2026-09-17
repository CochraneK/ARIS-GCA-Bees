# ARIS4C006 code

## Current pipeline

### `00_export_chinesenames.R`
Canonical confirmatory snapshot builder.

- pins `ChineseNames == 2025.8`;
- exports package datasets;
- builds surname-level and 26-initial population baselines;
- records package/session metadata.

Use this route for the final confirmatory baseline.

### `00b_build_initial_baseline.py`
Fast CI/engineering fallback.

- consumes a plain `familyname.csv` mirror of the ChineseNames table;
- validates the expected schema;
- computes the 26-initial population baseline;
- records input hash and row count.

This route is for reproducibility engineering/pilot checks. It does **not** replace the pinned R-package snapshot for confirmatory provenance.

### `01_openalex_alphabetization_pilot.py`
Bounded OpenAlex extraction pilot.

- selects works with `CN` institutional authorships;
- preserves listed author order and raw names;
- estimates crude observed-vs-random alphabetization by field/team size;
- adjusts chance probability for repeated surname tokens;
- writes a manifest marking outputs as non-confirmatory.

**Important:** the pilot parser uses the final Latin token only as an engineering heuristic. It is intentionally prohibited from substantive surname-effect inference.

## Planned modules before confirmatory analysis

- `02_build_surname_dictionary.py` — validated Chinese surname Romanization/exception dictionary;
- `03_parse_author_surnames.py` — tiered surname parser with confidence/evidence;
- `04_validate_surname_parser.py` — blinded validation metrics and differential-error tests;
- `05_identity_resolution_audit.py` — OpenAlex split/merge risk diagnostics;
- `06_estimate_alpha_exposure.py` — cross-fitted/lagged excess alphabetization by context;
- `07_build_author_year_panel.py` — longitudinal exposure/outcome panel;
- `08_preregistered_analysis.*` — frozen confirmatory models only after gates pass;
- `09_robustness_placebos.*` — negative controls, identity/parser sensitivity, shuffled-rank tests.

## Data rule

Do not commit unnecessary raw individual-level bibliographic dumps. Prefer:
- reproducible query manifests;
- hashes/version metadata;
- derived aggregate tables;
- bounded public-safe pilot artifacts.

## Analysis rule

No script may silently promote heuristic name parsing into confirmatory data. The parser version/tier must travel with every authorship record used downstream.
