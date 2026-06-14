#!/usr/bin/env python3
"""Validate the first playable Route 32 / Union Cave road slice."""

from __future__ import annotations

from pathlib import Path

try:
    import yaml
except ImportError as exc:
    raise SystemExit("PyYAML is required: python3 -m pip install PyYAML") from exc


ROOT = Path(__file__).resolve().parents[1]
ENGINE = ROOT / "engine" / "pokeemerald-expansion"
PATCH = ROOT / "patches" / "engine" / "0051-route32-union-cave-road.patch"
SPEC = ROOT / "docs" / "superpowers" / "specs" / "2026-06-14-route32-union-cave-road-design.md"
PLAN = ROOT / "docs" / "superpowers" / "plans" / "2026-06-14-route32-union-cave-road.md"
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
        errors.append("missing patch file: 0051-route32-union-cave-road.patch")
    elif PATCH.stat().st_size == 0:
        errors.append("empty patch file: 0051-route32-union-cave-road.patch")
    else:
        patch = read(PATCH)
        for marker in (
            "MAP_ROUTE32",
            "Route32_Frlg",
            "FLAG_ROUTE32_FIRST_STEPS_REACHED",
            "FLAG_ROUTE32_FIELD_CHECKLIST_REVIEWED",
            "Route32_Frlg_Text_LyraRoadGuide",
            "Route32_Frlg_Text_RedVioletBackup",
            "Route32_Frlg_Text_FieldChecklist",
            "Route32_Frlg_Text_SilverTrace",
            "Route32_Frlg_Text_GoldDustToll",
            "Route32_Frlg_Text_RocketUnionCave",
            "Union Cave next",
        ):
            if marker not in patch:
                errors.append(f"patch 0051 missing marker: {marker}")

    for doc_path, doc_name, markers in (
        (
            SPEC,
            "Route 32 spec",
            ("Field Checklist becomes route-specific", "Gold Dust toll pressure", "Union Cave next"),
        ),
        (
            PLAN,
            "Route 32 plan",
            ("Add failing validator", "Add Route 32 map", "Build the ROM"),
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
    route_map_path = ENGINE / "data" / "maps" / "Route32_Frlg" / "map.json"
    route_scripts_path = ENGINE / "data" / "maps" / "Route32_Frlg" / "scripts.inc"

    if "#define FLAG_ROUTE32_FIRST_STEPS_REACHED   0x0B6" not in flags:
        errors.append("flags_frlg.h missing FLAG_ROUTE32_FIRST_STEPS_REACHED at 0x0B6")
    if "#define FLAG_ROUTE32_FIELD_CHECKLIST_REVIEWED   0x0B7" not in flags:
        errors.append("flags_frlg.h missing FLAG_ROUTE32_FIELD_CHECKLIST_REVIEWED at 0x0B7")
    if '"Route32_Frlg"' not in map_groups:
        errors.append("map_groups.json missing Route32_Frlg")
    if not violet_map_path.exists():
        errors.append("missing VioletCity_Frlg map.json before Route 32 connection validation")
    elif '"map": "MAP_ROUTE32"' not in read(violet_map_path):
        errors.append("Violet City map missing connection to MAP_ROUTE32")

    if not route_map_path.exists():
        errors.append("missing Route32_Frlg map.json")
    else:
        route_map = read(route_map_path)
        for marker in (
            '"id": "MAP_ROUTE32"',
            '"region": "REGION_JOHTO"',
            '"layout": "LAYOUT_ROUTE3"',
            '"map": "MAP_VIOLET_CITY"',
            "Route32_Frlg_EventScript_LyraRoadGuide",
            "Route32_Frlg_EventScript_RedVioletBackup",
            "Route32_Frlg_EventScript_FieldChecklist",
            "Route32_Frlg_EventScript_SilverTrace",
            "Route32_Frlg_EventScript_GoldDustToll",
            "Route32_Frlg_EventScript_RocketUnionCave",
        ):
            if marker not in route_map:
                errors.append(f"Route 32 map.json missing marker: {marker}")

    if not route_scripts_path.exists():
        errors.append("missing Route32_Frlg scripts.inc")
    else:
        scripts = read(route_scripts_path)
        for marker in (
            "Route32_Frlg_MapScripts",
            "FLAG_ROUTE32_FIRST_STEPS_REACHED",
            "FLAG_ROUTE32_FIELD_CHECKLIST_REVIEWED",
            "LYRA: Route 32 opens wide",
            "RED: I am staying in Violet",
            "FIELD CHECKLIST: Route 32",
            "MAREEP",
            "WOOPER",
            "TOGEPI",
            "SILVER TRACE: No battle",
            "GOLD DUST TOLL: A clean route",
            "ROCKET REMNANT: Union Cave",
            "WorldLink: Union Cave next",
            "Hoenn remains locked",
        ):
            if marker not in scripts:
                errors.append(f"Route 32 scripts missing marker: {marker}")
    return errors


def validate_design_data() -> list[str]:
    errors: list[str] = []
    johto = load_yaml(JOHTO_CHAPTER)
    messages = load_yaml(JOHTO_WORLDLINK)
    regions = load_yaml(REGION_PROGRESSION)
    rivals = load_yaml(RIVAL_PROGRESSION)

    act2 = next((act for act in johto.get("acts", []) if act.get("id") == "act_2_azalea_goldenrod"), {})
    for required_map in ("route_32", "union_cave", "azalea_town", "slowpoke_well"):
        if required_map not in act2.get("required_maps", []):
            errors.append(f"Johto act 2 missing required map: {required_map}")
    for event_id in (
        "route_32_union_cave_road",
        "lyra_route32_physical_guide",
        "red_violet_backup_call",
        "route32_field_checklist_review",
        "mareep_wooper_togepi_hints",
        "silver_route32_worldlink_trace",
        "gold_dust_route32_toll_pressure",
        "rocket_union_cave_remnant_tease",
    ):
        if event_id not in act2.get("required_events", []):
            errors.append(f"Johto act 2 missing Route 32 event: {event_id}")
    for unlock_id in (
        "route_32_live_map",
        "field_checklist_route32_page",
        "union_cave_story_gate",
        "azalea_road_pressure",
    ):
        if unlock_id not in act2.get("unlocks", []):
            errors.append(f"Johto act 2 missing Route 32 unlock: {unlock_id}")

    message_ids = {message.get("id") for message in messages.get("messages", [])}
    for message_id in (
        "WL_JOHTO_ROUTE32_FIRST_STEPS",
        "WL_JOHTO_ROUTE32_FIELD_CHECKLIST",
        "WL_JOHTO_SILVER_ROUTE32_TRACE",
        "WL_JOHTO_UNION_CAVE_NEXT",
    ):
        if message_id not in message_ids:
            errors.append(f"Johto WorldLink missing id: {message_id}")

    transition = regions.get("worldlink_region_progression", {}).get("current_transition_state", {})
    if transition.get("current_safe_hub") not in {"route_32", "union_cave", "azalea_town", "slowpoke_well", "azalea_gym", "bugsy_gym"}:
        errors.append("current transition state must record Route 32 or Union Cave as current safe hub")
    if transition.get("current_route") not in {"route_32", "union_cave", "azalea_town", "slowpoke_well", "azalea_gym", "bugsy_gym"}:
        errors.append("current transition state must keep current route as route_32 or union_cave")
    if transition.get("next_required_story_node") not in {"union_cave_first_entry", "azalea_first_arrival", "slowpoke_well_first_entry", "bugsy_gym_challenge", "ilex_forest_first_entry"}:
        errors.append("current transition state must advance next node to union_cave_first_entry or azalea_first_arrival")
    if transition.get("hard_lock_next_region") != "hoenn":
        errors.append("Hoenn must remain the hard-locked next region")

    band = rivals.get("progression_bands", {}).get("johto_route32_union_cave_road", {})
    if band.get("companions", {}).get("lyra", {}).get("event") != "physical_route32_guide":
        errors.append("Rival progression must set Lyra as physical Route 32 guide")
    if band.get("rivals", {}).get("silver", {}).get("event") != "worldlink_trace_no_battle":
        errors.append("Rival progression must set Silver as WorldLink trace with no battle")
    return errors


def validate_build_notes() -> list[str]:
    if not BUILD_NOTES.exists():
        return ["missing build notes file"]
    notes = read(BUILD_NOTES)
    errors: list[str] = []
    for marker in (
        "0051-route32-union-cave-road.patch",
        "validate_route32_union_cave_road.py",
        "Route 32 Union Cave road",
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
        print("Route 32 Union Cave road validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Route 32 Union Cave road validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
