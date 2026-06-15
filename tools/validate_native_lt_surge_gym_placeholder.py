#!/usr/bin/env python3
"""Validate the native Lt. Surge Vermilion Gym placeholder battle slice."""

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
        "battle": NATIVE / "content" / "battles" / "lt_surge_vermilion_gym.json",
        "battle_script": NATIVE / "src" / "battle" / "BattlePlaceholder.gd",
        "save": NATIVE / "src" / "save" / "SaveState.gd",
        "main": NATIVE / "src" / "Main.gd",
        "sabotage": NATIVE / "src" / "world" / "VermilionPowerSabotage.gd",
        "worldlink": NATIVE / "src" / "worldlink" / "WorldLinkPanel.gd",
        "worldlink_batch": NATIVE / "content" / "worldlink" / "vermilion_surge_gym_batch.json",
        "test": NATIVE / "tests" / "lt_surge_gym_placeholder_test.gd",
    }
    contents = {name: require_file(path, errors) for name, path in files.items()}
    if errors:
        return errors

    battle_data = json.loads(contents["battle"])
    if battle_data.get("id") != "lt_surge_vermilion_gym":
        errors.append("Lt. Surge battle data must use id lt_surge_vermilion_gym")
    if battle_data.get("battle_type") != "gym_leader":
        errors.append("Lt. Surge battle data must use battle_type gym_leader")
    if battle_data.get("location") != "vermilion_city":
        errors.append("Lt. Surge battle data must use location vermilion_city")
    if battle_data.get("level_cap") != 26:
        errors.append("Lt. Surge placeholder should document level cap 26")
    if battle_data.get("badge") != "Thunder Badge":
        errors.append("Lt. Surge battle data must award Thunder Badge")
    opponent = battle_data.get("opponent", {})
    if opponent.get("display_name") != "Lt. Surge":
        errors.append("Lt. Surge battle opponent display_name must be Lt. Surge")
    slots = opponent.get("slots", [])
    for species in ["Voltorb", "Pikachu", "Raichu"]:
        if not any(slot.get("species") == species for slot in slots):
            errors.append(f"Lt. Surge battle must include {species}")

    batch = json.loads(contents["worldlink_batch"])
    if batch.get("id") != "vermilion_surge_gym_batch":
        errors.append("Surge WorldLink batch must use id vermilion_surge_gym_batch")
    ids = {item.get("id") for item in batch.get("feed", [])}
    for message_id in [
        "wl_surge_vermilion_gym_started",
        "wl_surge_vermilion_gym_finished",
        "wl_thunder_badge_earned",
        "wl_surge_respect_scene",
        "wl_route_11_path_unlocked",
    ]:
        if message_id not in ids:
            errors.append(f"Surge WorldLink batch missing id: {message_id}")

    markers = {
        "battle_script": (
            "lt_surge_vermilion_gym",
            "lt_surge_vermilion_gym.json",
            "opponent_summary",
        ),
        "save": (
            "surge_vermilion_gym_started",
            "surge_vermilion_gym_finished",
            "thunder_badge_earned",
            "route_11_path_unlocked",
            "queue_vermilion_surge_gym_batch",
        ),
        "main": (
            "battle_return_scene == \"vermilion_power_sabotage\"",
            "_show_vermilion_power_sabotage",
        ),
        "sabotage": (
            "start_battle_placeholder",
            "trigger_surge_gym_battle",
            "surge_gym_battle_unlocked",
            "lt_surge_vermilion_gym",
            "Thunder Badge",
        ),
        "worldlink": (
            "VERMILION_SURGE_GYM_BATCH_PATH",
            "Challenge Lt. Surge's gym",
            "Earn Thunder Badge",
            "Unlock Route 11",
        ),
        "test": (
            "lt_surge_gym_placeholder_test",
            "trigger_surge_gym_battle",
            "lt_surge_vermilion_gym",
            "thunder_badge_earned",
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
        print("Native Lt. Surge gym placeholder validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print("Native Lt. Surge gym placeholder validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
