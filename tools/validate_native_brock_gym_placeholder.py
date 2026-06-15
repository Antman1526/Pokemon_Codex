#!/usr/bin/env python3
"""Validate the native Brock Pewter Gym placeholder battle slice."""

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
        "battle": NATIVE / "content" / "battles" / "brock_pewter_gym.json",
        "battle_script": NATIVE / "src" / "battle" / "BattlePlaceholder.gd",
        "save": NATIVE / "src" / "save" / "SaveState.gd",
        "main": NATIVE / "src" / "Main.gd",
        "pewter": NATIVE / "src" / "world" / "PewterCity.gd",
        "test": NATIVE / "tests" / "brock_gym_placeholder_test.gd",
    }
    contents = {name: require_file(path, errors) for name, path in files.items()}
    if errors:
        return errors

    data = json.loads(contents["battle"])
    if data.get("id") != "brock_pewter_gym":
        errors.append("Brock battle data must use id brock_pewter_gym")
    if data.get("location") != "pewter_city":
        errors.append("Brock battle data must use location pewter_city")
    if data.get("level_cap") != 14:
        errors.append("Brock placeholder should document level cap 14")
    opponent = data.get("opponent", {})
    if opponent.get("display_name") != "Brock":
        errors.append("Brock battle opponent display_name must be Brock")
    slots = opponent.get("slots", [])
    if not any(slot.get("species") == "Geodude" for slot in slots):
        errors.append("Brock battle must include Geodude")
    if not any(slot.get("species") == "Onix" for slot in slots):
        errors.append("Brock battle must include Onix")

    markers = {
        "battle_script": (
            "brock_pewter_gym",
            "opponent_display_name",
            "opponent_summary",
        ),
        "save": (
            "brock_pewter_gym_started",
            "brock_pewter_gym_finished",
            "brock_pewter_badge_earned",
        ),
        "main": (
            "_on_start_battle_placeholder",
            "_on_battle_placeholder_finished",
            "_show_pewter_city",
        ),
        "pewter": (
            "start_battle_placeholder",
            "trigger_brock_gym_challenge",
            "brock_pewter_gym",
        ),
        "test": (
            "brock_gym_placeholder_test",
            "trigger_brock_gym_challenge",
            "brock_pewter_gym",
            "brock_pewter_badge_earned",
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
        print("Native Brock gym placeholder validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print("Native Brock gym placeholder validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
