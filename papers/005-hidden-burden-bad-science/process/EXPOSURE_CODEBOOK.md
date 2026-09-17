# EXPOSURE CODEBOOK — ARIS4C005

## Why one binary “fraud” variable is not enough

Retraction Watch reasons mix at least four different concepts:

1. evidence of **intentional misconduct**;
2. evidence that the **scientific claims/data are unreliable**;
3. failure of the **publication process** (authorship, peer review, policy, duplication, etc.);
4. **honest/unattributed error**.

These axes overlap but are not equivalent.

A plagiarized paper may contain scientifically correct results while violating research integrity. An honest analytical error may make the scientific conclusion unreliable without misconduct. A paper-mill article may implicate both scientific reliability and publication-process integrity.

Therefore the project never maps all retractions into one “fake paper” bucket.

---

# 1. Event-level variables

For every correction/retraction event derive:

- `notice_nature`: retraction / expression of concern / correction / removal / other;
- `rw_reasons_raw`: original multi-label Retraction Watch reasons;
- `explicit_intent`: yes / no / unclear;
- `author_attributed`: yes / no / unclear;
- `scientific_reliability_materially_compromised`: yes / no / unclear;
- `publication_process_compromised`: yes / no / unclear;
- `misconduct_explicit`: yes / no / unclear;
- `organized_fraud_signal`: yes / no / unclear;
- `honest_error_signal`: yes / no / unclear;
- `evidence_strength`: formal finding / explicit notice / database coding / inference only;
- `manual_review_required`: yes / no.

The raw reasons are always retained so mappings can be reproduced under alternative definitions.

---

# 2. Confirmatory exposure families

## E1-S — confirmed severe scientific unreliability with integrity evidence

This is the narrow primary exposure for contamination/opportunity-cost analyses.

### Strong direct reasons

Default high-specificity mapping when the Retraction Watch record/notice supports the reason:

- `Falsification/Fabrication of Data`
- `Falsification/Fabrication of Image`
- `Falsification/Fabrication of Results`
- `Paper Mill` **when the article's research content is judged unreliable**
- explicit formal misconduct finding tied to unreliable data/results
- `Manipulation of Data/Images/Results` only when accompanying evidence establishes deceptive/material scientific manipulation

### Requires manual/context review

- `Unreliable Data`
- `Unreliable Image`
- `Unreliable Results and/or Conclusions`
- `Original Data and/or Images not Provided and/or not Available`
- `Results Not Reproducible`
- `Concerns/Issues About Data/Image/Results and/or Conclusions`
- generic `Euphemisms for Misconduct`
- broad `Ethical Violations by Author`

These can indicate serious unreliability without identifying fabrication/falsification or intent.

---

## E1-M — confirmed misconduct / major research-integrity violation

Broader integrity exposure; useful for researcher/career/governance analyses.

Includes E1-S plus, where explicitly supported:

- plagiarism categories;
- false/forged authorship or affiliation;
- fake/manipulated peer review;
- salami slicing / duplicate publication when intentional and materially abusive;
- ethical violations by author;
- lack of IRB/IACUC approval/compliance;
- informed/patient consent violations;
- taken-via-peer-review theft;
- organized authorship/citation/publication fraud.

### Key boundary

`E1-M` is **not** used as the primary denominator for “false scientific findings,” because some misconduct types do not make the underlying result false.

---

## E1-P — publication-process integrity failure

Examples:

- fake/compromised peer review;
- rogue editor;
- false/forged authorship or affiliation;
- paper mill;
- third-party publication manipulation;
- citation/reference manipulation;
- intentional duplicate/salami publication;
- computer-generated/manufactured content where integrity is compromised.

E1-P may overlap E1-S and E1-M.

---

# 3. E3 — broader research waste / unreliability without a misconduct claim

Default examples when no stronger intentional evidence exists:

- `Error in Analyses`
- `Error in Data`
- `Error in Image`
- `Error in Materials`
- `Error in Methods`
- `Error in Results and/or Conclusions`
- `Error in Text`
- `Contamination of Cell Lines/Tissues`
- `Contamination of Materials`
- `Results Not Reproducible`
- `Unreliable Data/Image/Results` when intent is not established
- bias/balance problems without evidence of misconduct
- nonpublication/discontinuation in the trial extension
- journal/publisher errors.

