#!/usr/bin/env python3
"""Validate the Lavender Tower Silph Scope return payoff slice."""

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
    patch_path = ROOT / "patches/engine/0022-silph-scope-return.patch"
    if not patch_path.exists():
        errors.append("Missing patches/engine/0022-silph-scope-return.patch")
        return

    patch = patch_path.read_text(encoding="utf-8")
    require_markers(
        "Silph Scope return patch",
        patch,
        (
            "data/maps/PokemonTower_6F_Frlg/map.json",
            "data/maps/PokemonTower_6F_Frlg/scripts.inc",
            "data/maps/PokemonTower_7F_Frlg/scripts.inc",
            "data/maps/LavenderTown_VolunteerPokemonHouse_Frlg/scripts.inc",
            "OBJ_EVENT_GFX_RED",
            "PokemonTower_6F_EventScript_RedMarowakSupport",
            "Silph Scope",
            "MAROWAK",
            "Team Moonlight",
            "WorldLink",
            "POKé FLUTE",
            "SNORLAX",
            "FUCHSIA",
            "SAFFRON",
        ),
        errors,
    )


def validate_design_data(errors: list[str]) -> None:
    chapter = read("data_design/kanto_chapter.yaml")
    require_markers(
        "kanto_chapter",
        chapter,
        (
            "silph_scope_tower_return",
            "red_marowak_grief_support",
            "marowak_spirit_calmed",
            "fuji_poke_flute_route_open",
            "snorlax_path_objective",
            "saffron_fuchsia_branch_warning",
        ),
        errors,
    )

    messages = read("data_design/kanto_worldlink_messages.yaml")
    require_markers(
        "kanto_worldlink_messages",
        messages,
        (
            "WL_KANTO_MAROWAK_CALMED",
            "WL_KANTO_POKE_FLUTE_ROUTE_OPEN",
            "WL_KANTO_SAFFRON_FUCHSIA_BRANCH",
            "Marowak",
            "Poke Flute",
            "Snorlax",
            "Fuchsia",
            "Saffron",
        ),
        errors,
    )

    rivals = read("data_design/rival_progression_kanto.yaml")
    require_markers(
        "rival_progression_kanto",
        rivals,
        (
            "silph_scope_lavender_return",
            "red_marowak_grief_support",
            "misty_tower_aftercare_call",
            "brock_fuji_route_call",
            "blue_tower_pressure_reconsidered",
            "ava_marowak_signal_research",
            "dax_snorlax_training_report",
            "lyra_poke_flute_locked_profile",
        ),
        errors,
    )


def validate_build_notes(errors: list[str]) -> None:
    notes = read("build_notes/FIRST_PLAYABLE_OPENEMU_SMOKE_TEST.md")
    require_markers(
        "build notes",
        notes,
        (
            "0022-silph-scope-return.patch",
            "validate_silph_scope_return.py",
            "Silph Scope return",
            "Marowak grief support",
            "Poke Flute route unlock",
        ),
        errors,
    )


def main() -> int:
    errors: list[str] = []
    validate_patch(errors)
    validate_design_data(errors)
    validate_build_notes(errors)

    if errors:
        print("Silph Scope return validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Silph Scope return validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
