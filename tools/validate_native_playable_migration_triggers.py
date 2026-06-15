#!/usr/bin/env python3
"""Validate playable Route 1 and Route 2 migration encounter triggers."""

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
        "service": NATIVE / "src" / "encounter" / "EncounterService.gd",
        "route1": NATIVE / "src" / "world" / "Route1.gd",
        "route2": NATIVE / "src" / "world" / "Route2ForestGate.gd",
        "save": NATIVE / "src" / "save" / "SaveState.gd",
        "test": NATIVE / "tests" / "playable_migration_triggers_test.gd",
    }
    contents = {name: require_file(path, errors) for name, path in files.items()}
    if errors:
        return errors

    markers = {
        "service": (
            "pick_early_migration_encounter",
            "captured_creatures",
            "get_early_migration_encounters_for_route",
        ),
        "route1": (
            "trigger_route_1_migration_encounter",
            "pick_early_migration_encounter",
            "Route 1 migration",
        ),
        "route2": (
            "trigger_route_2_migration_encounter",
            "pick_early_migration_encounter",
            "Route 2 migration",
        ),
        "save": (
            "captured_creatures",
            "finish_wild_encounter",
        ),
        "test": (
            "playable_migration_triggers_test",
            "trigger_route_1_migration_encounter",
            "trigger_route_2_migration_encounter",
            "route_1_migration_bulbasaur",
            "route_2_migration_treecko",
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
        print("Native playable migration trigger validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print("Native playable migration trigger validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
