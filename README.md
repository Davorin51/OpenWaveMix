# OpenWaveMix

**A Windows-first open-source audio mixer, built incrementally on tested audio foundations.**

Current release: **0.1.0a1 — device discovery and input metering CLI**.
This is the first engineering milestone, not a completed virtual mixer.

## What works today

- Enumerate PortAudio input/output endpoints, channel counts, default rates and host APIs.
- Show each host API's default input/output endpoint; duplicate device names stay distinguishable.
- Capture mono or multichannel input from an explicitly selected device.
- Report per-channel sample peak, RMS, dBFS and full-scale sample counts as JSON lines.
- Count input overflow events, expose backend-reported input latency and time level calculation.
- Validate device capabilities and input format; close streams on failures and interruption.
- Inject an audio backend for hardware-independent testing.

Audio is measured in memory and discarded. The application does not record files or play audio.
“Monitoring” currently means **level metering**, not headphone monitoring.

| Capability | Status |
| --- | --- |
| Endpoint discovery, capture, peak/RMS | Implemented; real Windows hardware validation pending |
| Multi-source mix, faders and playback | Planned, Phase 2 |
| PySide6 dark desktop UI | Planned, Phase 2 |
| DSP effects and two independently routed mixes | Planned, Phase 3 |
| Per-process capture, loopback and hot-plug recovery | Research/design only |
| Profiles and localhost automation | Planned, Phase 4 |
| Virtual microphone driver | Not implemented; external endpoint required for planned OBS routing |

## Install and run (Windows 11, Python 3.12+)

In PowerShell, from the repository root:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python -m pip install -e ".[dev]"
.\.venv\Scripts\openwavemix devices
.\.venv\Scripts\openwavemix devices --json
# Replace 3 with a current INPUT index from the list (prefer Windows WASAPI).
.\.venv\Scripts\openwavemix monitor --device 3 --channels 1 --sample-rate 48000 --seconds 10
```

Indices can change after reboot or reconnection. Re-list devices before selecting one.
Names such as “Speakers” do not make an endpoint capture-capable. This backend cannot
turn an output-only endpoint into a loopback input. The selected input must support
the requested channel count and sample rate; try its listed default rate on rejection.
`Ctrl+C` closes capture. Exit codes: 0 success, 1 audio/configuration error, 2 CLI usage, 130 interrupt.

Linux development requires a system PortAudio library (e.g. `sudo apt install libportaudio2`).
The Python package is portable; Windows-specific capabilities have not been validated here.

## Development

```shell
python -m pip install -e ".[dev]"
pytest --cov=openwavemix --cov-report=term-missing
ruff check .
ruff format --check .
mypy
python -m build
```

Hardware capture is skipped unless `OWM_TEST_INPUT_DEVICE` is explicitly set.
See [testing](docs/testing.md), [validation results](docs/validation.md),
[architecture](docs/architecture/overview.md), [technology evaluation](docs/architecture/technology-evaluation.md),
[roadmap](docs/roadmap.md), [troubleshooting](docs/troubleshooting.md),
[Windows packaging](docs/windows-packaging.md), and [contributing](CONTRIBUTING.md).

## License and attribution

Original OpenWaveMix code is [MIT](LICENSE). Dependencies keep their own licenses;
see [third-party notes](THIRD_PARTY_NOTICES.md). No source, visual assets or branding
from Elgato, Voicemeeter, OBS, EasyEffects or Audio Router is bundled.

Screenshots will be added when the working desktop UI exists. No mock screenshot is
presented as a working mixer.
