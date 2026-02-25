from cq_models.t_bracket import make_t_bracket


def test_default_t_bracket_is_valid():
    result = make_t_bracket()
    assert result.val().isValid()


def test_bounding_box_matches_params():
    outer, inner, height = 60, 44, 3
    result = make_t_bracket(outer=outer, inner=inner, height=height)
    bb = result.val().BoundingBox()
    arm_w = outer - inner  # 16
    stem_len = outer / 2  # 30
    loop_offset = 5  # default
    # loop centre at (outer/2, loop_offset) = (30, 5), radius=10
    # x: bar dominates → 0 to outer = 60
    # y: loop bottom at loop_offset - 10 = -5, stem top at arm_w + stem_len = 46
    assert abs(bb.xlen - outer) < 0.5
    assert abs(bb.ylen - (arm_w + stem_len + 10 - loop_offset)) < 0.5
    assert abs(bb.zlen - height) < 0.1


def test_volume_positive():
    result = make_t_bracket()
    assert result.val().Volume() > 0


def test_volume_less_than_bounding_box():
    outer, inner, height = 60, 44, 3
    arm_w = outer - inner
    stem_len = outer / 2
    bbox_vol = outer * (arm_w + stem_len) * height
    result = make_t_bracket(outer=outer, inner=inner, height=height)
    assert result.val().Volume() < bbox_vol


def test_custom_params_produce_valid_bracket():
    result = make_t_bracket(outer=80, inner=50, height=5)
    assert result.val().isValid()
