import json

import pytest

from openwavemix.app import cli
from openwavemix.audio.backend import AudioError
from openwavemix.audio.devices.catalog import discover_devices
from openwavemix.audio.monitoring.input import InputMonitor


def test_devices_json(monkeypatch, capsys, backend):
    monkeypatch.setattr(cli, "discover_devices", lambda: discover_devices(backend))
    assert cli.main(["devices", "--json"]) == 0
    assert json.loads(capsys.readouterr().out)[0]["host_api"] == "Windows WASAPI"


def test_no_devices(monkeypatch, capsys):
    monkeypatch.setattr(cli, "discover_devices", lambda: ())
    assert cli.main(["devices"]) == 0
    assert "No audio devices" in capsys.readouterr().out


def test_readable_devices(monkeypatch, capsys, backend):
    monkeypatch.setattr(cli, "discover_devices", lambda: discover_devices(backend))
    assert cli.main(["devices"]) == 0
    assert "default-in=True" in capsys.readouterr().out


def test_monitor_json_and_cleanup(monkeypatch, capsys, backend):
    monkeypatch.setattr(cli, "InputMonitor", lambda config: InputMonitor(config, backend))
    times = iter([0, 0, 0, 1])
    monkeypatch.setattr(cli, "monotonic", lambda: next(times))
    assert cli.main(["monitor", "--device", "0", "--seconds", "1"]) == 0
    assert json.loads(capsys.readouterr().out)["frames_read"] == 1024
    backend.InputStream.return_value.close.assert_called_once()


@pytest.mark.parametrize("seconds", ["nan", "inf", "0", "-1", "86401"])
def test_duration_validation(seconds, capsys):
    assert cli.main(["monitor", "--device", "0", "--seconds", seconds]) == 1
    assert "seconds must" in capsys.readouterr().err


def test_audio_error(monkeypatch, capsys):
    def fail():
        raise AudioError("No driver")

    monkeypatch.setattr(cli, "discover_devices", fail)
    assert cli.main(["devices"]) == 1
    assert "No driver" in capsys.readouterr().err


def test_keyboard_interrupt_cleans_up(monkeypatch, backend):
    monkeypatch.setattr(cli, "InputMonitor", lambda config: InputMonitor(config, backend))
    backend.InputStream.return_value.read.side_effect = KeyboardInterrupt
    assert cli.main(["monitor", "--device", "0"]) == 130
    backend.InputStream.return_value.close.assert_called_once()
