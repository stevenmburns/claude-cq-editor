import math

import cadquery as cq


def make_gravity_well(
    disc_r=60.0,
    rs=8.0,
    depth=35.0,
    base_t=3.0,
    n_pts=60,
):
    """Gravity well — Flamm's paraboloid disc with central event-horizon hole.

    Models the spacetime curvature embedding diagram used to visualise a
    black hole or massive star in general relativity.  The funnel profile
    follows a square-root (Flamm) curve that is nearly vertical at the inner
    edge rs (the "event horizon") and flares out to flat at disc_r.  A
    cylindrical hole of radius rs at the centre represents the region where
    the embedding breaks down.

    Profile: z(r) = -depth * (1 - sqrt((r - rs) / (disc_r - rs)))

    Args:
        disc_r: overall disc radius (mm)
        rs: event-horizon radius — inner hole radius and funnel base (mm)
        depth: funnel depth at the inner edge (mm)
        base_t: solid floor thickness under the funnel (mm)
        n_pts: spline resolution (more = smoother near the steep inner edge)
    """
    d = depth

    # Quadratic r-spacing concentrates points near rs where the slope is steepest.
    # r_vals runs from just above rs to disc_r (the moveTo provides the rs start).
    r_vals = [rs + (disc_r - rs) * (i / (n_pts - 1)) ** 2 for i in range(1, n_pts)]
    funnel_pts = [(r, -d * (1.0 - math.sqrt((r - rs) / (disc_r - rs)))) for r in r_vals]
    # funnel_pts[0]  ≈ (rs + ε, -depth + ε)  — near bottom of the well
    # funnel_pts[-1] = (disc_r, 0)            — flat outer rim

    # Closed profile in the XZ plane (local x = radial, local y = world Z).
    # Revolved 360° around world Z (local axis (0,0)→(0,1)).
    #
    # Shape cross-section (r increasing left → right):
    #
    #                              ___________  ← z=0  (outer flat rim)
    #   steep                    /
    #   inner  \________________/              ← Flamm curve
    #   wall   |                |
    #          |________________|              ← z=-(depth+base_t) flat floor
    #          rs               disc_r
    profile = (
        cq.Workplane("XZ")
        .moveTo(rs, -d)  # top of inner cylindrical wall
        .spline(funnel_pts)  # Flamm curve up to outer rim
        .lineTo(disc_r, -(d + base_t))  # outer wall down
        .lineTo(rs, -(d + base_t))  # flat floor inward
        .close()  # up the inner wall back to start
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
