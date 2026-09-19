from china_stable_id_enrichment import enrich_nodes, enrich_one


def test_exact_uscc_attaches_only_allowlisted_factual_attributes():
    node={
        "id":"cn-uscc:91310000MA1K000001",
        "name":"示例供应商有限公司",
        "stable_ids":["CN-USCC:91310000MA1K000001"],
    }
    obs={
        "source_id":"official_corporate_registry",
        "source_record_id":"r1",
        "name":"示例供应商有限公司",
        "stable_ids":["91310000MA1K000001"],
        "attributes":{
            "registered_name":"示例供应商有限公司",
            "organization_type":"limited_company",
            "registration_status":"active",
            "public_registry_url":"https://example.invalid/r1",
            "phone":"must-not-propagate",
            "contact_person":"must-not-propagate",
        },
        "source_url":"https://example.invalid/r1",
        "retrieved_at":"2026-09-19T00:00:00Z",
        "source_access_state":"AVAILABLE",
    }
    out=enrich_one(node,obs)
    assert out["status"]=="ENRICHED_EXACT_STABLE_ID"
    assert out["auto_attach"] is True
    assert out["corruption_inference"] is False
    assert out["attached_attributes"]["registered_name"]=="示例供应商有限公司"
    assert "phone" not in out["attached_attributes"]
    assert "contact_person" not in out["attached_attributes"]


def test_name_only_match_never_auto_attaches():
    node={
        "id":"cn-ccgp-local:supplier:x",
        "name":"同名机构",
        "stable_ids":[],
    }
    obs={
        "source_id":"official_source",
        "source_record_id":"r2",
        "name":"同名机构",
        "stable_ids":[],
        "attributes":{"registration_status":"active"},
        "source_url":"https://example.invalid/r2",
        "retrieved_at":"2026-09-19T00:00:00Z",
        "source_access_state":"AVAILABLE",
    }
    out=enrich_one(node,obs)
    assert out["status"]=="REVIEW_CANDIDATE"
    assert out["auto_attach"] is False
    assert out["attached_attributes"]=={}
    assert out["corruption_inference"] is False


def test_same_name_disjoint_uscc_is_conflict_not_merge():
    node={
        "id":"CN-USCC:91310000MA1K000001",
        "name":"同名机构",
        "stable_ids":[],
    }
    obs={
        "source_id":"official_source",
        "source_record_id":"r3",
        "name":"同名机构",
        "stable_ids":["CN-USCC:91310000MA1K000002"],
        "attributes":{"registration_status":"active"},
        "source_url":"https://example.invalid/r3",
        "retrieved_at":"2026-09-19T00:00:00Z",
        "source_access_state":"AVAILABLE",
    }
    out=enrich_one(node,obs)
    assert out["status"]=="STABLE_ID_CONFLICT"
    assert out["auto_attach"] is False


def test_interactive_or_unavailable_source_is_coverage_gap():
    graph=[{
        "id":"CN-USCC:91310000MA1K000001",
        "name":"示例机构",
        "stable_ids":[],
    }]
    obs=[{
        "source_id":"cn_gsxt",
        "source_record_id":"",
        "name":"",
        "stable_ids":[],
        "attributes":{},
        "source_url":"https://www.gsxt.gov.cn/",
        "retrieved_at":"2026-09-19T00:00:00Z",
        "source_access_state":"INTERACTIVE_ONLY",
    }]
    out=enrich_nodes(graph,obs)
    assert out["coverage_gap_count"]==1
    assert out["auto_attached_count"]==0
    assert out["decisions"][0]["status"]=="COVERAGE_GAP"
    assert out["corruption_inference"] is False


def test_exact_id_and_name_only_are_separated_in_batch():
    graph=[
        {
            "id":"CN-USCC:91310000MA1K000001",
            "name":"A公司",
            "stable_ids":[],
        },
        {
            "id":"local:b",
            "name":"B公司",
            "stable_ids":[],
        },
    ]
    obs=[
        {
            "source_id":"official_1",
            "source_record_id":"a",
            "name":"A公司",
            "stable_ids":["91310000MA1K000001"],
            "attributes":{"registration_status":"active"},
            "source_url":"https://example.invalid/a",
            "retrieved_at":"2026-09-19T00:00:00Z",
            "source_access_state":"AVAILABLE",
        },
        {
            "source_id":"official_2",
            "source_record_id":"b",
            "name":"B公司",
            "stable_ids":[],
            "attributes":{"registration_status":"active"},
            "source_url":"https://example.invalid/b",
            "retrieved_at":"2026-09-19T00:00:00Z",
            "source_access_state":"AVAILABLE",
        },
    ]
    out=enrich_nodes(graph,obs)
    assert out["status_counts"]["ENRICHED_EXACT_STABLE_ID"]==1
    assert out["status_counts"]["REVIEW_CANDIDATE"]==1
    assert out["auto_attached_count"]==1
    assert out["review_required_count"]==1
