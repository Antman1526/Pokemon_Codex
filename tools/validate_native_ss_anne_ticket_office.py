#!/usr/bin/env python3
"""Validate the native S.S. Anne ticket office setup slice."""

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
        "vermilion": NATIVE / "src" / "world" / "VermilionCity.gd",
        "ticket_scene": NATIVE / "scenes" / "world" / "SSAnneTicketOffice.tscn",
        "ticket_script": NATIVE / "src" / "world" / "SSAnneTicketOffice.gd",
        "worldlink": NATIVE / "src" / "worldlink" / "WorldLinkPanel.gd",
        "worldlink_batch": NATIVE / "content" / "worldlink" / "ss_anne_ticket_office_batch.json",
        "test": NATIVE / "tests" / "ss_anne_ticket_office_test.gd",
    }
    contents = {name: require_file(path, errors) for name, path in files.items()}
    if errors:
        return errors

    batch = json.loads(contents["worldlink_batch"])
    if batch.get("id") != "ss_anne_ticket_office_batch":
        errors.append("S.S. Anne WorldLink batch must use id ss_anne_ticket_office_batch")
    ids = {item.get("id") for item in batch.get("feed", [])}
    for message_id in [
        "wl_ss_anne_ticket_office_reached",
        "wl_ss_anne_manifest_checked",
        "wl_bill_manifest_decode_seen",
        "wl_red_harbor_guard_scene",
        "wl_ss_anne_boarding_pass_earned",
    ]:
        if message_id not in ids:
            errors.append(f"S.S. Anne WorldLink batch missing id: {message_id}")

    markers = {
        "main": (
            "SSAnneTicketOfficeScene",
            "_on_go_to_ss_anne_ticket_office",
            "_show_ss_anne_ticket_office",
            "go_to_vermilion_city",
        ),
        "save": (
            "ss_anne_ticket_office_reached",
            "ss_anne_manifest_checked",
            "bill_manifest_decode_seen",
            "red_harbor_guard_scene_seen",
            "ss_anne_boarding_pass_earned",
            "queue_ss_anne_ticket_office_batch",
        ),
        "vermilion": (
            "go_to_ss_anne_ticket_office",
            "trigger_ss_anne_ticket_office_entry",
            "ss_anne_ticket_lead_seen",
            "harbor",
        ),
        "ticket_script": (
            "S.S. Anne Ticket Office",
            "trigger_ticket_office_scene",
            "record_ss_anne_ticket_office_scene",
            "Bill",
            "Misty",
            "Red",
            "boarding pass",
        ),
        "worldlink": (
            "SS_ANNE_TICKET_OFFICE_BATCH_PATH",
            "Reach S.S. Anne ticket office",
            "Check S.S. Anne manifest",
            "Decode Bill's manifest anomaly",
            "Earn S.S. Anne boarding pass",
        ),
        "test": (
            "ss_anne_ticket_office_test",
            "trigger_ss_anne_ticket_office_entry",
            "trigger_ticket_office_scene",
            "ss_anne_boarding_pass_earned",
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
        print("Native S.S. Anne ticket office validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print("Native S.S. Anne ticket office validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
