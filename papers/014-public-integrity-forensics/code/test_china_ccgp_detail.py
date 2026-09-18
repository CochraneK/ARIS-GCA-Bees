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


def test_central_notice_three_section_schema():
    html = """
    <p>2026年09月18日 14:18 来源：</p>
    <table>
      <tr><td>采购单位</td><td>中国中医科学院广安门医院</td></tr>
      <tr><td>代理机构名称</td><td>中国仪器进出口集团有限公司</td></tr>
    </table>
    <p>一、项目编号：26CNIC381070-044（招标文件编号：26CNIC381070-044）</p>
    <p>二、项目名称：中国中医科学院广安门医院移动推车工作站采购</p>
    <p>三、中标（成交）信息</p>
    <p>供应商名称：北京医惠科技有限公司</p>
    <p>供应商地址：不公开进规范化结果</p>
    <p>中标（成交）金额：84.6000000（万元）</p>
    <p>四、主要标的信息</p>
    """
    n = parse_ccgp_award_detail(
        html,
        source_url="https://www.ccgp.gov.cn/central-example.htm",
        retrieved_at="2026-09-18T00:00:00Z",
    )
    assert n.project_id == "26CNIC381070-044"
    assert n.procurement_plan_id is None
    assert n.project_name == "中国中医科学院广安门医院移动推车工作站采购"
    assert len(n.lots) == 1
    assert n.lots[0].supplier_name == "北京医惠科技有限公司"
    assert n.lots[0].award_value_yuan == 846000.0
    assert n.lots[0].pricing_basis == "currency"


def test_local_simple_award_heading_and_unit_in_label():
    html = """
    <table><tr><td>采购单位</td><td>蒙自市某学校</td></tr></table>
    <p>一、项目编号:HHZC2025-G3-02322-YNWM-0049</p>
    <p>二、项目名称：综合保障责任保险采购项目</p>
    <p>三、中标信息</p>
    <p>供应商名称：中国平安财产保险股份有限公司云南分公司</p>
    <p>中标金额(万元)：259.071</p>
    <p>四、主要标的信息</p>
    """
    n = parse_ccgp_award_detail(
        html,
        source_url="https://www.ccgp.gov.cn/local-simple.htm",
        retrieved_at="2026-09-18T00:00:00Z",
    )
    assert n.project_id == "HHZC2025-G3-02322-YNWM-0049"
    assert len(n.lots) == 1
    assert n.lots[0].supplier_name == "中国平安财产保险股份有限公司云南分公司"
    assert n.lots[0].award_value_yuan == 2590710.0
    assert n.lots[0].result_status == "awarded"
    assert n.lots[0].candidate_rank is None


def test_ranked_bid_candidates_are_not_final_awards():
    html = """
    <table><tr><td>采购单位</td><td>东北师范大学</td></tr></table>
    <p>一、项目编号：SYZX2026-093</p>
    <p>二、项目名称：监理服务</p>
    <p>三、中标（成交）信息</p>
    <p>供应商名称：第一中标候选人：吉林建院工程建设监理咨询有限公司</p>
    <p>中标（成交）金额：158.33（万元）</p>
    <p>供应商名称：第二中标候选人：长春一汽建设监理有限责任公司</p>
    <p>中标（成交）金额：157（万元）</p>
    <p>四、主要标的信息</p>
    """
    n = parse_ccgp_award_detail(
        html,
        source_url="https://www.ccgp.gov.cn/candidates.htm",
        retrieved_at="2026-09-18T00:00:00Z",
    )
    assert len(n.lots) == 2
    assert n.lots[0].supplier_name == "吉林建院工程建设监理咨询有限公司"
    assert n.lots[0].result_status == "candidate"
    assert n.lots[0].candidate_rank == 1
    assert n.lots[1].supplier_name == "长春一汽建设监理有限责任公司"
    assert n.lots[1].result_status == "candidate"
    assert n.lots[1].candidate_rank == 2


def test_structured_table_extracts_uscc_without_contact_fields():
    html = """
    <table><tr><td>采购单位</td><td>天津科技大学</td></tr></table>
    <p>一、项目编号：SHGP-2026-A409</p>
    <p>二、项目名称：全自动细胞荧光处理系统等设备采购项目</p>
    <p>三、中标信息</p>
    <table>
      <tr>
        <th>供应商名称</th><th>供应商地址</th><th>统一社会信用代码</th>
        <th>企业办公电话</th><th>中标金额(万元)</th><th>评审得分</th>
      </tr>
      <tr>
        <td>全视未来（北京）科技有限公司</td><td>北京市某地址</td>
        <td>91110108MA01KRJX1U</td><td>010-00000000</td><td>49.9</td><td>89.00</td>
      </tr>
    </table>
    <p>四、主要标的信息</p>
    """
    n = parse_ccgp_award_detail(
        html,
        source_url="https://www.ccgp.gov.cn/uscc-example.htm",
        retrieved_at="2026-09-18T00:00:00Z",
    )
    assert len(n.lots) == 1
    assert n.lots[0].supplier_name == "全视未来（北京）科技有限公司"
    assert n.lots[0].supplier_uscc == "91110108MA01KRJX1U"
    assert n.lots[0].award_value_yuan == 499000.0
    assert n.lots[0].score == 89.0
    payload = str(n.as_json())
    assert "北京市某地址" not in payload
    assert "010-00000000" not in payload


def test_bid_ranking_table_without_uscc_is_not_promoted_to_final_award():
    html = """
    <table><tr><td>采购单位</td><td>天津科技大学</td></tr></table>
    <p>一、项目编号：P-3</p>
    <p>二、项目名称：设备采购</p>
    <p>三、中标信息</p>
    <table>
      <tr><th>排序</th><th>供应商名称</th><th>评审报价（万元）</th><th>评审得分</th></tr>
      <tr><td>1</td><td>甲公司</td><td>10</td><td>90</td></tr>
      <tr><td>2</td><td>乙公司</td><td>11</td><td>80</td></tr>
    </table>
    <p>四、主要标的信息</p>
    """
    n = parse_ccgp_award_detail(
        html,
        source_url="https://www.ccgp.gov.cn/rank-only.htm",
        retrieved_at="2026-09-18T00:00:00Z",
    )
    assert n.lots == ()
    assert "no_supplier_lots_parsed" in n.warnings
