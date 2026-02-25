# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Purpose

Python package (`cq-models`) for generating 3D-printable STL models using CadQuery / CQ-editor. Workflow: implement a model in `src/cq_models/`, iterate visually in CQ-editor, run `pytest` to validate geometry, export to STL for printing.

## Project Structure

```
src/cq_models/
    l_bracket.py     # make_l_bracket() + 'l_bracket' CLI entry point
    t_bracket.py     # make_t_bracket() + 't_bracket' CLI entry point
    u_cutter.py      # make_u_cutter() reusable wire-retention component
test/
    test_l_bracket.py
    test_t_bracket.py
    test_u_cutter.py
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
flatpak install flathub net.meshlab.MeshLab
```

## Environment Setup

All commands must be run with the virtual environment active. Direct invocation (no activation needed):
```bash
.venv/bin/python -m pytest
.venv/bin/cq-editor src/cq_models/l_bracket.py
```

Note: venv shebangs embed absolute paths — if the project directory is renamed, fix with:
```bash
grep -rl 'OLD-DIR-NAME' .venv/bin/ | xargs sed -i 's|OLD-DIR-NAME|NEW-DIR-NAME|g'
```

## Running and Exporting

```bash
cq-editor src/cq_models/l_bracket.py   # open in GUI for visual iteration
.venv/bin/python -m pytest              # run geometry tests
.venv/bin/l_bracket                     # export l_bracket.stl
.venv/bin/t_bracket                     # export t_bracket.stl
```

CQ-editor displays geometry via `show_object()` (injected builtin) or a variable named `result`.

## Adding a New Model

1. Create `src/cq_models/<name>.py` with `make_<name>(**params)` and `main()` that exports STL
2. Add `[project.scripts]` entry in `pyproject.toml`: `<name> = "cq_models.<name>:main"`
3. Re-run `pip install -e ".[dev]"` to register the entry point
4. Add `test/test_<name>.py` asserting on `isValid()`, `BoundingBox()`, `Volume()`

## Testing

```bash
.venv/bin/python -m pytest -v
```

## Slicing and Printing

**OrcaSlicer** is installed as an AppImage at `~/OrcaSlicer.AppImage` (v2.3.1, Ubuntu 24.04 build).

**Printer:** Elegoo Centauri Carbon at `192.168.1.38` (WiFi).

**Headless slicing:**
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
grep "estimated\|filament used" /tmp/orca_out/plate_1.gcode
```

Process profiles (in `$MOUNT/resources/profiles/Elegoo/process/ECC/`):
- `0.12mm Fine`, `0.20mm Standard`, `0.24mm Draft` — all `@Elegoo CC 0.4 nozzle.json`

Filaments (in `$MOUNT/resources/profiles/Elegoo/filament/EC/`):
- `Elegoo PLA @EC.json`, `Elegoo PETG PRO @EC.json`, `Elegoo ASA @EC.json`

## Rendering STL Files

```bash
f3d output.stl                          # fast viewer
flatpak run net.meshlab.MeshLab output.stl
f3d --output render.png output.stl      # render to PNG
```

## STL Export Settings

```python
cq.exporters.export(result, "output.stl", exportType="STL",
                    tolerance=0.001, angularTolerance=0.1)
```

## CadQuery Notes

**Sweep profile positioning:** `moveTo()` only moves a 2D cursor — use `origin=` on the Workplane constructor to set the 3D world position:
```python
swept = cq.Workplane("YZ", origin=(-5, 0, height)).circle(r).sweep(path)
```

Full docs: https://cadquery.readthedocs.io/
