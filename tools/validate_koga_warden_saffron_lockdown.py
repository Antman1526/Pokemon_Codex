#!/usr/bin/env python3
"""Validate the Koga Warden notes and Saffron lockdown slice."""

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
    patch_path = ROOT / "patches/engine/0025-koga-warden-saffron-lockdown.patch"
    if not patch_path.exists():
        errors.append("Missing patches/engine/0025-koga-warden-saffron-lockdown.patch")
        return

    patch = patch_path.read_text(encoding="utf-8")
    require_markers(
        "Koga Warden Saffron patch",
        patch,
        (
            "data/maps/FuchsiaCity_Gym_Frlg/scripts.inc",
            "data/maps/FuchsiaCity_WardensHouse_Frlg/scripts.inc",
            "data/maps/SaffronCity_Frlg/scripts.inc",
            "Soul Badge",
            "status trial",
            "WARDEN",
            "habitat notes",
            "Gold Dust",
            "WorldLink",
            "SAFFRON",
            "SILPH",
            "Blue",
        ),
        errors,
    )


def validate_design_data(errors: list[str]) -> None:
    chapter = read("data_design/kanto_chapter.yaml")
    require_markers(
        "kanto_chapter",
        chapter,
        (
            "koga_status_trial",
            "soul_badge_worldlink_handoff",
            "warden_habitat_notes_stolen",
            "saffron_lockdown_after_fuchsia",
            "blue_saffron_security_loss",
        ),
        errors,
    )

    messages = read("data_design/kanto_worldlink_messages.yaml")
    require_markers(
        "kanto_worldlink_messages",
        messages,
        (
            "WL_KANTO_KOGA_SOUL_BADGE_CLEAR",
            "WL_KANTO_WARDEN_NOTES_STOLEN",
            "WL_KANTO_SAFFRON_LOCKDOWN_HANDOFF",
            "Soul Badge",
            "Gold Dust",
            "Silph",
        ),
        errors,
    )

    rivals = read("data_design/rival_progression_kanto.yaml")
    require_markers(
        "rival_progression_kanto",
        rivals,
        (
            "koga_warden_saffron_lockdown",
            "red_soul_badge_debrief",
            "misty_status_recovery_check",
            "brock_full_heal_advice",
            "blue_saffron_security_loss",
            "ava_warden_notes_theft",
            "dax_koga_badge_race",
        ),
        errors,
    )


def validate_build_notes(errors: list[str]) -> None:
    notes = read("build_notes/FIRST_PLAYABLE_OPENEMU_SMOKE_TEST.md")
    require_markers(
        "build notes",
        notes,
        (
            "0025-koga-warden-saffron-lockdown.patch",
            "validate_koga_warden_saffron_lockdown.py",
            "Koga status trial",
            "Warden notes theft",
            "Saffron lockdown handoff",
        ),
        errors,
    )


def main() -> int:
    errors: list[str] = []
    validate_patch(errors)
    validate_design_data(errors)
    validate_build_notes(errors)

    if errors:
        print("Koga Warden Saffron validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Koga Warden Saffron validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
