#!/usr/bin/env python3
"""Validate the native Celadon Rocket Hideout elevator slice."""

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
        "b3f_script": NATIVE / "src" / "world" / "CeladonRocketHideoutB3F.gd",
        "elevator_scene": NATIVE / "scenes" / "world" / "CeladonRocketHideoutElevator.tscn",
        "elevator_script": NATIVE / "src" / "world" / "CeladonRocketHideoutElevator.gd",
        "worldlink": NATIVE / "src" / "worldlink" / "WorldLinkPanel.gd",
        "worldlink_batch": NATIVE / "content" / "worldlink" / "celadon_rocket_hideout_elevator_batch.json",
        "test": NATIVE / "tests" / "celadon_rocket_hideout_elevator_test.gd",
    }
    contents = {name: require_file(path, errors) for name, path in files.items()}
    if errors:
        return errors

    batch = json.loads(contents["worldlink_batch"])
    if batch.get("id") != "celadon_rocket_hideout_elevator_batch":
        errors.append("Rocket Hideout elevator WorldLink batch must use id celadon_rocket_hideout_elevator_batch")
    ids = {item.get("id") for item in batch.get("feed", [])}
    for message_id in [
        "wl_celadon_rocket_hideout_elevator_reached",
        "wl_red_hideout_elevator_guard",
        "wl_bill_nexus_order_elevator_override",
        "wl_rocket_elevator_panel_restored",
        "wl_gold_dust_elevator_ledger_decoded",
        "wl_team_moonlight_elevator_sleep_signal",
        "wl_giovanni_command_floor_route_seen",
        "wl_rocket_command_floor_path_unlocked",
    ]:
        if message_id not in ids:
            errors.append(f"Rocket Hideout elevator WorldLink batch missing id: {message_id}")

    markers = {
        "main": (
            "CeladonRocketHideoutElevatorScene",
            "_on_go_to_rocket_hideout_elevator",
            "_show_celadon_rocket_hideout_elevator",
            "go_to_rocket_hideout_elevator",
            "celadon_rocket_hideout_elevator",
        ),
        "save": (
            "celadon_rocket_hideout_elevator_reached",
            "red_hideout_elevator_guard_seen",
            "bill_nexus_order_elevator_override_seen",
            "rocket_elevator_panel_restored_seen",
            "gold_dust_elevator_ledger_decoded_seen",
            "team_moonlight_elevator_sleep_signal_seen",
            "giovanni_command_floor_route_seen",
            "rocket_command_floor_path_unlocked",
            "queue_celadon_rocket_hideout_elevator_batch",
        ),
        "b3f_script": (
            "go_to_rocket_hideout_elevator",
            "trigger_rocket_hideout_elevator_entry",
            "rocket_hideout_elevator_path_unlocked",
            "Lift Key",
        ),
        "elevator_script": (
            "Celadon Rocket Hideout - Elevator",
            "trigger_rocket_hideout_elevator_scene",
            "record_celadon_rocket_hideout_elevator_scene",
            "go_to_rocket_command_floor",
            "go_to_rocket_hideout_b3f",
            "Red",
            "Bill",
            "Rocket",
            "Gold Dust",
            "Moonlight",
            "Nexus Order",
            "Giovanni",
            "elevator",
            "command floor",
        ),
        "worldlink": (
            "CELADON_ROCKET_HIDEOUT_ELEVATOR_BATCH_PATH",
            "Reach Rocket Hideout elevator",
            "Decode Nexus Order elevator override",
            "Restore Rocket elevator panel",
            "Find Giovanni command floor route",
            "Unlock Rocket command floor",
        ),
        "test": (
            "celadon_rocket_hideout_elevator_test",
            "trigger_rocket_hideout_elevator_entry",
            "trigger_rocket_hideout_elevator_scene",
            "rocket_command_floor_path_unlocked",
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
        print("Native Celadon Rocket Hideout elevator validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print("Native Celadon Rocket Hideout elevator validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
