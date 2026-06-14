#!/usr/bin/env python3
"""Validate the first playable Union Cave entry slice."""

from __future__ import annotations

from pathlib import Path

try:
    import yaml
except ImportError as exc:
    raise SystemExit("PyYAML is required: python3 -m pip install PyYAML") from exc


ROOT = Path(__file__).resolve().parents[1]
ENGINE = ROOT / "engine" / "pokeemerald-expansion"
PATCH = ROOT / "patches" / "engine" / "0052-union-cave-first-entry.patch"
SPEC = ROOT / "docs" / "superpowers" / "specs" / "2026-06-14-union-cave-first-entry-design.md"
PLAN = ROOT / "docs" / "superpowers" / "plans" / "2026-06-14-union-cave-first-entry.md"
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
        errors.append("missing patch file: 0052-union-cave-first-entry.patch")
    elif PATCH.stat().st_size == 0:
        errors.append("empty patch file: 0052-union-cave-first-entry.patch")
    else:
        patch = read(PATCH)
        for marker in (
            "MAP_UNION_CAVE_1F",
            "UnionCave_1F_Frlg",
            "FLAG_UNION_CAVE_FIRST_ENTRY_REACHED",
            "FLAG_UNION_CAVE_FIELD_CHECKLIST_REVIEWED",
            "FLAG_UNION_CAVE_RED_EMERGENCY_REACHED",
            "UnionCave_1F_Frlg_Text_LyraEntry",
            "UnionCave_1F_Frlg_Text_RocketGoldDustClash",
            "UnionCave_1F_Frlg_Text_RedEmergency",
            "UnionCave_1F_Frlg_Text_CaveChecklist",
            "UnionCave_1F_Frlg_Text_SilverExitTrace",
            "Azalea next",
        ):
            if marker not in patch:
                errors.append(f"patch 0052 missing marker: {marker}")

    for doc_path, doc_name, markers in (
        (
            SPEC,
            "Union Cave spec",
            ("Rocket remnants and Gold Dust actively fighting", "first cave-specific Field Checklist", "azalea_first_arrival", "slowpoke_well_first_entry"),
        ),
        (
            PLAN,
            "Union Cave plan",
            ("Add a failing validator", "Add `MAP_UNION_CAVE_1F`", "Build the ROM"),
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
    route32_map_path = ENGINE / "data" / "maps" / "Route32_Frlg" / "map.json"
    cave_map_path = ENGINE / "data" / "maps" / "UnionCave_1F_Frlg" / "map.json"
    cave_scripts_path = ENGINE / "data" / "maps" / "UnionCave_1F_Frlg" / "scripts.inc"

    for marker in (
        "#define FLAG_UNION_CAVE_FIRST_ENTRY_REACHED   0x0B8",
        "#define FLAG_UNION_CAVE_FIELD_CHECKLIST_REVIEWED   0x0B9",
        "#define FLAG_UNION_CAVE_RED_EMERGENCY_REACHED   0x0BA",
    ):
        if marker not in flags:
            errors.append(f"flags_frlg.h missing marker: {marker}")
    if '"UnionCave_1F_Frlg"' not in map_groups:
        errors.append("map_groups.json missing UnionCave_1F_Frlg")
    if not route32_map_path.exists():
        errors.append("missing Route32_Frlg map.json before Union Cave warp validation")
    elif '"dest_map": "MAP_UNION_CAVE_1F"' not in read(route32_map_path):
        errors.append("Route 32 map missing warp to MAP_UNION_CAVE_1F")

    if not cave_map_path.exists():
        errors.append("missing UnionCave_1F_Frlg map.json")
    else:
        cave_map = read(cave_map_path)
        for marker in (
            '"id": "MAP_UNION_CAVE_1F"',
            '"region": "REGION_JOHTO"',
            '"layout": "LAYOUT_MT_MOON_1F"',
            '"map_type": "MAP_TYPE_UNDERGROUND"',
            '"dest_map": "MAP_ROUTE32"',
            "UnionCave_1F_Frlg_EventScript_LyraEntry",
            "UnionCave_1F_Frlg_EventScript_RocketGoldDustClash",
            "UnionCave_1F_Frlg_EventScript_RedEmergency",
            "UnionCave_1F_Frlg_EventScript_CaveChecklist",
            "UnionCave_1F_Frlg_EventScript_SilverExitTrace",
            "UnionCave_1F_Frlg_EventScript_AzaleaExitLock",
        ):
            if marker not in cave_map:
                errors.append(f"Union Cave map.json missing marker: {marker}")

    if not cave_scripts_path.exists():
        errors.append("missing UnionCave_1F_Frlg scripts.inc")
    else:
        scripts = read(cave_scripts_path)
        for marker in (
            "UnionCave_1F_Frlg_MapScripts",
            "FLAG_UNION_CAVE_FIRST_ENTRY_REACHED",
            "FLAG_UNION_CAVE_FIELD_CHECKLIST_REVIEWED",
            "FLAG_UNION_CAVE_RED_EMERGENCY_REACHED",
            "LYRA: Union Cave is where",
            "ROCKET: This tunnel is still",
            "GOLD DUST: Ownership beats",
            "RED: I heard the WorldLink",
            "CAVE CHECKLIST: Union Cave",
            "ZUBAT",
            "ONIX",
            "SILVER TRACE: Exit side",
            "WorldLink: Azalea next",
            "Hoenn remains locked",
        ):
            if marker not in scripts:
                errors.append(f"Union Cave scripts missing marker: {marker}")
    return errors


def validate_design_data() -> list[str]:
    errors: list[str] = []
    johto = load_yaml(JOHTO_CHAPTER)
    messages = load_yaml(JOHTO_WORLDLINK)
    regions = load_yaml(REGION_PROGRESSION)
    rivals = load_yaml(RIVAL_PROGRESSION)

    act2 = next((act for act in johto.get("acts", []) if act.get("id") == "act_2_azalea_goldenrod"), {})
    for event_id in (
        "union_cave_first_entry",
        "lyra_union_cave_entrance_support",
        "rocket_gold_dust_cave_clash",
        "red_union_cave_emergency_tag_scene",
        "cave_field_checklist_page",
        "silver_union_cave_exit_trace",
        "azalea_exit_locked_until_kurt",
    ):
        if event_id not in act2.get("required_events", []):
            errors.append(f"Johto act 2 missing Union Cave event: {event_id}")
    for unlock_id in (
        "union_cave_live_map",
        "field_checklist_union_cave_page",
        "rocket_gold_dust_cave_conflict",
        "azalea_story_gate",
    ):
        if unlock_id not in act2.get("unlocks", []):
            errors.append(f"Johto act 2 missing Union Cave unlock: {unlock_id}")

    message_ids = {message.get("id") for message in messages.get("messages", [])}
    for message_id in (
        "WL_JOHTO_UNION_CAVE_FIRST_ENTRY",
        "WL_JOHTO_UNION_CAVE_FIELD_CHECKLIST",
        "WL_JOHTO_ROCKET_GOLD_DUST_CAVE_CLASH",
        "WL_JOHTO_RED_UNION_CAVE_EMERGENCY",
        "WL_JOHTO_AZALEA_NEXT",
    ):
        if message_id not in message_ids:
            errors.append(f"Johto WorldLink missing id: {message_id}")

    transition = regions.get("worldlink_region_progression", {}).get("current_transition_state", {})
    if transition.get("current_safe_hub") not in {"union_cave", "azalea_town"}:
        errors.append("current transition state must record Union Cave or Azalea Town as current safe hub")
    if transition.get("current_route") not in {"union_cave", "azalea_town"}:
        errors.append("current transition state must keep current route as union_cave or azalea_town")
    if transition.get("next_required_story_node") not in {"azalea_first_arrival", "slowpoke_well_first_entry"}:
        errors.append("current transition state must advance next node to azalea_first_arrival or slowpoke_well_first_entry")
    if transition.get("hard_lock_next_region") != "hoenn":
        errors.append("Hoenn must remain the hard-locked next region")

    band = rivals.get("progression_bands", {}).get("johto_union_cave_first_entry", {})
    if band.get("companions", {}).get("lyra", {}).get("event") != "union_cave_entrance_support":
        errors.append("Rival progression must set Lyra as Union Cave entrance support")
    if band.get("companions", {}).get("red", {}).get("event") != "emergency_cave_tag_scene":
        errors.append("Rival progression must set Red as emergency cave tag scene")
    if band.get("rivals", {}).get("silver", {}).get("event") != "azalea_exit_trace_no_battle":
        errors.append("Rival progression must set Silver as Azalea exit trace with no battle")
    return errors


def validate_build_notes() -> list[str]:
    if not BUILD_NOTES.exists():
        return ["missing build notes file"]
    notes = read(BUILD_NOTES)
    errors: list[str] = []
    for marker in (
        "0052-union-cave-first-entry.patch",
        "validate_union_cave_first_entry.py",
        "Union Cave first entry",
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
        print("Union Cave first entry validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Union Cave first entry validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
