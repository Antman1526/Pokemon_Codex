#!/usr/bin/env python3
"""Validate the Safari Gold Dust Field Log slice."""

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
    patch_path = ROOT / "patches/engine/0024-safari-gold-dust-field-log.patch"
    if not patch_path.exists():
        errors.append("Missing patches/engine/0024-safari-gold-dust-field-log.patch")
        return

    patch = patch_path.read_text(encoding="utf-8")
    require_markers(
        "Safari Gold Dust patch",
        patch,
        (
            "data/maps/FuchsiaCity_SafariZone_Entrance_Frlg/map.json",
            "data/maps/FuchsiaCity_SafariZone_Entrance_Frlg/scripts.inc",
            "data/maps/FuchsiaCity_SafariZone_Office_Frlg/map.json",
            "data/maps/FuchsiaCity_SafariZone_Office_Frlg/scripts.inc",
            "FuchsiaCity_SafariZone_Entrance_EventScript_AvaFieldLog",
            "FuchsiaCity_SafariZone_Office_EventScript_GoldDustScout",
            "WorldLink",
            "Safari Field Log",
            "Gold Dust",
            "SAFARI ZONE",
            "KOGA",
            "WARDEN",
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
            "safari_field_log_checklist",
            "ava_safari_research_scene",
            "gold_dust_safari_scout",
            "warden_prize_route_tease",
            "koga_status_preparation",
            "saffron_after_safari_pressure",
        ),
        errors,
    )

    messages = read("data_design/kanto_worldlink_messages.yaml")
    require_markers(
        "kanto_worldlink_messages",
        messages,
        (
            "WL_KANTO_SAFARI_FIELD_LOG",
            "WL_KANTO_GOLD_DUST_SAFARI_SCOUT",
            "WL_KANTO_KOGA_STATUS_PREP",
            "Safari Field Log",
            "Gold Dust",
            "Koga",
        ),
        errors,
    )

    rivals = read("data_design/rival_progression_kanto.yaml")
    require_markers(
        "rival_progression_kanto",
        rivals,
        (
            "safari_gold_dust_field_log",
            "ava_safari_field_log",
            "dax_safari_competition",
            "blue_saffron_loss_rumor",
            "red_misty_fuchsia_check",
        ),
        errors,
    )


def validate_build_notes(errors: list[str]) -> None:
    notes = read("build_notes/FIRST_PLAYABLE_OPENEMU_SMOKE_TEST.md")
    require_markers(
        "build notes",
        notes,
        (
            "0024-safari-gold-dust-field-log.patch",
            "validate_safari_gold_dust_field_log.py",
            "Safari Field Log",
            "Gold Dust scout",
            "Koga status prep",
        ),
        errors,
    )


def main() -> int:
    errors: list[str] = []
    validate_patch(errors)
    validate_design_data(errors)
    validate_build_notes(errors)

    if errors:
        print("Safari Gold Dust Field Log validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Safari Gold Dust Field Log validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
