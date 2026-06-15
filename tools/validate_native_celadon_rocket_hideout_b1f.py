#!/usr/bin/env python3
"""Validate the native Celadon Rocket Hideout B1F slice."""

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
        "entry_script": NATIVE / "src" / "world" / "CeladonRocketHideoutEntry.gd",
        "b1f_scene": NATIVE / "scenes" / "world" / "CeladonRocketHideoutB1F.tscn",
        "b1f_script": NATIVE / "src" / "world" / "CeladonRocketHideoutB1F.gd",
        "worldlink": NATIVE / "src" / "worldlink" / "WorldLinkPanel.gd",
        "worldlink_batch": NATIVE / "content" / "worldlink" / "celadon_rocket_hideout_b1f_batch.json",
        "test": NATIVE / "tests" / "celadon_rocket_hideout_b1f_test.gd",
    }
    contents = {name: require_file(path, errors) for name, path in files.items()}
    if errors:
        return errors

    batch = json.loads(contents["worldlink_batch"])
    if batch.get("id") != "celadon_rocket_hideout_b1f_batch":
        errors.append("Rocket Hideout B1F WorldLink batch must use id celadon_rocket_hideout_b1f_batch")
    ids = {item.get("id") for item in batch.get("feed", [])}
    for message_id in [
        "wl_celadon_rocket_hideout_b1f_reached",
        "wl_red_hideout_b1f_maze_guard",
        "wl_bill_silph_scope_machine_trace",
        "wl_rocket_spinner_maze",
        "wl_gold_dust_hideout_infiltration",
        "wl_team_moonlight_hideout_signal_bleed",
        "wl_lift_key_deeper_trail",
        "wl_rocket_hideout_b2f_path_unlocked",
    ]:
        if message_id not in ids:
            errors.append(f"Rocket Hideout B1F WorldLink batch missing id: {message_id}")

    markers = {
        "main": (
            "CeladonRocketHideoutB1FScene",
            "_on_go_to_rocket_hideout_b1f",
            "_show_celadon_rocket_hideout_b1f",
            "go_to_rocket_hideout_b1f",
            "celadon_rocket_hideout_b1f",
        ),
        "save": (
            "celadon_rocket_hideout_b1f_reached",
            "red_hideout_b1f_maze_guard_seen",
            "bill_silph_scope_machine_trace_seen",
            "rocket_spinner_maze_seen",
            "gold_dust_hideout_infiltration_seen",
            "team_moonlight_hideout_signal_bleed_seen",
            "lift_key_deeper_trail_seen",
            "rocket_hideout_b2f_path_unlocked",
            "queue_celadon_rocket_hideout_b1f_batch",
        ),
        "entry_script": (
            "go_to_rocket_hideout_b1f",
            "trigger_rocket_hideout_b1f_entry",
            "rocket_hideout_b1f_path_unlocked",
        ),
        "b1f_script": (
            "Celadon Rocket Hideout - B1F",
            "trigger_rocket_hideout_b1f_scene",
            "record_celadon_rocket_hideout_b1f_scene",
            "go_to_rocket_hideout_b2f",
            "go_to_rocket_hideout_entry",
            "Red",
            "Bill",
            "Rocket",
            "Gold Dust",
            "Moonlight",
            "spinner",
            "Silph Scope",
            "Lift Key",
            "B2F",
        ),
        "worldlink": (
            "CELADON_ROCKET_HIDEOUT_B1F_BATCH_PATH",
            "Reach Rocket Hideout B1F",
            "Map Rocket spinner maze",
            "Spot Gold Dust infiltration",
            "Trace Moonlight hideout signal",
            "Unlock Hideout B2F path",
        ),
        "test": (
            "celadon_rocket_hideout_b1f_test",
            "trigger_rocket_hideout_b1f_entry",
            "trigger_rocket_hideout_b1f_scene",
            "rocket_hideout_b2f_path_unlocked",
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
        print("Native Celadon Rocket Hideout B1F validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print("Native Celadon Rocket Hideout B1F validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
