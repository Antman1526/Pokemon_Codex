#!/usr/bin/env python3
"""Validate the native S.S. Anne boarding and main deck setup slice."""

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
        "ticket": NATIVE / "src" / "world" / "SSAnneTicketOffice.gd",
        "deck_scene": NATIVE / "scenes" / "world" / "SSAnneMainDeck.tscn",
        "deck_script": NATIVE / "src" / "world" / "SSAnneMainDeck.gd",
        "worldlink": NATIVE / "src" / "worldlink" / "WorldLinkPanel.gd",
        "worldlink_batch": NATIVE / "content" / "worldlink" / "ss_anne_boarding_batch.json",
        "test": NATIVE / "tests" / "ss_anne_boarding_test.gd",
    }
    contents = {name: require_file(path, errors) for name, path in files.items()}
    if errors:
        return errors

    batch = json.loads(contents["worldlink_batch"])
    if batch.get("id") != "ss_anne_boarding_batch":
        errors.append("S.S. Anne boarding WorldLink batch must use id ss_anne_boarding_batch")
    ids = {item.get("id") for item in batch.get("feed", [])}
    for message_id in [
        "wl_ss_anne_boarded",
        "wl_red_ss_anne_boarding_scene",
        "wl_blue_ship_rival_tease",
        "wl_rocket_cargo_hold_clue",
        "wl_captain_trail_cutter_lead",
    ]:
        if message_id not in ids:
            errors.append(f"S.S. Anne boarding WorldLink batch missing id: {message_id}")

    markers = {
        "main": (
            "SSAnneMainDeckScene",
            "_on_go_to_ss_anne_main_deck",
            "_show_ss_anne_main_deck",
            "go_to_ss_anne_ticket_office",
        ),
        "save": (
            "ss_anne_main_deck_reached",
            "ss_anne_boarded",
            "red_ss_anne_boarding_scene_seen",
            "blue_ship_rival_teased",
            "rocket_cargo_hold_clue_seen",
            "captain_trail_cutter_lead_seen",
            "queue_ss_anne_boarding_batch",
        ),
        "ticket": (
            "go_to_ss_anne_main_deck",
            "trigger_ss_anne_boarding",
            "ss_anne_boarding_pass_earned",
            "boarding pass",
        ),
        "deck_script": (
            "S.S. Anne Main Deck",
            "trigger_deck_boarding_scene",
            "record_ss_anne_deck_boarding_scene",
            "Blue",
            "Rocket",
            "Trail Cutter",
        ),
        "worldlink": (
            "SS_ANNE_BOARDING_BATCH_PATH",
            "Board S.S. Anne",
            "Spot Blue aboard S.S. Anne",
            "Find Rocket cargo-hold clue",
            "Track Captain's Trail Cutter lead",
        ),
        "test": (
            "ss_anne_boarding_test",
            "trigger_ss_anne_boarding",
            "trigger_deck_boarding_scene",
            "captain_trail_cutter_lead_seen",
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
        print("Native S.S. Anne boarding validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print("Native S.S. Anne boarding validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
