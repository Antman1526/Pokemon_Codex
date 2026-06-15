#!/usr/bin/env python3
"""Validate the native Route 2 east field lab slice."""

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
        "cave_script": NATIVE / "src" / "world" / "DiglettCaveDetour.gd",
        "lab_scene": NATIVE / "scenes" / "world" / "Route2EastFieldLab.tscn",
        "lab_script": NATIVE / "src" / "world" / "Route2EastFieldLab.gd",
        "worldlink": NATIVE / "src" / "worldlink" / "WorldLinkPanel.gd",
        "worldlink_batch": NATIVE / "content" / "worldlink" / "route_2_east_field_lab_batch.json",
        "test": NATIVE / "tests" / "route2_east_field_lab_test.gd",
    }
    contents = {name: require_file(path, errors) for name, path in files.items()}
    if errors:
        return errors

    batch = json.loads(contents["worldlink_batch"])
    if batch.get("id") != "route_2_east_field_lab_batch":
        errors.append("Route 2 field lab WorldLink batch must use id route_2_east_field_lab_batch")
    ids = {item.get("id") for item in batch.get("feed", [])}
    for message_id in [
        "wl_route_2_east_field_lab_reached",
        "wl_red_route_2_east_exit",
        "wl_bill_echo_flute_decoder",
        "wl_oak_aide_field_tool_brief",
        "wl_rocket_moonlight_sleep_signal",
        "wl_lavender_signal_path_teased",
        "wl_route_9_rock_tunnel_path_unlocked",
    ]:
        if message_id not in ids:
            errors.append(f"Route 2 field lab WorldLink batch missing id: {message_id}")

    markers = {
        "main": (
            "Route2EastFieldLabScene",
            "_on_go_to_route_2_east_field_lab",
            "_show_route_2_east_field_lab",
            "go_to_route_2_east_field_lab",
        ),
        "save": (
            "route_2_east_field_lab_reached",
            "red_route_2_east_exit_seen",
            "bill_echo_flute_decoder_seen",
            "oak_aide_field_tool_brief_seen",
            "rocket_moonlight_sleep_signal_seen",
            "lavender_signal_path_teased",
            "route_9_rock_tunnel_path_unlocked",
            "queue_route_2_east_field_lab_batch",
        ),
        "cave_script": (
            "go_to_route_2_east_field_lab",
            "trigger_route_2_east_field_lab_entry",
            "echo_flute_lead_seen",
            "Route 2",
            "Echo Flute",
        ),
        "lab_script": (
            "Route 2 East Field Lab",
            "trigger_route_2_field_lab_scene",
            "record_route_2_field_lab_scene",
            "go_to_diglett_cave_detour",
            "Red",
            "Bill",
            "Oak",
            "Rocket",
            "Moonlight",
            "Echo Flute",
            "Lavender",
            "Rock Tunnel",
        ),
        "worldlink": (
            "ROUTE_2_EAST_FIELD_LAB_BATCH_PATH",
            "Reach Route 2 east field lab",
            "Decode Echo Flute frequency",
            "Trace Rocket and Moonlight sleep signal",
            "Unlock Route 9 toward Rock Tunnel",
        ),
        "test": (
            "route2_east_field_lab_test",
            "trigger_route_2_east_field_lab_entry",
            "trigger_route_2_field_lab_scene",
            "route_9_rock_tunnel_path_unlocked",
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
        print("Native Route 2 east field lab validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print("Native Route 2 east field lab validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
