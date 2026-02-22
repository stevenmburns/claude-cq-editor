import cadquery as cq

# A simple parametric box with a counterbored hole and filleted edges
result = (
    cq.Workplane("XY")
    .box(60, 40, 20)
    .faces(">Z")
    .workplane()
    .cboreHole(diameter=8, cboreDiameter=14, cboreDepth=6)
    .edges("|Z")
    .fillet(4)
)

cq.exporters.export(result, "test_model.stl", tolerance=0.01, angularTolerance=0.1)
print("Exported test_model.stl")
