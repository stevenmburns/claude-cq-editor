from cq_models.u_cutter import make_u_cutter


def test_default_u_cutter_is_valid():
    result = make_u_cutter()
    assert result.val().isValid()


def test_bounding_box_matches_params():
    result = make_u_cutter(height=3, body_w=10, body_d=5)
    bb = result.val().BoundingBox()
    assert abs(bb.xlen - 10) < 0.1
    assert abs(bb.ylen - 5) < 0.1
    assert abs(bb.zlen - 3) < 0.1


def test_volume_less_than_solid():
    height, body_w, body_d = 3, 10, 5
    solid_vol = body_w * body_d * height
    result = make_u_cutter(height=height, body_w=body_w, body_d=body_d)
    assert result.val().Volume() < solid_vol


def test_custom_params_produce_valid_cutter():
    result = make_u_cutter(height=5, body_w=15, body_d=8, slot_w=6, base_d=2)
    assert result.val().isValid()
