#!/usr/bin/env python3
"""Validate the native wild encounter command menu slice."""

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
        "encounter": NATIVE / "src" / "encounter" / "WildEncounterPlaceholder.gd",
        "test": NATIVE / "tests" / "wild_command_menu_test.gd",
    }
    contents = {name: require_file(path, errors) for name, path in files.items()}
    if errors:
        return errors

    markers = {
        "encounter": (
            "command_menu",
            "fight_button",
            "catch_button",
            "run_button",
            "_build_command_menu",
            "_update_command_menu",
            "Fight",
            "Catch",
            "Run",
        ),
        "test": (
            "wild_command_menu_test",
            "fight_button",
            "catch_button",
            "run_button",
            "catch_success",
            "placeholder_run",
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
        print("Native wild command menu validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print("Native wild command menu validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
