from cq_models.u_cutter import make_u_cutter


def test_default_u_cutter_is_valid():
    result = make_u_cutter()
    assert result.val().isValid()


def test_bounding_box_matches_params():
    height, body_w, body_d = 3, 10, 9
    extend_wire, wire_radius = 4, 1.5
    result = make_u_cutter(height=height, body_w=body_w, body_d=body_d)
    bb = result.val().BoundingBox()
    # wire arms extend extend_wire past each side of body_w
    assert abs(bb.xlen - (body_w + 2 * extend_wire)) < 0.1
    assert abs(bb.ylen - body_d) < 0.1
    # wire arms at top (z=height+wire_radius) and bottom (z=-wire_radius)
    assert abs(bb.zlen - (height + 2 * wire_radius)) < 0.1


def test_volume_positive():
    result = make_u_cutter()
    assert result.val().Volume() > 0


def test_custom_params_produce_valid_cutter():
    result = make_u_cutter(height=5, body_w=15, body_d=8, slot_w=6, base_d=2)
    assert result.val().isValid()
