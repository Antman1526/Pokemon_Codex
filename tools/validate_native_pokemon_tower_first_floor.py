#!/usr/bin/env python3
"""Validate the native Pokemon Tower first floor slice."""

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
        "lavender_script": NATIVE / "src" / "world" / "LavenderOutskirts.gd",
        "tower_scene": NATIVE / "scenes" / "world" / "PokemonTowerFirstFloor.tscn",
        "tower_script": NATIVE / "src" / "world" / "PokemonTowerFirstFloor.gd",
        "worldlink": NATIVE / "src" / "worldlink" / "WorldLinkPanel.gd",
        "worldlink_batch": NATIVE / "content" / "worldlink" / "pokemon_tower_first_floor_batch.json",
        "test": NATIVE / "tests" / "pokemon_tower_first_floor_test.gd",
    }
    contents = {name: require_file(path, errors) for name, path in files.items()}
    if errors:
        return errors

    batch = json.loads(contents["worldlink_batch"])
    if batch.get("id") != "pokemon_tower_first_floor_batch":
        errors.append("Pokemon Tower first floor WorldLink batch must use id pokemon_tower_first_floor_batch")
    ids = {item.get("id") for item in batch.get("feed", [])}
    for message_id in [
        "wl_pokemon_tower_first_floor_reached",
        "wl_red_pokemon_tower_guard",
        "wl_bill_tower_echo_flute_distortion",
        "wl_team_moonlight_tower_pressure",
        "wl_rocket_tower_grunt_seen",
        "wl_cubone_mr_fuji_thread",
        "wl_silph_scope_need_seen",
        "wl_pokemon_tower_deeper_path_locked",
    ]:
        if message_id not in ids:
            errors.append(f"Pokemon Tower WorldLink batch missing id: {message_id}")

    markers = {
        "main": (
            "PokemonTowerFirstFloorScene",
            "_on_go_to_pokemon_tower_first_floor",
            "_show_pokemon_tower_first_floor",
            "go_to_pokemon_tower_first_floor",
        ),
        "save": (
            "pokemon_tower_first_floor_reached",
            "red_pokemon_tower_guard_seen",
            "bill_tower_echo_flute_distortion_seen",
            "team_moonlight_tower_pressure_seen",
            "rocket_tower_grunt_seen",
            "cubone_mr_fuji_thread_seen",
            "silph_scope_need_seen",
            "pokemon_tower_deeper_path_locked",
            "queue_pokemon_tower_first_floor_batch",
        ),
        "lavender_script": (
            "go_to_pokemon_tower_first_floor",
            "trigger_pokemon_tower_entry",
            "pokemon_tower_entry_unlocked",
            "Pokemon Tower",
        ),
        "tower_script": (
            "Pokemon Tower - First Floor",
            "trigger_pokemon_tower_first_floor_scene",
            "record_pokemon_tower_first_floor_scene",
            "trigger_deeper_tower_path",
            "go_to_lavender_outskirts",
            "Red",
            "Bill",
            "Moonlight",
            "Rocket",
            "Pokemon Tower",
            "Echo Flute",
            "Cubone",
            "Mr. Fuji",
            "Silph Scope",
        ),
        "worldlink": (
            "POKEMON_TOWER_FIRST_FLOOR_BATCH_PATH",
            "Enter Pokemon Tower",
            "Decode tower Echo Flute distortion",
            "Find Cubone and Mr. Fuji thread",
            "Lock deeper tower behind Silph Scope",
        ),
        "test": (
            "pokemon_tower_first_floor_test",
            "trigger_pokemon_tower_entry",
            "trigger_pokemon_tower_first_floor_scene",
            "trigger_deeper_tower_path",
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
        print("Native Pokemon Tower first floor validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print("Native Pokemon Tower first floor validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
