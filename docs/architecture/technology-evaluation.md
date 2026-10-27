# Technology evaluation and decision

Decision date: 2026-10-27. Scope: first functional device/capture/metering milestone.
Reviewed primary repository metadata, README and license files rather than assuming
that public visibility grants reuse rights. Maintenance observations below use
GitHub `pushed_at`, not `updated_at`; pushes are not evidence of release quality.
All reviewed repositories reported `archived=false` on this date.

## Existing projects

| Project | Architecture/features/dependencies | License evidence | Maintenance observation | Fit/reuse decision |
| --- | --- | --- | --- | --- |
| [EasyEffects](https://github.com/wwmm/easyeffects) | C++/Qt/QML/Kirigami with native PipeWire filters; ordered gate/EQ/compressor/limiter effects; LV2/LSP, RNNoise and other optional DSP dependencies | [LICENSE](https://github.com/wwmm/easyeffects/blob/master/LICENSE) and README: GPL-3.0-or-later | Last push 2026-10-27; active development signal | Strong effect-chain reference, but Linux/PipeWire architecture is unsuitable as a Windows Python base; do not copy its GPL implementation into this MIT project |
| [OBS Studio](https://github.com/obsproject/obs-studio) | Native C/C++ core and Qt UI, modular capture/mix/monitor/encode pipeline; Windows `win-wasapi` links libobs and Avrt | [COPYING](https://github.com/obsproject/obs-studio/blob/master/COPYING), README: GPL-2.0-or-later | Last push 2026-10-27 | Mature integration target and architecture reference; extending OBS would make a plugin/product with OBS licensing constraints, not the requested independent MIT Python app |
| [JACK2](https://github.com/jackaudio/jack2) | C++ audio server, graph activation and lock-free graph access; Windows support requires a separately installed server/driver setup | [COPYING](https://github.com/jackaudio/jack2/blob/develop/COPYING): GPL v2; [client header](https://github.com/jackaudio/jack2/blob/develop/common/jack/jack.h): LGPL-2.1-or-later. Licensing differs by component | Last push 2026-01-07 | Technically viable optional client backend, but user setup and routing differ from ordinary Windows apps. Not selected for MVP; assess exact linked components if adopted |
| [Audio Router](https://github.com/audiorouterdev/audio-router) | Windows C++ router/GUI/bootstrapper; routes or duplicates app audio, not a Python DSP mixer; README reports format/duplication limitations | [LICENSE.md](https://github.com/audiorouterdev/audio-router/blob/open/LICENSE.md): GPL v3 | Last push 2021-08-16 despite recent repository activity timestamps | Older maintenance signal and fragile routing assumptions; not a Windows 11 foundation without extensive revalidation; no code reused |
| [NAudio](https://github.com/naudio/NAudio) | .NET audio library with WASAPI playback/capture/loopback, mixing/resampling/DSP; current README describes NAudio 3 package split and net9.0 requirement | [LICENSE](https://github.com/naudio/NAudio/blob/main/LICENSE): MIT | Last push 2026-10-25 | Legally extendable with notices. Strong Windows alternative, but Python/.NET interop and another runtime complicate distribution. Reconsider a separate .NET audio host if Windows requirements dominate |

No candidate above was built or benchmarked in this evaluation. None is claimed
validated on the user's Windows machine. No upstream application source was copied,
so there are no upstream modifications to attribute. A GPL fork remains possible
if the project's licensing/product goals change; its derived work cannot simply
be relabeled MIT. Independently written original MIT modules and separately
licensed dependencies must retain their respective notices.

## Selected libraries and alternatives

- [python-sounddevice](https://github.com/spatialaudio/python-sounddevice): MIT
  ([LICENSE](https://github.com/spatialaudio/python-sounddevice/blob/master/LICENSE),
  blob `4afca0686f4a27a3d657a498e316e141dbc18e92` at review). Last push
  2026-10-26. CFFI interface to native PortAudio, device queries, format validation,
  streams and WASAPI host support. Chosen as an external dependency, not vendored.
- [PortAudio license](https://portaudio.com/docs/v19-doxydocs/License.html):
  MIT-style permissive terms; retain its notices when redistributing binaries.
- NumPy: BSD-3-Clause primary license; binary wheels may contain additional licensed
  libraries. Reuse vectorized operations for meters and future reference DSP.
- SciPy: candidate BSD-licensed filter design/reference DSP dependency; deferred
  until effects are implemented. Stateful filters must preserve state across blocks.
- PySide6: selected future GUI framework, not installed or implemented for this
  milestone. Qt for Python offers LGPLv3/GPLv3/commercial options, not MIT.
  [Official license inventory](https://doc.qt.io/qtforpython-6/licenses.html).
  Select eligible modules and preserve LGPL requirements when packaging; keep Qt
  replaceable/dynamically linked and supply notices/source information as required.

## Windows capabilities and Python limits

Python 3.12's ordinary CPython build has a GIL. Python callbacks must acquire it;
GUI work, allocation, garbage collection and OS scheduling introduce unpredictable
pauses. NumPy may release the GIL for native operations but temporary arrays,
interpreter entry and filter state still need care. A 256-frame block at 48 kHz
has a nominal 5.33 ms period, **not a measured round-trip latency**. Shared-mode
engine buffering, conversion, USB drivers and physical device clocks add delay.

PortAudio's [stream contract](https://python-sounddevice.readthedocs.io/en/latest/api/streams.html)
prohibits blocking operations and unpredictable allocations in real-time callbacks.
The first module deliberately uses blocking InputStream.read outside callbacks;
NumPy analysis and terminal JSON serialization run in the caller. It is a capture
and diagnostic path, not the future low-latency mixer engine. The future GUI must
own this session on a worker thread and poll immutable readings. No locks, GUI
signals, disk I/O or HTTP calls belong in a real-time audio callback.

[WasapiSettings](https://python-sounddevice.readthedocs.io/en/latest/api/platform-specific-settings.html)
is not a per-process capture API. This version's adapter implements ordinary input
capture only; it does not implement system loopback even where underlying
PortAudio versions have additional capabilities. Enumerating session volume
controls would not provide isolated PCM streams.

Microsoft's [application loopback sample](https://learn.microsoft.com/en-us/samples/microsoft/windows-classic-samples/applicationloopbackaudio-sample/)
uses ActivateAudioInterfaceAsync to include/exclude a process tree, separately
from whole-endpoint loopback. This is a future native-backend candidate, subject
to supported OS build/API checks, process lifetime handling and actual audio tests.
It does not create a virtual output endpoint. DRM/protected or special-mode audio
must be validated rather than assumed capturable.

For OBS to select a future Stream Mix as a microphone, an actual capture endpoint
must exist: use a separately installed compatible virtual cable (subject to its
own license), or develop a signed Windows audio driver as a separate project.
OpenWaveMix cannot manufacture such an endpoint with a GUI or Python object.
No driver is bundled or installed. A future route would write Stream Mix to a
virtual cable's render endpoint and OBS would select its paired capture endpoint.
An explicitly named Game/Discord channel requires real process capture or a
separate routed input; renaming the same input would duplicate the same signal.

For robust low-latency multi-device mixing, plan a C++ (PortAudio/WASAPI) or Rust
host with preallocated buffers, bounded single-producer/single-consumer transport,
native metering/DSP and event-driven device notifications. Native code does not
by itself solve independent clocks: multi-device buses require buffering,
asynchronous resampling, drift control and a defined drop/zero-fill policy.
Choose native migration based on measured deadline misses and source/backend
capabilities, rather than promising professional latency from Python alone.

## Build versus extend

An original Python control/UI layer plus a replaceable native I/O boundary meets
the language, MIT-original-code and incremental validation goals best. Reusing
permissive libraries is cheaper than reimplementing device APIs. Forking the GPL
applications offers mature functionality but changes the license and introduces
substantial platform or product mismatch. A full .NET app with NAudio is the
strongest Windows-focused alternative if Python ceases to be a hard requirement.

## Achievable MVP after this first milestone

1. Select one physical mono/stereo source and an explicit playback endpoint,
   validate the pair, and implement gain/mute/metering with headphones-based tests.
2. Add a second independently capturable source; define clock-master, buffering
   and resampling policy before claiming stable multi-device mixing.
3. Add an original PySide6 interface with working selectors, faders, start/stop
   and status. No synthetic meters in production mode.
4. Produce independent Monitor and Stream gain matrices, each with a selected
   real render endpoint; validate audible separation and OBS capture through
   an externally installed cable before claiming stream routing.
5. Add a limiter and persistent validated profiles after deterministic mixing
   tests; then add localhost automation with strict validation.

Acceptance: audible output, independent routes demonstrated on Windows, sensible
failure states on device loss, a recorded soak test and loopback latency evidence.
The current task delivers discovery/capture/metering plus tests, not these later
acceptance criteria.
