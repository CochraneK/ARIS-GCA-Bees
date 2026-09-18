from pilot0 import grim_item_mean, review_priority, sample_size_consistency


def test_grim_flags_impossible_item_mean():
    finding = grim_item_mean("6.98", n=25, scale_min=1, scale_max=7)
    assert finding.applicable
    assert finding.status == "FLAG"
    assert finding.misconduct_inference is False


def test_grim_passes_possible_item_mean():
    finding = grim_item_mean("6.96", n=25, scale_min=1, scale_max=7)
    assert finding.status == "PASS"


def test_sample_size_mismatch():
    finding = sample_size_consistency({"methods": 42, "table": 37})
    assert finding.status == "FLAG"


def test_two_strong_independent_families_raise_review_priority():
    a = grim_item_mean("6.98", n=25, scale_min=1, scale_max=7)
    b = sample_size_consistency({"methods": 42, "table": 37})
    out = review_priority([a, b])
    assert out["review_priority"] == "HIGH"
