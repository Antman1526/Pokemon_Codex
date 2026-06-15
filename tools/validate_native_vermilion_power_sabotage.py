#!/usr/bin/env python3
"""Validate the native Vermilion power sabotage setup slice."""

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
        "vermilion_script": NATIVE / "src" / "world" / "VermilionCity.gd",
        "sabotage_scene": NATIVE / "scenes" / "world" / "VermilionPowerSabotage.tscn",
        "sabotage_script": NATIVE / "src" / "world" / "VermilionPowerSabotage.gd",
        "worldlink": NATIVE / "src" / "worldlink" / "WorldLinkPanel.gd",
        "worldlink_batch": NATIVE / "content" / "worldlink" / "vermilion_power_sabotage_batch.json",
        "test": NATIVE / "tests" / "vermilion_power_sabotage_test.gd",
    }
    contents = {name: require_file(path, errors) for name, path in files.items()}
    if errors:
        return errors

    batch = json.loads(contents["worldlink_batch"])
    if batch.get("id") != "vermilion_power_sabotage_batch":
        errors.append("Power sabotage WorldLink batch must use id vermilion_power_sabotage_batch")
    ids = {item.get("id") for item in batch.get("feed", [])}
    for message_id in [
        "wl_vermilion_power_sabotage_reached",
        "wl_rocket_gas_power_sabotage",
        "wl_team_gas_kanto_debut",
        "wl_red_misty_surge_prep",
        "wl_bill_power_grid_decode",
        "wl_surge_gym_battle_unlocked",
    ]:
        if message_id not in ids:
            errors.append(f"Power sabotage WorldLink batch missing id: {message_id}")

    markers = {
        "main": (
            "VermilionPowerSabotageScene",
            "_on_go_to_vermilion_power_sabotage",
            "_show_vermilion_power_sabotage",
            "go_to_vermilion_city",
        ),
        "save": (
            "vermilion_power_sabotage_reached",
            "rocket_gas_power_sabotage_seen",
            "team_gas_kanto_debut_seen",
            "red_misty_surge_prep_seen",
            "bill_power_grid_decode_seen",
            "surge_gym_battle_unlocked",
            "queue_vermilion_power_sabotage_batch",
        ),
        "vermilion_script": (
            "go_to_vermilion_power_sabotage",
            "trigger_surge_power_sabotage_entry",
            "trail_cutter_field_tool_unlocked",
            "Power Sabotage",
        ),
        "sabotage_script": (
            "Vermilion Power Sabotage",
            "trigger_power_sabotage_scene",
            "record_vermilion_power_sabotage_scene",
            "Red",
            "Misty",
            "Bill",
            "Rocket",
            "Team Gas",
            "Surge",
        ),
        "worldlink": (
            "VERMILION_POWER_SABOTAGE_BATCH_PATH",
            "Reach Vermilion power sabotage",
            "Expose Rocket and Team Gas",
            "Prepare with Red and Misty",
            "Unlock Lt. Surge gym battle",
        ),
        "test": (
            "vermilion_power_sabotage_test",
            "trigger_surge_power_sabotage_entry",
            "trigger_power_sabotage_scene",
            "team_gas_kanto_debut_seen",
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
        print("Native Vermilion power sabotage validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print("Native Vermilion power sabotage validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
