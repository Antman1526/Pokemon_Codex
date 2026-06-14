#!/usr/bin/env python3
"""Validate the Surge grid sabotage and WorldLink feed slice."""

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
PATCH = ROOT / "patches" / "engine" / "0015-surge-grid-worldlink.patch"
SPEC = ROOT / "docs" / "superpowers" / "specs" / "2026-06-14-surge-grid-worldlink-design.md"
KANTO = ROOT / "data_design" / "kanto_chapter.yaml"
WORLDLINK_MESSAGES = ROOT / "data_design" / "kanto_worldlink_messages.yaml"
RIVAL_PROGRESSION = ROOT / "data_design" / "rival_progression_kanto.yaml"
BOSS_TEAMS = ROOT / "data_design" / "kanto_boss_teams.yaml"
BUILD_NOTES = ROOT / "build_notes" / "FIRST_PLAYABLE_OPENEMU_SMOKE_TEST.md"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def load_map(name: str) -> dict:
    return json.loads(read(ENGINE / "data" / "maps" / name / "map.json"))


def validate_patch_and_spec() -> list[str]:
    errors: list[str] = []
    if not PATCH.exists():
        errors.append("missing patch file: 0015-surge-grid-worldlink.patch")
    elif PATCH.stat().st_size == 0:
        errors.append("empty patch file: 0015-surge-grid-worldlink.patch")
    else:
        patch = read(PATCH)
        for marker in (
            "VermilionCity_Gym_EventScript_RocketGridSabotage",
            "TRAINER_TEAM_ROCKET_GRUNT_SURGE_GRID",
            "TRAIL CUTTER prototype",
            "WorldLink Rival Feed",
            "GOLD DUST collector",
            "Pikachu",
            "+Level: 22",
        ):
            if marker not in patch:
                errors.append(f"patch 0015 missing marker: {marker}")

    if not SPEC.exists():
        errors.append("missing Surge grid spec")
    else:
        spec = read(SPEC)
        for marker in ("Rocket power-grid sabotage", "Trail Cutter", "Lyra / Johto"):
            if marker not in spec:
                errors.append(f"spec missing marker: {marker}")
    return errors


def validate_gym() -> list[str]:
    errors: list[str] = []
    gym = load_map("VermilionCity_Gym_Frlg")
    scripts = read(ENGINE / "data" / "maps" / "VermilionCity_Gym_Frlg" / "scripts.inc")

    if not any(
        obj.get("graphics_id") == "OBJ_EVENT_GFX_ROCKET_M"
        and obj.get("script") == "VermilionCity_Gym_EventScript_RocketGridSabotage"
        for obj in gym.get("object_events", [])
    ):
        errors.append("Vermilion Gym missing Rocket grid sabotage object")

    for marker in (
        "VermilionCity_Gym_EventScript_RocketGridSabotage",
        "trainerbattle_single TRAINER_TEAM_ROCKET_GRUNT_SURGE_GRID",
        "S.S. ANNE manifest",
        "WorldLink Alert: VERMILION GYM",
        "TRAIL CUTTER prototype",
        "WorldLink Rival Feed",
        "BLUE cleared the S.S. ANNE route",
        "AVA logged JOHTO resonance",
        "DAX beat a SAILOR",
        "LYRA / JOHTO",
    ):
        if marker not in scripts:
            errors.append(f"Vermilion Gym scripts missing marker: {marker}")

    return errors


def validate_trainers() -> list[str]:
    errors: list[str] = []
    trainers = read(ENGINE / "src" / "data" / "trainers_frlg.party")
    opponents = read(ENGINE / "include" / "constants" / "opponents_frlg.h")

    for marker in (
        "#define TRAINER_TEAM_ROCKET_GRUNT_SURGE_GRID       628",
        "=== TRAINER_TEAM_ROCKET_GRUNT_SURGE_GRID ===",
        "Voltorb\nLevel: 23",
        "Magnemite\nLevel: 23",
        "Pikachu\nLevel: 22",
        "Raichu\nLevel: 24",
    ):
        source = opponents if marker.startswith("#define") else trainers
        if marker not in source:
            errors.append(f"Trainer/constants missing marker: {marker}")

    count_match = re.search(r"#define TRAINERS_COUNT_FRLG\s+(\d+)", opponents)
    if not count_match:
        errors.append("Opponent constants missing TRAINERS_COUNT_FRLG")
    elif int(count_match.group(1)) < 629:
        errors.append(f"TRAINERS_COUNT_FRLG must be at least 629, got {count_match.group(1)}")

    return errors


