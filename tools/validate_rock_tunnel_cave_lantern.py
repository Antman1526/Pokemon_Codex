#!/usr/bin/env python3
"""Validate the Rock Tunnel Cave Lantern slice."""

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
    patch_path = ROOT / "patches/engine/0017-rock-tunnel-cave-lantern.patch"
    if not patch_path.exists():
        errors.append("Missing patches/engine/0017-rock-tunnel-cave-lantern.patch")
        return

    patch = patch_path.read_text(encoding="utf-8")
    require_markers(
        "Rock Tunnel Cave Lantern patch",
        patch,
        (
            "data/maps/Route10_PokemonCenter_1F_Frlg/map.json",
            "data/maps/RockTunnel_1F_Frlg/scripts.inc",
            "data/maps/RockTunnel_B1F_Frlg/scripts.inc",
            "data/maps/LavenderTown_Frlg/scripts.inc",
            "OBJ_EVENT_GFX_BROCK",
            "OBJ_EVENT_GFX_RED",
            "Route10_PokemonCenter_1F_EventScript_BrockCaveLantern",
            "RockTunnel_1F_EventScript_RedCaveLantern",
            "RockTunnel_B1F_EventScript_MoonlightEcho",
            "FLAG_SYS_USE_FLASH",
            "FLAG_BADGE03_GET",
            "Cave Lantern",
            "WorldLink",
            "Thunder Badge",
            "Moonlight Echo",
            "low-light static",
        ),
        errors,
    )


def validate_design_data(errors: list[str]) -> None:
    chapter = read("data_design/kanto_chapter.yaml")
    require_markers(
        "kanto_chapter",
        chapter,
        (
            "cave_lantern_auto_flash_protocol",
            "brock_route10_cave_lantern_advice",
            "red_rock_tunnel_companion_check",
            "moonlight_echo_low_light_static",
            "lavender_low_light_static_arrival",
        ),
        errors,
    )

    messages = read("data_design/kanto_worldlink_messages.yaml")
    require_markers(
        "kanto_worldlink_messages",
        messages,
        (
            "WL_KANTO_CAVE_LANTERN_READY",
            "WL_KANTO_RED_ROCK_TUNNEL_CHECK",
            "WL_KANTO_MOONLIGHT_ECHO",
            "Cave Lantern protocol",
            "Red entered Rock Tunnel",
            "Moonlight Echo",
        ),
        errors,
    )

    rivals = read("data_design/rival_progression_kanto.yaml")
    require_markers(
        "rival_progression_kanto",
        rivals,
        (
            "rock_tunnel_lavender_approach",
            "brock_cave_lantern_advice",
            "warm_rock_tunnel_companion_check",
            "lavender_tower_waterline_warning",
            "pokemon_tower_race_pressure",
            "low_light_static_research",
            "route10_training_report",
            "lyra_tower_signal_locked",
        ),
        errors,
    )


def validate_build_notes(errors: list[str]) -> None:
    notes = read("build_notes/FIRST_PLAYABLE_OPENEMU_SMOKE_TEST.md")
    require_markers(
        "build notes",
        notes,
        (
            "0017-rock-tunnel-cave-lantern.patch",
            "validate_rock_tunnel_cave_lantern.py",
            "Rock Tunnel Cave Lantern",
            "Moonlight Echo",
        ),
        errors,
    )


def main() -> int:
    errors: list[str] = []
    validate_patch(errors)
    validate_design_data(errors)
    validate_build_notes(errors)

    if errors:
        print("Rock Tunnel Cave Lantern validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Rock Tunnel Cave Lantern validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
