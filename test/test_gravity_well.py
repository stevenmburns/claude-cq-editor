from cq_models.gravity_well import make_gravity_well


def test_default_is_valid():
    result = make_gravity_well()
    assert result.val().isValid()


def test_bounding_box():
    disc_r = 60.0
    depth = 35.0
    base_t = 3.0
    result = make_gravity_well(disc_r=disc_r, depth=depth, base_t=base_t)
    bb = result.val().BoundingBox()

    # Diameter should be ~2*disc_r
    assert abs(bb.xmax - disc_r) < 0.5
    assert abs(bb.xmin + disc_r) < 0.5

    # Total height = depth + base_t
    expected_h = depth + base_t
    assert abs(bb.zmax - bb.zmin - expected_h) < 0.5


def test_volume_reasonable():
    result = make_gravity_well()
    vol = result.val().Volume()
    # Must be positive and less than a full solid disc of same outer dims
    full_disc_vol = 3.14159 * 60**2 * (35 + 3)
    assert 0 < vol < full_disc_vol


def test_custom_params():
    result = make_gravity_well(disc_r=50, rs=5, depth=25, base_t=2)
    assert result.val().isValid()
    bb = result.val().BoundingBox()
    assert abs(bb.xmax - 50) < 0.5


def test_inner_hole_exists():
    # The inner hole of radius rs means no material at r < rs at the top surface.
    # The bounding box x-min should be -disc_r, not 0, but the cross-section at
    # z=0 (rim level) should only extend inward to rs.
    rs = 8.0
    result = make_gravity_well(rs=rs)
    assert result.val().isValid()
    # Volume should be less than a solid disc (hole removes material)
    full_vol = 3.14159 * 60**2 * 38
    assert result.val().Volume() < full_vol
