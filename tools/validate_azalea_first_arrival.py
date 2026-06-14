#!/usr/bin/env python3
"""Validate the first playable Azalea Town arrival slice."""

from __future__ import annotations

from pathlib import Path

try:
    import yaml
except ImportError as exc:
    raise SystemExit("PyYAML is required: python3 -m pip install PyYAML") from exc


ROOT = Path(__file__).resolve().parents[1]
ENGINE = ROOT / "engine" / "pokeemerald-expansion"
PATCH = ROOT / "patches" / "engine" / "0053-azalea-first-arrival.patch"
SPEC = ROOT / "docs" / "superpowers" / "specs" / "2026-06-14-azalea-first-arrival-design.md"
PLAN = ROOT / "docs" / "superpowers" / "plans" / "2026-06-14-azalea-first-arrival.md"
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
        errors.append("missing patch file: 0053-azalea-first-arrival.patch")
    elif PATCH.stat().st_size == 0:
        errors.append("empty patch file: 0053-azalea-first-arrival.patch")
    else:
        patch = read(PATCH)
        for marker in (
            "MAP_AZALEA_TOWN",
            "AzaleaTown_Frlg",
            "FLAG_AZALEA_FIRST_ARRIVAL_REACHED",
            "FLAG_AZALEA_KURT_WARNING_REACHED",
            "FLAG_AZALEA_SLOWPOKE_WELL_GATE_CHECKED",
            "AzaleaTown_Frlg_Text_LyraTownEdge",
            "AzaleaTown_Frlg_Text_KurtWarning",
            "AzaleaTown_Frlg_Text_RocketWellGuard",
            "AzaleaTown_Frlg_Text_GoldDustTailMarket",
            "AzaleaTown_Frlg_Text_BugsyAide",
            "Slowpoke Well next",
        ):
            if marker not in patch:
                errors.append(f"patch 0053 missing marker: {marker}")

    for doc_path, doc_name, markers in (
        (
            SPEC,
            "Azalea spec",
            ("tense quiet scene", "Apricorn Balls are teased", "slowpoke_well_first_entry"),
        ),
        (
            PLAN,
            "Azalea plan",
            ("Add a failing validator", "Add `MAP_AZALEA_TOWN`", "Build the ROM"),
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
    cave_map_path = ENGINE / "data" / "maps" / "UnionCave_1F_Frlg" / "map.json"
    azalea_map_path = ENGINE / "data" / "maps" / "AzaleaTown_Frlg" / "map.json"
    azalea_scripts_path = ENGINE / "data" / "maps" / "AzaleaTown_Frlg" / "scripts.inc"

    for marker in (
        "#define FLAG_AZALEA_FIRST_ARRIVAL_REACHED   0x0BB",
        "#define FLAG_AZALEA_KURT_WARNING_REACHED   0x0BC",
        "#define FLAG_AZALEA_SLOWPOKE_WELL_GATE_CHECKED   0x0BD",
    ):
        if marker not in flags:
            errors.append(f"flags_frlg.h missing marker: {marker}")
    if '"AzaleaTown_Frlg"' not in map_groups:
        errors.append("map_groups.json missing AzaleaTown_Frlg")
    if not cave_map_path.exists():
        errors.append("missing UnionCave_1F_Frlg map.json before Azalea warp validation")
    elif '"dest_map": "MAP_AZALEA_TOWN"' not in read(cave_map_path):
        errors.append("Union Cave map missing warp to MAP_AZALEA_TOWN")

    if not azalea_map_path.exists():
        errors.append("missing AzaleaTown_Frlg map.json")
    else:
        azalea_map = read(azalea_map_path)
        for marker in (
            '"id": "MAP_AZALEA_TOWN"',
            '"region": "REGION_JOHTO"',
            '"layout": "LAYOUT_LAVENDER_TOWN"',
            '"map_type": "MAP_TYPE_TOWN"',
            '"dest_map": "MAP_UNION_CAVE_1F"',
            "AzaleaTown_Frlg_EventScript_LyraTownEdge",
            "AzaleaTown_Frlg_EventScript_RedTownWatch",
            "AzaleaTown_Frlg_EventScript_KurtWarning",
            "AzaleaTown_Frlg_EventScript_RocketWellGuard",
            "AzaleaTown_Frlg_EventScript_GoldDustTailMarket",
            "AzaleaTown_Frlg_EventScript_BugsyAide",
            "AzaleaTown_Frlg_EventScript_SilverTrace",
            "AzaleaTown_Frlg_EventScript_SlowpokeWellLock",
        ):
            if marker not in azalea_map:
                errors.append(f"Azalea map.json missing marker: {marker}")

    if not azalea_scripts_path.exists():
        errors.append("missing AzaleaTown_Frlg scripts.inc")
    else:
        scripts = read(azalea_scripts_path)
        for marker in (
            "AzaleaTown_Frlg_MapScripts",
            "FLAG_AZALEA_FIRST_ARRIVAL_REACHED",
            "FLAG_AZALEA_KURT_WARNING_REACHED",
            "FLAG_AZALEA_SLOWPOKE_WELL_GATE_CHECKED",
            "LYRA: Azalea is quiet",
            "RED: I will watch the cave",
            "KURT: Slowpoke are not",
            "ROCKET: The well is closed",
            "GOLD DUST: A market is",
            "BUGSY AIDE: Gym challenge",
            "SILVER TRACE: Well side",
            "WorldLink: Slowpoke Well next",
            "Hoenn remains locked",
        ):
            if marker not in scripts:
                errors.append(f"Azalea scripts missing marker: {marker}")
    return errors


def validate_design_data() -> list[str]:
    errors: list[str] = []
    johto = load_yaml(JOHTO_CHAPTER)
    messages = load_yaml(JOHTO_WORLDLINK)
    regions = load_yaml(REGION_PROGRESSION)
    rivals = load_yaml(RIVAL_PROGRESSION)

    act2 = next((act for act in johto.get("acts", []) if act.get("id") == "act_2_azalea_goldenrod"), {})
    for event_id in (
        "azalea_first_arrival",
        "lyra_azalea_silence_warning",
        "red_azalea_cave_watch",
        "kurt_slowpoke_moral_warning",
        "rocket_well_guard_lock",
        "gold_dust_tail_market_pressure",
        "bugsy_gym_locked_until_well",
        "apricorn_balls_tease",
        "worldlink_slowpoke_well_next",
    ):
        if event_id not in act2.get("required_events", []):
            errors.append(f"Johto act 2 missing Azalea event: {event_id}")
    for unlock_id in (
        "azalea_town_live_map",
        "azalea_town_checklist_page",
        "slowpoke_well_story_gate",
        "bugsy_gym_story_gate_locked",
        "apricorn_balls_tease",
    ):
        if unlock_id not in act2.get("unlocks", []):
            errors.append(f"Johto act 2 missing Azalea unlock: {unlock_id}")

    message_ids = {message.get("id") for message in messages.get("messages", [])}
    for message_id in (
        "WL_JOHTO_AZALEA_FIRST_ARRIVAL",
        "WL_JOHTO_KURT_WARNING",
        "WL_JOHTO_ROCKET_GOLD_DUST_TAIL_MARKET",
        "WL_JOHTO_BUGSY_LOCKED",
        "WL_JOHTO_SLOWPOKE_WELL_NEXT",
    ):
        if message_id not in message_ids:
            errors.append(f"Johto WorldLink missing id: {message_id}")

    transition = regions.get("worldlink_region_progression", {}).get("current_transition_state", {})
    if transition.get("current_safe_hub") != "azalea_town":
        errors.append("current transition state must record Azalea Town as current safe hub")
    if transition.get("current_route") != "azalea_town":
        errors.append("current transition state must keep current route as azalea_town")
    if transition.get("next_required_story_node") != "slowpoke_well_first_entry":
        errors.append("current transition state must advance next node to slowpoke_well_first_entry")
    if transition.get("hard_lock_next_region") != "hoenn":
        errors.append("Hoenn must remain the hard-locked next region")

    band = rivals.get("progression_bands", {}).get("johto_azalea_first_arrival", {})
    if band.get("companions", {}).get("red", {}).get("event") != "azalea_cave_watch":
        errors.append("Rival progression must set Red as Azalea cave watch")
    if band.get("companions", {}).get("lyra", {}).get("event") != "azalea_silence_warning":
        errors.append("Rival progression must set Lyra as Azalea silence warning")
    if band.get("rivals", {}).get("silver", {}).get("event") != "slowpoke_well_trace_no_battle":
        errors.append("Rival progression must set Silver as Slowpoke Well trace with no battle")
    return errors


def validate_build_notes() -> list[str]:
    if not BUILD_NOTES.exists():
        return ["missing build notes file"]
    notes = read(BUILD_NOTES)
    errors: list[str] = []
    for marker in (
        "0053-azalea-first-arrival.patch",
        "validate_azalea_first_arrival.py",
        "Azalea first arrival",
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
        print("Azalea first arrival validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Azalea first arrival validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
