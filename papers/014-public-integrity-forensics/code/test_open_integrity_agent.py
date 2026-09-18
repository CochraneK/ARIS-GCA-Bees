from datetime import date

from open_integrity_agent import (
    ContractRecord,
    DebarmentRecord,
    EntityRecord,
    EvidenceClass,
    IntegrityCase,
    NearThresholdDetector,
    OpenIntegrityAgent,
    PublicOfficeOwnershipLinkDetector,
    RelationRecord,
    SingleBidderDetector,
    SourceRef,
    Status,
    review_priority,
)


SRC = SourceRef("synthetic", "r1")


def base_case(**contract_overrides):
    kwargs = dict(
        contract_id="c1",
        authority_id="a1",
        supplier_ids=("s1",),
        award_date=date(2026, 1, 10),
        award_value=99_000,
        legal_threshold=100_000,
        bid_count=1,
        source_refs=(SRC,),
    )
    kwargs.update(contract_overrides)
    return IntegrityCase(subject_id="case-1", contract=ContractRecord(**kwargs))


def test_single_bidder_flags_but_does_not_infer_corruption():
    finding = SingleBidderDetector().run(base_case())
    assert finding.status == Status.FLAG
    assert finding.evidence_class == EvidenceClass.E0
    assert finding.corruption_inference is False


def test_missing_bid_count_abstains_not_passes():
    finding = SingleBidderDetector().run(base_case(bid_count=None))
    assert finding.status == Status.ABSTAIN
    assert finding.applicable is False


def test_near_threshold_is_observation_not_guilt():
    finding = NearThresholdDetector(margin_fraction=0.02).run(base_case())
    assert finding.status == Status.FLAG
    assert finding.evidence_class == EvidenceClass.E0
    assert finding.corruption_inference is False


def test_name_only_office_owner_match_abstains():
    case = base_case()
    case.entities["p1"] = EntityRecord(
        entity_id="p1",
        name="Alex Example",
        entity_type="person",
        public_office_from=date(2025, 1, 1),
        public_office_to=date(2027, 1, 1),
    )
    case.relations.append(
        RelationRecord(
            left_id="p1",
            relation="BENEFICIAL_OWNER_OF",
            right_id="s1",
            source_ref=SRC,
            identity_strength="name_only",
        )
    )
    finding = PublicOfficeOwnershipLinkDetector().run(case)
    assert finding.status == Status.ABSTAIN
    assert finding.evidence_class == EvidenceClass.E5


def test_identity_resolved_office_owner_link_is_e2_fact():
    case = base_case()
    case.entities["p1"] = EntityRecord(
        entity_id="p1",
        name="Alex Example",
        entity_type="person",
        public_office_from=date(2025, 1, 1),
        public_office_to=date(2027, 1, 1),
    )
    case.relations.append(
        RelationRecord(
            left_id="p1",
            relation="BENEFICIAL_OWNER_OF",
            right_id="s1",
            source_ref=SRC,
            identity_strength="stable_id",
            valid_from=date(2025, 1, 1),
        )
    )
    finding = PublicOfficeOwnershipLinkDetector().run(case)
    assert finding.status == Status.FLAG
    assert finding.evidence_class == EvidenceClass.E2
    assert finding.corruption_inference is False


def test_future_debarment_is_not_backfilled_to_award():
    case = base_case()
    case.debarments.append(
        DebarmentRecord(
            entity_id="s1",
            imposed_from=date(2026, 2, 1),
            imposed_to=None,
            source_ref=SRC,
        )
    )
    result = OpenIntegrityAgent().run(case)
    debarment = next(f for f in result["findings"] if f["detector_id"] == "in_force_debarment")
    assert debarment["status"] == "PASS"


def test_in_force_debarment_flags_external_fact():
    case = base_case()
    case.debarments.append(
        DebarmentRecord(
            entity_id="s1",
            imposed_from=date(2025, 2, 1),
            imposed_to=date(2026, 12, 31),
            source_ref=SRC,
        )
    )
    result = OpenIntegrityAgent().run(case)
    debarment = next(f for f in result["findings"] if f["detector_id"] == "in_force_debarment")
    assert debarment["status"] == "FLAG"
    assert debarment["evidence_class"] == "E2"
    assert result["corruption_inference"] is False


def test_e5_alone_can_never_be_high_priority():
    case = base_case()
    case.entities["p1"] = EntityRecord(
        entity_id="p1",
        name="Alex Example",
        entity_type="person",
        public_office_from=date(2025, 1, 1),
        public_office_to=date(2027, 1, 1),
    )
    case.relations.append(
        RelationRecord(
            left_id="p1",
            relation="OWNS",
            right_id="s1",
            source_ref=SRC,
            identity_strength="name_only",
        )
    )
    f = PublicOfficeOwnershipLinkDetector().run(case)
    # ABSTAIN is not even a flag; if an E5 flag is later introduced the priority
    # policy still forbids E5-only HIGH.
    assert review_priority([f]) != "HIGH"


def test_missing_debarment_coverage_abstains_instead_of_passing():
    from open_integrity_agent import InForceDebarmentDetector

    finding = InForceDebarmentDetector().run(base_case())
    assert finding.status == Status.ABSTAIN
    assert finding.applicable is False


def test_explicit_debarment_coverage_can_support_negative_pass():
    from open_integrity_agent import InForceDebarmentDetector

    case = base_case()
    case.source_coverage.add("debarment")
    finding = InForceDebarmentDetector().run(case)
    assert finding.status == Status.PASS
    assert finding.applicable is True


def test_missing_ownership_or_public_office_coverage_abstains():
    finding = PublicOfficeOwnershipLinkDetector().run(base_case())
    assert finding.status == Status.ABSTAIN
    assert finding.applicable is False
