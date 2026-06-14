#!/usr/bin/env python3
"""Validate the first playable Ilex Forest entry slice."""

from __future__ import annotations

from pathlib import Path

try:
    import yaml
except ImportError as exc:
    raise SystemExit("PyYAML is required: python3 -m pip install PyYAML") from exc


ROOT = Path(__file__).resolve().parents[1]
ENGINE = ROOT / "engine" / "pokeemerald-expansion"
PATCH = ROOT / "patches" / "engine" / "0056-ilex-forest-first-entry.patch"
SPEC = ROOT / "docs" / "superpowers" / "specs" / "2026-06-14-ilex-forest-first-entry-design.md"
PLAN = ROOT / "docs" / "superpowers" / "plans" / "2026-06-14-ilex-forest-first-entry.md"
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
        errors.append("missing patch file: 0056-ilex-forest-first-entry.patch")
    elif PATCH.stat().st_size == 0:
        errors.append("empty patch file: 0056-ilex-forest-first-entry.patch")
    else:
        patch = read(PATCH)
        for marker in (
            "MAP_ILEX_FOREST",
            "IlexForest_Frlg",
            "FLAG_ILEX_FOREST_FIRST_ENTRY_REACHED",
            "FLAG_ILEX_FIELD_TOOL_STATIC_REACHED",
            "FLAG_ILEX_SILVER_SECRET_ASSIST_REACHED",
            "IlexForest_Frlg_Text_FieldToolStatic",
            "IlexForest_Frlg_Text_MoonlightShrine",
            "IlexForest_Frlg_Text_SilverSecretAssist",
            "IlexForest_Frlg_Text_CelebiWhisper",
            "WorldLink: Goldenrod City next",
        ):
            if marker not in patch:
                errors.append(f"patch 0056 missing marker: {marker}")

    for doc_path, doc_name, markers in (
        (
            SPEC,
            "Ilex Forest spec",
            ("Field Tool static as a prototype", "Celebi appears only as a shrine whisper", "goldenrod_city_first_arrival"),
        ),
        (
            PLAN,
            "Ilex Forest plan",
            ("Add a failing validator", "Add `MAP_ILEX_FOREST`", "Build the FireRed target ROM"),
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
    azalea_map_path = ENGINE / "data" / "maps" / "AzaleaTown_Frlg" / "map.json"
    ilex_map_path = ENGINE / "data" / "maps" / "IlexForest_Frlg" / "map.json"
    ilex_scripts_path = ENGINE / "data" / "maps" / "IlexForest_Frlg" / "scripts.inc"
    flags = read(ENGINE / "include" / "constants" / "flags_frlg.h")

    if not ilex_map_path.exists() or "FLAG_ILEX_FOREST_FIRST_ENTRY_REACHED" not in flags:
        patch = read(PATCH) if PATCH.exists() else ""
        for marker in (
            "#define FLAG_ILEX_FOREST_FIRST_ENTRY_REACHED   0x0C4",
            "#define FLAG_ILEX_FIELD_TOOL_STATIC_REACHED   0x0C5",
            "#define FLAG_ILEX_SILVER_SECRET_ASSIST_REACHED   0x0C6",
            '"IlexForest_Frlg"',
            '"dest_map": "MAP_ILEX_FOREST"',
            '"id": "MAP_ILEX_FOREST"',
            '"region": "REGION_JOHTO"',
            '"layout": "LAYOUT_VIRIDIAN_FOREST"',
            '"dest_map": "MAP_AZALEA_TOWN"',
            "IlexForest_Frlg_EventScript_RedEdgeSupport",
            "IlexForest_Frlg_EventScript_LyraFarfetchdMemory",
            "IlexForest_Frlg_EventScript_FieldToolStatic",
            "IlexForest_Frlg_EventScript_MoonlightShrine",
            "IlexForest_Frlg_EventScript_SilverSecretAssist",
            "IlexForest_Frlg_EventScript_CelebiWhisper",
            "IlexForest_Frlg_EventScript_GoldenrodNext",
            "IlexForest_Frlg_MapScripts",
            "RED: Old forests",
            "LYRA: This is the old Farfetch'd",
            "FIELD TOOL STATIC",
            "MOONLIGHT: Memory is a path",
            "SILVER TRACE: Cut branch",
            "CELEBI SHRINE: Time remembers",
            "Following Pokemon remains locked",
            "WorldLink: Goldenrod City next",
            "Hoenn remains locked",
        ):
            if marker not in patch:
                errors.append(f"patch 0056 missing engine marker: {marker}")
        return errors

    map_groups = read(ENGINE / "data" / "maps" / "map_groups.json")

    for marker in (
        "#define FLAG_ILEX_FOREST_FIRST_ENTRY_REACHED   0x0C4",
        "#define FLAG_ILEX_FIELD_TOOL_STATIC_REACHED   0x0C5",
        "#define FLAG_ILEX_SILVER_SECRET_ASSIST_REACHED   0x0C6",
    ):
        if marker not in flags:
            errors.append(f"flags_frlg.h missing marker: {marker}")
    if '"IlexForest_Frlg"' not in map_groups:
        errors.append("map_groups.json missing IlexForest_Frlg")
    if not azalea_map_path.exists():
        errors.append("missing AzaleaTown_Frlg map.json before Ilex warp validation")
    elif '"dest_map": "MAP_ILEX_FOREST"' not in read(azalea_map_path):
        errors.append("Azalea map missing warp to MAP_ILEX_FOREST")

    if not ilex_map_path.exists():
        errors.append("missing IlexForest_Frlg map.json")
    else:
        ilex_map = read(ilex_map_path)
        for marker in (
            '"id": "MAP_ILEX_FOREST"',
            '"region": "REGION_JOHTO"',
            '"layout": "LAYOUT_VIRIDIAN_FOREST"',
            '"dest_map": "MAP_AZALEA_TOWN"',
            "IlexForest_Frlg_EventScript_RedEdgeSupport",
            "IlexForest_Frlg_EventScript_LyraFarfetchdMemory",
            "IlexForest_Frlg_EventScript_FieldToolStatic",
            "IlexForest_Frlg_EventScript_MoonlightShrine",
            "IlexForest_Frlg_EventScript_SilverSecretAssist",
            "IlexForest_Frlg_EventScript_CelebiWhisper",
            "IlexForest_Frlg_EventScript_GoldenrodNext",
        ):
            if marker not in ilex_map:
                errors.append(f"Ilex Forest map.json missing marker: {marker}")

    if not ilex_scripts_path.exists():
        errors.append("missing IlexForest_Frlg scripts.inc")
    else:
        scripts = read(ilex_scripts_path)
        for marker in (
            "IlexForest_Frlg_MapScripts",
            "FLAG_ILEX_FOREST_FIRST_ENTRY_REACHED",
            "FLAG_ILEX_FIELD_TOOL_STATIC_REACHED",
            "FLAG_ILEX_SILVER_SECRET_ASSIST_REACHED",
            "RED: Old forests",
            "LYRA: This is the old Farfetch'd",
            "FIELD TOOL STATIC",
            "MOONLIGHT: Memory is a path",
            "SILVER TRACE: Cut branch",
            "CELEBI SHRINE: Time remembers",
            "Following Pokemon remains locked",
            "WorldLink: Goldenrod City next",
            "Hoenn remains locked",
        ):
            if marker not in scripts:
                errors.append(f"Ilex Forest scripts missing marker: {marker}")
    return errors


def validate_design_data() -> list[str]:
    errors: list[str] = []
    johto = load_yaml(JOHTO_CHAPTER)
    messages = load_yaml(JOHTO_WORLDLINK)
    regions = load_yaml(REGION_PROGRESSION)
    rivals = load_yaml(RIVAL_PROGRESSION)

    act2 = next((act for act in johto.get("acts", []) if act.get("id") == "act_2_azalea_goldenrod"), {})
    for event_id in (
        "ilex_forest_first_entry",
        "red_ilex_edge_support",
        "lyra_farfetchd_route_memory",
        "field_tool_static_prototype",
        "moonlight_shrine_memory_pressure",
        "silver_secret_path_assist",
        "celebi_shrine_whisper",
        "goldenrod_city_next_objective",
        "following_pokemon_goldenrod_tease",
    ):
        if event_id not in act2.get("required_events", []):
            errors.append(f"Johto act 2 missing Ilex event: {event_id}")
    for unlock_id in (
        "ilex_forest_live_map",
        "field_tool_static_prototype",
        "celebi_shrine_tease",
        "following_pokemon_goldenrod_tease",
        "goldenrod_city_story_gate",
    ):
        if unlock_id not in act2.get("unlocks", []):
            errors.append(f"Johto act 2 missing Ilex unlock: {unlock_id}")

    message_ids = {message.get("id") for message in messages.get("messages", [])}
    for message_id in (
        "WL_JOHTO_ILEX_FOREST_FIRST_ENTRY",
        "WL_JOHTO_FIELD_TOOL_STATIC",
        "WL_JOHTO_SILVER_SECRET_ASSIST",
        "WL_JOHTO_CELEBI_SHRINE_WHISPER",
        "WL_JOHTO_GOLDENROD_NEXT",
    ):
        if message_id not in message_ids:
            errors.append(f"Johto WorldLink missing id: {message_id}")

    transition = regions.get("worldlink_region_progression", {}).get("current_transition_state", {})
    if transition.get("current_safe_hub") != "ilex_forest":
        errors.append("current transition state must record Ilex Forest as current safe hub")
    if transition.get("current_route") != "ilex_forest":
        errors.append("current transition state must keep current route as ilex_forest")
    if transition.get("next_required_story_node") != "goldenrod_city_first_arrival":
        errors.append("current transition state must advance next node to goldenrod_city_first_arrival")
    if transition.get("hard_lock_next_region") != "hoenn":
        errors.append("Hoenn must remain the hard-locked next region")

    band = rivals.get("progression_bands", {}).get("johto_ilex_forest_first_entry", {})
    if band.get("companions", {}).get("red", {}).get("event") != "ilex_edge_support":
        errors.append("Rival progression must set Red as Ilex edge support")
    if band.get("companions", {}).get("lyra", {}).get("event") != "farfetchd_route_memory":
        errors.append("Rival progression must set Lyra as Farfetch'd route memory guide")
    if band.get("rivals", {}).get("silver", {}).get("event") != "secret_path_assist_no_battle":
        errors.append("Rival progression must set Silver as secret no-battle assist")
    if band.get("rivals", {}).get("moonlight", {}).get("event") != "shrine_memory_pressure":
        errors.append("Rival progression must set Moonlight as shrine memory pressure")
    return errors


def validate_build_notes() -> list[str]:
    if not BUILD_NOTES.exists():
        return ["missing build notes file"]
    notes = read(BUILD_NOTES)
    errors: list[str] = []
    for marker in (
        "0056-ilex-forest-first-entry.patch",
        "validate_ilex_forest_first_entry.py",
        "Ilex Forest first entry milestone",
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
        print("Ilex Forest first entry validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Ilex Forest first entry validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
