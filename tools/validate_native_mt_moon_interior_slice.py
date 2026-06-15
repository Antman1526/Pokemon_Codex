#!/usr/bin/env python3
"""Validate the native Mt. Moon first interior fossil-choice setup slice."""

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
        "entrance": NATIVE / "src" / "world" / "MtMoonEntrance.gd",
        "interior_scene": NATIVE / "scenes" / "world" / "MtMoonInterior1.tscn",
        "interior_script": NATIVE / "src" / "world" / "MtMoonInterior1.gd",
        "worldlink": NATIVE / "src" / "worldlink" / "WorldLinkPanel.gd",
        "batch": NATIVE / "content" / "worldlink" / "mt_moon_interior_split_batch.json",
        "test": NATIVE / "tests" / "mt_moon_interior_test.gd",
    }
    contents = {name: require_file(path, errors) for name, path in files.items()}
    if errors:
        return errors

    markers = {
        "main": (
            "MtMoonInterior1Scene",
            "_on_go_to_mt_moon_interior_1",
            "_show_mt_moon_interior_1",
        ),
        "save": (
            "enter_mt_moon_interior_1",
            "mt_moon_interior_1_reached",
            "red_mt_moon_interior_support_seen",
            "rocket_mt_moon_left_path_seen",
            "gold_dust_mt_moon_right_path_seen",
            "fossil_choice_setup_seen",
            "queue_mt_moon_interior_split_batch",
        ),
        "entrance": (
            "go_to_mt_moon_interior_1",
            "trigger_cave_entry",
            "rocket_gold_dust_mt_moon_conflict_seen",
        ),
        "interior_script": (
            "Mt. Moon Interior 1",
            "trigger_split_path_scouting",
            "Team Rocket",
            "Team Gold Dust",
            "Dome Fossil",
            "Helix Fossil",
            "Nexus Fossil",
            "return_to_mt_moon_entrance",
        ),
        "worldlink": (
            "MT_MOON_INTERIOR_BATCH_PATH",
            "mt_moon_interior_split_batch.json",
            "Enter Mt. Moon interior",
            "Map the fossil split paths",
        ),
        "test": (
            "mt_moon_interior_test",
            "trigger_cave_entry",
            "trigger_split_path_scouting",
            "fossil_choice_setup_seen",
            "wl_fossil_choice_setup",
        ),
    }
    for name, expected_markers in markers.items():
        for marker in expected_markers:
            if marker not in contents[name]:
                errors.append(f"{files[name].relative_to(ROOT)} missing marker: {marker}")

    data = json.loads(contents["batch"])
    if data.get("id") != "mt_moon_interior_split_batch":
        errors.append("Mt. Moon interior batch must use id mt_moon_interior_split_batch")
    if data.get("trigger") != "mt_moon_interior_split_path_fossil_setup":
        errors.append("Mt. Moon interior batch must use trigger mt_moon_interior_split_path_fossil_setup")
    entry_ids = {entry.get("id") for entry in data.get("feed", [])}
    for required_id in (
        "wl_red_mt_moon_interior_support",
        "wl_rocket_mt_moon_left_path",
        "wl_gold_dust_mt_moon_right_path",
        "wl_fossil_choice_setup",
    ):
        if required_id not in entry_ids:
            errors.append(f"Mt. Moon interior batch missing id: {required_id}")

    return errors


def main() -> int:
    errors = validate_files()
    if errors:
        print("Native Mt. Moon interior validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print("Native Mt. Moon interior validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
