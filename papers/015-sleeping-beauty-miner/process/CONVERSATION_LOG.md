# ARIS4C015 Conversation / Decision Log

This is a distilled record of the useful decisions from the ChatGPT research
thread, preserved so the project does not depend on chat history.

## 2026-09-18 — project framing

User request: build a Sleeping Beauty mining agent using ARIS4C011.

Decisions:
- reuse 011 for integrity/provenance rather than duplicating forensic modules
- separate retrospective SB identification from prospective rediscovery
- use Candidate Evidence Cards rather than one opaque score
- treat citations as attention signals, not truth/value
- enforce historical-cutoff safety and ABSTAIN semantics

Implemented:
- reusable Agent Skill
- B / awakening metrics
- OpenAlex and SciSciNet adapters
- historical backtest and transparent citation baselines
- ranking/calibration metrics
- ARIS4C011 integrity adapter
- semantic/network proxy contract
- Prince-candidate extraction

## 2026-09-18 to 2026-09-19 — cross-source metric checks

Classic Ke et al. cases were reconstructed in OpenAlex through 2011.

Observed:
- Hummers awakening 2007 vs reference 2007
- EPR 1991 vs reference 1994
- Washburn 1995 vs reference 1995
- absolute B differed by about 13.3% on average in the three-case probe

Decision:
- awakening timing may be more source-stable than absolute B
- B thresholds must be source-calibrated rather than treated as universal

## 2026-09-19 — random mechanism cohorts fail to yield real SB cases

A real OpenAlex 100-paper 1980 Physics smoke produced 0 robust SB.
A five-seed merged cohort produced 497 unique papers and still 0 robust SB.

There were 22 low-early/high-late unconfirmed papers. Only one was a near-miss
that passed sleep/wake + provisional B but had 29 total citations through 2011,
below the recognition floor of 50.

Decision:
- stop scaling random cohorts merely to wait for rare SB events
- random cohorts belong to prospective Track B
- mechanism Track M should be case-enriched

## 2026-09-19 — known-case enriched mechanism pilot

Three classic literature cases were injected:
- Hummers 1958
- EPR 1935
- Washburn 1921

Same-year/same-field OpenAlex controls were sampled.

The first enriched run exposed a definition conflict:
all three classics passed the robust full-trajectory SB gate, but
cohort-relative early/late percentiles could label them AMBIGUOUS or
IMMEDIATE_HIT.

Decision:
- robust SB identity and cohort-relative quadrant are separate variables
- relative quadrant cannot veto robust identity

After that correction, the 153-paper enriched cohort contained 5 robust SB:
the 3 known cases plus 2 provisional additional candidates.

## 2026-09-19 — matching redesign

Initial primary comparison: SB vs Forgotten.

Problem:
- match rate could be 100% while balance was poor
- SB-vs-Forgotten sleep-window SMD ~= 3.317
- Forgotten papers were often much more deeply uncited than real SB cases

Decision:
- promote event-time risk-set matching to the primary mechanism design
- compare an SB at its awakening time with same-field/year papers that are
  still dormant at that event time
- allow a control to awaken later
- never use post-event control outcomes to select the match

Pilot M v3:
- 153 papers
- 5 robust SB
- 5/5 risk-set matches
- sleep-rate SMD ~= 0.950
- reference-count SMD ~= 0.562
- author-count SMD ~= 0.566
- balance still fails SMD < 0.10
- OpenAlex B calibration remains provisional

Decision:
- do not run mechanism regression yet
- expand the at-risk control reservoir instead of relaxing balance criteria

## 2026-09-19 — third mechanism dimension

A provisional 1921 robust-SB candidate showed that a paper may awaken and later
fade again.

Decision:
Separate post-awakening fate from both SB identity and early/late quadrant.

Implemented descriptors:
- TRANSIENT_OR_FADED
- ROUGHLY_SUSTAINED
- EXPANDED_AFTER_AWAKENING

## 2026-09-19 — time ordering of mechanism features

Mechanism features are divided into:
- M0 publication-state
- M1 sleep-period
- M2 awakening-window
- M3 post-awakening

Anti-time-reversal rule:
later events may explain awakening but cannot retroactively explain initial
neglect without an explicit longitudinal/causal design.

## Current decision state

Canonical recovery sources:
- process/HANDOFF.md
- process/STATUS.md

The original chat can be deleted without losing the current research state,
provided those files remain in Git.
