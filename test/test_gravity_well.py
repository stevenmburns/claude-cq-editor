from cq_models.gravity_well import make_gravity_well


def test_default_is_valid():
    result = make_gravity_well()
    assert result.val().isValid()


def test_bounding_box():
    disc_r = 60.0
    depth = 15.0
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
    # Solid disc volume would be pi*60^2*(15+3) ≈ 203575 mm^3
    # With funnel removed it should be significantly less
    full_disc_vol = 3.14159 * 60**2 * 18
    assert 0 < vol < full_disc_vol


def test_custom_params():
    result = make_gravity_well(disc_r=40, well_r=25, depth=10, base_t=2)
    assert result.val().isValid()
    bb = result.val().BoundingBox()
    assert abs(bb.xmax - 40) < 0.5
