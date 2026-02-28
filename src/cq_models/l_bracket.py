import math

import cadquery as cq


def make_l_bracket(
    arm_w=16,
    arm_len=60,
    height=3,
    body_w=10,
    body_d=8,
    slot_w=5,
    base_d=2,
    n_cuts=2,
    start_offset=20,
    end_offset=15,
    loop_offset=5,
    fillet_r=3,
    roundover_r=1,
    arm_angle=90,
):
    """Parametric L-bracket with U-slot cuts.

    Origin is at the intersection of the two arm centrelines (centre of the
    corner junction).  The first arm extends along +X; the second arm extends
    at arm_angle degrees CCW from +X.  Each arm extends arm_len from the origin
    and arm_w/2 in the opposite direction to form the corner junction.

    Args:
        arm_w: width (thickness) of each arm (mm)
        arm_len: length of each arm from the centre junction to its tip (mm)
        height: bracket thickness (mm)
        body_w: U-cutter width along arm (mm)
        body_d: depth of cut into arm (mm)
        slot_w: slot opening width (mm)
        base_d: U base thickness — closed end of U (mm)
        n_cuts: number of U-cuts per arm
        start_offset: distance from arm origin (junction) to center of first cut (mm)
        end_offset: distance from arm tip to center of last cut (mm)
        loop_offset: distance the loop center is set back from the outer corner (mm)
        fillet_r: fillet radius on vertical corners (mm)
        roundover_r: fillet radius on top/bottom face edges (mm), must be < height/2
        arm_angle: angle between the two arms in degrees (default 90)
    """
    arm_angle_rad = math.radians(arm_angle)

    # Arm slab: x: 0 → +arm_len, y: -arm_w/2 → +arm_w/2
    def _arm_slab():
        return (
            cq.Workplane("XY")
            .moveTo(arm_len / 2, 0)
            .rect(arm_len, arm_w)
            .extrude(height)
        )

    h_arm = _arm_slab()
    v_arm = _arm_slab().rotate((0, 0, 0), (0, 0, 1), arm_angle)
    disk = cq.Workplane("XY").circle(arm_w / 2).extrude(height)

    from cq_models.u_cutter import make_u_cutter

    bracket = h_arm.union(v_arm).union(disk)
    bracket = bracket.edges("|Z").fillet(fillet_r)

    # Loop at the outer corner of the junction (along the exterior bisector)
    bisector_rad = math.radians(arm_angle / 2)
    loop_dist = math.sqrt(2) * (arm_w / 2 - loop_offset)
    loop_cx = -loop_dist * math.cos(bisector_rad)
    loop_cy = -loop_dist * math.sin(bisector_rad)

    loop_body = cq.Workplane("XY").moveTo(loop_cx, loop_cy).circle(10).extrude(height)
    loop_cut = cq.Workplane("XY").moveTo(loop_cx, loop_cy).circle(6).extrude(height)
    bracket = bracket.union(loop_body).cut(loop_cut)

    for face_sel in [">Z", "<Z"]:
        bracket = bracket.faces(face_sel).edges().fillet(roundover_r)

    pitch = (arm_len - start_offset - end_offset) / (n_cuts - 1) if n_cuts > 1 else 0

    # U-cuts on horizontal arm (+X direction)
    for i in range(n_cuts):
        x = start_offset + i * pitch
        bracket = bracket.cut(
            make_u_cutter(height, body_w, body_d, slot_w, base_d).translate((x, 0, 0))
        )

    # U-cuts on second arm (along arm_angle direction)
    for i in range(n_cuts):
        d = start_offset + i * pitch
        tx = d * math.cos(arm_angle_rad)
        ty = d * math.sin(arm_angle_rad)
        bracket = bracket.cut(
            make_u_cutter(height, body_w, body_d, slot_w, base_d)
            .rotate((0, 0, 0), (0, 0, 1), arm_angle)
            .translate((tx, ty, 0))
        )

    return bracket


# show_object is injected by cq-editor; this guard displays the model
# in the GUI without building it on plain import or test runs.
if "show_object" in dir():
    show_object(make_l_bracket())  # noqa: F821


def main():
    import argparse

    p = argparse.ArgumentParser(description="Export an L-bracket STL")
    p.add_argument(
        "--arm-angle",
        type=float,
        default=90,
        help="Angle between arms in degrees (default: 90)",
    )
    p.add_argument(
        "--arm-len",
        type=float,
        default=60,
        help="Arm length from junction to tip in mm (default: 60)",
    )
    p.add_argument(
        "--arm-w",
        type=float,
        default=16,
        help="Arm width/thickness in mm (default: 16)",
    )
    p.add_argument(
        "--height", type=float, default=3, help="Bracket thickness in mm (default: 3)"
    )
    p.add_argument(
        "--n-cuts", type=int, default=2, help="Number of U-cuts per arm (default: 2)"
    )
    p.add_argument(
        "--output",
        default="l_bracket.stl",
        help="Output STL filename (default: l_bracket.stl)",
    )
    args = p.parse_args()

    result = make_l_bracket(
        arm_angle=args.arm_angle,
        arm_len=args.arm_len,
        arm_w=args.arm_w,
        height=args.height,
        n_cuts=args.n_cuts,
    )
    cq.exporters.export(result, args.output)
    print(f"Exported {args.output}")


if __name__ == "__main__":
    main()
