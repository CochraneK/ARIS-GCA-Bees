# CHATGPT HANDOFF · ARIS4C008

Updated: 2026-09-19  
Canonical branch: **aris4c008-pilot9**

This file is the rolling handoff for another computer, account, ChatGPT session, coding agent or reviewer.

## 1. What this project is really asking

The project began from a cross-species “skill allocation” intuition, but the scientifically important target became:

> **Which conditions are necessary, sufficient, enabling, bottleneck or amplifying for the evolution of advanced, open-ended cumulative intelligence; what combination makes humans unusual; and which nonhuman animals already overlap substantially with that combination?**

Do not reduce the question to “which animal is smartest”.

Do not interpret “potential” as a prediction that a living species will evolve into humans. Here, **potential = overlap with a hypothesized causal configuration under explicit uncertainty**.

## 2. Canonical scientific framing

The working model is a **bootstrap / conjunctive architecture**, not one magic trait and not a fixed total “skill-point budget”.

Condition modules:

- **A** generative cognition
- **B** social transmission
- **C** communication
- **D** manipulation / embodiment
- **E** persistent externalization
- **F** social architecture
- **G** life history / learning opportunity
- **H** energetics / neural budget
- **I** ecological challenge / opportunity
- **J** demography / cultural population

Outcomes are coded separately (O1–O7). Never infer outcomes directly from A–J.

Key candidate architectures:
- additive;
- weakest-link;
- threshold / conjunctive;
- dynamic feedback / temporal-network interaction, which must be modeled separately rather than as a static catch-all.

## 3. Current canonical data state

Use:

- data/module_evidence_state_tier1_v2.csv
- data/deep_coding_cell_queue_v2.csv

Tier-1 panel: **79 taxa = retained29 + new50**.

Current observed coverage:

| Module | Observed / 79 |
|---|---:|
| A | 21 |
| B | 22 |
| C | 34 |
| D | 18 |
| E | 17 |
| F | 32 |
| G | 60 |
| H | 55 |
| I | 53 |
| J | 41 |

A–F:
- 144 observed cells;
- **330 unobserved cells**.

Cohort split:
- retained29: 46/174 observed, **128 missing**;
- new50: 98/300 observed, **202 missing**.

All new50 have completed standardized first-pass A–F coding.

The former “remaining21” workstream is **closed at first pass**:
- 126/126 cells have a state;
- 0 pending_first_pass.

## 4. Current next queue

Canonical: data/deep_coding_cell_queue_v2.csv

The queue has 330 cells:
- retained29_backfill = 128;
- new50_targeted_second_pass = 202.

Process in balanced bundles:

### ABE core
A generative cognition  
B social transmission  
E persistent externalization

### CDF support
C communication  
D manipulation/embodiment  
F social architecture

Do not simply complete one module column globally. Pilot-9 simulations showed that uneven missingness can make threshold/weakest-link architectures less recoverable even when total coverage rises.

## 5. Evidence rules that must not be relaxed

### Exact species
Same-genus / same-family evidence does **not** substitute for focal-species evidence.

Allowed:
- documented synonym/current-name crosswalk;
- explicit operational taxon crosswalk.

### Retrieval fallback
If scientific-name retrieval is sparse, run common-name fallback. This was especially important for cetaceans.

### Missingness
not_located_first_pass is **not a zero** and **not trait absence**.

### Tested negative
A negative is accepted only when a named subindicator/task was explicitly tested and failed.

A tested negative narrows a module and can coexist with positive evidence in the same module.

Examples:
- Melursus ursinus: spatial-transposition positive evidence + failure on one novel problem.
- Gasterosteus aculeatus: social learning positive + no evidence for individual recognition in one paradigm.
- Crocuta crocuta: innovation/cooperation positive + demonstrator opportunity did not raise novel technical-problem solving success.
- Nephila clavipes: other learning evidence + site-tenacity experience effect not supported.
- Hyla versicolor: acoustic communication positive + one auditory-streaming effect not supported.

## 6. Important newly coded examples

Do not overgeneralize beyond the cited task.

