import numpy as np
import pytest

from openwavemix.audio.monitoring.levels import amplitude_to_dbfs, measure_levels


def test_silence_is_finite():
    levels = measure_levels(np.zeros((1024, 2), np.float32))
    assert levels.peak == levels.rms == (0, 0)
    assert levels.peak_dbfs == levels.rms_dbfs == (-120, -120)
    assert levels.clipped_samples == (0, 0)


def test_sine_rms_and_independent_stereo():
    # An integer number of cycles ensures a reproducible RMS expectation.
    t = np.arange(4800) / 48000
    samples = np.column_stack((0.5 * np.sin(2 * np.pi * 1000 * t), np.zeros_like(t)))
    samples = samples.astype(np.float32)
    original = samples.copy()
    levels = measure_levels(samples)
    assert levels.peak == pytest.approx((0.5, 0), abs=1e-6)
    assert levels.rms == pytest.approx((0.5 / np.sqrt(2), 0), abs=1e-6)
    assert levels.peak_dbfs[0] == pytest.approx(-6.0205999)
    assert levels.rms_dbfs[0] == pytest.approx(-9.0308999)
    np.testing.assert_array_equal(samples, original)


def test_overload_is_reported_without_clamping():
    levels = measure_levels(np.array([[1, -1], [1.2, -0.5]], np.float32))
    assert levels.peak[0] == pytest.approx(1.2)
    assert levels.peak_dbfs[0] > 0
    assert levels.clipped_samples == (2, 1)


@pytest.mark.parametrize("amplitude,expected", [(1, 0), (0.1, -20), (0, -120), (1e-8, -120)])
def test_dbfs(amplitude, expected):
    assert amplitude_to_dbfs(amplitude) == pytest.approx(expected)


@pytest.mark.parametrize("amplitude", [-1, float("nan"), float("inf")])
def test_invalid_amplitude(amplitude):
    with pytest.raises(ValueError):
        amplitude_to_dbfs(amplitude)


@pytest.mark.parametrize("floor", [0, 2, float("nan"), -float("inf")])
def test_invalid_db_floor(floor):
    with pytest.raises(ValueError):
        amplitude_to_dbfs(0.5, floor)


@pytest.mark.parametrize(
    "samples",
    [
        np.zeros(10, np.float32),
        np.zeros((0, 2), np.float32),
        np.zeros((10, 0), np.float32),
        np.array([[np.nan]], np.float32),
        np.array([[np.inf]], np.float32),
        np.array([[1]], np.int16),
    ],
)
def test_invalid_audio(samples):
    with pytest.raises(ValueError):
        measure_levels(samples)
