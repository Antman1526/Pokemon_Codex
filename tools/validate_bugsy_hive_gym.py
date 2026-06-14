#!/usr/bin/env python3
"""Validate the first playable Bugsy Hive Gym slice."""

from __future__ import annotations

from pathlib import Path

try:
    import yaml
except ImportError as exc:
    raise SystemExit("PyYAML is required: python3 -m pip install PyYAML") from exc


ROOT = Path(__file__).resolve().parents[1]
ENGINE = ROOT / "engine" / "pokeemerald-expansion"
PATCH = ROOT / "patches" / "engine" / "0055-bugsy-hive-gym.patch"
SPEC = ROOT / "docs" / "superpowers" / "specs" / "2026-06-14-bugsy-hive-gym-design.md"
PLAN = ROOT / "docs" / "superpowers" / "plans" / "2026-06-14-bugsy-hive-gym.md"
JOHTO_CHAPTER = ROOT / "data_design" / "johto_chapter.yaml"
JOHTO_WORLDLINK = ROOT / "data_design" / "johto_worldlink_messages.yaml"
REGION_PROGRESSION = ROOT / "data_design" / "worldlink_region_progression.yaml"
RIVAL_PROGRESSION = ROOT / "data_design" / "rival_progression_kanto.yaml"
BUILD_NOTES = ROOT / "build_notes" / "FIRST_PLAYABLE_OPENEMU_SMOKE_TEST.md"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def load_yaml(path: Path):
    return yaml.safe_load(read(path))


def validate_patch_docs() -> list[str]:
    errors: list[str] = []
    if not PATCH.exists():
        errors.append("missing patch file: 0055-bugsy-hive-gym.patch")
    elif PATCH.stat().st_size == 0:
        errors.append("empty patch file: 0055-bugsy-hive-gym.patch")
    else:
        patch = read(PATCH)
        for marker in (
            "MAP_AZALEA_GYM",
            "AzaleaTown_Gym_Frlg",
            "FLAG_BUGSY_GYM_REACHED",
            "FLAG_HIVE_BADGE_REGISTERED",
            "FLAG_APRICORN_FIRST_BATCH_RECEIVED",
            "AzaleaTown_Gym_Frlg_Text_BugsyBattleScene",
            "AzaleaTown_Gym_Frlg_Text_KurtApricornReward",
            "AzaleaTown_Gym_Frlg_Text_RedBoundary",
            "AzaleaTown_Gym_Frlg_Text_SilverIlexTrace",
            "WorldLink: Ilex Forest next",
        ):
            if marker not in patch:
                errors.append(f"patch 0055 missing marker: {marker}")

    for doc_path, doc_name, markers in (
        (
            SPEC,
            "Bugsy Hive Gym spec",
            ("Bugsy does not open with a normal gym lobby", "first-batch Apricorn reward", "ilex_forest_first_entry"),
        ),
        (
            PLAN,
            "Bugsy Hive Gym plan",
            ("Add a failing validator", "Add `MAP_AZALEA_GYM`", "Build the FireRed target ROM"),
        ),
    ):
        if not doc_path.exists():
            errors.append(f"missing {doc_name}")
            continue
        doc = read(doc_path)
        for marker in markers:
            if marker not in doc:
                errors.append(f"{doc_name} missing marker: {marker}")
    return errors


def validate_engine() -> list[str]:
    errors: list[str] = []
    flags = read(ENGINE / "include" / "constants" / "flags_frlg.h")
    map_groups = read(ENGINE / "data" / "maps" / "map_groups.json")
    azalea_map_path = ENGINE / "data" / "maps" / "AzaleaTown_Frlg" / "map.json"
    gym_map_path = ENGINE / "data" / "maps" / "AzaleaTown_Gym_Frlg" / "map.json"
    gym_scripts_path = ENGINE / "data" / "maps" / "AzaleaTown_Gym_Frlg" / "scripts.inc"

    for marker in (
        "#define FLAG_BUGSY_GYM_REACHED   0x0C1",
        "#define FLAG_HIVE_BADGE_REGISTERED   0x0C2",
        "#define FLAG_APRICORN_FIRST_BATCH_RECEIVED   0x0C3",
    ):
        if marker not in flags:
            errors.append(f"flags_frlg.h missing marker: {marker}")
    if '"AzaleaTown_Gym_Frlg"' not in map_groups:
        errors.append("map_groups.json missing AzaleaTown_Gym_Frlg")
    if not azalea_map_path.exists():
        errors.append("missing AzaleaTown_Frlg map.json before Bugsy Gym warp validation")
    elif '"dest_map": "MAP_AZALEA_GYM"' not in read(azalea_map_path):
        errors.append("Azalea map missing warp to MAP_AZALEA_GYM")

    if not gym_map_path.exists():
        errors.append("missing AzaleaTown_Gym_Frlg map.json")
    else:
        gym_map = read(gym_map_path)
        for marker in (
            '"id": "MAP_AZALEA_GYM"',
            '"region": "REGION_JOHTO"',
            '"layout": "LAYOUT_PEWTER_CITY_GYM"',
            '"dest_map": "MAP_AZALEA_TOWN"',
            "AzaleaTown_Gym_Frlg_EventScript_BugsyBattleScene",
            "AzaleaTown_Gym_Frlg_EventScript_KurtApricornReward",
            "AzaleaTown_Gym_Frlg_EventScript_RedBoundary",
            "AzaleaTown_Gym_Frlg_EventScript_SilverIlexTrace",
            "AzaleaTown_Gym_Frlg_EventScript_IlexNext",
        ):
            if marker not in gym_map:
                errors.append(f"Azalea Gym map.json missing marker: {marker}")

    if not gym_scripts_path.exists():
        errors.append("missing AzaleaTown_Gym_Frlg scripts.inc")
    else:
        scripts = read(gym_scripts_path)
        for marker in (
            "AzaleaTown_Gym_Frlg_MapScripts",
            "FLAG_BUGSY_GYM_REACHED",
            "FLAG_HIVE_BADGE_REGISTERED",
            "FLAG_APRICORN_FIRST_BATCH_RECEIVED",
            "KURT: First batch only",
            "RED: I am right here",
            "BUGSY: A swarm is not chaos",
            "HIVE BADGE registered",
            "SILVER TRACE: Ilex side",
            "WorldLink: Ilex Forest next",
            "Hoenn remains locked",
        ):
            if marker not in scripts:
                errors.append(f"Azalea Gym scripts missing marker: {marker}")
    return errors


