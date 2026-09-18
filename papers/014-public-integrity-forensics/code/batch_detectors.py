"""Cross-contract and cross-bidder detectors for OpenIntegrity Pilot 0.

These detectors operate on small normalized observations instead of a single
IntegrityCase. Their outputs are still review leads, not corruption labels.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from typing import Iterable, Optional

from open_integrity_agent import EvidenceClass, SourceRef, Status


@dataclass(frozen=True)
class AwardObservation:
    contract_id: str
    authority_id: str
    supplier_id: str
    award_date: date
    amount: float
    threshold: Optional[float] = None
    procurement_key: Optional[str] = None
    source_ref: Optional[SourceRef] = None


@dataclass(frozen=True)
class BidderObservation:
    contract_id: str
    bidder_id: str
    address: Optional[str] = None
    stable_ids: tuple[str, ...] = ()
    source_ref: Optional[SourceRef] = None


@dataclass
class BatchFinding:
    detector_id: str
    family: str
    status: Status
    evidence_class: EvidenceClass
    claim: str
    evidence: dict = field(default_factory=dict)
    dependency_group: str = ""
    benign_explanations: list[str] = field(default_factory=list)
    corruption_inference: bool = False

    def __post_init__(self) -> None:
        self.corruption_inference = False


class SplitAwardDetector:
    detector_id = "split_awards_near_threshold"
    family = "value_threshold"

    def __init__(self, window_days: int = 30, near_fraction: float = 0.8) -> None:
        self.window_days = window_days
        self.near_fraction = near_fraction

    def run(self, awards: Iterable[AwardObservation]) -> list[BatchFinding]:
        rows = list(awards)
        groups: dict[tuple[str, str, str], list[AwardObservation]] = {}
        for a in rows:
            if a.threshold is None or a.threshold <= 0 or not a.procurement_key:
                continue
            key = (a.authority_id, a.supplier_id, a.procurement_key)
            groups.setdefault(key, []).append(a)

        findings: list[BatchFinding] = []
        for key, group in groups.items():
            group = sorted(group, key=lambda x: x.award_date)
            for start in range(len(group)):
                window = [group[start]]
                for candidate in group[start + 1 :]:
                    if (candidate.award_date - group[start].award_date).days <= self.window_days:
                        window.append(candidate)
                    else:
                        break
                if len(window) < 2:
                    continue
                threshold = window[0].threshold
                if threshold is None:
                    continue
                if any(x.threshold != threshold for x in window):
                    continue
                individually_below = all(x.amount < threshold for x in window)
                individually_near = all(x.amount >= threshold * self.near_fraction for x in window)
                combined = sum(x.amount for x in window)
                if individually_below and individually_near and combined >= threshold:
                    findings.append(
                        BatchFinding(
                            detector_id=self.detector_id,
                            family=self.family,
                            status=Status.FLAG,
                            evidence_class=EvidenceClass.E1,
                            claim="Multiple comparable awards fall below the same configured threshold while their combined value exceeds it.",
                            evidence={
                                "authority_id": key[0],
                                "supplier_id": key[1],
                                "procurement_key": key[2],
                                "contract_ids": [x.contract_id for x in window],
                                "amounts": [x.amount for x in window],
                                "threshold": threshold,
                                "combined_value": combined,
                                "window_days": self.window_days,
                            },
                            dependency_group=f"split:{key[0]}:{key[1]}:{key[2]}",
                            benign_explanations=[
                                "The awards may represent genuinely separate needs or budgets.",
                                "The configured threshold may not apply to aggregation in this jurisdiction or procurement type.",
                            ],
                        )
                    )
                    break
        return findings


class SupplierConcentrationDetector:
    detector_id = "supplier_concentration"
    family = "supplier_concentration"

    def __init__(self, min_awards: int = 5, share_threshold: float = 0.8) -> None:
        self.min_awards = min_awards
        self.share_threshold = share_threshold

    def run(self, awards: Iterable[AwardObservation]) -> list[BatchFinding]:
        by_authority: dict[str, list[AwardObservation]] = {}
        for a in awards:
            by_authority.setdefault(a.authority_id, []).append(a)

        out: list[BatchFinding] = []
        for authority, rows in by_authority.items():
            if len(rows) < self.min_awards:
                continue
            counts: dict[str, int] = {}
            values: dict[str, float] = {}
            for row in rows:
                counts[row.supplier_id] = counts.get(row.supplier_id, 0) + 1
                values[row.supplier_id] = values.get(row.supplier_id, 0.0) + row.amount
            top_supplier = max(counts, key=counts.get)
            count_share = counts[top_supplier] / len(rows)
            total_value = sum(x.amount for x in rows)
            value_share = values[top_supplier] / total_value if total_value > 0 else 0.0
            if count_share >= self.share_threshold or value_share >= self.share_threshold:
                out.append(
                    BatchFinding(
                        detector_id=self.detector_id,
                        family=self.family,
                        status=Status.FLAG,
                        evidence_class=EvidenceClass.E4,
                        claim="One supplier accounts for an unusually large share under the configured concentration rule.",
                        evidence={
                            "authority_id": authority,
                            "award_count": len(rows),
                            "top_supplier": top_supplier,
                            "count_share": count_share,
                            "value_share": value_share,
                            "configured_share_threshold": self.share_threshold,
                        },
                        dependency_group=f"concentration:{authority}",
                        benign_explanations=[
                            "A specialized market can legitimately have one dominant supplier.",
                            "Framework agreements or centralized purchasing can produce high concentration.",
                            "A real deployment must calibrate this rule by sector, value band, and procurement method.",
                        ],
                    )
                )
        return out


def _norm_address(value: Optional[str]) -> str:
    if not value:
        return ""
    import re
    text = re.sub(r"[^a-z0-9]+", " ", value.lower()).strip()
    return re.sub(r"\s+", " ", text)


class SharedAddressBidderDetector:
    detector_id = "shared_address_bidders"
    family = "corporate_ownership"

    def run(self, bidders: Iterable[BidderObservation]) -> list[BatchFinding]:
        by_contract: dict[str, list[BidderObservation]] = {}
        for b in bidders:
            by_contract.setdefault(b.contract_id, []).append(b)

        out: list[BatchFinding] = []
        for contract_id, rows in by_contract.items():
            address_groups: dict[str, list[BidderObservation]] = {}
            for row in rows:
                addr = _norm_address(row.address)
                if addr:
                    address_groups.setdefault(addr, []).append(row)
            for addr, group in address_groups.items():
                unique_bidders = {x.bidder_id for x in group}
                if len(unique_bidders) < 2:
                    continue
                out.append(
                    BatchFinding(
                        detector_id=self.detector_id,
                        family=self.family,
                        status=Status.FLAG,
                        evidence_class=EvidenceClass.E0,
                        claim="Two or more nominally distinct bidders share the same normalized public address.",
                        evidence={
                            "contract_id": contract_id,
                            "normalized_address": addr,
                            "bidder_ids": sorted(unique_bidders),
                        },
                        dependency_group=f"shared_address:{contract_id}:{addr}",
                        benign_explanations=[
                            "Different companies can legitimately share an accountant, registered office, incubator, or group address.",
                            "Address reuse alone does not establish common control or bid coordination.",
                        ],
                    )
                )
        return out
