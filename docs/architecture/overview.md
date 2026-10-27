# Architecture

Implemented path:

`CLI → device catalog / InputMonitor → injected Backend → sounddevice → PortAudio → host API`

`InputMonitor.read → float32 block → measure_levels → immutable reading → CLI JSON`

The catalog includes inputs and outputs; monitoring opens inputs only. Device
indices are PortAudio enumeration positions, valid only for the current catalog.
Defaults are per host API, not a global application routing decision. Opening
always validates the requested format via check_input_settings. No sample-rate
support is inferred from a device's default rate alone.

InputMonitor is a synchronous, single-owner context manager. It starts capture,
reads complete blocks, accumulates overflow events and frame counts, and aborts
and closes on shutdown. A read failure closes the stream and raises AudioError;
refresh/reselect/restart is explicit. Silent fallback could capture the wrong
microphone and is intentionally absent. Automatic hot-plug reconnection, stalled
driver watchdogs and persistent Windows endpoint IDs are future work.

Metering uses per-channel maximum absolute sample and square-mean-root with
float64 accumulation. Silence is floored at -120 dBFS for finite JSON output.
Samples at or beyond ±1 are counted, not clamped; this is a potential overload
indicator, not proof that analog clipping occurred. RMS is block-local, without
smoothing, LUFS weighting or true-peak oversampling.

The native capture layer has no Python callback. Read, measurement and JSON
printing allocate and may block, which is acceptable in a diagnostics caller.
The default high latency requests robustness; it is not a low-latency claim.
Future desktop integration runs this owner on a worker, with bounded UI update
rate and explicit cancellation/watchdog design. Do not use this synchronous
reader directly in the UI event loop or as a two-bus real-time mixer.

Planned boundaries: `audio/engine` owns scheduling; `audio/dsp` owns stateful
processors; `audio/routing` owns validated source-to-bus matrices; `profiles`
serializes configuration; `automation` uses the same command service as `gui`.
Directories marked planned contain documentation only, with no dummy classes.

Future DSP order: input gain → HPF/EQ → gate → compressor → channel sends →
bus sum → bus limiter. Every effect needs bypass/state continuity and synthetic
signal tests. Parameter changes are staged off the audio thread and applied at
block boundaries; smooth gain changes to prevent clicks.

Future API: localhost-only listener; typed bounded commands, no arbitrary file
paths/eval/shell operations. Add token authentication and Origin/Host defenses
before shipping browser-accessible control. Remote binding requires a separate
security design and explicit opt-in. No API currently listens on any port.
