#!/usr/bin/env python3
"""Validate the native Pewter City Brock/Red intro slice."""

from __future__ import annotations

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
        "route3": NATIVE / "src" / "world" / "Route3.gd",
        "pewter_scene": NATIVE / "scenes" / "world" / "PewterCity.tscn",
        "pewter_script": NATIVE / "src" / "world" / "PewterCity.gd",
        "test": NATIVE / "tests" / "pewter_city_test.gd",
    }
    contents = {name: require_file(path, errors) for name, path in files.items()}
    if errors:
        return errors

    markers = {
        "main": (
            "PewterCityScene",
            "_on_go_to_pewter_city",
            "_show_pewter_city",
        ),
        "save": (
            "enter_pewter_city",
            "pewter_city_reached",
            "brock_pewter_intro_seen",
            "red_pewter_training_seen",
        ),
        "route3": (
            "go_to_pewter_city",
            "trigger_pewter_city_entry",
            "Pewter City",
        ),
        "pewter_script": (
            "Pewter City",
            "trigger_brock_intro",
            "trigger_red_training",
            "Brock:",
            "Red:",
            "go_to_route_3",
        ),
        "test": (
            "pewter_city_test",
            "trigger_pewter_city_entry",
            "trigger_brock_intro",
            "trigger_red_training",
            "pewter_city_reached",
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
        print("Native Pewter City validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print("Native Pewter City validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
