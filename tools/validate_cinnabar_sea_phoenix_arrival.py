#!/usr/bin/env python3
"""Validate the Cinnabar sea route and Team Phoenix first-contact slice."""

from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(path: str, errors: list[str]) -> str:
    full_path = ROOT / path
    if not full_path.exists():
        errors.append(f"Missing {path}")
        return ""
    return full_path.read_text(encoding="utf-8")


def require_markers(name: str, text: str, markers: tuple[str, ...], errors: list[str]) -> None:
    for marker in markers:
        if marker not in text:
            errors.append(f"{name} missing marker: {marker}")


def validate_patch(errors: list[str]) -> None:
    patch_path = ROOT / "patches/engine/0030-cinnabar-sea-phoenix-arrival.patch"
    if not patch_path.exists():
        errors.append("Missing patches/engine/0030-cinnabar-sea-phoenix-arrival.patch")
        return

    patch = patch_path.read_text(encoding="utf-8")
    require_markers(
        "Cinnabar Phoenix patch",
        patch,
        (
            "data/maps/Route19_Frlg/map.json",
            "data/maps/Route19_Frlg/scripts.inc",
            "data/maps/CinnabarIsland_Frlg/map.json",
            "data/maps/CinnabarIsland_Frlg/scripts.inc",
            "data/maps/CinnabarIsland_PokemonLab_ResearchRoom_Frlg/scripts.inc",
            "data/maps/PokemonMansion_1F_Frlg/scripts.inc",
            "Route19_EventScript_RedSeaRoute",
            "CinnabarIsland_EventScript_RedCinnabarRestraint",
            "CinnabarIsland_PokemonLab_ResearchRoom_EventScript_PhoenixResearcher",
            "PokemonMansion_1F_EventScript_PhoenixMewtwoEcho",
            "Phoenix",
            "WorldLink",
            "Tide Rider",
            "old fire",
            "Mewtwo",
            "Red",
        ),
        errors,
    )


def validate_design_data(errors: list[str]) -> None:
    chapter = read("data_design/kanto_chapter.yaml", errors)
    require_markers(
        "kanto_chapter",
        chapter,
        (
            "route19_tide_rider_handoff",
            "cinnabar_arrival_old_fire",
            "red_cinnabar_restraint_scene",
            "phoenix_lab_first_contact",
            "pokemon_mansion_mewtwo_phoenix_echo",
        ),
        errors,
    )

    messages = read("data_design/kanto_worldlink_messages.yaml", errors)
    require_markers(
        "kanto_worldlink_messages",
        messages,
        (
            "WL_KANTO_TIDE_RIDER_SEA_ROUTE",
            "WL_KANTO_CINNABAR_OLD_FIRE",
            "WL_KANTO_PHOENIX_FIRST_CONTACT",
            "WL_KANTO_MANSION_MEWTWO_ECHO",
        ),
        errors,
    )

    rivals = read("data_design/rival_progression_kanto.yaml", errors)
    require_markers(
        "rival_progression_kanto",
        rivals,
        (
            "cinnabar_sea_phoenix_arrival",
            "red_route19_sea_route_support",
            "misty_tide_rider_safety_check",
            "brock_cinnabar_fossil_ethics",
            "blue_cinnabar_silent_return",
            "ava_phoenix_lab_trace",
            "dax_sea_route_training_report",
        ),
        errors,
    )


def validate_docs(errors: list[str]) -> None:
    spec = read("docs/superpowers/specs/2026-06-14-cinnabar-sea-phoenix-arrival-design.md", errors)
    require_markers(
        "Cinnabar Phoenix spec",
        spec,
        (
            "Cinnabar Sea and Phoenix Arrival Design",
            "WorldLink remains Kanto-locked",
            "Red's restraint scene",
            "Team Phoenix appears through lab research",
            "Pokemon Mansion carries the Mewtwo echo",
        ),
        errors,
    )

    notes = read("build_notes/FIRST_PLAYABLE_OPENEMU_SMOKE_TEST.md", errors)
    require_markers(
        "build notes",
        notes,
        (
            "0030-cinnabar-sea-phoenix-arrival.patch",
            "validate_cinnabar_sea_phoenix_arrival.py",
            "Route 19 Red Tide Rider sea-route scene",
            "Cinnabar Red restraint scene",
            "Cinnabar Lab Phoenix first-contact scene",
            "Pokemon Mansion Mewtwo Phoenix echo",
        ),
        errors,
    )


def main() -> int:
    errors: list[str] = []
    validate_patch(errors)
    validate_design_data(errors)
    validate_docs(errors)

    if errors:
        print("Cinnabar sea Phoenix validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Cinnabar sea Phoenix validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
