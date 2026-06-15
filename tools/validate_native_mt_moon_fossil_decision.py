#!/usr/bin/env python3
"""Validate the native Mt. Moon fossil decision scene slice."""

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
        "interior": NATIVE / "src" / "world" / "MtMoonInterior1.gd",
        "decision_scene": NATIVE / "scenes" / "world" / "MtMoonFossilDecision.tscn",
        "decision_script": NATIVE / "src" / "world" / "MtMoonFossilDecision.gd",
        "worldlink": NATIVE / "src" / "worldlink" / "WorldLinkPanel.gd",
        "batch": NATIVE / "content" / "worldlink" / "mt_moon_fossil_decision_batch.json",
        "test": NATIVE / "tests" / "mt_moon_fossil_decision_test.gd",
    }
    contents = {name: require_file(path, errors) for name, path in files.items()}
    if errors:
        return errors

    markers = {
        "main": (
            "MtMoonFossilDecisionScene",
            "_on_go_to_mt_moon_fossil_decision",
            "_show_mt_moon_fossil_decision",
        ),
        "save": (
            "enter_mt_moon_fossil_decision",
            "choose_mt_moon_fossil",
            "mt_moon_fossil_decision_reached",
            "mt_moon_fossil_choice_made",
            "dome_fossil_chosen",
            "helix_fossil_chosen",
            "nexus_fossil_deeper_signal_seen",
        ),
        "interior": (
            "go_to_mt_moon_fossil_decision",
            "trigger_fossil_decision_scene",
            "mt_moon_rocket_left_battle_finished",
            "mt_moon_gold_dust_right_battle_finished",
        ),
        "decision_script": (
            "Mt. Moon Fossil Decision",
            "choose_dome_fossil",
            "choose_helix_fossil",
            "Dome Fossil",
            "Helix Fossil",
            "Nexus Fossil",
            "return_to_mt_moon_interior_1",
        ),
        "worldlink": (
            "MT_MOON_FOSSIL_DECISION_BATCH_PATH",
            "mt_moon_fossil_decision_batch.json",
            "Reach fossil decision",
            "Choose Mt. Moon fossil",
        ),
        "test": (
            "mt_moon_fossil_decision_test",
            "trigger_fossil_decision_scene",
            "choose_dome_fossil",
            "dome_fossil_chosen",
            "nexus_fossil_deeper_signal_seen",
        ),
    }
    for name, expected_markers in markers.items():
        for marker in expected_markers:
            if marker not in contents[name]:
                errors.append(f"{files[name].relative_to(ROOT)} missing marker: {marker}")

    data = json.loads(contents["batch"])
    if data.get("id") != "mt_moon_fossil_decision_batch":
        errors.append("Mt. Moon fossil decision batch must use id mt_moon_fossil_decision_batch")
    if data.get("trigger") != "mt_moon_fossil_decision_after_faction_pressure":
        errors.append("Mt. Moon fossil decision batch must use trigger mt_moon_fossil_decision_after_faction_pressure")
    entry_ids = {entry.get("id") for entry in data.get("feed", [])}
    for required_id in (
        "wl_mt_moon_fossil_decision_reached",
        "wl_mt_moon_fossil_choice_made",
        "wl_nexus_fossil_deeper_signal",
    ):
        if required_id not in entry_ids:
            errors.append(f"Mt. Moon fossil decision batch missing id: {required_id}")

    return errors


def main() -> int:
    errors = validate_files()
    if errors:
        print("Native Mt. Moon fossil decision validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print("Native Mt. Moon fossil decision validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
