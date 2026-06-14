#!/usr/bin/env python3
"""Validate the Route 25 Red and Gold Dust tag setup slice."""

from __future__ import annotations

import json
import re
from pathlib import Path

try:
    import yaml
except ImportError as exc:
    raise SystemExit("PyYAML is required: python3 -m pip install PyYAML") from exc


ROOT = Path(__file__).resolve().parents[1]
ENGINE = ROOT / "engine" / "pokeemerald-expansion"
PATCH = ROOT / "patches" / "engine" / "0013-route25-red-gold-dust-tag.patch"
POLICY = ROOT / "data_design" / "red_tag_battle_policy.yaml"
WORLDLINK = ROOT / "data_design" / "worldlink_region_progression.yaml"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def load_map(name: str) -> dict:
    return json.loads(read(ENGINE / "data" / "maps" / name / "map.json"))


def validate_patch_file() -> list[str]:
    if not PATCH.exists():
        return ["missing patch file: 0013-route25-red-gold-dust-tag.patch"]
    if PATCH.stat().st_size == 0:
        return ["empty patch file: 0013-route25-red-gold-dust-tag.patch"]
    patch = read(PATCH)
    if "Nosepass" in patch:
        return ["patch 0013 must not include Brock/Nosepass changes from patch 0009"]
    return []


def validate_route25() -> list[str]:
    errors: list[str] = []
    scripts = read(ENGINE / "data" / "maps" / "Route25_Frlg" / "scripts.inc")
    route = load_map("Route25_Frlg")

    for marker in (
        "Route25_EventScript_RedGoldDustTag",
        "trainerbattle_two_trainers TRAINER_TEAM_ROCKET_GRUNT_ROUTE25_NEXUS",
        "TRAINER_GOLD_DUST_BROKER_AUREL",
        "GOLD DUST: Claimed?",
        "first tag win",
        "BLUE heard I was traveling with you",
    ):
        if marker not in scripts:
            errors.append(f"Route 25 missing marker: {marker}")

    objects = route.get("object_events", [])
    required_objects = {
        "OBJ_EVENT_GFX_RED": "Route25_EventScript_RedGoldDustTag",
        "OBJ_EVENT_GFX_ROCKET_M": "Route25_EventScript_RedGoldDustTag",
        "OBJ_EVENT_GFX_GENTLEMAN": "Route25_EventScript_RedGoldDustTag",
    }
    for graphics_id, script in required_objects.items():
        if not any(obj.get("graphics_id") == graphics_id and obj.get("script") == script for obj in objects):
            errors.append(f"Route 25 missing object {graphics_id} with script {script}")

    return errors


def validate_bill_text() -> list[str]:
    errors: list[str] = []
    scripts = read(ENGINE / "data" / "maps" / "Route25_SeaCottage_Frlg" / "scripts.inc")
    for marker in (
        "WorldLink pulse",
        "gold fossil shard",
        "WorldLink residue",
        "Now I'm combined with a POKéMON",
    ):
        if marker not in scripts:
            errors.append(f"Bill text missing marker: {marker}")
    return errors


def validate_trainers() -> list[str]:
    errors: list[str] = []
    trainers = read(ENGINE / "src" / "data" / "trainers_frlg.party")
    opponents = read(ENGINE / "include" / "constants" / "opponents_frlg.h")
    required_markers = (
        "=== TRAINER_TEAM_ROCKET_GRUNT_ROUTE25_NEXUS ===",
        "Koffing\nLevel: 18",
        "=== TRAINER_GOLD_DUST_BROKER_AUREL ===",
        "Name: AUREL",
        "Meowth\nLevel: 18",
        "- Pay Day",
    )
    for marker in required_markers:
        if marker not in trainers:
            errors.append(f"Trainer data missing marker: {marker}")

    for marker in (
        "#define TRAINER_TEAM_ROCKET_GRUNT_ROUTE25_NEXUS    624",
        "#define TRAINER_GOLD_DUST_BROKER_AUREL             625",
    ):
        if marker not in opponents:
            errors.append(f"Opponent constants missing marker: {marker}")
    count_match = re.search(r"#define TRAINERS_COUNT_FRLG\s+(\d+)", opponents)
    if not count_match:
        errors.append("Opponent constants missing TRAINERS_COUNT_FRLG")
    elif int(count_match.group(1)) < 626:
        errors.append(f"TRAINERS_COUNT_FRLG must be at least 626, got {count_match.group(1)}")
    return errors


def validate_policy() -> list[str]:
    errors: list[str] = []
    data = yaml.safe_load(read(POLICY))
    kanto = data.get("red_tag_battle_policy", {}).get("region_cadence", {}).get("kanto", {})
    candidate = kanto.get("first_true_tag_battle_candidate", "")
    if "Route 25" not in candidate:
        errors.append("Kanto first tag-battle policy must name Route 25")
    if "Team Gold Dust" not in candidate:
        errors.append("Kanto first tag-battle policy must include Team Gold Dust")
    return errors


def validate_worldlink_progression() -> list[str]:
    errors: list[str] = []
    if not WORLDLINK.exists():
        return ["missing data_design/worldlink_region_progression.yaml"]

    data = yaml.safe_load(read(WORLDLINK))
    progression = data.get("worldlink_region_progression", {})
    if "not a free fast-travel region selector" not in progression.get("principle", ""):
        errors.append("WorldLink principle must reject free region selection during main story")
    if "Only the active region is open" not in progression.get("current_main_story_rule", ""):
        errors.append("WorldLink rule must limit main-story access to the active region")

    order = progression.get("unlock_order", [])
    expected = [
        "kanto",
        "johto",
        "hoenn",
        "sinnoh_hisui",
        "unova",
        "kalos",
        "alola",
        "galar",
        "paldea",
    ]
    actual = [region.get("region") for region in order]
    if actual != expected:
        errors.append(f"WorldLink unlock order mismatch: {actual}")
    if order and order[0].get("unlock_state") != "unlocked_at_new_game":
        errors.append("Kanto must be unlocked at new game")
    for region in order[1:]:
        if region.get("region") == "johto":
            if region.get("unlock_state") not in {"locked", "unlocked_after_kanto_passport"}:
                errors.append("Johto must stay locked until Kanto passport clearance")
            if "after Kanto" not in region.get("lock_condition", ""):
                errors.append("Johto lock condition must remain tied to Kanto completion")
            continue
        if region.get("unlock_state") != "locked":
            errors.append(f"{region.get('region')} must start locked")

    return errors


def main() -> int:
    errors: list[str] = []
    errors.extend(validate_patch_file())
    errors.extend(validate_route25())
    errors.extend(validate_bill_text())
    errors.extend(validate_trainers())
    errors.extend(validate_policy())
    errors.extend(validate_worldlink_progression())

    if errors:
        print("Route 25 Red Gold Dust validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Route 25 Red Gold Dust validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
