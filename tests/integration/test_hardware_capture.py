"""Explicit opt-in: microphone capture is never started by normal CI."""

import os

import pytest

from openwavemix.audio.monitoring.input import InputMonitor, MonitorConfig


@pytest.mark.hardware
def test_real_input():
    index = os.environ.get("OWM_TEST_INPUT_DEVICE")
    if index is None:
        pytest.skip("Set OWM_TEST_INPUT_DEVICE to an explicitly selected input index")
    with InputMonitor(MonitorConfig(int(index))) as monitor:
        for _ in range(5):
            reading = monitor.read()
            assert reading.frames_read > 0
            assert len(reading.levels.peak) == 1
            assert reading.input_latency_seconds >= 0
