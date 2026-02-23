import cadquery as cq


def make_u_cutter(height=3, body_w=10, body_d=5, slot_w=5, base_d=2):
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
    body = (
        cq.Workplane("XY")
        .moveTo(0, 0)
        .rect(body_w, body_d)
        .extrude(height)
    )
    slot = (
        cq.Workplane("XY")
        .moveTo(0, -base_d / 2)
        .rect(slot_w, body_d - base_d)
        .extrude(height)
    )
    wire_radius = 1.5

    extend_wire = 4

    wire_z = height

    slot_x = slot_w/2
    s_x = body_w/2 + extend_wire

    # the whole length, and then cut out the middle, because the first move doesn't seem to make any difference. FIX THIS: We don't understand the interface and this is a hack.
    path0 = cq.Workplane("XZ").moveTo(-s_x, wire_z).lineTo(s_x, wire_z)
    swept0 = cq.Workplane("YZ").moveTo(0, wire_z).circle(wire_radius).sweep(path0)

    path1 = cq.Workplane("XZ").moveTo(-slot_x, wire_z).lineTo(slot_x, wire_z)
    swept1 = cq.Workplane("YZ").moveTo(0, wire_z).circle(wire_radius).sweep(path1)

    path2 = cq.Workplane("XZ").moveTo(-slot_x, 0).lineTo(slot_x, 0)
    swept2 = cq.Workplane("YZ").moveTo(0, 0).circle(wire_radius).sweep(path2)

    return body.cut(slot).union(swept0.cut(swept1)).union(swept2) 


# show_object is injected by cq-editor; this guard displays the model
# in the GUI without building it on plain import or test runs.
if "show_object" in dir():
    show_object(make_u_cutter())

def main():
    result = make_u_cutter()
    cq.exporters.export(result, "u_cutter.stl")

if __name__ == "__main__":
    main()
