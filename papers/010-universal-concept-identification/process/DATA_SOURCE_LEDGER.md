# ARIS4C010 · Data Source Ledger

**Updated:** 2026-09-18  
**Purpose:** record what each external resource may contribute to UCID, what it cannot establish, and redistribution/licensing constraints before Benchmark v0 is populated.

This is an engineering/research ledger, not legal advice. License terms must be rechecked at the exact version/date used in a public release.

| Resource | Planned role | Current license signal | Main value | Main limitation / action |
|---|---|---|---|---|
| Open English WordNet | lexical senses, synonym sets, lexical relations, polysemy strata | CC BY 4.0 | open synset-based lexical backbone; current site reports 120,068 synsets and 153,261 entries | English lexicalization is not a universal concept ontology; preserve attribution and source IDs |
| Wikidata | entities, classes, properties, lexemes, external identifiers | structured data in main/Property/Lexeme/EntitySchema namespaces under CC0 | huge multilingual knowledge graph; useful for referents and open-world sampling | graph is community-curated and ontologically heterogeneous; do not treat class hierarchy as philosophical ground truth |
| Basic Formal Ontology (BFO) | upper-level comparison / mapping baseline | CC BY 4.0 | explicit upper-level scientific ontology and typed continuant/occurrent-style distinctions | deliberately narrow/scientific-realist; insufficient alone for fiction, lexical ambiguity, many social/phenomenal targets |
| THINGS / THINGSplus | concrete-object bridge stratum and norms | current THINGS site says original images are academic-use-only; THINGSplus supplies 1,854 license-free alternative images; concept metadata must be version-checked separately | 1,854 object concepts, category structure, typicality/nameability and semantic dimensions | do not redistribute original images; UCID can initially use concept identifiers/metadata and avoid images unless exact rights are verified |
| ConceptNet 5 | commonsense relations / external graph baseline | complete data CC BY-SA 4.0; code Apache 2.0 | broad multilingual relation graph and useful non-is-a relations | ShareAlike matters when combining/distributing data; safest v0 role is external baseline/lookup unless release licensing is designed around it |
| ICML 2025 Twenty Questions data | bridge benchmark for adaptive natural-language elicitation | **license not yet verified in this ledger** | directly comparable concrete-object hidden-target benchmark; reported hundreds of objects and large question bank | do not vendor or redistribute until exact dataset license/version is recorded |
| BIG-bench twenty_questions | task-design prior / possible small comparison | repository license/version must be checked at ingestion time | explicit Twenty Questions LM task; task authors note arbitrary categories and suggest more comprehensive ontology | not broad enough for UCID target ontology; use mainly as prior-art/task reference |
| Constructed UCID stress cases | compositional, empty, impossible, vague, indexical, paradoxical, undecidable and ineffability-boundary cases | ARIS4C-authored metadata | lets the benchmark target regimes poorly covered by lexical/object resources | labels are theory-laden; require transparent definitions and human/expert adjudication before gold status |

## Resource policy

### 1. No source is "the concept universe"

Each resource covers a different projection:

- WordNet-like resources: **lexicalized senses**;
- Wikidata: **referents + community knowledge graph**;
- BFO: **upper-level ontological commitments**;
- THINGS: **concrete object concepts**;
- ConceptNet: **commonsense relational associations**;
- UCID stress suite: **formal/semantic boundary cases**.

UCID should preserve these provenance layers instead of merging them into one supposedly neutral truth graph.

### 2. Keep source-native identifiers

Where available, every imported record should retain:
- resource name;
- release/version;
- native ID;
- retrieval date;
- license;
- original label/gloss;
- transformation log.

### 3. Separate import from adjudication

An imported label such as a Wikidata class or WordNet hypernym is evidence from that resource, not automatically a UCID gold ontology label.

The pipeline should maintain:

```text
source assertion
→ normalized candidate mapping
→ automated checks
→ human/adjudicated UCID mapping
```

### 4. License isolation

Resources with reciprocal/share-alike obligations should be stored in clearly separated derived artifacts where practical. The core UCID-authored benchmark should not accidentally inherit incompatible distribution terms because one external graph was bulk-merged without planning.

### 5. No image dependency in the core benchmark

The core scientific result concerns semantic query identifiability. Images may later support ostensive/multimodal grounding, but v0 should remain reproducible without redistributing third-party image corpora.

## Immediate v0 source stack

Recommended first implementation:

1. **Open English WordNet** — sense-level lexical backbone;
2. **Wikidata** — referent/entity bridge and multilingual IDs;
3. **THINGS concept list / norms** — concrete bridge stratum, with no original-image redistribution;
4. **BFO** — one upper-ontology baseline, not canonical truth;
5. **UCID-authored stress suite** — semantic regimes missing from ordinary resources;
6. **ConceptNet** — evaluation/lookup baseline first, bulk merge later only if licensing architecture is explicit.

## Pre-release checklist

- [ ] freeze exact resource versions;
- [ ] store retrieval dates and checksums;
- [ ] attach license text/URLs in provenance metadata;
- [ ] confirm whether transformed/combined outputs trigger attribution/share-alike requirements;
- [ ] ensure no unlicensed image redistribution;
- [ ] document every normalization/mapping script;
- [ ] separate machine-generated mappings from adjudicated labels;
- [ ] provide citations for all imported resources.
