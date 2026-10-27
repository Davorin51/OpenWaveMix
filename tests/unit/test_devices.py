import pytest

from openwavemix.audio.backend import AudioError
from openwavemix.audio.devices.catalog import discover_devices


def test_enumeration_preserves_host_and_capabilities(backend):
    devices = discover_devices(backend)
    assert len(devices) == 3
    assert devices[0].name == devices[2].name
    assert devices[0].host_api == "Windows WASAPI"
    assert devices[2].host_api == "MME"
    assert devices[0].input_channels == 2
    assert devices[1].output_channels == 2
    assert devices[0].default_input and not devices[1].default_input
    assert devices[1].default_output and not devices[2].default_output


def test_empty_catalog(backend):
    backend.query_devices.return_value = []
    assert discover_devices(backend) == ()


def test_refresh_reads_new_catalog(backend):
    assert len(discover_devices(backend)) == 3
    backend.query_devices.return_value = []
    assert discover_devices(backend) == ()


def test_backend_error(backend):
    backend.query_hostapis.side_effect = RuntimeError("Audio service unavailable")
    with pytest.raises(AudioError, match="Audio service unavailable"):
        discover_devices(backend)