def validate_design_data() -> list[str]:
    errors: list[str] = []
    johto = load_yaml(JOHTO_CHAPTER)
    messages = load_yaml(JOHTO_WORLDLINK)
    regions = load_yaml(REGION_PROGRESSION)
    rivals = load_yaml(RIVAL_PROGRESSION)

    act2 = next((act for act in johto.get("acts", []) if act.get("id") == "act_2_azalea_goldenrod"), {})
    for event_id in (
        "bugsy_swarm_lesson",
        "kurt_first_batch_apricorn_reward",
        "red_bugsy_boundary_scene",
        "bugsy_hive_badge_registered",
        "silver_ilex_no_battle_confrontation",
        "ilex_forest_next_objective",
    ):
        if event_id not in act2.get("required_events", []):
            errors.append(f"Johto act 2 missing Bugsy event: {event_id}")
    for unlock_id in (
        "bugsy_gym_live_map",
        "hive_badge_story_key",
        "apricorn_first_batch_reward",
        "johto_rematch_board_tier_1_live",
        "ilex_forest_story_gate",
    ):
        if unlock_id not in act2.get("unlocks", []):
            errors.append(f"Johto act 2 missing Bugsy unlock: {unlock_id}")

    message_ids = {message.get("id") for message in messages.get("messages", [])}
    for message_id in (
        "WL_JOHTO_BUGSY_GYM_ARRIVAL",
        "WL_JOHTO_APRICORN_FIRST_BATCH",
        "WL_JOHTO_HIVE_BADGE_REGISTERED",
        "WL_JOHTO_ILEX_FOREST_NEXT",
    ):
        if message_id not in message_ids:
            errors.append(f"Johto WorldLink missing id: {message_id}")

    transition = regions.get("worldlink_region_progression", {}).get("current_transition_state", {})
    if transition.get("current_safe_hub") not in {"azalea_gym", "ilex_forest"}:
        errors.append("current transition state must record Azalea Gym or Ilex Forest as current safe hub")
    if transition.get("current_route") not in {"bugsy_gym", "ilex_forest"}:
        errors.append("current transition state must keep current route as bugsy_gym or ilex_forest")
    if transition.get("next_required_story_node") not in {"ilex_forest_first_entry", "goldenrod_city_first_arrival"}:
        errors.append("current transition state must advance next node to ilex_forest_first_entry or goldenrod_city_first_arrival")
    if transition.get("hard_lock_next_region") != "hoenn":
        errors.append("Hoenn must remain the hard-locked next region")

    band = rivals.get("progression_bands", {}).get("johto_bugsy_hive_gym", {})
    if band.get("companions", {}).get("red", {}).get("event") != "bugsy_boundary_scene":
        errors.append("Rival progression must set Red as Bugsy boundary companion")
    if band.get("companions", {}).get("kurt", {}).get("event") != "first_batch_apricorn_reward":
        errors.append("Rival progression must set Kurt as first-batch Apricorn reward")
    if band.get("rivals", {}).get("silver", {}).get("event") != "ilex_no_battle_confrontation":
        errors.append("Rival progression must set Silver as Ilex no-battle confrontation")
    return errors


def validate_build_notes() -> list[str]:
    if not BUILD_NOTES.exists():
        return ["missing build notes file"]
    notes = read(BUILD_NOTES)
    errors: list[str] = []
    for marker in (
        "0055-bugsy-hive-gym.patch",
        "validate_bugsy_hive_gym.py",
        "Bugsy Hive Gym milestone",
    ):
        if marker not in notes:
            errors.append(f"Build notes missing marker: {marker}")
    return errors


def main() -> int:
    errors: list[str] = []
    errors.extend(validate_patch_docs())
    errors.extend(validate_engine())
    errors.extend(validate_design_data())
    errors.extend(validate_build_notes())

    if errors:
        print("Bugsy Hive Gym validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Bugsy Hive Gym validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
