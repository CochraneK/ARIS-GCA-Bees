# WorkBuddy Handoff · ARIS Secondary Review

**Review slot:** `002`  
**Important:** there is intentionally no formal `papers/002-*` directory yet.  
**002 pointer:** `papers/002-REVIEW-CANDIDATE.md`  
**Project:** ARIS4C  
**Candidate:** `language-periodic-system`  
**Canonical candidate path:** `ideas/language-periodic-system/`  
**Canonical branch:** `main`  
**Primary executor family:** OpenAI GPT / ChatGPT-side ARIS4C workflow  
**Required reviewer:** a **different model family** from the primary executor  
**Formal Paper ID:** not assigned until review passes  
**Current gate:** formal identity-bearing ARIS secondary novelty/research review  
**Requested verdict:** `PASS` / `REVISE` / `STOP`

> If you arrived here by searching for “002”, you are in the correct place. **002 is a reserved review slot, not yet a promoted paper.** Review the candidate under `ideas/language-periodic-system/`; do not report “002 missing”.

---

## 0. Your role

You are the **independent secondary reviewer**, not a continuation of the primary executor.

Your job is to try to falsify the current framing, identify prior-art collisions, detect model-comparison unfairness, and decide whether this candidate is mature enough to be promoted to formal Paper 002.

Do **not** optimize for agreement with the primary executor.
Do **not** treat the existing summaries as authoritative.
Do **not** rewrite the scientific conclusion merely to make it more positive.
A negative or `STOP` verdict is valid if the evidence warrants it.

### Independence requirement

Before reviewing, record:

- reviewer provider / application;
- exact model name if exposed;
- model family;
- review timestamp;
- fresh-thread / fresh-session identifier or trace ID if available.

The reviewer family must be genuinely different from the primary executor family.
If you are another OpenAI GPT/Codex-family reviewer, **do not certify this gate as independent**. You may provide an advisory review, but mark it `NON_INDEPENDENT_ADVISORY`, not `PASS`.

---

## 1. Canonical source of truth

Review **only the canonical `main` branch** unless a later handoff explicitly says otherwise.

### 002 navigation

- Review-slot pointer: `papers/002-REVIEW-CANDIDATE.md`
- Candidate root: `ideas/language-periodic-system/`
- This handoff: `ideas/language-periodic-system/refine-logs/WORKBUDDY_HANDOFF.md`

Start here:

1. `ideas/language-periodic-system/refine-logs/SECONDARY_REVIEW_PACKET.md`
2. `ideas/language-periodic-system/refine-logs/FINAL_PROPOSAL.md`
3. `ideas/language-periodic-system/ARIS_STATUS.md`
4. `ideas/language-periodic-system/refine-logs/MODEL_CAPACITY_NOTE.md`
5. `ideas/language-periodic-system/refine-logs/EXPERIMENT_TRACKER.md`

Then inspect the evidence reports:

- `PILOT_REPORT.md`
- `STAGE1_REPORT.md`
- `STAGE1B_REPORT.md`
- `STAGE1C_REPORT.md`
- `STAGE1D_REPORT.md`
- `STAGE1E_REPORT.md`
- `STAGE1F_REPORT.md`
- `STAGE1G_REPORT.md`
- `STAGE1H_REPORT.md`
- `STAGE1I_REPORT.md`

If a result appears decisive, inspect the corresponding `stage1*.py` and `stage1*-results.json` rather than relying only on prose.

---

## 2. Current bounded claim under review

The primary executor proposes the following bounded conclusion:

> **The simple global circular form of the language periodic-table hypothesis is not supported by held-out predictive or direct circularity evidence. Hierarchical/non-circular structure is a stronger family-held-out benchmark across TLI, GBI, and WALS, but the study does not establish one universal tree geometry.**

You are reviewing whether **this exact bounded claim** is:

1. novel enough;
2. methodologically fair enough;
3. statistically supported enough;
4. sufficiently informative for a paper.

You are **not** being asked to certify any broader claim such as “language is a tree” or “no linguistic periodicity can exist.”

