#!/usr/bin/env python3
"""Validate the native S.S. Anne Rocket cargo hold investigation slice."""

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
        "deck": NATIVE / "src" / "world" / "SSAnneMainDeck.gd",
        "cargo_scene": NATIVE / "scenes" / "world" / "SSAnneCargoHold.tscn",
        "cargo_script": NATIVE / "src" / "world" / "SSAnneCargoHold.gd",
        "worldlink": NATIVE / "src" / "worldlink" / "WorldLinkPanel.gd",
        "worldlink_batch": NATIVE / "content" / "worldlink" / "ss_anne_cargo_hold_batch.json",
        "test": NATIVE / "tests" / "ss_anne_cargo_hold_test.gd",
    }
    contents = {name: require_file(path, errors) for name, path in files.items()}
    if errors:
        return errors

    batch = json.loads(contents["worldlink_batch"])
    if batch.get("id") != "ss_anne_cargo_hold_batch":
        errors.append("Cargo hold WorldLink batch must use id ss_anne_cargo_hold_batch")
    ids = {item.get("id") for item in batch.get("feed", [])}
    for message_id in [
        "wl_ss_anne_cargo_hold_reached",
        "wl_rocket_cargo_manifest_recovered",
        "wl_nexus_order_crate_symbol_seen",
        "wl_bill_cargo_decode_seen",
        "wl_ss_anne_captain_path_unlocked",
    ]:
        if message_id not in ids:
            errors.append(f"Cargo hold WorldLink batch missing id: {message_id}")

    markers = {
        "main": (
            "SSAnneCargoHoldScene",
            "_on_go_to_ss_anne_cargo_hold",
            "_show_ss_anne_cargo_hold",
            "go_to_ss_anne_main_deck",
        ),
        "save": (
            "ss_anne_cargo_hold_reached",
            "rocket_cargo_manifest_recovered",
            "nexus_order_crate_symbol_seen",
            "bill_cargo_decode_seen",
            "misty_lower_deck_waterline_seen",
            "red_cargo_hold_guard_seen",
            "ss_anne_captain_path_unlocked",
            "queue_ss_anne_cargo_hold_batch",
        ),
        "deck": (
            "go_to_ss_anne_cargo_hold",
            "trigger_cargo_hold_entry",
            "blue_ss_anne_battle_finished",
            "Cargo Hold",
        ),
        "cargo_script": (
            "S.S. Anne Cargo Hold",
            "trigger_cargo_hold_investigation",
            "record_ss_anne_cargo_hold_investigation",
            "Rocket",
            "Nexus Order",
            "Captain",
        ),
        "worldlink": (
            "SS_ANNE_CARGO_HOLD_BATCH_PATH",
            "Enter S.S. Anne cargo hold",
            "Recover Rocket cargo manifest",
            "Spot Nexus Order crate symbol",
            "Unlock Captain path",
        ),
        "test": (
            "ss_anne_cargo_hold_test",
            "trigger_cargo_hold_entry",
            "trigger_cargo_hold_investigation",
            "ss_anne_captain_path_unlocked",
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
        print("Native S.S. Anne cargo hold validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print("Native S.S. Anne cargo hold validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
