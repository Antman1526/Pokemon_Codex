#!/usr/bin/env python3
"""Validate the native S.S. Anne Captain cabin and Trail Cutter payoff slice."""

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
        "cargo_script": NATIVE / "src" / "world" / "SSAnneCargoHold.gd",
        "captain_scene": NATIVE / "scenes" / "world" / "SSAnneCaptainCabin.tscn",
        "captain_script": NATIVE / "src" / "world" / "SSAnneCaptainCabin.gd",
        "worldlink": NATIVE / "src" / "worldlink" / "WorldLinkPanel.gd",
        "worldlink_batch": NATIVE / "content" / "worldlink" / "ss_anne_captain_cabin_batch.json",
        "test": NATIVE / "tests" / "ss_anne_captain_cabin_test.gd",
    }
    contents = {name: require_file(path, errors) for name, path in files.items()}
    if errors:
        return errors

    batch = json.loads(contents["worldlink_batch"])
    if batch.get("id") != "ss_anne_captain_cabin_batch":
        errors.append("Captain cabin WorldLink batch must use id ss_anne_captain_cabin_batch")
    ids = {item.get("id") for item in batch.get("feed", [])}
    for message_id in [
        "wl_ss_anne_captain_cabin_reached",
        "wl_captain_seasick_scene_seen",
        "wl_trail_cutter_obtained",
        "wl_trail_cutter_field_tool_unlocked",
        "wl_surge_gym_access_unlocked",
    ]:
        if message_id not in ids:
            errors.append(f"Captain cabin WorldLink batch missing id: {message_id}")

    markers = {
        "main": (
            "SSAnneCaptainCabinScene",
            "_on_go_to_ss_anne_captain_cabin",
            "_show_ss_anne_captain_cabin",
            "go_to_ss_anne_cargo_hold",
        ),
        "save": (
            "ss_anne_captain_cabin_reached",
            "captain_seasick_scene_seen",
            "trail_cutter_obtained",
            "trail_cutter_field_tool_unlocked",
            "surge_gym_access_unlocked",
            "queue_ss_anne_captain_cabin_batch",
        ),
        "cargo_script": (
            "go_to_ss_anne_captain_cabin",
            "trigger_captain_cabin_entry",
            "ss_anne_captain_path_unlocked",
            "Captain Cabin",
        ),
        "captain_script": (
            "S.S. Anne Captain Cabin",
            "trigger_captain_cabin_scene",
            "record_ss_anne_captain_cabin_scene",
            "Red",
            "Misty",
            "Bill",
            "Trail Cutter",
            "Surge",
        ),
        "worldlink": (
            "SS_ANNE_CAPTAIN_CABIN_BATCH_PATH",
            "Reach Captain cabin",
            "Help S.S. Anne Captain",
            "Obtain Trail Cutter",
            "Unlock Lt. Surge gym access",
        ),
        "test": (
            "ss_anne_captain_cabin_test",
            "trigger_captain_cabin_entry",
            "trigger_captain_cabin_scene",
            "trail_cutter_field_tool_unlocked",
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
        print("Native S.S. Anne Captain cabin validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print("Native S.S. Anne Captain cabin validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
