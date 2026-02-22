# claude-cq-editor

Python scripts for generating 3D-printable STL models using [CadQuery](https://cadquery.readthedocs.io/) and CQ-editor, developed with Claude Code.

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install cq-editor
```

STL renderers (system packages):
```bash
sudo apt install f3d
sudo apt install flatpak
flatpak remote-add --if-not-exists flathub https://dl.flathub.org/repo/flathub.flatpakrepo
sudo flatpak install flathub net.meshlab.MeshLab
```

## Usage

**Interactive GUI** (live preview as you edit):
```bash
cq-editor model.py
```

**Headless export to STL:**
```bash
python model.py
```

**View the result:**
```bash
f3d output.stl                          # fast viewer
flatpak run net.meshlab.MeshLab output.stl  # mesh inspection
```

## Models

| File | Description |
|------|-------------|
| `test_model.py` | Box with counterbored hole and filleted edges |
| `mechanical_test.py` | Flanged pipe fitting — revolve + shell + polar bolt pattern |
