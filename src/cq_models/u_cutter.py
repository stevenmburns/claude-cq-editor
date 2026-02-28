import cadquery as cq


def make_u_cutter(height=3, body_w=10, body_d=9, slot_w=5, base_d=2.5):
    """U-shaped cutter profile centered on the origin.

    The body is centered at y=0, so the open face is at y=-body_d/2
    and the closed end is at y=+body_d/2.

    Args:
        height: extrusion height (mm)
        body_w: overall cutter width (mm)
        body_d: depth of cut into arm (mm)
        slot_w: slot opening width (mm)
        base_d: U base thickness — closed end of U (mm)
    """
    body = cq.Workplane("XY").moveTo(0, 0).rect(body_w, body_d).extrude(height)
    slot = (
        cq.Workplane("XY")
        .moveTo(0, -base_d / 2)
        .rect(slot_w, body_d - base_d)
        .extrude(height)
    )
    wire_radius = 1.5
    extend_wire = 4
    wire_z = height
    slot_x = slot_w / 2
    s_x = body_w / 2 + extend_wire

    path_left = cq.Workplane("XZ").moveTo(-s_x, wire_z).lineTo(-slot_x, wire_z)
    path_right = cq.Workplane("XZ").moveTo(slot_x, wire_z).lineTo(s_x, wire_z)
    path_bot = cq.Workplane("XZ").moveTo(-slot_x, 0).lineTo(slot_x, 0)

    swept_left = (
        cq.Workplane("YZ", origin=(-s_x, 0, wire_z))
        .circle(wire_radius)
        .sweep(path_left)
    )
    swept_right = (
        cq.Workplane("YZ", origin=(slot_x, 0, wire_z))
        .circle(wire_radius)
        .sweep(path_right)
    )
    swept_bot = (
        cq.Workplane("YZ", origin=(-slot_x, 0, 0)).circle(wire_radius).sweep(path_bot)
    )

    return body.cut(slot).union(swept_left).union(swept_right).union(swept_bot)


# show_object is injected by cq-editor; this guard displays the model
# in the GUI without building it on plain import or test runs.
if "show_object" in dir():
    show_object(make_u_cutter())  # noqa: F821


def main():
    result = make_u_cutter()
    cq.exporters.export(result, "u_cutter.stl")


if __name__ == "__main__":
    main()
