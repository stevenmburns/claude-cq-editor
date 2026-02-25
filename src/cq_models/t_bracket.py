import cadquery as cq

from cq_models.u_cutter import make_u_cutter


def make_t_bracket(
    arm_w=16,
    arm_len=60,
    height=3,
    body_w=10,
    body_d=8,
    slot_w=5,
    base_d=2,
    n_cuts=2,
    loop_offset=0,
    fillet_r=3,
    roundover_r=1,
):
    """Parametric T-bracket with U-slot cuts on each of the three arms.

    The T is oriented with a horizontal bar at the base and a vertical stem
    rising from the center.  Three arm ends: left, right, and top.

    Args:
        arm_w: width (thickness) of each arm (mm)
        arm_len: length of each arm from the centre junction (mm)
        height: bracket thickness (mm)
        body_w: U-cutter width along arm (mm)
        body_d: depth of cut into arm (mm)
        slot_w: slot opening width (mm)
        base_d: U base thickness — closed end of U (mm)
        n_cuts: number of U-cuts per arm, equally spaced along each arm
        loop_offset: distance the loop center is set back from the bottom of the bar (mm)
        fillet_r: fillet radius on vertical corners (mm)
        roundover_r: fillet radius on top/bottom face edges (mm), must be < height/2
    """

    # Horizontal bar: 2×arm_len wide × arm_w tall
    h_bar = (
        cq.Workplane("XY")
        .moveTo(arm_len, arm_w / 2)
        .rect(2 * arm_len, arm_w)
        .extrude(height)
    )

    # Vertical stem: arm_w wide, arm_len tall, centred on the bar
    v_stem = (
        cq.Workplane("XY")
        .moveTo(arm_len, arm_w + arm_len / 2)
        .rect(arm_w, arm_len)
        .extrude(height)
    )

    bracket = h_bar.union(v_stem).edges("|Z").fillet(fillet_r)

    # Loop at the bottom of the horizontal bar, opposite the stem
    loop_cx = arm_len
    loop_cy = loop_offset

    loop_body = cq.Workplane("XY").moveTo(loop_cx, loop_cy).circle(10).extrude(height)
    loop_cut = cq.Workplane("XY").moveTo(loop_cx, loop_cy).circle(6).extrude(height)

    bracket = bracket.union(loop_body).cut(loop_cut)

    for face_sel in [">Z", "<Z"]:
        bracket = bracket.faces(face_sel).edges().fillet(roundover_r)

    # U-cuts on left horizontal arm (x: 0 → arm_len, centred in y at arm_w/2)
    for i in range(n_cuts):
        x = (i + 1) * arm_len / (n_cuts + 1)
        bracket = bracket.cut(
            make_u_cutter(height, body_w, body_d, slot_w, base_d).translate(
                (x, arm_w / 2, 0)
            )
        )

    # U-cuts on right horizontal arm (x: arm_len → 2×arm_len, centred in y at arm_w/2)
    for i in range(n_cuts):
        x = arm_len + (i + 1) * arm_len / (n_cuts + 1)
        bracket = bracket.cut(
            make_u_cutter(height, body_w, body_d, slot_w, base_d).translate(
                (x, arm_w / 2, 0)
            )
        )

    # U-cuts on vertical stem arm (y: arm_w → arm_w + arm_len, centred in x at arm_len)
    # Rotate -90° around Z so body_w runs along Y and body_d runs along X
    for i in range(n_cuts):
        y = arm_w + (i + 1) * arm_len / (n_cuts + 1)
        bracket = bracket.cut(
            make_u_cutter(height, body_w, body_d, slot_w, base_d)
            .rotate((0, 0, 0), (0, 0, 1), -90)
            .translate((arm_len, y, 0))
        )

    return bracket


# show_object is injected by cq-editor; this guard displays the model
# in the GUI without building it on plain import or test runs.
if "show_object" in dir():
    show_object(make_t_bracket())  # noqa: F821


def main():
    result = make_t_bracket()
    cq.exporters.export(result, "t_bracket.stl")


if __name__ == "__main__":
    main()