---

## 3. Independent prior-art check — mandatory

Do an independent literature search through the date of your review.

At minimum, inspect or verify the relationship to:

- Baker (2001), *The Atoms of Language*, especially “Toward a Periodic Table of Languages”;
- Port et al. (2018), *Persistent Topology of Syntax*;
- Port, Karidi & Marcolli (2022), *Topological Analysis of Syntactic Structures*;
- Skirgård et al. (2023), Grambank;
- Graff et al. (2025), GBI/TLI curation;
- Verkerk et al. (2025/2026), spatiophylogenetic grammatical-universal work;
- SIGTYP / computational typology feature-prediction literature;
- circular seriation / circular-Robinson literature, including Armstrong, Guzmán & Sing-Long and related work.

### Critical novelty question

Search specifically for studies that already do something equivalent to:

> **periodic/circular linguistic geometry vs tree / graph / low-rank / other non-periodic alternatives, evaluated out of sample on global typological structure with family-aware validation.**

If an essentially equivalent paper already exists, identify it precisely and recommend `STOP` or a major novelty reframe.

Do not accept the primary executor's prior-art search without independent checking.

---

## 4. Methodological review — mandatory

Review the following issues explicitly.

### A. Faithfulness of the periodic model

Decide whether:

- direct optimization of one angular coordinate per feature;
- circular kernels;
- circular-Robinson-style diagnostics;
- explicit wrap-around closure tests;

constitute a fair test of the **simple global circular** form of the historical periodic-table idea.

If not, specify exactly what stronger periodic baseline is indispensable.

### B. Capacity fairness

Tree / graph models can be more flexible than a single circle.

Determine whether the current claim boundary handles this correctly.

A tree win alone is **not** sufficient evidence that language is tree-shaped.
Assess whether the direct circularity failures, low-rank comparisons, repeated split results, and cross-dataset replication make the narrower “simple circle not supported” conclusion defensible.

### C. Leakage and dependence

Assess:

- top-level-family hold-out;
- geographic block hold-out;
- matched-size geographic calibration;
- TLI vs GBI curation replication;
- WALS external sanity replication.

Decide whether a full phylogenetic / spatiophylogenetic model is **mandatory before publication**, merely desirable, or unnecessary for the bounded claim.

### D. Statistics

Assess:

- repeated-split summaries;
- bootstrap CI over split-level contrasts;
- number of splits;
- feature-selection rules;
- multiple exploratory stages;
- whether confirmatory language is warranted.

State what uncertainty analysis must appear in the manuscript.

### E. Contradictory geography result

Preserve this contradiction:

- TLI / GBI: weak cross-area transfer;
- WALS: much stronger cross-Macroarea transfer.

The manuscript must not convert this into a universal geography claim.

---

## 5. Required reviewer questions

Answer every item explicitly.

1. **Novelty collision:** Is there prior work that already performs essentially the same predictive test?
2. **Faithfulness:** Is the tested circle a fair operationalization of the simple global periodic hypothesis?
3. **Capacity:** Is the claim boundary sufficiently cautious about tree/model flexibility?
4. **Validation:** Are family / geography / curation / WALS checks enough for the bounded paper claim?
5. **Statistics:** What analyses are adequate, inadequate, or still required?
6. **Data dependence:** How should the WALS-vs-TLI/GBI geography contradiction affect framing?
7. **Publication value:** Is constraining/falsifying the periodic-table hypothesis scientifically useful given Baker / Port / Grambank?
8. **Decision:** `PASS`, `REVISE`, or `STOP`.
9. **Mandatory changes:** List only changes required before promotion/submission, separated from optional improvements.
10. **Claim rewrite:** Provide the strongest manuscript claim you would personally permit.

---

## 6. Decision rules

### PASS

Use only if all are true:

- no fatal prior-art collision;
- the simple-global-circle test is judged sufficiently faithful;
- the bounded negative/mixed claim is supported;
- remaining weaknesses can be handled in normal manuscript limitations;
- no additional analysis is mandatory before promotion to formal Paper 002.

### REVISE

