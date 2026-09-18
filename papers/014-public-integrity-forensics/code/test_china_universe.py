from china_universe import parse_cas_research_units, parse_sasac_central_soe


def test_sasac_parser_extracts_organization_names_only():
    html = """
    <table>
      <tr><td>1</td><td>中国核工业集团有限公司</td></tr>
      <tr><td>2</td><td>中国航天科技集团有限公司</td></tr>
    </table>
    """
    snap = parse_sasac_central_soe(html, retrieved_at="2026-09-18T00:00:00Z")
    assert [x.name for x in snap.seeds] == [
        "中国核工业集团有限公司",
        "中国航天科技集团有限公司",
    ]
    assert all(x.institution_type == "soe" for x in snap.seeds)
    assert all(x.corruption_inference is False for x in snap.seeds)


def test_cas_parser_normalizes_research_unit_names():
    html = """
    <div>
      <a>物理研究所</a>
      <a>理论物理研究所</a>
      <a>中国科学院大学</a>
      <a>研究单位</a>
    </div>
    """
    snap = parse_cas_research_units(html, retrieved_at="2026-09-18T00:00:00Z")
    assert [x.name for x in snap.seeds] == [
        "中国科学院物理研究所",
        "中国科学院理论物理研究所",
    ]
    assert all(x.institution_type == "research_institute" for x in snap.seeds)
