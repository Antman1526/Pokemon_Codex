#!/usr/bin/env python3
"""Validate the native Route 2 catch tutorial slice."""

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
        "save": NATIVE / "src" / "save" / "SaveState.gd",
        "service": NATIVE / "src" / "encounter" / "EncounterService.gd",
        "route2": NATIVE / "src" / "world" / "Route2ForestGate.gd",
        "data": NATIVE / "content" / "encounters" / "route_2_wild_encounters.json",
        "test": NATIVE / "tests" / "route2_catch_tutorial_test.gd",
    }
    contents = {name: require_file(path, errors) for name, path in files.items()}
    if errors:
        return errors

    markers = {
        "main": (
            "route_2_forest_gate",
            "_show_route_2_forest_gate",
            "_return_from_wild_encounter",
        ),
        "save": (
            "encounter_return_scene",
            "route_2_catch_tutorial_seen",
            "route_2_catch_tutorial_caught",
        ),
        "service": (
            "route_2_wild_encounters.json",
            "pick_route_2_encounter",
            "route_2_red_catch_tutorial_pidgey",
            "pick_early_migration_encounter",
        ),
        "route2": (
            "start_wild_encounter",
            "trigger_route_2_catch_tutorial",
            "Pidgey",
            "Red:",
        ),
        "test": (
            "route2_catch_tutorial_test",
            "pick_route_2_encounter",
            "route_2_red_catch_tutorial_pidgey",
            "route_2_catch_tutorial_caught",
            "route_2_migration_treecko",
        ),
    }
    for name, expected_markers in markers.items():
        for marker in expected_markers:
            if marker not in contents[name]:
                errors.append(f"{files[name].relative_to(ROOT)} missing marker: {marker}")

    data = json.loads(contents["data"])
    if data.get("route_id") != "route_2":
        errors.append("Route 2 wild encounter data must use route_id route_2")
    if data.get("status") != "placeholder_playable":
        errors.append("Route 2 wild encounter data must be marked placeholder_playable")
    if data.get("level_cap_context") != "pre_brock":
        errors.append("Route 2 wild encounter data must define pre_brock level cap context")

    entries = data.get("encounters", [])
    ids = {entry.get("id") for entry in entries}
    for required_id in ("route_2_red_catch_tutorial_pidgey", "route_2_common_caterpie", "route_2_common_rattata"):
        if required_id not in ids:
            errors.append(f"Route 2 wild encounter data missing id: {required_id}")

    first = next((entry for entry in entries if entry.get("id") == "route_2_red_catch_tutorial_pidgey"), {})
    if first.get("species") != "Pidgey":
        errors.append("route_2_red_catch_tutorial_pidgey must currently be Pidgey")
    if first.get("level") != 4:
        errors.append("route_2_red_catch_tutorial_pidgey must currently be level 4")
    if first.get("return_scene") != "route_2_forest_gate":
        errors.append("Route 2 tutorial encounter must return to route_2_forest_gate")

    return errors


def main() -> int:
    errors = validate_files()
    if errors:
        print("Native Route 2 catch tutorial validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print("Native Route 2 catch tutorial validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
