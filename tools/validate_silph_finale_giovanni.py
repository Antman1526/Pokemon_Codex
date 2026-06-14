#!/usr/bin/env python3
"""Validate the Silph upper floors, Giovanni finale, and Master Ball payoff slice."""

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
    patch_path = ROOT / "patches/engine/0028-silph-finale-giovanni.patch"
    if not patch_path.exists():
        errors.append("Missing patches/engine/0028-silph-finale-giovanni.patch")
        return

    patch = patch_path.read_text(encoding="utf-8")
    require_markers(
        "Silph finale patch",
        patch,
        (
            "data/maps/SilphCo_8F_Frlg/scripts.inc",
            "data/maps/SilphCo_9F_Frlg/scripts.inc",
            "data/maps/SilphCo_10F_Frlg/map.json",
            "data/maps/SilphCo_10F_Frlg/scripts.inc",
            "data/maps/SilphCo_11F_Frlg/scripts.inc",
            "SilphCo_10F_EventScript_RedBoardroomCheck",
            "Meridian Gate",
            "Master Ball",
            "WorldLink",
            "Moonlight",
            "Sabrina",
            "Gold Dust",
            "Red",
            "Giovanni",
        ),
        errors,
    )


def validate_design_data(errors: list[str]) -> None:
    chapter = read("data_design/kanto_chapter.yaml")
    require_markers(
        "kanto_chapter",
        chapter,
        (
            "silph_8f_buyer_network_evidence",
            "silph_9f_emergency_heal_hub",
            "silph_10f_red_final_stair_check",
            "silph_11f_giovanni_meridian_gate",
            "master_ball_worldlink_payoff",
            "sabrina_moonlight_handoff",
        ),
        errors,
    )

    messages = read("data_design/kanto_worldlink_messages.yaml")
    require_markers(
        "kanto_worldlink_messages",
        messages,
        (
            "WL_KANTO_SILPH_UPPER_FLOORS",
            "WL_KANTO_RED_BOARDROOM_CHECK",
            "WL_KANTO_GIOVANNI_MERIDIAN_GATE",
            "WL_KANTO_MASTER_BALL_RESTORED",
            "WL_KANTO_SABRINA_MOONLIGHT_HANDOFF",
        ),
        errors,
    )

    rivals = read("data_design/rival_progression_kanto.yaml")
    require_markers(
        "rival_progression_kanto",
        rivals,
        (
            "silph_finale_giovanni_master_ball",
            "red_final_stair_check",
            "misty_post_silph_calm",
            "brock_master_ball_warning",
            "blue_post_silph_silence",
            "ava_meridian_gate_analysis",
            "dax_rocket_floor_count_finale",
        ),
        errors,
    )


def validate_docs(errors: list[str]) -> None:
    spec = read("docs/superpowers/specs/2026-06-14-silph-finale-giovanni-design.md")
    require_markers(
        "Silph finale spec",
        spec,
        (
            "Silph Finale and Giovanni Design",
            "Red reaches the final stair",
            "Giovanni calls Silph the first Meridian Gate",
            "Master Ball is a responsibility, not a trophy",
            "Sabrina becomes the next required Kanto chapter",
        ),
        errors,
    )

    notes = read("build_notes/FIRST_PLAYABLE_OPENEMU_SMOKE_TEST.md")
    require_markers(
        "build notes",
        notes,
        (
            "0028-silph-finale-giovanni.patch",
            "validate_silph_finale_giovanni.py",
            "Silph 10F Red boardroom check",
            "Silph 11F Giovanni Meridian Gate speech",
            "Master Ball WorldLink payoff",
            "Sabrina Moonlight handoff",
        ),
        errors,
    )


def main() -> int:
    errors: list[str] = []
    validate_patch(errors)
    validate_design_data(errors)
    validate_docs(errors)

    if errors:
        print("Silph finale Giovanni validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Silph finale Giovanni validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
