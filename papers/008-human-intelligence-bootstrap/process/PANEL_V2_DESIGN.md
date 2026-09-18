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
