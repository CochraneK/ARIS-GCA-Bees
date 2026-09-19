# ChatGPT conversation distill · ARIS4C008 · 2026-09-19

This is a **distilled research record**, not a verbatim transcript. It preserves the parts of the conversation that materially affect future work.

## Origin of the idea

The starting intuition was a cross-species “skill-point allocation” analogy:

- humans: unusually strong cognition, but not exceptional raw force;
- small animals: different mobility/speed/body-size trade-offs;
- insects/spiders: fragile bodies but specialized locomotion or construction;
- long-lived animals: different pace-of-life allocations.

The early comparative framing connected this intuition to:
- life-history trade-offs;
- functional traits;
- allometry;
- evolutionary performance trade-offs;
- Pareto fronts / multi-objective optimization.

The key methodological rule from this stage was: **body mass, phylogeny and environment are constraints/covariates, not “skill points”.**

## Central pivot

The user then identified the most important scientific target:

> Find the sufficient and necessary conditions that make humans different, use them to study the core evolutionary ingredients of advanced intelligence, and identify animals that resemble parts of the human configuration / have relevant latent potential.

This changed ARIS4C008 from a general animal-trait atlas into **The Human Intelligence Bootstrap**.

## Important conceptual decisions

### 1. No single global intelligence score
Avoid “human=100, mouse=20”.

Separate cognitive/social/embodied/externalization/life-history dimensions.

### 2. No anthropocentric evolutionary ladder
Similarity to humans is not biological worth and is not destiny.

### 3. Necessary/sufficient claims require dissociations
A trait occurring in many species without advanced cumulative outcomes is evidence against simple sufficiency.

A high-level outcome occurring without a proposed condition would weaken necessity.

### 4. Human open-ended culture is not a simple binary regression target
There is effectively one extant human positive lineage, so the project must triangulate:
- lower-level transitions;
- convergent lineages;
- anti-sufficiency counterexamples;
- hominin temporal evidence;
- phylogenetically informed comparisons.

### 5. Condition and outcome coding must be independent
A–J are candidate explanatory modules.
O1–O7 are outcome states.
Do not define the outcome using the same indicators used as predictors.

## Sampling evolution

The project expanded from an initial deep seed to:
- broad 238-taxon screening pool;
- staged 79-taxon Tier-1 deep panel;
- 29 retained + 50 additions.

The 50 additions were deliberately mixed:
- theory-discriminating taxa;
- underrepresented-clade calibration taxa;
- matched ordinary controls;
- data-driven source candidates.

This was intended to prevent the study from becoming a “famous smart animals only” dataset.

## Exact-species calibration lesson

The underrepresented-clade calibration was scientifically valuable because it exposed false hits.

Examples:
- a Porcellio vibration/aggregation hit was actually another woodlouse species;
- Camponotus learning hits often referred to other Camponotus species;
- Ctenophorus search results often did not clearly focalize C. nuchalis.

Decision:
**do not borrow evidence across related species.**

## Important retrieval lesson

Scientific-name-only retrieval can undercount literature.

Cetaceans were a clear example: exact papers became much easier to locate using common names.

Decision:
use scientific name first, then common-name fallback, then exact-species verification.

## Tested-negative lesson

Absence of a hit is not a negative.

The project began explicitly collecting tested negatives, including cases where a species has positive evidence in one part of a module and failure in another.

This is important because “A present” versus “A absent” is too crude for final causal claims.

## Pilot-9 recoverability lesson

An early result looked paradoxical: more coded cells improved additive recovery but could worsen threshold recovery.

The investigation found two things:

1. comparing scenarios with different random seeds mixed Monte Carlo variation into missingness effects;
2. after fixing this with common random numbers, the larger lesson remained: **unbalanced missingness geometry can genuinely reduce architecture discrimination**.

This is why the project switched from species-only queues to **taxon × module cell queues**.

Single-column completion is not the preferred strategy.

## First cell-level queue

The first balanced queue had 351 missing A–F cells while 21 new taxa were still pending first pass.

After the remaining21 were completed and all new50 were integrated, the canonical matrix moved to v2.

The refreshed queue is now:
- **330 cells**
- 128 retained29 backfill
- 202 new50 targeted second pass

Canonical: data/deep_coding_cell_queue_v2.csv.

## Current evidence highlights from the conversation

### Guppy · Poecilia reticulata
Direct evidence located for:
- innovation;
- social learning;
- visual sexual signalling;
- social-network/information effects.

### Vampire bat · Desmodus rotundus
Direct result from the maze social-learning study:
- demonstrator presence increased exits by naive bats;
- four of five successful naive observers retained the ability after demonstrator removal;
- no naive bat exited in trials without a potential demonstrator.

Also direct cooperative/social-foraging evidence.

### Three-spined stickleback · Gasterosteus aculeatus
Direct evidence for:
- social learning;
- nest construction / environmental response;
- persistent constructed nest.

Separate tested-negative:
- no evidence for individual recognition in the tested paradigm.

### Sloth bear · Melursus ursinus
Direct positive proxy:
- spatial transposition / hidden displacement representation.

Direct tested-negative boundary:
- failure to spontaneously solve one novel problem even with social cues and relevant experience.

### Spotted hyena · Crocuta crocuta
Direct evidence for:
- innovative problem solving;
- multimodal communication;
- communication-linked cooperation.

Boundary:
- directed social-learning opportunity did not increase solution success on one novel technical task, though social effects on neophobia/attention existed.

### Whale cases
Direct species-level acoustic evidence was found for:
- Balaenoptera musculus;
- Eschrichtius robustus;
- Eubalaena australis;
- Eubalaena glacialis.

Decision:
acoustic repertoire/call evidence supports C, but does **not** automatically support B social transmission/culture.

## Current numbers at chat deletion handoff

Tier-1 v2 observed:
- A 21/79
- B 22/79
- C 34/79
- D 18/79
- E 17/79
- F 32/79
- G 60/79
- H 55/79
- I 53/79
- J 41/79

remaining21:
- 126/126 closed;
- 0 pending.

A–F remaining:
- 330 cells.

## Current research priority

The project is **not ready** to answer “what conditions are necessary/sufficient?” as a final result.

The scientifically correct next move is:
- balanced A–F backfill / second pass;
- full O1–O7 coding;
- J/H improvement;
- empirical/latent values and uncertainty;
- phylogenetic timing;
- rerun architecture recovery;
- only then estimate candidate necessary/sufficient/bottleneck configurations.

## Deletion recovery instruction

If the original ChatGPT conversation is deleted, resume from:

1. process/CHATGPT_HANDOFF.md
2. process/STATUS.md
3. process/PILOT9_NEXT_DEEP_CODING.md
4. data/module_evidence_state_tier1_v2.csv
5. data/deep_coding_cell_queue_v2.csv

The repository, not this chat, is the canonical recovery source.
