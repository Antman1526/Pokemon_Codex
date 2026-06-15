#!/usr/bin/env python3
"""Validate the native Celadon City arrival and Game Corner exterior slice."""

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
        "underground_script": NATIVE / "src" / "world" / "CeladonUndergroundPath.gd",
        "city_scene": NATIVE / "scenes" / "world" / "CeladonCity.tscn",
        "city_script": NATIVE / "src" / "world" / "CeladonCity.gd",
        "worldlink": NATIVE / "src" / "worldlink" / "WorldLinkPanel.gd",
        "worldlink_batch": NATIVE / "content" / "worldlink" / "celadon_city_arrival_batch.json",
        "test": NATIVE / "tests" / "celadon_city_arrival_test.gd",
    }
    contents = {name: require_file(path, errors) for name, path in files.items()}
    if errors:
        return errors

    batch = json.loads(contents["worldlink_batch"])
    if batch.get("id") != "celadon_city_arrival_batch":
        errors.append("Celadon City WorldLink batch must use id celadon_city_arrival_batch")
    ids = {item.get("id") for item in batch.get("feed", [])}
    for message_id in [
        "wl_celadon_city_reached",
        "wl_red_celadon_city_arrival",
        "wl_bill_game_corner_exterior_signal",
        "wl_rocket_game_corner_front",
        "wl_team_moonlight_celadon_ad",
        "wl_erika_gym_teased",
        "wl_game_corner_investigation_unlocked",
    ]:
        if message_id not in ids:
            errors.append(f"Celadon City WorldLink batch missing id: {message_id}")

    markers = {
        "main": (
            "CeladonCityScene",
            "_on_go_to_celadon_city",
            "_show_celadon_city",
            "go_to_celadon_city",
        ),
        "save": (
            "celadon_city_reached",
            "red_celadon_city_arrival_seen",
            "bill_game_corner_exterior_signal_seen",
            "rocket_game_corner_front_seen",
            "team_moonlight_celadon_ad_seen",
            "erika_gym_teased_seen",
            "game_corner_investigation_unlocked",
            "queue_celadon_city_arrival_batch",
        ),
        "underground_script": (
            "go_to_celadon_city",
            "trigger_celadon_city_entry",
            "celadon_city_arrival_unlocked",
            "Celadon",
        ),
        "city_script": (
            "Celadon City - Arrival",
            "trigger_celadon_city_arrival_scene",
            "record_celadon_city_arrival_scene",
            "go_to_celadon_underground_path",
            "Red",
            "Bill",
            "Rocket",
            "Moonlight",
            "Celadon",
            "Game Corner",
            "Silph Scope",
            "Erika",
        ),
        "worldlink": (
            "CELADON_CITY_ARRIVAL_BATCH_PATH",
            "Reach Celadon City",
            "Scout Game Corner exterior",
            "Spot Moonlight city ad",
            "Tease Erika's gym",
            "Unlock Game Corner investigation",
        ),
        "test": (
            "celadon_city_arrival_test",
            "trigger_celadon_city_entry",
            "trigger_celadon_city_arrival_scene",
            "game_corner_investigation_unlocked",
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
        print("Native Celadon City arrival validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print("Native Celadon City arrival validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
