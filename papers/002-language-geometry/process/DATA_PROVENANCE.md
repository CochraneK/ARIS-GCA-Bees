# Paper 002 · Data Provenance and Reproducibility Freeze

**Freeze date:** 2026-09-18  
**Purpose:** record upstream repository states visible at manuscript preparation.

## Important limitation

Historical Stage 0–1I scripts fetched several upstream files from mutable `main` / `master` URLs at runtime. The commit hashes below record the upstream states visible at manuscript freeze. They improve future reproducibility, but they do **not** establish cryptographically that every historical run used byte-identical files from these exact commits.

Future reruns should replace mutable raw URLs with commit-pinned URLs or vendor checksummed input manifests.

## Upstream snapshots

| Resource | Repository | Branch | Freeze commit | Role |
|---|---|---|---|---|
| TLI / GBI curated data | `annagraff/crossling-curated` | `main` | `255632bc62ce05674f1af195b88efea5aef7afce` | primary TLI; GBI curation replication |
| WALS CLDF | `cldf-datasets/wals` | `master` | `f97440d6edbaed0097d1bd307a5a20ea3f09e271` | external sparse sanity replication |
| Glottolog CLDF | `glottolog/glottolog-cldf` | `master` | `072ca0d0410039fb8b779be8fc165bac575d2cda` | family / macroarea / coordinates |

At freeze, the Glottolog CLDF head commit message identifies release 5.3.

## Primary TLI file used by Stage 1

`curated_data/TLI/statisticalTLI/full/statisticalTLI_full_densified_small.csv`

Stage 1 code source:
`ideas/language-periodic-system/stage1.py`

Selection rules:
- language matrix must contain `glottocode`;
- feature observed count ≥ 180;
- feature cardinality 2–15;
- rank eligible features by coverage, then lower cardinality;
- main global screen takes top 60 features;
- pairwise NMI minimum support = 60.

## GBI and WALS

Exact selection and support rules are encoded in:
- `ideas/language-periodic-system/stage1h.py`
- `ideas/language-periodic-system/stage1i.py`

WALS Stage 1I:
- 30 best-covered eligible categorical parameters;
- minimum feature observations = 250;
- maximum cardinality = 20;
- minimum feature-pair observations = 40.

## Reproduction policy from manuscript v1 onward

Before any new numerical rerun:

1. pin every upstream URL to a commit SHA;
2. record SHA256 checksums of downloaded CSV inputs;
3. record Python and dependency versions;
4. keep random seeds in machine-readable run metadata;
5. do not silently overwrite Stage 0–1I results; new analyses receive new stage labels or a documented correction record.
