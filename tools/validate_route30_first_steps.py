#!/usr/bin/env python3
"""Validate the first playable Route 30 slice."""

from __future__ import annotations

from pathlib import Path

try:
    import yaml
except ImportError as exc:
    raise SystemExit("PyYAML is required: python3 -m pip install PyYAML") from exc


ROOT = Path(__file__).resolve().parents[1]
ENGINE = ROOT / "engine" / "pokeemerald-expansion"
PATCH = ROOT / "patches" / "engine" / "0045-route30-first-steps.patch"
SPEC = ROOT / "docs" / "superpowers" / "specs" / "2026-06-14-route30-first-steps-design.md"
PLAN = ROOT / "docs" / "superpowers" / "plans" / "2026-06-14-route30-first-steps.md"
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
        errors.append("missing patch file: 0045-route30-first-steps.patch")
    elif PATCH.stat().st_size == 0:
        errors.append("empty patch file: 0045-route30-first-steps.patch")
    else:
        patch = read(PATCH)
        for marker in (
            "MAP_ROUTE30",
            "Route30_Frlg",
            "FLAG_ROUTE30_FIRST_STEPS_REACHED",
            "Route30_Frlg_Text_LyraRoadSupport",
            "Route30_Frlg_Text_RedWorldLinkCall",
            "Route30_Frlg_Text_GoldDustScout",
            "Route30_Frlg_Text_MoonlightPilgrim",
            "Mr. Pokemon",
        ):
            if marker not in patch:
                errors.append(f"patch 0045 missing marker: {marker}")

    for doc_path, doc_name, markers in (
        (
            SPEC,
            "Route 30 first steps spec",
            ("first trainer-road pressure test", "Silver battle waits", "Mr. Pokemon"),
        ),
        (
            PLAN,
            "Route 30 first steps plan",
            ("Add failing validator", "Add Route 30 map", "Build the ROM"),
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
    cherrygrove_map = read(ENGINE / "data" / "maps" / "CherrygroveCity_Frlg" / "map.json")
    route_map_path = ENGINE / "data" / "maps" / "Route30_Frlg" / "map.json"
    route_scripts_path = ENGINE / "data" / "maps" / "Route30_Frlg" / "scripts.inc"

    if "#define FLAG_ROUTE30_FIRST_STEPS_REACHED   0x0AF" not in flags:
        errors.append("flags_frlg.h missing FLAG_ROUTE30_FIRST_STEPS_REACHED at 0x0AF")
    if '"Route30_Frlg"' not in map_groups:
        errors.append("map_groups.json missing Route30_Frlg")
    if '"map": "MAP_ROUTE30"' not in cherrygrove_map:
        errors.append("Cherrygrove map missing connection to MAP_ROUTE30")

    if not route_map_path.exists():
        errors.append("missing Route30_Frlg map.json")
    else:
        route_map = read(route_map_path)
        for marker in (
            '"id": "MAP_ROUTE30"',
            '"region": "REGION_JOHTO"',
            '"layout": "LAYOUT_ROUTE3"',
            '"map": "MAP_CHERRYGROVE_CITY"',
            "Route30_Frlg_EventScript_LyraRoadSupport",
            "Route30_Frlg_EventScript_RedWorldLinkCall",
            "Route30_Frlg_EventScript_GoldDustScout",
            "Route30_Frlg_EventScript_MoonlightPilgrim",
            "Route30_Frlg_EventScript_MrPokemonObjective",
        ):
            if marker not in route_map:
                errors.append(f"Route 30 map.json missing marker: {marker}")

    if not route_scripts_path.exists():
        errors.append("missing Route30_Frlg scripts.inc")
    else:
        scripts = read(route_scripts_path)
        for marker in (
            "Route30_Frlg_MapScripts",
            "FLAG_ROUTE30_FIRST_STEPS_REACHED",
            "LYRA: This is Route 30",
            "RED: WorldLink check-in",
            "first trainer road",
            "Silver battle waits",
            "Gold Dust",
            "MOONLIGHT PILGRIM",
            "WorldLink: Mr. Pokemon next",
            "No Hoenn route registered",
        ):
            if marker not in scripts:
                errors.append(f"Route 30 scripts missing marker: {marker}")

    return errors


def validate_design_data() -> list[str]:
    errors: list[str] = []
    johto = load_yaml(JOHTO_CHAPTER)
    messages = load_yaml(JOHTO_WORLDLINK)
    regions = load_yaml(REGION_PROGRESSION)
    rivals = load_yaml(RIVAL_PROGRESSION)

    act1 = next((act for act in johto.get("acts", []) if act.get("id") == "act_1_new_bark_to_violet"), {})
    for event_id in (
        "route_30_first_steps",
        "lyra_route30_walk_support",
        "red_route30_worldlink_check_in",
        "route30_first_trainer_road_pressure",
        "mr_pokemon_house_objective",
        "gold_dust_route30_scouter",
        "moonlight_sprout_tower_whisper",
        "silver_battle_waits_until_sprout_tower",
    ):
        if event_id not in act1.get("required_events", []):
            errors.append(f"Johto act 1 missing Route 30 event: {event_id}")
    for unlock_id in (
        "route_30_live_map",
        "route30_trainer_road",
        "mr_pokemon_story_gate",
        "sprout_tower_shadow_tease",
    ):
        if unlock_id not in act1.get("unlocks", []):
            errors.append(f"Johto act 1 missing Route 30 unlock: {unlock_id}")

    message_ids = {message.get("id") for message in messages.get("messages", [])}
    for message_id in (
        "WL_JOHTO_ROUTE30_FIRST_STEPS",
        "WL_JOHTO_ROUTE30_TRAINER_ROAD",
        "WL_JOHTO_MR_POKEMON_NEXT",
        "WL_JOHTO_SPROUT_TOWER_SHADOW",
    ):
        if message_id not in message_ids:
            errors.append(f"Johto WorldLink missing id: {message_id}")

    transition = regions.get("worldlink_region_progression", {}).get("current_transition_state", {})
    if transition.get("current_route") not in {"route_30", "route_32"}:
        errors.append("current transition state must record current_route route_30")
    if transition.get("next_required_story_node") not in {"mr_pokemon_house_first_visit", "violet_city_first_arrival", "sprout_tower_first_floor", "sprout_tower_upper_floor", "falkner_gym_battle", "route_32_union_cave_road", "union_cave_first_entry"}:
        errors.append("current transition state must advance next node to mr_pokemon_house_first_visit")
    if transition.get("hard_lock_next_region") != "hoenn":
        errors.append("Hoenn must remain the hard-locked next region")

    band = rivals.get("progression_bands", {}).get("johto_route30_first_steps", {})
    if band.get("companions", {}).get("lyra", {}).get("event") != "walks_first_trainer_road":
        errors.append("Rival progression must set Lyra as Route 30 walking support")
    if band.get("companions", {}).get("red", {}).get("event") != "worldlink_check_in_not_physical":
        errors.append("Rival progression must make Red a WorldLink check-in on Route 30")
    if band.get("rivals", {}).get("silver", {}).get("event") != "battle_waits_until_sprout_tower":
        errors.append("Rival progression must hold Silver battle until Sprout Tower")

    return errors


def validate_build_notes() -> list[str]:
    if not BUILD_NOTES.exists():
        return ["missing build notes file"]
    notes = read(BUILD_NOTES)
    errors: list[str] = []
    for marker in (
        "0045-route30-first-steps.patch",
        "validate_route30_first_steps.py",
        "Route 30 first steps",
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
        print("Route 30 first steps validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Route 30 first steps validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
