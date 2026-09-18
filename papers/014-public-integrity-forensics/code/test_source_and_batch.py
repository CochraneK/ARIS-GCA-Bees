from datetime import date

from batch_detectors import (
    AwardObservation,
    BidderObservation,
    SharedAddressBidderDetector,
    SplitAwardDetector,
    SupplierConcentrationDetector,
)
from entity_resolution import IdentityProfile, resolve_identity
from source_adapters import normalize_companies_house, normalize_ocds_release


def test_ocds_release_normalizes_award_and_stable_party_ids():
    release = {
        "ocid": "ocds-test-001",
        "id": "release-1",
        "date": "2026-01-11T10:30:00Z",
        "buyer": {"id": "buyer-1"},
        "parties": [
            {
                "id": "buyer-1",
                "name": "Example Ministry",
                "identifier": {"scheme": "GB-COH", "id": "11111111"},
            },
            {
                "id": "supplier-1",
                "name": "Example Supplier Ltd",
                "identifier": {"scheme": "GB-COH", "id": "22222222"},
            },
        ],
        "tender": {
            "numberOfTenderers": 1,
            "procurementMethod": "open",
        },
        "awards": [
            {
                "id": "award-1",
                "date": "2026-01-10T00:00:00Z",
                "value": {"amount": 99000, "currency": "GBP"},
                "suppliers": [{"id": "supplier-1"}],
            }
        ],
    }
    result = normalize_ocds_release(release, jurisdiction="GB")
    assert result.warnings == []
    assert len(result.cases) == 1
    case = result.cases[0]
    assert case.contract.contract_id == "ocds-test-001:award-1"
    assert case.contract.authority_id == "GB-COH:11111111"
    assert case.contract.supplier_ids == ("GB-COH:22222222",)
    assert case.contract.bid_count == 1
    assert case.contract.legal_threshold is None


def test_ocds_missing_supplier_is_warning_not_invented_identity():
    release = {
        "ocid": "ocds-test-002",
        "id": "release-2",
        "awards": [{"id": "a1", "value": {"amount": 100}}],
    }
    result = normalize_ocds_release(release)
    assert "award_without_supplier:a1" in result.warnings
    assert result.cases[0].contract.supplier_ids == ()


def test_companies_house_psc_natural_person_is_company_scoped():
    profile = {
        "company_number": "01234567",
        "company_name": "Supplier Ltd",
        "date_of_creation": "2024-01-01",
    }
    psc = [
        {
            "kind": "individual-person-with-significant-control",
            "name": "Alex Example",
            "notified_on": "2024-01-02",
            "links": {"self": "/company/01234567/persons-with-significant-control/individual/abc"},
        }
    ]
    result = normalize_companies_house(profile, psc)
    assert result.company.entity_id == "GB-COH:01234567"
    owner_id = next(iter(result.owner_entities))
    assert owner_id.startswith("GB-PSC:01234567:")
    assert result.relations[0].identity_strength == "multi_attribute"


def test_entity_resolution_same_name_only_abstains():
    a = IdentityProfile(label="Alex Example")
    b = IdentityProfile(label="Alex Example")
    result = resolve_identity(a, b)
    assert result.status == "ABSTAIN"
    assert result.strength == "name_only"
    assert result.usable_for_high_priority is False


def test_entity_resolution_conflicting_birth_year_blocks_match():
    a = IdentityProfile(label="Alex Example", birth_year=1970)
    b = IdentityProfile(label="Alex Example", birth_year=1980)
    result = resolve_identity(a, b)
    assert result.status == "CONFLICT"
    assert result.score == 0.0


def test_entity_resolution_name_plus_multiple_attributes_can_match():
    a = IdentityProfile(
        label="Alex Example",
        birth_year=1970,
        birth_month=5,
        address="1 High Street, London",
        jurisdiction="GB",
    )
    b = IdentityProfile(
        label="Alex Example",
        birth_year=1970,
        birth_month=5,
        address="1 High Street London",
        jurisdiction="GB",
    )
    result = resolve_identity(a, b)
    assert result.status == "MATCH"
    assert result.strength == "multi_attribute"
    assert result.usable_for_high_priority is True


