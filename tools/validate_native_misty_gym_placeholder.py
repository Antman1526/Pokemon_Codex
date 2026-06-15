#!/usr/bin/env python3
"""Validate the native Misty Cerulean Gym placeholder battle slice."""

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
        "battle": NATIVE / "content" / "battles" / "misty_cerulean_gym.json",
        "battle_script": NATIVE / "src" / "battle" / "BattlePlaceholder.gd",
        "save": NATIVE / "src" / "save" / "SaveState.gd",
        "main": NATIVE / "src" / "Main.gd",
        "cerulean": NATIVE / "src" / "world" / "CeruleanCity.gd",
        "worldlink": NATIVE / "src" / "worldlink" / "WorldLinkPanel.gd",
        "test": NATIVE / "tests" / "misty_gym_placeholder_test.gd",
    }
    contents = {name: require_file(path, errors) for name, path in files.items()}
    if errors:
        return errors

    data = json.loads(contents["battle"])
    if data.get("id") != "misty_cerulean_gym":
        errors.append("Misty battle data must use id misty_cerulean_gym")
    if data.get("battle_type") != "gym_leader":
        errors.append("Misty battle data must use battle_type gym_leader")
    if data.get("location") != "cerulean_city":
        errors.append("Misty battle data must use location cerulean_city")
    if data.get("level_cap") != 21:
        errors.append("Misty placeholder should document level cap 21")
    if data.get("badge") != "Cascade Badge":
        errors.append("Misty battle data must award Cascade Badge")
    opponent = data.get("opponent", {})
    if opponent.get("display_name") != "Misty":
        errors.append("Misty battle opponent display_name must be Misty")
    slots = opponent.get("slots", [])
    if not any(slot.get("species") == "Staryu" for slot in slots):
        errors.append("Misty battle must include Staryu")
    if not any(slot.get("species") == "Starmie" for slot in slots):
        errors.append("Misty battle must include Starmie")

    markers = {
        "battle_script": (
            "misty_cerulean_gym",
            "misty_cerulean_gym.json",
            "opponent_summary",
        ),
        "save": (
            "misty_cerulean_gym_started",
            "misty_cerulean_gym_finished",
            "cascade_badge_earned",
            "wl_misty_cascade_badge_earned",
        ),
        "main": (
            "_on_start_battle_placeholder",
            "battle_return_scene == \"cerulean_city\"",
            "_show_cerulean_city",
        ),
        "cerulean": (
            "start_battle_placeholder",
            "trigger_misty_gym_battle",
            "misty_gym_unlocked",
            "misty_cerulean_gym",
            "Cascade Badge",
        ),
        "worldlink": (
            "Challenge Misty's gym",
            "Earn Cascade Badge",
            "cascade_badge_earned",
        ),
        "test": (
            "misty_gym_placeholder_test",
            "trigger_misty_gym_battle",
            "misty_cerulean_gym",
            "cascade_badge_earned",
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
        print("Native Misty gym placeholder validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print("Native Misty gym placeholder validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
