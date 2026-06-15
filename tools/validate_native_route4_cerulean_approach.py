#!/usr/bin/env python3
"""Validate the native Route 4 Cerulean approach slice."""

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
        "decision_script": NATIVE / "src" / "world" / "MtMoonFossilDecision.gd",
        "route4_scene": NATIVE / "scenes" / "world" / "Route4CeruleanApproach.tscn",
        "route4_script": NATIVE / "src" / "world" / "Route4CeruleanApproach.gd",
        "worldlink": NATIVE / "src" / "worldlink" / "WorldLinkPanel.gd",
        "batch": NATIVE / "content" / "worldlink" / "route_4_cerulean_approach_batch.json",
        "test": NATIVE / "tests" / "route4_cerulean_approach_test.gd",
    }
    contents = {name: require_file(path, errors) for name, path in files.items()}
    if errors:
        return errors

    markers = {
        "main": (
            "Route4CeruleanApproachScene",
            "_on_go_to_route_4_cerulean_approach",
            "_show_route_4_cerulean_approach",
        ),
        "save": (
            "enter_route_4_cerulean_approach",
            "record_red_route_4_cerulean_warning",
            "route_4_cerulean_approach_reached",
            "red_route_4_cerulean_warning_seen",
            "cerulean_bridge_threat_teased",
            "worldlink_route_4_cerulean_batch_queued",
        ),
        "decision_script": (
            "go_to_route_4_cerulean_approach",
            "proceed_to_route_4_cerulean_approach",
            "mt_moon_fossil_choice_made",
        ),
        "route4_script": (
            "Route 4 - Cerulean Approach",
            "trigger_red_cerulean_warning",
            "return_to_mt_moon_fossil_decision",
            "Cerulean",
            "Misty",
            "Rocket",
            "Gold Dust",
        ),
        "worldlink": (
            "ROUTE_4_CERULEAN_BATCH_PATH",
            "route_4_cerulean_approach_batch.json",
            "Reach Route 4",
            "Hear Red's Cerulean warning",
        ),
        "test": (
            "route4_cerulean_approach_test",
            "proceed_to_route_4_cerulean_approach",
            "trigger_red_cerulean_warning",
            "cerulean_bridge_threat_teased",
        ),
    }
    for name, expected_markers in markers.items():
        for marker in expected_markers:
            if marker not in contents[name]:
                errors.append(f"{files[name].relative_to(ROOT)} missing marker: {marker}")

    data = json.loads(contents["batch"])
    if data.get("id") != "route_4_cerulean_approach_batch":
        errors.append("Route 4 Cerulean batch must use id route_4_cerulean_approach_batch")
    if data.get("trigger") != "route_4_after_mt_moon_fossil_choice":
        errors.append("Route 4 Cerulean batch must use trigger route_4_after_mt_moon_fossil_choice")
    entry_ids = {entry.get("id") for entry in data.get("feed", [])}
    for required_id in (
        "wl_route_4_cerulean_approach",
        "wl_red_route_4_cerulean_warning",
        "wl_cerulean_bridge_threat_tease",
    ):
        if required_id not in entry_ids:
            errors.append(f"Route 4 Cerulean batch missing id: {required_id}")

    return errors


def main() -> int:
    errors = validate_files()
    if errors:
        print("Native Route 4 Cerulean approach validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print("Native Route 4 Cerulean approach validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
