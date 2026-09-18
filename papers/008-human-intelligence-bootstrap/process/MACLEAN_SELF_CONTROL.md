# MacLean cross-species self-control extraction · ARIS4C008

**Dataset:** MacLean et al. PNAS 2014 Self-Control Data, Figshare article 5579335.

## Exact v2 matches

The original individual-level A-not-B and Cylinder CSVs were parsed directly. Only source labels that can be mapped unambiguously to a current 008 species terminal were retained.

Current exact/unambiguous matches:
- **Pan paniscus** — A-not-B and Cylinder;
- **Pan troglodytes** — A-not-B and Cylinder;
- **Elephas maximus** — A-not-B (source file misspells genus as “Elphas”);
- **Columba livia** — A-not-B and Cylinder via White Carneau/Carnea pigeon breed label.

Ambiguous source labels such as “Gorilla”, “Orangutan”, “Marmoset” and “Capuchin” are **not** silently assigned to one v2 species.

## Key task warning

The Asian elephant row has 0% A-not-B test accuracy in seven animals. This is retained as a task result, not coded as “elephants lack self-control” or “generative cognition = 0”.

The task requires a particular sensorimotor interaction, warm-up/training path and motivation. ARIS4C008 therefore stores:
- task;
- sample size;
- mean and dispersion;
- taxonomic scope;
- accessibility/comparability caveat.

## Role in module A

This dataset contributes a **standardized inhibitory-control proxy** within A / generative cognition. It does not by itself measure:
- innovation breadth;
- causal reasoning;
- planning;
- transfer;
- cross-domain generativity.

It should enter later latent/hierarchical modeling as one indicator, not as module A itself.
