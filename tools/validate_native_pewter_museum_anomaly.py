#!/usr/bin/env python3
"""Validate the native post-Brock Pewter Museum anomaly slice."""

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
        "pewter": NATIVE / "src" / "world" / "PewterCity.gd",
        "worldlink": NATIVE / "src" / "worldlink" / "WorldLinkPanel.gd",
        "batch": NATIVE / "content" / "worldlink" / "pewter_museum_anomaly_batch.json",
        "test": NATIVE / "tests" / "pewter_museum_anomaly_test.gd",
    }
    contents = {name: require_file(path, errors) for name, path in files.items()}
    if errors:
        return errors

    markers = {
        "save": (
            "pewter_museum_anomaly_seen",
            "worldlink_pewter_museum_batch_queued",
            "record_pewter_museum_anomaly",
            "queue_pewter_museum_batch",
            "wl_rocket_pewter_museum_anomaly",
        ),
        "pewter": (
            "investigate_museum_anomaly",
            "brock_pewter_badge_earned",
            "Pewter Museum",
            "Red:",
            "Rocket",
        ),
        "worldlink": (
            "PEWTER_MUSEUM_BATCH_PATH",
            "pewter_museum_anomaly_batch.json",
            "Earn Boulder Badge",
            "Investigate Pewter Museum anomaly",
        ),
        "test": (
            "pewter_museum_anomaly_test",
            "investigate_museum_anomaly",
            "pewter_museum_anomaly_seen",
            "wl_red_pewter_museum_scan",
            "wl_rocket_pewter_museum_anomaly",
        ),
    }
    for name, expected_markers in markers.items():
        for marker in expected_markers:
            if marker not in contents[name]:
                errors.append(f"{files[name].relative_to(ROOT)} missing marker: {marker}")

    data = json.loads(contents["batch"])
    if data.get("id") != "pewter_museum_anomaly_batch":
        errors.append("Pewter Museum batch must use id pewter_museum_anomaly_batch")
    if data.get("trigger") != "post_brock_pewter_museum_anomaly":
        errors.append("Pewter Museum batch must use trigger post_brock_pewter_museum_anomaly")
    entry_ids = {entry.get("id") for entry in data.get("feed", [])}
    for required_id in (
        "wl_red_pewter_museum_scan",
        "wl_rocket_pewter_museum_anomaly",
        "wl_bill_fossil_energy_ping",
    ):
        if required_id not in entry_ids:
            errors.append(f"Pewter Museum batch missing id: {required_id}")

    return errors


def main() -> int:
    errors = validate_files()
    if errors:
        print("Native Pewter Museum anomaly validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print("Native Pewter Museum anomaly validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
