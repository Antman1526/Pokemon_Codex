#!/usr/bin/env python3
"""Validate the native Celadon Game Corner exterior and Rocket guard slice."""

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
        "battle_script": NATIVE / "src" / "battle" / "BattlePlaceholder.gd",
        "city_script": NATIVE / "src" / "world" / "CeladonCity.gd",
        "exterior_scene": NATIVE / "scenes" / "world" / "CeladonGameCornerExterior.tscn",
        "exterior_script": NATIVE / "src" / "world" / "CeladonGameCornerExterior.gd",
        "battle_data": NATIVE / "content" / "battles" / "rocket_game_corner_guard.json",
        "worldlink": NATIVE / "src" / "worldlink" / "WorldLinkPanel.gd",
        "worldlink_batch": NATIVE / "content" / "worldlink" / "celadon_game_corner_exterior_batch.json",
        "test": NATIVE / "tests" / "celadon_game_corner_exterior_test.gd",
    }
    contents = {name: require_file(path, errors) for name, path in files.items()}
    if errors:
        return errors

    battle = json.loads(contents["battle_data"])
    if battle.get("id") != "rocket_game_corner_guard":
        errors.append("Rocket Game Corner guard battle must use id rocket_game_corner_guard")
    if battle.get("location") != "celadon_game_corner_exterior":
        errors.append("Rocket Game Corner guard battle must use celadon_game_corner_exterior location")
    slots = battle.get("opponent", {}).get("slots", [])
    for species in ["Raticate", "Koffing"]:
        if not any(slot.get("species") == species for slot in slots):
            errors.append(f"Rocket Game Corner guard battle must include {species}")

    batch = json.loads(contents["worldlink_batch"])
    if batch.get("id") != "celadon_game_corner_exterior_batch":
        errors.append("Game Corner exterior WorldLink batch must use id celadon_game_corner_exterior_batch")
    ids = {item.get("id") for item in batch.get("feed", [])}
    for message_id in [
        "wl_game_corner_exterior_reached",
        "wl_red_game_corner_door_guard",
        "wl_bill_coin_case_signal",
        "wl_rocket_game_corner_guard_exposed",
        "wl_team_moonlight_sleep_coin",
        "wl_game_corner_guard_battle_unlocked",
        "wl_rocket_game_corner_guard_battle_finished",
        "wl_rocket_hideout_switch_lead_seen",
        "wl_game_corner_hideout_entry_unlocked",
    ]:
        if message_id not in ids:
            errors.append(f"Game Corner exterior WorldLink batch missing id: {message_id}")

    markers = {
        "main": (
            "CeladonGameCornerExteriorScene",
            "_on_go_to_game_corner_exterior",
            "_show_celadon_game_corner_exterior",
            "go_to_game_corner_exterior",
            "celadon_game_corner_exterior",
        ),
        "save": (
            "game_corner_exterior_reached",
            "red_game_corner_door_guard_seen",
            "bill_coin_case_signal_seen",
            "rocket_game_corner_guard_exposed",
            "team_moonlight_sleep_coin_seen",
            "game_corner_guard_battle_unlocked",
            "rocket_game_corner_guard_battle_started",
            "rocket_game_corner_guard_battle_finished",
            "rocket_hideout_switch_lead_seen",
            "game_corner_hideout_entry_unlocked",
            "queue_celadon_game_corner_exterior_batch",
        ),
        "battle_script": (
            "rocket_game_corner_guard",
            "rocket_game_corner_guard.json",
        ),
        "city_script": (
            "go_to_game_corner_exterior",
            "trigger_game_corner_exterior_entry",
            "game_corner_investigation_unlocked",
            "Game Corner",
        ),
        "exterior_script": (
            "Celadon Game Corner - Exterior",
            "trigger_game_corner_exterior_scene",
            "trigger_game_corner_guard_battle",
            "trigger_game_corner_hideout_entry",
            "start_battle_placeholder",
            "go_to_game_corner_hideout_entry",
            "go_to_celadon_city",
            "Red",
            "Bill",
            "Rocket",
            "Moonlight",
            "Game Corner",
            "Coin Case",
            "Silph Scope",
        ),
        "worldlink": (
            "CELADON_GAME_CORNER_EXTERIOR_BATCH_PATH",
            "Reach Game Corner exterior",
            "Expose Rocket Game Corner guard",
            "Battle Game Corner guard",
            "Unlock hideout-entry lead",
        ),
        "test": (
            "celadon_game_corner_exterior_test",
            "trigger_game_corner_exterior_entry",
            "trigger_game_corner_guard_battle",
            "rocket_game_corner_guard",
            "game_corner_hideout_entry_unlocked",
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
        print("Native Celadon Game Corner exterior validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print("Native Celadon Game Corner exterior validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