Use if the core contribution is still viable but one or more **mandatory** repairs are needed.

A `REVISE` verdict does **not** authorize creation of formal `papers/002-*` yet.

### STOP

Use if any is true:

- fatal prior-art collision;
- periodic operationalization is fundamentally invalid for the bounded conclusion;
- irreparable leakage/design flaw;
- after proper claim narrowing, the contribution collapses to already-known results;
- the question is not sufficiently informative for a standalone paper.

---

## 7. Required receipt to write back

When review is complete, create:

`ideas/language-periodic-system/refine-logs/SECONDARY_REVIEW_RECEIPT.md`

Use this top-level structure:

```markdown
# ARIS Secondary Review Receipt

## Reviewer identity
- provider/app:
- exact model:
- model family:
- independent from primary executor: YES / NO
- fresh thread/session: YES / NO
- trace/session ID:
- timestamp:
- literature search cutoff:

## Verdict
PASS / REVISE / STOP / NON_INDEPENDENT_ADVISORY

## Executive rationale
...

## 1. Novelty collision
...

## 2. Faithfulness of periodic operationalization
...

## 3. Model-capacity fairness
...

## 4. Validation and dependence
...

## 5. Statistical adequacy
...

## 6. Dataset/representation contradiction
...

## 7. Publication value
...

## 8. Mandatory changes before promotion
1. ...
2. ...

## Optional improvements
- ...

## Permitted manuscript claim
> ...

## Prohibited / unsupported claims
- ...

## Promotion authorization
AUTHORIZED / NOT_AUTHORIZED

## Evidence inspected
- file/path
- DOI / paper / source
...

## Reviewer integrity statement
I independently reviewed the candidate rather than merely endorsing the primary executor's summary.
```

### Receipt integrity rules

- Do not overwrite `SECONDARY_REVIEW_PACKET.md`.
- Do not edit old stage result JSON merely to make the verdict cleaner.
- If you find a computational error, document it and create a separate correction commit or requested-action item.
- A receipt with `independent from primary executor: NO` cannot satisfy the formal ARIS gate.
- A receipt without model-family identity and timestamp cannot satisfy the formal ARIS gate.
- A `PASS` receipt must have `Promotion authorization: AUTHORIZED`.
- `REVISE` and `STOP` must use `NOT_AUTHORIZED`.

---

## 8. Optional machine-readable companion

If convenient, also create:

`ideas/language-periodic-system/refine-logs/SECONDARY_REVIEW_RECEIPT.json`

A template already exists at:

`ideas/language-periodic-system/refine-logs/SECONDARY_REVIEW_RECEIPT.template.json`

---

## 9. What happens after you finish

### If PASS

Do **not** silently create the formal paper directory unless your WorkBuddy task explicitly includes promotion.

Instead:

1. write the receipt;
2. commit it to `main`;
3. hand control back to the ARIS4C integrator.

The integrator will:

- verify reviewer independence;
- update `ARIS_STATUS.md`;
- convert reserved review slot **002** into the formal `papers/002-<slug>/`;
- freeze the reviewed proposal;
- begin manuscript-generation and reviewer loops.

### If REVISE

Keep slot 002 reserved but unpromoted, write the receipt, and make required repairs testable.

### If STOP

Release/close the reserved review slot according to the integrator's numbering policy; do not create a formal Paper 002 directory.

---

## 10. Short prompt for WorkBuddy

> Review **ARIS4C review slot 002**. There is intentionally no formal `papers/002-*` directory yet. Start at `papers/002-REVIEW-CANDIDATE.md`, which points to `ideas/language-periodic-system/`. Then read `ideas/language-periodic-system/refine-logs/WORKBUDDY_HANDOFF.md` and follow it exactly. You are the independent secondary reviewer and must be from a different model family than the OpenAI GPT primary executor to certify the gate. Independently verify prior art and methods, return PASS/REVISE/STOP, and write `SECONDARY_REVIEW_RECEIPT.md`. Do not say “002 is missing”: 002 is currently a reserved review slot, not a promoted paper.
