# Research-effort pilot · ARIS4C008

## Why this gate matters

Observed animal abilities are partly a function of how intensely a taxon has been studied. A famous great ape can have hundreds of specialized experiments while another lineage may have only a few behavioural papers. Treating "not reported" as "absent" would therefore manufacture human-like or primate-like uniqueness.

## OpenAlex proxy

A live OpenAlex query set was run for all **29 species-level v2 taxa** over publications dated **1990-01-01 through 2026-09-18**.

Each query required the exact scientific-name phrase and counted full-text search matches for:

- all taxon mentions;
- broad behaviour / cognition / learning;
- cognition / intelligence / innovation;
- social learning / teaching / culture / tradition;
- tool / manipulation / construction / object;
- communication / vocal / signal / language.

All **174 query cells** were ultimately retrieved. The first parallel pass triggered anonymous API rate limiting; failed cells were re-run serially with backoff. Missing/429 cells were never converted to zero.

## Scale of exposure imbalance

The proxy is extremely uneven.

For the broad `behavior_general` query:
- Goffin's cockatoo: **188**
- New Caledonian crow: **682**
- chimpanzee: **20,450**
- honey bee: **48,974**
- human: **116,150**

Across the current panel the largest-to-smallest ratio is about **618×**.

This alone makes a raw "number of reported abilities" comparison unacceptable.

## What this proxy is — and is not

It **is**:
- a reproducible literature-exposure covariate;
- useful for missingness models and sensitivity analyses;
- a warning signal for highly over- or under-studied taxa.

It is **not**:
- a count of high-quality cognition experiments;
- an ability score;
- an unbiased estimate of true scientific attention;
- evidence that highly published taxa are smarter.

OpenAlex work search covers title, abstract and full text, so scientific names can appear in biomedical, ecological or methodological contexts unrelated to the module. The broad keyword sets also overlap.

## Planned use

Primary bias handling should combine:

1. `log1p(all_taxon)` as a generic publication-exposure proxy;
2. module-specific `log1p(count)` terms when the corresponding behavioural outcome is modeled;
3. source-count / tested-negative metadata in the hand-curated evidence table;
4. sensitivity analyses excluding extremely high-exposure taxa;
5. missingness models that distinguish **not tested**, **tested negative**, **ambiguous**, and **positive**.

The proxy must be treated as nuisance structure rather than "correcting away" real biology.

## Reproducibility

- `data/openalex_research_effort_v0.csv`
- `code/build_openalex_effort_proxy.py`

The script supports an optional `OPENALEX_API_KEY` environment variable but can operate keyless at lower limits.
