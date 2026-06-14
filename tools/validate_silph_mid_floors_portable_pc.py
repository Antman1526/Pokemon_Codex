#!/usr/bin/env python3
"""Validate the Silph mid-floors and Portable PC full-access slice."""

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
    patch_path = ROOT / "patches/engine/0027-silph-mid-floors-portable-pc.patch"
    if not patch_path.exists():
        errors.append("Missing patches/engine/0027-silph-mid-floors-portable-pc.patch")
        return

    patch = patch_path.read_text(encoding="utf-8")
    require_markers(
        "Silph mid-floors patch",
        patch,
        (
            "data/maps/SilphCo_4F_Frlg/scripts.inc",
            "data/maps/SilphCo_5F_Frlg/scripts.inc",
            "data/maps/SilphCo_5F_Frlg/map.json",
            "data/maps/SilphCo_6F_Frlg/scripts.inc",
            "data/maps/SilphCo_7F_Frlg/scripts.inc",
            "SilphCo_5F_EventScript_PortablePcFullAccess",
            "goto EventScript_PC",
            "Portable PC full access",
            "Gold Dust",
            "WorldLink",
            "Rocket logistics",
            "Red",
            "Blue",
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
            "silph_mid_floor_systems",
            "silph_4f_gold_dust_terminal",
            "silph_5f_portable_pc_full_unlock",
            "silph_6f_red_civilian_route",
            "silph_7f_blue_emotional_pressure",
            "portable_pc_full",
        ),
        errors,
    )

    messages = read("data_design/kanto_worldlink_messages.yaml")
    require_markers(
        "kanto_worldlink_messages",
        messages,
        (
            "WL_KANTO_SILPH_MID_FLOORS",
            "WL_KANTO_PORTABLE_PC_FULL_UNLOCK",
            "WL_KANTO_BLUE_SILPH_RIVAL_PRESSURE",
            "Portable PC full access",
            "Gold Dust terminal",
        ),
        errors,
    )

    rivals = read("data_design/rival_progression_kanto.yaml")
    require_markers(
        "rival_progression_kanto",
        rivals,
        (
            "silph_mid_floors_portable_pc",
            "red_civilian_route_update",
            "misty_saffron_exit_watch",
            "brock_portable_pc_systems",
            "blue_emotional_silph_rival",
            "ava_gold_dust_terminal_trace",
            "dax_silph_floor_count",
        ),
        errors,
    )


def validate_docs(errors: list[str]) -> None:
    spec = read("docs/superpowers/specs/2026-06-14-silph-mid-floors-portable-pc-design.md")
    require_markers(
        "Silph mid-floors spec",
        spec,
        (
            "Silph Mid-Floors and Portable PC Design",
            "Gold Dust terminal",
            "Portable PC full access",
            "Blue is not comic relief here",
        ),
        errors,
    )

    notes = read("build_notes/FIRST_PLAYABLE_OPENEMU_SMOKE_TEST.md")
    require_markers(
        "build notes",
        notes,
        (
            "0027-silph-mid-floors-portable-pc.patch",
            "validate_silph_mid_floors_portable_pc.py",
            "Silph 4F Gold Dust terminal",
            "Silph 5F Portable PC full access terminal",
            "Silph 7F Blue emotional pressure scene",
        ),
        errors,
    )


def main() -> int:
    errors: list[str] = []
    validate_patch(errors)
    validate_design_data(errors)
    validate_docs(errors)

    if errors:
        print("Silph mid-floors Portable PC validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Silph mid-floors Portable PC validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
