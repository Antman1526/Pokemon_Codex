#!/usr/bin/env python3
"""Validate the native Route 1 wild encounter placeholder slice."""

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
        "route": NATIVE / "src" / "world" / "Route1.gd",
        "save": NATIVE / "src" / "save" / "SaveState.gd",
        "service": NATIVE / "src" / "encounter" / "EncounterService.gd",
        "scene": NATIVE / "scenes" / "encounter" / "WildEncounterPlaceholder.tscn",
        "script": NATIVE / "src" / "encounter" / "WildEncounterPlaceholder.gd",
        "data": NATIVE / "content" / "encounters" / "route_1_wild_encounters.json",
        "test": NATIVE / "tests" / "route1_wild_encounter_test.gd",
    }
    contents = {name: require_file(path, errors) for name, path in files.items()}
    if errors:
        return errors

    markers = {
        "main": (
            "WildEncounterPlaceholderScene",
            "_on_start_wild_encounter",
            "_on_wild_encounter_finished",
        ),
        "route": ("start_wild_encounter", "trigger_route_1_wild_encounter", "EncounterService"),
        "save": (
            "active_encounter_id",
            "active_encounter_data",
            "party_roster",
            "captured_creatures",
            "start_wild_encounter",
            "finish_wild_encounter",
        ),
        "service": (
            "route_1_wild_encounters.json",
            "pick_route_1_encounter",
            "route_1_first_wild",
            "pick_early_migration_encounter",
        ),
        "script": ("encounter_finished", "placeholder_catch", "wild encounter placeholder"),
        "test": (
            "route1_wild_encounter_test",
            "placeholder_catch",
            "Rattata",
            "route_1_migration_bulbasaur",
        ),
    }
    for name, expected_markers in markers.items():
        for marker in expected_markers:
            if marker not in contents[name]:
                errors.append(f"{files[name].relative_to(ROOT)} missing marker: {marker}")

    data = json.loads(contents["data"])
    if data.get("route_id") != "route_1":
        errors.append("Route 1 wild encounter data must use route_id route_1")
    if data.get("status") != "placeholder_playable":
        errors.append("Route 1 wild encounter data must be marked placeholder_playable")
    if data.get("level_cap_context") != "pre_brock":
        errors.append("Route 1 wild encounter data must define pre_brock level cap context")

    entries = data.get("encounters", [])
    ids = {entry.get("id") for entry in entries}
    for required_id in ("route_1_first_wild", "route_1_common_rattata", "route_1_starter_migration_bulbasaur"):
        if required_id not in ids:
            errors.append(f"Route 1 wild encounter data missing id: {required_id}")

    first = next((entry for entry in entries if entry.get("id") == "route_1_first_wild"), {})
    if first.get("species") != "Rattata":
        errors.append("route_1_first_wild must currently be Rattata for deterministic smoke tests")
    if first.get("level") != 3:
        errors.append("route_1_first_wild must currently be level 3")

    return errors


def main() -> int:
    errors = validate_files()
    if errors:
        print("Native Route 1 wild encounter validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print("Native Route 1 wild encounter validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
