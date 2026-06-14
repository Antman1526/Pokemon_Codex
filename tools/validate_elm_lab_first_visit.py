#!/usr/bin/env python3
"""Validate the first playable Elm Lab visit slice."""

from __future__ import annotations

from pathlib import Path

try:
    import yaml
except ImportError as exc:
    raise SystemExit("PyYAML is required: python3 -m pip install PyYAML") from exc


ROOT = Path(__file__).resolve().parents[1]
ENGINE = ROOT / "engine" / "pokeemerald-expansion"
PATCH = ROOT / "patches" / "engine" / "0042-elm-lab-first-visit.patch"
SPEC = ROOT / "docs" / "superpowers" / "specs" / "2026-06-14-elm-lab-first-visit-design.md"
PLAN = ROOT / "docs" / "superpowers" / "plans" / "2026-06-14-elm-lab-first-visit.md"
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
        errors.append("missing patch file: 0042-elm-lab-first-visit.patch")
    elif PATCH.stat().st_size == 0:
        errors.append("empty patch file: 0042-elm-lab-first-visit.patch")
    else:
        patch = read(PATCH)
        for marker in (
            "MAP_NEW_BARK_TOWN_ELM_LAB",
            "NewBarkTown_ElmLab_Frlg",
            "FLAG_ELM_LAB_FIRST_VISIT_REACHED",
            "NewBarkTown_ElmLab_Frlg_Text_ElmFirstVisit",
            "Route 29 is the next required road",
            "Silver's signal crossed Route 29",
        ):
            if marker not in patch:
                errors.append(f"patch 0042 missing marker: {marker}")

    for doc_path, doc_name, markers in (
        (
            SPEC,
            "Elm Lab first visit spec",
            ("first Johto interior", "Route 29", "Red and Lyra"),
        ),
        (
            PLAN,
            "Elm Lab first visit plan",
            ("Add failing validator", "Add Elm Lab map", "Build the ROM"),
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
    new_bark_scripts = read(ENGINE / "data" / "maps" / "NewBarkTown_Frlg" / "scripts.inc")
    lab_map_path = ENGINE / "data" / "maps" / "NewBarkTown_ElmLab_Frlg" / "map.json"
    lab_scripts_path = ENGINE / "data" / "maps" / "NewBarkTown_ElmLab_Frlg" / "scripts.inc"

    if "#define FLAG_ELM_LAB_FIRST_VISIT_REACHED   0x025" not in flags:
        errors.append("flags_frlg.h missing FLAG_ELM_LAB_FIRST_VISIT_REACHED at 0x025")
    if '"NewBarkTown_ElmLab_Frlg"' not in map_groups:
        errors.append("map_groups.json missing NewBarkTown_ElmLab_Frlg")
    for marker in (
        '"dest_map": "MAP_NEW_BARK_TOWN_ELM_LAB"',
        "NewBarkTown_Frlg_Text_ElmLabDoor",
        "Elm Lab",
    ):
        if marker not in new_bark_map + new_bark_scripts:
            errors.append(f"New Bark town missing Elm Lab marker: {marker}")

    if not lab_map_path.exists():
        errors.append("missing NewBarkTown_ElmLab_Frlg map.json")
    else:
        lab_map = read(lab_map_path)
        for marker in (
            '"id": "MAP_NEW_BARK_TOWN_ELM_LAB"',
            '"region": "REGION_JOHTO"',
            '"layout": "LAYOUT_PALLET_TOWN_PROFESSOR_OAKS_LAB"',
            '"dest_map": "MAP_NEW_BARK_TOWN"',
            "NewBarkTown_ElmLab_Frlg_EventScript_ElmFirstVisit",
            "NewBarkTown_ElmLab_Frlg_EventScript_RedLabSupport",
            "NewBarkTown_ElmLab_Frlg_EventScript_LyraLabGuide",
        ):
            if marker not in lab_map:
                errors.append(f"Elm Lab map.json missing marker: {marker}")

    if not lab_scripts_path.exists():
        errors.append("missing NewBarkTown_ElmLab_Frlg scripts.inc")
    else:
        lab_scripts = read(lab_scripts_path)
        for marker in (
            "NewBarkTown_ElmLab_Frlg_MapScripts",
            "FLAG_ELM_LAB_FIRST_VISIT_REACHED",
            "ELM: Welcome to my lab",
            "Route 29 is the next required road",
            "RED: I will walk the first stretch",
            "LYRA: I know the Cherrygrove guide",
            "Silver's signal crossed Route 29",
            "Hoenn remains locked",
        ):
            if marker not in lab_scripts:
                errors.append(f"Elm Lab scripts missing marker: {marker}")

    return errors


def validate_design_data() -> list[str]:
    errors: list[str] = []
    johto = load_yaml(JOHTO_CHAPTER)
    messages = load_yaml(JOHTO_WORLDLINK)
    regions = load_yaml(REGION_PROGRESSION)
    rivals = load_yaml(RIVAL_PROGRESSION)

    act1 = next((act for act in johto.get("acts", []) if act.get("id") == "act_1_new_bark_to_violet"), {})
    for event_id in (
        "elm_lab_first_visit",
        "elm_habitat_checklist",
        "red_route29_support_confirmed",
        "lyra_cherrygrove_guide_confirmed",
        "silver_route29_shadow",
    ):
        if event_id not in act1.get("required_events", []):
            errors.append(f"Johto act 1 missing Elm Lab event: {event_id}")
    for unlock_id in ("elm_lab_live_map", "route_29_story_gate", "johto_habitat_checklist"):
        if unlock_id not in act1.get("unlocks", []):
            errors.append(f"Johto act 1 missing Elm Lab unlock: {unlock_id}")

    message_ids = {message.get("id") for message in messages.get("messages", [])}
    for message_id in (
        "WL_JOHTO_ELM_LAB_FIRST_VISIT",
        "WL_JOHTO_ROUTE29_OBJECTIVE",
        "WL_JOHTO_SILVER_ROUTE29_SHADOW",
    ):
        if message_id not in message_ids:
            errors.append(f"Johto WorldLink missing id: {message_id}")

    transition = regions.get("worldlink_region_progression", {}).get("current_transition_state", {})
    if transition.get("next_required_story_node") not in {"route_29_first_steps", "cherrygrove_first_arrival", "route_30_first_steps", "mr_pokemon_house_first_visit", "violet_city_first_arrival", "sprout_tower_first_floor", "sprout_tower_upper_floor", "falkner_gym_battle", "route_32_union_cave_road", "union_cave_first_entry", "azalea_first_arrival"}:
        errors.append("current transition state must advance next node to Route 29 or later Cherrygrove follow-up")
    if transition.get("current_safe_hub") not in {"elm_lab", "cherrygrove_city", "mr_pokemon_house", "violet_city", "sprout_tower_1f", "sprout_tower_upper", "violet_gym", "route_32", "union_cave"}:
        errors.append("current transition state must record Elm Lab or a later Johto safe hub")
    if transition.get("hard_lock_next_region") != "hoenn":
        errors.append("Hoenn must remain the hard-locked next region")

    band = rivals.get("progression_bands", {}).get("johto_new_bark_elm_lab", {})
    if band.get("companions", {}).get("red", {}).get("event") != "route29_support_confirmed":
        errors.append("Rival progression must confirm Red's Route 29 support")
    if band.get("rivals", {}).get("silver", {}).get("event") != "route29_shadow_before_contact":
        errors.append("Rival progression must keep Silver as a Route 29 shadow before contact")

    return errors


def validate_build_notes() -> list[str]:
    if not BUILD_NOTES.exists():
        return ["missing build notes file"]
    notes = read(BUILD_NOTES)
    errors: list[str] = []
    for marker in (
        "0042-elm-lab-first-visit.patch",
        "validate_elm_lab_first_visit.py",
        "Elm Lab first visit",
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
        print("Elm Lab first visit validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Elm Lab first visit validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
