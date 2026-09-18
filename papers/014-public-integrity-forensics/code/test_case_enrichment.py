from datetime import date

import pytest

from case_enrichment import (
    PublicOfficeObservation,
    attach_companies_house,
    attach_public_office,
)
from entity_resolution import IdentityProfile, resolve_identity
from open_integrity_agent import (
    ContractRecord,
    IntegrityCase,
    OpenIntegrityAgent,
    SourceRef,
)
from source_adapters import normalize_companies_house


SRC = SourceRef("synthetic procurement", "p1")


def procurement_case():
    supplier_id = "GB-COH:01234567"
    return IntegrityCase(
        subject_id="join-case",
        contract=ContractRecord(
            contract_id="c1",
            authority_id="authority",
            supplier_ids=(supplier_id,),
            award_date=date(2026, 6, 1),
            bid_count=3,
            source_refs=(SRC,),
        ),
        source_coverage={"procurement_award", "procurement_competition"},
    )


def ch_bundle():
    return normalize_companies_house(
        {
            "company_number": "01234567",
            "company_name": "Supplier Ltd",
            "date_of_creation": "2024-01-01",
        },
        [
            {
                "kind": "individual-person-with-significant-control",
                "name": "Alex Example",
                "notified_on": "2024-01-02",
                "links": {
                    "self": "/company/01234567/persons-with-significant-control/individual/abc"
                },
            }
        ],
    )


def test_exact_company_identifier_attaches_ownership_without_name_matching():
    case = procurement_case()
    attach_companies_house(case, ch_bundle())
    assert "ownership" in case.source_coverage
    assert case.entities["GB-COH:01234567"].incorporated_on == date(2024, 1, 1)
    assert len(case.relations) == 1
    assert case.relations[0].right_id == "GB-COH:01234567"


def test_unmatched_company_cannot_attach_by_name_only():
    case = IntegrityCase(
        subject_id="bad-join",
        contract=ContractRecord(
            contract_id="c2",
            authority_id="a",
            supplier_ids=("local-supplier-1",),
            award_date=date(2026, 6, 1),
        ),
    )
    with pytest.raises(ValueError):
        attach_companies_house(case, ch_bundle())


def test_cross_source_public_office_requires_explicit_resolved_person():
    case = procurement_case()
    imported = ch_bundle()
    attach_companies_house(case, imported)
    owner_id = next(iter(imported.owner_entities))

    decision = resolve_identity(
        IdentityProfile(
            label="Alex Example",
            birth_year=1970,
            address="1 High Street",
            jurisdiction="GB",
        ),
        IdentityProfile(
            label="Alex Example",
            birth_year=1970,
            address="1 High Street",
            jurisdiction="GB",
        ),
    )
    assert decision.usable_for_high_priority

    office_src = SourceRef("official office register", "office-1")
    attach_public_office(
        case,
        PublicOfficeObservation(
            person_id=owner_id,
            title="Synthetic Public Office",
            valid_from=date(2025, 1, 1),
            valid_to=date(2027, 1, 1),
            source_ref=office_src,
        ),
        source_person_id="external-person-id",
        match_decision=decision,
    )
    assert "public_office" in case.source_coverage

    report = OpenIntegrityAgent().run(case)
    finding = next(
        f for f in report["findings"]
        if f["detector_id"] == "public_office_ownership_link"
    )
    assert finding["status"] == "FLAG"
    assert finding["evidence_class"] == "E2"
    assert finding["corruption_inference"] is False
    assert report["corruption_inference"] is False


def test_name_only_public_office_resolution_is_rejected():
    case = procurement_case()
    imported = ch_bundle()
    attach_companies_house(case, imported)
    owner_id = next(iter(imported.owner_entities))
    weak = resolve_identity(
        IdentityProfile(label="Alex Example"),
        IdentityProfile(label="Alex Example"),
    )
    assert not weak.usable_for_high_priority

    with pytest.raises(ValueError):
        attach_public_office(
            case,
            PublicOfficeObservation(
                person_id=owner_id,
                title="Synthetic Office",
                valid_from=date(2025, 1, 1),
                valid_to=None,
                source_ref=SourceRef("office", "1"),
            ),
            source_person_id="external-name-only",
            match_decision=weak,
        )
