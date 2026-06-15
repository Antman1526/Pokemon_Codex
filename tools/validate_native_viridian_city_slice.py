#!/usr/bin/env python3
"""Validate the native Viridian City shell slice."""

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
        "route": NATIVE / "src" / "world" / "Route1.gd",
        "save": NATIVE / "src" / "save" / "SaveState.gd",
        "scene": NATIVE / "scenes" / "world" / "ViridianCity.tscn",
        "script": NATIVE / "src" / "world" / "ViridianCity.gd",
        "test": NATIVE / "tests" / "viridian_city_test.gd",
    }
    contents = {name: require_file(path, errors) for name, path in files.items()}
    if errors:
        return errors

    markers = {
        "main": (
            "ViridianCityScene",
            "_on_go_to_viridian_city",
            "_show_viridian_city",
        ),
        "route": (
            "go_to_viridian_city",
            "trigger_viridian_city_entry",
            "viridian_city",
        ),
        "save": (
            "enter_viridian_city",
            "viridian_city_reached",
            "viridian_center_visited",
            "viridian_mart_visited",
            "player_money",
        ),
        "script": (
            "Viridian City",
            "Pokemon Center",
            "Poke Mart",
            "Nurse Joy",
            "interact_pokemon_center",
            "interact_poke_mart",
        ),
        "test": (
            "viridian_city_test",
            "trigger_viridian_city_entry",
            "interact_pokemon_center",
            "interact_poke_mart",
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
        print("Native Viridian City validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print("Native Viridian City validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
