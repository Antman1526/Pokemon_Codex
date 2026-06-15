#!/usr/bin/env python3
"""Validate the native Cerulean City intro slice."""

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
        "route4": NATIVE / "src" / "world" / "Route4CeruleanApproach.gd",
        "cerulean_scene": NATIVE / "scenes" / "world" / "CeruleanCity.tscn",
        "cerulean_script": NATIVE / "src" / "world" / "CeruleanCity.gd",
        "worldlink": NATIVE / "src" / "worldlink" / "WorldLinkPanel.gd",
        "batch": NATIVE / "content" / "worldlink" / "cerulean_city_intro_batch.json",
        "test": NATIVE / "tests" / "cerulean_city_intro_test.gd",
    }
    contents = {name: require_file(path, errors) for name, path in files.items()}
    if errors:
        return errors

    markers = {
        "main": (
            "CeruleanCityScene",
            "_on_go_to_cerulean_city",
            "_show_cerulean_city",
        ),
        "save": (
            "enter_cerulean_city",
            "record_misty_cerulean_intro",
            "cerulean_city_reached",
            "misty_cerulean_intro_seen",
            "nugget_bridge_threat_setup_seen",
            "worldlink_cerulean_city_batch_queued",
        ),
        "route4": (
            "go_to_cerulean_city",
            "trigger_cerulean_city_entry",
            "red_route_4_cerulean_warning_seen",
        ),
        "cerulean_script": (
            "Cerulean City",
            "trigger_misty_intro",
            "return_to_route_4_cerulean_approach",
            "Misty",
            "Red",
            "Nugget Bridge",
            "Rocket",
            "Gold Dust",
        ),
        "worldlink": (
            "CERULEAN_CITY_BATCH_PATH",
            "cerulean_city_intro_batch.json",
            "Reach Cerulean City",
            "Meet Misty",
            "Identify Nugget Bridge threat",
        ),
        "test": (
            "cerulean_city_intro_test",
            "trigger_cerulean_city_entry",
            "trigger_misty_intro",
            "nugget_bridge_threat_setup_seen",
        ),
    }
    for name, expected_markers in markers.items():
        for marker in expected_markers:
            if marker not in contents[name]:
                errors.append(f"{files[name].relative_to(ROOT)} missing marker: {marker}")

    data = json.loads(contents["batch"])
    if data.get("id") != "cerulean_city_intro_batch":
        errors.append("Cerulean City batch must use id cerulean_city_intro_batch")
    if data.get("trigger") != "cerulean_city_first_entry_after_route_4_warning":
        errors.append("Cerulean City batch must use trigger cerulean_city_first_entry_after_route_4_warning")
    entry_ids = {entry.get("id") for entry in data.get("feed", [])}
    for required_id in (
        "wl_cerulean_city_reached",
        "wl_misty_cerulean_intro",
        "wl_nugget_bridge_threat_setup",
    ):
        if required_id not in entry_ids:
            errors.append(f"Cerulean City batch missing id: {required_id}")

    return errors


def main() -> int:
    errors = validate_files()
    if errors:
        print("Native Cerulean City intro validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print("Native Cerulean City intro validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
