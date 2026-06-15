#!/usr/bin/env python3
"""Validate the native Route 25 Bill intro and Nexus network clue slice."""

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
        "route25_scene": NATIVE / "scenes" / "world" / "Route25Bill.tscn",
        "route25_script": NATIVE / "src" / "world" / "Route25Bill.gd",
        "worldlink": NATIVE / "src" / "worldlink" / "WorldLinkPanel.gd",
        "worldlink_batch": NATIVE / "content" / "worldlink" / "route_25_bill_batch.json",
        "test": NATIVE / "tests" / "route25_bill_intro_test.gd",
    }
    contents = {name: require_file(path, errors) for name, path in files.items()}
    if errors:
        return errors

    batch = json.loads(contents["worldlink_batch"])
    if batch.get("id") != "route_25_bill_batch":
        errors.append("Route 25 Bill WorldLink batch must use id route_25_bill_batch")
    ids = {item.get("id") for item in batch.get("feed", [])}
    for message_id in [
        "wl_route_25_bill_reached",
        "wl_bill_route25_intro",
        "wl_bill_storage_network_clue",
        "wl_nexus_network_first_decode",
    ]:
        if message_id not in ids:
            errors.append(f"Route 25 Bill WorldLink batch missing id: {message_id}")

    markers = {
        "main": (
            "Route25BillScene",
            "_on_go_to_route_25_bill",
            "_show_route_25_bill",
            "go_to_cerulean_city",
        ),
        "save": (
            "route_25_bill_reached",
            "misty_recurring_friend_unlocked",
            "bill_route25_intro_seen",
            "bill_storage_network_clue_seen",
            "nexus_network_first_decode_seen",
            "queue_route_25_bill_batch",
        ),
        "cerulean": (
            "go_to_route_25_bill",
            "trigger_route_25_bill_entry",
            "cascade_badge_earned",
            "Route 25",
        ),
        "route25_script": (
            "Route 25 - Bill's Cottage",
            "trigger_bill_intro",
            "record_bill_route25_intro",
            "Nexus",
            "WorldLink",
        ),
        "worldlink": (
            "ROUTE_25_BILL_BATCH_PATH",
            "Reach Route 25",
            "Meet Bill",
            "Decode first Nexus network clue",
            "nexus_network_first_decode_seen",
        ),
        "test": (
            "route25_bill_intro_test",
            "trigger_route_25_bill_entry",
            "trigger_bill_intro",
            "nexus_network_first_decode_seen",
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
        print("Native Route 25 Bill intro validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print("Native Route 25 Bill intro validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
