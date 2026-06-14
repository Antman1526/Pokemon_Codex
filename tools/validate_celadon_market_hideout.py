#!/usr/bin/env python3
"""Validate the Celadon market and Game Corner hideout slice."""

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
    patch_path = ROOT / "patches/engine/0019-celadon-market-hideout.patch"
    if not patch_path.exists():
        errors.append("Missing patches/engine/0019-celadon-market-hideout.patch")
        return

    patch = patch_path.read_text(encoding="utf-8")
    require_markers(
        "Celadon market hideout patch",
        patch,
        (
            "data/maps/CeladonCity_Restaurant_Frlg/scripts.inc",
            "data/maps/CeladonCity_Restaurant_Frlg/map.json",
            "data/maps/CeladonCity_GameCorner_Frlg/scripts.inc",
            "data/maps/CeladonCity_DepartmentStore_2F_Frlg/scripts.inc",
            "data/maps/CeladonCity_DepartmentStore_2F_Frlg/map.json",
            "data/maps/CeladonCity_Gym_Frlg/scripts.inc",
            "CeladonCity_Restaurant_EventScript_GoldDustBuyer",
            "Team Gold Dust",
            "Celadon buyer",
            "Rocket Game Corner",
            "WorldLink",
            "ITEM_ABILITY_CAPSULE",
            "Ability Capsule",
            "CeladonCity_DepartmentStore_2F_EventScript_AbilityCapsuleVendor",
            "Erika",
        ),
        errors,
    )


def validate_design_data(errors: list[str]) -> None:
    chapter = read("data_design/kanto_chapter.yaml")
    require_markers(
        "kanto_chapter",
        chapter,
        (
            "celadon_gold_dust_buyer",
            "rocket_game_corner_worldlink_pulse",
            "ability_capsule_vendor_field_trial",
            "erika_market_warning",
        ),
        errors,
    )

    messages = read("data_design/kanto_worldlink_messages.yaml")
    require_markers(
        "kanto_worldlink_messages",
        messages,
        (
            "WL_KANTO_CELADON_MARKET_SIGNAL",
            "WL_KANTO_GAME_CORNER_HIDEOUT",
            "WL_KANTO_ABILITY_CAPSULE_TRIAL",
            "WL_KANTO_ERIKA_MARKET_WARNING",
            "Ability Capsule",
            "Gold Dust",
            "Rocket Game Corner",
        ),
        errors,
    )

    rivals = read("data_design/rival_progression_kanto.yaml")
    require_markers(
        "rival_progression_kanto",
        rivals,
        (
            "celadon_market_hideout",
            "red_celadon_market_watch",
            "misty_celadon_current_call",
            "brock_celadon_patience_call",
            "blue_game_corner_race",
            "ava_gold_dust_buyer_research",
            "dax_celadon_arcade_report",
            "lyra_celadon_locked_profile",
        ),
        errors,
    )


def validate_build_notes(errors: list[str]) -> None:
    notes = read("build_notes/FIRST_PLAYABLE_OPENEMU_SMOKE_TEST.md")
    require_markers(
        "build notes",
        notes,
        (
            "0019-celadon-market-hideout.patch",
            "validate_celadon_market_hideout.py",
            "Celadon market hideout",
            "Ability Capsule",
        ),
        errors,
    )


def main() -> int:
    errors: list[str] = []
    validate_patch(errors)
    validate_design_data(errors)
    validate_build_notes(errors)

    if errors:
        print("Celadon market hideout validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Celadon market hideout validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
