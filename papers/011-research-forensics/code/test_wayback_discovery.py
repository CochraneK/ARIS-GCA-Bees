from wayback_discovery import (
    CdxRecord,
    build_cdx_url,
    filter_identity,
    parse_cdx_json,
    pre_event_records,
)


def test_build_cdx_url_ends_day_before_event():
    url = build_cdx_url(
        "https://example.org/article",
        event_date="2024-03-21",
        from_year=2016,
    )
    assert "filter=statuscode%3A200" in url
    assert "to=20240320" in url
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


def test_identity_guard_blocks_jstage_prefix_collisions():
    records = [
        CdxRecord("20180611212411", "https://www.jstage.jst.go.jp/article/expanim/54/1/54_1_1/_article", "TARGET"),
        CdxRecord("20180612120941", "https://www.jstage.jst.go.jp/article/expanim/54/1/54_1_101/_article", "NEIGHBOUR101"),
        CdxRecord("20180612152618", "https://www.jstage.jst.go.jp/article/expanim/54/1/54_1_107/_article", "NEIGHBOUR107"),
        CdxRecord("20180609171356", "https://www.jstage.jst.go.jp/article/expanim/54/1/54_1_13/_article", "NEIGHBOUR13"),
    ]
    kept = filter_identity(records, "/54_1_1/")
    assert [r.digest for r in kept] == ["TARGET"]


def test_identity_guard_can_be_disabled_for_exact_queries():
    records = [CdxRecord("20200101000000", "https://example.org/a", "A")]
    assert filter_identity(records, None) == records
