#!/usr/bin/env python3
"""Validate the first playable New Bark arrival slice."""

from __future__ import annotations

from pathlib import Path

try:
    import yaml
except ImportError as exc:
    raise SystemExit("PyYAML is required: python3 -m pip install PyYAML") from exc


ROOT = Path(__file__).resolve().parents[1]
ENGINE = ROOT / "engine" / "pokeemerald-expansion"
PATCH = ROOT / "patches" / "engine" / "0041-new-bark-arrival-map.patch"
SPEC = ROOT / "docs" / "superpowers" / "specs" / "2026-06-14-new-bark-arrival-map-design.md"
PLAN = ROOT / "docs" / "superpowers" / "plans" / "2026-06-14-new-bark-arrival-map.md"
JOHTO_CHAPTER = ROOT / "data_design" / "johto_chapter.yaml"
JOHTO_WORLDLINK = ROOT / "data_design" / "johto_worldlink_messages.yaml"
REGION_PROGRESSION = ROOT / "data_design" / "worldlink_region_progression.yaml"
BUILD_NOTES = ROOT / "build_notes" / "FIRST_PLAYABLE_OPENEMU_SMOKE_TEST.md"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def load_yaml(path: Path):
    return yaml.safe_load(read(path))


def validate_patch_docs() -> list[str]:
    errors: list[str] = []
    if not PATCH.exists():
        errors.append("missing patch file: 0041-new-bark-arrival-map.patch")
    elif PATCH.stat().st_size == 0:
        errors.append("empty patch file: 0041-new-bark-arrival-map.patch")
    else:
        patch = read(PATCH)
        for marker in (
            "MAP_NEW_BARK_TOWN",
            "NewBarkTown_Frlg",
            "FLAG_NEW_BARK_ARRIVAL_REACHED",
            "NewBarkTown_Frlg_Text_LyraArrival",
            "WorldLink: Johto active",
            "Hoenn remains locked",
        ):
            if marker not in patch:
                errors.append(f"patch 0041 missing marker: {marker}")

    for doc_path, doc_name, markers in (
        (
            SPEC,
            "New Bark arrival map spec",
            ("first real Johto playable map", "Red arrives with Antman", "Hoenn remains locked"),
        ),
        (
            PLAN,
            "New Bark arrival map plan",
            ("Add failing validator", "Add New Bark map", "Build the ROM"),
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
    pallet_scripts = read(ENGINE / "data" / "maps" / "PalletTown_Frlg" / "scripts.inc")
    new_bark_map_path = ENGINE / "data" / "maps" / "NewBarkTown_Frlg" / "map.json"
    new_bark_scripts_path = ENGINE / "data" / "maps" / "NewBarkTown_Frlg" / "scripts.inc"

    if "#define FLAG_NEW_BARK_ARRIVAL_REACHED       0x024" not in flags:
        errors.append("flags_frlg.h missing FLAG_NEW_BARK_ARRIVAL_REACHED at 0x024")
    if '"NewBarkTown_Frlg"' not in map_groups:
        errors.append("map_groups.json missing NewBarkTown_Frlg")
    for marker in (
        "warp MAP_NEW_BARK_TOWN",
        "setflag FLAG_NEW_BARK_ARRIVAL_REACHED",
        "PalletTown_Text_WorldCircuitGateDepartureConfirmed",
    ):
        if marker not in pallet_scripts:
            errors.append(f"Pallet scripts missing New Bark departure marker: {marker}")

    if not new_bark_map_path.exists():
        errors.append("missing NewBarkTown_Frlg map.json")
    else:
        new_bark_map = read(new_bark_map_path)
        for marker in (
            '"id": "MAP_NEW_BARK_TOWN"',
            '"region": "REGION_JOHTO"',
            '"layout": "LAYOUT_PALLET_TOWN"',
            "NewBarkTown_Frlg_EventScript_RedArrival",
            "NewBarkTown_Frlg_EventScript_LyraArrival",
            "NewBarkTown_Frlg_EventScript_ElmSignal",
        ):
            if marker not in new_bark_map:
                errors.append(f"New Bark map.json missing marker: {marker}")

    if not new_bark_scripts_path.exists():
        errors.append("missing NewBarkTown_Frlg scripts.inc")
    else:
        scripts = read(new_bark_scripts_path)
        for marker in (
            "NewBarkTown_Frlg_MapScripts",
            "FLAG_NEW_BARK_ARRIVAL_REACHED",
            "WorldLink: Johto active",
            "RED: We made it",
            "LYRA: Welcome to Johto",
            "ELM: New Bark Lab has your clearance",
            "Silver profile moved toward Cherrygrove",
            "Hoenn remains locked",
        ):
            if marker not in scripts:
                errors.append(f"New Bark scripts missing marker: {marker}")

    return errors


def validate_design_data() -> list[str]:
    errors: list[str] = []
    johto = load_yaml(JOHTO_CHAPTER)
    messages = load_yaml(JOHTO_WORLDLINK)
    regions = load_yaml(REGION_PROGRESSION)

    act1 = next((act for act in johto.get("acts", []) if act.get("id") == "act_1_new_bark_to_violet"), {})
    for event_id in (
        "new_bark_arrival_map_live",
        "lyra_first_physical_contact",
        "red_arrives_as_johto_companion",
        "elm_remote_lab_clearance",
        "silver_cherrygrove_profile_moved",
    ):
        if event_id not in act1.get("required_events", []):
            errors.append(f"Johto act 1 missing New Bark event: {event_id}")
    if "new_bark_town_live_map" not in act1.get("unlocks", []):
        errors.append("Johto act 1 must unlock new_bark_town_live_map")

    message_ids = {message.get("id") for message in messages.get("messages", [])}
    for message_id in (
        "WL_JOHTO_NEW_BARK_MAP_LIVE",
        "WL_JOHTO_LYRA_FIRST_CONTACT",
        "WL_JOHTO_HOENN_LOCK_CONFIRMED",
    ):
        if message_id not in message_ids:
            errors.append(f"Johto WorldLink missing id: {message_id}")

    transition = regions.get("worldlink_region_progression", {}).get("current_transition_state", {})
    if transition.get("next_required_story_node") not in {"elm_lab_first_visit", "route_29_first_steps", "cherrygrove_first_arrival", "route_30_first_steps", "mr_pokemon_house_first_visit", "violet_city_first_arrival", "sprout_tower_first_floor", "sprout_tower_upper_floor", "falkner_gym_battle", "route_32_union_cave_road", "union_cave_first_entry", "azalea_first_arrival"}:
        errors.append("current transition state must advance next node to Elm Lab or later Route 29 follow-up")
    if transition.get("arrival_map") != "new_bark_town":
        errors.append("current transition state must record arrival_map new_bark_town")
    if transition.get("hard_lock_next_region") != "hoenn":
        errors.append("Hoenn must remain the hard-locked next region")

    return errors


def validate_build_notes() -> list[str]:
    if not BUILD_NOTES.exists():
        return ["missing build notes file"]
    notes = read(BUILD_NOTES)
    errors: list[str] = []
    for marker in (
        "0041-new-bark-arrival-map.patch",
        "validate_new_bark_arrival_map.py",
        "New Bark arrival map",
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
        print("New Bark arrival map validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("New Bark arrival map validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
