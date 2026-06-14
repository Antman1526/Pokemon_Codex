#!/usr/bin/env python3
"""Validate the first playable Mr. Pokemon house slice."""

from __future__ import annotations

from pathlib import Path

try:
    import yaml
except ImportError as exc:
    raise SystemExit("PyYAML is required: python3 -m pip install PyYAML") from exc


ROOT = Path(__file__).resolve().parents[1]
ENGINE = ROOT / "engine" / "pokeemerald-expansion"
PATCH = ROOT / "patches" / "engine" / "0046-mr-pokemon-house-first-visit.patch"
SPEC = ROOT / "docs" / "superpowers" / "specs" / "2026-06-14-mr-pokemon-house-first-visit-design.md"
PLAN = ROOT / "docs" / "superpowers" / "plans" / "2026-06-14-mr-pokemon-house-first-visit.md"
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
        errors.append("missing patch file: 0046-mr-pokemon-house-first-visit.patch")
    elif PATCH.stat().st_size == 0:
        errors.append("empty patch file: 0046-mr-pokemon-house-first-visit.patch")
    else:
        patch = read(PATCH)
        for marker in (
            "MAP_MR_POKEMONS_HOUSE",
            "MrPokemonsHouse_Frlg",
            "FLAG_MR_POKEMON_HOUSE_FIRST_VISIT_REACHED",
            "MrPokemonsHouse_Frlg_Text_MrPokemonNexusEgg",
            "MrPokemonsHouse_Frlg_Text_OakOldStoryNewMap",
            "MrPokemonsHouse_Frlg_Text_AvaResearchFeed",
            "Nexus Egg",
            "WorldLink: Violet City next",
        ):
            if marker not in patch:
                errors.append(f"patch 0046 missing marker: {marker}")

    for doc_path, doc_name, markers in (
        (
            SPEC,
            "Mr. Pokemon house spec",
            ("Nexus Egg", "Oak physically appears", "Ava remote feed"),
        ),
        (
            PLAN,
            "Mr. Pokemon house plan",
            ("Add failing validator", "Add Mr. Pokemon house map", "Build the ROM"),
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
    route30_map = read(ENGINE / "data" / "maps" / "Route30_Frlg" / "map.json")
    house_map_path = ENGINE / "data" / "maps" / "MrPokemonsHouse_Frlg" / "map.json"
    house_scripts_path = ENGINE / "data" / "maps" / "MrPokemonsHouse_Frlg" / "scripts.inc"

    if "#define FLAG_MR_POKEMON_HOUSE_FIRST_VISIT_REACHED   0x0B0" not in flags:
        errors.append("flags_frlg.h missing FLAG_MR_POKEMON_HOUSE_FIRST_VISIT_REACHED at 0x0B0")
    if '"MrPokemonsHouse_Frlg"' not in map_groups:
        errors.append("map_groups.json missing MrPokemonsHouse_Frlg")
    if '"dest_map": "MAP_MR_POKEMONS_HOUSE"' not in route30_map:
        errors.append("Route 30 map missing warp to MAP_MR_POKEMONS_HOUSE")

    if not house_map_path.exists():
        errors.append("missing MrPokemonsHouse_Frlg map.json")
    else:
        house_map = read(house_map_path)
        for marker in (
            '"id": "MAP_MR_POKEMONS_HOUSE"',
            '"region": "REGION_JOHTO"',
            '"layout": "LAYOUT_ROUTE25_SEA_COTTAGE"',
            '"dest_map": "MAP_ROUTE30"',
            "MrPokemonsHouse_Frlg_EventScript_MrPokemonNexusEgg",
            "MrPokemonsHouse_Frlg_EventScript_OakOldStoryNewMap",
            "MrPokemonsHouse_Frlg_EventScript_AvaResearchFeed",
            "MrPokemonsHouse_Frlg_EventScript_ElmVioletHandoff",
        ):
            if marker not in house_map:
                errors.append(f"Mr. Pokemon map.json missing marker: {marker}")

    if not house_scripts_path.exists():
        errors.append("missing MrPokemonsHouse_Frlg scripts.inc")
    else:
        scripts = read(house_scripts_path)
        for marker in (
            "MrPokemonsHouse_Frlg_MapScripts",
            "FLAG_MR_POKEMON_HOUSE_FIRST_VISIT_REACHED",
            "MR. POKEMON: This is not a normal egg",
            "Nexus Egg",
            "OAK: The old story is still true",
            "AVA: Remote feed stable",
            "ELM: Violet City next",
            "WorldLink: Violet City next",
            "Hoenn remains locked",
        ):
            if marker not in scripts:
                errors.append(f"Mr. Pokemon scripts missing marker: {marker}")

    return errors


def validate_design_data() -> list[str]:
    errors: list[str] = []
    johto = load_yaml(JOHTO_CHAPTER)
    messages = load_yaml(JOHTO_WORLDLINK)
    regions = load_yaml(REGION_PROGRESSION)
    rivals = load_yaml(RIVAL_PROGRESSION)

    act1 = next((act for act in johto.get("acts", []) if act.get("id") == "act_1_new_bark_to_violet"), {})
    if "mr_pokemon_house" not in act1.get("required_maps", []):
        errors.append("Johto act 1 missing required map: mr_pokemon_house")
    for event_id in (
        "mr_pokemon_house_first_visit",
        "mr_pokemon_nexus_egg_reveal",
        "oak_old_story_new_map",
        "ava_remote_egg_research_feed",
        "elm_violet_city_handoff",
        "sprout_tower_records_edited",
    ):
        if event_id not in act1.get("required_events", []):
            errors.append(f"Johto act 1 missing Mr. Pokemon event: {event_id}")
    for unlock_id in (
        "mr_pokemon_house_live_map",
        "nexus_egg_story_key_item",
        "violet_city_story_gate",
        "sprout_tower_records_warning",
    ):
        if unlock_id not in act1.get("unlocks", []):
            errors.append(f"Johto act 1 missing Mr. Pokemon unlock: {unlock_id}")

    message_ids = {message.get("id") for message in messages.get("messages", [])}
    for message_id in (
        "WL_JOHTO_MR_POKEMON_HOUSE_ARRIVAL",
        "WL_JOHTO_NEXUS_EGG_REVEAL",
        "WL_JOHTO_OAK_AVA_RESEARCH_SYNC",
        "WL_JOHTO_VIOLET_CITY_NEXT",
    ):
        if message_id not in message_ids:
            errors.append(f"Johto WorldLink missing id: {message_id}")

    transition = regions.get("worldlink_region_progression", {}).get("current_transition_state", {})
    if transition.get("current_safe_hub") != "mr_pokemon_house":
        errors.append("current transition state must record Mr. Pokemon house as current safe hub")
    if transition.get("next_required_story_node") != "violet_city_first_arrival":
        errors.append("current transition state must advance next node to violet_city_first_arrival")
    if transition.get("hard_lock_next_region") != "hoenn":
        errors.append("Hoenn must remain the hard-locked next region")

    band = rivals.get("progression_bands", {}).get("johto_mr_pokemon_house_first_visit", {})
    if band.get("companions", {}).get("oak", {}).get("event") != "old_story_new_map":
        errors.append("Rival progression must set Oak as old-story/new-map contact")
    if band.get("rivals", {}).get("ava", {}).get("event") != "remote_nexus_egg_research":
        errors.append("Rival progression must set Ava as remote Nexus Egg research")

    return errors


def validate_build_notes() -> list[str]:
    if not BUILD_NOTES.exists():
        return ["missing build notes file"]
    notes = read(BUILD_NOTES)
    errors: list[str] = []
    for marker in (
        "0046-mr-pokemon-house-first-visit.patch",
        "validate_mr_pokemon_house_first_visit.py",
        "Mr. Pokemon house first visit",
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
        print("Mr. Pokemon house first visit validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Mr. Pokemon house first visit validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
