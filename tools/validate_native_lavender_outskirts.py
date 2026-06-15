#!/usr/bin/env python3
"""Validate the native Lavender outskirts slice."""

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
        "tunnel_script": NATIVE / "src" / "world" / "RockTunnelInterior.gd",
        "lavender_scene": NATIVE / "scenes" / "world" / "LavenderOutskirts.tscn",
        "lavender_script": NATIVE / "src" / "world" / "LavenderOutskirts.gd",
        "worldlink": NATIVE / "src" / "worldlink" / "WorldLinkPanel.gd",
        "worldlink_batch": NATIVE / "content" / "worldlink" / "lavender_outskirts_batch.json",
        "test": NATIVE / "tests" / "lavender_outskirts_test.gd",
    }
    contents = {name: require_file(path, errors) for name, path in files.items()}
    if errors:
        return errors

    batch = json.loads(contents["worldlink_batch"])
    if batch.get("id") != "lavender_outskirts_batch":
        errors.append("Lavender outskirts WorldLink batch must use id lavender_outskirts_batch")
    ids = {item.get("id") for item in batch.get("feed", [])}
    for message_id in [
        "wl_lavender_outskirts_reached",
        "wl_red_lavender_arrival",
        "wl_bill_pokemon_tower_signal_decode",
        "wl_team_moonlight_lavender_presence",
        "wl_rocket_lavender_surveillance",
        "wl_pokemon_tower_signal_confirmed",
        "wl_pokemon_tower_entry_unlocked",
    ]:
        if message_id not in ids:
            errors.append(f"Lavender outskirts WorldLink batch missing id: {message_id}")

    markers = {
        "main": (
            "LavenderOutskirtsScene",
            "_on_go_to_lavender_outskirts",
            "_show_lavender_outskirts",
            "go_to_lavender_outskirts",
        ),
        "save": (
            "lavender_outskirts_reached",
            "red_lavender_arrival_seen",
            "bill_pokemon_tower_signal_decode_seen",
            "team_moonlight_lavender_presence_seen",
            "rocket_lavender_surveillance_seen",
            "pokemon_tower_signal_confirmed",
            "pokemon_tower_entry_unlocked",
            "queue_lavender_outskirts_batch",
        ),
        "tunnel_script": (
            "go_to_lavender_outskirts",
            "trigger_lavender_exit",
            "lavender_exit_path_unlocked",
            "Lavender",
        ),
        "lavender_script": (
            "Lavender Outskirts",
            "trigger_lavender_outskirts_scene",
            "record_lavender_outskirts_scene",
            "go_to_rock_tunnel_interior",
            "Red",
            "Bill",
            "Moonlight",
            "Rocket",
            "Lavender",
            "Pokemon Tower",
            "Echo Flute",
        ),
        "worldlink": (
            "LAVENDER_OUTSKIRTS_BATCH_PATH",
            "Reach Lavender outskirts",
            "Decode Pokemon Tower signal",
            "Spot Moonlight in Lavender",
            "Unlock Pokemon Tower entry",
        ),
        "test": (
            "lavender_outskirts_test",
            "trigger_lavender_exit",
            "trigger_lavender_outskirts_scene",
            "pokemon_tower_entry_unlocked",
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
        print("Native Lavender outskirts validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print("Native Lavender outskirts validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
