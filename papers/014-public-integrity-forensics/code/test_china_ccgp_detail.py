from china_ccgp_detail import parse_ccgp_award_detail


def test_multi_package_detail_normalizes_one_lot_per_supplier():
    html = """
    <html><body>
    <p>2026年09月09日 18:14 来源：</p>
    <table>
      <tr><td>采购单位</td><td>湖北省林业科学研究院</td></tr>
      <tr><td>代理机构名称</td><td>武汉某招标代理有限公司</td></tr>
    </table>
    <h2>一、项目编号</h2><p>WHXLH-202608-1013</p>
    <h2>二、采购计划备案号</h2><p>420000-2026-08634</p>
    <h2>三、项目名称</h2><p>森林混交提质经营技术推广示范</p>
    <h2>四、中标（成交）信息</h2>
    <p>包名称：包1：种苗抚育物资</p>
    <p>供应商名称：甲供应商有限公司</p>
    <p>供应商地址：不应进入结构化输出</p>
    <p>中标（成交）金额：3.3175(万元)</p>
    <p>综合评分法：91.6（分）</p>
    <p>名称：种苗抚育物资</p>
    <p>包名称：包2：技术示范</p>
    <p>供应商名称：乙供应商有限公司</p>
    <p>中标（成交）金额：54.2(万元)</p>
    <h2>五、评审小组成员</h2>
    <p>某某</p>
    </body></html>
    """
    n = parse_ccgp_award_detail(
        html,
        source_url="https://www.ccgp.gov.cn/example.htm",
        retrieved_at="2026-09-18T00:00:00Z",
    )
    assert n.project_id == "WHXLH-202608-1013"
    assert n.procurement_plan_id == "420000-2026-08634"
    assert n.project_name == "森林混交提质经营技术推广示范"
    assert n.buyer_name == "湖北省林业科学研究院"
    assert n.buyer_institution_type == "research_institute"
    assert len(n.lots) == 2
    assert n.lots[0].package_name == "包1：种苗抚育物资"
    assert n.lots[0].award_value_yuan == 33175.0
    assert n.lots[1].award_value_yuan == 542000.0
    assert "不应进入结构化输出" not in str(n.as_json())


def test_percentage_quote_never_becomes_currency():
    html = """
    <p>2026年09月09日 18:14 来源：</p>
    <table><tr><td>采购单位</td><td>武汉市肺科医院</td></tr></table>
    <h2>一、项目编号</h2><p>HBZLT-WH-126149</p>
    <h2>二、采购计划备案号</h2><p>420100-2026-04078</p>
    <h2>三、项目名称</h2><p>零星工程服务</p>
    <h2>四、中标（成交）信息</h2>
    <p>供应商名称：湖北某建设有限公司</p>
    <p>中标（成交）金额：95(%)</p>
    <h2>五、评审小组成员</h2>
    """
    n = parse_ccgp_award_detail(
        html,
        source_url="https://www.ccgp.gov.cn/example2.htm",
        retrieved_at="2026-09-18T00:00:00Z",
    )
    assert n.buyer_institution_type == "hospital"
    assert n.lots[0].award_value_yuan is None
    assert n.lots[0].pricing_basis == "percentage"
    assert n.corruption_inference is False
