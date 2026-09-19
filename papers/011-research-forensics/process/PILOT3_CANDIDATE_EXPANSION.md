# Pilot 3 — reproducible correction-candidate expansion

Updated: 2026-09-18

## Why this stage exists

After the first real pre-outcome true-positive, manually searching correction notices one at a time became the next bottleneck. Pilot 3 converts candidate selection into an auditable queue.

This queue is **not** the confirmatory benchmark. It is an acquisition-enrichment device used to decide where historical-object recovery effort is most likely to produce valid Track A cases. Later correction text may guide acquisition priority, but it is never exposed to Track A detectors.

## Priority dimensions

Candidates are scored on five dimensions:

1. **artifact state** — SAFE_EXACT material already known is favoured;
2. **verification mode** — deterministic/internal checks are favoured over re-analysis;
3. **required role** — tables/text/references are generally easier to recover than image-only or raw-data cases;
4. **scientific-content relevance** — substantive errors outrank formatting-only corrections;
5. **publication-to-correction window** — longer windows improve the chance that a clean historical object was archived.

Completed true-positive cases are removed from active acquisition. Formatting-only cases are explicitly routed to CONTROL even if the historical object is excellent.

## Current queue

### PRIORITY

1. **10.1371/journal.pone.0293412** — Table 1 country counts/proportions.
   - correction: 10.1371/journal.pone.0317174
   - pre-correction HTML exists;
   - exact historical table object still unresolved;
   - candidate F3 arithmetic/sum check.

2. **10.1371/journal.pone.0180906** — two columns missing from Table 1B.
   - correction: 10.1371/journal.pone.0192570
   - strong F3 structural-completeness target;
   - first printable-PDF archive query returned no pre-correction capture.

### SECONDARY

3. **10.1371/journal.pone.0180395** — corrected two-tailed p-values plus table-schema changes.
   - potential F1/F3 case;
   - may require recoverable source statistics or raw data.

4. **10.1371/journal.pone.0163749** — multiple Table 2 Brodmann-area entry errors.
   - potential F3 structural/token anomaly case;
   - historical table object still needed.

### CONTROL

**10.1371/journal.pone.0263337** — comma-versus-period decimal formatting in the Cronbach alpha column.
- exact pre-correction PLOS PDF exists in Wayback from 2022-02-09;
- digest: JH73D3J2WEFFQC75H7OUERJ74OJMJZKP;
- archived Table 2 prints values such as 0,943 and 0,819;
- this is deliberately treated as a low-risk formatting/honest-error control rather than a scientific contradiction.

### DEFER

- 10.1371/journal.pone.0075637 — scientifically meaningful model/outlier correction, but it requires re-analysis rather than a cheap deterministic check.
- 10.1371/journal.pone.0142234 — 21-day correction window and largely heading/statement corrections.

## Selection-bias rule

Pilot 3 is allowed to be enriched for recoverable, detector-compatible cases because its purpose is pipeline development.

No confirmatory sensitivity, precision, or comparative-performance claim may be calculated from this queue. A later confirmatory cohort must be selected under a frozen, broader sampling protocol independent of whether a detector is expected to succeed.


## Pilot 3B resolution of the former rank-1 case

The music-country case (10.1371/journal.pone.0293412) is no longer an active acquisition target.

New evidence changed its routing:

- the Humboldt-Universität repository record is dated 2023-10-26 and stores journal.pone.0293412.pdf;
- that file is byte-identical to the PLOS printable PDF (SHA-256 95460abea1594e8f8f1aec4e8fb029df0e0faacf4e7244ba7ddb25dc7eefe60b);
- the public OSF file survey1_ratings.csv is version 1, created/modified 2023-07-28, with SHA-256 90f86ae54abb67e980a3379bfc95ab796fb9ebfe1ea9580fa4afde8743a035bb;
- the historical table's Mexico 16/4.5% is internally arithmetic-consistent with the table because Other is simultaneously 88;
- raw-data normalization of Mexico/México/MÉXICO yields 17/4.8%.

Accordingly, the candidate was reclassified from DETERMINISTIC_INTERNAL to RAW_DATA_RECOMPUTE and from ACTIVE to COMPLETE. This demonstrates why candidate routing is provisional during pipeline development: source anatomy can change which detector is actually capable of detecting a documented error.


## Pilot 3C resolution of the Toxoplasma candidate

The former active-rank-1 Toxoplasma case (10.1371/journal.pone.0180906) produced a valid Track A signal, but not through the originally targeted missing-column route.

A PLOS publisher HTML snapshot from 2017-07-24 (Wayback digest MTJNXHVAUJZCTOAR47PRAO7AVYGIDJ7O) predates the 2018 correction. In that same historical artifact:

- the Results text explicitly attributes multiple-analysis household findings to Table 1 and reports model p-values/confidence intervals;
- the Table 1 caption describes the table only as results of univariate logistic regression analysis.

A cross-section scope-coherence detector therefore flags a body-to-caption scope mismatch without access to the later correction. The 2018 correction subsequently states that the Table 1 caption was wrong and changes it to cover univariate and logistic regression analysis.

The historical Table 1 image endpoint itself was not preserved in the archive. Therefore the correction's separate statement that two columns were missing from Table 1B remains **BLOCKED** for primary Track A evaluation. Pilot 3C is counted only for the independently documented caption error.

This case illustrates issue decomposition: one correction notice can contain multiple sub-issues with different artifact requirements and different Track A eligibility.
