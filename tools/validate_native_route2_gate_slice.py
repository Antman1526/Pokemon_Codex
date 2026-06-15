#!/usr/bin/env python3
"""Validate the native Route 2 / Viridian Forest gate slice."""

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
        "viridian": NATIVE / "src" / "world" / "ViridianCity.gd",
        "scene": NATIVE / "scenes" / "world" / "Route2ForestGate.tscn",
        "script": NATIVE / "src" / "world" / "Route2ForestGate.gd",
        "test": NATIVE / "tests" / "route2_forest_gate_test.gd",
    }
    contents = {name: require_file(path, errors) for name, path in files.items()}
    if errors:
        return errors

    markers = {
        "main": (
            "Route2ForestGateScene",
            "_on_go_to_route_2_forest_gate",
            "_show_route_2_forest_gate",
        ),
        "save": (
            "enter_route_2_forest_gate",
            "route_2_forest_gate_reached",
            "red_route_2_warning_seen",
        ),
        "viridian": (
            "go_to_route_2_forest_gate",
            "trigger_route_2_gate_entry",
            "viridian_rocket_clue_found",
        ),
        "script": (
            "Route 2",
            "Viridian Forest Gate",
            "Red:",
            "Rocket activity",
            "go_to_viridian_city",
        ),
        "test": (
            "route2_forest_gate_test",
            "trigger_route_2_gate_entry",
            "route_2_forest_gate_reached",
            "red_route_2_warning_seen",
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
        print("Native Route 2 forest gate validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print("Native Route 2 forest gate validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
