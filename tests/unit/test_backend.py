import sys
from types import ModuleType

import pytest

from openwavemix.audio.backend import AudioError, load_backend


def test_backend_import_is_lazy_and_injectable(monkeypatch):
    module = ModuleType("sounddevice")
    monkeypatch.setitem(sys.modules, "sounddevice", module)
    assert load_backend() is module


def test_missing_backend_has_actionable_message(monkeypatch):
    monkeypatch.setitem(sys.modules, "sounddevice", None)
    with pytest.raises(AudioError, match="PortAudio"):
        load_backend()
