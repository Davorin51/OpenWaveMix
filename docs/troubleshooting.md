# Troubleshooting

- **PortAudio cannot load:** install dependencies in the active virtual environment.
  Windows wheels supply a native PortAudio library; Linux needs its system library.
  Check Python/OS bitness and preserve native dependency errors when reporting issues.
- **No devices:** check the audio service, driver and physical connection. A headless
  development runner may correctly enumerate zero devices.
- **Input unavailable:** Windows Settings → Privacy & security → Microphone → allow
  desktop app access. Check exclusive use by another app and run `devices` again.
- **Unsupported format:** choose a real input with sufficient channels and try its
  default rate. OpenWaveMix reports rejection; it does not silently resample.
- **Only outputs listed:** this backend does not capture output-only devices via
  loopback. An input from a separately installed virtual cable can be selected
  if PortAudio exposes it, but that does not isolate arbitrary applications.
- **Overflow events:** reduce other CPU load, keep default robust latency and test
  a larger `--block-frames`. Record the format/driver and event count; fewer JSON
  messages do not prove fewer audio errors.
- **Disconnected input:** errors close the session. Re-list, reselect and restart.
  Automatic recovery and protection against a hung native driver are not implemented.
- **No sound from speakers:** this milestone meters input only. It never opens output.
- **Silence meters:** select the intended microphone, unmute it in Windows, confirm
  capture permissions, and try one channel at the device's supported sample rate.
