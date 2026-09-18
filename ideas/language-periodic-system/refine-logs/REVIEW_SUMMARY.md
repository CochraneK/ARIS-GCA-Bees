# Review Summary · Language Periodic System

**Formal secondary reviewer:** `PENDING`  
**Current state:** confirmatory evidence package complete; review packet ready; **not** an ARIS reviewer receipt.

## What survived the primary + confirmatory stress tests

The project survives only in the narrow form of a predictive test of the historical periodic-table hypothesis.

The original broad novelty claims do **not** survive prior-art review:

- Baker already proposed a periodic table of languages;
- Port/Marcolli already analyze topology, dimensionality, clustering, and loops in syntactic-parameter spaces;
- Grambank already studies global latent structure and strong genealogical constraints;
- typological feature prediction is already an established computational task.

The surviving wedge is the explicit operationalization of a simple global periodic/circular geometry as a model that can lose, followed by out-of-sample comparison and direct circularity tests.

## Earlier reviewer concerns and current status

1. **Periodic strawman risk — ADDRESSED.** Stage-1B directly optimizes one angular coordinate per feature rather than using spectral angles as the final representation.
2. **Disconnected spectral affinity — ADDRESSED.** Connected-affinity sensitivity is included.
3. **Capacity mismatch — PARTLY ADDRESSED / CLAIM-BOUNDED.** `MODEL_CAPACITY_NOTE.md` documents why tree > circle is not interpreted as proof of a universal tree geometry. Direct circularity tests make the negative periodic conclusion less dependent on competitor flexibility.
4. **Genealogical leakage — PARTLY ADDRESSED.** Repeated top-level-family hold-outs are included, with GBI/WALS qualitative replication. A full phylogenetic covariance model has not been fit.
5. **Areal leakage — ADDRESSED AS ROBUSTNESS, NOT CAUSAL MODEL.** TLI geography blocks and matched-size controls are included; WALS contradicts the strong geography result, so geographic collapse is not promoted as universal.
6. **Feature construction — CLAIM-BOUNDED.** TLI/GBI curation reduces dependencies but features are not treated as natural linguistic atoms.
7. **Outcome framing — ADDRESSED.** No decorative periodic table is produced. The result is explicitly negative/mixed for the simple global periodic hypothesis.
8. **Replication — ADDRESSED QUALITATIVELY.** GBI repeats the tree-over-circle ordering under alternative curation; WALS externally reproduces the same qualitative ordering despite very different sparsity/geographic behavior.

## Strongest current evidence

- Stage-1D: `CIRCULAR_ROBINSON_NOT_SUPPORTED`; 60-feature circular closure/internal-adjacency ratio ≈0.037.
- Stage-1F: tree beats optimized circular in 20/20 TLI family-held-out splits; paired mean +0.073, 95% bootstrap CI [0.055, 0.092].
- Stage-1H: GBI tree 0.122 vs circular 0.073; tree win fraction 1.00.
- Stage-1I: WALS tree 0.603 vs circular 0.410; tree win fraction 1.00.

## Important non-result / contradiction

TLI and GBI show weak transfer of the association structure across large geographic regions, but WALS shows strong Macroarea transfer. Therefore geography is a secondary, representation-dependent finding and cannot be the paper's central novelty.

## Current bounded conclusion

> **The simple global circular form of the language periodic-table hypothesis is not supported by held-out predictive or direct circularity evidence. Hierarchical/non-circular models provide stronger family-held-out predictive benchmarks across TLI, GBI, and WALS, without proving a universal tree geometry.**

## Formal ARIS gate

The upstream ARIS contract still requires an actual identity-bearing secondary reviewer verdict/trace.

Current status:

- novelty-check primary evidence: complete;
- research-review primary/confirmatory stress test: complete;
- secondary-review packet: complete (`SECONDARY_REVIEW_PACKET.md`);
- formal secondary review: **PENDING**;
- final reviewer-bearing evidence gate: **NOT PASS YET**.

No model identity, trace ID, reviewer verdict, or acceptance status is fabricated.

## Next legal transition

A secondary reviewer should inspect `SECONDARY_REVIEW_PACKET.md` and return `PASS / REVISE / STOP` with an identity-bearing receipt.

- `PASS` → promote to next Paper ID and start manuscript-generation / reviewer loops.
- `REVISE` → implement only the reviewer-mandated changes, rerun affected analyses, then resubmit to the secondary gate.
- `STOP` → park/reframe without consuming a paper number.
