#!/usr/bin/env python3
"""Validate the Routes 1-3 early starter and bonus migration pool."""

from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
NATIVE = ROOT / "native" / "nexus-red"

OFFICIAL_STARTERS = [
    "Bulbasaur", "Charmander", "Squirtle",
    "Chikorita", "Cyndaquil", "Totodile",
    "Treecko", "Torchic", "Mudkip",
    "Turtwig", "Chimchar", "Piplup",
    "Snivy", "Tepig", "Oshawott",
    "Chespin", "Fennekin", "Froakie",
    "Rowlet", "Litten", "Popplio",
    "Grookey", "Scorbunny", "Sobble",
    "Sprigatito", "Fuecoco", "Quaxly",
]
BONUS_STARTERS = [
    "Eevee", "Pikachu", "Dratini", "Abra", "Gastly", "Larvitar",
    "Sandile", "Kubfu", "Staryu", "Shroomish", "Rockruff", "Ralts",
]
REQUIRED_SPECIES = OFFICIAL_STARTERS + BONUS_STARTERS
REQUIRED_ROUTES = {"route_1", "route_2", "route_3"}


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
        "starter_data": NATIVE / "content" / "starters" / "starter_choices.json",
        "migration_data": NATIVE / "content" / "encounters" / "route_1_to_3_migration_encounters.json",
        "service": NATIVE / "src" / "encounter" / "EncounterService.gd",
        "test": NATIVE / "tests" / "early_migration_pool_test.gd",
    }
    contents = {name: require_file(path, errors) for name, path in files.items()}
    if errors:
        return errors

    starter_data = json.loads(contents["starter_data"])
    starter_species = [entry.get("species") for entry in starter_data.get("starters", [])]
    if starter_species[:27] != OFFICIAL_STARTERS:
        errors.append("Starter selector must keep all 27 official starters first and in generation order")
    for species in BONUS_STARTERS:
        if species not in starter_species:
            errors.append(f"Starter selector missing bonus starter: {species}")

    migration_data = json.loads(contents["migration_data"])
    if migration_data.get("pool_id") != "route_1_to_3_migration":
        errors.append("Migration data must use pool_id route_1_to_3_migration")
    if migration_data.get("level_cap_context") != "pre_brock":
        errors.append("Migration data must define pre_brock level cap context")
    if set(migration_data.get("routes", [])) != REQUIRED_ROUTES:
        errors.append("Migration data must cover exactly route_1, route_2, and route_3")

    encounters = migration_data.get("encounters", [])
    species_names = [entry.get("species") for entry in encounters]
    if sorted(species_names) != sorted(REQUIRED_SPECIES):
        missing = sorted(set(REQUIRED_SPECIES) - set(species_names))
        extra = sorted(set(species_names) - set(REQUIRED_SPECIES))
        if missing:
            errors.append("Migration data missing species: " + ", ".join(missing))
        if extra:
            errors.append("Migration data has unexpected species: " + ", ".join(extra))
    if len(species_names) != len(set(species_names)):
        errors.append("Migration data must not duplicate species entries")

    route_counts = {route_id: 0 for route_id in REQUIRED_ROUTES}
    for entry in encounters:
        route_id = entry.get("route_id")
        route_counts[route_id] = route_counts.get(route_id, 0) + 1
        level = entry.get("level")
        if route_id not in REQUIRED_ROUTES:
            errors.append(f"Unexpected migration route_id: {route_id}")
        if not isinstance(level, int) or level < 3 or level > 7:
            errors.append(f"{entry.get('species')} must stay in pre-Brock level band 3-7")
        if not entry.get("return_scene"):
            errors.append(f"{entry.get('species')} missing return_scene")
        if "route_1_to_3_migration_pool" not in entry.get("tags", []):
            errors.append(f"{entry.get('species')} missing route_1_to_3_migration_pool tag")
    for route_id in REQUIRED_ROUTES:
        if route_counts.get(route_id, 0) != 13:
            errors.append(f"{route_id} must have 13 migration encounters")

    markers = {
        "service": (
            "route_1_to_3_migration_encounters.json",
            "get_early_migration_pool",
            "get_early_migration_encounters_for_route",
            "find_early_migration_species",
        ),
        "test": (
            "early_migration_pool_test",
            "get_early_migration_pool",
            "find_early_migration_species",
            "Kubfu",
            "Sprigatito",
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
        print("Native early migration pool validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print("Native early migration pool validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
