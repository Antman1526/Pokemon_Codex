#!/usr/bin/env python3
"""Validate the native Celadon Rocket Hideout B3F slice."""

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
        "b2f_script": NATIVE / "src" / "world" / "CeladonRocketHideoutB2F.gd",
        "b3f_scene": NATIVE / "scenes" / "world" / "CeladonRocketHideoutB3F.tscn",
        "b3f_script": NATIVE / "src" / "world" / "CeladonRocketHideoutB3F.gd",
        "battle_data": NATIVE / "content" / "battles" / "rocket_hideout_b3f_admin.json",
        "worldlink": NATIVE / "src" / "worldlink" / "WorldLinkPanel.gd",
        "worldlink_batch": NATIVE / "content" / "worldlink" / "celadon_rocket_hideout_b3f_batch.json",
        "test": NATIVE / "tests" / "celadon_rocket_hideout_b3f_test.gd",
    }
    contents = {name: require_file(path, errors) for name, path in files.items()}
    if errors:
        return errors

    batch = json.loads(contents["worldlink_batch"])
    if batch.get("id") != "celadon_rocket_hideout_b3f_batch":
        errors.append("Rocket Hideout B3F WorldLink batch must use id celadon_rocket_hideout_b3f_batch")
    ids = {item.get("id") for item in batch.get("feed", [])}
    for message_id in [
        "wl_celadon_rocket_hideout_b3f_reached",
        "wl_red_hideout_b3f_lift_key_warning",
        "wl_bill_nexus_order_elevator_trace",
        "wl_rocket_admin_lift_key_battle_unlocked",
        "wl_gold_dust_ledger_recovered",
        "wl_team_moonlight_sleep_panel",
        "wl_giovanni_elevator_route_seen",
        "wl_rocket_admin_lift_key_battle_finished",
        "wl_rocket_lift_key_obtained",
        "wl_rocket_hideout_elevator_path_unlocked",
    ]:
        if message_id not in ids:
            errors.append(f"Rocket Hideout B3F WorldLink batch missing id: {message_id}")

    battle = json.loads(contents["battle_data"])
    if battle.get("id") != "rocket_hideout_b3f_admin":
        errors.append("Rocket Hideout B3F admin battle must use id rocket_hideout_b3f_admin")
    if battle.get("location") != "celadon_rocket_hideout_b3f":
        errors.append("Rocket Hideout B3F admin battle must use location celadon_rocket_hideout_b3f")
    opponent = battle.get("opponent", {})
    if opponent.get("faction") != "rocket":
        errors.append("Rocket Hideout B3F admin opponent must be faction rocket")

    markers = {
        "main": (
            "CeladonRocketHideoutB3FScene",
            "_on_go_to_rocket_hideout_b3f",
            "_show_celadon_rocket_hideout_b3f",
            "go_to_rocket_hideout_b3f",
            "celadon_rocket_hideout_b3f",
            "start_battle_placeholder.connect(_on_start_battle_placeholder)",
        ),
        "save": (
            "celadon_rocket_hideout_b3f_reached",
            "red_hideout_b3f_lift_key_warning_seen",
            "bill_nexus_order_elevator_trace_seen",
            "rocket_admin_lift_key_battle_unlocked",
            "rocket_admin_lift_key_battle_started",
            "rocket_admin_lift_key_battle_finished",
            "gold_dust_ledger_recovered_seen",
            "team_moonlight_sleep_panel_seen",
            "giovanni_elevator_route_seen",
            "rocket_lift_key_obtained",
            "rocket_hideout_elevator_path_unlocked",
            "queue_celadon_rocket_hideout_b3f_batch",
        ),
        "battle": (
            "rocket_hideout_b3f_admin",
            "rocket_hideout_b3f_admin.json",
        ),
        "b2f_script": (
            "go_to_rocket_hideout_b3f",
            "trigger_rocket_hideout_b3f_entry",
            "rocket_hideout_b3f_path_unlocked",
        ),
        "b3f_script": (
            "Celadon Rocket Hideout - B3F",
            "start_battle_placeholder",
            "trigger_rocket_hideout_b3f_scene",
            "trigger_rocket_hideout_b3f_admin_battle",
            "record_celadon_rocket_hideout_b3f_scene",
            "go_to_rocket_hideout_elevator",
            "go_to_rocket_hideout_b2f",
            "Red",
            "Bill",
            "Rocket Admin",
            "Gold Dust",
            "Moonlight",
            "Nexus Order",
            "Lift Key",
            "Giovanni",
            "elevator",
        ),
        "worldlink": (
            "CELADON_ROCKET_HIDEOUT_B3F_BATCH_PATH",
            "Reach Rocket Hideout B3F",
            "Trace Nexus Order elevator",
            "Battle B3F Rocket Admin",
            "Obtain Rocket Lift Key",
            "Unlock Hideout elevator path",
        ),
        "test": (
            "celadon_rocket_hideout_b3f_test",
            "trigger_rocket_hideout_b3f_entry",
            "trigger_rocket_hideout_b3f_scene",
            "trigger_rocket_hideout_b3f_admin_battle",
            "rocket_hideout_elevator_path_unlocked",
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
        print("Native Celadon Rocket Hideout B3F validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print("Native Celadon Rocket Hideout B3F validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
