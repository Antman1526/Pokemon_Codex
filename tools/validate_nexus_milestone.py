#!/usr/bin/env python3
"""Validate the current Pokemon Nexus Red early-Kanto milestone."""

from __future__ import annotations

import json
from pathlib import Path

try:
    import yaml
except ImportError as exc:
    raise SystemExit("PyYAML is required: python3 -m pip install PyYAML") from exc


ROOT = Path(__file__).resolve().parents[1]
DATA_YAML = ROOT / "data_design" / "kanto_progression_scaling.yaml"
WILD_JSON = ROOT / "engine" / "pokeemerald-expansion" / "src" / "data" / "wild_encounters.json"

OFFICIAL_STARTERS = {
    "SPECIES_BULBASAUR", "SPECIES_CHARMANDER", "SPECIES_SQUIRTLE",
    "SPECIES_CHIKORITA", "SPECIES_CYNDAQUIL", "SPECIES_TOTODILE",
    "SPECIES_TREECKO", "SPECIES_TORCHIC", "SPECIES_MUDKIP",
    "SPECIES_TURTWIG", "SPECIES_CHIMCHAR", "SPECIES_PIPLUP",
    "SPECIES_SNIVY", "SPECIES_TEPIG", "SPECIES_OSHAWOTT",
    "SPECIES_CHESPIN", "SPECIES_FENNEKIN", "SPECIES_FROAKIE",
    "SPECIES_ROWLET", "SPECIES_LITTEN", "SPECIES_POPPLIO",
    "SPECIES_GROOKEY", "SPECIES_SCORBUNNY", "SPECIES_SOBBLE",
    "SPECIES_SPRIGATITO", "SPECIES_FUECOCO", "SPECIES_QUAXLY",
}

SPECIAL_EARLY = {
    "SPECIES_EEVEE", "SPECIES_PIKACHU", "SPECIES_DRATINI",
    "SPECIES_ABRA", "SPECIES_GASTLY", "SPECIES_LARVITAR",
    "SPECIES_SANDILE", "SPECIES_KUBFU", "SPECIES_STARYU",
    "SPECIES_SHROOMISH", "SPECIES_ROCKRUFF", "SPECIES_RALTS",
}

ROUTE_LEVEL_CAPS = {
    "MAP_ROUTE1": 5,
    "MAP_ROUTE2": 6,
    "MAP_ROUTE3": 8,
}

STATIC_ANOMALIES = {
    "SPECIES_GROOKEY": 7,
    "SPECIES_SCORBUNNY": 7,
    "SPECIES_SOBBLE": 7,
    "SPECIES_SPRIGATITO": 7,
    "SPECIES_FUECOCO": 7,
    "SPECIES_QUAXLY": 7,
    "SPECIES_DRATINI": 7,
    "SPECIES_LARVITAR": 7,
    "SPECIES_KUBFU": 7,
}

REQUIRED_TRAINER_SCALING_KEYS = {
    "rule",
    "early_rivals",
    "pre_brock_trainers",
    "post_brock_route_3_trainers",
}


def iter_route_land_mons():
    data = json.loads(WILD_JSON.read_text(encoding="utf-8"))
    for group in data["wild_encounter_groups"]:
        if group.get("label") != "gWildMonHeaders":
            continue
        for encounter in group["encounters"]:
            route = encounter.get("map")
            if route not in ROUTE_LEVEL_CAPS:
                continue
            land = encounter.get("land_mons")
            if not land:
                continue
            yield route, encounter.get("base_label"), land["mons"]


def validate_progression_source() -> list[str]:
    errors: list[str] = []
    data = yaml.safe_load(DATA_YAML.read_text(encoding="utf-8"))
    progression = data.get("early_kanto_progression", {})
    trainer_scaling = progression.get("trainer_scaling", {})
    missing = REQUIRED_TRAINER_SCALING_KEYS - set(trainer_scaling)
    if missing:
        errors.append(f"kanto_progression_scaling.yaml missing trainer scaling keys: {sorted(missing)}")
    if progression.get("brock", {}).get("level_cap") != 14:
        errors.append("Brock level cap must remain 14 for the first Kanto milestone")
    return errors


def validate_route_catchability() -> list[str]:
    seen = set(STATIC_ANOMALIES)
    errors: list[str] = []

    for route, label, mons in iter_route_land_mons():
        if len(mons) != 12:
            errors.append(f"{label} must have exactly 12 land slots, found {len(mons)}")
        cap = ROUTE_LEVEL_CAPS[route]
        for mon in mons:
            species = mon["species"]
            seen.add(species)
            if mon["min_level"] > mon["max_level"]:
                errors.append(f"{label} {species} has min level above max level")
            if mon["max_level"] > cap:
                errors.append(f"{label} {species} exceeds {route} cap {cap}")

    for species, level in STATIC_ANOMALIES.items():
        if level > ROUTE_LEVEL_CAPS["MAP_ROUTE3"]:
            errors.append(f"{species} static anomaly exceeds Route 3 cap")

    required = OFFICIAL_STARTERS | SPECIAL_EARLY
    missing = sorted(required - seen)
    if missing:
        errors.append("Missing early catchability: " + ", ".join(missing))

    return errors


def main() -> int:
    errors = []
    errors.extend(validate_progression_source())
    errors.extend(validate_route_catchability())

    if errors:
        print("Nexus milestone validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Nexus milestone validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
