# ARIS4C004 data

This directory stores **derived/reconstructable research data only**. Do not commit copyrighted biographies, restricted clinical/archival documents, API secrets, or a multi-hundred-GB OpenAlex snapshot.

## Recommended local layout

```text
data/
├── README.md
├── raw/          # local / gitignored when large or license-restricted
├── interim/      # identity-resolution and coding work products
└── derived/      # public-safe analytic tables where licensing permits
```

## Science-pilot reconstruction

### 1. Obtain the cross-verified candidate source

Preferred source:

- Laouenan et al. (2022), *A cross-verified database of notable people, 3500BC–2018AD*.
- Dataset DOI: `10.21410/7E4/RDAG3O`.
- Use the **cross-verified restricted dataset**, not the unverified exhaustive intermediate dataset.
- The publication reports the cross-verified data under CC-BY-SA. Preserve attribution/license notices for redistributed derivatives.

Expected source filename is commonly `cross-verified-database.csv` or `.csv.gz`; the script accepts either.

### 2. Build the mental-health-independent candidate frame

```bash
python code/acquire/build_candidate_frame.py \
  data/raw/cross-verified-database.csv.gz \
  --output data/interim/science_candidates_frozen.csv \
  --target 100 \
  --seed 20260918
```

This step filters only on historical/disciplinary metadata and samples within period × visibility strata. It does **not** inspect mental-health information.

### 3. Enrich identifier leads from Wikidata

```bash
python code/resolve/wikidata_identifiers.py \
  data/interim/science_candidates_frozen.csv \
  --output data/interim/science_candidates_identifiers.csv
```

Wikidata ORCID/OpenAlex identifiers are identity-resolution leads. They must be validated against OpenAlex records; do not assume every historical identifier is current/correct.

### 4. Fetch bounded OpenAlex metadata

Keyless casual API use is supported by OpenAlex at the time this pilot was designed. For a larger pilot, create a free OpenAlex key and expose it as an environment variable; never commit it.

```bash
# optional
export OPENALEX_API_KEY="..."

python code/acquire/openalex_pilot.py \
  data/interim/science_candidates_identifiers.csv \
  --out-dir data/interim/openalex \
  --year-min 1900 \
  --year-max 2000
```

The acquisition script writes authors, works, unresolved rows, and a coverage summary. It does not search for mental-health terms.

## Exposure coding

Create the exposure table only **after the candidate frame is frozen**. Follow `process/EXPOSURE_CODEBOOK.md` and validate with:

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

- IDs;
- source citations/provenance;
- derived numeric/network features;
- evidence tiers and non-sensitive historical coding;
- scripts/configs/seeds.

Avoid committing:

- long copyrighted source text;
- raw biography books/articles;
- raw medical files;
- living-person health information;
- secret/API keys;
- large OpenAlex snapshots.

The goal is **reconstruction**, not mirroring every upstream dataset.
