#!/usr/bin/env python3
"""Validate the native Pokemon Tower Mr. Fuji rescue slice."""

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
        "silph_scope_script": NATIVE / "src" / "world" / "PokemonTowerSilphScopeFloor.gd",
        "fuji_scene": NATIVE / "scenes" / "world" / "PokemonTowerFujiRescue.tscn",
        "fuji_script": NATIVE / "src" / "world" / "PokemonTowerFujiRescue.gd",
        "battle_placeholder": NATIVE / "src" / "battle" / "BattlePlaceholder.gd",
        "battle_data": NATIVE / "content" / "battles" / "rocket_tower_fuji_guard.json",
        "worldlink": NATIVE / "src" / "worldlink" / "WorldLinkPanel.gd",
        "worldlink_batch": NATIVE / "content" / "worldlink" / "pokemon_tower_fuji_rescue_batch.json",
        "test": NATIVE / "tests" / "pokemon_tower_fuji_rescue_test.gd",
    }
    contents = {name: require_file(path, errors) for name, path in files.items()}
    if errors:
        return errors

    batch = json.loads(contents["worldlink_batch"])
    if batch.get("id") != "pokemon_tower_fuji_rescue_batch":
        errors.append("Pokemon Tower Fuji rescue WorldLink batch must use id pokemon_tower_fuji_rescue_batch")
    ids = {item.get("id") for item in batch.get("feed", [])}
    for message_id in [
        "wl_pokemon_tower_fuji_rescue_reached",
        "wl_red_fuji_rescue_guard",
        "wl_bill_fuji_signal_clean",
        "wl_rocket_tower_fuji_guard_seen",
        "wl_team_moonlight_retreat_signal",
        "wl_fuji_rescue_battle_unlocked",
        "wl_rocket_tower_fuji_guard_battle_finished",
        "wl_mr_fuji_rescued",
        "wl_poke_flute_obtained",
        "wl_snorlax_wake_path_unlocked",
    ]:
        if message_id not in ids:
            errors.append(f"Pokemon Tower Fuji rescue WorldLink batch missing id: {message_id}")

    battle = json.loads(contents["battle_data"])
    if battle.get("id") != "rocket_tower_fuji_guard":
        errors.append("Fuji rescue battle must use id rocket_tower_fuji_guard")
    if battle.get("location") != "pokemon_tower_fuji_rescue":
        errors.append("Fuji rescue battle must use location pokemon_tower_fuji_rescue")
    opponent = battle.get("opponent", {})
    if opponent.get("id") != "rocket_tower_guard":
        errors.append("Fuji rescue battle opponent must be rocket_tower_guard")
    if opponent.get("faction") != "rocket":
        errors.append("Fuji rescue battle opponent faction must be rocket")

    markers = {
        "main": (
            "PokemonTowerFujiRescueScene",
            "_on_go_to_pokemon_tower_fuji_rescue",
            "_show_pokemon_tower_fuji_rescue",
            "go_to_pokemon_tower_fuji_rescue",
            "pokemon_tower_fuji_rescue",
        ),
        "save": (
            "pokemon_tower_fuji_rescue_reached",
            "red_fuji_rescue_guard_seen",
            "bill_fuji_signal_clean_seen",
            "rocket_tower_fuji_guard_seen",
            "team_moonlight_retreat_signal_seen",
            "fuji_rescue_battle_unlocked",
            "rocket_tower_fuji_guard_battle_started",
            "rocket_tower_fuji_guard_battle_finished",
            "mr_fuji_rescued",
            "poke_flute_obtained",
            "snorlax_wake_path_unlocked",
            "queue_pokemon_tower_fuji_rescue_batch",
        ),
        "silph_scope_script": (
            "go_to_pokemon_tower_fuji_rescue",
            "trigger_fuji_rescue_path",
            "mr_fuji_rescue_path_unlocked",
            "poke_flute_lead_unlocked",
        ),
        "fuji_script": (
            "Pokemon Tower - Mr. Fuji Rescue",
            "start_battle_placeholder",
            "trigger_pokemon_tower_fuji_rescue_scene",
            "trigger_fuji_rescue_battle",
            "record_pokemon_tower_fuji_rescue_scene",
            "go_to_pokemon_tower_silph_scope_floor",
            "Red",
            "Bill",
            "Rocket",
            "Moonlight",
            "Mr. Fuji",
            "Poke Flute",
            "Snorlax",
        ),
        "battle_placeholder": (
            "rocket_tower_fuji_guard",
            "rocket_tower_fuji_guard.json",
        ),
        "worldlink": (
            "POKEMON_TOWER_FUJI_RESCUE_BATCH_PATH",
            "Reach Mr. Fuji rescue",
            "Battle Rocket tower guard",
            "Rescue Mr. Fuji",
            "Obtain Poke Flute",
            "Unlock Snorlax wake path",
        ),
        "test": (
            "pokemon_tower_fuji_rescue_test",
            "trigger_fuji_rescue_path",
            "trigger_pokemon_tower_fuji_rescue_scene",
            "trigger_fuji_rescue_battle",
            "rocket_tower_fuji_guard",
            "poke_flute_obtained",
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
        print("Native Pokemon Tower Fuji rescue validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print("Native Pokemon Tower Fuji rescue validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
