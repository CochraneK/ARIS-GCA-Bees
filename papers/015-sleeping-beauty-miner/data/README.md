# ARIS4C015 Data

No empirical dataset is committed here yet.

## Planned open-data layers

1. OpenAlex / SciSciNet paper and citation data.
2. Crossref DOI metadata and update relations.
3. OpenCitations citation-edge cross-checks where useful.
4. PubMed / Europe PMC for biomedical enrichment where applicable.
5. Optional patent / non-patent-literature linkage only when access, coverage and licensing are reproducible.

## Historical-cutoff rule

Prospective benchmark records must carry a `cutoff_year` (or finer timestamp where available).

Any field whose information became available after the cutoff must be excluded from model features, even if the current API returns it today.

## Minimum provenance fields

- source;
- source version / snapshot date;
- retrieval date;
- raw identifier;
- normalized identifier;
- field-level timestamp availability;
- transformation script / commit;
- known coverage limitations.

## Data labels

Synthetic fixtures used for code tests must be explicitly labeled **SYNTHETIC** and must never be reported as empirical Sleeping Beauty cases.
