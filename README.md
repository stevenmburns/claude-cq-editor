# claude-cq-editor

Python package for generating 3D-printable STL models using [CadQuery](https://cadquery.readthedocs.io/) and CQ-editor, developed with Claude Code.

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install cq-editor
pip install -e ".[dev]"
```

**OrcaSlicer** (AppImage, for slicing and sending to printer):
```bash
curl -L -o ~/OrcaSlicer.AppImage \
  https://github.com/OrcaSlicer/OrcaSlicer/releases/download/v2.3.1/OrcaSlicer_Linux_AppImage_Ubuntu2404_V2.3.1.AppImage
chmod +x ~/OrcaSlicer.AppImage
```

## Usage

**Interactive GUI** (live preview as you edit):
```bash
cq-editor src/cq_models/l_bracket.py
```

**Export to STL:**
```bash
.venv/bin/l_bracket
.venv/bin/t_bracket
```

**Run tests:**
```bash
.venv/bin/python -m pytest
```

**Headless slice with OrcaSlicer** (Elegoo Centauri Carbon, 0.4mm, PETG Pro, 0.2mm layers):
```bash
~/OrcaSlicer.AppImage --appimage-mount &
MPID=$! ; sleep 5
MOUNT=$(ls -d /tmp/.mount_OrcaSl* | head -1)
DISPLAY= ~/OrcaSlicer.AppImage \
  --load-settings "$MOUNT/resources/profiles/Elegoo/machine/ECC/Elegoo Centauri Carbon 0.4 nozzle.json;$MOUNT/resources/profiles/Elegoo/process/ECC/0.20mm Standard @Elegoo CC 0.4 nozzle.json" \
  --load-filaments "$MOUNT/resources/profiles/Elegoo/filament/EC/Elegoo PETG PRO @EC.json" \
  --slice 0 --outputdir ./ model.stl
kill $MPID
```

**Printer:** Elegoo Centauri Carbon at `192.168.1.38` — connect via OrcaSlicer GUI.

## Models

| Module | CLI | Description |
|--------|-----|-------------|
| `src/cq_models/l_bracket.py` | `l_bracket` | Parametric L-bracket with U-slot cuts per arm |
| `src/cq_models/t_bracket.py` | `t_bracket` | T-bracket with three arms, each with U-slot cuts |
| `src/cq_models/u_cutter.py` | — | Reusable U-shaped cutter with wire-retention arms |
