from wayback_discovery import (
    build_cdx_url,
    parse_cdx_json,
    pre_event_records,
)


def test_build_cdx_url_has_fail_closed_date_and_status_filter():
    url = build_cdx_url(
        "https://example.org/article",
        event_date="2024-03-21",
        from_year=2016,
    )
    assert "filter=statuscode%3A200" in url
    assert "to=20240321" in url
    assert "from=2016" in url
    assert "collapse=digest" in url


def test_parse_and_filter_strictly_pre_event():
    payload = """[
      ["timestamp","original","digest","statuscode","mimetype"],
      ["20220520171120","https://example.org/a","AAA","200","text/html"],
      ["20240321000000","https://example.org/a","BBB","200","text/html"],
      ["20210101000000","https://example.org/a","CCC","404","text/html"]
    ]"""
    records = parse_cdx_json(payload)
    kept = pre_event_records(records, "2024-03-21")
    assert [r.digest for r in kept] == ["AAA"]
