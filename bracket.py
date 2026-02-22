import cadquery as cq

# --- Bracket parameters ---
OUTER  = 60   # outer square side length (mm)
INNER  = 40   # inner cutout side length (mm)
HEIGHT =  3   # bracket thickness (mm)

# --- U-cutter parameters ---
BODY_W = 10   # overall cutter width (along arm)
BODY_D =  5   # depth of cut into arm
SLOT_W =  5   # slot opening width
BASE_D =  1   # U base thickness (closed end of U)

# Offset of cut from the inner edge of each arm
CUT_OFFSET = 10

# --- Bracket body ---
outer = (
    cq.Workplane("XY")
    .moveTo(OUTER / 2, OUTER / 2)
    .rect(OUTER, OUTER)
    .extrude(HEIGHT)
)

inner = (
    cq.Workplane("XY")
    .moveTo(INNER / 2, INNER / 2)
    .rect(INNER, INNER)
    .extrude(HEIGHT)
)

bracket = outer.cut(inner)

# --- U-cutter reference body ---
# Built at origin: centered in X, open face at y=0, extends in +Y
def make_u_cutter():
    body = (cq.Workplane("XY")
            .moveTo(0, BODY_D / 2)
            .rect(BODY_W, BODY_D)
            .extrude(HEIGHT))
    slot = (cq.Workplane("XY")
            .moveTo(0, (BODY_D - BASE_D) / 2)
            .rect(SLOT_W, BODY_D - BASE_D)
            .extrude(HEIGHT))
    return body.cut(slot)

# Top arm: centered at x=OUTER/2, open face at y=INNER+CUT_OFFSET
top_cutter = make_u_cutter().translate((OUTER / 2, INNER + CUT_OFFSET, 0))

# Right arm: rotate -90° around Z (open face now points in +X), then position
right_cutter = (make_u_cutter()
                .rotate((0, 0, 0), (0, 0, 1), -90)
                .translate((INNER + CUT_OFFSET, INNER / 2, 0)))

result = bracket.cut(top_cutter).cut(right_cutter)

cq.exporters.export(result, "bracket.stl")