- **Poecilia reticulata**: foraging innovation; social learning of foraging routes; visual courtship signalling; social-network/information effects.
- **Desmodus rotundus**: observer bats learned a maze exit with demonstrators and most successful observers retained it after demonstrator removal; long-term cooperative relationships predict social foraging.
- **Gasterosteus aculeatus**: social learning plus persistent nest construction; separate tested-negative individual-recognition result.
- **Bison bison**: memory-guided adaptive foraging; acoustic mother-offspring communication; collective movement decision-making.
- **Crocuta crocuta**: innovation, multimodal communication, cooperation; social-learning technical-task boundary.
- **Balaenoptera musculus / Eschrichtius robustus / Eubalaena spp.**: exact-species acoustic communication evidence. Do not auto-convert whale song/call evidence into B cultural transmission.
- **Galerella sanguinea**: measured social organization of a largely solitary carnivore.
- **Hyaena brunnea**: scent-marking communication plus communal denning/clan associations.
- **Leptonychotes weddellii**: structured underwater vocal repertoire.
- **Oophaga pumilio** is the current name used in direct navigation evidence for operational Dendrobates pumilio; maintain the taxonomic crosswalk.

## 7. Recoverability: what is valid and what is stale

The architecture-balanced simulation logic is useful as a design diagnostic.

Important findings:
- sample size alone is not enough;
- balanced module coverage matters;
- random complete configurations are less informative than deliberately discriminating configuration geometry;
- A/B/E are high-value for distinguishing candidate architectures, but C/D/F cannot be ignored.

**Caution:** tier1_recoverability_v3.csv was generated before the final all-new50 first-pass closure. It is an interim design artifact, not the latest recovery result for module_evidence_state_tier1_v2.csv.

The v3 code also had an important implementation correction:
- scenarios should share common random numbers when comparing masks;
- otherwise scenario-specific random seeds confound mask effects.

A browser execution of a larger marginal simulation timed out; a lower-repetition exploratory run was used. Before publication-quality claims, rerun with more repetitions in a stable environment / CI.

## 8. Outcome status

O1–O7 coding exists for theory/calibration subsets but is **not complete for all 79 taxa**.

This is a major blocker.

Do not estimate necessary/sufficient condition sets until outcomes are independently coded across Tier-1.

## 9. G–J priority

After sufficient A–F progress:

1. J demography / cultural population
2. H energetics / neural budget
3. I ecology
4. G life history last among G–J

## 10. Confirmatory gate remains blocked

Do not make claims such as:
- “X is necessary for human intelligence”
- “Y is sufficient”
- “species Z has the highest evolutionary potential”

until:
- A–F are substantially more balanced;
- O1–O7 covers all 79;
- J/H are improved;
- phylogenetic branch lengths/timing are justified;
- measurement uncertainty is propagated;
- evidence-presence states are replaced by empirical/ordinal/latent module values;
- observed-data architecture recoverability is acceptable.

## 11. Files to read first in a new session

1. process/STATUS.md
2. process/PILOT9_NEXT_DEEP_CODING.md
3. process/CONDITION_ONTOLOGY.md
4. process/OUTCOME_CODEBOOK.md
5. process/TIER1_MODULE_MATRIX.md
6. data/module_evidence_state_tier1_v2.csv
7. data/deep_coding_cell_queue_v2.csv
8. process/UNDERREPRESENTED_CLADE_CONTROLS.md
9. process/THEORY_CANDIDATE_EVIDENCE.md
10. process/OBSERVED_MISSINGNESS_RECOVERABILITY.md
11. code/build_deep_coding_cell_queue.py
12. code/simulate_tier1_recoverability_v3.py

## 12. Exact next actions for the next agent

1. Take a small balanced batch from deep_coding_cell_queue_v2.csv.
2. Include both ABE and CDF cells in the batch.
3. Prioritize retained29 backfill while interleaving new50 second-pass cells.
4. Verify focal species before coding.
5. Search tested-negative evidence in parallel.
6. Update evidence tables and regenerate the matrix/queue after each meaningful batch.
7. Begin full-79 O1–O7 outcome expansion in parallel.
8. After a balanced milestone, rerun recoverability against the current matrix.
9. Preserve old versions; create v3/v4 artifacts rather than silently overwriting audit history.

## 13. User workflow preference relevant to this project

When scope is clear, work in **GO mode**:
- continue autonomously;
- minimize confirmation prompts;
- implement, inspect, correct and continue;
- persist progress to Git frequently;
- keep one canonical source of truth in the repository.

For every ARIS4C paper, Git should retain enough handoff/chat context for another computer/account/agent to resume without the original conversation.
