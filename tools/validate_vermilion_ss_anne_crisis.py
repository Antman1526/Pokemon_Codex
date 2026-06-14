#!/usr/bin/env python3
"""Validate the Vermilion and S.S. Anne crisis slice."""

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
PATCH = ROOT / "patches" / "engine" / "0014-vermilion-ss-anne-crisis.patch"
COMPANIONS = ROOT / "data_design" / "companions.yaml"
KANTO = ROOT / "data_design" / "kanto_chapter.yaml"
WORLDLINK = ROOT / "data_design" / "worldlink_region_progression.yaml"
SPEC = ROOT / "docs" / "superpowers" / "specs" / "2026-06-13-vermilion-ss-anne-crisis-design.md"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def load_map(name: str) -> dict:
    return json.loads(read(ENGINE / "data" / "maps" / name / "map.json"))


def validate_patch_and_spec() -> list[str]:
    errors: list[str] = []
    if not PATCH.exists():
        errors.append("missing patch file: 0014-vermilion-ss-anne-crisis.patch")
    elif PATCH.stat().st_size == 0:
        errors.append("empty patch file: 0014-vermilion-ss-anne-crisis.patch")
    else:
        patch = read(PATCH)
        for marker in (
            "VermilionCity_EventScript_BlueJealousy",
            "SSAnne_2F_Corridor_EventScript_ManifestCrisis",
            "TRAINER_TEAM_ROCKET_GRUNT_SS_ANNE_MANIFEST",
            "TRAINER_GOLD_DUST_BROKER_MIDAS",
        ):
            if marker not in patch:
                errors.append(f"patch 0014 missing marker: {marker}")

    if not SPEC.exists():
        errors.append("missing Vermilion S.S. Anne crisis spec")
    else:
        spec = read(SPEC)
        for marker in ("Misty becomes a recurring companion after the S.S. Anne crisis", "Johto remains locked"):
            if marker not in spec:
                errors.append(f"spec missing marker: {marker}")
    return errors


def validate_vermilion() -> list[str]:
    errors: list[str] = []
    scripts = read(ENGINE / "data" / "maps" / "VermilionCity_Frlg" / "scripts.inc")
    vermilion = load_map("VermilionCity_Frlg")

    for marker in (
        "VermilionCity_EventScript_RedHarbor",
        "VermilionCity_EventScript_BlueJealousy",
        "VermilionCity_EventScript_MistyHarbor",
        "RED is waiting around",
        "I'm in",
        "JOHTO signal detected",
        "Region access locked until KANTO",
    ):
        if marker not in scripts:
            errors.append(f"Vermilion scripts missing marker: {marker}")

    required_objects = {
        "OBJ_EVENT_GFX_RED": "VermilionCity_EventScript_RedHarbor",
        "OBJ_EVENT_GFX_BLUE": "VermilionCity_EventScript_BlueJealousy",
        "OBJ_EVENT_GFX_MISTY": "VermilionCity_EventScript_MistyHarbor",
    }
    objects = vermilion.get("object_events", [])
    for graphics_id, script in required_objects.items():
        if not any(obj.get("graphics_id") == graphics_id and obj.get("script") == script for obj in objects):
            errors.append(f"Vermilion missing object {graphics_id} with script {script}")

    return errors


def validate_ss_anne() -> list[str]:
    errors: list[str] = []
    scripts = read(ENGINE / "data" / "maps" / "SSAnne_2F_Corridor_Frlg" / "scripts.inc")
    ssanne = load_map("SSAnne_2F_Corridor_Frlg")
    captain = read(ENGINE / "data" / "maps" / "SSAnne_CaptainsOffice_Frlg" / "scripts.inc")

    for marker in (
        "SSAnne_2F_Corridor_EventScript_ManifestCrisis",
        "BELL TOWER COURIER",
        "ROCKET: The routes belong to us",
        "GOLD DUST: You break what you touch",
        "trainerbattle_two_trainers TRAINER_TEAM_ROCKET_GRUNT_SS_ANNE_MANIFEST",
        "TRAINER_GOLD_DUST_BROKER_MIDAS",
        "RED get you on the list",
        "manifest panic",
    ):
        if marker not in scripts:
            errors.append(f"S.S. Anne 2F scripts missing marker: {marker}")

    required_objects = {
        "OBJ_EVENT_GFX_ROCKET_M": "SSAnne_2F_Corridor_EventScript_ManifestCrisis",
        "OBJ_EVENT_GFX_GENTLEMAN": "SSAnne_2F_Corridor_EventScript_ManifestCrisis",
    }
    objects = ssanne.get("object_events", [])
    for graphics_id, script in required_objects.items():
        if not any(obj.get("graphics_id") == graphics_id and obj.get("script") == script for obj in objects):
            errors.append(f"S.S. Anne missing object {graphics_id} with script {script}")

    for marker in (
        "manifest flashed gold",
        "compass pointed toward JOHTO",
        "ROCKET and GOLD DUST both chased",
        "TRAIL",
        "CUTTER upgrade",
        "JOHTO reading is locked",
    ):
        if marker not in captain:
            errors.append(f"Captain text missing marker: {marker}")

    return errors


