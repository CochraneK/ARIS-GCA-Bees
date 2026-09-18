from companies_house_uri import normalize_companies_house_uri


def test_companies_house_uri_normalizes_ddmmyyyy_without_address_retention():
    entity, meta = normalize_companies_house_uri(
        {
            "CompanyName": "Example Ltd",
            "CompanyNumber": "01234567",
            "IncorporationDate": "31/12/2024",
            "CompanyStatus": "Active",
            "RegAddress": {
                "AddressLine1": "Sensitive-for-this-test address should not be copied"
            },
        },
        source_url="http://data.companieshouse.gov.uk/doc/company/01234567.json",
    )
    assert entity.entity_id == "GB-COH:01234567"
    assert entity.incorporated_on.isoformat() == "2024-12-31"
    assert "RegAddress" not in meta
    assert "address" not in meta


def test_companies_house_uri_accepts_iso_date():
    entity, _ = normalize_companies_house_uri(
        {
            "CompanyName": "Example Ltd",
            "CompanyNumber": "SC001234",
            "IncorporationDate": "2020-01-02",
        },
        source_url="http://data.companieshouse.gov.uk/doc/company/SC001234.json",
    )
    assert entity.incorporated_on.isoformat() == "2020-01-02"
