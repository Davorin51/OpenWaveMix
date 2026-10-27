"""Reproducible per-channel sample peak and RMS, with an explicit dBFS floor."""

from dataclasses import dataclass

import numpy as np
from numpy.typing import NDArray


@dataclass(frozen=True, slots=True)
class Levels:
    peak: tuple[float, ...]
    rms: tuple[float, ...]
    peak_dbfs: tuple[float, ...]
    rms_dbfs: tuple[float, ...]
    clipped_samples: tuple[int, ...]


def amplitude_to_dbfs(amplitude: float, floor_db: float = -120.0) -> float:
    if not np.isfinite(amplitude) or amplitude < 0:
        raise ValueError("amplitude must be finite and non-negative")
    if not np.isfinite(floor_db) or floor_db >= 0:
        raise ValueError("floor_db must be finite and negative")
    if amplitude == 0:
        return floor_db
    return max(floor_db, float(20 * np.log10(amplitude)))


def measure_levels(samples: NDArray[np.float32]) -> Levels:
    """Expect normalized float audio shaped (frames, channels); never modify input.

    Values outside [-1, 1] are retained so overloads are visible. Sample peaks
    are not inter-sample true peaks. Allocations here run outside RT callbacks.
    """
    if samples.ndim != 2 or 0 in samples.shape:
        raise ValueError("samples must have non-empty shape (frames, channels)")
    if samples.dtype.kind != "f" or not np.isfinite(samples).all():
        raise ValueError("samples must contain finite floating-point audio")
    absolute = np.abs(samples)
    peak = tuple(float(x) for x in absolute.max(axis=0))
    # Double precision accumulation avoids overflow from float32 squaring.
    rms = tuple(float(x) for x in np.sqrt(np.mean(np.square(samples, dtype=np.float64), axis=0)))
    return Levels(
        peak=peak,
        rms=rms,
        peak_dbfs=tuple(amplitude_to_dbfs(x) for x in peak),
        rms_dbfs=tuple(amplitude_to_dbfs(x) for x in rms),
        clipped_samples=tuple(int(x) for x in np.count_nonzero(absolute >= 1, axis=0)),
    )
