# ARIS4C004 data

This directory stores **derived/reconstructable research data only**. Do not commit copyrighted biographies, restricted clinical/archival documents, API secrets, or a multi-hundred-GB OpenAlex snapshot.

## Layout

```text
data/
├── README.md
├── raw/          # local / gitignored when large or license-restricted
├── interim/      # identity-resolution and coding work products
└── derived/      # public-safe frozen/analytic tables where licensing permits
```

## Frozen science candidate frame

`derived/science_candidates_frozen.csv` is the canonical **pre-exposure 100-person science feasibility frame**.

It was generated before any mental-health evidence was used, with:

- source: Laouenan et al. (2022), *A cross-verified database of notable people, 3500BC–2018AD*;
- dataset DOI: `10.21410/7E4/RDAG3O`;
- verified source-mirror SHA-256: `fe44aa6f97cf9f6c12d040137f92a9f4d0fd1f50e28f7f5d80eeae29b487828d`;
- eligibility: `Discovery/Science`, required Wikidata ID and usable birth/death years within the pilot bounds;
- fixed random seed: `20260918`;
- stratification: birth cohort × source visibility quartile;
- target: 100 candidates, 5 in each of 20 strata.

The cross-verified dataset is reported by the publication under CC-BY-SA; preserve attribution/share-alike requirements for redistributed derivatives.

This frozen file should **not be regenerated merely because a later identity/exposure result is inconvenient**. Any future alternate frame must be versioned as a separate design/sensitivity frame and created without using mental-health outcomes.

## Reconstructing the frozen frame from upstream data

Obtain the official/cross-verified dataset and run:

```bash
python code/acquire/build_candidate_frame.py \
  data/raw/cross-verified-database.csv.gz \
  --output data/interim/science_candidates_rebuilt.csv \
  --target 100 \
  --seed 20260918
```

The source mirror used during the pilot contains mixed/legacy text bytes. The script reads losslessly via Latin-1 and repairs only reversible UTF-8-as-Latin-1 mojibake at the cell level. It never uses `errors=ignore`.

The current real-data identity workflow consumes the committed frozen frame directly so resolver changes do not repeatedly download/scan the ~250MB upstream source.

## Identity-resolution pipeline

### 1. Enrich identifier leads from Wikidata

```bash
python code/resolve/wikidata_identifiers.py \
  data/derived/science_candidates_frozen.csv \
  --output data/interim/science_candidates_identifiers.csv
```

Wikidata identifiers are leads, not final identity decisions. The first 100-person pilot yielded only one ORCID lead and zero OpenAlex-ID leads through Wikidata.

### 2. Search/fetch bounded OpenAlex metadata

```bash
# optional free key for a larger request budget
export OPENALEX_API_KEY="..."

python code/acquire/openalex_pilot.py \
  data/interim/science_candidates_identifiers.csv \
  --out-dir data/interim/openalex \
  --year-min 1900 \
  --year-max 2000
```

The resolver preserves `accepted`, `ambiguous`, and `unresolved` states and writes an audit trail. An automated top hit is **not** final identity verification.

### 3. Detect Author-ID fragmentation

```bash
python code/resolve/openalex_cluster_review.py \
  data/interim/openalex/openalex_resolution_audit.jsonl \
  --output-csv data/interim/openalex/identity_review_queue.csv \
  --summary-json data/interim/openalex/identity_review_summary.json
```

The first-30 pilot classified 11/30 candidates as possible author fragmentation, so the final mapping target is person → one or more verified OpenAlex Author IDs.

### 4. Collect pairwise fragment evidence

```bash
python code/resolve/openalex_cluster_evidence.py \
  data/interim/openalex/identity_review_queue.csv \
  --out-dir data/interim/openalex/cluster_evidence \
  --year-min 1800 \
  --year-max 2026
```

This collects DOI/title overlap, coauthors, institutions, topics, publication timing, ORCID agreement/conflict, and representative works for human review. Its `support/conflict/needs_review` labels are **review-priority heuristics only** and never auto-create a verified cluster.

### 5. Lock person-level identity decisions

Use `identity_decisions_template.csv` and `process/IDENTITY_CODEBOOK.md`, then validate:

```bash
python code/validate_identity.py data/interim/identity_decisions.csv
```

Only `VERIFIED_SINGLE` and `VERIFIED_CLUSTER` may enter the confirmatory science-network analytic frame.

## Exposure coding

Create the exposure table only **after the network-observable identity frame is frozen without using mental-health information**. Follow `process/EXPOSURE_CODEBOOK.md` and validate with:

```bash
python code/validate_exposure.py data/interim/exposure_codes.csv
```

`U` / unknown is never converted to `healthy` by default.

## Provenance record

Every derived dataset should carry or be accompanied by:

- source DOI/URL/version/date;
- acquisition date;
- source license/reuse note;
- exact command/config;
- script Git commit;
- random seed where applicable;
- raw-file checksum when the local source is downloaded.

## Public repository policy

Prefer committing:

- frozen pre-exposure candidate IDs/metadata where licensing permits;
- verified person ↔ OpenAlex author-cluster decisions and evidence provenance;
- derived numerical/network features;
- historical evidence tiers and source identifiers;
- scripts/configs/seeds.

Avoid committing:

- long copyrighted source text;
- raw biography books/articles;
- raw medical files;
- living-person health information;
- secret/API keys;
- large OpenAlex snapshots.

The goal is **reconstruction and auditable decision provenance**, not mirroring every upstream dataset.
