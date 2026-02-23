import cadquery as cq


def make_u_cutter(height=3, body_w=10, body_d=5, slot_w=5, base_d=1, y_offset=2.5):
    """U-shaped cutter profile, open face at y=-y_offset, extending in +Y.

    The origin sits y_offset above the open face, so y=0 is y_offset into
    the body from the opening. Default y_offset=2.5 places the origin at
    the midpoint of body_d=5.

    Args:
        height: extrusion height (mm)
        body_w: overall cutter width (mm)
        body_d: depth of cut into arm (mm)
        slot_w: slot opening width (mm)
        base_d: U base thickness — closed end of U (mm)
        y_offset: distance from open face to origin (mm)
    """
    body = (
        cq.Workplane("XY")
        .moveTo(0, body_d / 2)
        .rect(body_w, body_d)
        .extrude(height)
    )
    slot = (
        cq.Workplane("XY")
        .moveTo(0, (body_d - base_d) / 2)
        .rect(slot_w, body_d - base_d)
        .extrude(height)
    )
    return body.cut(slot).translate((0, -y_offset, 0))


# show_object is injected by cq-editor; this guard displays the model
# in the GUI without building it on plain import or test runs.
if "show_object" in dir():
    show_object(make_u_cutter())
