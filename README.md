# claude-cq-editor

Python package for generating 3D-printable STL models using [CadQuery](https://cadquery.readthedocs.io/) and CQ-editor, developed with Claude Code.

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install cq-editor
pip install -e ".[dev]"
```

STL renderers (system packages):
```bash
sudo apt install f3d
sudo apt install flatpak
flatpak remote-add --if-not-exists flathub https://dl.flathub.org/repo/flathub.flatpakrepo
sudo flatpak install flathub net.meshlab.MeshLab
```

**OrcaSlicer** (AppImage, for slicing and sending to printer):
```bash
# Download v2.3.1 AppImage for Ubuntu 24.04
curl -L -o ~/OrcaSlicer.AppImage \
  https://github.com/OrcaSlicer/OrcaSlicer/releases/download/v2.3.1/OrcaSlicer_Linux_AppImage_Ubuntu2404_V2.3.1.AppImage
chmod +x ~/OrcaSlicer.AppImage
```

## Usage

**Interactive GUI** (live preview as you edit):
```bash
cq-editor src/cq_models/bracket.py
```

**Export to STL:**
```bash
bracket
```

**Run tests:**
```bash
pytest
```

**View the result:**
```bash
f3d bracket.stl                             # fast viewer
flatpak run net.meshlab.MeshLab bracket.stl # mesh inspection
```

**Headless slice with OrcaSlicer** (Elegoo Centauri Carbon, 0.4mm, PETG Pro, 0.2mm layers):
```bash
~/OrcaSlicer.AppImage --appimage-mount &
MPID=$! ; sleep 5
MOUNT=$(ls -d /tmp/.mount_OrcaSl* | head -1)
DISPLAY= ~/OrcaSlicer.AppImage \
  --load-settings "$MOUNT/resources/profiles/Elegoo/machine/ECC/Elegoo Centauri Carbon 0.4 nozzle.json;$MOUNT/resources/profiles/Elegoo/process/ECC/0.20mm Standard @Elegoo CC 0.4 nozzle.json" \
  --load-filaments "$MOUNT/resources/profiles/Elegoo/filament/EC/Elegoo PETG PRO @EC.json" \
  --slice 0 --outputdir ./  bracket.stl
kill $MPID
```

**Printer:** Elegoo Centauri Carbon at `192.168.1.38` — connect via OrcaSlicer GUI.

## Models

| Module | Description |
|--------|-------------|
| `src/cq_models/bracket.py` | Parametric L-bracket with equally spaced U-slot cuts per arm |
| `src/cq_models/u_cutter.py` | Reusable U-shaped cutter component |
