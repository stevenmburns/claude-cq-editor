from cq_models.l_bracket import make_l_bracket


def test_default_bracket_is_valid():
    result = make_l_bracket()
    assert result.val().isValid()


def test_bounding_box_matches_params():
    arm_w, arm_len, height = 20, 50, 3
    result = make_l_bracket(arm_w=arm_w, arm_len=arm_len, height=height)
    bb = result.val().BoundingBox()
    loop_offset = 5  # default
    # loop at (arm_w/2 - loop_offset, arm_w/2 - loop_offset) = (5, 5), radius=10
    # xmax = arm_w/2 - loop_offset + 10 = 15, xmin = -arm_len = -50 → xlen = 65
    expected = arm_len + arm_w / 2 + 10 - loop_offset
    assert abs(bb.xlen - expected) < 0.1
    assert abs(bb.ylen - expected) < 0.1
    assert abs(bb.zlen - height) < 0.1


def test_volume_less_than_solid():
    arm_w, arm_len, height = 20, 50, 3
    solid_vol = (arm_len + arm_w / 2) ** 2 * height
    result = make_l_bracket(arm_w=arm_w, arm_len=arm_len, height=height)
    assert result.val().Volume() < solid_vol


def test_volume_positive():
    result = make_l_bracket()
    assert result.val().Volume() > 0


def test_custom_params_produce_valid_bracket():
    result = make_l_bracket(arm_w=30, arm_len=65, height=5)
    assert result.val().isValid()
