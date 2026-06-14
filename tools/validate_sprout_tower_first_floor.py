#!/usr/bin/env python3
"""Validate the first playable Sprout Tower 1F slice."""

from __future__ import annotations

from pathlib import Path

try:
    import yaml
except ImportError as exc:
    raise SystemExit("PyYAML is required: python3 -m pip install PyYAML") from exc


ROOT = Path(__file__).resolve().parents[1]
ENGINE = ROOT / "engine" / "pokeemerald-expansion"
PATCH = ROOT / "patches" / "engine" / "0048-sprout-tower-first-floor.patch"
SPEC = ROOT / "docs" / "superpowers" / "specs" / "2026-06-14-sprout-tower-first-floor-design.md"
PLAN = ROOT / "docs" / "superpowers" / "plans" / "2026-06-14-sprout-tower-first-floor.md"
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
        errors.append("missing patch file: 0048-sprout-tower-first-floor.patch")
    elif PATCH.stat().st_size == 0:
        errors.append("empty patch file: 0048-sprout-tower-first-floor.patch")
    else:
        patch = read(PATCH)
        for marker in (
            "MAP_SPROUT_TOWER_1F",
            "SproutTower_1F_Frlg",
            "FLAG_SPROUT_TOWER_FIRST_FLOOR_REACHED",
            "SproutTower_1F_Frlg_Text_SilverFirstFloor",
            "SproutTower_1F_Frlg_Text_MoonlightBellInk",
            "SproutTower_1F_Frlg_Text_GoldDustArchivePressure",
            "SproutTower_1F_Frlg_Text_ElderUpperFloor",
            "Red stays outside",
        ):
            if marker not in patch:
                errors.append(f"patch 0048 missing marker: {marker}")

    for doc_path, doc_name, markers in (
        (
            SPEC,
            "Sprout Tower 1F spec",
            ("Red stays outside", "Silver first-floor confrontation", "Moonlight is the main threat"),
        ),
        (
            PLAN,
            "Sprout Tower 1F plan",
            ("Add failing validator", "Add Sprout Tower 1F map", "Build the ROM"),
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
    violet_map = read(ENGINE / "data" / "maps" / "VioletCity_Frlg" / "map.json")
    tower_map_path = ENGINE / "data" / "maps" / "SproutTower_1F_Frlg" / "map.json"
    tower_scripts_path = ENGINE / "data" / "maps" / "SproutTower_1F_Frlg" / "scripts.inc"

    if "#define FLAG_SPROUT_TOWER_FIRST_FLOOR_REACHED   0x0B2" not in flags:
        errors.append("flags_frlg.h missing FLAG_SPROUT_TOWER_FIRST_FLOOR_REACHED at 0x0B2")
    if '"SproutTower_1F_Frlg"' not in map_groups:
        errors.append("map_groups.json missing SproutTower_1F_Frlg")
    if '"dest_map": "MAP_SPROUT_TOWER_1F"' not in violet_map:
        errors.append("Violet City map missing warp to MAP_SPROUT_TOWER_1F")

    if not tower_map_path.exists():
        errors.append("missing SproutTower_1F_Frlg map.json")
    else:
        tower_map = read(tower_map_path)
        for marker in (
            '"id": "MAP_SPROUT_TOWER_1F"',
            '"region": "REGION_JOHTO"',
            '"layout": "LAYOUT_POKEMON_TOWER_2F"',
            '"dest_map": "MAP_VIOLET_CITY"',
            "SproutTower_1F_Frlg_EventScript_SilverFirstFloor",
            "SproutTower_1F_Frlg_EventScript_MoonlightBellInk",
            "SproutTower_1F_Frlg_EventScript_GoldDustArchivePressure",
            "SproutTower_1F_Frlg_EventScript_ElderUpperFloor",
            "SproutTower_1F_Frlg_EventScript_RedStaysOutsideNote",
        ):
            if marker not in tower_map:
                errors.append(f"Sprout Tower map.json missing marker: {marker}")

    if not tower_scripts_path.exists():
        errors.append("missing SproutTower_1F_Frlg scripts.inc")
    else:
        scripts = read(tower_scripts_path)
        for marker in (
            "SproutTower_1F_Frlg_MapScripts",
            "FLAG_SPROUT_TOWER_FIRST_FLOOR_REACHED",
            "SILVER: Not here",
            "MOONLIGHT PILGRIM: The bells are written over",
            "GOLD DUST BUYER: Archives are cleaner",
            "ELDER: Climb higher",
            "RED: I am staying outside",
            "WorldLink: Sprout Tower upper floor next",
            "Hoenn remains locked",
        ):
            if marker not in scripts:
                errors.append(f"Sprout Tower scripts missing marker: {marker}")
    return errors


def validate_design_data() -> list[str]:
    errors: list[str] = []
    johto = load_yaml(JOHTO_CHAPTER)
    messages = load_yaml(JOHTO_WORLDLINK)
    regions = load_yaml(REGION_PROGRESSION)
    rivals = load_yaml(RIVAL_PROGRESSION)

    act1 = next((act for act in johto.get("acts", []) if act.get("id") == "act_1_new_bark_to_violet"), {})
    for event_id in (
        "sprout_tower_first_floor",
        "red_stays_outside_sprout_tower",
        "silver_first_floor_confrontation_no_battle",
        "moonlight_bell_ink_reveal",
        "gold_dust_archive_pressure",
        "elder_points_to_upper_floor",
    ):
        if event_id not in act1.get("required_events", []):
            errors.append(f"Johto act 1 missing Sprout Tower event: {event_id}")
    for unlock_id in (
        "sprout_tower_1f_live_map",
        "sprout_tower_upper_floor_gate",
        "silver_battle_upper_floor_setup",
        "tower_record_checklist",
    ):
        if unlock_id not in act1.get("unlocks", []):
            errors.append(f"Johto act 1 missing Sprout Tower unlock: {unlock_id}")

    message_ids = {message.get("id") for message in messages.get("messages", [])}
    for message_id in (
        "WL_JOHTO_SPROUT_TOWER_1F_ARRIVAL",
        "WL_JOHTO_RED_STAYS_OUTSIDE",
        "WL_JOHTO_SILVER_UPPER_FLOOR_SETUP",
        "WL_JOHTO_MOONLIGHT_MAIN_THREAT",
    ):
        if message_id not in message_ids:
            errors.append(f"Johto WorldLink missing id: {message_id}")

    transition = regions.get("worldlink_region_progression", {}).get("current_transition_state", {})
    if transition.get("current_safe_hub") not in {"sprout_tower_1f", "sprout_tower_upper", "violet_gym", "route_32"}:
        errors.append("current transition state must record Sprout Tower 1F as current safe hub")
    if transition.get("next_required_story_node") not in {"sprout_tower_upper_floor", "falkner_gym_battle", "route_32_union_cave_road", "union_cave_first_entry"}:
        errors.append("current transition state must advance next node to sprout_tower_upper_floor")
    if transition.get("hard_lock_next_region") != "hoenn":
        errors.append("Hoenn must remain the hard-locked next region")

    band = rivals.get("progression_bands", {}).get("johto_sprout_tower_first_floor", {})
    if band.get("companions", {}).get("red", {}).get("event") != "stays_outside_sprout_tower":
        errors.append("Rival progression must set Red as staying outside Sprout Tower")
    if band.get("rivals", {}).get("silver", {}).get("event") != "first_floor_confrontation_no_battle":
        errors.append("Rival progression must set Silver as first-floor no-battle confrontation")
    return errors


def validate_build_notes() -> list[str]:
    if not BUILD_NOTES.exists():
        return ["missing build notes file"]
    notes = read(BUILD_NOTES)
    errors: list[str] = []
    for marker in (
        "0048-sprout-tower-first-floor.patch",
        "validate_sprout_tower_first_floor.py",
        "Sprout Tower first floor",
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
        print("Sprout Tower first floor validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Sprout Tower first floor validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
