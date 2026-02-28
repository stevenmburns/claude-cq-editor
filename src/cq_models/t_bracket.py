import cadquery as cq

from cq_models.u_cutter import make_u_cutter


def make_t_bracket(
    arm_w=16,
    arm_len=60,
    height=3,
    body_w=10,
    body_d=9,
    slot_w=5,
    base_d=2.5,
    n_cuts=2,
    start_offset=20,
    end_offset=15,
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
        n_cuts: number of U-cuts per arm
        start_offset: distance from arm origin (junction) to center of first cut (mm)
        end_offset: distance from arm tip to center of last cut (mm)
        loop_offset: distance the loop center is set back from the bottom of the bar (mm)
        fillet_r: fillet radius on vertical corners (mm)
        roundover_r: fillet radius on top/bottom face edges (mm), must be < height/2
    """

    # Origin = intersection of bar and stem centrelines.
    # Horizontal bar: x: -arm_len → +arm_len, y: -arm_w/2 → +arm_w/2
    h_bar = cq.Workplane("XY").rect(2 * arm_len, arm_w).extrude(height)

    # Vertical stem: x: -arm_w/2 → +arm_w/2, y: +arm_w/2 → +arm_w/2 + arm_len
    v_stem = (
        cq.Workplane("XY")
        .moveTo(0, arm_w / 2 + arm_len / 2)
        .rect(arm_w, arm_len)
        .extrude(height)
    )

    bracket = h_bar.union(v_stem).edges("|Z").fillet(fillet_r)

    # Loop at the bottom of the horizontal bar, opposite the stem
    loop_body = (
        cq.Workplane("XY").moveTo(0, loop_offset - arm_w / 2).circle(10).extrude(height)
    )
    loop_cut = (
        cq.Workplane("XY").moveTo(0, loop_offset - arm_w / 2).circle(6).extrude(height)
    )

    bracket = bracket.union(loop_body).cut(loop_cut)

    for face_sel in [">Z", "<Z"]:
        bracket = bracket.faces(face_sel).edges().fillet(roundover_r)

    pitch = (arm_len - start_offset - end_offset) / (n_cuts - 1) if n_cuts > 1 else 0

    # U-cuts on left horizontal arm (x: -arm_len → 0, centred in y at 0)
    for i in range(n_cuts):
        x = -(start_offset + i * pitch)
        bracket = bracket.cut(
            make_u_cutter(height, body_w, body_d, slot_w, base_d).translate((x, 0, 0))
        )

    # U-cuts on right horizontal arm (x: 0 → +arm_len, centred in y at 0)
    for i in range(n_cuts):
        x = start_offset + i * pitch
        bracket = bracket.cut(
            make_u_cutter(height, body_w, body_d, slot_w, base_d).translate((x, 0, 0))
        )

    # U-cuts on vertical stem arm (y: arm_w/2 → arm_w/2 + arm_len, centred in x at 0)
    # Rotate -90° around Z so body_w runs along Y and body_d runs along X
    for i in range(n_cuts):
        y = arm_w / 2 + start_offset + i * pitch
        bracket = bracket.cut(
            make_u_cutter(height, body_w, body_d, slot_w, base_d)
            .rotate((0, 0, 0), (0, 0, 1), -90)
            .translate((0, y, 0))
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
