#!/usr/bin/env python3
"""Validate the native Route 3 migration scene slice."""

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
        "route2": NATIVE / "src" / "world" / "Route2ForestGate.gd",
        "route3_scene": NATIVE / "scenes" / "world" / "Route3.tscn",
        "route3_script": NATIVE / "src" / "world" / "Route3.gd",
        "test": NATIVE / "tests" / "route3_migration_scene_test.gd",
    }
    contents = {name: require_file(path, errors) for name, path in files.items()}
    if errors:
        return errors

    markers = {
        "main": (
            "Route3Scene",
            "_on_go_to_route_3",
            "_show_route_3",
            "route_3",
        ),
        "save": (
            "enter_route_3",
            "route_3_reached",
            "red_route_3_migration_scene_seen",
        ),
        "route2": (
            "go_to_route_3",
            "trigger_route_3_entry",
        ),
        "route3_script": (
            "Route 3",
            "trigger_route_3_migration_encounter",
            "pick_early_migration_encounter",
            "route_3_migration_chespin",
            "go_to_route_2_forest_gate",
        ),
        "test": (
            "route3_migration_scene_test",
            "trigger_route_3_entry",
            "trigger_route_3_migration_encounter",
            "route_3_migration_chespin",
            "route_3_reached",
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
        print("Native Route 3 migration scene validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print("Native Route 3 migration scene validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
