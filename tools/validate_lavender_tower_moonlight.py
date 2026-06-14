#!/usr/bin/env python3
"""Validate the Lavender Tower Moonlight reveal slice."""

from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def require_markers(name: str, text: str, markers: tuple[str, ...], errors: list[str]) -> None:
    for marker in markers:
        if marker not in text:
            errors.append(f"{name} missing marker: {marker}")


def validate_patch(errors: list[str]) -> None:
    patch_path = ROOT / "patches/engine/0018-lavender-tower-moonlight.patch"
    if not patch_path.exists():
        errors.append("Missing patches/engine/0018-lavender-tower-moonlight.patch")
        return

    patch = patch_path.read_text(encoding="utf-8")
    require_markers(
        "Lavender Tower Moonlight patch",
        patch,
        (
            "data/maps/PokemonTower_2F_Frlg/scripts.inc",
            "data/maps/PokemonTower_2F_Frlg/map.json",
            "data/maps/PokemonTower_5F_Frlg/scripts.inc",
            "data/maps/PokemonTower_5F_Frlg/map.json",
            "data/maps/PokemonTower_6F_Frlg/scripts.inc",
            "data/maps/PokemonTower_7F_Frlg/scripts.inc",
            "data/maps/LavenderTown_VolunteerPokemonHouse_Frlg/scripts.inc",
            "PokemonTower_2F_EventScript_RedTowerCheck",
            "OBJ_EVENT_GFX_RED",
            "Team Moonlight",
            "Moonlight Veil",
            "dream static",
            "WorldLink",
            "Cubone's mother",
            "Silph Scope",
            "Poke Flute",
            "Rocket",
        ),
        errors,
    )


def validate_design_data(errors: list[str]) -> None:
    chapter = read("data_design/kanto_chapter.yaml")
    require_markers(
        "kanto_chapter",
        chapter,
        (
            "pokemon_tower_blue_rival_pressure",
            "red_pokemon_tower_after_blue_check",
            "team_moonlight_name_reveal",
            "marowak_dream_static_layer",
            "fuji_rocket_moonlight_warning",
        ),
        errors,
    )

    messages = read("data_design/kanto_worldlink_messages.yaml")
    require_markers(
        "kanto_worldlink_messages",
        messages,
        (
            "WL_KANTO_POKEMON_TOWER_BLUE_RACE",
            "WL_KANTO_TEAM_MOONLIGHT_REVEALED",
            "WL_KANTO_FUJI_DREAM_STATIC",
            "Team Moonlight",
            "Fuji",
            "dream static",
        ),
        errors,
    )

    rivals = read("data_design/rival_progression_kanto.yaml")
    require_markers(
        "rival_progression_kanto",
        rivals,
        (
            "pokemon_tower_moonlight_reveal",
            "red_pokemon_tower_after_blue_check",
            "blue_tower_race_pressure",
            "ava_moonlight_signal_research",
            "dax_tower_bravery_report",
            "misty_lavender_grief_warning",
            "brock_fuji_grounding_call",
            "lyra_moonlight_locked_profile",
        ),
        errors,
    )


def validate_build_notes(errors: list[str]) -> None:
    notes = read("build_notes/FIRST_PLAYABLE_OPENEMU_SMOKE_TEST.md")
    require_markers(
        "build notes",
        notes,
        (
            "0018-lavender-tower-moonlight.patch",
            "validate_lavender_tower_moonlight.py",
            "Lavender Tower Moonlight",
            "Team Moonlight",
        ),
        errors,
    )


def main() -> int:
    errors: list[str] = []
    validate_patch(errors)
    validate_design_data(errors)
    validate_build_notes(errors)

    if errors:
        print("Lavender Tower Moonlight validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Lavender Tower Moonlight validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
