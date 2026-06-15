#!/usr/bin/env python3
"""Validate the PSDK import seed manifest against the current reference data."""

from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "psdk" / "nexus-red" / "project" / "Data" / "nexus_red_seed" / "import_manifest.json"

OFFICIAL_STARTERS = [
    "Bulbasaur", "Charmander", "Squirtle",
    "Chikorita", "Cyndaquil", "Totodile",
    "Treecko", "Torchic", "Mudkip",
    "Turtwig", "Chimchar", "Piplup",
    "Snivy", "Tepig", "Oshawott",
    "Chespin", "Fennekin", "Froakie",
    "Rowlet", "Litten", "Popplio",
    "Grookey", "Scorbunny", "Sobble",
    "Sprigatito", "Fuecoco", "Quaxly",
]
SPECIAL_STARTERS = [
    "Eevee", "Pikachu", "Dratini", "Abra", "Gastly", "Larvitar",
    "Sandile", "Kubfu", "Staryu", "Shroomish", "Rockruff", "Ralts",
]
REQUIRED_SPECIES = OFFICIAL_STARTERS + SPECIAL_STARTERS
REQUIRED_IMPORT_IDS = {
    "oak_lab_39_first_partner_selector",
    "routes_1_to_3_migration_encounters",
    "world_region_progression_spine",
    "custom_faction_war_registry",
    "core_companion_registry",
}
REQUIRED_ROUTES = {"route_1", "route_2", "route_3"}
REQUIRED_REGIONS = [
    "kanto",
    "johto",
    "hoenn",
    "sinnoh_hisui",
    "unova",
    "kalos",
    "alola",
    "galar",
    "paldea",
    "nexus_island",
]
REQUIRED_FACTIONS = [
    "team_rocket",
    "team_magma",
    "team_aqua",
    "team_phoenix",
    "team_moonlight",
    "team_gold_dust",
    "team_gas",
    "team_clover",
    "nexus_order",
]
DROPPED_ACTIVE_CANONICAL_FACTIONS = {
    "team_galactic",
    "team_plasma",
    "team_flare",
    "team_skull",
    "macro_cosmos",
    "team_star",
}
REQUIRED_COMPANIONS = ["red", "ash", "misty", "brock", "blue", "may", "bill"]


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def source_path(manifest_entry: dict) -> Path:
    return ROOT / manifest_entry.get("source_path", "")


def target_path(manifest_entry: dict) -> Path:
    return ROOT / "psdk" / "nexus-red" / manifest_entry.get("psdk_target", "")


def validate_manifest_shape(manifest: dict) -> list[str]:
    errors: list[str] = []
    if manifest.get("schema_version") != 1:
        errors.append("manifest schema_version must be 1")
    if manifest.get("target_engine") != "pokemon_studio_psdk":
        errors.append("manifest target_engine must be pokemon_studio_psdk")
    if manifest.get("source_reference_engine") != "godot_4_reference":
        errors.append("manifest source_reference_engine must be godot_4_reference")
    if not (ROOT / manifest.get("design_contract", "")).exists():
        errors.append("manifest design_contract must point to an existing file")

    imports = manifest.get("imports", [])
    ids = {entry.get("id") for entry in imports}
    if ids != REQUIRED_IMPORT_IDS:
        errors.append("manifest imports must contain exactly: " + ", ".join(sorted(REQUIRED_IMPORT_IDS)))
    for entry in imports:
        path = source_path(entry)
        if not path.exists():
            errors.append(f"manifest source_path does not exist: {entry.get('source_path')}")
        if not entry.get("psdk_target", "").startswith("project/Data/nexus_red_seed/generated/"):
            errors.append(f"{entry.get('id')} must target generated seed data under project/Data/nexus_red_seed/generated/")
        if not target_path(entry).exists():
            errors.append(f"manifest psdk_target does not exist: {entry.get('psdk_target')}")
        if "psdk" not in entry.get("psdk_system", "") and "pokemon_studio" not in entry.get("psdk_system", ""):
            errors.append(f"{entry.get('id')} must describe a PSDK/Studio import system")

    for flag in ("red_companion_intro_seen", "starter_chosen", "worldlink_stub_unlocked"):
        if flag not in manifest.get("first_psdk_slice_flags", []):
            errors.append(f"first_psdk_slice_flags missing {flag}")
    for blocked in ("commercial_rom_assets", "ripped_assets", "psdk_binaries"):
        if blocked not in manifest.get("do_not_import", []):
            errors.append(f"do_not_import missing {blocked}")

    return errors


