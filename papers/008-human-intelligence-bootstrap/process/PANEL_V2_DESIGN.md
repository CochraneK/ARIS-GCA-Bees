# Pilot panel v2 design · model-discriminating sampling

## Why the panel must change

The first 25 taxa were chosen mainly because they are high-information comparative cognition cases. The recoverability pilot shows that this is not enough: taxa clustered in a generally "high cognition / high social complexity" corner make additive, weakest-link and threshold architectures difficult to distinguish.

The v2 panel therefore optimizes **configuration contrast**, not a "smart animal" list.

## Sampling objective

For each candidate taxon, estimate a provisional module signature with uncertainty. Prefer additions that occupy cells where the competing models make different predictions:

1. **high average / severe bottleneck** — many strong modules, one weak module;
2. **moderate average / no severe bottleneck** — tests whether balance can outperform specialization;
3. **threshold straddlers** — several modules close to the candidate transition threshold;
4. **cognition-matched / embodiment-different** pairs;
5. **social-learning-matched / life-history-different** pairs;
6. **externalization-high / individual-cognition-modest** cases;
7. **long-life / low cultural breadth** controls;
8. **high cooperation / low manipulatory technology** controls.

## Candidate calibration taxa — evidence review required before inclusion

These are **sampling candidates, not claims that the listed contrast is already established**.

| Candidate | Intended contrast cell |
|---|---|
| zebra finch / another well-studied songbird | high vocal learning, limited manipulatory technology |
| greater sac-winged bat or another vocal-learning bat | mammalian vocal-learning convergence |
| sea otter | habitual tool use under non-primate embodiment |
| beaver | persistent environmental construction / externalization |
| bowerbird | persistent construction and socially structured display |
| wolf or African wild dog | cooperation with limited precision manipulation |
| Norway rat | general learning / social learning calibration |
| naked mole-rat | extreme sociality + longevity configuration |
| giant tortoise | extreme longevity without assumed high cultural breadth |
| cleaner wrasse | social cognition under very different neural/body constraints |
| Portia jumping spider | flexible problem solving with a tiny nervous system |
| leaf-cutter ant | division of labour and persistent colony infrastructure |
| great tit | experimentally seeded cultural diffusion |
| scrub-jay | caching / future-oriented information use |
| sea lion / pinniped comparator | marine social cognition with different manipulation from cetaceans |

## Inclusion rule

A candidate enters v2 only when:
- at least two critical modules have source-traceable evidence;
- its configuration adds measurable model disagreement relative to current taxa;
- missingness is not worse than the expected information gain;
- a compatible phylogeny/taxonomy key can be assigned.

## Selection algorithm

Once provisional module values exist for a larger candidate pool:

1. calculate predicted outcomes under additive, weakest-link and threshold models;
2. standardize those predictions;
3. choose taxa that maximize pairwise distance in **model-prediction signature space**;
4. add phylogenetic coverage as a secondary objective;
5. reserve ~20% of the final panel for deliberately ordinary/negative calibration taxa.

The final paper should report both the selection algorithm and sensitivity to an unselected/random panel.


## Pilot 7 recoverability implication

The observed 29 × 10 module mask confirms that the seed panel is not merely incomplete; it is **structurally under-informative** for weakest-link/threshold discrimination.

Current exact/proxy measurement coverage is especially sparse in A, C, D, E and F.

A design simulation found:
- current observed mask: threshold recovery ~0.16;
- complete but randomly configured 29 taxa: threshold recovery ~0.26;
- complete 29-taxon oracle configuration-aware selection: threshold recovery ~0.67.

These are not biological power calculations. They show that **configuration diversity is at least as important as row count**.

### Revised sampling workflow

1. Build a broad **screening pool**, not a fixed “smart animal” shortlist.
2. Obtain inexpensive provisional A–J indicators for the pool.
3. Compute candidate prediction signatures under additive / minimum / threshold summaries.
4. Select taxa that maximize disagreement in prediction-signature space.
5. Add phylogenetic diversity and data recoverability constraints.
6. Reserve ordinary/negative calibration taxa.
7. Only then spend effort on deep source-level coding.

The screening pool should be substantially larger than the final deeply coded panel. The current simulations do **not** justify a single magic target sample size such as 40, 60 or 80; sample size and configuration geometry must be evaluated jointly.

### Priority gaps

Immediate deep-coding priority:
1. A · generative cognition;
2. D · manipulation / embodiment;
3. E · persistent externalization;
4. C · communication;
5. F · social architecture.

G, I and J now have substantially better standardized coverage and are no longer the first-order bottleneck.
