#!/usr/bin/env python3
"""Validate the native Route 5 Underground Path setup slice."""

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
        "route5_scene": NATIVE / "scenes" / "world" / "Route5UndergroundPath.tscn",
        "route5_script": NATIVE / "src" / "world" / "Route5UndergroundPath.gd",
        "worldlink": NATIVE / "src" / "worldlink" / "WorldLinkPanel.gd",
        "worldlink_batch": NATIVE / "content" / "worldlink" / "route_5_underground_path_batch.json",
        "test": NATIVE / "tests" / "route5_underground_path_test.gd",
    }
    contents = {name: require_file(path, errors) for name, path in files.items()}
    if errors:
        return errors

    batch = json.loads(contents["worldlink_batch"])
    if batch.get("id") != "route_5_underground_path_batch":
        errors.append("Route 5 WorldLink batch must use id route_5_underground_path_batch")
    ids = {item.get("id") for item in batch.get("feed", [])}
    for message_id in [
        "wl_route_5_underground_path_reached",
        "wl_underground_path_scouted",
        "wl_vermilion_shipping_lead",
        "wl_vermilion_city_teased",
    ]:
        if message_id not in ids:
            errors.append(f"Route 5 WorldLink batch missing id: {message_id}")

    markers = {
        "main": (
            "Route5UndergroundPathScene",
            "_on_go_to_route_5_underground_path",
            "_show_route_5_underground_path",
            "go_to_cerulean_city",
        ),
        "save": (
            "route_5_underground_path_reached",
            "underground_path_scouted",
            "vermilion_shipping_lead_seen",
            "vermilion_city_teased",
            "queue_route_5_underground_path_batch",
        ),
        "cerulean": (
            "go_to_route_5_underground_path",
            "trigger_route_5_underground_path_entry",
            "route_5_vermilion_path_unlocked",
            "stolen TM",
        ),
        "route5_script": (
            "Route 5 - Underground Path",
            "trigger_underground_path_scouting",
            "record_underground_path_scouting",
            "Vermilion",
            "Underground Path",
        ),
        "worldlink": (
            "ROUTE_5_UNDERGROUND_PATH_BATCH_PATH",
            "Reach Route 5",
            "Scout Underground Path",
            "Track Vermilion shipping lead",
            "vermilion_shipping_lead_seen",
        ),
        "test": (
            "route5_underground_path_test",
            "trigger_route_5_underground_path_entry",
            "trigger_underground_path_scouting",
            "vermilion_shipping_lead_seen",
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
        print("Native Route 5 Underground Path validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print("Native Route 5 Underground Path validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
