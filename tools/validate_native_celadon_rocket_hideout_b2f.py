#!/usr/bin/env python3
"""Validate the native Celadon Rocket Hideout B2F slice."""

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
        "b1f_script": NATIVE / "src" / "world" / "CeladonRocketHideoutB1F.gd",
        "b2f_scene": NATIVE / "scenes" / "world" / "CeladonRocketHideoutB2F.tscn",
        "b2f_script": NATIVE / "src" / "world" / "CeladonRocketHideoutB2F.gd",
        "battle_data": NATIVE / "content" / "battles" / "rocket_hideout_b2f_patrol.json",
        "worldlink": NATIVE / "src" / "worldlink" / "WorldLinkPanel.gd",
        "worldlink_batch": NATIVE / "content" / "worldlink" / "celadon_rocket_hideout_b2f_batch.json",
        "test": NATIVE / "tests" / "celadon_rocket_hideout_b2f_test.gd",
    }
    contents = {name: require_file(path, errors) for name, path in files.items()}
    if errors:
        return errors

    batch = json.loads(contents["worldlink_batch"])
    if batch.get("id") != "celadon_rocket_hideout_b2f_batch":
        errors.append("Rocket Hideout B2F WorldLink batch must use id celadon_rocket_hideout_b2f_batch")
    ids = {item.get("id") for item in batch.get("feed", [])}
    for message_id in [
        "wl_celadon_rocket_hideout_b2f_reached",
        "wl_red_hideout_b2f_patrol_warning",
        "wl_bill_stolen_silph_scope_crate",
        "wl_rocket_hideout_b2f_patrol_unlocked",
        "wl_rocket_gold_dust_b2f_conflict",
        "wl_team_moonlight_control_room_interference",
        "wl_lift_key_b3f_route_seen",
        "wl_rocket_hideout_b2f_patrol_finished",
        "wl_rocket_hideout_b3f_path_unlocked",
    ]:
        if message_id not in ids:
            errors.append(f"Rocket Hideout B2F WorldLink batch missing id: {message_id}")

    battle = json.loads(contents["battle_data"])
    if battle.get("id") != "rocket_hideout_b2f_patrol":
        errors.append("Rocket Hideout B2F patrol battle must use id rocket_hideout_b2f_patrol")
    if battle.get("location") != "celadon_rocket_hideout_b2f":
        errors.append("Rocket Hideout B2F patrol battle must use location celadon_rocket_hideout_b2f")
    opponent = battle.get("opponent", {})
    if opponent.get("faction") != "rocket":
        errors.append("Rocket Hideout B2F patrol opponent must be faction rocket")

    markers = {
        "main": (
            "CeladonRocketHideoutB2FScene",
            "_on_go_to_rocket_hideout_b2f",
            "_show_celadon_rocket_hideout_b2f",
            "go_to_rocket_hideout_b2f",
            "celadon_rocket_hideout_b2f",
            "start_battle_placeholder.connect(_on_start_battle_placeholder)",
        ),
        "save": (
            "celadon_rocket_hideout_b2f_reached",
            "red_hideout_b2f_patrol_warning_seen",
            "bill_stolen_silph_scope_crate_seen",
            "rocket_hideout_b2f_patrol_battle_unlocked",
            "rocket_hideout_b2f_patrol_battle_started",
            "rocket_hideout_b2f_patrol_battle_finished",
            "rocket_gold_dust_b2f_conflict_seen",
            "team_moonlight_control_room_interference_seen",
            "lift_key_b3f_route_seen",
            "rocket_hideout_b3f_path_unlocked",
            "queue_celadon_rocket_hideout_b2f_batch",
        ),
        "battle": (
            "rocket_hideout_b2f_patrol",
            "rocket_hideout_b2f_patrol.json",
        ),
        "b1f_script": (
            "go_to_rocket_hideout_b2f",
            "trigger_rocket_hideout_b2f_entry",
            "rocket_hideout_b2f_path_unlocked",
        ),
        "b2f_script": (
            "Celadon Rocket Hideout - B2F",
            "start_battle_placeholder",
            "trigger_rocket_hideout_b2f_scene",
            "trigger_rocket_hideout_b2f_patrol_battle",
            "record_celadon_rocket_hideout_b2f_scene",
            "go_to_rocket_hideout_b3f",
            "go_to_rocket_hideout_b1f",
            "Red",
            "Bill",
            "Rocket",
            "Gold Dust",
            "Moonlight",
            "Silph Scope",
            "Lift Key",
            "patrol",
            "B3F",
        ),
        "worldlink": (
            "CELADON_ROCKET_HIDEOUT_B2F_BATCH_PATH",
            "Reach Rocket Hideout B2F",
            "Find stolen Silph Scope crate",
            "Battle B2F Rocket patrol",
            "Spot B2F faction conflict",
            "Unlock Hideout B3F path",
        ),
        "test": (
            "celadon_rocket_hideout_b2f_test",
            "trigger_rocket_hideout_b2f_entry",
            "trigger_rocket_hideout_b2f_scene",
            "trigger_rocket_hideout_b2f_patrol_battle",
            "rocket_hideout_b3f_path_unlocked",
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
        print("Native Celadon Rocket Hideout B2F validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print("Native Celadon Rocket Hideout B2F validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
