# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Purpose

This repository is a Python package (`cq-models`) for generating 3D-printable STL models using CadQuery / CQ-editor. The workflow is: implement a model as a function in `src/cq_models/`, iterate visually in CQ-editor's GUI, run `pytest` to validate geometry, then export to STL for printing.

## Project Structure

```
src/cq_models/       # installable package
    bracket.py       # make_bracket() + 'bracket' CLI entry point
    u_cutter.py      # make_u_cutter() reusable component with swept wire-retention arms
test/
    test_bracket.py  # pytest geometry tests
    test_u_cutter.py # pytest geometry tests
pyproject.toml       # setuptools config, entry points, dev deps
```

## Installation

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install cq-editor
pip install -e ".[dev]"   # installs the package + pytest
```

**STL renderers** (system packages, not in venv):
```bash
sudo apt install f3d
sudo apt install flatpak
flatpak remote-add --if-not-exists flathub https://dl.flathub.org/repo/flathub.flatpakrepo
sudo flatpak install flathub net.meshlab.MeshLab
```

## Environment Setup

All commands must be run with the virtual environment active:
```bash
source .venv/bin/activate
```

Or invoke directly without activating:
```bash
.venv/bin/bracket
.venv/bin/cq-editor src/cq_models/bracket.py
```

## Running and Exporting

**CQ-editor GUI** (recommended for iterating):
```bash
cq-editor src/cq_models/bracket.py
```

**Export to STL** (via CLI entry point):
```bash
bracket
```

**Run tests:**
```bash
pytest
```

**Export to STL from within a module:**
```python
import cadquery as cq
result = cq.Workplane("XY").box(10, 10, 10)
cq.exporters.export(result, "output.stl")
```

CQ-editor also has File → Export STL directly from the GUI.

## Adding a New Model

1. Create `src/cq_models/<name>.py` with a `make_<name>(**params)` function and a `main()` that calls it and exports STL
2. Add a `[project.scripts]` entry in `pyproject.toml`: `<name> = "cq_models.<name>:main"`
3. Re-run `pip install -e ".[dev]"` to register the new entry point
4. Add `test/test_<name>.py` with geometry assertions (`isValid()`, bounding box, volume)

## Testing

Models are tested by asserting on the CadQuery solid's geometric properties — no visual comparison needed:

```python
from cq_models.bracket import make_bracket

def test_valid():
    assert make_bracket().val().isValid()

def test_bbox():
    bb = make_bracket(outer=60, height=3).val().BoundingBox()
    # bracket has a loop at (outer, outer) with radius 10, so xlen/ylen = outer + 10
    assert abs(bb.xlen - 70) < 0.1
    assert abs(bb.zlen - 3) < 0.1
```

Useful properties to assert on: `isValid()`, `BoundingBox()` (xlen/ylen/zlen), `Volume()`.

## Slicing and Printing

**OrcaSlicer** is installed as an AppImage at `~/OrcaSlicer.AppImage` (v2.3.1, Ubuntu 24.04 build).

**Printer:** Elegoo Centauri Carbon at `192.168.1.38` (WiFi). Connect via OrcaSlicer GUI or use the headless CLI below.

**Headless slicing** (mount the AppImage to access bundled profiles, then slice):
```bash
~/OrcaSlicer.AppImage --appimage-mount &
MPID=$! ; sleep 5
MOUNT=$(ls -d /tmp/.mount_OrcaSl* | head -1)

DISPLAY= ~/OrcaSlicer.AppImage \
  --load-settings "$MOUNT/resources/profiles/Elegoo/machine/ECC/Elegoo Centauri Carbon 0.4 nozzle.json;$MOUNT/resources/profiles/Elegoo/process/ECC/0.20mm Standard @Elegoo CC 0.4 nozzle.json" \
  --load-filaments "$MOUNT/resources/profiles/Elegoo/filament/EC/Elegoo PETG PRO @EC.json" \
  --slice 0 \
  --outputdir /tmp/orca_out \
  model.stl

