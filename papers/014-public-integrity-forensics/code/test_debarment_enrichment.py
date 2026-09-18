from datetime import date

import pytest

from debarment_enrichment import (
    attach_debarment_to_supplier,
    mark_debarment_scan_complete,
    normalize_external_debarment,
)
from entity_resolution import IdentityProfile, resolve_identity
from open_integrity_agent import (
    ContractRecord,
    EntityRecord,
    InForceDebarmentDetector,
    IntegrityCase,
    Status,
)


def supplier_case():
    supplier = EntityRecord(
        entity_id="GB-COH:01234567",
        name="Example Engineering Ltd",
        stable_ids=("GB-COH:01234567",),
    )
    return IntegrityCase(
        subject_id="deb-case",
        contract=ContractRecord(
            contract_id="c1",
            authority_id="a1",
            supplier_ids=(supplier.entity_id,),
            award_date=date(2026, 6, 1),
        ),
        entities={supplier.entity_id: supplier},
        source_coverage={"procurement_award"},
    )


def external():
    return normalize_external_debarment(
        {
            "record_id": "wb-1",
            "name": "Example Engineering",
            "country": "United Kingdom",
            "address": "1 High Street London",
            "imposed_from": "2026-01-01",
            "imposed_to": "2026-12-31",
        },
        source_name="World Bank official debarment list",
        source_url="https://www.worldbank.org/debarr",
    )


def test_name_only_debarment_join_is_rejected():
    case = supplier_case()
    weak = resolve_identity(
        IdentityProfile(label="Example Engineering Ltd"),
        external().identity_profile(),
    )
    assert not weak.usable_for_high_priority
    with pytest.raises(ValueError):
        attach_debarment_to_supplier(
            case,
            external(),
            supplier_id="GB-COH:01234567",
            match_decision=weak,
            source_scan_complete=True,
        )


def test_multi_attribute_match_can_attach_dated_external_fact():
    case = supplier_case()
    left = IdentityProfile(
        label="Example Engineering",
        address="1 High Street, London",
        jurisdiction="United Kingdom",
        birth_year=None,
    )
    right = external().identity_profile()
    # name + address + jurisdiction gives two contextual corroborators.
    decision = resolve_identity(left, right)
    assert decision.usable_for_high_priority

    attach_debarment_to_supplier(
        case,
        external(),
        supplier_id="GB-COH:01234567",
        match_decision=decision,
        source_scan_complete=True,
    )
    finding = InForceDebarmentDetector().run(case)
    assert finding.status == Status.FLAG
    assert finding.corruption_inference is False


def test_completed_scan_with_no_match_can_support_pass():
    case = supplier_case()
    mark_debarment_scan_complete(case)
    finding = InForceDebarmentDetector().run(case)
    assert finding.status == Status.PASS


def test_unperformed_scan_remains_abstain():
    case = supplier_case()
    finding = InForceDebarmentDetector().run(case)
    assert finding.status == Status.ABSTAIN
