# ARIS4C015 Data

No empirical dataset is committed here yet.

## Planned open-data layers

1. **SciSciNet-v2** as the preferred large-scale backbone when feasible; it is refreshed from OpenAlex and includes publication, citation and patent-linkage data.
2. SciSciNet v1 for reproducibility checks against published Sleeping Beauty coefficients.
3. OpenAlex for IDs, metadata, references, topics and live citation graph access.
4. Crossref DOI metadata and update relations.
5. OpenCitations citation-edge cross-checks where useful.
6. PubMed / Europe PMC for biomedical enrichment where applicable.

## OpenAlex trajectory caveat

A Work's `counts_by_year` contains only roughly the latest ten years of yearly citations and omits years with zero citations.

Therefore it is **not sufficient on its own** for historical Sleeping Beauty reconstruction.

For full trajectories:

- obtain citing-paper edges for the target paper;
- join citing papers to publication year;
- aggregate citations by target-paper age;
- explicitly insert zero-citation years;
- verify the reconstructed total against available citation totals, allowing for source-update drift.

Where possible, SciSciNet / SciSciNet-v2 should be used for large-scale reconstruction and cross-checking.

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
