import pytest
from cq_models.bracket import make_bracket


def test_default_bracket_is_valid():
    result = make_bracket()
    assert result.val().isValid()


def test_bounding_box_matches_params():
    result = make_bracket(outer=60, inner=40, height=3)
    bb = result.val().BoundingBox()
    assert abs(bb.xlen - 60) < 0.1
    assert abs(bb.ylen - 60) < 0.1
    assert abs(bb.zlen - 3) < 0.1


def test_volume_less_than_solid():
    outer, inner, height = 60, 40, 3
    solid_vol = outer * outer * height
    result = make_bracket(outer=outer, inner=inner, height=height)
    assert result.val().Volume() < solid_vol


def test_volume_positive():
    result = make_bracket()
    assert result.val().Volume() > 0


def test_custom_params_produce_valid_bracket():
    result = make_bracket(outer=80, inner=50, height=5, cut_offset=15)
    assert result.val().isValid()
