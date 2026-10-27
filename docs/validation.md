# Validation record — 2026-10-27

Environment: Linux x86_64, CPython 3.12.14, NumPy 2.5.4,
sounddevice 0.5.6, pytest 9.1.1, pytest-cov 7.1.0, Ruff 0.17.3,
mypy 1.20.2, build 1.6.1, isolated build setuptools 84.2.1.

| Check executed | Actual outcome |
| --- | --- |
| `pytest --cov=openwavemix --cov-report=term-missing` | 64 passed, 1 skipped (0.19 s on this runner) |
| Coverage in that run | 99% statements; module entry point excluded by execution path, not by coverage configuration |
| `ruff check .` | Passed |
| `ruff format --check .` | Passed |
| `mypy` | Passed, 11 source files, strict mode |
| `python -m build` | Built sdist and universal Python wheel successfully |
| Wheel install in separate venv; `python -m openwavemix --help` | Passed without relying on editable source import |
| `python -m openwavemix devices --json` in development venv | Exit 1, correctly reports unavailable PortAudio library |
| Actual microphone capture | Not executed: this runner has no usable native audio backend/hardware |
| Windows 11 WASAPI, device loss, latency and CPU/RSS soak | Not executed |
| PyInstaller Windows executable | Recipe only; not built or validated here |
| Hosted GitHub Actions matrix | Defined, not run on GitHub |

Coverage reflects deterministic in-process tests using injected backends, not
proof of driver correctness or audible output. Tests verify cleanup failures do
not mask primary errors. The skipped integration test requires explicit device
selection through OWM_TEST_INPUT_DEVICE; no microphone is opened by default.

No callback/round-trip latency, CPU, memory or underrun benchmark is claimed.
The stream has no playback or Python callback in this milestone. See testing.md
for interpreting exposed timing and overflow fields and the hardware protocol.

During the initial local validation, GitHub inspection returned 404 for
Davorin51/OpenWaveMix; publication had not yet occurred. The original local
checkout used feat/device-monitoring. Main was not modified.

Packaging smoke-test detail: the first isolated install used
`--no-deps` in an empty venv; importing the CLI then failed because NumPy was
absent. Installing the wheel with its declared runtime dependencies resolved
that failure and the module help command succeeded. This does not require
PortAudio because backend loading is lazy. The host's native PortAudio package
could not be installed from the available system package environment.

## GitHub publication — 2026-10-27

The repository was subsequently created and the milestone imported on
`development`, the default development branch. No main branch was created or
modified. Remote commit `87a8f3759381a4ca4a9cbff540840a2539d999a2`
has tree `09bc89360bdb1956cb936faf7f9c737d9c5904f8`, matching the
complete tested local milestone tree exactly. This documentation update records
publication without changing the audio implementation. Hosted CI is tracked
in the repository Actions tab; the earlier table records local validation only.
