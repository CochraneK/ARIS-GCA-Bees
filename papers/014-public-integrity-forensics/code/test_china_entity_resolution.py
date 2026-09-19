from china_entity_resolution import (
    build_resolution_audit,
    normalize_cn_uscc,
    normalize_org_name,
    resolve_pair,
)


def test_exact_uscc_auto_merge():
    a={"id":"src:a","name":"甲公司","stable_ids":["CN-USCC:91310000123456789X"]}
    b={"id":"src:b","name":"甲公司有限公司","stable_ids":["CN-USCC:91310000123456789X"]}
    d=resolve_pair(a,b)
    assert d is not None
    assert d.relation=="SAME_ORG"
    assert d.auto_merge is True
    assert d.corruption_inference is False


def test_exact_name_without_stable_id_never_auto_merges():
    a={"id":"src:a","name":"中国科学院测试研究所","stable_ids":[]}
    b={"id":"src:b","name":" 中国科学院测试研究所 ","stable_ids":[]}
    d=resolve_pair(a,b)
    assert d is not None
    assert d.relation=="REVIEW_CANDIDATE"
    assert d.auto_merge is False


def test_same_name_disjoint_stable_ids_is_conflict():
    a={"id":"src:a","name":"甲公司","stable_ids":["CN-USCC:91310000123456789X"]}
    b={"id":"src:b","name":"甲公司","stable_ids":["CN-USCC:91310000123456788W"]}
    d=resolve_pair(a,b)
    assert d is not None
    assert d.relation=="STABLE_ID_CONFLICT"
    assert d.auto_merge is False
    assert d.corruption_inference is False


def test_unmatched_name_has_no_link():
    a={"id":"a","name":"甲医院","stable_ids":[]}
    b={"id":"b","name":"乙医院","stable_ids":[]}
    assert resolve_pair(a,b) is None


def test_normalization_is_narrow():
    assert normalize_org_name(" 中国科学院（北京） ")=="中国科学院(北京)"


def test_cn_uscc_normalization_and_invalid_rejection():
    assert normalize_cn_uscc(" cn-uscc:91310000123456789x ") == "CN-USCC:91310000123456789X"
    assert normalize_cn_uscc("CN-USCC:123") is None
    assert normalize_cn_uscc("CN-USCC:91310000123456789I") is None


def test_resolution_audit_separates_merge_review_conflict_and_unlinked():
    nodes=[
        {"id":"ccgp:a","name":"甲公司","stable_ids":["CN-USCC:91310000123456789X"]},
        {"id":"corp:a","name":"甲公司有限公司","stable_ids":["91310000123456789X"]},
        {"id":"source:b","name":"乙机构","stable_ids":[]},
        {"id":"source:c","name":" 乙机构 ","stable_ids":[]},
        {"id":"source:d","name":"丙机构","stable_ids":["CN-USCC:91310000123456788W"]},
        {"id":"source:e","name":"丙机构","stable_ids":["CN-USCC:91310000123456787U"]},
        {"id":"source:f","name":"丁机构","stable_ids":[]},
    ]
    audit=build_resolution_audit(nodes)

    assert audit["nodes"] == 7
    assert audit["nodes_with_valid_cn_uscc"] == 4
    assert audit["exact_stable_id_cluster_count"] == 1
    assert audit["exact_stable_id_clusters"][0]["stable_id"] == "CN-USCC:91310000123456789X"
    assert audit["exact_stable_id_clusters"][0]["node_ids"] == ["ccgp:a","corp:a"]
    assert audit["auto_merge_decision_count"] == 1
    assert audit["name_only_review_candidate_count"] == 1
    assert audit["stable_id_conflict_count"] == 1
    assert audit["unlinked_node_ids"] == ["source:f"]
    assert audit["corruption_inference"] is False


def test_resolution_audit_rejects_duplicate_node_ids():
    nodes=[
        {"id":"dup","name":"甲","stable_ids":[]},
        {"id":"dup","name":"乙","stable_ids":[]},
    ]
    try:
        build_resolution_audit(nodes)
    except ValueError as exc:
        assert "unique" in str(exc)
    else:
        raise AssertionError("expected ValueError")
