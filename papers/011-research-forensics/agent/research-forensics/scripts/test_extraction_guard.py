from extraction_guard import verify_metadata_claims


def test_jstage_real_extraction_error_is_caught():
    authoritative = {
        "title": "Effect of Treadmill Exercise on Bone Mass in Female Rats",
        "year": "2005",
        "volume": "54",
        "issue": "1",
        "pages": "1–6",
    }
    extracted = {
        "title": "Effect of Treadmill Exercise on Bone Mass in Female Rats",
        "year": "2004",
        "volume": "54",
        "issue": "1",
        "pages": "1-8",
    }
    locators = {
        "title": "PDF p.1 title",
        "year": "PDF p.1 running header",
        "volume": "PDF p.1 running header",
        "issue": "PDF p.1 running header",
        "pages": "PDF p.1 running header",
    }
    out = verify_metadata_claims(extracted, authoritative, locators)
    assert out["safe"] is False
    assert {m["field"] for m in out["mismatches"]} == {"year", "pages"}


def test_verified_metadata_passes_after_source_correction():
    values = {
        "title": "Effect of Treadmill Exercise on Bone Mass in Female Rats",
        "year": "2005",
        "volume": "54",
        "issue": "1",
        "pages": "1-6",
    }
    locators = {field: "PDF p.1" for field in values}
    out = verify_metadata_claims(values, values, locators)
    assert out["safe"] is True


def test_unanchored_authoritative_field_fails_closed():
    out = verify_metadata_claims(
        {"year": "2005"},
        {"year": "2005"},
        {},
    )
    assert out["safe"] is False
    assert out["unanchored_fields"] == ["year"]
