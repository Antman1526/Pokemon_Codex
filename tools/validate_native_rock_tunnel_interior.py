#!/usr/bin/env python3
"""Validate the native Rock Tunnel interior slice."""

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
        "route9_script": NATIVE / "src" / "world" / "Route9RockTunnelApproach.gd",
        "tunnel_scene": NATIVE / "scenes" / "world" / "RockTunnelInterior.tscn",
        "tunnel_script": NATIVE / "src" / "world" / "RockTunnelInterior.gd",
        "worldlink": NATIVE / "src" / "worldlink" / "WorldLinkPanel.gd",
        "worldlink_batch": NATIVE / "content" / "worldlink" / "rock_tunnel_interior_batch.json",
        "test": NATIVE / "tests" / "rock_tunnel_interior_test.gd",
    }
    contents = {name: require_file(path, errors) for name, path in files.items()}
    if errors:
        return errors

    batch = json.loads(contents["worldlink_batch"])
    if batch.get("id") != "rock_tunnel_interior_batch":
        errors.append("Rock Tunnel WorldLink batch must use id rock_tunnel_interior_batch")
    ids = {item.get("id") for item in batch.get("feed", [])}
    for message_id in [
        "wl_rock_tunnel_interior_reached",
        "wl_red_rock_tunnel_guidance",
        "wl_bill_lavender_echo_trace",
        "wl_team_moonlight_cave_pressure",
        "wl_rocket_dark_cache",
        "wl_flash_lantern_needed",
        "wl_lavender_exit_path_unlocked",
    ]:
        if message_id not in ids:
            errors.append(f"Rock Tunnel WorldLink batch missing id: {message_id}")

    markers = {
        "main": (
            "RockTunnelInteriorScene",
            "_on_go_to_rock_tunnel_interior",
            "_show_rock_tunnel_interior",
            "go_to_rock_tunnel_interior",
        ),
        "save": (
            "rock_tunnel_interior_reached",
            "red_rock_tunnel_guidance_seen",
            "bill_lavender_echo_trace_seen",
            "team_moonlight_cave_pressure_seen",
            "rocket_dark_cache_seen",
            "flash_lantern_needed_seen",
            "lavender_exit_path_unlocked",
            "queue_rock_tunnel_interior_batch",
        ),
        "route9_script": (
            "go_to_rock_tunnel_interior",
            "trigger_rock_tunnel_entry",
            "rock_tunnel_entry_unlocked",
            "Rock Tunnel",
        ),
        "tunnel_script": (
            "Rock Tunnel - Interior",
            "trigger_rock_tunnel_interior_scene",
            "record_rock_tunnel_interior_scene",
            "go_to_route_9_rock_tunnel_approach",
            "Red",
            "Bill",
            "Moonlight",
            "Rocket",
            "Lavender",
            "Echo Flute",
            "Flash Lantern",
            "Rock Tunnel",
        ),
        "worldlink": (
            "ROCK_TUNNEL_INTERIOR_BATCH_PATH",
            "Enter Rock Tunnel",
            "Track Lavender echo",
            "Pressure Team Moonlight in Rock Tunnel",
            "Unlock Lavender exit path",
        ),
        "test": (
            "rock_tunnel_interior_test",
            "trigger_rock_tunnel_entry",
            "trigger_rock_tunnel_interior_scene",
            "lavender_exit_path_unlocked",
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
        print("Native Rock Tunnel interior validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print("Native Rock Tunnel interior validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
