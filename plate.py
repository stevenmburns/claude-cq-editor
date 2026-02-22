import cadquery as cq

# --- Parameters ---
plate_length = 50.0    # mm, X dimension
plate_width  = 50.0    # mm, Y dimension
plate_height = 4.0     # mm, thickness

corner_radius   = 8.0   # mm
hole_diameter   = 12.0  # mm

# --- Model ---
result = (
    cq.Workplane("XY")
    .box(plate_length, plate_width, plate_height)
    .edges("|Z")                    # the 4 vertical corner edges
    .fillet(corner_radius)
    .faces(">Z")
    .workplane()
    .hole(hole_diameter)
)

# Export to STL
cq.exporters.export(result, "plate.stl")
