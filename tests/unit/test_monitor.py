import numpy as np
import pytest

from openwavemix.audio.backend import AudioError
from openwavemix.audio.monitoring.input import InputMonitor, MonitorConfig


def test_capture_levels_and_overflow(backend):
    stream = backend.InputStream.return_value
    stream.read.return_value = (np.full((1024, 2), 0.25, np.float32), True)
    with InputMonitor(MonitorConfig(0, channels=2), backend) as monitor:
        first = monitor.read()
        second = monitor.read()
        assert first.levels.peak == (0.25, 0.25)
        assert second.levels.rms == (0.25, 0.25)
        assert first.frames_read == 1024
        assert second.frames_read == 2048
        assert second.overflow_events == 2
        assert second.processing_seconds >= 0
        assert second.input_latency_seconds == 0.08
    stream.abort.assert_called_once()
    stream.close.assert_called_once()
    assert "callback" not in backend.InputStream.call_args.kwargs
    backend.check_input_settings.assert_called_once()


def test_close_is_idempotent(backend):
    monitor = InputMonitor(MonitorConfig(0), backend)
    monitor.close()
    monitor.start()
    monitor.close()
    monitor.close()
    backend.InputStream.return_value.close.assert_called_once()


def test_lifecycle_guards(backend):
    monitor = InputMonitor(MonitorConfig(0), backend)
    with pytest.raises(AudioError, match="not started"):
        monitor.read()
    with monitor:
        with pytest.raises(AudioError, match="already started"):
            monitor.start()


def test_restart_resets_counters(backend):
    monitor = InputMonitor(MonitorConfig(0), backend)
    with monitor:
        monitor.read()
    with monitor:
        assert monitor.read().frames_read == 1024


@pytest.mark.parametrize(
    "config", [MonitorConfig(9), MonitorConfig(1), MonitorConfig(0, channels=3)]
)
def test_missing_or_incompatible_device(backend, config):
    with pytest.raises(AudioError):
        InputMonitor(config, backend).start()
    backend.InputStream.assert_not_called()


def test_unsupported_rate(backend):
    backend.check_input_settings.side_effect = ValueError("Invalid sample rate")
    with pytest.raises(AudioError, match="Invalid sample rate"):
        InputMonitor(MonitorConfig(0), backend).start()
    backend.InputStream.assert_not_called()


def test_failed_start_closes_stream(backend):
    stream = backend.InputStream.return_value
    stream.start.side_effect = RuntimeError("Access denied")
    with pytest.raises(AudioError, match="Access denied"):
        InputMonitor(MonitorConfig(0), backend).start()
    stream.close.assert_called_once()


def test_disconnection_closes_stream_and_can_retry(backend):
    stream = backend.InputStream.return_value
    monitor = InputMonitor(MonitorConfig(0), backend)
    monitor.start()
    stream.read.side_effect = RuntimeError("Device disconnected")
    with pytest.raises(AudioError, match="Device disconnected"):
        monitor.read()
    stream.close.assert_called_once()
    stream.read.side_effect = None
    with monitor:
        assert monitor.read().frames_read == 1024


@pytest.mark.parametrize("data", [np.zeros((12, 1), np.float32), np.full((1024, 1), np.nan)])
def test_bad_backend_data_closes_stream(backend, data):
    stream = backend.InputStream.return_value
    stream.read.return_value = (data, False)
    with InputMonitor(MonitorConfig(0), backend) as monitor:
        with pytest.raises(AudioError):
            monitor.read()
    stream.close.assert_called_once()


@pytest.mark.parametrize(
    "kwargs",
    [
        {"device": -1},
        {"device": True},
        {"channels": 0},
        {"channels": 1.5},
        {"channels": 65},
        {"block_frames": 0},
        {"block_frames": 65537},
        {"sample_rate": 0},
        {"sample_rate": float("nan")},
        {"sample_rate": float("inf")},
    ],
)
def test_config_validation(kwargs):
    with pytest.raises(ValueError):
        MonitorConfig(**({"device": 0} | kwargs))


def test_start_error_survives_cleanup_failure(backend):
    stream = backend.InputStream.return_value
    stream.start.side_effect = RuntimeError("Access denied")
    stream.close.side_effect = RuntimeError("Broken close")
    with pytest.raises(AudioError, match="Access denied") as caught:
        InputMonitor(MonitorConfig(0), backend).start()
    assert "Broken close" in caught.value.__cause__.__notes__[0]


def test_read_error_survives_cleanup_failure(backend):
    stream = backend.InputStream.return_value
    stream.read.side_effect = RuntimeError("Device lost")
    stream.close.side_effect = RuntimeError("Broken close")
    monitor = InputMonitor(MonitorConfig(0), backend)
    monitor.start()
    with pytest.raises(AudioError, match="Device lost") as caught:
        monitor.read()
    assert "Broken close" in caught.value.__cause__.__notes__[0]
    monitor.close()  # no stale stream retained


def test_abort_failure_still_closes(backend):
    stream = backend.InputStream.return_value
    stream.abort.side_effect = RuntimeError("Cannot abort")
    monitor = InputMonitor(MonitorConfig(0), backend)
    monitor.start()
    with pytest.raises(AudioError, match="Cannot abort"):
        monitor.close()
    stream.close.assert_called_once()


def test_context_close_failure_reported(backend):
    backend.InputStream.return_value.close.side_effect = RuntimeError("Broken close")
    with pytest.raises(AudioError, match="Broken close"):
        with InputMonitor(MonitorConfig(0), backend):
            pass


def test_context_preserves_primary_exception(backend):
    backend.InputStream.return_value.close.side_effect = RuntimeError("Broken close")
    with pytest.raises(ValueError, match="Primary") as caught:
        with InputMonitor(MonitorConfig(0), backend):
            raise ValueError("Primary")
    assert "Broken close" in caught.value.__notes__[0]
