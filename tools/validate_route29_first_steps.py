#!/usr/bin/env python3
"""Validate the first playable Route 29 slice."""

from __future__ import annotations

from pathlib import Path

try:
    import yaml
except ImportError as exc:
    raise SystemExit("PyYAML is required: python3 -m pip install PyYAML") from exc


ROOT = Path(__file__).resolve().parents[1]
ENGINE = ROOT / "engine" / "pokeemerald-expansion"
PATCH = ROOT / "patches" / "engine" / "0043-route29-first-steps.patch"
SPEC = ROOT / "docs" / "superpowers" / "specs" / "2026-06-14-route29-first-steps-design.md"
PLAN = ROOT / "docs" / "superpowers" / "plans" / "2026-06-14-route29-first-steps.md"
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
        errors.append("missing patch file: 0043-route29-first-steps.patch")
    elif PATCH.stat().st_size == 0:
        errors.append("empty patch file: 0043-route29-first-steps.patch")
    else:
        patch = read(PATCH)
        for marker in (
            "MAP_ROUTE29",
            "Route29_Frlg",
            "FLAG_ROUTE29_FIRST_STEPS_REACHED",
            "Route29_Frlg_Text_RedFieldSupport",
            "Route29_Frlg_Text_SilverShadow",
            "day and night",
            "Cherrygrove",
        ):
            if marker not in patch:
                errors.append(f"patch 0043 missing marker: {marker}")

    for doc_path, doc_name, markers in (
        (
            SPEC,
            "Route 29 first steps spec",
            ("calm road with hidden tension", "Red field support", "Silver shadow"),
        ),
        (
            PLAN,
            "Route 29 first steps plan",
            ("Add failing validator", "Add Route 29 map", "Build the ROM"),
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
    new_bark_map = read(ENGINE / "data" / "maps" / "NewBarkTown_Frlg" / "map.json")
    route_map_path = ENGINE / "data" / "maps" / "Route29_Frlg" / "map.json"
    route_scripts_path = ENGINE / "data" / "maps" / "Route29_Frlg" / "scripts.inc"

    if "#define FLAG_ROUTE29_FIRST_STEPS_REACHED   0x026" not in flags:
        errors.append("flags_frlg.h missing FLAG_ROUTE29_FIRST_STEPS_REACHED at 0x026")
    if '"Route29_Frlg"' not in map_groups:
        errors.append("map_groups.json missing Route29_Frlg")
    if '"map": "MAP_ROUTE29"' not in new_bark_map:
        errors.append("New Bark map missing connection to MAP_ROUTE29")

    if not route_map_path.exists():
        errors.append("missing Route29_Frlg map.json")
    else:
        route_map = read(route_map_path)
        for marker in (
            '"id": "MAP_ROUTE29"',
            '"region": "REGION_JOHTO"',
            '"layout": "LAYOUT_ROUTE1"',
            '"map": "MAP_NEW_BARK_TOWN"',
            "Route29_Frlg_EventScript_RedFieldSupport",
            "Route29_Frlg_EventScript_LyraCherrygroveHandoff",
            "Route29_Frlg_EventScript_SilverShadow",
            "Route29_Frlg_EventScript_DayNightSign",
        ):
            if marker not in route_map:
                errors.append(f"Route 29 map.json missing marker: {marker}")

    if not route_scripts_path.exists():
        errors.append("missing Route29_Frlg scripts.inc")
    else:
        scripts = read(route_scripts_path)
        for marker in (
            "Route29_Frlg_MapScripts",
            "FLAG_ROUTE29_FIRST_STEPS_REACHED",
            "RED: This is Johto's first real road",
            "day and night",
            "LYRA: Cherrygrove is close",
            "SILVER: ...",
            "WorldLink: Cherrygrove next",
            "No Hoenn route registered",
        ):
            if marker not in scripts:
                errors.append(f"Route 29 scripts missing marker: {marker}")

    return errors


def validate_design_data() -> list[str]:
    errors: list[str] = []
    johto = load_yaml(JOHTO_CHAPTER)
    messages = load_yaml(JOHTO_WORLDLINK)
    regions = load_yaml(REGION_PROGRESSION)
    rivals = load_yaml(RIVAL_PROGRESSION)

    act1 = next((act for act in johto.get("acts", []) if act.get("id") == "act_1_new_bark_to_violet"), {})
    for event_id in (
        "route_29_first_steps",
        "red_route29_field_support",
        "route29_day_night_encounter_tease",
        "silver_route29_shadow_sighting",
        "lyra_cherrygrove_handoff",
    ):
        if event_id not in act1.get("required_events", []):
            errors.append(f"Johto act 1 missing Route 29 event: {event_id}")
    for unlock_id in ("route_29_live_map", "route29_day_night_tracking", "cherrygrove_story_gate"):
        if unlock_id not in act1.get("unlocks", []):
            errors.append(f"Johto act 1 missing Route 29 unlock: {unlock_id}")

    message_ids = {message.get("id") for message in messages.get("messages", [])}
    for message_id in (
        "WL_JOHTO_ROUTE29_FIRST_STEPS",
        "WL_JOHTO_ROUTE29_DAY_NIGHT",
        "WL_JOHTO_CHERRYGROVE_NEXT",
    ):
        if message_id not in message_ids:
            errors.append(f"Johto WorldLink missing id: {message_id}")

    transition = regions.get("worldlink_region_progression", {}).get("current_transition_state", {})
    if transition.get("current_route") not in {"route_29", "route_30", "route_32", "union_cave"}:
        errors.append("current transition state must record Route 29 or a later Johto route")
    if transition.get("next_required_story_node") not in {"cherrygrove_first_arrival", "route_30_first_steps", "mr_pokemon_house_first_visit", "violet_city_first_arrival", "sprout_tower_first_floor", "sprout_tower_upper_floor", "falkner_gym_battle", "route_32_union_cave_road", "union_cave_first_entry", "azalea_first_arrival"}:
        errors.append("current transition state must advance next node to Cherrygrove or later")
    if transition.get("hard_lock_next_region") != "hoenn":
        errors.append("Hoenn must remain the hard-locked next region")

    band = rivals.get("progression_bands", {}).get("johto_route29_first_steps", {})
    if band.get("companions", {}).get("red", {}).get("event") != "field_support_without_battle_control":
        errors.append("Rival progression must set Red as field support without battle control")
    if band.get("rivals", {}).get("silver", {}).get("event") != "shadow_sighting_no_battle":
        errors.append("Rival progression must keep Silver as a shadow sighting with no battle")

    return errors


def validate_build_notes() -> list[str]:
    if not BUILD_NOTES.exists():
        return ["missing build notes file"]
    notes = read(BUILD_NOTES)
    errors: list[str] = []
    for marker in (
        "0043-route29-first-steps.patch",
        "validate_route29_first_steps.py",
        "Route 29 first steps",
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
        print("Route 29 first steps validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Route 29 first steps validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
