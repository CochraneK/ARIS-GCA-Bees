# Evidence model

## Principle

OpenIntegrity stores **observations, source facts, identity hypotheses, constraints, temporal relationships, and review leads**. It does not store an automated conclusion that a person or organization is corrupt.

## Evidence classes

### E0 — direct metadata / process observation
Examples:
- one bid was recorded;
- award used a non-open procedure;
- supplier was incorporated 20 days before award;
- the award amount is within 1% below a configured legal threshold;
- beneficial-ownership data are absent.

E0 can be useful as a red flag but is not evidence of corruption.

### E1 — deterministic incompatibility or rule-conditioned anomaly
Examples:
- dates are impossible under the published timeline;
- component awards deterministically exceed/contradict a reported aggregate;
- multiple awards to the same supplier deterministically partition a requirement around a configured threshold, when the legal/configuration assumptions are satisfied.

E1 establishes the computational fact, not unlawful intent.

### E2 — externally verifiable official/public-record fact
Examples:
- a stable-ID match to an official debarment that was in force on the award date;
- an official registry records person X as beneficial owner of company Y during the relevant period;
- an official declaration records a stated interest;
- an official audit/enforcement decision exists.

E2 must preserve source, date, and scope.

### E3 — high-specificity cross-source forensic match
Examples:
- supposedly independent bidders share a verified director/address/contact plus coordinated bidding patterns;
- an exact corporate identifier links bidder and declared interest through an ownership chain;
- a high-specificity historical ownership path joins a decision-maker to a supplier at the relevant time.

E3 requires entity-resolution provenance and benign alternatives.

### E4 — model-derived or peer-distribution anomaly
Examples:
- unusually high supplier concentration after conditioning on agency/sector/value;
- graph community anomaly;
- learned bid-rigging similarity score;
- price outlier model.

E4 must report calibration/reference population.

### E5 — weak/context-dependent heuristic
Examples:
- Benford deviation without strong generative assumptions;
- excessive round numbers;
- generic name-similarity match;
- stylometric/document oddity without corroboration.

E5 alone can never create high review priority.

Evidence classes are **not guilt levels**.

## Finding contract

Every detector must emit:

```json
{
  "finding_id": "...",
  "subject_id": "...",
  "detector_id": "...",
  "detector_version": "...",
  "family": "...",
  "applicable": true,
  "applicability_reason": "...",
  "status": "FLAG | PASS | ABSTAIN | ERROR",
  "evidence_class": "E0 | E1 | E2 | E3 | E4 | E5",
  "claim": "...",
  "evidence": {},
  "source_refs": [],
  "dependency_group": "...",
  "observed_at": null,
  "reproducible": "yes | no | unknown",
  "confidence": null,
  "calibration_reference": null,
  "benign_explanations": [],
  "corruption_inference": false
}
```

PASS means the detector was applicable and did not flag.
ABSTAIN means the required assumptions/data/identity resolution were insufficient.
ERROR means the detector should have been applicable but execution failed.

## Evidence graph

Node types:
- contract;
- tender;
- lot;
- authority;
- supplier;
- legal entity;
- natural person;
- beneficial owner;
- officer;
- public office;
- office occupancy;
- address;
- sanction/debarment;
- disclosure;
- donation/lobbying record;
- offshore entity;
- document;
- source record;
- detector finding.

Important edges:
- AWARDED_TO;
- BID_FOR;
- OWNS;
- CONTROLS;
- OFFICER_OF;
- OCCUPIED_PUBLIC_OFFICE;
- SHARES_ADDRESS_WITH;
- SANCTIONED_OR_DEBARRED;
- DECLARED_INTEREST_IN;
- DONATED_TO;
- LOBBIED;
- RELATED_TO;
- SAME_ENTITY_AS;
- POSSIBLE_MATCH;
- DERIVED_FROM;
- CORROBORATES;
- CONTRADICTS;
- DEPENDS_ON.

## Independence

Multiple findings derived from the same underlying datum are not independent evidence.

Examples:
- "single bidder" and an LLM summary saying "competition was low" are one dependency group;
- OpenSanctions and a downstream dataset copied from OpenSanctions are not independent;
- two name-matching algorithms identifying the same ambiguous person are not independent;
- a graph feature derived from a PSC ownership edge and a detector directly flagging that same PSC edge share evidence.

## Temporal integrity

Every source-side fact should distinguish, where possible:

- `valid_from` / `valid_to`: when the real-world relation was true;
- `published_at`: when the information became public;
- `retrieved_at`: when OpenIntegrity obtained the record.

Track A may only use facts whose public availability precedes the cutoff.

## Review priority

Transparent Pilot rules:

- HIGH: at least two independent families with E2/E3 support, or an E1 deterministic issue plus independent E2/E3 corroboration;
- MODERATE: one E2/E3 finding, multiple independent E0/E1/E4 findings, or a calibrated high-yield model anomaly;
- LOW: isolated E0/E4;
- VERY LOW: E5-only evidence;
- ABSTAIN: insufficient source/identity/temporal validity.

HIGH means "review first", not "probably corrupt".

## Human-facing verification packet

Every surfaced lead should answer:

1. What exactly triggered?
2. Which source records support it?
3. Were those records public at the relevant time?
4. How were the entities resolved?
5. Can the computation be reproduced?
6. Which evidence is independent?
7. What benign explanations remain?
8. What additional public record should a reviewer inspect next?
