#!/usr/bin/env python3
"""Validate the Rocket Hideout Giovanni and Silph Scope payoff slice."""

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
    patch_path = ROOT / "patches/engine/0021-giovanni-silph-scope.patch"
    if not patch_path.exists():
        errors.append("Missing patches/engine/0021-giovanni-silph-scope.patch")
        return

    patch = patch_path.read_text(encoding="utf-8")
    require_markers(
        "Giovanni Silph Scope patch",
        patch,
        (
            "data/maps/RocketHideout_B3F_Frlg/map.json",
            "data/maps/RocketHideout_B3F_Frlg/scripts.inc",
            "data/maps/RocketHideout_B4F_Frlg/map.json",
            "data/maps/RocketHideout_B4F_Frlg/scripts.inc",
            "OBJ_EVENT_GFX_BLUE",
            "OBJ_EVENT_GFX_RED",
            "RocketHideout_B3F_EventScript_BlueLateArrival",
            "RocketHideout_B4F_EventScript_RedGiovanniCheck",
            "RocketHideout_B4F_Text_SilphScopeWorldLink",
            "Meridian prototype",
            "Silph Scope",
            "WorldLink",
            "Portable PC beta",
            "Lavender Tower",
            "Team Rocket",
        ),
        errors,
    )


def validate_design_data(errors: list[str]) -> None:
    chapter = read("data_design/kanto_chapter.yaml")
    require_markers(
        "kanto_chapter",
        chapter,
        (
            "rocket_hideout_blue_late_arrival",
            "red_giovanni_preboss_check",
            "giovanni_meridian_prototype_hint",
            "silph_scope_worldlink_return",
            "portable_pc_beta_storage_handshake",
        ),
        errors,
    )

    messages = read("data_design/kanto_worldlink_messages.yaml")
    require_markers(
        "kanto_worldlink_messages",
        messages,
        (
            "WL_KANTO_BLUE_HIDEOUT_LATE",
            "WL_KANTO_GIOVANNI_MERIDIAN_HINT",
            "WL_KANTO_SILPH_SCOPE_RETURN",
            "Meridian prototype",
            "Silph Scope",
            "Lavender Tower",
            "Portable PC beta",
        ),
        errors,
    )

    rivals = read("data_design/rival_progression_kanto.yaml")
    require_markers(
        "rival_progression_kanto",
        rivals,
        (
            "giovanni_silph_scope_payoff",
            "red_giovanni_preboss_check",
            "blue_hideout_late_arrival",
            "ava_meridian_signal_research",
            "dax_giovanni_training_report",
            "misty_silph_scope_return_call",
            "brock_giovanni_grounding_call",
            "lyra_meridian_locked_profile",
        ),
        errors,
    )


def validate_build_notes(errors: list[str]) -> None:
    notes = read("build_notes/FIRST_PLAYABLE_OPENEMU_SMOKE_TEST.md")
    require_markers(
        "build notes",
        notes,
        (
            "0021-giovanni-silph-scope.patch",
            "validate_giovanni_silph_scope.py",
            "Giovanni Silph Scope",
            "Meridian prototype",
        ),
        errors,
    )


def main() -> int:
    errors: list[str] = []
    validate_patch(errors)
    validate_design_data(errors)
    validate_build_notes(errors)

    if errors:
        print("Giovanni Silph Scope validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Giovanni Silph Scope validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