kill $MPID
```

Other available process profiles (in `$MOUNT/resources/profiles/Elegoo/process/ECC/`):
- `0.12mm Fine @Elegoo CC 0.4 nozzle.json` — fine detail
- `0.20mm Standard @Elegoo CC 0.4 nozzle.json` — general use
- `0.24mm Draft @Elegoo CC 0.4 nozzle.json` — fast prototyping

Other filaments (in `$MOUNT/resources/profiles/Elegoo/filament/EC/`):
- `Elegoo PLA @EC.json`
- `Elegoo PETG PRO @EC.json`
- `Elegoo ASA @EC.json`

**Render G-code preview to check stats:**
```bash
grep "estimated\|filament used" output.gcode
```

## Rendering STL Files

**F3D** — fast viewer, use for quick inspection:
```bash
f3d output.stl
```
- Left-click drag to rotate, scroll to zoom
- Render to PNG: `f3d --output render.png output.stl`

**MeshLab** — mesh inspection and repair (installed via Flatpak):
```bash
flatpak run net.meshlab.MeshLab output.stl
```

## CadQuery Core Concepts

### The Fluent API Pattern

Every model starts with a `Workplane` and chains operations. The result of each method is a new `Workplane` (or the modified solid), enabling jQuery-style chaining:

```python
import cadquery as cq

result = (
    cq.Workplane("XY")
    .box(30, 20, 10)
    .faces(">Z")
    .hole(5)
    .edges("|Z")
    .fillet(1)
)
```

### Workplane Initialization

- `"XY"` — builds upward along Z (most common)
- `"XZ"` — builds outward along Y
- `"YZ"` — builds outward along X

### Common 3D Operations

| Method | Description |
|--------|-------------|
| `box(l, w, h)` | Rectangular solid centered at origin |
| `cylinder(height, radius)` | Cylinder |
| `sphere(radius)` | Sphere |
| `extrude(distance)` | Extrude a 2D sketch into 3D |
| `revolve(angleDegrees)` | Revolve a 2D profile around an axis |
| `loft()` | Loft between two wire profiles |
| `sweep(path)` | Sweep a profile along a path |
| `shell(thickness)` | Hollow out a solid |
| `fillet(radius)` | Round edges |
| `chamfer(length)` | Bevel edges |

### Boolean Operations

```python
result = body1.cut(body2)        # Subtract body2 from body1
result = body1.union(body2)      # Combine
result = body1.intersect(body2)  # Keep only overlap
```

Or use `.add()` to union into the current stack:
```python
result = cq.Workplane("XY").box(10,10,10).add(other_solid)
```

### Hole Operations

```python
.hole(diameter, depth)                        # Simple through or blind hole
.cboreHole(diameter, cboreDiameter, cboreDepth)  # Counterbore
.cskHole(diameter, cskDiameter, cskAngle)    # Countersink
```

### Polar and Rectangular Arrays

```python
# Polar: place features at equal angles around a circle
.polarArray(radius, startAngle, angle, count)

# Rectangular: grid of features
.rarray(xSpacing, ySpacing, xCount, yCount)
```

Both position the workplane at each point — chain `.hole()`, `.circle().extrude()`, etc. after.

### Revolve Profile Pattern

Draw the cross-section in the XZ plane (X = radius, Z = height), close it to the axis, then revolve around Y:

```python
profile = (
    cq.Workplane("XZ")
    .moveTo(0, 0)
    .lineTo(outerR, 0)
    .lineTo(outerR, height)
    .lineTo(0, height)
    .close()
    .revolve(360, (0, 0, 0), (0, 1, 0))
)
```

The profile must be closed and must not cross the axis of revolution.

### Sweep Profile Positioning

`moveTo()` on the profile Workplane only moves a 2D cursor — it does **not** set the profile's 3D position. Use the `origin` parameter on the Workplane constructor to place the profile at the correct world-space location:

```python
# Path along X at z=height
path = cq.Workplane("XZ").moveTo(-5, height).lineTo(5, height)

