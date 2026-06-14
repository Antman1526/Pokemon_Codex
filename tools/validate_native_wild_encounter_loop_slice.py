#!/usr/bin/env python3
"""Validate the minimal native wild encounter attack/catch loop."""

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
        "rules": NATIVE / "src" / "encounter" / "CaptureRules.gd",
        "encounter": NATIVE / "src" / "encounter" / "WildEncounterPlaceholder.gd",
        "save": NATIVE / "src" / "save" / "SaveState.gd",
        "test": NATIVE / "tests" / "wild_encounter_loop_test.gd",
    }
    contents = {name: require_file(path, errors) for name, path in files.items()}
    if errors:
        return errors

    markers = {
        "rules": (
            "calculate_max_hp",
            "calculate_attack_damage",
            "can_capture",
            "catch_success",
        ),
        "encounter": (
            "CaptureRules",
            "wild_hp",
            "wild_max_hp",
            "attack_wild",
            "attempt_capture",
            "Red:",
        ),
        "save": (
            "catch_success",
            "route_1_first_wild_caught",
            "captured_creatures",
        ),
        "test": (
            "wild_encounter_loop_test",
            "attempt_capture",
            "attack_wild",
            "catch_success",
            "Rattata",
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
        print("Native wild encounter loop validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print("Native wild encounter loop validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
