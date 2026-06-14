#!/usr/bin/env python3
"""Validate the native Route 1 WorldLink rumor slice."""

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
        "save": NATIVE / "src" / "save" / "SaveState.gd",
        "worldlink": NATIVE / "src" / "worldlink" / "WorldLinkPanel.gd",
        "route": NATIVE / "src" / "world" / "Route1.gd",
        "bedroom": NATIVE / "src" / "world" / "Bedroom.gd",
        "rumors": NATIVE / "content" / "encounters" / "route_1_rumors.json",
        "batch": NATIVE / "content" / "worldlink" / "route_1_rival_batch.json",
        "test": NATIVE / "tests" / "worldlink_route1_test.gd",
    }
    contents = {name: require_file(path, errors) for name, path in files.items()}
    if errors:
        return errors

    markers = {
        "save": (
            "route_1_rumors_unlocked",
            "worldlink_route_1_rival_batch_queued",
            "unlock_route_1_rumors",
            "queue_route_1_rival_batch",
        ),
        "worldlink": (
            "route_1_rival_batch.json",
            "route_1_rumors.json",
            "save_state",
            "Route 1 Rumors",
        ),
        "route": ("worldlink_panel.save_state = save_state",),
        "bedroom": ("worldlink_panel.save_state = save_state",),
        "test": ("worldlink_route1_test", "wl_blue_route_1_battle_done", "rumor_route_1_unusual_tracks"),
    }
    for name, expected_markers in markers.items():
        for marker in expected_markers:
            if marker not in contents[name]:
                errors.append(f"{files[name].relative_to(ROOT)} missing marker: {marker}")

    rumors = json.loads(contents["rumors"])
    if rumors.get("route_id") != "route_1":
        errors.append("Route 1 rumors must use route_id route_1")
    if rumors.get("status") != "rumor_only":
        errors.append("Route 1 rumors must be marked rumor_only until the encounter engine exists")
    rumor_ids = {entry.get("id") for entry in rumors.get("rumors", [])}
    required_rumors = {
        "rumor_route_1_unusual_tracks",
        "rumor_route_1_starter_migration",
        "rumor_route_1_blue_shortcut",
    }
    missing_rumors = sorted(required_rumors - rumor_ids)
    if missing_rumors:
        errors.append(f"Route 1 rumors missing ids: {', '.join(missing_rumors)}")

    batch = json.loads(contents["batch"])
    if batch.get("id") != "route_1_rival_batch":
        errors.append("Route 1 rival batch must use id route_1_rival_batch")
    entries = batch.get("feed", [])
    entry_ids = {entry.get("id") for entry in entries}
    required_entries = {
        "wl_blue_route_1_battle_done",
        "wl_ava_route_1_capture",
        "wl_dax_route_1_training",
        "wl_red_route_1_checkin",
        "wl_silver_johto_tease",
    }
    missing_entries = sorted(required_entries - entry_ids)
    if missing_entries:
        errors.append(f"Route 1 rival batch missing ids: {', '.join(missing_entries)}")

    rivals = {entry.get("rival") for entry in entries}
    for rival in ("blue", "ava", "dax", "red", "silver"):
        if rival not in rivals:
            errors.append(f"Route 1 rival batch missing rival: {rival}")

    return errors


def main() -> int:
    errors = validate_files()
    if errors:
        print("Native Route 1 WorldLink validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print("Native Route 1 WorldLink validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
