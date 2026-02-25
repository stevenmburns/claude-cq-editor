from cq_models.l_bracket import make_l_bracket


def test_default_bracket_is_valid():
    result = make_l_bracket()
    assert result.val().isValid()


def test_bounding_box_matches_params():
    result = make_l_bracket(outer=60, inner=40, height=3)
    bb = result.val().BoundingBox()
    # loop center at (outer - loop_offset, outer - loop_offset), default loop_offset=5, radius=10
    assert abs(bb.xlen - 65) < 0.1
    assert abs(bb.ylen - 65) < 0.1
    assert abs(bb.zlen - 3) < 0.1


def test_volume_less_than_solid():
    outer, inner, height = 60, 40, 3
    solid_vol = outer * outer * height
    result = make_l_bracket(outer=outer, inner=inner, height=height)
    assert result.val().Volume() < solid_vol


def test_volume_positive():
    result = make_l_bracket()
    assert result.val().Volume() > 0


def test_custom_params_produce_valid_bracket():
    result = make_l_bracket(outer=80, inner=50, height=5)
    assert result.val().isValid()
