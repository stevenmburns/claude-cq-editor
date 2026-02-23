import cadquery as cq

from cq_models.u_cutter import make_u_cutter


def make_bracket(
    outer=60,
    inner=40,
    height=3,
    body_w=10,
    body_d=5,
    slot_w=5,
    base_d=1,
    cut_offset=10,
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
    """
    outer_body = (
        cq.Workplane("XY")
        .moveTo(outer / 2, outer / 2)
        .rect(outer, outer)
        .extrude(height)
    )

    inner_body = (
        cq.Workplane("XY")
        .moveTo(inner / 2, inner / 2)
        .rect(inner, inner)
        .extrude(height)
    )

    bracket = outer_body.cut(inner_body)

    top_cutter = (
        make_u_cutter(height, body_w, body_d, slot_w, base_d)
        .translate((outer / 2, inner + cut_offset + body_d / 2, 0))
    )
    right_cutter = (
        make_u_cutter(height, body_w, body_d, slot_w, base_d)
        .rotate((0, 0, 0), (0, 0, 1), -90)
        .translate((inner + cut_offset + body_d / 2, inner / 2, 0))
    )

    return bracket.cut(top_cutter).cut(right_cutter)


# show_object is injected by cq-editor; this guard displays the model
# in the GUI without building it on plain import or test runs.
if "show_object" in dir():
    show_object(make_bracket())


def main():
    result = make_bracket()
    cq.exporters.export(result, "bracket.stl")


if __name__ == "__main__":
    main()
