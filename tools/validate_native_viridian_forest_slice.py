#!/usr/bin/env python3
"""Validate the native Viridian Forest mini-dungeon slice."""

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
        "forest_scene": NATIVE / "scenes" / "world" / "ViridianForest.tscn",
        "forest_script": NATIVE / "src" / "world" / "ViridianForest.gd",
        "test": NATIVE / "tests" / "viridian_forest_test.gd",
    }
    contents = {name: require_file(path, errors) for name, path in files.items()}
    if errors:
        return errors

    markers = {
        "main": (
            "ViridianForestScene",
            "_on_go_to_viridian_forest",
            "_show_viridian_forest",
        ),
        "save": (
            "enter_viridian_forest",
            "viridian_forest_reached",
            "red_viridian_forest_scene_seen",
            "rocket_forest_scout_seen",
        ),
        "route2": (
            "go_to_viridian_forest",
            "trigger_viridian_forest_entry",
        ),
        "forest_script": (
            "Viridian Forest",
            "trigger_rocket_scout_scene",
            "go_to_route_3",
            "go_to_route_2_forest_gate",
            "Rocket scout",
            "Red:",
        ),
        "test": (
            "viridian_forest_test",
            "trigger_viridian_forest_entry",
            "trigger_rocket_scout_scene",
            "viridian_forest_reached",
            "rocket_forest_scout_seen",
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
        print("Native Viridian Forest validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print("Native Viridian Forest validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
