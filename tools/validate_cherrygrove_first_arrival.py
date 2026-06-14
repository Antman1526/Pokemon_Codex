#!/usr/bin/env python3
"""Validate the first playable Cherrygrove City slice."""

from __future__ import annotations

from pathlib import Path

try:
    import yaml
except ImportError as exc:
    raise SystemExit("PyYAML is required: python3 -m pip install PyYAML") from exc


ROOT = Path(__file__).resolve().parents[1]
ENGINE = ROOT / "engine" / "pokeemerald-expansion"
PATCH = ROOT / "patches" / "engine" / "0044-cherrygrove-first-arrival.patch"
SPEC = ROOT / "docs" / "superpowers" / "specs" / "2026-06-14-cherrygrove-first-arrival-design.md"
PLAN = ROOT / "docs" / "superpowers" / "plans" / "2026-06-14-cherrygrove-first-arrival.md"
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
        errors.append("missing patch file: 0044-cherrygrove-first-arrival.patch")
    elif PATCH.stat().st_size == 0:
        errors.append("empty patch file: 0044-cherrygrove-first-arrival.patch")
    else:
        patch = read(PATCH)
        for marker in (
            "MAP_CHERRYGROVE_CITY",
            "CherrygroveCity_Frlg",
            "FLAG_CHERRYGROVE_FIRST_ARRIVAL_REACHED",
            "CherrygroveCity_Frlg_Text_GuideWatchNetwork",
            "CherrygroveCity_Frlg_Text_SilverWarning",
            "Map Card",
            "Apricorn Case",
            "Gold Dust",
            "Route 30 next",
        ):
            if marker not in patch:
                errors.append(f"patch 0044 missing marker: {marker}")

    for doc_path, doc_name, markers in (
        (
            SPEC,
            "Cherrygrove first arrival spec",
            ("friendly guide with surveillance tension", "Map Card", "Silver warning"),
        ),
        (
            PLAN,
            "Cherrygrove first arrival plan",
            ("Add failing validator", "Add Cherrygrove map", "Build the ROM"),
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
    route29_map = read(ENGINE / "data" / "maps" / "Route29_Frlg" / "map.json")
    city_map_path = ENGINE / "data" / "maps" / "CherrygroveCity_Frlg" / "map.json"
    city_scripts_path = ENGINE / "data" / "maps" / "CherrygroveCity_Frlg" / "scripts.inc"

    if "#define FLAG_CHERRYGROVE_FIRST_ARRIVAL_REACHED   0x027" not in flags:
        errors.append("flags_frlg.h missing FLAG_CHERRYGROVE_FIRST_ARRIVAL_REACHED at 0x027")
    if '"CherrygroveCity_Frlg"' not in map_groups:
        errors.append("map_groups.json missing CherrygroveCity_Frlg")
    if '"map": "MAP_CHERRYGROVE_CITY"' not in route29_map:
        errors.append("Route 29 map missing connection to MAP_CHERRYGROVE_CITY")

    if not city_map_path.exists():
        errors.append("missing CherrygroveCity_Frlg map.json")
    else:
        city_map = read(city_map_path)
        for marker in (
            '"id": "MAP_CHERRYGROVE_CITY"',
            '"region": "REGION_JOHTO"',
            '"layout": "LAYOUT_VIRIDIAN_CITY"',
            '"map": "MAP_ROUTE29"',
            "CherrygroveCity_Frlg_EventScript_RedCheckIn",
            "CherrygroveCity_Frlg_EventScript_LyraCheckpoint",
            "CherrygroveCity_Frlg_EventScript_GuideWatchNetwork",
            "CherrygroveCity_Frlg_EventScript_SilverWarning",
            "CherrygroveCity_Frlg_EventScript_GoldDustReceipt",
        ):
            if marker not in city_map:
                errors.append(f"Cherrygrove map.json missing marker: {marker}")

    if not city_scripts_path.exists():
        errors.append("missing CherrygroveCity_Frlg scripts.inc")
    else:
        scripts = read(city_scripts_path)
        for marker in (
            "CherrygroveCity_Frlg_MapScripts",
            "FLAG_CHERRYGROVE_FIRST_ARRIVAL_REACHED",
            "RED: Cherrygrove feels quiet",
            "LYRA: This is where Johto starts",
            "watching back",
            "Map Card",
            "Apricorn Case",
            "guide network",
            "SILVER: You keep following the map",
            "Gold Dust",
            "WorldLink: Route 30 next",
            "No Hoenn route registered",
        ):
            if marker not in scripts:
                errors.append(f"Cherrygrove scripts missing marker: {marker}")

    return errors


def validate_design_data() -> list[str]:
    errors: list[str] = []
    johto = load_yaml(JOHTO_CHAPTER)
    messages = load_yaml(JOHTO_WORLDLINK)
    regions = load_yaml(REGION_PROGRESSION)
    rivals = load_yaml(RIVAL_PROGRESSION)

    act1 = next((act for act in johto.get("acts", []) if act.get("id") == "act_1_new_bark_to_violet"), {})
    for event_id in (
        "cherrygrove_first_arrival",
        "cherrygrove_map_card_reward",
        "cherrygrove_apricorn_case_tease",
        "guide_worldlink_watch_network",
        "red_cherrygrove_check_in",
        "lyra_cherrygrove_checkpoint",
        "silver_cherrygrove_first_warning",
        "gold_dust_old_tower_receipt",
    ):
        if event_id not in act1.get("required_events", []):
            errors.append(f"Johto act 1 missing Cherrygrove event: {event_id}")
    for unlock_id in (
        "cherrygrove_live_map",
        "johto_map_card",
        "apricorn_case_tease",
        "guide_watch_network",
        "route_30_story_gate",
    ):
        if unlock_id not in act1.get("unlocks", []):
            errors.append(f"Johto act 1 missing Cherrygrove unlock: {unlock_id}")

    message_ids = {message.get("id") for message in messages.get("messages", [])}
    for message_id in (
        "WL_JOHTO_CHERRYGROVE_ARRIVAL",
        "WL_JOHTO_GUIDE_WATCH_NETWORK",
        "WL_JOHTO_SILVER_CHERRYGROVE_WARNING",
        "WL_JOHTO_ROUTE30_NEXT",
    ):
        if message_id not in message_ids:
            errors.append(f"Johto WorldLink missing id: {message_id}")

    transition = regions.get("worldlink_region_progression", {}).get("current_transition_state", {})
    if transition.get("current_safe_hub") not in {"cherrygrove_city", "mr_pokemon_house", "violet_city", "sprout_tower_1f", "sprout_tower_upper", "violet_gym", "route_32", "union_cave", "azalea_town", "slowpoke_well", "azalea_gym", "bugsy_gym"}:
        errors.append("current transition state must record Cherrygrove as current safe hub")
    if transition.get("next_required_story_node") not in {"route_30_first_steps", "mr_pokemon_house_first_visit", "violet_city_first_arrival", "sprout_tower_first_floor", "sprout_tower_upper_floor", "falkner_gym_battle", "route_32_union_cave_road", "union_cave_first_entry", "azalea_first_arrival", "slowpoke_well_first_entry", "bugsy_gym_challenge", "ilex_forest_first_entry"}:
        errors.append("current transition state must advance next node to Route 30 or later")
    if transition.get("hard_lock_next_region") != "hoenn":
        errors.append("Hoenn must remain the hard-locked next region")

    band = rivals.get("progression_bands", {}).get("johto_cherrygrove_first_arrival", {})
    if band.get("companions", {}).get("red", {}).get("event") != "quiet_town_check_in":
        errors.append("Rival progression must keep Red as a quiet Cherrygrove check-in")
    if band.get("rivals", {}).get("silver", {}).get("event") != "first_warning_no_battle":
        errors.append("Rival progression must set Silver as first warning with no battle")

    return errors


def validate_build_notes() -> list[str]:
    if not BUILD_NOTES.exists():
        return ["missing build notes file"]
    notes = read(BUILD_NOTES)
    errors: list[str] = []
    for marker in (
        "0044-cherrygrove-first-arrival.patch",
        "validate_cherrygrove_first_arrival.py",
        "Cherrygrove first arrival",
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
        print("Cherrygrove first arrival validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Cherrygrove first arrival validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
