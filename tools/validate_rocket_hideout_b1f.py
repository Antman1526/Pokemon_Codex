#!/usr/bin/env python3
"""Validate the Rocket Hideout B1F infiltration slice."""

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
    patch_path = ROOT / "patches/engine/0020-rocket-hideout-b1f.patch"
    if not patch_path.exists():
        errors.append("Missing patches/engine/0020-rocket-hideout-b1f.patch")
        return

    patch = patch_path.read_text(encoding="utf-8")
    require_markers(
        "Rocket Hideout B1F patch",
        patch,
        (
            "data/maps/RocketHideout_B1F_Frlg/scripts.inc",
            "data/maps/RocketHideout_B1F_Frlg/map.json",
            "RocketHideout_B1F_EventScript_RedInfiltrationCheck",
            "RocketHideout_B1F_EventScript_PortablePcBeta",
            "RocketHideout_B1F_EventScript_GoldDustLedger",
            "OBJ_EVENT_GFX_RED",
            "EventScript_PC",
            "Portable PC beta",
            "Team Gold Dust",
            "Gold Dust ledger",
            "WorldLink",
            "Silph Scope",
            "Rocket logistics",
            "Celadon buyer",
        ),
        errors,
    )


def validate_design_data(errors: list[str]) -> None:
    chapter = read("data_design/kanto_chapter.yaml")
    require_markers(
        "kanto_chapter",
        chapter,
        (
            "rocket_hideout_b1f_infiltration",
            "red_hideout_entry_check",
            "rocket_coin_logistics",
            "gold_dust_ledger_clue",
            "portable_pc_beta_terminal",
        ),
        errors,
    )

    messages = read("data_design/kanto_worldlink_messages.yaml")
    require_markers(
        "kanto_worldlink_messages",
        messages,
        (
            "WL_KANTO_ROCKET_HIDEOUT_B1F",
            "WL_KANTO_GOLD_DUST_LEDGER",
            "WL_KANTO_PORTABLE_PC_BETA",
            "Rocket Hideout",
            "Gold Dust ledger",
            "Portable PC beta",
        ),
        errors,
    )

    rivals = read("data_design/rival_progression_kanto.yaml")
    require_markers(
        "rival_progression_kanto",
        rivals,
        (
            "rocket_hideout_b1f_infiltration",
            "red_hideout_entry_check",
            "misty_hideout_current_call",
            "brock_hideout_grounding_call",
            "blue_hideout_race",
            "ava_gold_dust_ledger_research",
            "dax_hideout_training_report",
            "lyra_hideout_locked_profile",
        ),
        errors,
    )


def validate_build_notes(errors: list[str]) -> None:
    notes = read("build_notes/FIRST_PLAYABLE_OPENEMU_SMOKE_TEST.md")
    require_markers(
        "build notes",
        notes,
        (
            "0020-rocket-hideout-b1f.patch",
            "validate_rocket_hideout_b1f.py",
            "Rocket Hideout B1F",
            "Portable PC beta",
        ),
        errors,
    )


def main() -> int:
    errors: list[str] = []
    validate_patch(errors)
    validate_design_data(errors)
    validate_build_notes(errors)

    if errors:
        print("Rocket Hideout B1F validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Rocket Hideout B1F validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
