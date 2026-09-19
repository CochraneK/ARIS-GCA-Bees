# ARIS4C014 · Repository Architecture Decision

Date: 2026-09-19
Status: accepted design direction; implementation pending

## Decision

Separate the growing implementation into three responsibilities:

### ARIS4C014

**Role: scientific parent / research record**

Keep:

- paper and bilingual manuscript outputs;
- research questions and hypotheses;
- source-feasibility pilots;
- frozen results and artifacts;
- methods / protocol / validation;
- scientific decisions and limitations;
- links to the reusable implementation.

ARIS4C014 should remain permanently available even after reusable code is extracted.

### OpenIntegrity

**Role: reusable implementation / agent product**

Create a dedicated repository for the reusable engine once extraction begins.

Expected top-level responsibilities:

- source adapters;
- organization ontology;
- identity resolution;
- evidence graph;
- detectors;
- reports / review packets;
- agent / skill interfaces;
- tests;
- CI / live source-smoke workflows;
- public documentation.

Suggested module shape:

```text
OpenIntegrity/
  openintegrity/
    sources/
    ontology/
    identity/
    graph/
    detectors/
    reports/
    agents/
  tests/
  examples/
  docs/
  SKILL.md
```

The current ARIS4C implementation is the seed for this repository.

### repo-auditor

**Role: independent repository auditor**

Do not merge OpenIntegrity into repo-auditor.

repo-auditor should review OpenIntegrity for:

- reproducibility;
- provenance;
- source contracts;
- security;
- privacy;
- defamation / claim-strength safeguards;
- code quality;
- test coverage;
- public-release readiness.

This preserves separation between the system being built and the system auditing it.

## Why split now

OpenIntegrity has already moved beyond a small paper appendix. The current ARIS4C014 implementation includes:

- live China procurement adapters;
- USCC stable-ID extraction;
- institution-universe adapters;
- cross-source identity logic;
- Evidence Graph;
- detector semantics;
- CI and live workflows;
- Agent Skill;
- UK portability baseline.

Future hospital, SOE, university, rural-collective, social-organization, fund and audit/outcome modules would otherwise make the paper repository increasingly product-like.

## Relationship after extraction

```text
ARIS4C014
  scientific methods / pilots / papers
          |
          v
OpenIntegrity
  reusable engine / data adapters / graph / detectors
          |
          v
repo-auditor
  independent quality / safety / release audit
```

Future ARIS4C papers may reuse the same OpenIntegrity engine rather than duplicate implementation.

## Current implementation state

As of this decision, no separate repository named `OpenIntegrity` was found in the connected GitHub installation.

Therefore this is a recorded architecture decision, not a claim that migration has already happened.

## Migration rule

When creating the standalone repository:

1. copy/migrate reusable code and tests from ARIS4C014;
2. preserve Git-visible provenance and links back to ARIS4C014;
3. keep frozen pilot artifacts and scientific interpretation in ARIS4C014;
4. avoid deleting working ARIS4C014 code until parity tests pass in OpenIntegrity;
5. run repo-auditor after extraction;
6. update both repositories with reciprocal links;
7. only then mark the reusable implementation in ARIS4C014 as delegated.

## Immediate next implementation sequence

1. bootstrap the standalone OpenIntegrity repository;
2. migrate reusable core + China adapters + tests/workflows without changing semantics;
3. verify parity under CI;
4. continue exact-stable-ID cross-source enrichment;
5. implement high-value institution-universe modules from `CHINA_INSTITUTION_ONTOLOGY.md`;
6. run repo-auditor on the extracted repository.
