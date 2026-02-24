import cadquery as cq

from cq_models.u_cutter import make_u_cutter


def make_bracket(
    outer=60,
    inner=40,
    height=3,
    body_w=10,
    body_d=8,
    slot_w=5,
    base_d=2,
    cut_offset=10,
    n_cuts=2,
    loop_offset=5,
    fillet_r=3,
    roundover_r=1,
):
    """Parametric L-bracket with U-slot cuts.

    Args:
        outer: outer square side length (mm)
        inner: inner cutout side length (mm)
        height: bracket thickness (mm)
        body_w: U-cutter width along arm (mm)
        body_d: depth of cut into arm (mm)
        slot_w: slot opening width (mm)
        base_d: U base thickness — closed end of U (mm)
        cut_offset: offset of cut from inner edge of each arm (mm)
        n_cuts: number of U-cuts per arm, equally spaced along the arm
        loop_offset: distance the loop center is set back from the outer corner of the bracket (mm)
        fillet_r: fillet radius on vertical corners (mm)
        roundover_r: fillet radius on top/bottom face edges (mm), must be < height/2
    """
    outer_body = (
        cq.Workplane("XY")
        .moveTo(outer / 2, outer / 2)
        .rect(outer, outer)
        .extrude(height)
        .edges("|Z")
        .fillet(fillet_r)
    )

    inner_body = (
        cq.Workplane("XY")
        .moveTo(inner / 2, inner / 2)
        .rect(inner, inner)
        .extrude(height)
    )

    bracket = outer_body.cut(inner_body)

    for pt in [(inner, inner, height / 2), (inner, 0, height / 2), (0, inner, height / 2)]:
        bracket = bracket.edges(cq.selectors.NearestToPointSelector(pt)).fillet(fillet_r)



    # Add loop on end
    loop_cx = outer - loop_offset
    loop_cy = outer - loop_offset

    loop_body = (
        cq.Workplane("XY")
        .moveTo(loop_cx, loop_cy)
        .circle(10)
        .extrude(height)
    )

    loop_cut = (
        cq.Workplane("XY")
        .moveTo(loop_cx, loop_cy)
        .circle(6)
        .extrude(height)
    )

    bracket = bracket.union(loop_body).cut(loop_cut)

    for face_sel in [">Z", "<Z"]:
        bracket = bracket.faces(face_sel).edges().fillet(roundover_r)

    for i in range(n_cuts):
        x = (i + 0.75) * outer / (n_cuts + 1)
        bracket = bracket.cut(
            make_u_cutter(height, body_w, body_d, slot_w, base_d)
            .translate((x, inner + cut_offset, 0))
        )

    for i in range(n_cuts):
        y = (i + 0.75) * outer / (n_cuts + 1)
        bracket = bracket.cut(
            make_u_cutter(height, body_w, body_d, slot_w, base_d)
            .rotate((0, 0, 0), (0, 0, 1), -90)
            .translate((inner + cut_offset, y, 0))
        )

    return bracket


# show_object is injected by cq-editor; this guard displays the model
# in the GUI without building it on plain import or test runs.
if "show_object" in dir():
    show_object(make_bracket())


def main():
    result = make_bracket()
    cq.exporters.export(result, "bracket.stl")


if __name__ == "__main__":
    main()
