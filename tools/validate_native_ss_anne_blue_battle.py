#!/usr/bin/env python3
"""Validate the native S.S. Anne Blue rival battle slice."""

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
        "deck": NATIVE / "src" / "world" / "SSAnneMainDeck.gd",
        "battle_data": NATIVE / "content" / "battles" / "blue_ss_anne.json",
        "worldlink": NATIVE / "src" / "worldlink" / "WorldLinkPanel.gd",
        "worldlink_batch": NATIVE / "content" / "worldlink" / "ss_anne_blue_battle_batch.json",
        "test": NATIVE / "tests" / "ss_anne_blue_battle_test.gd",
    }
    contents = {name: require_file(path, errors) for name, path in files.items()}
    if errors:
        return errors

    battle_data = json.loads(contents["battle_data"])
    if battle_data.get("id") != "blue_ss_anne":
        errors.append("Blue S.S. Anne battle data must use id blue_ss_anne")
    if battle_data.get("location") != "ss_anne_main_deck":
        errors.append("Blue S.S. Anne battle must be located on ss_anne_main_deck")
    if battle_data.get("level_cap") != 24:
        errors.append("Blue S.S. Anne battle should use level cap 24")
    opponent = battle_data.get("opponent", {})
    if opponent.get("display_name") != "Blue":
        errors.append("Blue S.S. Anne opponent display_name must be Blue")
    slots = opponent.get("slots", [])
    slot_text = json.dumps(slots)
    for marker in ["blue_starter", "Pidgeotto", "Raticate", "Kadabra"]:
        if marker not in slot_text:
            errors.append(f"Blue S.S. Anne battle slots missing marker: {marker}")

    batch = json.loads(contents["worldlink_batch"])
    if batch.get("id") != "ss_anne_blue_battle_batch":
        errors.append("Blue S.S. Anne WorldLink batch must use id ss_anne_blue_battle_batch")
    ids = {item.get("id") for item in batch.get("feed", [])}
    for message_id in [
        "wl_blue_ss_anne_battle_started",
        "wl_blue_ss_anne_battle_finished",
        "wl_blue_ss_anne_rival_respect",
    ]:
        if message_id not in ids:
            errors.append(f"Blue S.S. Anne WorldLink batch missing id: {message_id}")

    markers = {
        "main": (
            "ss_anne_main_deck",
            "_show_ss_anne_main_deck",
        ),
        "save": (
            "blue_ss_anne_battle_started",
            "blue_ss_anne_battle_finished",
            "blue_ss_anne_rival_respect_seen",
            "queue_ss_anne_blue_battle_batch",
        ),
        "battle": (
            '"blue_ss_anne"',
            "blue_ss_anne.json",
            "_resolve_slot_species",
        ),
        "deck": (
            "start_battle_placeholder",
            "trigger_blue_ship_battle",
            "blue_ship_rival_teased",
            "blue_ss_anne",
        ),
        "worldlink": (
            "SS_ANNE_BLUE_BATTLE_BATCH_PATH",
            "Battle Blue on S.S. Anne",
            "Earn Blue's ship respect",
        ),
        "test": (
            "ss_anne_blue_battle_test",
            "trigger_blue_ship_battle",
            "blue_ss_anne_battle_finished",
            "Charmander",
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
        print("Native S.S. Anne Blue battle validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print("Native S.S. Anne Blue battle validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
