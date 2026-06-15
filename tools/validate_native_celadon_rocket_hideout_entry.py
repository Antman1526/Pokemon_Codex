#!/usr/bin/env python3
"""Validate the native Celadon Rocket Hideout entry floor slice."""

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
        "exterior_script": NATIVE / "src" / "world" / "CeladonGameCornerExterior.gd",
        "hideout_scene": NATIVE / "scenes" / "world" / "CeladonRocketHideoutEntry.tscn",
        "hideout_script": NATIVE / "src" / "world" / "CeladonRocketHideoutEntry.gd",
        "worldlink": NATIVE / "src" / "worldlink" / "WorldLinkPanel.gd",
        "worldlink_batch": NATIVE / "content" / "worldlink" / "celadon_rocket_hideout_entry_batch.json",
        "test": NATIVE / "tests" / "celadon_rocket_hideout_entry_test.gd",
    }
    contents = {name: require_file(path, errors) for name, path in files.items()}
    if errors:
        return errors

    batch = json.loads(contents["worldlink_batch"])
    if batch.get("id") != "celadon_rocket_hideout_entry_batch":
        errors.append("Rocket Hideout entry WorldLink batch must use id celadon_rocket_hideout_entry_batch")
    ids = {item.get("id") for item in batch.get("feed", [])}
    for message_id in [
        "wl_celadon_rocket_hideout_entry_reached",
        "wl_red_hideout_entry_watch",
        "wl_bill_hideout_elevator_signal",
        "wl_rocket_lift_key_required",
        "wl_giovanni_hideout_command",
        "wl_team_moonlight_rocket_interference",
        "wl_rocket_hideout_b1f_path_unlocked",
    ]:
        if message_id not in ids:
            errors.append(f"Rocket Hideout entry WorldLink batch missing id: {message_id}")

    markers = {
        "main": (
            "CeladonRocketHideoutEntryScene",
            "_on_go_to_game_corner_hideout_entry",
            "_show_celadon_rocket_hideout_entry",
            "go_to_game_corner_hideout_entry",
            "celadon_rocket_hideout_entry",
        ),
        "save": (
            "celadon_rocket_hideout_entry_reached",
            "red_hideout_entry_watch_seen",
            "bill_hideout_elevator_signal_seen",
            "rocket_lift_key_required_seen",
            "giovanni_hideout_command_seen",
            "team_moonlight_rocket_interference_seen",
            "rocket_hideout_b1f_path_unlocked",
            "queue_celadon_rocket_hideout_entry_batch",
        ),
        "exterior_script": (
            "go_to_game_corner_hideout_entry",
            "trigger_game_corner_hideout_entry",
            "game_corner_hideout_entry_unlocked",
        ),
        "hideout_script": (
            "Celadon Rocket Hideout - Entry",
            "trigger_rocket_hideout_entry_scene",
            "record_celadon_rocket_hideout_entry_scene",
            "go_to_rocket_hideout_b1f",
            "go_to_game_corner_exterior",
            "Red",
            "Bill",
            "Rocket",
            "Giovanni",
            "Moonlight",
            "elevator",
            "Lift Key",
            "Silph Scope",
            "Hideout",
        ),
        "worldlink": (
            "CELADON_ROCKET_HIDEOUT_ENTRY_BATCH_PATH",
            "Reach Rocket Hideout entry",
            "Trace hideout elevator signal",
            "Find Lift Key requirement",
            "Hear Giovanni command",
            "Unlock Hideout B1F path",
        ),
        "test": (
            "celadon_rocket_hideout_entry_test",
            "trigger_game_corner_hideout_entry",
            "trigger_rocket_hideout_entry_scene",
            "rocket_hideout_b1f_path_unlocked",
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
        print("Native Celadon Rocket Hideout entry validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print("Native Celadon Rocket Hideout entry validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
