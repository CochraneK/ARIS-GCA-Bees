from china_ccgp_detail import parse_ccgp_award_detail
from china_procurement_graph import ccgp_notice_graph, graph_summary


def test_candidate_never_becomes_awarded_to_edge():
    html = """
    <table><tr><td>采购单位</td><td>某大学</td></tr></table>
    <p>一、项目编号：P-1</p>
    <p>二、项目名称：监理服务</p>
    <p>三、中标（成交）信息</p>
    <p>供应商名称：第一中标候选人：甲公司</p>
    <p>中标（成交）金额：100（万元）</p>
    <p>供应商名称：第二中标候选人：乙公司</p>
    <p>中标（成交）金额：98（万元）</p>
    <p>四、主要标的信息</p>
    """
    notice = parse_ccgp_award_detail(
        html,
        source_url="https://www.ccgp.gov.cn/p-1.htm",
        retrieved_at="2026-09-18T00:00:00Z",
    )
    graph = ccgp_notice_graph(notice)
    types = [x["type"] for x in graph["edges"]]
    assert types.count("AWARDED_TO") == 0
    assert types.count("HAS_RANKED_CANDIDATE") == 2
    assert graph_summary(graph)["candidate_edges"] == 2
    assert graph["identity_resolution_required"] is True
    assert graph["corruption_inference"] is False


def test_final_supplier_gets_awarded_edge_but_source_local_identity():
    html = """
    <table>
      <tr><td>采购单位</td><td>某医院</td></tr>
      <tr><td>代理机构名称</td><td>某代理有限公司</td></tr>
    </table>
    <p>一、项目编号：P-2</p>
    <p>二、项目名称：设备采购</p>
    <p>三、中标信息</p>
    <p>供应商名称：某设备有限公司</p>
    <p>中标金额(万元)：12.5</p>
    <p>四、主要标的信息</p>
    """
    notice = parse_ccgp_award_detail(
        html,
        source_url="https://www.ccgp.gov.cn/p-2.htm",
        retrieved_at="2026-09-18T00:00:00Z",
    )
    graph = ccgp_notice_graph(notice)
    awarded = [x for x in graph["edges"] if x["type"] == "AWARDED_TO"]
    assert len(awarded) == 1
    assert awarded[0]["award_value_yuan"] == 125000.0

    supplier_nodes = [x for x in graph["nodes"] if x["type"] == "supplier"]
    assert len(supplier_nodes) == 1
    assert supplier_nodes[0]["identity_scope"] == "source_local_name"
    assert supplier_nodes[0]["stable_ids"] == []


def test_same_supplier_name_across_notices_is_not_auto_merged():
    def make(url, project):
        html = f"""
        <table><tr><td>采购单位</td><td>某医院</td></tr></table>
        <p>一、项目编号：{project}</p>
        <p>二、项目名称：设备采购</p>
        <p>三、中标信息</p>
        <p>供应商名称：同名供应商有限公司</p>
        <p>中标金额(万元)：10</p>
        <p>四、主要标的信息</p>
        """
        return parse_ccgp_award_detail(
            html, source_url=url, retrieved_at="2026-09-18T00:00:00Z"
        )

    g1 = ccgp_notice_graph(make("https://www.ccgp.gov.cn/a.htm", "A"))
    g2 = ccgp_notice_graph(make("https://www.ccgp.gov.cn/b.htm", "B"))
    s1 = next(x["id"] for x in g1["nodes"] if x["type"] == "supplier")
    s2 = next(x["id"] for x in g2["nodes"] if x["type"] == "supplier")
    assert s1 != s2
