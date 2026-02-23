import cadquery as cq


def make_u_cutter(height=3, body_w=10, body_d=5, slot_w=5, base_d=1):
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
    return body.cut(slot)


# show_object is injected by cq-editor; this guard displays the model
# in the GUI without building it on plain import or test runs.
if "show_object" in dir():
    show_object(make_u_cutter())
