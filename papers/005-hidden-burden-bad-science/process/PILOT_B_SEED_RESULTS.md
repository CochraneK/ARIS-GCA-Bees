# PILOT B SEED RESULTS — ARIS4C005

**Date:** 2026-09-18  
**Classification:** real probability-traceable seed frame; **not prevalence**

## B1. Frozen pilot target

For the first article-level calibration pilot:

- OpenAlex corpus: `core`
- work types: `article|review`
- years: **2015–2020**
- target-universe metadata count: **38,451,124**
- random-sample seed: `20260918`

Population-random component:

- requested: **600**
- resolved unique OpenAlex works: **600**
- first-order random inclusion probability: **1.5604225e-05**
- random-only design weight: **64,085.21**

This random component is what prevents the project from estimating prevalence only among already-suspected papers.

---

## B2. Retraction Watch enrichment frame

The frozen 2015–2020 Retraction Watch DOI frame contained **8,769 unique candidate DOIs** across five mutually exclusive enrichment strata.

| stratum | RW DOI frame N | target n | p_enrich | resolved selected works |
|---|---:|---:|---:|---:|
| narrow E1-S | 472 | 200 | 0.423729 | 181 |
| expression of concern | 1,103 | 100 | 0.090662 | 100 |
| major error E3 | 2,516 | 150 | 0.059618 | 138 |
| paper mill | 2,682 | 200 | 0.074571 | 176 |
| process integrity | 1,996 | 150 | 0.075150 | 144 |

Requested enrichment DOIs: **800**

Selected enrichment DOIs resolving into the OpenAlex target universe: **739**

The enrichment probability is defined on the frozen RW DOI frame *before* OpenAlex resolution. Therefore, for a target-universe work belonging to stratum s:

`p_enrich,s = n_s / N_s`

and combined inclusion probability is:

`pi_i = 1 - (1 - p_random)(1 - p_enrich,s)`

This avoids resolving the entire RW candidate frame before sampling while preserving the correct first-order probability.

---

## B3. Real seed sample

Unique selected works:

**1,339**

Composition:

- population random: **600**
- RW enrichment: **739**

Realized enrichment composition:

- narrow E1-S: 181
- paper mill: 176
- process integrity: 144
- major error: 138
- expression of concern: 100

Work types:

- article: **1,335**
- review: **4**

Broad OpenAlex domains:

- Physical Sciences: **417**
- Health Sciences: **347**
- Life Sciences: **343**
- Social Sciences: **226**
- topic/domain missing: **6**

Years:

- 2015: 184
- 2016: 166
- 2017: 213
- 2018: 238
- 2019: 268
- 2020: 270

---

## B4. DOI coverage finding

Among the **600 population-random** works:

- **229 lacked a DOI** in the downloaded OpenAlex seed frame;
- **371 had a DOI**.

All 739 RW-enrichment works necessarily had a resolvable DOI because DOI is the enrichment key.

### Implication

A DOI-only global prevalence design would exclude a substantial part of the random target universe and could induce selection bias.

Therefore:

- OpenAlex ID remains a first-class identity key;
- DOI is not required for a random paper to remain in the study;
- notice/detector applicability missingness must be modeled rather than turning DOI absence into a negative integrity signal.

---

## B5. Design-weight contrast

Approximate design weights in the realized seed:

- population-random only: **64,085.21**
- narrow E1-S: **2.36**
- expression of concern: **11.03**
- paper mill: **13.41**
- process integrity: **13.30**
- major error: **16.77**

This extreme contrast is intentional: enrichment efficiently supplies positive/ambiguous cases for detector calibration, while the small-probability random component carries population information.

Raw sample proportions are therefore scientifically meaningless for prevalence.

---

## B6. Blinded adjudication packet

Full seed:

- unique works: **1,339**
- reviewer assignments: **1,607**
- planned double-coded assignment rows correspond to a 20% work-level double-code design.

Reviewer-facing packets exclude:

- RW enrichment stratum;
- detector flags;
- inclusion probability;
- design weight.

Manager linkage retains these fields and reconnects them after review using hashed assignment IDs.

The blinding invariant is unit-tested.

---

## B7. 60-work micro-pilot

A balanced protocol micro-pilot was generated from the real seed.

Works: **60**

All six groups contribute 10 works:

- population random: 10
- narrow E1-S: 10
- paper mill: 10
- major error: 10
- expression of concern: 10
- process integrity: 10

All 60 are double coded:

**120 reviewer assignments**

Broad-domain composition:

- Physical Sciences: 21
- Life Sciences: 15
- Health Sciences: 14
- Social Sciences: 10

Selection forces at least one work from each available broad domain within each signal group before random fill.

### Purpose

The 60-work micro-pilot is **not** a prevalence sample.

It tests:

1. whether the six-state scientific-state ontology is usable;
2. how often reviewers disagree;
3. how often evidence is inaccessible or indeterminate;
4. how much review effort is required;
5. whether the materiality definition works across fields.

---

## B8. Gate decision

**Engineering gate: PASS**

Completed:

- real random sample;
- real enrichment sample;
- exact inclusion probabilities;
- public-safe provenance;
- blinded reviewer packet;
- manager linkage;
- balanced double-coded micro-pilot;
- merge/QA validator;
- automated CI invariants.

**Scientific adjudication gate: PENDING**

The next empirical requirement is independent adjudication of the 60-work micro-pilot.

No global latent-prevalence estimate is authorized until real adjudication and detector calibration exist.
