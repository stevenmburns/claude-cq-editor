import cadquery as cq


def make_gravity_well(
    disc_r=60.0,
    well_r=40.0,
    depth=15.0,
    base_t=3.0,
    n_pts=50,
):
    """Gravity well — disc with a parabolic central depression.

    Models the classic rubber-sheet analogy used to visualise spacetime
    curvature in general relativity.  A flat disc of radius disc_r has a
    smooth parabolic funnel of radius well_r depressed depth mm below
    the flat rim surface.

    Args:
        disc_r: overall disc radius (mm)
        well_r: radius of the parabolic funnel (mm), must be < disc_r
        depth: funnel depth at centre (mm)
        base_t: solid floor thickness under the funnel (mm)
        n_pts: number of spline points on the funnel curve
    """
    d = depth
    wr = well_r

    # Parabolic funnel: z(r) = -d*(1 - (r/wr)^2), r in [0, wr]
    # At r=0 → z=-d;  at r=wr → z=0
    r_step = wr / (n_pts - 1)
    funnel_pts = [
        (i * r_step, -d * (1 - (i * r_step / wr) ** 2)) for i in range(1, n_pts)
    ]

    # Closed profile in the XZ plane (local x = radial, local y = world Z).
    # Revolved 360° around the world Z axis (local (0,0)→(0,1)).
    profile = (
        cq.Workplane("XZ")
        .moveTo(0, -d)  # funnel centre (deepest point)
        .spline(funnel_pts)  # parabolic curve up to funnel rim
        .lineTo(disc_r, 0)  # flat annular top surface
        .lineTo(disc_r, -(d + base_t))  # outer wall
        .lineTo(0, -(d + base_t))  # flat bottom
        .close()  # up the central axis back to start
    )

    return profile.revolve(360, (0, 0), (0, 1))


# show_object is injected by cq-editor; this guard displays the model
# in the GUI without building it on plain import or test runs.
if "show_object" in dir():
    show_object(make_gravity_well())  # noqa: F821


def main():
    result = make_gravity_well()
    cq.exporters.export(
        result,
        "gravity_well.stl",
        exportType="STL",
        tolerance=0.001,
        angularTolerance=0.1,
    )
    print("Exported gravity_well.stl")


if __name__ == "__main__":
    main()
