#!/usr/bin/env python3
"""Validate the native Route 1, Red companion, and Blue battle placeholder slice."""

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
        "oak_lab": NATIVE / "src" / "world" / "OakLab.gd",
        "route_scene": NATIVE / "scenes" / "world" / "Route1.tscn",
        "route_script": NATIVE / "src" / "world" / "Route1.gd",
        "player": NATIVE / "src" / "world" / "PlayerAvatar.gd",
        "save": NATIVE / "src" / "save" / "SaveState.gd",
        "smoke": NATIVE / "tests" / "route1_slice_test.gd",
    }
    contents = {name: require_file(path, errors) for name, path in files.items()}
    if errors:
        return errors

    markers = {
        "main": ("Route1Scene", "_on_go_to_route_1"),
        "oak_lab": ("go_to_route_1", "Step onto Route 1"),
        "route_scene": ("Route1",),
        "route_script": ("Red:", "Blue:", "red_route_1_companion_scene_seen", "blue_battle_placeholder_seen"),
        "player": ("move_speed", "ui_right", "ui_left", "ui_down", "ui_up"),
        "save": ("route_1_reached", "red_route_1_companion_scene_seen", "blue_battle_placeholder_seen"),
        "smoke": ("route1_slice_test", "trigger_red_scene", "trigger_blue_battle_placeholder"),
    }
    for name, expected_markers in markers.items():
        for marker in expected_markers:
            if marker not in contents[name]:
                errors.append(f"{files[name].relative_to(ROOT)} missing marker: {marker}")

    return errors


def main() -> int:
    errors = validate_files()
    if errors:
        print("Native Route 1 slice validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print("Native Route 1 slice validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
