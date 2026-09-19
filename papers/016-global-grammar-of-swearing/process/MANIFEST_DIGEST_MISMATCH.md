# ARIS4C016 Frozen-Manifest Digest Mismatch

Recorded: 2026-09-19
Status of this item: **tooling / record defect. It is not a research finding about
swearing, and it is not coder disagreement.** No lexical item, translation, or
private coding-sheet content appears in this document.

## What the freeze claims

`process/AUDIT_SAMPLE_FREEZE.md` freezes the 300-row ontology audit sample used for
the independent Coder A/B reliability gate, and declares the SHA-256 of the public
manifest (`sample,row_index,row_hash,stratum`) to be the *canonical sample
identity*:

```
48c58f91901e8c2a1aab01958e95ea28afaf0f33e7a98677f98e58b8a412c9b4
```

`code/export_private_coding_sheet.py:24` and `code/score_coder_reliability.py:27`
both hard-code that value and **fail closed** when the regenerated manifest does
not match. So the whole Coder A/B chain is gated on reproducing one digest.

## What was executed on 2026-09-19

1. Regenerated the sample with the committed sampler at this commit
   (`code/build_audit_sample.py`, HEAD `a1131fea`, unmodified in the working tree,
   `core.autocrlf=false`).
2. The sampler verified the OSF source digest
   `c725a30913e604e8344f4990c8d63990dcf0271e3a65765ddc3fa591b8cb1387` on every run.
3. Two independent fresh runs against OSF produced byte-identical row sets:

   ```
   manifest SHA-256 = 910a47c353a7ebbe0ccbe48c0001fea536c9f24e9cb6242dcec46d9e3e541751
   ```

4. The aggregate structure of that sample **matches the freeze document exactly**:

   - 300 rows, 18 communities;
   - 16 communities × 15 rows, Setswana (BW) × 30, Spanish (ES) × 30;
   - strata: missing-primary 42, unresolved 116, multi-label 61, random 81.

5. 86 alternative serialisations were tested (row orderings, column subsets,
   header spellings, `LF`/`CRLF`, trailing newline, BOM, and the freeze document's
   hyphenated stratum labels). **None reproduces `48c58f91…`.**
   Details: `data/manifest_digest_diagnosis.json`, reproducible with
   `code/verify_frozen_manifest.py`.

## Why this is a record defect rather than a broken checkout

The regenerated sample has the frozen size, the frozen per-community allocation,
and the frozen per-stratum counts, and the sampler is deterministic and unmodified.
A wrong checkout, a line-ending normalisation, or a changed source file would not
preserve all three count vectors simultaneously. The most economical
explanations are:

- **A:** the frozen digest was computed by an ad-hoc script or manual step whose
  exact serialisation is not in the repository, and that step is now unrecoverable;
- **B:** the digest was computed against a sampler revision that was never
  committed (the freeze is dated one day after the only sampler commit);
- **C:** the digest was computed over a *different 300-row draw* that happens to
  share the same allocation and stratum totals — plausible because those totals are
  fixed by the design, not by the draw, so this cannot be ruled out from the
  aggregate counts alone.

There is no way to discriminate A/B/C from the repository, because the original
manifest rows were never committed: only the digest survives
(`AUDIT_SAMPLE_FREEZE.md:73`, restated in `HANDOFF.md:127`, `STATUS.md:57`,
`CODER_HANDOFF.md:172`, `DELETE_SAFE_CHECKPOINT.md:20`).

## Consequences

- The private coder sheet cannot be exported, and reliability cannot be scored,
  without either reproducing the frozen digest or superseding it.
- Coding must **not** start on the regenerated 300 rows: if the frozen sample is
  real and different, that would silently swap the prespecified sample and destroy
  the anti-cherry-picking guarantee that `AUDIT_SAMPLE_FREEZE.md` exists to provide.
- This does not affect any already-collected 016 evidence (Phase-0 audits,
  repeated-item controls, G2P technical coverage).

## Decision requested from the maintainer / reviewing AI

Choose exactly one, and record it in `DECISIONS.md` before any coder is briefed:

1. **Recover** the artifact that produced `48c58f91…` (an uncommitted freeze script,
   a local copy of the manifest, or the private sheet generated on 2026-09-19).
   `data/manifest_digest_diagnosis.json` publishes partial digests —
   whole-column, row-hash-only, `(row_index,row_hash)` pairs, canonical JSON, and
   one digest per community — so a holder of the original file can identify the
   serialisation and the diverging community without leaking lexical content.
   If it is recovered, verify it and keep `48c58f91…` as canonical.
2. **Supersede** the freeze: cut a new, versioned sample
   (`manifest_version: v0.1`, digest `910a47c3…`) from the committed sampler *while
   no coder has yet seen any item*, append a superseding section to
   `AUDIT_SAMPLE_FREEZE.md` that keeps the old digest and states why it is retired,
   and update the two constants in
   `code/export_private_coding_sheet.py` and `code/score_coder_reliability.py`
   together. This is explicitly allowed by the freeze's own rule that any
   replacement "must use the same deterministic sampler and receive a new
   manifest version/hash".
3. **Narrow** the gate (e.g. drop the manifest digest from the independence test and
   key it to the sampler commit + source digest instead). Not recommended: it
   weakens the only prespecification check this gate has.

Option 2 is the fallback if nothing turns up; it must still be an explicit,
recorded decision rather than a silent re-freeze, because the retired digest is
currently cited as canonical in five documents.

## Reproduce locally

```bash
python papers/016-global-grammar-of-swearing/code/verify_frozen_manifest.py
# or offline against a captured payload:
python papers/016-global-grammar-of-swearing/code/verify_frozen_manifest.py \
  --cached-payload <audit_sample.json> --out manifest_digest_diagnosis.json
```
