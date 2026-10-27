"""Small injectable boundary; importing the package does not load PortAudio."""

from typing import Any, Protocol

import numpy as np
from numpy.typing import NDArray


class AudioError(RuntimeError):
    """An actionable audio device or stream failure."""


class InputStream(Protocol):
    @property
    def latency(self) -> float: ...
    def start(self) -> None: ...
    def read(self, frames: int) -> tuple[NDArray[np.float32], bool]: ...
    def abort(self) -> None: ...
    def close(self) -> None: ...


class Backend(Protocol):
    def query_devices(self) -> Any: ...
    def query_hostapis(self) -> Any: ...
    def check_input_settings(self, **kwargs: Any) -> None: ...
    def InputStream(self, **kwargs: Any) -> InputStream: ...  # noqa: N802


def load_backend() -> Backend:
    try:
        import sounddevice
    except (ImportError, OSError) as exc:
        raise AudioError(
            "Cannot load sounddevice/PortAudio. Install dependencies; "
            "on Linux install libportaudio2."
        ) from exc
    from typing import cast

    return cast(Backend, sounddevice)
