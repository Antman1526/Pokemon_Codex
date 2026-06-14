#!/usr/bin/env python3
"""Validate the Route 12 Snorlax and Fuchsia arrival slice."""

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
    patch_path = ROOT / "patches/engine/0023-route12-snorlax-fuchsia.patch"
    if not patch_path.exists():
        errors.append("Missing patches/engine/0023-route12-snorlax-fuchsia.patch")
        return

    patch = patch_path.read_text(encoding="utf-8")
    require_markers(
        "Route 12 Snorlax Fuchsia patch",
        patch,
        (
            "data/maps/Route12_Frlg/map.json",
            "data/maps/Route12_Frlg/scripts.inc",
            "data/maps/FuchsiaCity_Frlg/map.json",
            "data/maps/FuchsiaCity_Frlg/scripts.inc",
            "OBJ_EVENT_GFX_RED",
            "OBJ_EVENT_GFX_MISTY",
            "FuchsiaCity_EventScript_DaxArrival",
            "Route12_EventScript_RedSnorlaxSupport",
            "Route12_EventScript_MistySnorlaxSupport",
            "SNORLAX",
            "POKé FLUTE",
            "WorldLink",
            "FUCHSIA",
            "SAFARI ZONE",
            "KOGA",
            "SAFFRON",
            "Gold Dust",
        ),
        errors,
    )


def validate_design_data(errors: list[str]) -> None:
    chapter = read("data_design/kanto_chapter.yaml")
    require_markers(
        "kanto_chapter",
        chapter,
        (
            "route12_snorlax_poke_flute_gate",
            "red_misty_snorlax_support",
            "dax_snorlax_rival_pressure",
            "fuchsia_arrival_safari_koga_hook",
            "saffron_pressure_deferred",
        ),
        errors,
    )

    messages = read("data_design/kanto_worldlink_messages.yaml")
    require_markers(
        "kanto_worldlink_messages",
        messages,
        (
            "WL_KANTO_ROUTE12_SNORLAX_AWAKENED",
            "WL_KANTO_FUCHSIA_PATH_OPEN",
            "WL_KANTO_SAFFRON_PRESSURE_DEFERRED",
            "Snorlax",
            "Fuchsia",
            "Safari Zone",
            "Saffron",
        ),
        errors,
    )

    rivals = read("data_design/rival_progression_kanto.yaml")
    require_markers(
        "rival_progression_kanto",
        rivals,
        (
            "route12_snorlax_fuchsia_path",
            "red_snorlax_field_support",
            "misty_fuchsia_current_advice",
            "dax_snorlax_wakeup_report",
            "blue_saffron_impatience_warning",
            "ava_safari_rare_habitat_research",
        ),
        errors,
    )


def validate_build_notes(errors: list[str]) -> None:
    notes = read("build_notes/FIRST_PLAYABLE_OPENEMU_SMOKE_TEST.md")
    require_markers(
        "build notes",
        notes,
        (
            "0023-route12-snorlax-fuchsia.patch",
            "validate_route12_snorlax_fuchsia.py",
            "Route 12 Snorlax",
            "Fuchsia arrival",
            "Safari/Koga hook",
        ),
        errors,
    )


def main() -> int:
    errors: list[str] = []
    validate_patch(errors)
    validate_design_data(errors)
    validate_build_notes(errors)

    if errors:
        print("Route 12 Snorlax Fuchsia validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Route 12 Snorlax Fuchsia validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
