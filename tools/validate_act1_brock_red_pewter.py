#!/usr/bin/env python3
"""Validate the Act 1 Brock, Red, and Pewter Museum slice."""

from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ENGINE = ROOT / "engine" / "pokeemerald-expansion"

REQUIRED_PATCHES = (
    "0008-red-route1-viridian-pewter-training.patch",
    "0009-brock-expanded-starter-pool-balance.patch",
    "0010-pewter-museum-rocket-anomaly-hook.patch",
)


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def load_map(name: str) -> dict:
    return json.loads(read(ENGINE / "data" / "maps" / name / "map.json"))


def validate_patch_files() -> list[str]:
    errors: list[str] = []
    for patch_name in REQUIRED_PATCHES:
        patch_path = ROOT / "patches" / "engine" / patch_name
        if not patch_path.exists():
            errors.append(f"missing patch file: {patch_name}")
        elif patch_path.stat().st_size == 0:
            errors.append(f"empty patch file: {patch_name}")
    return errors


def validate_red_scenes() -> list[str]:
    errors: list[str] = []
    map_specs = {
        "Route1_Frlg": ("Route1_EventScript_RedTraining", "Antman, over here"),
        "ViridianCity_Frlg": ("ViridianCity_EventScript_RedTraining", "Build a bench before PEWTER"),
        "PewterCity_Frlg": ("PewterCity_EventScript_RedTraining", "WORLDLINK just flagged PEWTER"),
    }

    for map_name, (script_name, required_text) in map_specs.items():
        scripts = read(ENGINE / "data" / "maps" / map_name / "scripts.inc")
        if script_name not in scripts:
            errors.append(f"{map_name} missing {script_name}")
        if required_text not in scripts:
            errors.append(f"{map_name} missing Red dialogue marker: {required_text}")

        map_data = load_map(map_name)
        objects = map_data.get("object_events", [])
        has_red = any(
            obj.get("graphics_id") == "OBJ_EVENT_GFX_RED"
            and obj.get("script") == script_name
            for obj in objects
        )
        if not has_red:
            errors.append(f"{map_name} missing Red object for {script_name}")

    pewter_scripts = read(ENGINE / "data" / "maps" / "PewterCity_Frlg" / "scripts.inc")
    if "goto_if_set FLAG_BADGE01_GET, PewterCity_EventScript_RedTrainingPostBrock" not in pewter_scripts:
        errors.append("Pewter Red scene must change after Boulder Badge")

    return errors


def brock_block() -> str:
    trainers = read(ENGINE / "src" / "data" / "trainers_frlg.party")
    match = re.search(
        r"=== TRAINER_LEADER_BROCK ===(?P<block>.*?)\n=== TRAINER_",
        trainers,
        re.S,
    )
    if not match:
        raise ValueError("TRAINER_LEADER_BROCK block not found")
    return match.group("block")


def validate_brock_balance() -> list[str]:
    errors: list[str] = []
    try:
        block = brock_block()
    except ValueError as exc:
        return [str(exc)]

    expected_species = ("Geodude", "Nosepass", "Onix")
    for species in expected_species:
        if species not in block:
            errors.append(f"Brock missing {species}")

    levels = [int(level) for level in re.findall(r"Level: (\d+)", block)]
    if levels != [12, 12, 14]:
        errors.append(f"Brock levels should be [12, 12, 14], found {levels}")
    if max(levels or [0]) > 14:
        errors.append("Brock exceeds first badge level cap 14")
    if "Rock Throw" not in block or "Rock Tomb" not in block:
        errors.append("Brock should keep Rock pressure through Rock Throw and Rock Tomb")

    return errors


def validate_pewter_museum_hook() -> list[str]:
    errors: list[str] = []
    gym_scripts = read(ENGINE / "data" / "maps" / "PewterCity_Gym_Frlg" / "scripts.inc")
    museum_scripts = read(ENGINE / "data" / "maps" / "PewterCity_Museum_1F_Frlg" / "scripts.inc")
    museum_map = load_map("PewterCity_Museum_1F_Frlg")

    gym_markers = ("PewterCity_Gym_Text_WorldLinkMuseumAlert", "PEWTER MUSEUM", "fossil scan")
    for marker in gym_markers:
        if marker not in gym_scripts:
            errors.append(f"Pewter Gym missing WorldLink alert marker: {marker}")

    museum_markers = (
        "PewterCity_Museum_1F_EventScript_NexusFossilAide",
        "goto_if_unset FLAG_BADGE01_GET",
        "ROCKET",
        "wasn't purely KANTO",
        "MT. MOON starts glowing",
    )
    for marker in museum_markers:
        if marker not in museum_scripts:
            errors.append(f"Pewter Museum missing anomaly marker: {marker}")

    has_aide = any(
        obj.get("script") == "PewterCity_Museum_1F_EventScript_NexusFossilAide"
        for obj in museum_map.get("object_events", [])
    )
    if not has_aide:
        errors.append("Pewter Museum missing Nexus fossil aide object")

    return errors


def main() -> int:
    errors: list[str] = []
    errors.extend(validate_patch_files())
    errors.extend(validate_red_scenes())
    errors.extend(validate_brock_balance())
    errors.extend(validate_pewter_museum_hook())

    if errors:
        print("Act 1 Brock/Red/Pewter validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Act 1 Brock/Red/Pewter validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
