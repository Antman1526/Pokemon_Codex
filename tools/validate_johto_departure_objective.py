#!/usr/bin/env python3
"""Validate the Johto departure objective slice."""

from __future__ import annotations

from pathlib import Path

try:
    import yaml
except ImportError as exc:
    raise SystemExit("PyYAML is required: python3 -m pip install PyYAML") from exc


ROOT = Path(__file__).resolve().parents[1]
ENGINE = ROOT / "engine" / "pokeemerald-expansion"
PATCH = ROOT / "patches" / "engine" / "0040-johto-departure-objective.patch"
SPEC = ROOT / "docs" / "superpowers" / "specs" / "2026-06-14-johto-departure-objective-design.md"
PLAN = ROOT / "docs" / "superpowers" / "plans" / "2026-06-14-johto-departure-objective.md"
KANTO = ROOT / "data_design" / "kanto_chapter.yaml"
KANTO_WORLDLINK = ROOT / "data_design" / "kanto_worldlink_messages.yaml"
RIVAL_PROGRESSION = ROOT / "data_design" / "rival_progression_kanto.yaml"
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
        errors.append("missing patch file: 0040-johto-departure-objective.patch")
    elif PATCH.stat().st_size == 0:
        errors.append("empty patch file: 0040-johto-departure-objective.patch")
    else:
        patch = read(PATCH)
        for marker in (
            "FLAG_JOHTO_DEPARTURE_CONFIRMED",
            "PalletTown_EventScript_RedWorldCircuitGateConfirmDeparture",
            "ELM: New Bark Lab receiving",
            "SILVER profile detected",
            "WorldLink Objective: Enter Johto",
        ):
            if marker not in patch:
                errors.append(f"patch 0040 missing marker: {marker}")

    for doc_path, doc_name, markers in (
        (
            SPEC,
            "Johto departure objective spec",
            ("Elm and Lyra", "Silver is only a profile tease", "no Hoenn unlock"),
        ),
        (
            PLAN,
            "Johto departure objective plan",
            ("Add a failing validator", "Patch Pallet Gate", "Build the ROM"),
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
    scripts = read(ENGINE / "data" / "maps" / "PalletTown_Frlg" / "scripts.inc")

    if "#define FLAG_JOHTO_DEPARTURE_CONFIRMED       0x023" not in flags:
        errors.append("flags_frlg.h missing FLAG_JOHTO_DEPARTURE_CONFIRMED at 0x023")

    for marker in (
        "goto_if_unset FLAG_JOHTO_DEPARTURE_CONFIRMED",
        "PalletTown_EventScript_RedWorldCircuitGateConfirmDeparture",
        "setflag FLAG_JOHTO_DEPARTURE_CONFIRMED",
        "PalletTown_Text_WorldCircuitGateDepartureConfirmed",
        "ELM: New Bark Lab receiving",
        "LYRA: I will meet you",
        "SILVER profile detected",
        "WorldLink Objective: Enter Johto",
        "No Hoenn travel route registered",
    ):
        if marker not in scripts:
            errors.append(f"Pallet scripts missing Johto departure marker: {marker}")

    return errors


def validate_design_data() -> list[str]:
    errors: list[str] = []
    kanto = load_yaml(KANTO)
    kanto_messages = load_yaml(KANTO_WORLDLINK)
    rivals = load_yaml(RIVAL_PROGRESSION)
    regions = load_yaml(REGION_PROGRESSION)

    if not JOHTO_CHAPTER.exists():
        errors.append("missing johto_chapter.yaml")
    else:
        johto = load_yaml(JOHTO_CHAPTER)
        chapter = johto.get("chapter", {})
        if chapter.get("id") != "johto":
            errors.append("johto_chapter.yaml must define chapter id johto")
        if chapter.get("target_hours") != [12, 16]:
            errors.append("johto target hours must be [12, 16]")
        act1 = next((act for act in johto.get("acts", []) if act.get("id") == "act_1_new_bark_to_violet"), {})
        for event_id in (
            "new_bark_worldlink_arrival",
            "elm_lab_receiving_signal",
            "lyra_friendly_rival_join",
            "silver_profile_detected_no_theft_yet",
            "rocket_cherrygrove_remnant_tease",
            "gold_dust_tower_records_tease",
        ):
            if event_id not in act1.get("required_events", []):
                errors.append(f"Johto act 1 missing event: {event_id}")

    if not JOHTO_WORLDLINK.exists():
        errors.append("missing johto_worldlink_messages.yaml")
    else:
        message_ids = {message.get("id") for message in load_yaml(JOHTO_WORLDLINK).get("messages", [])}
        for message_id in (
            "WL_JOHTO_ARRIVAL_OBJECTIVE",
            "WL_JOHTO_ELM_LAB_SIGNAL",
            "WL_JOHTO_SILVER_PROFILE_TEASE",
        ):
            if message_id not in message_ids:
                errors.append(f"Johto WorldLink missing id: {message_id}")

    act7 = next((act for act in kanto.get("acts", []) if act.get("id") == "act_7_indigo"), {})
    for event_id in (
        "johto_departure_confirmed",
        "elm_lab_signal_opened",
        "silver_profile_tease_before_new_bark",
    ):
        if event_id not in act7.get("required_events", []):
            errors.append(f"Kanto act 7 missing departure event: {event_id}")

    kanto_message_ids = {message.get("id") for message in kanto_messages.get("messages", [])}
    if "WL_KANTO_JOHTO_DEPARTURE_CONFIRMED" not in kanto_message_ids:
        errors.append("Kanto WorldLink missing departure confirmed id")

    band = rivals.get("progression_bands", {}).get("johto_departure_objective", {})
    if band.get("companions", {}).get("red", {}).get("event") != "red_commits_to_early_johto_support":
        errors.append("Rival progression must keep Red committed to early Johto support")
    if band.get("rivals", {}).get("silver", {}).get("event") != "profile_detected_no_theft_yet":
        errors.append("Rival progression must tease Silver without starting the theft yet")

    unlock_order = regions.get("worldlink_region_progression", {}).get("unlock_order", [])
    hoenn = next((entry for entry in unlock_order if entry.get("region") == "hoenn"), {})
    if hoenn.get("unlock_state") != "locked":
        errors.append("Hoenn must remain locked during Johto departure")
    transition = regions.get("worldlink_region_progression", {}).get("current_transition_state", {})
    if transition.get("active_region") != "johto":
        errors.append("current transition state must mark Johto as active")
    if transition.get("next_required_story_node") not in {"new_bark_worldlink_arrival", "elm_lab_first_visit", "route_29_first_steps", "cherrygrove_first_arrival", "route_30_first_steps", "mr_pokemon_house_first_visit", "violet_city_first_arrival", "sprout_tower_first_floor", "sprout_tower_upper_floor", "falkner_gym_battle", "route_32_union_cave_road", "union_cave_first_entry", "azalea_first_arrival", "slowpoke_well_first_entry", "bugsy_gym_challenge", "ilex_forest_first_entry"}:
        errors.append("current transition state must point to New Bark arrival or later Johto follow-up")

    return errors


def validate_build_notes() -> list[str]:
    if not BUILD_NOTES.exists():
        return ["missing build notes file"]
    notes = read(BUILD_NOTES)
    errors: list[str] = []
    for marker in (
        "0040-johto-departure-objective.patch",
        "validate_johto_departure_objective.py",
        "Johto departure objective",
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
        print("Johto departure objective validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Johto departure objective validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
