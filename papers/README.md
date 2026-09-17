# Papers

This directory is the canonical registry of research projects produced with ARIS.

Each paper gets one stable folder:

```text
papers/
├── 001-gca-bees/
│   └── paper.json
├── 002-next-paper/
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

1. One paper, one numbered folder. Never reuse an ID.
2. `paper.json` is the canonical metadata record used by the portfolio page.
3. Record the exact ARIS release or commit used for every new paper.
4. Keep code, figures, research-process artifacts, and manuscript outputs with the paper that produced them.
5. Historical papers keep their original provenance even after ARIS is upgraded.
6. `docs/index.html` is the public portfolio, not the canonical data source. It should be generated from paper manifests.

## Existing paper

`001-gca-bees` currently indexes the repository's original root-level research bundle. The legacy files remain in place to avoid breaking existing links. New papers should use the folder layout above from the start.

## Create the next paper

```bash
python tools/new_paper.py "Paper title" --slug short-slug
```

Then fill the generated `paper.json`, run ARIS inside that paper folder, and regenerate the portfolio page.
