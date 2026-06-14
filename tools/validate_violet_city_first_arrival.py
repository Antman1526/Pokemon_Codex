#!/usr/bin/env python3
"""Validate the first playable Violet City arrival slice."""

from __future__ import annotations

from pathlib import Path

try:
    import yaml
except ImportError as exc:
    raise SystemExit("PyYAML is required: python3 -m pip install PyYAML") from exc


ROOT = Path(__file__).resolve().parents[1]
ENGINE = ROOT / "engine" / "pokeemerald-expansion"
PATCH = ROOT / "patches" / "engine" / "0047-violet-city-first-arrival.patch"
SPEC = ROOT / "docs" / "superpowers" / "specs" / "2026-06-14-violet-city-first-arrival-design.md"
PLAN = ROOT / "docs" / "superpowers" / "plans" / "2026-06-14-violet-city-first-arrival.md"
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
        errors.append("missing patch file: 0047-violet-city-first-arrival.patch")
    elif PATCH.stat().st_size == 0:
        errors.append("empty patch file: 0047-violet-city-first-arrival.patch")
    else:
        patch = read(PATCH)
        for marker in (
            "MAP_VIOLET_CITY",
            "VioletCity_Frlg",
            "FLAG_VIOLET_CITY_FIRST_ARRIVAL_REACHED",
            "VioletCity_Frlg_Text_RedVioletReturn",
            "VioletCity_Frlg_Text_LyraLocalGuide",
            "VioletCity_Frlg_Text_FalknerTowerGate",
            "VioletCity_Frlg_Text_SilverTowerWarning",
            "Sprout Tower before Falkner",
        ):
            if marker not in patch:
                errors.append(f"patch 0047 missing marker: {marker}")

    for doc_path, doc_name, markers in (
        (
            SPEC,
            "Violet City first arrival spec",
            ("Sprout Tower before Falkner", "Red physically returns", "Silver waits at the tower gate"),
        ),
        (
            PLAN,
            "Violet City first arrival plan",
            ("Add failing validator", "Add Violet City map", "Build the ROM"),
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
    route30_map = read(ENGINE / "data" / "maps" / "Route30_Frlg" / "map.json")
    violet_map_path = ENGINE / "data" / "maps" / "VioletCity_Frlg" / "map.json"
    violet_scripts_path = ENGINE / "data" / "maps" / "VioletCity_Frlg" / "scripts.inc"

    if "#define FLAG_VIOLET_CITY_FIRST_ARRIVAL_REACHED   0x0B1" not in flags:
        errors.append("flags_frlg.h missing FLAG_VIOLET_CITY_FIRST_ARRIVAL_REACHED at 0x0B1")
    if '"VioletCity_Frlg"' not in map_groups:
        errors.append("map_groups.json missing VioletCity_Frlg")
    if '"map": "MAP_VIOLET_CITY"' not in route30_map:
        errors.append("Route 30 map missing connection to MAP_VIOLET_CITY")

    if not violet_map_path.exists():
        errors.append("missing VioletCity_Frlg map.json")
    else:
        violet_map = read(violet_map_path)
        for marker in (
            '"id": "MAP_VIOLET_CITY"',
            '"region": "REGION_JOHTO"',
            '"layout": "LAYOUT_PEWTER_CITY"',
            '"map": "MAP_ROUTE30"',
            "VioletCity_Frlg_EventScript_RedVioletReturn",
            "VioletCity_Frlg_EventScript_LyraLocalGuide",
            "VioletCity_Frlg_EventScript_FalknerTowerGate",
            "VioletCity_Frlg_EventScript_SilverTowerWarning",
            "VioletCity_Frlg_EventScript_MoonlightBellRecord",
            "VioletCity_Frlg_EventScript_GoldDustArchiveBuyer",
        ):
            if marker not in violet_map:
                errors.append(f"Violet City map.json missing marker: {marker}")

    if not violet_scripts_path.exists():
        errors.append("missing VioletCity_Frlg scripts.inc")
    else:
        scripts = read(violet_scripts_path)
        for marker in (
            "VioletCity_Frlg_MapScripts",
            "FLAG_VIOLET_CITY_FIRST_ARRIVAL_REACHED",
            "RED: I caught up",
            "LYRA: Violet City",
            "FALKNER: Sprout Tower before Falkner",
            "SILVER: The tower first",
            "MOONLIGHT PILGRIM: Bell records",
            "GOLD DUST BUYER: Tower archives",
            "WorldLink: Sprout Tower next",
            "Hoenn remains locked",
        ):
            if marker not in scripts:
                errors.append(f"Violet City scripts missing marker: {marker}")

    return errors


def validate_design_data() -> list[str]:
    errors: list[str] = []
    johto = load_yaml(JOHTO_CHAPTER)
    messages = load_yaml(JOHTO_WORLDLINK)
    regions = load_yaml(REGION_PROGRESSION)
    rivals = load_yaml(RIVAL_PROGRESSION)

    act1 = next((act for act in johto.get("acts", []) if act.get("id") == "act_1_new_bark_to_violet"), {})
    for event_id in (
        "violet_city_first_arrival",
        "red_violet_city_return",
        "lyra_violet_city_local_guide",
        "falkner_requires_sprout_tower",
        "silver_sprout_tower_gate_warning",
        "moonlight_bell_record_pressure",
        "gold_dust_tower_archive_buyer",
    ):
        if event_id not in act1.get("required_events", []):
            errors.append(f"Johto act 1 missing Violet event: {event_id}")
    for unlock_id in (
        "violet_city_live_map",
        "sprout_tower_story_gate",
        "zephyr_gym_locked_until_tower",
        "violet_rematch_board_tease",
    ):
        if unlock_id not in act1.get("unlocks", []):
            errors.append(f"Johto act 1 missing Violet unlock: {unlock_id}")

    message_ids = {message.get("id") for message in messages.get("messages", [])}
    for message_id in (
        "WL_JOHTO_VIOLET_CITY_ARRIVAL",
        "WL_JOHTO_SPROUT_TOWER_REQUIRED",
        "WL_JOHTO_RED_LYRA_VIOLET_SUPPORT",
        "WL_JOHTO_SILVER_TOWER_GATE",
    ):
        if message_id not in message_ids:
            errors.append(f"Johto WorldLink missing id: {message_id}")

    transition = regions.get("worldlink_region_progression", {}).get("current_transition_state", {})
    if transition.get("current_safe_hub") not in {"violet_city", "sprout_tower_1f", "sprout_tower_upper", "violet_gym", "route_32", "union_cave", "azalea_town", "slowpoke_well", "azalea_gym", "bugsy_gym"}:
        errors.append("current transition state must record Violet City as current safe hub")
    if transition.get("next_required_story_node") not in {"sprout_tower_first_floor", "sprout_tower_upper_floor", "falkner_gym_battle", "route_32_union_cave_road", "union_cave_first_entry", "azalea_first_arrival", "slowpoke_well_first_entry", "bugsy_gym_challenge", "ilex_forest_first_entry"}:
        errors.append("current transition state must advance next node to sprout_tower_first_floor")
    if transition.get("hard_lock_next_region") != "hoenn":
        errors.append("Hoenn must remain the hard-locked next region")

    band = rivals.get("progression_bands", {}).get("johto_violet_city_first_arrival", {})
    if band.get("companions", {}).get("red", {}).get("event") != "physically_returns_in_violet":
        errors.append("Rival progression must set Red as physically returning in Violet")
    if band.get("rivals", {}).get("silver", {}).get("event") != "sprout_tower_gate_warning":
        errors.append("Rival progression must set Silver as Sprout Tower gate warning")

    return errors


def validate_build_notes() -> list[str]:
    if not BUILD_NOTES.exists():
        return ["missing build notes file"]
    notes = read(BUILD_NOTES)
    errors: list[str] = []
    for marker in (
        "0047-violet-city-first-arrival.patch",
        "validate_violet_city_first_arrival.py",
        "Violet City first arrival",
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
        print("Violet City first arrival validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Violet City first arrival validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
