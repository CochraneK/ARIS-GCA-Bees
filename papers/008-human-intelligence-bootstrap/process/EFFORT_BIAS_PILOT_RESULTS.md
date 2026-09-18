# ACDB × research-effort diagnostic · ARIS4C008

## Question

Is the number of cultural-behaviour rows currently extracted from ACDB basically just a proxy for how much a species has been studied?

A 13-species overlap was available between direct ACDB matches and the OpenAlex research-effort proxy.

## Pilot result

Using log-transformed OpenAlex exposure:

- Pearson, behavioural-effort vs ACDB behaviour rows: **−0.240**
- Spearman, behavioural-effort vs ACDB behaviour rows: **−0.438**
- Pearson, total taxon literature vs ACDB behaviour rows: **−0.265**
- Spearman, total taxon literature vs ACDB behaviour rows: **−0.492**
- Pearson, behavioural-effort vs number of ACDB coded domains: **−0.178**

## Interpretation

This does **not** mean research effort reduces animal culture.

It means a more important measurement problem has been exposed:

> **ACDB row count is not an exhaustive species-level cultural repertoire count.**

ACDB is a curated database of documented nonhuman cultural cases. Its current number of rows per species depends on database inclusion structure, group definitions, what behaviours were selected as records, and source organization. For example, highly studied chimpanzees and honey bees can have fewer ACDB rows than killer whales or New Caledonian crows in this release.

Therefore:

1. `ACDB n_behaviors` must **not** be used as the primary quantitative outcome for cultural capacity.
2. ACDB remains valuable for source-traceable **presence evidence, domain coding, transmission modes and case discovery**.
3. O4 cultural repertoire breadth needs a separately defined systematic-review protocol or a database explicitly designed for exhaustive repertoire comparison.
4. Research-effort correction remains necessary for literature-derived trait coding, but it cannot repair a non-exhaustive outcome by simple regression adjustment.
5. Pilot analyses should prefer explicitly coded outcome states and domain-level evidence over raw ACDB row counts.

This is a useful negative result: it prevents an attractive but invalid shortcut before confirmatory analysis begins.

## Reproducibility

- `data/acdb_openalex_effort_join_v0.csv`
- `code/analyze_acdb_effort_bias.py`
