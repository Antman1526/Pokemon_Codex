#!/usr/bin/env python3
"""Validate the native Vermilion City arrival shell slice."""

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
        "route5": NATIVE / "src" / "world" / "Route5UndergroundPath.gd",
        "vermilion_scene": NATIVE / "scenes" / "world" / "VermilionCity.tscn",
        "vermilion_script": NATIVE / "src" / "world" / "VermilionCity.gd",
        "worldlink": NATIVE / "src" / "worldlink" / "WorldLinkPanel.gd",
        "worldlink_batch": NATIVE / "content" / "worldlink" / "vermilion_city_arrival_batch.json",
        "test": NATIVE / "tests" / "vermilion_city_arrival_test.gd",
    }
    contents = {name: require_file(path, errors) for name, path in files.items()}
    if errors:
        return errors

    batch = json.loads(contents["worldlink_batch"])
    if batch.get("id") != "vermilion_city_arrival_batch":
        errors.append("Vermilion WorldLink batch must use id vermilion_city_arrival_batch")
    ids = {item.get("id") for item in batch.get("feed", [])}
    for message_id in [
        "wl_vermilion_city_reached",
        "wl_vermilion_harbor_scouted",
        "wl_ss_anne_ticket_lead",
        "wl_surge_power_sabotage_teased",
    ]:
        if message_id not in ids:
            errors.append(f"Vermilion WorldLink batch missing id: {message_id}")

    markers = {
        "main": (
            "VermilionCityScene",
            "_on_go_to_vermilion_city",
            "_show_vermilion_city",
            "go_to_route_5_underground_path",
        ),
        "save": (
            "vermilion_city_reached",
            "vermilion_harbor_scouted",
            "ss_anne_ticket_lead_seen",
            "surge_power_sabotage_teased",
            "queue_vermilion_city_arrival_batch",
        ),
        "route5": (
            "go_to_vermilion_city",
            "trigger_vermilion_city_entry",
            "vermilion_shipping_lead_seen",
            "Vermilion",
        ),
        "vermilion_script": (
            "Vermilion City",
            "trigger_vermilion_arrival_scene",
            "record_vermilion_arrival_scene",
            "S.S. Anne",
            "Surge",
            "Rocket",
        ),
        "worldlink": (
            "VERMILION_CITY_ARRIVAL_BATCH_PATH",
            "Reach Vermilion City",
            "Scout Vermilion harbor",
            "Find S.S. Anne ticket lead",
            "Tease Surge power sabotage",
        ),
        "test": (
            "vermilion_city_arrival_test",
            "trigger_vermilion_city_entry",
            "trigger_vermilion_arrival_scene",
            "surge_power_sabotage_teased",
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
        print("Native Vermilion City arrival validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print("Native Vermilion City arrival validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
