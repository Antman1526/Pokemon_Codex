#!/usr/bin/env python3
"""Validate the native Mt. Moon entrance faction-conflict slice."""

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
        "pewter": NATIVE / "src" / "world" / "PewterCity.gd",
        "mt_moon_scene": NATIVE / "scenes" / "world" / "MtMoonEntrance.tscn",
        "mt_moon_script": NATIVE / "src" / "world" / "MtMoonEntrance.gd",
        "worldlink": NATIVE / "src" / "worldlink" / "WorldLinkPanel.gd",
        "batch": NATIVE / "content" / "worldlink" / "mt_moon_faction_conflict_batch.json",
        "test": NATIVE / "tests" / "mt_moon_entrance_test.gd",
    }
    contents = {name: require_file(path, errors) for name, path in files.items()}
    if errors:
        return errors

    markers = {
        "main": (
            "MtMoonEntranceScene",
            "_on_go_to_mt_moon_entrance",
            "_show_mt_moon_entrance",
        ),
        "save": (
            "enter_mt_moon_entrance",
            "mt_moon_entrance_reached",
            "red_mt_moon_warning_seen",
            "rocket_gold_dust_mt_moon_conflict_seen",
            "nexus_fossil_hint_seen",
            "queue_mt_moon_faction_batch",
        ),
        "pewter": (
            "go_to_mt_moon_entrance",
            "trigger_mt_moon_departure",
            "pewter_museum_anomaly_seen",
            "Mt. Moon",
        ),
        "mt_moon_script": (
            "Mt. Moon Entrance",
            "trigger_faction_conflict",
            "Team Rocket",
            "Team Gold Dust",
            "Nexus Fossil",
            "return_to_pewter_city",
        ),
        "worldlink": (
            "MT_MOON_BATCH_PATH",
            "mt_moon_faction_conflict_batch.json",
            "Reach Mt. Moon entrance",
            "Witness Rocket and Gold Dust clash",
        ),
        "test": (
            "mt_moon_entrance_test",
            "trigger_mt_moon_departure",
            "trigger_faction_conflict",
            "rocket_gold_dust_mt_moon_conflict_seen",
            "wl_gold_dust_mt_moon_arrival",
        ),
    }
    for name, expected_markers in markers.items():
        for marker in expected_markers:
            if marker not in contents[name]:
                errors.append(f"{files[name].relative_to(ROOT)} missing marker: {marker}")

    data = json.loads(contents["batch"])
    if data.get("id") != "mt_moon_faction_conflict_batch":
        errors.append("Mt. Moon batch must use id mt_moon_faction_conflict_batch")
    if data.get("trigger") != "mt_moon_rocket_gold_dust_fossil_conflict":
        errors.append("Mt. Moon batch must use trigger mt_moon_rocket_gold_dust_fossil_conflict")
    entry_ids = {entry.get("id") for entry in data.get("feed", [])}
    for required_id in (
        "wl_red_mt_moon_warning",
        "wl_rocket_mt_moon_fossil_grab",
        "wl_gold_dust_mt_moon_arrival",
        "wl_nexus_fossil_hint",
    ):
        if required_id not in entry_ids:
            errors.append(f"Mt. Moon batch missing id: {required_id}")

    return errors


def main() -> int:
    errors = validate_files()
    if errors:
        print("Native Mt. Moon entrance validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print("Native Mt. Moon entrance validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
