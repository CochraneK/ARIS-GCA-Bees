# ARIS4C007 · Decision log

This file is append-oriented. Preserve superseded decisions when they explain why the project changed direction; mark them as superseded rather than deleting them.

## 2026-09-19 · Continuity-standard bootstrap

**Decision:** Adopt the repository-level ARIS4C continuity/handoff contract for this paper.

**Why:** The project must remain recoverable across ChatGPT conversations, accounts, computers, and external agents without relying on one chat's memory.

**Project-specific decisions distilled from surviving project context:**
- Reject one universal animal-year ratio; benchmark multiple biological-age axes.
- Treat species/stage dependence as a result rather than forcing one conversion formula.

**Canonical follow-up:** Future material decisions should be appended with date, rationale, and affected files/commits when known.

## 2026-09-19 · Pilot 3 molecular implementation and independence contract

**Decision:** Treat MMC v3.0.0 as the canonical Universal Mammalian Clock implementation for ARIS4C007.

**Why:** Pilot 3A reproduced MMC Clock 2/3 coefficient tables and linear predictors to numerical parity, while the released MammalMethylClock v1.1.0 Clock-3 inverse wrapper diverged materially from the MMC reference. The MMC documented Clock-3 transform reproduced the reference implementation to machine precision.

**Consequences:**
- Clock 2/3 coefficients and inverse transforms are pinned to MMC v3.0.0.
- MammalMethylClock may be used only as a coefficient inventory after version/hash checks; its released Clock-3 inverse wrapper is not canonical.
- Clock 1 remains quarantined pending separate validation because of a reference-script indexing issue.

## 2026-09-19 · Independent molecular holdout and transform-separation contract

**Decision:** Make the primary molecular validation a sample-level independent holdout with respect to pan-mammalian-clock training, and keep molecular signal separate from life-history inverse transforms.

**Frozen design:**
- GSE223748 metadata: 15,043 samples, 346 species, 70 tissue labels.
- Explicit pan-clock membership: 11,514 training / 3,529 non-training.
- Primary independent holdout: 50 `training=no` samples across 6 species.
- Smoke subset: 10 samples across those 6 species because two species have only one eligible sample.
- SeSAMe non-human Mammal40 preprocessing: `SHCDPB`, compressed `.idat.gz` read directly, `collapseToPfx=TRUE`.
- Hard smoke QC: >=95% Clock2 and Clock3 CpG coverage in every sample.
- Primary inverse-transform traits: MMC v3.0.0 clock-era `anage49.csv`.
- Sensitivity traits: current Pilot0/AnAge snapshot.
- Full molecular code stores Clock2/3 linear predictors before age inversion.

**Why:** Clock2 and Clock3 were trained on life-history-derived target coordinates. Held-out sample prediction tests molecular generalization, but does not make those target constructs independent gold standards for A1/A3.

## 2026-09-19 · Pilot 3C engineering incident: TSV CRLF

**Finding:** Smoke run `35424097947` successfully installed SeSAMe 1.26.0, resolved upstream artifacts, selected the 10-sample smoke set, and downloaded all 20 IDAT files. It failed only in the post-download filename count.

**Root cause:** Python `csv.DictWriter` emitted CRLF in `download_manifest.tsv`; Bash retained the final-column carriage return in `filename`, so local files acquired a hidden `\r` suffix and no longer matched `*.idat.gz` / SeSAMe manifest paths.

**Fix:** Force LF with `lineterminator="\n"` in both Pilot 3C manifest writers and defensively `trimws()` manifest filenames in both R runners.

**Current verification run:** `35433019496`.

## 2026-09-19 · Phylogeny and longevity-quality contract

**Decision:** Comparative inference will propagate phylogenetic uncertainty across posterior mammal trees rather than rely on one MCC tree, and maximum longevity will not be treated as error-free.

**Frozen direction:**
- Primary phylogeny: Upham et al. mammal credible tree set; target 100 posterior completed trees.
- Multi-tree PGLS / phylogenetic signal with leave-one-order-out validation.
- Longevity robustness includes AnAge confidence/sample-size class, Lu-style 1.3× correction, clock-era vs current AnAge traits, and alternative survival-derived longevity denominators on data-rich subsets.

**Canonical detail:** See `process/PILOT4_PHYLOGENY_PLAN.md`.