def validate_trainers() -> list[str]:
    errors: list[str] = []
    trainers = read(ENGINE / "src" / "data" / "trainers_frlg.party")
    opponents = read(ENGINE / "include" / "constants" / "opponents_frlg.h")

    for marker in (
        "#define TRAINER_TEAM_ROCKET_GRUNT_SS_ANNE_MANIFEST 626",
        "#define TRAINER_GOLD_DUST_BROKER_MIDAS             627",
    ):
        if marker not in opponents:
            errors.append(f"Opponent constants missing marker: {marker}")
    count_match = re.search(r"#define TRAINERS_COUNT_FRLG\s+(\d+)", opponents)
    if not count_match:
        errors.append("Opponent constants missing TRAINERS_COUNT_FRLG")
    elif int(count_match.group(1)) < 628:
        errors.append(f"TRAINERS_COUNT_FRLG must be at least 628, got {count_match.group(1)}")

    for marker in (
        "=== TRAINER_TEAM_ROCKET_GRUNT_SS_ANNE_MANIFEST ===",
        "Ekans\nLevel: 22",
        "Koffing\nLevel: 22",
        "=== TRAINER_GOLD_DUST_BROKER_MIDAS ===",
        "Name: MIDAS",
        "Meowth\nLevel: 22",
        "Sandshrew\nLevel: 22",
    ):
        if marker not in trainers:
            errors.append(f"Trainer data missing marker: {marker}")

    return errors


def validate_design_data() -> list[str]:
    errors: list[str] = []
    companions = yaml.safe_load(read(COMPANIONS))
    kanto = yaml.safe_load(read(KANTO))
    worldlink = yaml.safe_load(read(WORLDLINK)).get("worldlink_region_progression", {})

    misty = companions.get("companions", {}).get("misty", {})
    kanto_presence = misty.get("regional_presence", {}).get("kanto", [])
    if "post_ss_anne_join" not in kanto_presence:
        errors.append("Misty companion data must include post_ss_anne_join")
    if "after the S.S. Anne crisis" not in "\n".join(companions.get("global_rules", [])):
        errors.append("Companion global rules must preserve Misty's post-S.S. Anne joining timing")

    act3 = next((act for act in kanto.get("acts", []) if act.get("id") == "act_3_cerulean_to_vermilion"), {})
    events = act3.get("required_events", [])
    for event_id in (
        "blue_vermilion_jealousy_scene",
        "ss_anne_rocket_gold_dust_johto_manifest_crisis",
        "vermilion_harbor_johto_locked_hint",
        "misty_post_ss_anne_join_scene",
    ):
        if event_id not in events:
            errors.append(f"Kanto act 3 missing required event: {event_id}")

    preview = worldlink.get("first_locked_preview", {})
    if preview.get("region") != "johto":
        errors.append("WorldLink first locked preview must be Johto")
    if preview.get("location") != "vermilion_harbor":
        errors.append("WorldLink first locked preview must happen at Vermilion Harbor")
    if "not travel unlocks" not in worldlink.get("locked_preview_rule", ""):
        errors.append("WorldLink locked preview rule must reject early travel unlocks")
    if "Johto remains locked" not in worldlink.get("locked_preview_rule", ""):
        errors.append("WorldLink locked preview rule must keep Johto locked")

    return errors


def main() -> int:
    errors: list[str] = []
    errors.extend(validate_patch_and_spec())
    errors.extend(validate_vermilion())
    errors.extend(validate_ss_anne())
    errors.extend(validate_trainers())
    errors.extend(validate_design_data())

    if errors:
        print("Vermilion S.S. Anne crisis validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Vermilion S.S. Anne crisis validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