# Profile placed at the path's start point in world coordinates
swept = cq.Workplane("YZ", origin=(-5, 0, height)).circle(radius).sweep(path)
```

The `origin` tuple is `(world_x, world_y, world_z)` and must match the path's start point. For a path in "XZ" traveling along X, the profile plane is "YZ" and `origin[0]` selects the start X position.

### Shell Pattern

Select the face to open, then call `shell()` with a negative thickness to shell inward:

```python
body = solid.faces(">Z").shell(-wall_thickness)
```

Apply fillets/chamfers **before** `shell()` — shelling restructures edge topology and makes post-shell edge selection unreliable.

### 2D Sketch Operations (for extrude/revolve)

```python
cq.Workplane("XY")
  .lineTo(x, y)
  .line(dx, dy)      # relative
  .circle(r)
  .rect(w, h)
  .polyline([(x1,y1), (x2,y2), ...])
  .spline([(x1,y1), (x2,y2), ...])
  .threePointArc(midPt, endPt)
  .close()           # close the wire
  .extrude(depth)
```

## Selector String Syntax

Selectors are used with `.faces()`, `.edges()`, `.vertices()` to pick geometry for subsequent operations.

| Selector | Meaning |
|----------|---------|
| `">Z"` | Face/edge with highest Z center (top) |
| `"<Z"` | Face/edge with lowest Z center (bottom) |
| `">X"`, `"<X"`, `">Y"`, `"<Y"` | Max/min in that axis |
| `"+Z"` | Face whose normal points in +Z |
| `"-Z"` | Face whose normal points in -Z |
| `"\|Z"` | Edges parallel to Z axis |
| `"#Z"` | Edges/faces perpendicular to Z |
| `"%Plane"` | All planar faces |
| `"%Cylinder"` | All cylindrical faces |

Selectors can be combined:
```python
.edges(">Z and |X")   # Top edges that are also parallel to X
```

### Positioning New Features

After selecting a face, call `.workplane()` to set the construction plane there:
```python
result = (
    cq.Workplane("XY")
    .box(20, 20, 10)
    .faces(">Z")        # select top face
    .workplane()        # new workplane on top face
    .circle(5)
    .extrude(5)         # add a boss
)
```

## CQ-editor Script Structure

CQ-editor looks for a variable named `result` (or calls `show_object()`) to display geometry:

```python
import cadquery as cq

result = cq.Workplane("XY").box(10, 10, 10)

# Option 1: just assign to `result`
# Option 2: show multiple objects with labels
show_object(result, name="box")
show_object(other, name="other", options={"color": "red"})
```

`show_object()` is a CQ-editor builtin — not available in plain Python scripts.

## Assemblies (Multi-Part Models)

```python
import cadquery as cq
from cadquery import Assembly, Location, Vector

assy = Assembly()
assy.add(part1, loc=Location(Vector(0, 0, 0)), name="base")
assy.add(part2, loc=Location(Vector(0, 0, 10)), name="lid")
assy.export("assembly.step")   # STEP preserves assembly structure
```

## Typical Model Recipe

1. Create `src/cq_models/<name>.py` with a `make_<name>(**params)` function
2. Sketch the base profile on a named workplane inside the function
3. `extrude()` or `revolve()` into 3D
4. Select faces with string selectors and add/cut features
5. Apply `fillet()` or `chamfer()` before `shell()` (see Shell Pattern above)
6. Return the result; export in `main()` via `cq.exporters.export(result, "name.stl")`

## STL Export Settings

For 3D printing, angular tolerance and linear tolerance control mesh quality:
```python
cq.exporters.export(
    result,
    "output.stl",
    exportType="STL",
    tolerance=0.001,      # linear deflection (mm), smaller = finer mesh
    angularTolerance=0.1  # angular deflection (radians)
)
```

## Documentation

- Full docs: https://cadquery.readthedocs.io/
- API reference: https://cadquery.readthedocs.io/en/latest/apireference.html
- Example gallery: https://cadquery.readthedocs.io/en/latest/examples.html
