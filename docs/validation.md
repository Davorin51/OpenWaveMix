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

GitHub inspection returned 404 for Davorin51/OpenWaveMix, and the accessible
repository inventory did not contain it. No remote repository was created, no
branch was pushed, and no PR/hosted CI run exists. Work is committed locally on
feat/device-monitoring for review/import; main was not modified.
