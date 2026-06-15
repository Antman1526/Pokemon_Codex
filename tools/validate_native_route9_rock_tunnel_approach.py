#!/usr/bin/env python3
"""Validate the native Route 9 Rock Tunnel approach slice."""

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
        "lab_script": NATIVE / "src" / "world" / "Route2EastFieldLab.gd",
        "route9_scene": NATIVE / "scenes" / "world" / "Route9RockTunnelApproach.tscn",
        "route9_script": NATIVE / "src" / "world" / "Route9RockTunnelApproach.gd",
        "worldlink": NATIVE / "src" / "worldlink" / "WorldLinkPanel.gd",
        "worldlink_batch": NATIVE / "content" / "worldlink" / "route_9_rock_tunnel_approach_batch.json",
        "test": NATIVE / "tests" / "route9_rock_tunnel_approach_test.gd",
    }
    contents = {name: require_file(path, errors) for name, path in files.items()}
    if errors:
        return errors

    batch = json.loads(contents["worldlink_batch"])
    if batch.get("id") != "route_9_rock_tunnel_approach_batch":
        errors.append("Route 9 WorldLink batch must use id route_9_rock_tunnel_approach_batch")
    ids = {item.get("id") for item in batch.get("feed", [])}
    for message_id in [
        "wl_route_9_rock_tunnel_approach_reached",
        "wl_red_route_9_trainer_lane",
        "wl_bill_rock_tunnel_darkness_warning",
        "wl_team_moonlight_route_9_debut",
        "wl_rocket_route_9_supply_cache",
        "wl_lavender_tower_signal_confirmed",
        "wl_rock_tunnel_entry_unlocked",
    ]:
        if message_id not in ids:
            errors.append(f"Route 9 WorldLink batch missing id: {message_id}")

    markers = {
        "main": (
            "Route9RockTunnelApproachScene",
            "_on_go_to_route_9_rock_tunnel_approach",
            "_show_route_9_rock_tunnel_approach",
            "go_to_route_9_rock_tunnel_approach",
        ),
        "save": (
            "route_9_rock_tunnel_approach_reached",
            "red_route_9_trainer_lane_seen",
            "bill_rock_tunnel_darkness_warning_seen",
            "team_moonlight_route_9_debut_seen",
            "rocket_route_9_supply_cache_seen",
            "lavender_tower_signal_confirmed",
            "rock_tunnel_entry_unlocked",
            "queue_route_9_rock_tunnel_approach_batch",
        ),
        "lab_script": (
            "go_to_route_9_rock_tunnel_approach",
            "trigger_route_9_rock_tunnel_entry",
            "route_9_rock_tunnel_path_unlocked",
            "Rock Tunnel",
        ),
        "route9_script": (
            "Route 9 - Rock Tunnel Approach",
            "trigger_route_9_approach_scene",
            "record_route_9_approach_scene",
            "go_to_route_2_east_field_lab",
            "Red",
            "Bill",
            "Moonlight",
            "Rocket",
            "Lavender",
            "Rock Tunnel",
            "Echo Flute",
            "trainer lane",
        ),
        "worldlink": (
            "ROUTE_9_ROCK_TUNNEL_APPROACH_BATCH_PATH",
            "Reach Route 9",
            "Prepare for Rock Tunnel",
            "Expose Team Moonlight on Route 9",
            "Unlock Rock Tunnel entry",
        ),
        "test": (
            "route9_rock_tunnel_approach_test",
            "trigger_route_9_rock_tunnel_entry",
            "trigger_route_9_approach_scene",
            "rock_tunnel_entry_unlocked",
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
        print("Native Route 9 Rock Tunnel approach validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print("Native Route 9 Rock Tunnel approach validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
