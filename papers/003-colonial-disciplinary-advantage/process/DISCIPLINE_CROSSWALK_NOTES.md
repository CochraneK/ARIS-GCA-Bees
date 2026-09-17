# OPENALEX DISCIPLINE CROSSWALK NOTES — ARIS4C003

Date frozen: 2026-09-18

Primary machine-readable crosswalk: `DISCIPLINE_CROSSWALK.csv`.

## Classification rule

OpenAlex currently uses a four-level aboutness hierarchy: **domain → field → subfield → topic**. Topics are inferred from each work's own metadata/text/citation context, and the highest-scoring topic becomes `primary_topic`. Every classified work therefore has one primary subfield and one primary field.

For the confirmatory analysis, ARIS4C003 uses **only the primary topic roll-up**:

- `primary_topic.subfield.id` for narrow/mid-sized conceptual disciplines;
- `primary_topic.field.id` for intentionally broad comparator disciplines (Mathematics, Physics, Chemistry, Computer Science, Materials Science).

This makes primary discipline assignment mutually exclusive within the 21-category crosswalk: a work is not credited to multiple ARIS4C003 disciplines simply because secondary topics span several subjects.

OpenAlex reports that a nontrivial minority of works lack a classifiable topic. These works are excluded from the discipline-specific numerator but must be counted in a coverage diagnostic by country/year/language rather than silently ignored.

## Why not `topics.subfield.id`?

Filtering on `topics.subfield.id` matches any of a work's assigned topics and improves recall, but it permits one work to contribute to multiple disciplines. That is useful as a **sensitivity analysis**, not as the primary specialization count.

Primary: single `primary_topic` classification.

Sensitivity: any-of-topics classification with explicit multiple-count handling.

## Exact OpenAlex IDs

The IDs in the CSV were frozen from the current 2026 OpenAlex hierarchy. Relevant examples from the current hierarchy include:

- Anthropology `3314`
- Archaeology `1204`, `3302`
- Development `3303`
- Geography, Planning and Development `3305`
- Language and Linguistics `1203`; Linguistics and Language `3310`
- Education `3304`
- Demography `3317`
- Law `3308`
- Public Administration `3321`
- Sociology and Political Science `3312`
- Political Science and International Relations `3320`
- Public Health, Environmental and Occupational Health `2739`
- Epidemiology `2713`
- Infectious Diseases `2725`
- Parasitology `2405`
- Agronomy and Crop Science `1102`
- Forestry `1107`
- Horticulture `1108`
- Soil Science `1111`
- Geochemistry and Petrology `1906`
- Geology `1907`
- Geophysics `1908`
- OpenAlex fields: Mathematics `26`, Chemistry `16`, Computer Science `17`, Materials Science `25`, Physics and Astronomy `31`.

## Known construct caveats frozen before outcomes

### Archaeology

OpenAlex contains **two distinct subfields named Archeology** (`1204` and `3302`). Both are included. Dropping either after seeing outcomes is prohibited in the confirmatory analysis.

### Linguistics

OpenAlex similarly contains both `Language and Linguistics` (`1203`) and `Linguistics and Language` (`3310`). Both are included.

### Sociology

The closest standard OpenAlex subfield is `Sociology and Political Science` (`3312`). Because Political Science / IR also has its own separate subfield (`3320`), the sociology operationalization inherits some labeling ambiguity from the source taxonomy. This must be acknowledged rather than fixed post hoc.

A later topic-based **sociology-only** sensitivity mapping may be constructed, but only as a prespecified sensitivity and never substituted for the primary mapping based on whichever result is stronger.

### Tropical Medicine / colonial-health-related Public Health

OpenAlex has no single `Tropical Medicine` subfield. The primary operationalization therefore combines four historically and substantively relevant subfields:

- Epidemiology (`2713`)
- Public Health, Environmental and Occupational Health (`2739`)
- Infectious Diseases (`2725`)
- Parasitology (`2405`)

This is intentionally broader than a pure tropical-medicine topic set. Historical evidence shows tropical-medicine journals distribute their topics across exactly these kinds of subfields (for example malaria/mosquito control in public health, parasitic disease in infectious diseases, and parasite biology in parasitology).

A narrower topic-based tropical-medicine bundle is a **predeclared sensitivity**. It must be defined from topic labels/historical relevance without consulting country outcome patterns.

### Agriculture & Forestry

Primary bundle uses Agronomy/Crop Science, Forestry, Horticulture, and Soil Science. It intentionally excludes all Plant Science and all Agricultural & Biological Sciences to avoid turning the concept into a very broad basic-life-science field.

### Geology / Earth-resource sciences

Primary bundle uses Geochemistry & Petrology, Geology, and Geophysics. Paleontology and broad Earth-surface/environmental fields are excluded from the primary mapping.

### Public Administration / Social Policy

The primary mapping is deliberately narrow: `Public Administration` (`3321`). Social-policy topics occur across several OpenAlex subfields and would require a manually curated topic bundle. A topic-based social-policy extension is therefore sensitivity-only unless separately frozen before data extraction.

### Broad comparator fields

Mathematics, Physics, Chemistry, Computer Science, and Materials Science use the entire OpenAlex field rather than an arbitrarily selected "general" subfield. This matches their conceptual breadth and avoids choosing a particular subfield after outcomes are known.

Field breadth differs across the 21 concepts. The primary PPML design includes discipline×period fixed effects, which absorb global level/size differences but do not eliminate every consequence of category breadth. A secondary balanced-granularity analysis should therefore repeat the test using a prespecified subfield-only comparator set.

## Taxonomy versioning

OpenAlex's hierarchy and topic classifier can change. Every data build must record:

- snapshot/retrieval date;
- the displayed name for every frozen ID;
- whether an ID has been retired/remapped;
- the count of classified/unclassified works.

If a future OpenAlex snapshot changes the hierarchy, do **not** silently replace IDs. Create a versioned crosswalk amendment and rerun the original mapping where technically possible.

## No post-outcome substitution rule

Once the confirmatory outcome matrix is generated:

- no discipline may be removed for giving an inconvenient result;
- no ID may be swapped for a neighboring subfield because it produces a clearer pattern;
- topic-based narrowings are sensitivity analyses only unless frozen beforehand;
- all 21 conceptual disciplines remain reportable.