def validate_supporting_text() -> list[str]:
    errors: list[str] = []
    fan_club = read(ENGINE / "data" / "maps" / "VermilionCity_PokemonFanClub_Frlg" / "scripts.inc")
    vermilion = read(ENGINE / "data" / "maps" / "VermilionCity_Frlg" / "scripts.inc")

    fan_club_old = ("GOLD DUST collector", "CELADON buyer", "rare lineages")
    fan_club_refined = ("gold lapel pin", "blank auction card", "No name. Just a dust mark")
    if not all(marker in fan_club for marker in fan_club_old) and not all(
        marker in fan_club for marker in fan_club_refined
    ):
        errors.append("Fan Club text must contain either the original Gold Dust clue or the refined gold-lapel mystery clue")

    for marker in ("SURGE's Gym is pulsing", "Bring a GROUND answer"):
        if marker not in vermilion:
            errors.append(f"Vermilion harbor text missing marker: {marker}")
    if "SURGE's power is pulling" not in vermilion and "MISTY: Surge is not just a Gym" not in vermilion:
        errors.append("Vermilion harbor text missing Surge prep marker")

    return errors


def validate_design_data() -> list[str]:
    errors: list[str] = []
    kanto = yaml.safe_load(read(KANTO))
    messages = yaml.safe_load(read(WORLDLINK_MESSAGES))
    rivals = yaml.safe_load(read(RIVAL_PROGRESSION))
    bosses = yaml.safe_load(read(BOSS_TEAMS))

    act3 = next((act for act in kanto.get("acts", []) if act.get("id") == "act_3_cerulean_to_vermilion"), {})
    for event_id in (
        "surge_gym_power_grid_sabotage",
        "trail_cutter_prototype_registration",
        "post_surge_worldlink_rival_feed_batch",
        "fan_club_gold_dust_celadon_buyer_clue",
    ):
        if event_id not in act3.get("required_events", []):
            errors.append(f"Kanto act 3 missing event: {event_id}")

    message_ids = {message.get("id") for message in messages.get("messages", [])}
    for message_id in (
        "WL_KANTO_SURGE_GRID_WARNING",
        "WL_KANTO_POST_SURGE_RIVAL_BATCH",
        "WL_KANTO_TRAIL_CUTTER_PROTOTYPE",
    ):
        if message_id not in message_ids:
            errors.append(f"WorldLink messages missing id: {message_id}")

    vermilion = rivals.get("progression_bands", {}).get("vermilion_surge", {})
    if "lyra" not in vermilion.get("rivals", {}):
        errors.append("Rival progression must include locked Johto profile Lyra")

    surge_standard = bosses.get("kanto_bosses", {}).get("lt_surge", {}).get("standard", [])
    pikachu = next((mon for mon in surge_standard if mon.get("species") == "Pikachu"), {})
    if pikachu.get("level") != 22:
        errors.append("Design data must keep Surge Pikachu at level 22")

    return errors


def validate_build_notes() -> list[str]:
    if not BUILD_NOTES.exists():
        return ["missing build notes file"]
    notes = read(BUILD_NOTES)
    errors: list[str] = []
    for marker in (
        "0015-surge-grid-worldlink.patch",
        "validate_surge_grid_worldlink.py",
        "Rocket grid sabotage",
        "Trail Cutter prototype",
    ):
        if marker not in notes:
            errors.append(f"Build notes missing marker: {marker}")
    return errors


def main() -> int:
    errors: list[str] = []
    errors.extend(validate_patch_and_spec())
    errors.extend(validate_gym())
    errors.extend(validate_trainers())
    errors.extend(validate_supporting_text())
    errors.extend(validate_design_data())
    errors.extend(validate_build_notes())

    if errors:
        print("Surge grid WorldLink validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Surge grid WorldLink validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
