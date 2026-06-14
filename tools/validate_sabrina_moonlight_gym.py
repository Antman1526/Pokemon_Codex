#!/usr/bin/env python3
"""Validate the Saffron Gym Sabrina and Moonlight distortion slice."""

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
    patch_path = ROOT / "patches/engine/0029-sabrina-moonlight-gym.patch"
    if not patch_path.exists():
        errors.append("Missing patches/engine/0029-sabrina-moonlight-gym.patch")
        return

    patch = patch_path.read_text(encoding="utf-8")
    require_markers(
        "Sabrina Moonlight patch",
        patch,
        (
            "data/maps/SaffronCity_Frlg/map.json",
            "data/maps/SaffronCity_Frlg/scripts.inc",
            "data/maps/SaffronCity_Gym_Frlg/map.json",
            "data/maps/SaffronCity_Gym_Frlg/scripts.inc",
            "SaffronCity_EventScript_RedSabrinaGate",
            "SaffronCity_EventScript_MistySabrinaGate",
            "SaffronCity_Gym_EventScript_MoonlightVeil",
            "Moonlight Veil",
            "Marsh Badge",
            "WorldLink",
            "Red",
            "Misty",
            "Sabrina",
        ),
        errors,
    )


def validate_design_data(errors: list[str]) -> None:
    chapter = read("data_design/kanto_chapter.yaml")
    require_markers(
        "kanto_chapter",
        chapter,
        (
            "sabrina_gym_moonlight_distortion",
            "red_sabrina_gate_separation",
            "misty_saffron_current_support",
            "moonlight_veil_gym_signal",
            "marsh_badge_worldlink_stabilized",
        ),
        errors,
    )

    messages = read("data_design/kanto_worldlink_messages.yaml")
    require_markers(
        "kanto_worldlink_messages",
        messages,
        (
            "WL_KANTO_SABRINA_GYM_DISTORTION",
            "WL_KANTO_RED_MISTY_SABRINA_GATE",
            "WL_KANTO_MARSH_BADGE_STABILIZED",
        ),
        errors,
    )

    rivals = read("data_design/rival_progression_kanto.yaml")
    require_markers(
        "rival_progression_kanto",
        rivals,
        (
            "sabrina_moonlight_gym",
            "red_sabrina_gate_separation",
            "misty_saffron_current_support",
            "brock_psychic_grounding_note",
            "blue_post_silph_sabrina_silence",
            "ava_moonlight_veil_analysis",
            "dax_psychic_gym_warning",
        ),
        errors,
    )


def validate_docs(errors: list[str]) -> None:
    spec = read("docs/superpowers/specs/2026-06-14-sabrina-moonlight-gym-design.md")
    require_markers(
        "Sabrina Moonlight spec",
        spec,
        (
            "Sabrina Moonlight Gym Design",
            "Red cannot enter with Antman",
            "Misty steadies the city outside",
            "Moonlight Veil",
            "Sabrina remains the Gym Leader, not a villain",
        ),
        errors,
    )

    notes = read("build_notes/FIRST_PLAYABLE_OPENEMU_SMOKE_TEST.md")
    require_markers(
        "build notes",
        notes,
        (
            "0029-sabrina-moonlight-gym.patch",
            "validate_sabrina_moonlight_gym.py",
            "Saffron Red Sabrina gate scene",
            "Saffron Misty Sabrina support scene",
            "Saffron Gym Moonlight Veil",
            "Marsh Badge WorldLink stabilization",
        ),
        errors,
    )


def main() -> int:
    errors: list[str] = []
    validate_patch(errors)
    validate_design_data(errors)
    validate_docs(errors)

    if errors:
        print("Sabrina Moonlight Gym validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Sabrina Moonlight Gym validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
