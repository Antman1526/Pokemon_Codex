#!/usr/bin/env python3
"""Validate the native Celadon Underground Path slice."""

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
        "route8_script": NATIVE / "src" / "world" / "Route8CeladonRoad.gd",
        "underground_scene": NATIVE / "scenes" / "world" / "CeladonUndergroundPath.tscn",
        "underground_script": NATIVE / "src" / "world" / "CeladonUndergroundPath.gd",
        "worldlink": NATIVE / "src" / "worldlink" / "WorldLinkPanel.gd",
        "worldlink_batch": NATIVE / "content" / "worldlink" / "celadon_underground_path_batch.json",
        "test": NATIVE / "tests" / "celadon_underground_path_test.gd",
    }
    contents = {name: require_file(path, errors) for name, path in files.items()}
    if errors:
        return errors

    batch = json.loads(contents["worldlink_batch"])
    if batch.get("id") != "celadon_underground_path_batch":
        errors.append("Celadon Underground Path WorldLink batch must use id celadon_underground_path_batch")
    ids = {item.get("id") for item in batch.get("feed", [])}
    for message_id in [
        "wl_celadon_underground_path_reached",
        "wl_red_celadon_underpass_guard",
        "wl_bill_game_corner_signal_trace",
        "wl_rocket_underpass_smuggler",
        "wl_team_moonlight_dream_poster",
        "wl_silph_scope_game_corner_confirmed",
        "wl_celadon_city_arrival_unlocked",
    ]:
        if message_id not in ids:
            errors.append(f"Celadon Underground Path WorldLink batch missing id: {message_id}")

    markers = {
        "main": (
            "CeladonUndergroundPathScene",
            "_on_go_to_celadon_underground_path",
            "_show_celadon_underground_path",
            "go_to_celadon_underground_path",
        ),
        "save": (
            "celadon_underground_path_reached",
            "red_celadon_underpass_guard_seen",
            "bill_game_corner_signal_trace_seen",
            "rocket_underpass_smuggler_seen",
            "team_moonlight_dream_poster_seen",
            "silph_scope_game_corner_confirmed",
            "celadon_city_arrival_unlocked",
            "queue_celadon_underground_path_batch",
        ),
        "route8_script": (
            "go_to_celadon_underground_path",
            "trigger_celadon_underground_entry",
            "underground_path_to_celadon_unlocked",
            "Underground Path",
        ),
        "underground_script": (
            "Celadon Underground Path",
            "trigger_celadon_underground_path_scene",
            "record_celadon_underground_path_scene",
            "go_to_route_8_celadon_road",
            "Red",
            "Bill",
            "Rocket",
            "Moonlight",
            "Celadon",
            "Game Corner",
            "Silph Scope",
            "Underground Path",
        ),
        "worldlink": (
            "CELADON_UNDERGROUND_PATH_BATCH_PATH",
            "Enter Celadon Underground Path",
            "Trace Game Corner signal",
            "Spot Moonlight dream poster",
            "Unlock Celadon City arrival",
        ),
        "test": (
            "celadon_underground_path_test",
            "trigger_celadon_underground_entry",
            "trigger_celadon_underground_path_scene",
            "celadon_city_arrival_unlocked",
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
        print("Native Celadon Underground Path validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print("Native Celadon Underground Path validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
