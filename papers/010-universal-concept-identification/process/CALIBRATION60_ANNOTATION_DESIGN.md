# ARIS4C010 · Lexical Calibration60 Annotation Design

## Purpose

The 60-target OEWN source pool tests **within-surface-form semantic identification** before the project expands to the full mixed concept benchmark.

The source pool contains 10 lemma groups × 6 noun senses. All senses from one lemma remain grouped to prevent trivial surface-form leakage.

## Two layers

### Source layer
Generated automatically from pinned `oewn:2025` via `wn==1.1.1`.

It contains only:
- lemma;
- OEWN sense ID;
- OEWN synset ID;
- lexname;
- definition;
- examples;
- ILI when available.

### Annotation layer
Pairs source targets with 24 generic semantic questions.

No answers are pre-filled.

## Why a generic query bank

Pilot 2 used questions designed after inspecting `bank` and `spring` glosses. That is acceptable for an engineering pilot but creates optimism bias.

Calibration60 therefore uses a **fixed target-independent question bank**. Question wording cannot contain the target lemma or a synonym/gloss fragment.

## Packet sizes

- Full matrix: **60 × 24 = 1,440** target-query pairs.
- Initial human calibration subset: **60 × 12 = 720** pairs.

The 12-query subset is selected deterministically from group ID and source selection rank, without using any expected semantic response.

## P2 vs P6

Every pair is compatible with both protocols.

### P2
- YES
- NO

### P3
- YES
- NO
- MAYBE

P3 is the **coarse non-binary control**. It tests whether gains over P2 arise simply because participants receive an escape option when binary forcing is inappropriate.

### P6
- YES
- NO
- BORDERLINE
- UNKNOWN
- UNDEFINED
- BOTH

The same target-query pair must be used across all protocol conditions. Protocol assignment/counterbalancing occurs at participant/session level, not by changing the question set.

## Primary calibration outcomes

1. response agreement;
2. retest consistency;
3. per-class confusion;
4. response time;
5. confidence;
6. proportion of P6 responses that are not reducible to an ordinary confident YES/NO;
7. pairwise target separation using majority/probabilistic human responses;
8. semantic query overhead after human calibration.

## Important interpretation boundary

This lexical calibration primarily tests **semantic separability and oracle reliability for ordinary polysemy**.

It is not expected to generate many BORDERLINE/UNDEFINED/BOTH responses. Those states are tested more strongly in the mixed stress calibration containing vague, contextual, empty, contradictory and pathological targets.


## Why P3 is essential

ICML 2025 adaptive Twenty Questions work already uses a coarse multi-valued response style (e.g. no / maybe / yes). Therefore “more than two answer labels” is not a 010 novelty claim.

The mechanistic comparison is:

- **P2 → P3:** value of allowing any coarse uncertainty/escape response;
- **P3 → P6:** value of distinguishing *why* a binary answer fails;
- **P2 → P6:** total effect of the fine-grained semantic protocol.

A P6 advantage that disappears relative to P3 would imply that fine-grained semantic state distinctions add little beyond a generic MAYBE option.
