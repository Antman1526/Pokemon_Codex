#!/usr/bin/env python3
"""Validate the native Diglett's Cave detour slice."""

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
        "route11": NATIVE / "src" / "world" / "Route11.gd",
        "cave_scene": NATIVE / "scenes" / "world" / "DiglettCaveDetour.tscn",
        "cave_script": NATIVE / "src" / "world" / "DiglettCaveDetour.gd",
        "worldlink": NATIVE / "src" / "worldlink" / "WorldLinkPanel.gd",
        "worldlink_batch": NATIVE / "content" / "worldlink" / "diglett_cave_detour_batch.json",
        "test": NATIVE / "tests" / "diglett_cave_detour_test.gd",
    }
    contents = {name: require_file(path, errors) for name, path in files.items()}
    if errors:
        return errors

    batch = json.loads(contents["worldlink_batch"])
    if batch.get("id") != "diglett_cave_detour_batch":
        errors.append("Diglett's Cave WorldLink batch must use id diglett_cave_detour_batch")
    ids = {item.get("id") for item in batch.get("feed", [])}
    for message_id in [
        "wl_diglett_cave_detour_reached",
        "wl_red_diglett_cave_guard",
        "wl_bill_diglett_cave_relay_map",
        "wl_rocket_gold_dust_cave_argument",
        "wl_snorlax_route_12_block_confirmed",
        "wl_echo_flute_lead_seen",
    ]:
        if message_id not in ids:
            errors.append(f"Diglett's Cave WorldLink batch missing id: {message_id}")

    markers = {
        "main": (
            "DiglettCaveDetourScene",
            "_on_go_to_diglett_cave_detour",
            "_show_diglett_cave_detour",
            "go_to_diglett_cave_detour",
        ),
        "save": (
            "diglett_cave_detour_reached",
            "red_diglett_cave_guard_seen",
            "bill_diglett_cave_relay_map_seen",
            "rocket_gold_dust_cave_argument_seen",
            "snorlax_route_12_block_confirmed",
            "echo_flute_lead_seen",
            "queue_diglett_cave_detour_batch",
        ),
        "route11": (
            "go_to_diglett_cave_detour",
            "trigger_diglett_cave_entry",
            "snorlax_roadblock_teased",
            "Diglett's Cave",
        ),
        "cave_script": (
            "Diglett's Cave - Nexus Detour",
            "trigger_diglett_cave_detour_scene",
            "record_diglett_cave_detour_scene",
            "go_to_route_11",
            "Red",
            "Bill",
            "Rocket",
            "Gold Dust",
            "Snorlax",
            "Echo Flute",
            "Nexus",
            "Diglett",
        ),
        "worldlink": (
            "DIGLETT_CAVE_DETOUR_BATCH_PATH",
            "Reach Diglett's Cave",
            "Map Diglett's Cave Nexus relay",
            "Confirm Snorlax blocks Route 12",
            "Find Echo Flute lead",
        ),
        "test": (
            "diglett_cave_detour_test",
            "trigger_diglett_cave_entry",
            "trigger_diglett_cave_detour_scene",
            "echo_flute_lead_seen",
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
        print("Native Diglett's Cave detour validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print("Native Diglett's Cave detour validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