def validate_starter_import(entry: dict) -> list[str]:
    errors: list[str] = []
    data = read_json(source_path(entry))
    generated = read_json(target_path(entry)) if target_path(entry).exists() else {}
    starters = data.get("starters", [])
    species = [item.get("species") for item in starters]
    official = species[:27]
    special = species[27:]

    if entry.get("required_selectable_count") != 39:
        errors.append("starter import required_selectable_count must be 39")
    if entry.get("required_official_count") != 27:
        errors.append("starter import required_official_count must be 27")
    if entry.get("required_special_count") != 12:
        errors.append("starter import required_special_count must be 12")
    if species != REQUIRED_SPECIES:
        errors.append("starter source species order must match the 27 official + 12 special contract")
    if official != OFFICIAL_STARTERS:
        errors.append("official starter order drifted")
    if special != SPECIAL_STARTERS:
        errors.append("special starter order drifted")

    rules = set(entry.get("preserve_rules", []))
    for rule in ("blue_counter_pick_rules", "ava_priority_pool", "dax_priority_pool", "add_selected_species_to_party"):
        if rule not in rules:
            errors.append(f"starter import preserve_rules missing {rule}")
    for species_name in REQUIRED_SPECIES:
        if species_name not in data.get("blue_counter_rules", {}):
            errors.append(f"blue_counter_rules missing {species_name}")

    context = entry.get("story_context", {})
    if context.get("primary_companion") != "Red":
        errors.append("starter story_context must keep Red as primary companion")
    if context.get("protagonist") != "Antman":
        errors.append("starter story_context must keep Antman as protagonist")

    generated_species = [item.get("species") for item in generated.get("selectable_partners", [])]
    if generated.get("seed_type") != "psdk_oak_lab_first_partner_selector":
        errors.append("generated starter seed must use seed_type psdk_oak_lab_first_partner_selector")
    if generated_species != species:
        errors.append("generated starter seed species order must match source starter order")
    if generated.get("blue_counter_rules") != data.get("blue_counter_rules"):
        errors.append("generated starter seed blue_counter_rules must match source")
    if generated.get("story_context", {}).get("primary_companion") != "Red":
        errors.append("generated starter seed must keep Red as primary companion")

    return errors


def validate_encounter_import(entry: dict) -> list[str]:
    errors: list[str] = []
    data = read_json(source_path(entry))
    generated = read_json(target_path(entry)) if target_path(entry).exists() else {}
    encounters = data.get("encounters", [])
    species = [item.get("species") for item in encounters]
    routes = {item.get("route_id") for item in encounters}

    if entry.get("required_encounter_count") != 39:
        errors.append("encounter import required_encounter_count must be 39")
    if set(entry.get("required_routes", [])) != REQUIRED_ROUTES:
        errors.append("encounter import must require route_1, route_2, and route_3")
    if entry.get("level_cap_context") != "pre_brock":
        errors.append("encounter import level_cap_context must be pre_brock")
    if entry.get("allowed_level_range") != [4, 7]:
        errors.append("encounter import allowed_level_range must be [4, 7]")
    if sorted(species) != sorted(REQUIRED_SPECIES):
        errors.append("encounter source must contain all 39 first-partner species exactly once")
    if len(species) != len(set(species)):
        errors.append("encounter source must not duplicate species")
    if routes != REQUIRED_ROUTES:
        errors.append("encounter source must cover route_1, route_2, and route_3")

    route_targets = entry.get("route_targets", {})
    for route_id in REQUIRED_ROUTES:
        if route_id not in route_targets:
            errors.append(f"route_targets missing {route_id}")
        elif not route_targets[route_id].get("psdk_map_id", "").startswith("kanto_"):
            errors.append(f"{route_id} psdk_map_id must be a Kanto map id")

    route_counts = {route_id: 0 for route_id in REQUIRED_ROUTES}
    for encounter in encounters:
        route_id = encounter.get("route_id")
        route_counts[route_id] = route_counts.get(route_id, 0) + 1
        level = encounter.get("level")
        if not isinstance(level, int) or level < 4 or level > 7:
            errors.append(f"{encounter.get('species')} must stay in PSDK seed level band 4-7")
        if encounter.get("species") in {"Dratini", "Larvitar", "Kubfu"} and encounter.get("weight") != 1:
            errors.append(f"{encounter.get('species')} must keep rare weight 1 in the PSDK seed")
    for route_id, count in route_counts.items():
        if count != 13:
            errors.append(f"{route_id} must contain 13 migration encounters")

    rules = set(entry.get("preserve_rules", []))
    for rule in ("all_39_first_partner_species_catchable_before_brock", "local_kanto_wildlife_remains_common"):
        if rule not in rules:
            errors.append(f"encounter import preserve_rules missing {rule}")

    if generated.get("seed_type") != "psdk_routes_1_to_3_migration_encounters":
        errors.append("generated encounter seed must use seed_type psdk_routes_1_to_3_migration_encounters")
    generated_routes = generated.get("route_targets", {})
    generated_species: list[str] = []
    for route_id in REQUIRED_ROUTES:
        route_data = generated_routes.get(route_id, {})
        generated_species.extend(item.get("species") for item in route_data.get("encounters", []))
        if len(route_data.get("encounters", [])) != 13:
            errors.append(f"generated {route_id} must contain 13 migration encounters")
    if sorted(generated_species) != sorted(REQUIRED_SPECIES):
        errors.append("generated encounter seed must contain all 39 first-partner species")

    return errors


