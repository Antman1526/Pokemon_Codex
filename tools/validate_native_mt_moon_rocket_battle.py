#!/usr/bin/env python3
"""Validate the native Mt. Moon Rocket left-path placeholder battle slice."""

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
        "battle": NATIVE / "content" / "battles" / "mt_moon_rocket_left_path.json",
        "battle_script": NATIVE / "src" / "battle" / "BattlePlaceholder.gd",
        "save": NATIVE / "src" / "save" / "SaveState.gd",
        "main": NATIVE / "src" / "Main.gd",
        "interior": NATIVE / "src" / "world" / "MtMoonInterior1.gd",
        "test": NATIVE / "tests" / "mt_moon_rocket_battle_test.gd",
    }
    contents = {name: require_file(path, errors) for name, path in files.items()}
    if errors:
        return errors

    data = json.loads(contents["battle"])
    if data.get("id") != "mt_moon_rocket_left_path":
        errors.append("Mt. Moon Rocket battle data must use id mt_moon_rocket_left_path")
    if data.get("location") != "mt_moon_interior_1":
        errors.append("Mt. Moon Rocket battle data must use location mt_moon_interior_1")
    if data.get("battle_type") != "faction_grunt":
        errors.append("Mt. Moon Rocket battle must be battle_type faction_grunt")
    if data.get("level_cap") != 16:
        errors.append("Mt. Moon Rocket placeholder should document level cap 16")
    if not data.get("tag_story_setup", False):
        errors.append("Mt. Moon Rocket battle must mark tag_story_setup true")
    opponent = data.get("opponent", {})
    if opponent.get("display_name") != "Rocket Grunt":
        errors.append("Mt. Moon Rocket opponent display_name must be Rocket Grunt")
    slots = opponent.get("slots", [])
    for species in ("Zubat", "Rattata"):
        if not any(slot.get("species") == species for slot in slots):
            errors.append(f"Mt. Moon Rocket battle must include {species}")

    markers = {
        "battle_script": (
            "mt_moon_rocket_left_path",
            "mt_moon_rocket_left_path.json",
        ),
        "save": (
            "mt_moon_rocket_left_battle_started",
            "mt_moon_rocket_left_battle_finished",
            "red_mt_moon_tag_setup_seen",
        ),
        "main": (
            "battle_return_scene == \"mt_moon_interior_1\"",
            "_show_mt_moon_interior_1",
        ),
        "interior": (
            "start_battle_placeholder",
            "trigger_rocket_left_path_battle",
            "fossil_choice_setup_seen",
            "mt_moon_rocket_left_path",
        ),
        "test": (
            "mt_moon_rocket_battle_test",
            "trigger_rocket_left_path_battle",
            "mt_moon_rocket_left_path",
            "red_mt_moon_tag_setup_seen",
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
        print("Native Mt. Moon Rocket battle validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print("Native Mt. Moon Rocket battle validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
