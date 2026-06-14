#!/usr/bin/env python3
"""Validate the Saffron arrival and Silph lower floors slice."""

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
    patch_path = ROOT / "patches/engine/0026-saffron-silph-lower-floors.patch"
    if not patch_path.exists():
        errors.append("Missing patches/engine/0026-saffron-silph-lower-floors.patch")
        return

    patch = patch_path.read_text(encoding="utf-8")
    require_markers(
        "Saffron Silph lower floors patch",
        patch,
        (
            "data/maps/SaffronCity_Frlg/map.json",
            "data/maps/SaffronCity_Frlg/scripts.inc",
            "data/maps/SilphCo_1F_Frlg/scripts.inc",
            "data/maps/SilphCo_2F_Frlg/scripts.inc",
            "data/maps/SilphCo_3F_Frlg/scripts.inc",
            "SaffronCity_EventScript_RedSilphArrival",
            "Silph lower floors",
            "WorldLink",
            "Rocket logistics",
            "Blue",
            "Gold Dust",
            "Portable PC",
            "SAFFRON",
            "SILPH",
        ),
        errors,
    )


def validate_design_data(errors: list[str]) -> None:
    chapter = read("data_design/kanto_chapter.yaml")
    require_markers(
        "kanto_chapter",
        chapter,
        (
            "saffron_arrival_companion_scene",
            "red_silph_split",
            "silph_lobby_lockdown",
            "silph_2f_rocket_logistics",
            "silph_3f_blue_pressure_clue",
            "portable_pc_full_teaser",
        ),
        errors,
    )

    messages = read("data_design/kanto_worldlink_messages.yaml")
    require_markers(
        "kanto_worldlink_messages",
        messages,
        (
            "WL_KANTO_SAFFRON_CITY_ARRIVAL",
            "WL_KANTO_SILPH_LOBBY_LOCKDOWN",
            "WL_KANTO_SILPH_LOWER_FLOORS",
            "Saffron",
            "Silph",
            "Portable PC",
        ),
        errors,
    )

    rivals = read("data_design/rival_progression_kanto.yaml")
    require_markers(
        "rival_progression_kanto",
        rivals,
        (
            "saffron_silph_lower_floors",
            "red_saffron_arrival_split",
            "misty_saffron_support",
            "brock_silph_system_warning",
            "blue_silph_pressure_clue",
            "ava_gold_dust_silph_buyer",
            "dax_saffron_badge_race",
        ),
        errors,
    )


def validate_build_notes(errors: list[str]) -> None:
    notes = read("build_notes/FIRST_PLAYABLE_OPENEMU_SMOKE_TEST.md")
    require_markers(
        "build notes",
        notes,
        (
            "0026-saffron-silph-lower-floors.patch",
            "validate_saffron_silph_lower_floors.py",
            "Saffron arrival",
            "Silph lower floors",
            "Red Silph split",
        ),
        errors,
    )


def main() -> int:
    errors: list[str] = []
    validate_patch(errors)
    validate_design_data(errors)
    validate_build_notes(errors)

    if errors:
        print("Saffron Silph lower floors validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Saffron Silph lower floors validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
