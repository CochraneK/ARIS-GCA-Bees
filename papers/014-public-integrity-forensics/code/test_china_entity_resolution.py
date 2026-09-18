from china_entity_resolution import normalize_org_name, resolve_pair


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


def test_unmatched_name_has_no_link():
    a={"id":"a","name":"甲医院","stable_ids":[]}
    b={"id":"b","name":"乙医院","stable_ids":[]}
    assert resolve_pair(a,b) is None


def test_normalization_is_narrow():
    assert normalize_org_name(" 中国科学院（北京） ")=="中国科学院(北京)"
