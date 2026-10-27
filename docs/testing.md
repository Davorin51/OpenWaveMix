# Testing and measurement

Unit tests require no devices: injected backend mocks cover catalog data,
preflight, streaming lifecycle and failure paths. Synthetic signals cover silence,
known-RMS sine waves, independent stereo channels, overload and invalid samples.
CLI tests verify JSON output, validation, error codes and interruption cleanup.

Run `pytest --cov=openwavemix --cov-report=term-missing` for the suite.

## Hardware integration (explicit opt-in)

Windows PowerShell:

```powershell
openwavemix devices
$env:OWM_TEST_INPUT_DEVICE = '3' # explicitly select your current input index
pytest -m hardware -v
Remove-Item Env:OWM_TEST_INPUT_DEVICE
```

The test captures five input blocks and discards them. It does not play or save
audio. Without that variable it skips; CI excludes hardware tests explicitly.
A successful hardware smoke test is not validation of routing or round-trip latency.

## Manual Windows acceptance record

Record Windows build, Python/sounddevice/PortAudio versions, host API, device/driver,
format and block size. Run `openwavemix monitor --device INDEX --seconds 60` and
verify silence/speech/clipping indicators. Unplug the selected device during
capture; record failure, time to surface and resource cleanup. Re-list devices,
reconnect/reselect and restart. Test denied microphone permissions, occupied
exclusive devices and an unsupported format. A driver may hang rather than raise;
current code has no watchdog. Never claim automatic recovery based on mocks.

## Performance interpretation

`processing_seconds` times level calculation only; it excludes blocking read,
printing, driver and end-to-end delay. `input_latency_seconds` is PortAudio's
reported estimate. `overflow_events` counts reads where discarded input was
reported, not lost frames or output underruns. There is no playback or Python
callback, so round-trip latency, output underruns and Python callback timing are
not measured in this milestone. Blocking streams' cpu_load is not meaningful
and is deliberately omitted.

Use OS process tools or an external psutil sampler for CPU/RSS during a real
capture soak; record raw results and baseline/environment. Once playback exists,
measure a physical loopback impulse/cross-correlation round trip with the same
hardware, count deadline misses and repeat with GUI/API load. Keep native-driver
and resampler buffers in the latency budget. No benchmark thresholds are enforced
on unrelated CI hardware. `tests/performance` is reserved for that future harness.
