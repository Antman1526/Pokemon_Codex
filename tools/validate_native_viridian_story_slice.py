#!/usr/bin/env python3
"""Validate the native Viridian Red/Rocket WorldLink story slice."""

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
        "city": NATIVE / "src" / "world" / "ViridianCity.gd",
        "worldlink": NATIVE / "src" / "worldlink" / "WorldLinkPanel.gd",
        "batch": NATIVE / "content" / "worldlink" / "viridian_story_batch.json",
        "test": NATIVE / "tests" / "viridian_story_test.gd",
    }
    contents = {name: require_file(path, errors) for name, path in files.items()}
    if errors:
        return errors

    markers = {
        "save": (
            "viridian_red_scene_seen",
            "viridian_rocket_clue_found",
            "worldlink_viridian_story_batch_queued",
            "record_viridian_red_scene",
            "record_viridian_rocket_clue",
            "queue_viridian_story_batch",
        ),
        "city": (
            "interact_red_companion",
            "investigate_rocket_clue",
            "Rocket",
            "Red:",
        ),
        "worldlink": (
            "VIRIDIAN_BATCH_PATH",
            "viridian_story_batch.json",
            "Talk to Red in Viridian",
            "Find Viridian Rocket clue",
        ),
        "test": (
            "viridian_story_test",
            "interact_red_companion",
            "investigate_rocket_clue",
            "wl_red_viridian_checkin",
            "wl_rocket_viridian_clue",
        ),
    }
    for name, expected_markers in markers.items():
        for marker in expected_markers:
            if marker not in contents[name]:
                errors.append(f"{files[name].relative_to(ROOT)} missing marker: {marker}")

    data = json.loads(contents["batch"])
    if data.get("id") != "viridian_story_batch":
        errors.append("Viridian story batch must use id viridian_story_batch")
    entry_ids = {entry.get("id") for entry in data.get("feed", [])}
    for required_id in (
        "wl_red_viridian_checkin",
        "wl_rocket_viridian_clue",
        "wl_blue_viridian_sighting",
    ):
        if required_id not in entry_ids:
            errors.append(f"Viridian story batch missing id: {required_id}")

    return errors


def main() -> int:
    errors = validate_files()
    if errors:
        print("Native Viridian story validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print("Native Viridian story validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
