#!/usr/bin/env python3
"""Validate the native Celadon Rocket command floor slice."""

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
        "battle": NATIVE / "src" / "battle" / "BattlePlaceholder.gd",
        "elevator_script": NATIVE / "src" / "world" / "CeladonRocketHideoutElevator.gd",
        "command_floor_scene": NATIVE / "scenes" / "world" / "CeladonRocketCommandFloor.tscn",
        "command_floor_script": NATIVE / "src" / "world" / "CeladonRocketCommandFloor.gd",
        "battle_data": NATIVE / "content" / "battles" / "giovanni_celadon_command_floor.json",
        "worldlink": NATIVE / "src" / "worldlink" / "WorldLinkPanel.gd",
        "worldlink_batch": NATIVE / "content" / "worldlink" / "celadon_rocket_command_floor_batch.json",
        "test": NATIVE / "tests" / "celadon_rocket_command_floor_test.gd",
    }
    contents = {name: require_file(path, errors) for name, path in files.items()}
    if errors:
        return errors

    batch = json.loads(contents["worldlink_batch"])
    if batch.get("id") != "celadon_rocket_command_floor_batch":
        errors.append("Rocket command floor WorldLink batch must use id celadon_rocket_command_floor_batch")
    ids = {item.get("id") for item in batch.get("feed", [])}
    for message_id in [
        "wl_celadon_rocket_command_floor_reached",
        "wl_red_command_floor_door_guard",
        "wl_bill_nexus_order_command_terminal",
        "wl_giovanni_first_confrontation",
        "wl_rocket_silph_scope_cache",
        "wl_gold_dust_command_floor_ledger",
        "wl_team_moonlight_command_floor_signal",
        "wl_giovanni_command_floor_battle_unlocked",
        "wl_giovanni_command_floor_battle_finished",
        "wl_silph_scope_obtained",
        "wl_pokemon_tower_deeper_path_unlocked",
        "wl_erika_gym_path_unlocked",
    ]:
        if message_id not in ids:
            errors.append(f"Rocket command floor WorldLink batch missing id: {message_id}")

    battle = json.loads(contents["battle_data"])
    if battle.get("id") != "giovanni_celadon_command_floor":
        errors.append("Rocket command floor battle must use id giovanni_celadon_command_floor")
    if battle.get("location") != "celadon_rocket_command_floor":
        errors.append("Rocket command floor battle must use location celadon_rocket_command_floor")
    opponent = battle.get("opponent", {})
    if opponent.get("id") != "giovanni":
        errors.append("Rocket command floor opponent must be Giovanni")
    if opponent.get("faction") != "rocket":
        errors.append("Rocket command floor opponent must be faction rocket")

    markers = {
        "main": (
            "CeladonRocketCommandFloorScene",
            "_on_go_to_rocket_command_floor",
            "_show_celadon_rocket_command_floor",
            "go_to_rocket_command_floor",
            "celadon_rocket_command_floor",
            "start_battle_placeholder.connect(_on_start_battle_placeholder)",
        ),
        "save": (
            "celadon_rocket_command_floor_reached",
            "red_command_floor_door_guard_seen",
            "bill_nexus_order_command_terminal_seen",
            "giovanni_first_confrontation_seen",
            "rocket_silph_scope_cache_seen",
            "gold_dust_command_floor_ledger_seen",
            "team_moonlight_command_floor_signal_seen",
            "giovanni_command_floor_battle_unlocked",
            "giovanni_command_floor_battle_started",
            "giovanni_command_floor_battle_finished",
            "silph_scope_obtained",
            "pokemon_tower_deeper_path_unlocked",
            "erika_gym_path_unlocked",
            "queue_celadon_rocket_command_floor_batch",
        ),
        "battle": (
            "giovanni_celadon_command_floor",
            "giovanni_celadon_command_floor.json",
        ),
        "elevator_script": (
            "go_to_rocket_command_floor",
            "trigger_rocket_command_floor_entry",
            "rocket_command_floor_path_unlocked",
        ),
        "command_floor_script": (
            "Celadon Rocket Command Floor",
            "start_battle_placeholder",
            "trigger_rocket_command_floor_scene",
            "trigger_giovanni_command_floor_battle",
            "record_celadon_rocket_command_floor_scene",
            "go_to_rocket_hideout_elevator",
            "Red",
            "Bill",
            "Giovanni",
            "Silph Scope",
            "Gold Dust",
            "Moonlight",
            "Nexus Order",
            "Pokemon Tower",
            "Erika",
        ),
        "worldlink": (
            "CELADON_ROCKET_COMMAND_FLOOR_BATCH_PATH",
            "Reach Rocket command floor",
            "Battle Giovanni on command floor",
            "Obtain Silph Scope",
            "Unlock Pokemon Tower deeper path",
            "Unlock Erika gym path",
        ),
        "test": (
            "celadon_rocket_command_floor_test",
            "trigger_rocket_command_floor_entry",
            "trigger_rocket_command_floor_scene",
            "trigger_giovanni_command_floor_battle",
            "silph_scope_obtained",
            "pokemon_tower_deeper_path_unlocked",
            "erika_gym_path_unlocked",
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
        print("Native Celadon Rocket command floor validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print("Native Celadon Rocket command floor validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
