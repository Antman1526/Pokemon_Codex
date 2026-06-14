#!/usr/bin/env python3
"""Validate the shared native battle placeholder slice."""

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
        "battle_scene": NATIVE / "scenes" / "battle" / "BattlePlaceholder.tscn",
        "battle_script": NATIVE / "src" / "battle" / "BattlePlaceholder.gd",
        "route_script": NATIVE / "src" / "world" / "Route1.gd",
        "save": NATIVE / "src" / "save" / "SaveState.gd",
        "battle_data": NATIVE / "content" / "battles" / "blue_route_1.json",
        "smoke": NATIVE / "tests" / "battle_placeholder_test.gd",
    }
    contents = {name: require_file(path, errors) for name, path in files.items()}
    if errors:
        return errors

    markers = {
        "main": ("BattlePlaceholderScene", "_on_start_battle_placeholder", "_on_battle_placeholder_finished"),
        "battle_script": ("battle_finished", "Blue", "placeholder battle engine"),
        "route_script": ("start_battle_placeholder", "blue_route_1"),
        "save": ("active_battle_id", "last_battle_result", "start_battle_placeholder", "finish_battle_placeholder"),
        "smoke": ("battle_placeholder_test", "blue_route_1", "last_battle_result"),
    }
    for name, expected_markers in markers.items():
        for marker in expected_markers:
            if marker not in contents[name]:
                errors.append(f"{files[name].relative_to(ROOT)} missing marker: {marker}")

    data = json.loads(contents["battle_data"])
    if data.get("id") != "blue_route_1":
        errors.append("blue_route_1 battle data must use id blue_route_1")
    if data.get("opponent", {}).get("id") != "blue":
        errors.append("blue_route_1 opponent must be Blue")
    if "player_starter" not in data.get("player_side", {}).get("slots", []):
        errors.append("blue_route_1 must reserve player_starter slot")
    if "blue_starter" not in data.get("opponent", {}).get("slots", []):
        errors.append("blue_route_1 must reserve blue_starter slot")
    if data.get("status") != "placeholder":
        errors.append("blue_route_1 battle data must be marked placeholder")

    return errors


def main() -> int:
    errors = validate_files()
    if errors:
        print("Native battle placeholder validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print("Native battle placeholder validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
