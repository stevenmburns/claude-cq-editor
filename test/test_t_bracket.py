from cq_models.t_bracket import make_t_bracket


def test_default_t_bracket_is_valid():
    result = make_t_bracket()
    assert result.val().isValid()


def test_bounding_box_matches_params():
    outer, inner, height, arm_len = 60, 44, 3, 60
    result = make_t_bracket(outer=outer, inner=inner, height=height, arm_len=arm_len)
    bb = result.val().BoundingBox()
    arm_w = outer - inner  # 16
    loop_offset = 0  # default
    # loop centre at (arm_len, loop_offset) = (60, 0), radius=10
    # x: bar = 2×arm_len = 120
    # y: loop bottom at loop_offset - 10 = -10, stem top at arm_w + arm_len = 76
    assert abs(bb.xlen - 2 * arm_len) < 0.5
    assert abs(bb.ylen - (arm_w + arm_len + 10 - loop_offset)) < 0.5
    assert abs(bb.zlen - height) < 0.1


def test_volume_positive():
    result = make_t_bracket()
    assert result.val().Volume() > 0


def test_volume_less_than_bounding_box():
    outer, inner, height, arm_len = 60, 44, 3, 60
    arm_w = outer - inner
    bbox_vol = (2 * arm_len) * (arm_w + arm_len) * height
    result = make_t_bracket(outer=outer, inner=inner, height=height, arm_len=arm_len)
    assert result.val().Volume() < bbox_vol


def test_custom_params_produce_valid_bracket():
    result = make_t_bracket(outer=80, inner=50, height=5)
    assert result.val().isValid()