def validate_region_import(entry: dict) -> list[str]:
    errors: list[str] = []
    data = read_json(source_path(entry))
    generated = read_json(target_path(entry)) if target_path(entry).exists() else {}
    regions = sorted(data.get("regions", []), key=lambda item: item.get("order", 0))
    region_ids = [region.get("id") for region in regions]

    if entry.get("required_region_count") != 10:
        errors.append("region import required_region_count must be 10")
    if entry.get("required_order") != REQUIRED_REGIONS:
        errors.append("region import required_order must preserve the 9 regions plus Nexus Island")
    if region_ids != REQUIRED_REGIONS:
        errors.append("region source order must be Kanto through Nexus Island")
    if data.get("current_region") != "kanto":
        errors.append("region source current_region must start at kanto")
    if data.get("final_region") != "nexus_island":
        errors.append("region source final_region must be nexus_island")

    rules = set(entry.get("preserve_rules", []))
    for rule in ("one_region_unlocked_at_a_time", "nexus_island_is_full_final_region"):
        if rule not in rules:
            errors.append(f"region import preserve_rules missing {rule}")

    generated_ids = [region.get("region_id") for region in generated.get("region_unlocks", [])]
    if generated.get("seed_type") != "psdk_world_region_progression_spine":
        errors.append("generated region seed must use seed_type psdk_world_region_progression_spine")
    if generated_ids != REQUIRED_REGIONS:
        errors.append("generated region seed must preserve Kanto through Nexus Island order")
    for region in generated.get("region_unlocks", []):
        if region.get("worldlink_travel_mode") != "story_gated_single_region":
            errors.append(f"{region.get('region_id')} must use story_gated_single_region travel mode")

    return errors


