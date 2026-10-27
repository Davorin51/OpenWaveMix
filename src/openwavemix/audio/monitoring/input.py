"""Read-only hardware monitoring. This module never opens a playback endpoint."""

from dataclasses import dataclass
from math import isfinite
from time import perf_counter
from types import TracebackType
from typing import Self

from openwavemix.audio.backend import AudioError, Backend, InputStream, load_backend
from openwavemix.audio.devices.catalog import AudioDevice, discover_devices
from openwavemix.audio.monitoring.levels import Levels, measure_levels


@dataclass(frozen=True, slots=True)
class MonitorConfig:
    device: int
    channels: int = 1
    sample_rate: float = 48000.0
    block_frames: int = 1024

    def __post_init__(self) -> None:
        for name, value, minimum in (
            ("device", self.device, 0),
            ("channels", self.channels, 1),
            ("block_frames", self.block_frames, 1),
        ):
            if type(value) is not int or value < minimum:
                raise ValueError(f"{name} must be an integer >= {minimum}")
        if not isfinite(self.sample_rate) or self.sample_rate <= 0:
            raise ValueError("sample_rate must be finite and positive")
        if self.channels > 64 or self.block_frames > 65536:
            raise ValueError("channels <= 64 and block_frames <= 65536 required")


@dataclass(frozen=True, slots=True)
class MonitorReading:
    levels: Levels
    frames_read: int
    overflow_events: int
    processing_seconds: float
    input_latency_seconds: float


class InputMonitor:
    """A synchronous session owned by ONE caller (CLI now, worker thread later).

    PortAudio handles capture natively. Blocking reads and NumPy metering never
    execute in a Python real-time callback. Do not call read() on a GUI thread.
    Close and restart explicitly after device loss; no silent fallback device.
    """

    def __init__(self, config: MonitorConfig, backend: Backend | None = None):
        self.config = config
        self._backend = backend
        self._stream: InputStream | None = None
        self.device: AudioDevice | None = None
        self.frames_read = 0
        self.overflow_events = 0

    def start(self) -> None:
        if self._stream is not None:
            raise AudioError("Monitor already started")
        api = self._backend if self._backend is not None else load_backend()
        devices = discover_devices(api)
        if self.config.device >= len(devices):
            raise AudioError("Input device is missing; refresh the device list")
        device = devices[self.config.device]
        if self.config.channels > device.input_channels:
            raise AudioError(f"Device supports {device.input_channels} input channels")
        stream = None
        try:
            api.check_input_settings(
                device=device.index,
                channels=self.config.channels,
                samplerate=self.config.sample_rate,
                dtype="float32",
            )
            stream = api.InputStream(
                device=device.index,
                channels=self.config.channels,
                samplerate=self.config.sample_rate,
                blocksize=self.config.block_frames,
                dtype="float32",
                latency="high",
            )
            stream.start()
        except Exception as exc:
            if stream is not None:
                try:
                    stream.close()
                except Exception as cleanup:
                    exc.add_note(f"Stream cleanup also failed: {cleanup}")
            raise AudioError(f"Cannot open input device '{device.name}': {exc}") from exc
        self._stream = stream
        self.device = device
        self.frames_read = 0
        self.overflow_events = 0

    def read(self) -> MonitorReading:
        stream = self._stream
        if stream is None:
            raise AudioError("Monitor is not started")
        try:
            data, overflow = stream.read(self.config.block_frames)
            if data.shape != (self.config.block_frames, self.config.channels):
                raise ValueError("Backend returned an unexpected audio block shape")
            started = perf_counter()
            levels = measure_levels(data)
            processing = perf_counter() - started
            self.frames_read += len(data)
            self.overflow_events += int(overflow)
            return MonitorReading(
                levels, self.frames_read, self.overflow_events, processing, float(stream.latency)
            )
        except Exception as exc:
            try:
                self.close()
            except AudioError as cleanup:
                exc.add_note(str(cleanup))
            raise AudioError(f"Audio capture failed; refresh devices and restart: {exc}") from exc

    def close(self) -> None:
        stream, self._stream = self._stream, None
        if stream is not None:
            try:
                try:
                    stream.abort()
                finally:
                    stream.close()
            except Exception as exc:
                raise AudioError(f"Cannot close audio stream: {exc}") from exc

    def __enter__(self) -> Self:
        self.start()
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        try:
            self.close()
        except AudioError as cleanup:
            if exc is None:
                raise
            exc.add_note(str(cleanup))
