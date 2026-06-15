#!/usr/bin/env python3
"""Validate the native Route 12 Snorlax wake slice."""

from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
NATIVE = ROOT / "native" / "nexus-red"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def require_file(path: Path, errors: list[str]) -> str:
    if not path.exists():
        errors.append(f"Missing required file: {path.relative_to(ROOT)}")
        return ""
    return read(path)


def validate_files() -> list[str]:
    errors: list[str] = []
    files = {
        "main": NATIVE / "src" / "Main.gd",
        "save": NATIVE / "src" / "save" / "SaveState.gd",
        "fuji_script": NATIVE / "src" / "world" / "PokemonTowerFujiRescue.gd",
        "route12_scene": NATIVE / "scenes" / "world" / "Route12SnorlaxWake.tscn",
        "route12_script": NATIVE / "src" / "world" / "Route12SnorlaxWake.gd",
        "encounter_data": NATIVE / "content" / "encounters" / "route_12_snorlax_static.json",
        "worldlink": NATIVE / "src" / "worldlink" / "WorldLinkPanel.gd",
        "worldlink_batch": NATIVE / "content" / "worldlink" / "route_12_snorlax_wake_batch.json",
        "test": NATIVE / "tests" / "route12_snorlax_wake_test.gd",
    }
    contents = {name: require_file(path, errors) for name, path in files.items()}
    if errors:
        return errors

    batch = json.loads(contents["worldlink_batch"])
    if batch.get("id") != "route_12_snorlax_wake_batch":
        errors.append("Route 12 Snorlax WorldLink batch must use id route_12_snorlax_wake_batch")
    ids = {item.get("id") for item in batch.get("feed", [])}
    for message_id in [
        "wl_route_12_snorlax_wake_reached",
        "wl_red_route_12_flute_guard",
        "wl_bill_poke_flute_signal_confirmed",
        "wl_snorlax_static_encounter_seen",
        "wl_team_moonlight_sleep_echo_cleared",
        "wl_snorlax_roadblock_cleared",
        "wl_route_12_south_path_unlocked",
    ]:
        if message_id not in ids:
            errors.append(f"Route 12 Snorlax WorldLink batch missing id: {message_id}")

    encounter = json.loads(contents["encounter_data"])
    if encounter.get("id") != "route_12_snorlax_static":
        errors.append("Route 12 Snorlax static encounter must use id route_12_snorlax_static")
    if encounter.get("species") != "Snorlax":
        errors.append("Route 12 static encounter species must be Snorlax")
    if encounter.get("return_scene") != "route_12_snorlax_wake":
        errors.append("Route 12 Snorlax static encounter must return to route_12_snorlax_wake")

    markers = {
        "main": (
            "Route12SnorlaxWakeScene",
            "_on_go_to_route_12_snorlax_wake",
            "_show_route_12_snorlax_wake",
            "go_to_route_12_snorlax_wake",
            "route_12_snorlax_wake",
        ),
        "save": (
            "route_12_snorlax_wake_reached",
            "red_route_12_flute_guard_seen",
            "bill_poke_flute_signal_confirmed",
            "snorlax_static_encounter_seen",
            "team_moonlight_sleep_echo_cleared",
            "snorlax_roadblock_cleared",
            "route_12_south_path_unlocked",
            "queue_route_12_snorlax_wake_batch",
        ),
        "fuji_script": (
            "go_to_route_12_snorlax_wake",
            "trigger_route_12_snorlax_wake_path",
            "poke_flute_obtained",
            "snorlax_wake_path_unlocked",
        ),
        "route12_script": (
            "Route 12 - Snorlax Wake",
            "start_wild_encounter",
            "trigger_route_12_snorlax_wake_scene",
            "trigger_snorlax_static_encounter",
            "record_route_12_snorlax_wake_scene",
            "go_to_pokemon_tower_fuji_rescue",
            "Red",
            "Bill",
            "Poke Flute",
            "Snorlax",
            "Moonlight",
            "Route 12",
        ),
        "worldlink": (
            "ROUTE_12_SNORLAX_WAKE_BATCH_PATH",
            "Reach Route 12 Snorlax",
            "Wake Snorlax",
            "Clear Snorlax roadblock",
            "Unlock Route 12 south path",
        ),
        "test": (
            "route12_snorlax_wake_test",
            "trigger_route_12_snorlax_wake_path",
            "trigger_route_12_snorlax_wake_scene",
            "trigger_snorlax_static_encounter",
            "route_12_snorlax_static",
            "snorlax_roadblock_cleared",
        ),
    }
    for name, expected_markers in markers.items():
        for marker in expected_markers:
            if marker not in contents[name]:
                errors.append(f"{files[name].relative_to(ROOT)} missing marker: {marker}")

    return errors


def main() -> int:
    errors = validate_files()
    if errors:
        print("Native Route 12 Snorlax wake validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print("Native Route 12 Snorlax wake validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
