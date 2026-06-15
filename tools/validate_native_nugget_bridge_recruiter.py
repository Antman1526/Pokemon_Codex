#!/usr/bin/env python3
"""Validate the native Nugget Bridge recruiter slice."""

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
        "cerulean": NATIVE / "src" / "world" / "CeruleanCity.gd",
        "bridge_scene": NATIVE / "scenes" / "world" / "NuggetBridge.tscn",
        "bridge_script": NATIVE / "src" / "world" / "NuggetBridge.gd",
        "battle": NATIVE / "content" / "battles" / "nugget_bridge_recruiter_1.json",
        "battle_script": NATIVE / "src" / "battle" / "BattlePlaceholder.gd",
        "worldlink": NATIVE / "src" / "worldlink" / "WorldLinkPanel.gd",
        "batch": NATIVE / "content" / "worldlink" / "nugget_bridge_recruiter_batch.json",
        "test": NATIVE / "tests" / "nugget_bridge_recruiter_test.gd",
    }
    contents = {name: require_file(path, errors) for name, path in files.items()}
    if errors:
        return errors

    battle_data = json.loads(contents["battle"])
    if battle_data.get("id") != "nugget_bridge_recruiter_1":
        errors.append("Nugget Bridge battle data must use id nugget_bridge_recruiter_1")
    if battle_data.get("location") != "nugget_bridge":
        errors.append("Nugget Bridge battle data must use location nugget_bridge")
    if battle_data.get("battle_type") != "faction_recruiter":
        errors.append("Nugget Bridge battle must be battle_type faction_recruiter")
    if battle_data.get("level_cap") != 21:
        errors.append("Nugget Bridge recruiter placeholder should document level cap 21")
    opponent = battle_data.get("opponent", {})
    if opponent.get("display_name") != "Bridge Recruiter":
        errors.append("Nugget Bridge opponent display_name must be Bridge Recruiter")
    slots = opponent.get("slots", [])
    for species in ("Ekans", "Meowth"):
        if not any(slot.get("species") == species for slot in slots):
            errors.append(f"Nugget Bridge battle must include {species}")

    markers = {
        "main": (
            "NuggetBridgeScene",
            "_on_go_to_nugget_bridge",
            "_show_nugget_bridge",
            "battle_return_scene == \"nugget_bridge\"",
        ),
        "save": (
            "enter_nugget_bridge",
            "record_nugget_bridge_scouting",
            "nugget_bridge_reached",
            "red_misty_nugget_bridge_scout_seen",
            "nugget_bridge_recruiter_1_battle_started",
            "nugget_bridge_recruiter_1_battle_finished",
            "worldlink_nugget_bridge_batch_queued",
        ),
        "cerulean": (
            "go_to_nugget_bridge",
            "trigger_nugget_bridge_entry",
            "misty_cerulean_intro_seen",
        ),
        "bridge_script": (
            "Nugget Bridge",
            "trigger_bridge_scouting",
            "trigger_recruiter_battle",
            "start_battle_placeholder",
            "nugget_bridge_recruiter_1",
            "Rocket",
            "Gold Dust",
            "Misty",
        ),
        "battle_script": (
            "nugget_bridge_recruiter_1",
            "nugget_bridge_recruiter_1.json",
        ),
        "worldlink": (
            "NUGGET_BRIDGE_BATCH_PATH",
            "nugget_bridge_recruiter_batch.json",
            "Reach Nugget Bridge",
            "Scout bridge recruiters",
            "Defeat first bridge recruiter",
        ),
        "test": (
            "nugget_bridge_recruiter_test",
            "trigger_nugget_bridge_entry",
            "trigger_bridge_scouting",
            "trigger_recruiter_battle",
            "nugget_bridge_recruiter_1",
        ),
    }
    for name, expected_markers in markers.items():
        for marker in expected_markers:
            if marker not in contents[name]:
                errors.append(f"{files[name].relative_to(ROOT)} missing marker: {marker}")

    batch_data = json.loads(contents["batch"])
    if batch_data.get("id") != "nugget_bridge_recruiter_batch":
        errors.append("Nugget Bridge batch must use id nugget_bridge_recruiter_batch")
    if batch_data.get("trigger") != "nugget_bridge_rocket_gold_dust_recruiter_setup":
        errors.append("Nugget Bridge batch must use trigger nugget_bridge_rocket_gold_dust_recruiter_setup")
    entry_ids = {entry.get("id") for entry in batch_data.get("feed", [])}
    for required_id in (
        "wl_nugget_bridge_reached",
        "wl_nugget_bridge_scouting",
        "wl_nugget_bridge_recruiter_1_battle_finished",
    ):
        if required_id not in entry_ids:
            errors.append(f"Nugget Bridge batch missing id: {required_id}")

    return errors


def main() -> int:
    errors = validate_files()
    if errors:
        print("Native Nugget Bridge recruiter validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print("Native Nugget Bridge recruiter validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
