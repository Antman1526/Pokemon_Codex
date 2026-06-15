#!/usr/bin/env python3
"""Validate the native Cerulean Rocket house theft slice."""

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
        "battle": NATIVE / "content" / "battles" / "cerulean_rocket_house_thief.json",
        "battle_script": NATIVE / "src" / "battle" / "BattlePlaceholder.gd",
        "main": NATIVE / "src" / "Main.gd",
        "save": NATIVE / "src" / "save" / "SaveState.gd",
        "cerulean": NATIVE / "src" / "world" / "CeruleanCity.gd",
        "house_scene": NATIVE / "scenes" / "world" / "CeruleanRocketHouse.tscn",
        "house_script": NATIVE / "src" / "world" / "CeruleanRocketHouse.gd",
        "worldlink": NATIVE / "src" / "worldlink" / "WorldLinkPanel.gd",
        "worldlink_batch": NATIVE / "content" / "worldlink" / "cerulean_rocket_house_batch.json",
        "test": NATIVE / "tests" / "cerulean_rocket_house_test.gd",
    }
    contents = {name: require_file(path, errors) for name, path in files.items()}
    if errors:
        return errors

    battle = json.loads(contents["battle"])
    if battle.get("id") != "cerulean_rocket_house_thief":
        errors.append("Cerulean Rocket battle data must use id cerulean_rocket_house_thief")
    if battle.get("location") != "cerulean_rocket_house":
        errors.append("Cerulean Rocket battle data must use location cerulean_rocket_house")
    if battle.get("level_cap") != 22:
        errors.append("Cerulean Rocket house placeholder should document level cap 22")
    opponent = battle.get("opponent", {})
    if opponent.get("display_name") != "Rocket TM Thief":
        errors.append("Cerulean Rocket battle opponent display_name must be Rocket TM Thief")
    slots = opponent.get("slots", [])
    for species in ["Machop", "Drowzee"]:
        if not any(slot.get("species") == species for slot in slots):
            errors.append(f"Cerulean Rocket battle must include {species}")

    batch = json.loads(contents["worldlink_batch"])
    if batch.get("id") != "cerulean_rocket_house_batch":
        errors.append("Cerulean Rocket WorldLink batch must use id cerulean_rocket_house_batch")
    ids = {item.get("id") for item in batch.get("feed", [])}
    for message_id in [
        "wl_cerulean_house_theft_seen",
        "wl_rocket_stolen_tm_clue",
        "wl_stolen_tm_recovered",
        "wl_route_5_vermilion_path_unlocked",
    ]:
        if message_id not in ids:
            errors.append(f"Cerulean Rocket WorldLink batch missing id: {message_id}")

    markers = {
        "battle_script": (
            "cerulean_rocket_house_thief",
            "cerulean_rocket_house_thief.json",
        ),
        "main": (
            "CeruleanRocketHouseScene",
            "_on_go_to_cerulean_rocket_house",
            "_show_cerulean_rocket_house",
            "battle_return_scene == \"cerulean_rocket_house\"",
        ),
        "save": (
            "cerulean_rocket_house_reached",
            "cerulean_house_theft_seen",
            "rocket_stolen_tm_clue_seen",
            "cerulean_rocket_house_thief_battle_started",
            "cerulean_rocket_house_thief_battle_finished",
            "stolen_tm_recovered",
            "route_5_vermilion_path_unlocked",
            "queue_cerulean_rocket_house_batch",
        ),
        "cerulean": (
            "go_to_cerulean_rocket_house",
            "trigger_cerulean_rocket_house_entry",
            "bill_route25_intro_seen",
            "Rocket house",
        ),
        "house_script": (
            "Cerulean Rocket House",
            "trigger_house_investigation",
            "trigger_rocket_thief_battle",
            "cerulean_rocket_house_thief",
            "Vermilion",
        ),
        "worldlink": (
            "CERULEAN_ROCKET_HOUSE_BATCH_PATH",
            "Investigate Cerulean theft",
            "Recover stolen TM",
            "Unlock Route 5 toward Vermilion",
        ),
        "test": (
            "cerulean_rocket_house_test",
            "trigger_cerulean_rocket_house_entry",
            "trigger_rocket_thief_battle",
            "route_5_vermilion_path_unlocked",
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
        print("Native Cerulean Rocket house validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print("Native Cerulean Rocket house validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
