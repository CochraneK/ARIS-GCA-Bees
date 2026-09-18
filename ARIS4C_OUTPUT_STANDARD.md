# ARIS4C Final Output Standard · v1

**Effective:** 2026-09-18  
**Owner:** Cochrane Kang  
**Scope:** every numbered ARIS4C research project

ARIS4C treats a research project as complete only when the scientific work and the public-facing output package are both explicit. A project may be scientifically mature before it is publication-ready, but `submission-ready` / `final` status requires the output contract below.

## 0. Alignment with upstream ARIS

This contract strengthens, rather than replaces, the upstream ARIS paper workflow. The current ARIS `paper-writing` pipeline explicitly chains `paper-plan → paper-figure → paper-write → paper-compile → auto-paper-improvement-loop`; its planning stage includes figure/table placement and its writing/review stages require figures and tables to be described, referenced, and checked. ARIS4C therefore treats figures/tables as first-class paper artifacts.

The **bilingual full-paper requirement** and the **article-type-specific minimum visual package** below are ARIS4C-specific completion rules. They are not claimed to be universal journal rules or verbatim upstream ARIS requirements.

## 1. Bilingual paper contract

Every final project should provide:

1. **English full paper** — canonical submission-facing manuscript.
2. **Chinese full paper** — a complete Chinese mirror for reading, communication, teaching, and portfolio use.

The Chinese version may preserve English bibliographic references, technical symbols, equations, variable names, and journal-specific wording where translation would reduce precision. It must not silently broaden claims beyond the English canonical manuscript.

Preferred layout:

```
paper/
  en/
  zh/
manuscript/
  MAIN.md
  MAIN.zh-CN.md
```

During active research, a Chinese extended abstract is acceptable as an interim artifact. It is **not** sufficient for `submission-ready`.

## 2. Figure and table contract

Figures and tables are scientific communication artifacts, not decoration. The required visual package depends on article type.

### Empirical / quantitative papers
Default minimum:
- >= 2 substantive figures;
- >= 1 substantive table.

Examples: effect estimates, model comparison, robustness/sensitivity, sample/data flow, descriptive structure.

### Theory / synthesis / review papers
Default minimum:
- >= 1 conceptual or evidence-structure figure;
- >= 1 evidence/model table;
- if quantitative synthesis is present, >= 1 quantitative figure.

### Methods / benchmark / agent papers
Default minimum:
- >= 1 architecture/pipeline figure;
- >= 1 benchmark/evaluation table;
- empirical performance figures when results exist.

### Exceptions
A paper may have fewer figures/tables only when the manuscript explicitly records why a visual would add no scientific information. The exception must be visible in the paper's output metadata.

## 3. Reproducibility contract for visuals

Whenever possible:
- figure source data must be stored or reproducibly derived;
- figure-generation code must be committed;
- captions must distinguish empirical results from simulations/synthetic diagnostics;
- synthetic or illustrative figures must never be presented as empirical evidence;
- figure/table claims must agree with the canonical manuscript and machine-readable outputs.

Preferred layout:

```
figures/
tables/
code/
data/
```

## 4. Page contract

The ARIS4C public hub should expose, when available:

- English paper
- 中文论文
- Figures
- Tables
- Pipeline / Status
- Source

The dashboard should also make output completeness visible rather than treating manuscript progress alone as completion.

## 5. Final-status gate

A project may be marked `submission-ready` / `final` only if all applicable items pass:

- [ ] English full manuscript
- [ ] Chinese full manuscript
- [ ] appropriate figure package
- [ ] appropriate table package
- [ ] figures/tables traceable to evidence or explicitly labeled conceptual/synthetic
- [ ] references checked
- [ ] limitations explicit
- [ ] reproducibility artifacts present where applicable
- [ ] independent/reviewer gate complete where required
- [ ] Page/index links current

A journal portal submission itself remains an author action and is not required for repository-level scientific completion.
