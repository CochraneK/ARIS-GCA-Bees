# ARIS4C016 Chat / Decision Record

Updated: 2026-09-19

This file preserves the scientifically relevant decisions made in the ChatGPT
design thread so that deleting or changing chat surfaces does not remove the
project's rationale. Git remains canonical.

## Origin

Initial idea:
“世界各地脏话语言学分析”.

The idea was immediately reframed away from a country-by-country profanity
dictionary toward a comparative-linguistic question:

> What does humanity repeatedly turn into taboo language, and how much of the
> observed structure is universal, genealogically inherited, community-specific,
> or measurement-generated?

The user explicitly asked that ARIS4C016 follow the ARIS route; full completion
of every ARIS stage was not required before continuing.

## Major decisions

1. Do not make a swear-word dictionary the scientific endpoint.
2. Start from an existing open multi-lab dataset before collecting new data.
3. Treat community, language, language family and country as separate levels.
4. Never count repeated English country samples as independent languages.
5. Treat translation as annotation, not semantic identity.
6. Replace the source flat category field with an orthogonal multi-axis ontology.
7. Preserve unresolved/local labels rather than forcing them into global classes.
8. Model annotation coverage as part of the measurement process.
9. Do not call country correlations causal culture effects.
10. Do not claim phonological novelty for the existing approximant hypothesis.
11. Do not use the source transcription field as global IPA.
12. Keep raw taboo/slur strings out of public derived artifacts when not scientifically necessary.
13. Require independent Coder A/B before semantic fingerprints become confirmatory.
14. Freeze the coder sample before coding to prevent cherry-picking.
15. Keep English and Chinese working manuscripts in parallel.
16. Include scientific figures; avoid decorative world maps that imply unsupported precision.

## Important empirical turns

### Turn 1 — annotation heterogeneity became the main measurement problem

Direct inspection of Study 1 showed:
- 68 primary category values;
- spelling/local variants;
- large missingness differences;
- large multi-label differences;
- logical mixing of semantic, pragmatic and social categories.

This changed the project from “compare taboo categories” to
“repair measurement first, then compare”.

### Turn 2 — naïve semantic fingerprints failed

High-confidence semantic-source coverage ranged from about 10.9% to 70.7%
across samples. Apparent domain shares therefore reflected which source labels
were semantically explicit.

The failure was retained as a substantive result rather than hidden.

### Turn 3 — repeated English items gave a stronger design

Study 2 contains 139 taboo items shared by at least two English communities.

Item-fixed-effects FWL results:
- tabooness community partial R² .0265;
- offensiveness .0361.

This supported a stable-core + contextual-modulation framing.

### Turn 4 — filler control tightened the interpretation

Shared filler controls produced larger, though much less precise, community
effects than taboo items.

Therefore:
- community modulation exists;
- it is not yet shown to be taboo-specific;
- rating calibration / sample / procedure effects remain live alternatives.

This negative control was added to both manuscripts.

### Turn 5 — independent reliability became the true next gate

A deterministic 300-row sample was frozen across all 18 communities.

Manifest SHA-256:
`48c58f91901e8c2a1aab01958e95ea28afaf0f33e7a98677f98e58b8a412c9b4`

The current assistant must not impersonate two independent coders.

### Turn 6 — pronunciation engineering became executable

The project moved beyond a phonology feasibility plan. Epitran 1.35.2 was
actually run on the checksum-verified Study-1 inventory. English required
building Flite `lex_lookup` from source according to Epitran's official
instructions; the exact Flite commit was frozen.

Mandarin and Cantonese received a better Phase-0 route than character-level
dictionary lookup: the source study already contains high-coverage
romanization, so the project uses source transcription → `cmn-Latn` /
`yue-Latn` → IPA candidate.

### Turn 7 — all 13 languages passed the engineering-feasibility gate

The full-route audit produced technical pronunciation output for
**8,187 / 8,190 Study-1 rows (99.9634%)**.

The three non-success rows were:
- two Singapore-English rows with empty/non-letter output;
- one Mandarin row without source transcription.

This changed the phonology bottleneck from **tool coverage** to
**pronunciation validity**.

The project explicitly rejects the inference:
“99.9634% technical G2P success = 99.9634% pronunciation accuracy.”

The next phonology gate is stratified native/source-language pronunciation
validation, followed by matched neutral controls and frozen approximant coding.

## Current interpretation boundary

The current paper may say:
- cross-site annotation is non-equivalent;
- same taboo items are broadly stable but modestly community-sensitive;
- current community effects are not demonstrably taboo-specific;
- genealogy/sample structure limits global claims.

It may not yet say:
- country X has more sexual/religious/kinship taboo than country Y;
- culture causes the observed rating differences;
- a semantic domain is universally dominant;
- the approximant hypothesis has been independently replicated by 016.

## Canonical continuation

Read first:
1. `process/HANDOFF.md`
2. `process/STATUS.md`
3. `manuscript/DRAFT.md`
4. `process/CODER_HANDOFF.md`
5. `process/AUDIT_SAMPLE_FREEZE.md`

Then execute the independent reliability gate.


## Chat deletion safety checkpoint

As of 2026-09-19, the scientifically useful state of this conversation has
been persisted to Git.

A future agent should not require this chat transcript. Recovery order:

1. `process/STATUS.md`
2. `process/HANDOFF.md`
3. `process/CHATLOG_SUMMARY.md`
4. `paper.json`
5. `manuscript/DRAFT.md` and `manuscript/DRAFT.zh-CN.md`
6. `process/CODER_HANDOFF.md` and `process/AUDIT_SAMPLE_FREEZE.md`
7. `process/G2P_FULL_ROUTE_AUDIT.md` and `data/phonology_runtime_lock.json`

Git is the canonical source of truth; deletion of the chat should not be
treated as deletion of project state.
