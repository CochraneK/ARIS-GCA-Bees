from china_ccgp import aggregate, classify_buyer, parse_ccgp_award_list
from china_scope import InstitutionType


HTML = """
<html><body><ul>
<li><a href="/cggg/zygg/zbgg/202609/t1.htm">某医疗设备项目中标公告</a>
发布时间：2026-09-17 19:50 地域：山东 采购人：山东大学齐鲁医院</li>
<li><a href="/cggg/zygg/zbgg/202609/t2.htm">某仪器项目中标公告</a>
发布时间：2026-09-17 18:10 地域：北京 采购人：中国科学院物理研究所</li>
<li><a href="/cggg/zygg/zbgg/202609/t3.htm">某设备采购项目中标公告</a>
发布时间：2026-09-17 18:44 地域：北京 采购人：清华大学</li>
<li><a href="/cggg/zygg/zbgg/202609/t4.htm">某服务项目中标公告</a>
发布时间：2026-09-17 18:14 地域：广东 采购人：中华人民共和国深圳海关</li>
</ul></body></html>
"""


def test_ccgp_list_parser_extracts_public_metadata_without_contacts():
    out = parse_ccgp_award_list(
        HTML,
        source_url="https://www.ccgp.gov.cn/cggg/zygg/zbgg/index.htm",
        retrieved_at="2026-09-18T00:00:00+00:00",
    )
    assert len(out.leads) == 4
    assert out.leads[0].buyer_name == "山东大学齐鲁医院"
    assert out.leads[0].institution_type == "hospital"
    assert out.leads[1].institution_type == "research_institute"
    assert out.leads[2].institution_type == "university"
    assert out.leads[3].institution_type == "government"
    assert all(x.corruption_inference is False for x in out.leads)


def test_buyer_classifier_is_routing_not_forced_classification():
    assert classify_buyer("北京大学人民医院") is InstitutionType.HOSPITAL
    assert classify_buyer("中国科学院成都生物研究所") is InstitutionType.RESEARCH_INSTITUTE
    assert classify_buyer("中山大学") is InstitutionType.UNIVERSITY
    assert classify_buyer("某某科技有限公司") is InstitutionType.OTHER


def test_aggregate_is_source_feasibility_only():
    out = parse_ccgp_award_list(
        HTML,
        source_url="https://www.ccgp.gov.cn/cggg/zygg/zbgg/index.htm",
        retrieved_at="2026-09-18T00:00:00+00:00",
    )
    agg = aggregate([out])
    assert agg["unique_award_notice_leads"] == 4
    assert agg["buyer_metadata_coverage"] == 1.0
    assert agg["publication_time_coverage"] == 1.0
    assert agg["corruption_inference"] is False
