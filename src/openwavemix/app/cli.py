"""Device inspection and capture diagnostics; JSON-lines metering for tooling."""

import argparse
import json
import math
import sys
from dataclasses import asdict
from time import monotonic

from openwavemix.audio.backend import AudioError
from openwavemix.audio.devices.catalog import discover_devices
from openwavemix.audio.monitoring.input import InputMonitor, MonitorConfig


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="openwavemix")
    commands = parser.add_subparsers(dest="command", required=True)
    devices = commands.add_parser("devices", help="Refresh input/output endpoint list")
    devices.add_argument("--json", action="store_true")
    monitor = commands.add_parser("monitor", help="Capture input and print peak/RMS; no playback")
    monitor.add_argument("--device", type=int, required=True, help="Index from devices command")
    monitor.add_argument("--channels", type=int, default=1)
    monitor.add_argument("--sample-rate", type=float, default=48000)
    monitor.add_argument("--block-frames", type=int, default=1024)
    monitor.add_argument("--seconds", type=float, default=10)
    args = parser.parse_args(argv)
    try:
        if args.command == "devices":
            catalog = discover_devices()
            if args.json:
                print(json.dumps([asdict(device) for device in catalog]))
            elif not catalog:
                print("No audio devices found.")
            else:
                for device in catalog:
                    print(
                        f"{device.index}: {device.name} [{device.host_api}] "
                        f"in={device.input_channels} out={device.output_channels} "
                        f"default-rate={device.default_sample_rate:g} Hz "
                        f"default-in={device.default_input} default-out={device.default_output}"
                    )
            return 0
        if not math.isfinite(args.seconds) or not 0 < args.seconds <= 86400:
            raise ValueError("seconds must be finite and in (0, 86400]")
        config = MonitorConfig(args.device, args.channels, args.sample_rate, args.block_frames)
        with InputMonitor(config) as session:
            deadline = monotonic() + args.seconds
            next_report = 0.0
            while monotonic() < deadline:
                reading = session.read()
                now = monotonic()
                if now >= next_report:
                    print(json.dumps(asdict(reading)), flush=True)
                    next_report = now + 0.1
        return 0
    except (AudioError, ValueError) as exc:
        print(f"OpenWaveMix: {exc}", file=sys.stderr)
        return 1
    except KeyboardInterrupt:
        return 130
