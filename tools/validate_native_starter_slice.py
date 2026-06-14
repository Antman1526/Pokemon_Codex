#!/usr/bin/env python3
"""Validate the native Oak lab and 39-starter selector slice."""

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
        "bedroom": NATIVE / "src" / "world" / "Bedroom.gd",
        "oak_scene": NATIVE / "scenes" / "world" / "OakLab.tscn",
        "oak_script": NATIVE / "src" / "world" / "OakLab.gd",
        "selector_script": NATIVE / "src" / "starter" / "StarterSelector.gd",
        "save": NATIVE / "src" / "save" / "SaveState.gd",
        "starter_data": NATIVE / "content" / "starters" / "starter_choices.json",
        "smoke": NATIVE / "tests" / "starter_slice_test.gd",
    }
    contents = {name: require_file(path, errors) for name, path in files.items()}
    if errors:
        return errors

    markers = {
        "main": ("OakLabScene", "_on_go_to_oak_lab", "_on_return_to_bedroom"),
        "bedroom": ("go_to_oak_lab", "Oak is waiting"),
        "oak_script": ("Professor Oak", "starter_chosen", "Blue:"),
        "selector_script": ("starter_selected", "starter_choices.json", "choose_starter"),
        "save": ("player_starter", "blue_starter", "ava_starter", "dax_starter", "choose_starter"),
        "smoke": ("starter_slice_test", "Bulbasaur", "blue_starter"),
    }
    for name, expected_markers in markers.items():
        for marker in expected_markers:
            if marker not in contents[name]:
                errors.append(f"{files[name].relative_to(ROOT)} missing marker: {marker}")

    data = json.loads(contents["starter_data"])
    starters = data.get("starters", [])
    if len(starters) != 39:
        errors.append(f"Expected 39 selectable starters, found {len(starters)}")
    species = {starter.get("species") for starter in starters}
    for species_name in ("Bulbasaur", "Charmander", "Squirtle", "Eevee", "Pikachu", "Dratini", "Larvitar", "Kubfu", "Ralts"):
        if species_name not in species:
            errors.append(f"starter_choices.json missing starter: {species_name}")
    if len(species) != len(starters):
        errors.append("starter_choices.json contains duplicate species")

    blue_rules = data.get("blue_counter_rules", {})
    if blue_rules.get("Bulbasaur") != "Charmander":
        errors.append("Blue counter rule for Bulbasaur must be Charmander")
    if blue_rules.get("Charmander") != "Squirtle":
        errors.append("Blue counter rule for Charmander must be Squirtle")
    if blue_rules.get("Squirtle") != "Bulbasaur":
        errors.append("Blue counter rule for Squirtle must be Bulbasaur")

    return errors


def main() -> int:
    errors = validate_files()
    if errors:
        print("Native starter slice validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print("Native starter slice validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
