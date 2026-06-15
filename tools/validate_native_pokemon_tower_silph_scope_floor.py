#!/usr/bin/env python3
"""Validate the native Pokemon Tower Silph Scope floor slice."""

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
        "first_floor_script": NATIVE / "src" / "world" / "PokemonTowerFirstFloor.gd",
        "silph_scope_scene": NATIVE / "scenes" / "world" / "PokemonTowerSilphScopeFloor.tscn",
        "silph_scope_script": NATIVE / "src" / "world" / "PokemonTowerSilphScopeFloor.gd",
        "worldlink": NATIVE / "src" / "worldlink" / "WorldLinkPanel.gd",
        "worldlink_batch": NATIVE / "content" / "worldlink" / "pokemon_tower_silph_scope_floor_batch.json",
        "test": NATIVE / "tests" / "pokemon_tower_silph_scope_floor_test.gd",
    }
    contents = {name: require_file(path, errors) for name, path in files.items()}
    if errors:
        return errors

    batch = json.loads(contents["worldlink_batch"])
    if batch.get("id") != "pokemon_tower_silph_scope_floor_batch":
        errors.append("Pokemon Tower Silph Scope floor WorldLink batch must use id pokemon_tower_silph_scope_floor_batch")
    ids = {item.get("id") for item in batch.get("feed", [])}
    for message_id in [
        "wl_pokemon_tower_silph_scope_floor_reached",
        "wl_red_silph_scope_guard",
        "wl_bill_silph_scope_reading",
        "wl_marowak_spirit_revealed",
        "wl_cubone_grief_scene",
        "wl_team_moonlight_tower_ritual",
        "wl_rocket_mr_fuji_hold",
        "wl_mr_fuji_rescue_path_unlocked",
        "wl_poke_flute_lead_unlocked",
    ]:
        if message_id not in ids:
            errors.append(f"Pokemon Tower Silph Scope floor WorldLink batch missing id: {message_id}")

    markers = {
        "main": (
            "PokemonTowerSilphScopeFloorScene",
            "_on_go_to_pokemon_tower_silph_scope_floor",
            "_show_pokemon_tower_silph_scope_floor",
            "go_to_pokemon_tower_silph_scope_floor",
        ),
        "save": (
            "pokemon_tower_silph_scope_floor_reached",
            "red_silph_scope_guard_seen",
            "bill_silph_scope_reading_seen",
            "marowak_spirit_revealed",
            "cubone_grief_scene_seen",
            "team_moonlight_tower_ritual_seen",
            "rocket_mr_fuji_hold_seen",
            "mr_fuji_rescue_path_unlocked",
            "poke_flute_lead_unlocked",
            "queue_pokemon_tower_silph_scope_floor_batch",
        ),
        "first_floor_script": (
            "go_to_pokemon_tower_silph_scope_floor",
            "trigger_deeper_tower_path",
            "silph_scope_obtained",
            "pokemon_tower_deeper_path_unlocked",
        ),
        "silph_scope_script": (
            "Pokemon Tower - Silph Scope Floor",
            "trigger_pokemon_tower_silph_scope_floor_scene",
            "record_pokemon_tower_silph_scope_floor_scene",
            "go_to_pokemon_tower_first_floor",
            "Red",
            "Bill",
            "Silph Scope",
            "Marowak",
            "Cubone",
            "Mr. Fuji",
            "Rocket",
            "Moonlight",
            "Poke Flute",
        ),
        "worldlink": (
            "POKEMON_TOWER_SILPH_SCOPE_FLOOR_BATCH_PATH",
            "Reach Silph Scope floor",
            "Reveal Marowak spirit",
            "Unlock Mr. Fuji rescue path",
            "Unlock Poke Flute lead",
        ),
        "test": (
            "pokemon_tower_silph_scope_floor_test",
            "trigger_deeper_tower_path",
            "trigger_pokemon_tower_silph_scope_floor_scene",
            "silph_scope_obtained",
            "pokemon_tower_deeper_path_unlocked",
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
        print("Native Pokemon Tower Silph Scope floor validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print("Native Pokemon Tower Silph Scope floor validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
