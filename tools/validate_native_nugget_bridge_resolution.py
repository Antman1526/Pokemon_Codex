#!/usr/bin/env python3
"""Validate the native Nugget Bridge resolution slice."""

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
        "bridge_script": NATIVE / "src" / "world" / "NuggetBridge.gd",
        "battle": NATIVE / "content" / "battles" / "nugget_bridge_captain.json",
        "battle_script": NATIVE / "src" / "battle" / "BattlePlaceholder.gd",
        "worldlink": NATIVE / "src" / "worldlink" / "WorldLinkPanel.gd",
        "batch": NATIVE / "content" / "worldlink" / "nugget_bridge_recruiter_batch.json",
        "test": NATIVE / "tests" / "nugget_bridge_resolution_test.gd",
    }
    contents = {name: require_file(path, errors) for name, path in files.items()}
    if errors:
        return errors

    battle_data = json.loads(contents["battle"])
    if battle_data.get("id") != "nugget_bridge_captain":
        errors.append("Nugget Bridge captain battle data must use id nugget_bridge_captain")
    if battle_data.get("location") != "nugget_bridge":
        errors.append("Nugget Bridge captain battle data must use location nugget_bridge")
    if battle_data.get("battle_type") != "faction_recruiter_captain":
        errors.append("Nugget Bridge captain battle must be battle_type faction_recruiter_captain")
    if battle_data.get("level_cap") != 21:
        errors.append("Nugget Bridge captain placeholder should document level cap 21")
    opponent = battle_data.get("opponent", {})
    if opponent.get("display_name") != "Bridge Captain":
        errors.append("Nugget Bridge captain opponent display_name must be Bridge Captain")
    slots = opponent.get("slots", [])
    for species in ("Sandile", "Zubat"):
        if not any(slot.get("species") == species for slot in slots):
            errors.append(f"Nugget Bridge captain battle must include {species}")

    markers = {
        "main": (
            "battle_return_scene == \"nugget_bridge\"",
            "_show_nugget_bridge",
        ),
        "save": (
            "nugget_bridge_captain_battle_started",
            "nugget_bridge_captain_battle_finished",
            "nugget_bridge_crisis_cleared",
            "misty_gym_unlocked",
            "wl_nugget_bridge_crisis_cleared",
        ),
        "bridge_script": (
            "CAPTAIN_BATTLE_ID",
            "trigger_bridge_captain_battle",
            "show_bridge_resolution",
            "nugget_bridge_recruiter_1_battle_finished",
            "nugget_bridge_captain",
            "Misty",
            "Rocket",
            "Gold Dust",
        ),
        "battle_script": (
            "nugget_bridge_captain",
            "nugget_bridge_captain.json",
        ),
        "worldlink": (
            "Defeat bridge captain",
            "Clear Nugget Bridge crisis",
        ),
        "test": (
            "nugget_bridge_resolution_test",
            "trigger_bridge_captain_battle",
            "nugget_bridge_captain",
            "nugget_bridge_crisis_cleared",
            "misty_gym_unlocked",
        ),
    }
    for name, expected_markers in markers.items():
        for marker in expected_markers:
            if marker not in contents[name]:
                errors.append(f"{files[name].relative_to(ROOT)} missing marker: {marker}")

    batch_data = json.loads(contents["batch"])
    entry_ids = {entry.get("id") for entry in batch_data.get("feed", [])}
    for required_id in (
        "wl_nugget_bridge_captain_battle_finished",
        "wl_nugget_bridge_crisis_cleared",
    ):
        if required_id not in entry_ids:
            errors.append(f"Nugget Bridge batch missing resolution id: {required_id}")

    return errors


def main() -> int:
    errors = validate_files()
    if errors:
        print("Native Nugget Bridge resolution validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print("Native Nugget Bridge resolution validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
