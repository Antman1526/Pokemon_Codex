#!/usr/bin/env python3
"""Validate the native Route 1 party/status panel slice."""

from __future__ import annotations

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
        "route": NATIVE / "src" / "world" / "Route1.gd",
        "panel": NATIVE / "src" / "ui" / "PartyStatusPanel.gd",
        "test": NATIVE / "tests" / "route1_party_panel_test.gd",
    }
    contents = {name: require_file(path, errors) for name, path in files.items()}
    if errors:
        return errors

    markers = {
        "route": (
            "PartyStatusPanel",
            "party_panel",
            "_toggle_party_panel",
            "is_action_pressed(\"menu\")",
        ),
        "panel": (
            "Party Status",
            "party_roster",
            "captured_creatures",
            "refresh",
        ),
        "test": (
            "route1_party_panel_test",
            "_toggle_party_panel",
            "party_panel",
            "Bulbasaur",
            "Rattata",
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
        print("Native Route 1 party panel validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print("Native Route 1 party panel validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
