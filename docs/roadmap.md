# Development roadmap

## Phase 1 — foundations (current)

- Completed: source/license review, backend decision, package structure,
  device enumeration, explicit input capture, per-channel meters, CLI, tests and CI definition.
- Pending: Windows 11 hardware smoke test and recorded disconnect behavior.

## Phase 2 — audible MVP

- One input to a selected physical output with gain/mute and actual audible verification.
- PySide6 worker-owned capture and original dark channel strips, working selectors/status.
- Two independent sources only after buffering, clock drift and resampling are designed.
- Use headphones for loopback tests to avoid acoustic feedback.

## Phase 3 — processing and routing

- Stateful HPF/EQ/gate/compressor and bus limiter with generated-signal tests.
- Independent Monitor/Stream sends; test real outputs and external cable/OBS routing.
- Native process/system loopback backend spike; native engine deadline evaluation.
- Device notifications, stalled-driver recovery and long-duration soak testing.

## Phase 4 — control

- Validated versioned JSON profiles; atomic writes, import/export/restore and device identity matching.
- Gaming/Streaming/Meetings/Recording presets only with honest source mappings.
- Authenticated localhost control, command validation, automation examples and API tests.

## Phase 5 — release gates

- Windows latency round trip, callback deadline/miss distribution for the eventual callback engine,
  CPU/RSS trends, underruns/overflows and reconnect evidence.
- Real GUI screenshots, accessibility pass and tested PyInstaller build with full notices.
- CI on supported Python/Windows versions, clean-machine installation and release artifacts.

No dates or benchmark guarantees are assigned until hardware measurements exist.
