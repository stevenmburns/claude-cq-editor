import cadquery as cq

# --- Parameters ---
body_r = 30       # outer radius of the cylindrical body
body_h = 60       # total height
wall_t = 3        # shell wall thickness
flange_r = 42     # flange outer radius
flange_h = 6      # flange thickness
flange_holes = 6  # number of bolt holes on flange
bolt_r = 3        # bolt hole radius
bolt_pcd = 36     # bolt hole pitch circle diameter
neck_r = 12       # port neck radius
neck_h = 18       # port neck height
chamfer_e = 1.5   # chamfer size on port lip

# --- Revolve profile: cylindrical body with flange base ---
# Profile is drawn in the XZ plane (X=radius, Z=height), then revolved around Z
profile = (
    cq.Workplane("XZ")
    .moveTo(0, 0)
    .lineTo(flange_r, 0)               # flange bottom
    .lineTo(flange_r, flange_h)        # flange outer edge
    .lineTo(body_r, flange_h)          # step down to body
    .lineTo(body_r, body_h)            # body wall
    .lineTo(neck_r, body_h)            # shoulder to neck
    .lineTo(neck_r, body_h + neck_h)   # neck
    .lineTo(0, body_h + neck_h)        # close to axis
    .close()
    .revolve(360, (0, 0, 0), (0, 1, 0))
)

# --- Shell: hollow out the body, open at the top of the neck ---
body = profile.faces(">Z").shell(-wall_t)

# --- Bolt holes on flange, arranged in a polar pattern ---
body = (
    body
    .faces("<Z")
    .workplane()
    .polarArray(bolt_pcd / 2, 0, 360, flange_holes)
    .hole(bolt_r * 2)
)


cq.exporters.export(body, "mechanical_test.stl", tolerance=0.01, angularTolerance=0.1)
print("Exported mechanical_test.stl")
