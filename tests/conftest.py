from unittest.mock import Mock

import numpy as np
import pytest


@pytest.fixture
def backend():
    api = Mock()
    api.query_devices.return_value = [
        {
            "name": "USB Mic",
            "hostapi": 0,
            "max_input_channels": 2,
            "max_output_channels": 0,
            "default_samplerate": 48000,
        },
        {
            "name": "Speakers",
            "hostapi": 0,
            "max_input_channels": 0,
            "max_output_channels": 2,
            "default_samplerate": 48000,
        },
        {
            "name": "USB Mic",
            "hostapi": 1,
            "max_input_channels": 1,
            "max_output_channels": 0,
            "default_samplerate": 44100,
        },
    ]
    api.query_hostapis.return_value = [
        {"name": "Windows WASAPI", "default_input_device": 0, "default_output_device": 1},
        {"name": "MME", "default_input_device": 2, "default_output_device": -1},
    ]
    api.InputStream.return_value.latency = 0.08
    api.InputStream.return_value.read.return_value = (np.zeros((1024, 1), np.float32), False)
    return api
