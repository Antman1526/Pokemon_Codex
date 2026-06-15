#!/usr/bin/env python3
"""Validate the native Route 8 Celadon road slice."""

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
        "tower_script": NATIVE / "src" / "world" / "PokemonTowerFirstFloor.gd",
        "route8_scene": NATIVE / "scenes" / "world" / "Route8CeladonRoad.tscn",
        "route8_script": NATIVE / "src" / "world" / "Route8CeladonRoad.gd",
        "worldlink": NATIVE / "src" / "worldlink" / "WorldLinkPanel.gd",
        "worldlink_batch": NATIVE / "content" / "worldlink" / "route_8_celadon_road_batch.json",
        "test": NATIVE / "tests" / "route8_celadon_road_test.gd",
    }
    contents = {name: require_file(path, errors) for name, path in files.items()}
    if errors:
        return errors

    batch = json.loads(contents["worldlink_batch"])
    if batch.get("id") != "route_8_celadon_road_batch":
        errors.append("Route 8 Celadon road WorldLink batch must use id route_8_celadon_road_batch")
    ids = {item.get("id") for item in batch.get("feed", [])}
    for message_id in [
        "wl_route_8_celadon_road_reached",
        "wl_red_route_8_westbound",
        "wl_bill_silph_scope_celadon_trace",
        "wl_rocket_celadon_game_corner_lead",
        "wl_team_moonlight_route_8_shadow",
        "wl_underground_path_to_celadon_unlocked",
        "wl_celadon_city_teased",
    ]:
        if message_id not in ids:
            errors.append(f"Route 8 Celadon road WorldLink batch missing id: {message_id}")

    markers = {
        "main": (
            "Route8CeladonRoadScene",
            "_on_go_to_route_8_celadon_road",
            "_show_route_8_celadon_road",
            "go_to_route_8_celadon_road",
        ),
        "save": (
            "route_8_celadon_road_reached",
            "red_route_8_westbound_seen",
            "bill_silph_scope_celadon_trace_seen",
            "rocket_celadon_game_corner_lead_seen",
            "team_moonlight_route_8_shadow_seen",
            "underground_path_to_celadon_unlocked",
            "celadon_city_teased",
            "queue_route_8_celadon_road_batch",
        ),
        "tower_script": (
            "go_to_route_8_celadon_road",
            "trigger_route_8_celadon_lead",
            "silph_scope_need_seen",
            "Route 8",
            "Celadon",
        ),
        "route8_script": (
            "Route 8 - Celadon Road",
            "trigger_route_8_celadon_road_scene",
            "record_route_8_celadon_road_scene",
            "go_to_pokemon_tower_first_floor",
            "Red",
            "Bill",
            "Rocket",
            "Moonlight",
            "Route 8",
            "Celadon",
            "Silph Scope",
            "Game Corner",
            "Underground Path",
        ),
        "worldlink": (
            "ROUTE_8_CELADON_ROAD_BATCH_PATH",
            "Reach Route 8",
            "Trace Silph Scope toward Celadon",
            "Find Rocket Game Corner lead",
            "Unlock Underground Path to Celadon",
        ),
        "test": (
            "route8_celadon_road_test",
            "trigger_route_8_celadon_lead",
            "trigger_route_8_celadon_road_scene",
            "underground_path_to_celadon_unlocked",
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
        print("Native Route 8 Celadon road validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print("Native Route 8 Celadon road validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
