# ARIS4C007 · Pilot 3B GSE223748 metadata feasibility

Last updated: 2026-09-19

## Decision

**PILOT 3B PASS.**

GSE223748 is suitable for a bounded molecular validation without downloading the full normalized beta matrix.

## Canonical metadata source

Successful GitHub Actions run:

- workflow: `ARIS4C007 Pilot 3B GEO metadata`
- run ID: `35406673920`
- head SHA: `622338bfdd84b65c3b4d2d2e0ea90f14f669e3f5`
- artifact SHA-256: `fef313877ad09c59834ce8dbeb5909b60e0fea0041b991eef01853cd02b51298`

The metadata-first workflow uses the official compressed GEO family SOFT file rather than downloading the 4.2 GB normalized beta matrix or 11 GB raw archive.

## Coverage

GSE223748 metadata contains:

- **15,043 samples**
- **346 species**
- **70 tissue labels**
- **13,330 samples with parseable chronological age**
- all samples on **GPL28271**
- age range: **-1 to 139 years**

Sex counts:
- Female: **7,825**
- Male: **6,842**
- Unknown: **376**

## Pan-mammalian-clock training membership

The series explicitly records whether a sample was part of the pan-mammalian clock training set:

- training = yes: **11,514**
- training = no: **3,529**

This is critical for ARIS4C007 because molecular validation should not be based only on samples used to fit the universal clocks.

## Overlap with earlier pilots

Exact species-name overlap:

- Pilot 0 complete life-history set: **199 species**
- Pilot 1 Péron demographic set: **35 species**
- Pilot 2 Translating Time set: **4 species**

Pilot 2 overlap species present in GSE223748:
- `Felis catus`
- `Homo sapiens`
- `Mus musculus`
- `Pan troglodytes`

## Bounded descriptive Pilot-2 overlap sample

A deterministic age-spread sample of at most 24 samples/species yields:

- total **74 samples**
- cat: 24
- human: 24
- mouse: 24
- chimpanzee: 2

This set is useful for connecting molecular predictions to the event benchmark, but training membership is retained and it is **not** the primary independent molecular holdout.

## Primary independent pan-clock holdout

Selection rule:

1. exact Pilot 0 life-history species overlap;
2. `panmammalianclocktrainingset = no`;
3. parseable chronological age;
4. age-confidence >=90 when numeric;
5. individual supplementary IDAT links available;
6. deterministic age-spread sample of at most 12 samples/species.

Result:

- **50 samples**
- **6 species**

Species:
- `Delphinapterus leucas`: 12
- `Mus musculus`: 12
- `Orcinus orca`: 12
- `Rattus norvegicus`: 12
- `Didelphis virginiana`: 1
- `Vombatus ursinus`: 1

Top tissues:
- Blood: 14
- Liver: 7
- Kidney: 4
- Muscle: 4
- Striatum: 4
- Brain: 3
- Blubber: 3

Every selected sample has a pair of individual GEO supplementary IDAT files, so raw-data normalization can be bounded to these 50 samples instead of the full series.

## Consequence

Pilot 3C can be genuinely independent at the **sample level** with respect to pan-mammalian-clock training.

This does **not** make Clock 2 or Clock 3 independent of their target constructs:
- Clock 2 was trained on a maximum-lifespan relative-age target;
- Clock 3 was trained on a gestation/maturity log-linear target.

Therefore molecular prediction accuracy and target-transform circularity must remain separate quantities.

## Pilot 3C execution rule

Before all 50 samples:

1. run a 12-sample, 6-species smoke subset;
2. preprocess Mammal40 IDATs using SeSAMe's recommended non-human pipeline `SHCDPB`;
3. collapse probe designs to cg prefixes;
4. require >=95% of Clock 2 and Clock 3 CpGs to be available;
5. apply the MMC v3.0.0 reference coefficients/transforms;
6. only scale to all 50 if the smoke pipeline passes.

## Handoff

**Pilot 3B is complete. The primary molecular holdout is 50 non-training samples across six species, all with downloadable IDAT pairs. Pilot 3C should normalize a 12-sample smoke subset first, using SeSAMe SHCDPB and MMC v3.0.0 reference transforms, then expand to all 50.**
