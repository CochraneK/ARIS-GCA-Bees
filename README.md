<p align="right">
  <a href="./README.md"><img src="https://img.shields.io/badge/Language-English-blue" alt="English"></a>
  <a href="./README.zh-CN.md"><img src="https://img.shields.io/badge/语言-中文-red" alt="中文"></a>
</p>

<div align="center">

# ARIS4C

**ARIS for Cochrane · a living research hub for papers developed with ARIS**

[**Paper Hub**](docs/index.html) · [**Papers Registry**](papers/) · [**Paper 001**](docs/paper/en/main.html) · [**中文**](README.zh-CN.md)

</div>

## What is ARIS4C?

**ARIS4C = ARIS for Cochrane.** It is the long-lived research repository for papers developed with the [ARIS](https://github.com/wanshuiyin/Auto-claude-code-research-in-sleep) methodology.

ARIS is the research engine; ARIS4C is the paper registry, evidence trail and public portfolio. Each promoted paper owns its manuscript, code, data notes and process records under one numbered folder and records the exact ARIS version used.

## Repository model

    ARIS4C/
    ├── papers/
    │   ├── 001-gca-bees/
    │   │   ├── paper.json
    │   │   ├── README.md
    │   │   ├── code/
    │   │   ├── data/
    │   │   ├── manuscript/
    │   │   └── process/
    │   ├── 003-...
    │   └── ...
    ├── docs/
    │   └── index.html
    ├── tools/
    │   ├── new_paper.py
    │   ├── build_papers_index.py
    │   └── sync_aris.ps1
    └── aris.lock.json

## Paper 001 · reconstructed

**Uncertainty Monitoring and Cross-Task Cognitive Covariation in Honey Bees**

Paper 001 was fully reconstructed on 2026-09-18 with ARIS v0.4.26. The earlier single-precision/self-awareness simulation is no longer canonical. The new project compares domain-general, two-factor, associative and hybrid explanations and requires same-individual empirical evidence before making mechanistic claims.

- [English research-design page](docs/paper/en/main.html)
- [中文研究设计页](docs/paper/zh/main.html)
- [Canonical Paper 001 folder](papers/001-gca-bees/)
- [Status and gates](papers/001-gca-bees/process/STATUS.md)

## Final output contract

ARIS4C final papers now follow [ARIS4C_OUTPUT_STANDARD.md](ARIS4C_OUTPUT_STANDARD.md): English full paper + Chinese full paper + an article-type-appropriate figure/table package, with reproducible provenance where applicable. Final/submission-ready projects should expose these outputs on the public Research Command Center.

## Keep ARIS current

The repository currently recommends **ARIS v0.4.26** in aris.lock.json. New work records the exact tag/commit used; prior research history remains available through Git.

## Principle

> Upgrade the research engine, and allow stronger methods to replace weaker canonical claims when a paper is explicitly reconstructed.

Maintainer: **Cochrane Kang**