def test_split_award_detector_flags_configured_deterministic_pattern():
    rows = [
        AwardObservation(
            "c1", "a1", "s1", date(2026, 1, 1), 90000, 100000, "road-repair"
        ),
        AwardObservation(
            "c2", "a1", "s1", date(2026, 1, 15), 90000, 100000, "road-repair"
        ),
    ]
    findings = SplitAwardDetector(window_days=30).run(rows)
    assert len(findings) == 1
    assert findings[0].evidence_class.value == "E1"
    assert findings[0].corruption_inference is False


def test_split_award_requires_comparable_procurement_key():
    rows = [
        AwardObservation("c1", "a1", "s1", date(2026, 1, 1), 90000, 100000, None),
        AwardObservation("c2", "a1", "s1", date(2026, 1, 5), 90000, 100000, None),
    ]
    assert SplitAwardDetector().run(rows) == []


def test_supplier_concentration_is_model_context_e4_not_guilt():
    rows = [
        AwardObservation(f"c{i}", "a1", "s1" if i < 4 else "s2", date(2026, 1, i + 1), 10)
        for i in range(5)
    ]
    findings = SupplierConcentrationDetector(min_awards=5, share_threshold=0.8).run(rows)
    assert len(findings) == 1
    assert findings[0].evidence_class.value == "E4"
    assert findings[0].corruption_inference is False


def test_shared_address_is_contextual_e0_with_benign_explanation():
    rows = [
        BidderObservation("c1", "b1", "10 Market Street"),
        BidderObservation("c1", "b2", "10 MARKET STREET."),
    ]
    findings = SharedAddressBidderDetector().run(rows)
    assert len(findings) == 1
    assert findings[0].evidence_class.value == "E0"
    assert findings[0].benign_explanations


def test_offshore_context_alone_is_not_promoted_by_any_core_detector():
    # Pilot 0 negative control: the core has no rule that turns "offshore"
    # status alone into corruption evidence.
    from open_integrity_agent import (
        ContractRecord,
        IntegrityCase,
        OpenIntegrityAgent,
        RelationRecord,
        SourceRef,
    )

    src = SourceRef("synthetic", "offshore-1")
    case = IntegrityCase(
        subject_id="offshore-control",
        contract=ContractRecord(
            contract_id="c1",
            authority_id="a1",
            supplier_ids=("s1",),
            award_date=date(2026, 1, 1),
            bid_count=3,
            source_refs=(src,),
        ),
        relations=[
            RelationRecord(
                left_id="s1",
                relation="ASSOCIATED_WITH_OFFSHORE_ENTITY",
                right_id="offshore-entity-1",
                source_ref=src,
                identity_strength="stable_id",
            )
        ],
    )
    result = OpenIntegrityAgent().run(case)
    assert result["review_priority"] != "HIGH"
    assert result["corruption_inference"] is False


def test_usaspending_adapter_uses_uei_and_does_not_invent_bid_count():
    from source_adapters import normalize_usaspending_award

    row = {
        "Award ID": "CONT_AWD_123",
        "Recipient Name": "Example Federal Supplier",
        "Recipient UEI": "ABC123XYZ789",
        "Awarding Agency": "Example Agency",
        "Awarding Agency Code": "999",
        "Award Amount": 125000.0,
        "Base Obligation Date": "2026-01-12",
        "Last Modified Date": "2026-01-13",
        "Contract Award Type": "Definitive Contract",
    }
    result = normalize_usaspending_award(row)
    case = result.case
    assert case.contract.contract_id == "USAspending:CONT_AWD_123"
    assert case.contract.supplier_ids == ("US-UEI:ABC123XYZ789",)
    assert case.contract.authority_id == "US-FED-AGENCY:999"
    assert case.contract.bid_count is None
    assert case.contract.legal_threshold is None
    assert result.warnings == []


def test_usaspending_missing_uei_downgrades_identity_with_warning():
    from source_adapters import normalize_usaspending_award

    row = {
        "Award ID": "CONT_AWD_456",
        "Recipient Name": "Name Only Supplier",
        "recipient_id": "recipient-hash-L",
        "Awarding Agency": "Example Agency",
        "Awarding Agency Code": "999",
        "Award Amount": 10,
    }
    result = normalize_usaspending_award(row)
    supplier_id = result.case.contract.supplier_ids[0]
    assert supplier_id.startswith("USAspending-recipient:")
    assert "recipient_uei_missing" in result.warnings
    assert result.case.entities[supplier_id].stable_ids == ()