Retraction Watch's glossary explicitly treats “error” as a mistake without intention to mislead, while fabrication/falsification definitions explicitly entail intention to mislead. This distinction is preserved.

---

# 4. Reasons that must never become misconduct automatically

The following are discovery/context labels and require more evidence:

- `Author Unresponsive`
- `Concerns/Issues about Article`
- `Concerns/Issues About Data`
- `Concerns/Issues About Image`
- `Concerns/Issues about Results and/or Conclusions`
- `Original Data and/or Images not Provided and/or not Available`
- `Investigation by ...`
- `Objections by ...`
- `Legal Reasons and/or Threats`
- `Conflict of Interest`
- `Notice – Unable to Access via current resources`
- `Breach of Policy by Author`
- generic `Ethical Violations by Author`

An investigation or concern is not itself a finding.

---

# 5. Duplication and plagiarism boundary

Retraction Watch's glossary notes that reasons containing “duplication” do **not** state or imply intentionality.

Therefore:

- duplication alone → no automatic misconduct label;
- plagiarism explicitly supported → E1-M;
- scientific-reliability consequence of plagiarism is coded separately;
- journal-caused duplicate publication → publication-system error, not author misconduct.

---

# 6. Paper mills

`Paper Mill` gets three separate flags:

- `paper_mill_explicit = 1`;
- `publication_process_compromised = 1`;
- `scientific_reliability_materially_compromised` determined from notice/evidence.

Reason: a paper-mill label is powerful evidence of organized publication fraud, but downstream scientific-harm analyses should still document whether the research content itself can be trusted.

---

# 7. AI/computer-generated content

Retraction Watch includes a `Computer-Aided Content or Computer-Generated Content` reason.

This reason alone does not prove scientific fabrication or misconduct. Code additional evidence:

- fabricated/hallucinated references;
- fabricated data/results;
- policy breach only;
- undisclosed assistance;
- scientifically valid but procedurally noncompliant content.

The project avoids treating “AI used” as synonymous with fraudulent science.

---

# 8. Narrow/broad sensitivity definitions

## `E1S_NARROW`

Explicit fabrication/falsification of data/image/results, or a formal misconduct finding that clearly makes substantive scientific results unreliable.

Highest specificity; lowest coverage.

## `E1S_BROAD`

`E1S_NARROW` plus explicitly unreliable results/data with strong integrity evidence, validated paper-mill scientific content, and adjudicated deceptive manipulation.

## `E1M_BROAD`

All confirmed major misconduct/process-integrity violations, including plagiarism/authorship/peer-review categories.

## `E3_UNRELIABLE`

Material scientific unreliability/waste without sufficient evidence for E1.

Every major result is rerun under relevant definitions.

---

# 9. Multi-label logic

One article may be:

```text
E1-S = 1
E1-M = 1
E1-P = 1
E3 = 0
```

or:

```text
E1-S = 0
E1-M = 1   # e.g. plagiarism
E1-P = 1
E3 = 0/1 depending on scientific reliability
```

or:

```text
E1-S = 0
E1-M = 0
E1-P = 0
E3 = 1     # e.g. major honest analysis error
```

This is intentional. The categories answer different research questions.

---

# 10. Manual adjudication priority

Highest priority for manual review:

- vague notices with `Unreliable ...` or `Concerns/Issues ...`;
- multiple reasons pointing in conflicting directions;
- bulk retractions;
- paper-mill labels without clear content evidence;
- EOC → retraction transitions;
- notices where publisher and Retraction Watch coding disagree;
- apparent honest-error language alongside an explicit misconduct finding.

---

# 11. Versioning

Retraction Watch reason definitions change over time. The codebook records the source guide version/retrieval date and preserves raw labels.

Initial reference date: **2026-09-18**.

Primary source: Retraction Watch Database User Guide, Appendix B (Reasons) and Appendix E (Glossary), with Crossref production access documentation.
