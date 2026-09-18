# ARIS4C003 STATUS

**Canonical state:** `DESIGN_LOCKED / OUTCOME_LOCKED`  
**Updated:** 2026-09-18  
**Contemporary confirmatory outcomes opened:** **NO**

This file is the operational resume point for ARIS4C003. Historical exposure
data and schema-only metadata checks are allowed before outcome unlock;
country×discipline contemporary results are not.

## Closed gates

- [x] ARIS provenance frozen: v0.4.26 / `951654847b015585385b2448c5667dcd04e7b56b`.
- [x] 21 confirmatory concepts frozen as D01–D21.
- [x] Primary OpenAlex discipline crosswalk frozen.
- [x] IKES 11-dimension rubric frozen.
- [x] Coder A completed before modern outcome inspection.
- [x] Fresh-context Coder B packet frozen.
- [x] Coder-B raw-response ingestion validates matrix, D01–D21 evidence
      sections, confidence labels, and independence declaration.
- [x] IKES freeze provenance hashes Coder A/B, Coder B raw response/evidence
      notes, adjudication, and final frozen matrix; hard gate re-verifies hashes.
- [x] Unflagged IKES cells are immutable A/B means; only missing or
      abs-difference >=2 cells may be adjudicated.
- [x] COLDAT historical exposure pipeline audited.
- [x] COLDAT current-state country universe: 159/159 resolved.
- [x] COLDAT original-vs-OWID imperial-intensity cross-check: max relative
      difference 0.
- [x] CEPII Gravity V202211 audited: 12,561 complete unordered pairs and
      156 `col_dep_ever=1` ties.
- [x] OpenAlex public-S3 Works schema probe PASS without outcome aggregation.
- [x] Official OpenAlex Works Parquet manifest pinned (2026-06-26 snapshot
      manifest; 510,372,821 Works; SHA-256 verified against source ledger).
- [x] OpenAlex materializers support local Parquet or anonymous public S3.
- [x] Country and dyad fractional-counting rules frozen.
- [x] Primary mature period 2019–2022 frozen.
- [x] PPML/HDFE estimator and clustering frozen.
- [x] 999 IKES-label permutations and 21 leave-one-discipline-out diagnostics
      frozen.
- [x] Period-specific secondary persistence profiles frozen in Amendment 003.
- [x] Small-N imperial-center corroboration protocol frozen.
- [x] Pre-outcome synthetic CI covers data builders, Coder-B ingestion/freeze,
      PPML engine, and design gate.
- [x] Novelty claim narrowed: not “colonialism affects science,” but the
      cross-disciplinary historical exposure × independently coded field
      entanglement gradient.

## Coder B attempt history

### Attempt 1 status — preserved but not confirmatory

WorkBuddy completed a full second coding pass and explicitly stated that it did
not view Coder A scores or contemporary confirmatory outcomes. However, the same
context also stated that it briefly opened the paper-root `STATUS.md` and
`README.md` during task triage.

That violates the pre-existing whitelist-only blind-bundle rule. Therefore:

- the raw response remains preserved at
  `process/gptpage/2026-09-18_ikes-coder-b-raw.md`;
- its parsed scores are preserved at
  `process/IKES_CODER_B_ATTEMPT1_CONTAMINATED.csv`;
- its diagnostic agreement is documented in
  `process/IKES_CODER_B_ATTEMPT1_ASSESSMENT.md`;
- it is **not** promoted to canonical `IKES_CODER_B.csv`;
- it cannot unlock contemporary outcomes.

Attempt 1 nevertheless showed useful non-confirmatory stability: mean absolute
cell difference 0.442, IKES-mean ICC(2,1) 0.754, and 8/231 cells at the frozen
abs-difference >=2 adjudication threshold.

The retry contract now requires two independent machine-checked declarations:

- `BUNDLE_ACCESS_STATUS: PASS`
- `INDEPENDENCE_STATUS: PASS`

## Remaining integrity gate

The only irreducible pre-outcome step is a **fresh confirmatory Coder B retry**
in a new WorkBuddy/GPTPage/model context that has not seen:

- Coder A scores;
- contemporary country×discipline outcomes;
- confirmatory ranking/bibliometric results.

Preferred WorkBuddy route:

`process/coder_b_blind/WORKBUDDY_HANDOFF.md`

Allow WorkBuddy to read only the files whitelisted in:

`process/coder_b_blind/MANIFEST.json`

Do **not** give it the paper root or parent `process/` directory. The blind
bundle is pinned by Git blob SHA and validated in pre-outcome CI.

The older `process/IKES_CODER_B_PACKET.md` remains the canonical full protocol,
but WorkBuddy should receive the isolated blind-bundle copy rather than browse
the surrounding repository.

Save the untouched response under:

`process/gptpage/<date>_ikes-coder-b-raw.md`

Then execute:

```bash
python code/ingest_coder_b.py \
  process/gptpage/<date>_ikes-coder-b-raw.md \
  --output-csv process/IKES_CODER_B.csv \
  --output-notes process/IKES_CODER_B.md

python code/adjudicate_ikes.py \
  process/IKES_CODER_A.csv \
  process/IKES_CODER_B.csv \
  --output-dir process/ikes_adjudication
```

Resolve only the automatically flagged missing / abs-difference >=2 cells
against historical evidence, then:

```bash
python code/freeze_ikes.py \
  process/ikes_adjudication/IKES_DISAGREEMENTS.csv \
  --output process/IKES_FROZEN.csv \
  --provenance process/IKES_FROZEN.provenance.json \
  --coder-a process/IKES_CODER_A.csv \
  --coder-b process/IKES_CODER_B.csv \
  --coder-b-notes process/IKES_CODER_B.md \
  --coder-b-raw process/gptpage/<date>_ikes-coder-b-raw.md
```

## Unlock sequence after Coder B

Do not reorder these steps.

1. `python code/preoutcome_gate.py --strict`
2. Materialize OpenAlex country cells.
3. Materialize OpenAlex dyad-positive cells.
4. Build complete country×discipline and pair×discipline panels with explicit
   eligible zeros.
5. Run `run_confirmatory_models.py`.
6. Run `run_imperial_corroboration.py`.
7. Inspect the three headline 2019–2022 estimates **for the first time** along
   with permutation/LOO diagnostics.
8. Interpret the full prespecified temporal profile.
9. Only then proceed to secondary ranking/prestige and broad exploratory
   all-field layers.

## Headline family

Exactly three confirmatory gradient coefficients:

1. former-colony fractional output: Exposure × IKES;
2. former-colony Top-10% impact rate: Exposure × IKES;
3. former-colonial-tie collaboration: ColonialTie × IKES.

No ranking result, earlier/later period, colonizer stratum, or exploratory field
may replace a null/inconvenient headline result.

## Secondary source roles

- Leiden Open Edition: open processing/indicator robustness, but shares
  OpenAlex as the bibliographic source.
- QS Subject: prestige-heavy secondary layer.
- THE Subject: broad composite secondary layer.
- Shanghai GRAS: research-oriented external-source ranking contrast using
  WoS/InCites components.

These sources cannot be used to “rescue” the primary outcome family.

## Resume rule

If a future chat resumes ARIS4C003, read this file, `MODEL_SPEC_LOCK.json`,
the three preregistration amendments, and `preoutcome_gate.py` before changing
the design. Never infer that Coder B or outcome unlock happened merely because
time has passed.
