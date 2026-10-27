"""Enumerate endpoints without claiming per-application capture capabilities."""

from dataclasses import dataclass

from openwavemix.audio.backend import AudioError, Backend, load_backend


@dataclass(frozen=True, slots=True)
class AudioDevice:
    index: int
    name: str
    host_api: str
    input_channels: int
    output_channels: int
    default_sample_rate: float
    default_input: bool
    default_output: bool


def discover_devices(backend: Backend | None = None) -> tuple[AudioDevice, ...]:
    """Return a fresh catalog. Indices are ephemeral; never persist them as identity."""
    api = backend if backend is not None else load_backend()
    try:
        devices = api.query_devices()
        hosts = api.query_hostapis()
        return tuple(
            AudioDevice(
                index=i,
                name=str(device["name"]),
                host_api=str(hosts[int(device["hostapi"])]["name"]),
                input_channels=int(device["max_input_channels"]),
                output_channels=int(device["max_output_channels"]),
                default_sample_rate=float(device["default_samplerate"]),
                default_input=i == hosts[int(device["hostapi"])]["default_input_device"],
                default_output=i == hosts[int(device["hostapi"])]["default_output_device"],
            )
            for i, device in enumerate(devices)
        )
    except Exception as exc:
        raise AudioError(f"Cannot enumerate audio devices: {exc}") from exc
