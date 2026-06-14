#!/usr/bin/env python3
"""Validate the first playable Falkner / Zephyr Gym slice."""

from __future__ import annotations

from pathlib import Path

try:
    import yaml
except ImportError as exc:
    raise SystemExit("PyYAML is required: python3 -m pip install PyYAML") from exc


ROOT = Path(__file__).resolve().parents[1]
ENGINE = ROOT / "engine" / "pokeemerald-expansion"
PATCH = ROOT / "patches" / "engine" / "0050-falkner-zephyr-gym.patch"
SPEC = ROOT / "docs" / "superpowers" / "specs" / "2026-06-14-falkner-zephyr-gym-design.md"
PLAN = ROOT / "docs" / "superpowers" / "plans" / "2026-06-14-falkner-zephyr-gym.md"
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
        errors.append("missing patch file: 0050-falkner-zephyr-gym.patch")
    elif PATCH.stat().st_size == 0:
        errors.append("empty patch file: 0050-falkner-zephyr-gym.patch")
    else:
        patch = read(PATCH)
        for marker in (
            "MAP_VIOLET_CITY_GYM",
            "VioletCity_Gym_Frlg",
            "FLAG_FALKNER_GYM_REACHED",
            "FLAG_ZEPHYR_BADGE_REGISTERED",
            "VioletCity_Gym_Frlg_Text_RedAfterTower",
            "VioletCity_Gym_Frlg_Text_AvaBellAnalysis",
            "VioletCity_Gym_Frlg_Text_FalknerBattleScene",
            "VioletCity_Gym_Frlg_Text_FieldChecklist",
            "VioletCity_Gym_Frlg_Text_Route32Next",
            "ZEPHYR BADGE registered",
        ):
            if marker not in patch:
                errors.append(f"patch 0050 missing marker: {marker}")

    for doc_path, doc_name, markers in (
        (
            SPEC,
            "Falkner Zephyr Gym spec",
            ("Flying-type control lesson", "ZEPHYR BADGE registered", "Route 32 next"),
        ),
        (
            PLAN,
            "Falkner Zephyr Gym plan",
            ("Add failing validator", "Add Violet Gym map", "Build the ROM"),
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
    violet_map_path = ENGINE / "data" / "maps" / "VioletCity_Frlg" / "map.json"
    gym_map_path = ENGINE / "data" / "maps" / "VioletCity_Gym_Frlg" / "map.json"
    gym_scripts_path = ENGINE / "data" / "maps" / "VioletCity_Gym_Frlg" / "scripts.inc"

    if "#define FLAG_FALKNER_GYM_REACHED   0x0B4" not in flags:
        errors.append("flags_frlg.h missing FLAG_FALKNER_GYM_REACHED at 0x0B4")
    if "#define FLAG_ZEPHYR_BADGE_REGISTERED   0x0B5" not in flags:
        errors.append("flags_frlg.h missing FLAG_ZEPHYR_BADGE_REGISTERED at 0x0B5")
    if '"VioletCity_Gym_Frlg"' not in map_groups:
        errors.append("map_groups.json missing VioletCity_Gym_Frlg")
    if not violet_map_path.exists():
        errors.append("missing VioletCity_Frlg map.json before Gym warp validation")
    elif '"dest_map": "MAP_VIOLET_CITY_GYM"' not in read(violet_map_path):
        errors.append("Violet City map missing warp to MAP_VIOLET_CITY_GYM")

    if not gym_map_path.exists():
        errors.append("missing VioletCity_Gym_Frlg map.json")
    else:
        gym_map = read(gym_map_path)
        for marker in (
            '"id": "MAP_VIOLET_CITY_GYM"',
            '"region": "REGION_JOHTO"',
            '"layout": "LAYOUT_PEWTER_CITY_GYM"',
            '"dest_map": "MAP_VIOLET_CITY"',
            "VioletCity_Gym_Frlg_EventScript_RedAfterTower",
            "VioletCity_Gym_Frlg_EventScript_AvaBellAnalysis",
            "VioletCity_Gym_Frlg_EventScript_FalknerBattleScene",
            "VioletCity_Gym_Frlg_EventScript_FieldChecklist",
            "VioletCity_Gym_Frlg_EventScript_Route32Next",
        ):
            if marker not in gym_map:
                errors.append(f"Violet Gym map.json missing marker: {marker}")

    if not gym_scripts_path.exists():
        errors.append("missing VioletCity_Gym_Frlg scripts.inc")
    else:
        scripts = read(gym_scripts_path)
        for marker in (
            "VioletCity_Gym_Frlg_MapScripts",
            "FLAG_FALKNER_GYM_REACHED",
            "FLAG_ZEPHYR_BADGE_REGISTERED",
            "RED: You carried the tower",
            "AVA: Bell analysis complete",
            "FALKNER: Flying-type control lesson",
            "ZEPHYR BADGE registered",
            "Field Checklist page unlocked",
            "WorldLink: Route 32 next",
            "Hoenn remains locked",
        ):
            if marker not in scripts:
                errors.append(f"Violet Gym scripts missing marker: {marker}")
    return errors


def validate_design_data() -> list[str]:
    errors: list[str] = []
    johto = load_yaml(JOHTO_CHAPTER)
    messages = load_yaml(JOHTO_WORLDLINK)
    regions = load_yaml(REGION_PROGRESSION)
    rivals = load_yaml(RIVAL_PROGRESSION)

    act1 = next((act for act in johto.get("acts", []) if act.get("id") == "act_1_new_bark_to_violet"), {})
    for event_id in (
        "falkner_battle",
        "red_post_tower_reunion",
        "ava_cursed_bell_analysis",
        "zephyr_badge_registered",
        "field_checklist_page_unlocked",
        "silver_route32_silent_departure",
        "route32_unlocked",
    ):
        if event_id not in act1.get("required_events", []):
            errors.append(f"Johto act 1 missing Falkner event: {event_id}")
    for unlock_id in (
        "violet_gym_live_map",
        "zephyr_badge_story_key",
        "field_checklist_page_live",
        "route_32_story_gate",
        "azalea_arc_tease",
    ):
        if unlock_id not in act1.get("unlocks", []):
            errors.append(f"Johto act 1 missing Falkner unlock: {unlock_id}")

    message_ids = {message.get("id") for message in messages.get("messages", [])}
    for message_id in (
        "WL_JOHTO_FALKNER_GYM_ARRIVAL",
        "WL_JOHTO_ZEPHYR_BADGE_REGISTERED",
        "WL_JOHTO_FIELD_CHECKLIST_UNLOCKED",
        "WL_JOHTO_ROUTE32_NEXT",
    ):
        if message_id not in message_ids:
            errors.append(f"Johto WorldLink missing id: {message_id}")

    transition = regions.get("worldlink_region_progression", {}).get("current_transition_state", {})
    if transition.get("current_safe_hub") not in {"violet_gym", "route_32", "union_cave", "azalea_town", "slowpoke_well", "azalea_gym", "bugsy_gym", "ilex_forest"}:
        errors.append("current transition state must record Violet Gym as current safe hub")
    if transition.get("current_route") not in {"route_32", "union_cave", "azalea_town", "slowpoke_well", "azalea_gym", "bugsy_gym", "ilex_forest"}:
        errors.append("current transition state must point current route to route_32 or union_cave")
    if transition.get("next_required_story_node") not in {"route_32_union_cave_road", "union_cave_first_entry", "azalea_first_arrival", "slowpoke_well_first_entry", "bugsy_gym_challenge", "ilex_forest_first_entry", "goldenrod_city_first_arrival"}:
        errors.append("current transition state must advance next node to route_32_union_cave_road")
    if transition.get("hard_lock_next_region") != "hoenn":
        errors.append("Hoenn must remain the hard-locked next region")

    band = rivals.get("progression_bands", {}).get("johto_falkner_battle", {})
    if band.get("companions", {}).get("red", {}).get("event") != "post_tower_reunion_before_badge":
        errors.append("Rival progression must set Red as post-tower reunion before badge")
    if band.get("rivals", {}).get("silver", {}).get("event") != "silent_route32_departure":
        errors.append("Rival progression must set Silver as silently departing toward Route 32")
    return errors


def validate_build_notes() -> list[str]:
    if not BUILD_NOTES.exists():
        return ["missing build notes file"]
    notes = read(BUILD_NOTES)
    errors: list[str] = []
    for marker in (
        "0050-falkner-zephyr-gym.patch",
        "validate_falkner_zephyr_gym.py",
        "Falkner Zephyr Gym",
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
        print("Falkner Zephyr Gym validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Falkner Zephyr Gym validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
