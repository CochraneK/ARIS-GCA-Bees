# Papers

This directory is the canonical registry of research projects produced with ARIS.

## Numbering status

| Slot | Status | Location |
|---|---|---|
| 001 | formal paper | `papers/001-gca-bees/` |
| **002** | **RESERVED REVIEW CANDIDATE — not promoted** | `papers/002-REVIEW-CANDIDATE.md` → `ideas/language-periodic-system/` |
| 003 | formal paper | `papers/003-colonial-disciplinary-advantage/` |
| 004 | formal paper | `papers/004-counterfactual-cost-of-exclusion/` |
| 005 | formal paper | `papers/005-hidden-burden-bad-science/` |
| 006 | formal paper | `papers/006-chinese-alphabetical-exposure/` |

The 002 pointer is deliberately a **file, not a paper folder**. It makes the review candidate discoverable to WorkBuddy while preserving the rule that a numbered paper directory is created only after the ARIS promotion gate passes.

## Stable paper layout

Each promoted paper gets one stable folder:

```text
papers/
├── 001-gca-bees/
│   └── paper.json
├── 002-<slug>/        # created only after 002 passes review
│   ├── paper.json
│   ├── README.md
│   ├── code/
│   ├── data/
│   ├── figures/
│   ├── manuscript/
│   └── process/
└── ...
```

## Rules

1. One promoted paper, one numbered folder. Never reuse a promoted ID.
2. A review-slot pointer such as `002-REVIEW-CANDIDATE.md` is **not** a promoted paper.
3. `paper.json` is the canonical metadata record for promoted papers and the portfolio page.
4. Record the exact ARIS release or commit used for every new paper.
5. Keep code, figures, research-process artifacts, and manuscript outputs with the paper that produced them.
6. Historical papers keep their original provenance even after ARIS is upgraded.
7. `docs/index.html` is the public portfolio, not the canonical data source.

## 002 review

Reviewers looking for **002** should open:

`papers/002-REVIEW-CANDIDATE.md`

The actual review materials remain under:

`ideas/language-periodic-system/`

A formal `papers/002-*` folder must not be created until an independent ARIS reviewer authorizes promotion.
