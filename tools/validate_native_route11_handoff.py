#!/usr/bin/env python3
"""Validate the native Route 11 eastbound handoff slice."""

from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
NATIVE = ROOT / "native" / "nexus-red"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def require_file(path: Path, errors: list[str]) -> str:
    if not path.exists():
        errors.append(f"Missing required file: {path.relative_to(ROOT)}")
        return ""
    return read(path)


def validate_files() -> list[str]:
    errors: list[str] = []
    files = {
        "main": NATIVE / "src" / "Main.gd",
        "save": NATIVE / "src" / "save" / "SaveState.gd",
        "sabotage": NATIVE / "src" / "world" / "VermilionPowerSabotage.gd",
        "route11_scene": NATIVE / "scenes" / "world" / "Route11.tscn",
        "route11_script": NATIVE / "src" / "world" / "Route11.gd",
        "worldlink": NATIVE / "src" / "worldlink" / "WorldLinkPanel.gd",
        "worldlink_batch": NATIVE / "content" / "worldlink" / "route_11_handoff_batch.json",
        "test": NATIVE / "tests" / "route11_handoff_test.gd",
    }
    contents = {name: require_file(path, errors) for name, path in files.items()}
    if errors:
        return errors

    batch = json.loads(contents["worldlink_batch"])
    if batch.get("id") != "route_11_handoff_batch":
        errors.append("Route 11 WorldLink batch must use id route_11_handoff_batch")
    ids = {item.get("id") for item in batch.get("feed", [])}
    for message_id in [
        "wl_route_11_reached",
        "wl_red_route_11_eastbound_scene",
        "wl_misty_route_11_farewell",
        "wl_bill_route_11_signal_decode",
        "wl_rocket_gas_route_11_fallout",
        "wl_snorlax_roadblock_teased",
    ]:
        if message_id not in ids:
            errors.append(f"Route 11 WorldLink batch missing id: {message_id}")

    markers = {
        "main": (
            "Route11Scene",
            "_on_go_to_route_11",
            "_show_route_11",
            "go_to_route_11",
            "start_battle_placeholder.connect(_on_start_battle_placeholder)",
        ),
        "save": (
            "route_11_reached",
            "red_route_11_eastbound_scene_seen",
            "misty_route_11_farewell_seen",
            "bill_route_11_signal_decode_seen",
            "rocket_gas_route_11_fallout_seen",
            "snorlax_roadblock_teased",
            "queue_route_11_handoff_batch",
        ),
        "sabotage": (
            "go_to_route_11",
            "trigger_route_11_entry",
            "route_11_path_unlocked",
            "Thunder Badge",
        ),
        "route11_script": (
            "Route 11 - Eastbound Road",
            "trigger_route_11_handoff_scene",
            "record_route_11_handoff_scene",
            "go_to_vermilion_power_sabotage",
            "Red",
            "Misty",
            "Bill",
            "Rocket",
            "Team Gas",
            "Snorlax",
            "Nexus",
        ),
        "worldlink": (
            "ROUTE_11_HANDOFF_BATCH_PATH",
            "Reach Route 11",
            "Track Rocket and Team Gas fallout",
            "Decode Route 11 Nexus signal",
            "Tease Snorlax roadblock",
        ),
        "test": (
            "route11_handoff_test",
            "trigger_route_11_entry",
            "trigger_route_11_handoff_scene",
            "snorlax_roadblock_teased",
        ),
    }
    for name, expected_markers in markers.items():
        for marker in expected_markers:
            if marker not in contents[name]:
                errors.append(f"{files[name].relative_to(ROOT)} missing marker: {marker}")

    return errors


def main() -> int:
    errors = validate_files()
    if errors:
        print("Native Route 11 handoff validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print("Native Route 11 handoff validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
