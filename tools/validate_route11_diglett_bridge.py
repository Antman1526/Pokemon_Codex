#!/usr/bin/env python3
"""Validate the Route 11 and Diglett's Cave bridge slice."""

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
    patch_path = ROOT / "patches/engine/0016-route11-diglett-bridge.patch"
    if not patch_path.exists():
        errors.append("Missing patches/engine/0016-route11-diglett-bridge.patch")
        return

    patch = patch_path.read_text(encoding="utf-8")
    require_markers(
        "Route 11 Diglett bridge patch",
        patch,
        (
            "data/maps/Route11_Frlg/map.json",
            "OBJ_EVENT_GFX_RED",
            "OBJ_EVENT_GFX_BLUE",
            "Route11_EventScript_RedTrailCutter",
            "Route11_EventScript_BlueRivalRace",
            "Trail Cutter",
            "WorldLink",
            "ROCK TUNNEL",
            "DIGLETT'S CAVE",
            "not a region shortcut",
            "Checklist",
        ),
        errors,
    )


def validate_design_data(errors: list[str]) -> None:
    chapter = read("data_design/kanto_chapter.yaml")
    require_markers(
        "kanto_chapter",
        chapter,
        (
            "route_11",
            "digletts_cave",
            "route11_rival_race_checkpoint",
            "diglett_cave_trail_cutter_ground_ping",
            "brock_rock_tunnel_field_advice",
            "rock_tunnel_checklist_handoff",
        ),
        errors,
    )

    messages = read("data_design/kanto_worldlink_messages.yaml")
    require_markers(
        "kanto_worldlink_messages",
        messages,
        (
            "WL_KANTO_ROUTE11_RIVAL_RACE",
            "WL_KANTO_DIGLETT_TRAIL_CUTTER_PING",
            "WL_KANTO_ROCK_TUNNEL_CHECKLIST",
            "Blue is pressing east on Route 11",
            "Trail Cutter registered underground movement",
            "Rock Tunnel checklist",
        ),
        errors,
    )

    rivals = read("data_design/rival_progression_kanto.yaml")
    require_markers(
        "rival_progression_kanto",
        rivals,
        (
            "route11_diglett_bridge",
            "warm_route11_field_tool_guidance",
            "rock_tunnel_field_advice",
            "rival_race_pressure",
            "ground_route_research",
            "engineer_training_loss",
            "lyra_signal_remains_locked",
        ),
        errors,
    )


def validate_build_notes(errors: list[str]) -> None:
    notes = read("build_notes/FIRST_PLAYABLE_OPENEMU_SMOKE_TEST.md")
    require_markers(
        "build notes",
        notes,
        (
            "0016-route11-diglett-bridge.patch",
            "validate_route11_diglett_bridge.py",
            "Route 11 rival-race checkpoint",
            "Diglett's Cave Trail Cutter",
        ),
        errors,
    )


def main() -> int:
    errors: list[str] = []
    validate_patch(errors)
    validate_design_data(errors)
    validate_build_notes(errors)

    if errors:
        print("Route 11 Diglett bridge validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Route 11 Diglett bridge validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
