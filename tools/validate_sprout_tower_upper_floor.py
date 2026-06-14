#!/usr/bin/env python3
"""Validate the first playable Sprout Tower upper-floor slice."""

from __future__ import annotations

from pathlib import Path

try:
    import yaml
except ImportError as exc:
    raise SystemExit("PyYAML is required: python3 -m pip install PyYAML") from exc


ROOT = Path(__file__).resolve().parents[1]
ENGINE = ROOT / "engine" / "pokeemerald-expansion"
PATCH = ROOT / "patches" / "engine" / "0049-sprout-tower-upper-floor.patch"
SPEC = ROOT / "docs" / "superpowers" / "specs" / "2026-06-14-sprout-tower-upper-floor-design.md"
PLAN = ROOT / "docs" / "superpowers" / "plans" / "2026-06-14-sprout-tower-upper-floor.md"
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
        errors.append("missing patch file: 0049-sprout-tower-upper-floor.patch")
    elif PATCH.stat().st_size == 0:
        errors.append("empty patch file: 0049-sprout-tower-upper-floor.patch")
    else:
        patch = read(PATCH)
        for marker in (
            "MAP_SPROUT_TOWER_UPPER",
            "SproutTower_Upper_Frlg",
            "FLAG_SPROUT_TOWER_UPPER_FLOOR_REACHED",
            "SproutTower_Upper_Frlg_Text_ElderLesson",
            "SproutTower_Upper_Frlg_Text_SilverFirstBattle",
            "SproutTower_Upper_Frlg_Text_CursedBellRecord",
            "SproutTower_Upper_Frlg_Text_GoldDustReceipt",
            "SproutTower_Upper_Frlg_Text_FalknerGymUnlock",
            "FALKNER: Zephyr Gym unlocked",
        ):
            if marker not in patch:
                errors.append(f"patch 0049 missing marker: {marker}")

    for doc_path, doc_name, markers in (
        (
            SPEC,
            "Sprout Tower upper-floor spec",
            ("Elder lesson", "Silver first battle scene", "Falkner Gym unlocked"),
        ),
        (
            PLAN,
            "Sprout Tower upper-floor plan",
            ("Add failing validator", "Add Sprout Tower upper-floor map", "Build the ROM"),
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
    first_floor_map_path = ENGINE / "data" / "maps" / "SproutTower_1F_Frlg" / "map.json"
    upper_map_path = ENGINE / "data" / "maps" / "SproutTower_Upper_Frlg" / "map.json"
    upper_scripts_path = ENGINE / "data" / "maps" / "SproutTower_Upper_Frlg" / "scripts.inc"

    if "#define FLAG_SPROUT_TOWER_UPPER_FLOOR_REACHED   0x0B3" not in flags:
        errors.append("flags_frlg.h missing FLAG_SPROUT_TOWER_UPPER_FLOOR_REACHED at 0x0B3")
    if '"SproutTower_Upper_Frlg"' not in map_groups:
        errors.append("map_groups.json missing SproutTower_Upper_Frlg")
    if not first_floor_map_path.exists():
        errors.append("missing SproutTower_1F_Frlg map.json before upper-floor warp validation")
    elif '"dest_map": "MAP_SPROUT_TOWER_UPPER"' not in read(first_floor_map_path):
        errors.append("Sprout Tower 1F map missing warp to MAP_SPROUT_TOWER_UPPER")

    if not upper_map_path.exists():
        errors.append("missing SproutTower_Upper_Frlg map.json")
    else:
        upper_map = read(upper_map_path)
        for marker in (
            '"id": "MAP_SPROUT_TOWER_UPPER"',
            '"region": "REGION_JOHTO"',
            '"layout": "LAYOUT_POKEMON_TOWER_3F"',
            '"dest_map": "MAP_SPROUT_TOWER_1F"',
            "SproutTower_Upper_Frlg_EventScript_ElderLesson",
            "SproutTower_Upper_Frlg_EventScript_SilverFirstBattle",
            "SproutTower_Upper_Frlg_EventScript_CursedBellRecord",
            "SproutTower_Upper_Frlg_EventScript_GoldDustReceipt",
            "SproutTower_Upper_Frlg_EventScript_FalknerGymUnlock",
        ):
            if marker not in upper_map:
                errors.append(f"Sprout Tower upper map.json missing marker: {marker}")

    if not upper_scripts_path.exists():
        errors.append("missing SproutTower_Upper_Frlg scripts.inc")
    else:
        scripts = read(upper_scripts_path)
        for marker in (
            "SproutTower_Upper_Frlg_MapScripts",
            "FLAG_SPROUT_TOWER_UPPER_FLOOR_REACHED",
            "ELDER: Flexibility before force",
            "SILVER: Now we battle",
            "MOONLIGHT RECORD: Cursed bell record",
            "GOLD DUST RECEIPT: Archive purchase failed",
            "FALKNER: Zephyr Gym unlocked",
            "WorldLink: Falkner Gym next",
            "Hoenn remains locked",
        ):
            if marker not in scripts:
                errors.append(f"Sprout Tower upper scripts missing marker: {marker}")
    return errors


def validate_design_data() -> list[str]:
    errors: list[str] = []
    johto = load_yaml(JOHTO_CHAPTER)
    messages = load_yaml(JOHTO_WORLDLINK)
    regions = load_yaml(REGION_PROGRESSION)
    rivals = load_yaml(RIVAL_PROGRESSION)

    act1 = next((act for act in johto.get("acts", []) if act.get("id") == "act_1_new_bark_to_violet"), {})
    for event_id in (
        "sprout_tower_upper_floor",
        "elder_flexibility_lesson",
        "silver_first_battle_scene",
        "moonlight_cursed_bell_record",
        "gold_dust_archive_purchase_failed",
        "falkner_gym_unlocked",
    ):
        if event_id not in act1.get("required_events", []):
            errors.append(f"Johto act 1 missing Sprout Tower upper event: {event_id}")
    for unlock_id in (
        "sprout_tower_upper_floor_live_map",
        "cursed_bell_record_key_story",
        "zephyr_gym_story_gate_open",
        "field_checklist_page_tease",
    ):
        if unlock_id not in act1.get("unlocks", []):
            errors.append(f"Johto act 1 missing Sprout Tower upper unlock: {unlock_id}")

    message_ids = {message.get("id") for message in messages.get("messages", [])}
    for message_id in (
        "WL_JOHTO_SPROUT_TOWER_UPPER_ARRIVAL",
        "WL_JOHTO_SILVER_FIRST_BATTLE_SCENE",
        "WL_JOHTO_CURSED_BELL_RECORD",
        "WL_JOHTO_FALKNER_GYM_UNLOCKED",
    ):
        if message_id not in message_ids:
            errors.append(f"Johto WorldLink missing id: {message_id}")

    transition = regions.get("worldlink_region_progression", {}).get("current_transition_state", {})
    if transition.get("current_safe_hub") not in {"sprout_tower_upper", "violet_gym"}:
        errors.append("current transition state must record Sprout Tower upper floor as current safe hub")
    if transition.get("next_required_story_node") not in {"falkner_gym_battle", "route_32_union_cave_road"}:
        errors.append("current transition state must advance next node to falkner_gym_battle")
    if transition.get("hard_lock_next_region") != "hoenn":
        errors.append("Hoenn must remain the hard-locked next region")

    band = rivals.get("progression_bands", {}).get("johto_sprout_tower_upper_floor", {})
    if band.get("companions", {}).get("red", {}).get("event") != "trusts_antman_after_tower_test":
        errors.append("Rival progression must set Red as trusting Antman after the tower test")
    if band.get("rivals", {}).get("silver", {}).get("event") != "first_battle_scene_after_elder_lesson":
        errors.append("Rival progression must set Silver as first battle scene after Elder lesson")
    return errors


def validate_build_notes() -> list[str]:
    if not BUILD_NOTES.exists():
        return ["missing build notes file"]
    notes = read(BUILD_NOTES)
    errors: list[str] = []
    for marker in (
        "0049-sprout-tower-upper-floor.patch",
        "validate_sprout_tower_upper_floor.py",
        "Sprout Tower upper floor",
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
        print("Sprout Tower upper floor validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Sprout Tower upper floor validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