def validate_faction_import(entry: dict) -> list[str]:
    errors: list[str] = []
    data = read_json(source_path(entry))
    generated = read_json(target_path(entry)) if target_path(entry).exists() else {}
    faction_ids = [faction.get("id") for faction in data.get("factions", [])]

    if entry.get("primary_antagonist") != "team_rocket":
        errors.append("faction import primary_antagonist must be team_rocket")
    if entry.get("hidden_meta_villain") != "nexus_order":
        errors.append("faction import hidden_meta_villain must be nexus_order")
    if entry.get("required_factions") != REQUIRED_FACTIONS:
        errors.append("faction import required_factions must match the custom faction war")
    if set(entry.get("dropped_active_canonical_factions", [])) != DROPPED_ACTIVE_CANONICAL_FACTIONS:
        errors.append("faction import must list all dropped active canonical factions")
    if faction_ids != REQUIRED_FACTIONS:
        errors.append("faction source must contain only the custom faction war registry in order")
    if data.get("primary_antagonist") != "team_rocket":
        errors.append("faction source primary_antagonist must be team_rocket")
    if data.get("hidden_meta_villain") != "nexus_order":
        errors.append("faction source hidden_meta_villain must be nexus_order")
    if DROPPED_ACTIVE_CANONICAL_FACTIONS.intersection(faction_ids):
        errors.append("canonical later villain teams must not be active factions")

    rules = set(entry.get("preserve_rules", []))
    for rule in ("giovanni_is_final_human_antagonist", "custom_faction_wars_replace_later_canonical_villain_teams"):
        if rule not in rules:
            errors.append(f"faction import preserve_rules missing {rule}")

    generated_ids = [faction.get("faction_id") for faction in generated.get("factions", [])]
    if generated.get("seed_type") != "psdk_custom_faction_war_registry":
        errors.append("generated faction seed must use seed_type psdk_custom_faction_war_registry")
    if generated_ids != REQUIRED_FACTIONS:
        errors.append("generated faction seed must preserve the custom faction list")
    if generated.get("primary_antagonist") != "team_rocket":
        errors.append("generated faction seed primary_antagonist must be team_rocket")
    if generated.get("hidden_meta_villain") != "nexus_order":
        errors.append("generated faction seed hidden_meta_villain must be nexus_order")
    if set(generated.get("dropped_active_canonical_factions", [])) != DROPPED_ACTIVE_CANONICAL_FACTIONS:
        errors.append("generated faction seed must preserve dropped active canonical factions")

    return errors


def validate_companion_import(entry: dict) -> list[str]:
    errors: list[str] = []
    data = read_json(source_path(entry))
    generated = read_json(target_path(entry)) if target_path(entry).exists() else {}
    companion_ids = [companion.get("id") for companion in data.get("companions", [])]

    if entry.get("primary_companion") != "red":
        errors.append("companion import primary_companion must be red")
    if entry.get("required_companions") != REQUIRED_COMPANIONS:
        errors.append("companion import required_companions must preserve the core companion cast")
    if data.get("primary_companion") != "red":
        errors.append("companion source primary_companion must be red")
    if companion_ids != REQUIRED_COMPANIONS:
        errors.append("companion source must preserve Red, Ash, Misty, Brock, Blue, May, Bill")

    rules = set(entry.get("preserve_rules", []))
    for rule in ("red_is_primary_full_game_companion", "companions_help_in_story_and_tag_battles_but_not_gym_battles"):
        if rule not in rules:
            errors.append(f"companion import preserve_rules missing {rule}")

    generated_ids = [companion.get("companion_id") for companion in generated.get("companions", [])]
    if generated.get("seed_type") != "psdk_core_companion_registry":
        errors.append("generated companion seed must use seed_type psdk_core_companion_registry")
    if generated.get("primary_companion") != "red":
        errors.append("generated companion seed primary_companion must be red")
    if generated_ids != REQUIRED_COMPANIONS:
        errors.append("generated companion seed must preserve the core companion cast")
    for companion in generated.get("companions", []):
        if companion.get("gym_battle_partner") is not False:
            errors.append(f"{companion.get('companion_id')} must not be a gym battle partner")

    return errors


def validate() -> list[str]:
    if not MANIFEST.exists():
        return [f"missing PSDK seed manifest: {rel(MANIFEST)}"]

    errors: list[str] = []
    manifest = read_json(MANIFEST)
    errors.extend(validate_manifest_shape(manifest))
    imports = {entry.get("id"): entry for entry in manifest.get("imports", [])}

    starter_entry = imports.get("oak_lab_39_first_partner_selector")
    if starter_entry:
        errors.extend(validate_starter_import(starter_entry))
    encounter_entry = imports.get("routes_1_to_3_migration_encounters")
    if encounter_entry:
        errors.extend(validate_encounter_import(encounter_entry))
    region_entry = imports.get("world_region_progression_spine")
    if region_entry:
        errors.extend(validate_region_import(region_entry))
    faction_entry = imports.get("custom_faction_war_registry")
    if faction_entry:
        errors.extend(validate_faction_import(faction_entry))
    companion_entry = imports.get("core_companion_registry")
    if companion_entry:
        errors.extend(validate_companion_import(companion_entry))

    return errors


def main() -> int:
    errors = validate()
    if errors:
        print("PSDK seed manifest validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print("PSDK seed manifest validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
