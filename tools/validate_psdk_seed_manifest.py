#!/usr/bin/env python3
"""Validate the PSDK import seed manifest against the current reference data."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import yaml


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
    "rival_worldlink_registry",
    "gameplay_systems_registry",
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
REQUIRED_COMPANIONS = ["red", "ash", "misty", "brock", "blue", "may", "bill", "sabrina"]
REQUIRED_RIVALS = [
    "blue",
    "ava",
    "dax",
    "silver",
    "hoenn_researcher",
    "sinnoh_researcher",
    "n",
    "kalos_rival",
    "marnie",
    "nemona",
]
REQUIRED_WORLDLINK_CATEGORIES = {
    "rival_badge",
    "rival_capture",
    "rival_rare_capture",
    "rival_loss",
    "rival_request",
    "rival_region_entry",
    "villain_alert",
    "legendary_anomaly",
}
REQUIRED_BATTLE_MECHANICS = {
    "physical_special_split",
    "fairy_type",
    "modern_move_categories",
    "modern_abilities_through_gen_9",
    "modern_moves_through_gen_9",
    "expanded_reusable_tm_list",
    "held_items",
    "ability_capsule",
    "ability_patch",
    "smarter_battle_ai_profiles",
}
REQUIRED_QOL_SYSTEMS = {
    "infinite_repel_toggle",
    "portable_pc",
    "field_healing",
    "skip_text",
    "fast_battle_animation_toggle",
    "level_caps",
    "infinite_rare_candies_after_first_badge",
    "trainer_rematches",
    "adjusted_trade_evolutions",
    "no_hm_slaves",
    "built_in_nuzlocke_tools",
    "difficulty_options",
}


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def read_yaml(path: Path):
    with path.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle)


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
        for extra_path in entry.get("extra_source_paths", []):
            if not (ROOT / extra_path).exists():
                errors.append(f"manifest extra_source_path does not exist: {extra_path}")
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
        errors.append("companion import required_companions must preserve the core companion cast and Saffron support ally")
    if data.get("primary_companion") != "red":
        errors.append("companion source primary_companion must be red")
    if companion_ids != REQUIRED_COMPANIONS:
        errors.append("companion source must preserve Red, Ash, Misty, Brock, Blue, May, Bill, and Sabrina")

    rules = set(entry.get("preserve_rules", []))
    for rule in ("red_is_primary_full_game_companion", "sabrina_supports_saffron_psychic_and_moonlight_residue_arcs", "companions_help_in_story_and_tag_battles_but_not_gym_battles"):
        if rule not in rules:
            errors.append(f"companion import preserve_rules missing {rule}")

    generated_ids = [companion.get("companion_id") for companion in generated.get("companions", [])]
    if generated.get("seed_type") != "psdk_core_companion_registry":
        errors.append("generated companion seed must use seed_type psdk_core_companion_registry")
    if generated.get("primary_companion") != "red":
        errors.append("generated companion seed primary_companion must be red")
    if generated_ids != REQUIRED_COMPANIONS:
        errors.append("generated companion seed must preserve the core companion cast and Saffron support ally")
    for companion in generated.get("companions", []):
        if companion.get("gym_battle_partner") is not False:
            errors.append(f"{companion.get('companion_id')} must not be a gym battle partner")
        if companion.get("companion_id") in {"bill", "sabrina"} and companion.get("tag_battle_eligible") is not False:
            errors.append(f"{companion.get('companion_id')} must remain a non-tag-battle support companion")

    return errors


def validate_rival_worldlink_import(entry: dict) -> list[str]:
    errors: list[str] = []
    data = read_yaml(source_path(entry))
    notifications = read_yaml(ROOT / "data_design" / "worldlink_notifications.yaml")
    schema = read_yaml(ROOT / "data_design" / "worldlink_schema.yaml")
    generated = read_json(target_path(entry)) if target_path(entry).exists() else {}
    rivals = data.get("rivals", [])
    rival_ids = [rival.get("rival_id") for rival in rivals]

    if entry.get("required_rival_count") != 10:
        errors.append("rival import required_rival_count must be 10")
    if entry.get("starting_rivals") != ["blue", "ava", "dax"]:
        errors.append("rival import starting_rivals must be blue, ava, dax")
    if entry.get("signature_rival") != "blue":
        errors.append("rival import signature_rival must be blue")
    if rival_ids != REQUIRED_RIVALS:
        errors.append("rival source must preserve all 10 rivals in expected order")
    for rival_id in ("blue", "ava", "dax"):
        rival = next((item for item in rivals if item.get("rival_id") == rival_id), {})
        if rival.get("starting_status") != "starts_with_player":
            errors.append(f"{rival_id} must start with the player")
    if set(entry.get("required_notification_categories", [])) != REQUIRED_WORLDLINK_CATEGORIES:
        errors.append("rival import required_notification_categories must cover core WorldLink rival alerts")
    for category_id in REQUIRED_WORLDLINK_CATEGORIES:
        if category_id not in notifications.get("categories", {}):
            errors.append(f"worldlink notifications missing category {category_id}")

    worldlink = schema.get("worldlink", {})
    if worldlink.get("default_notification_mode") != "major_only":
        errors.append("WorldLink default notification mode must be major_only")
    pause_and_digest = set(schema.get("delivery_rules", {}).get("pause_and_digest", []))
    for paused_area in ("cave", "villain_hideout", "ruins", "tower", "story_dungeon"):
        if paused_area not in pause_and_digest:
            errors.append(f"WorldLink pause_and_digest missing {paused_area}")

    rules = set(entry.get("preserve_rules", []))
    for rule in (
        "ten_rivals_travel_the_same_world_path",
        "worldlink_pauses_during_caves_dungeons_hideouts_and_boss_events",
        "rival_notifications_respect_major_only_default",
    ):
        if rule not in rules:
            errors.append(f"rival import preserve_rules missing {rule}")

    generated_ids = [rival.get("rival_id") for rival in generated.get("rivals", [])]
    if generated.get("seed_type") != "psdk_rival_worldlink_registry":
        errors.append("generated rival seed must use seed_type psdk_rival_worldlink_registry")
    if generated_ids != REQUIRED_RIVALS:
        errors.append("generated rival seed must preserve all 10 rivals")
    if generated.get("starting_rivals") != ["blue", "ava", "dax"]:
        errors.append("generated rival seed must preserve the three Kanto starting rivals")
    if generated.get("signature_rival") != "blue":
        errors.append("generated rival seed must keep Blue as signature rival")
    generated_categories = set(generated.get("required_notification_categories", {}))
    if generated_categories != REQUIRED_WORLDLINK_CATEGORIES:
        errors.append("generated rival seed must preserve required WorldLink categories")
    generated_settings = generated.get("worldlink_settings", {})
    if generated_settings.get("default_notification_mode") != "major_only":
        errors.append("generated WorldLink settings must default to major_only")
    generated_pause = set(generated_settings.get("delivery_rules", {}).get("pause_and_digest", []))
    if "cave" not in generated_pause or "villain_hideout" not in generated_pause:
        errors.append("generated WorldLink settings must pause in caves and villain hideouts")
    if len(generated.get("opening_feed", [])) < 4:
        errors.append("generated rival seed must include opening WorldLink feed entries")

    return errors


def validate_gameplay_systems_import(entry: dict) -> list[str]:
    errors: list[str] = []
    data = read_yaml(source_path(entry))
    generated = read_json(target_path(entry)) if target_path(entry).exists() else {}

    if set(entry.get("required_battle_mechanics", [])) != REQUIRED_BATTLE_MECHANICS:
        errors.append("gameplay import required_battle_mechanics must match core battle system commitments")
    if set(entry.get("required_qol_systems", [])) != REQUIRED_QOL_SYSTEMS:
        errors.append("gameplay import required_qol_systems must match core QoL commitments")

    battle_required = set(data.get("battle_mechanics", {}).get("required", []))
    if not REQUIRED_BATTLE_MECHANICS.issubset(battle_required):
        errors.append("gameplay source missing required battle mechanics")
    qol_required = set(data.get("qol_systems", {}).get("must_have", []))
    if not REQUIRED_QOL_SYSTEMS.issubset(qol_required):
        errors.append("gameplay source missing required QoL systems")

    gimmicks = data.get("battle_mechanics", {}).get("gimmick_gating", {})
    if gimmicks.get("dynamax_gigantamax", {}).get("first_preview") != "after_hoenn":
        errors.append("gameplay source must gate Dynamax/Gigantamax preview until after Hoenn")
    if gimmicks.get("terastallization", {}).get("first_preview") != "after_hoenn":
        errors.append("gameplay source must gate Terastallization preview until after Hoenn")

    availability = data.get("pokedex_and_availability", {})
    if availability.get("all_base_species_before_final_boss") is not True:
        errors.append("gameplay source must make all base species available before final boss")
    if availability.get("postgame_required_for_base_species") is not False:
        errors.append("gameplay source must not require postgame for base species")
    if availability.get("species_scope") != "through_generation_9":
        errors.append("gameplay source species_scope must be through_generation_9")
    for channel in ("wild_grass", "time_of_day", "weather", "fishing", "breeding", "raid_dens", "ultra_wormholes", "area_zero_anomalies", "legendary_trials"):
        if channel not in availability.get("availability_channels", []):
            errors.append(f"gameplay availability missing channel {channel}")

    field_tools = data.get("field_tools", {})
    for tool in ("trail_cutter", "tide_rider", "sky_pass", "rock_gauntlet", "cave_lantern", "climb_gear", "waterfall_gear", "dive_gear", "dig_kit"):
        if tool not in field_tools.get("hm_replacements", {}):
            errors.append(f"gameplay field tools missing {tool}")

    if generated.get("seed_type") != "psdk_gameplay_systems_registry":
        errors.append("generated gameplay seed must use seed_type psdk_gameplay_systems_registry")
    generated_battle = set(generated.get("battle_mechanics", {}).get("required", []))
    if not REQUIRED_BATTLE_MECHANICS.issubset(generated_battle):
        errors.append("generated gameplay seed missing required battle mechanics")
    generated_qol = set(generated.get("qol_systems", {}).get("must_have", []))
    if not REQUIRED_QOL_SYSTEMS.issubset(generated_qol):
        errors.append("generated gameplay seed missing required QoL systems")
    generated_availability = generated.get("pokedex_and_availability", {})
    if generated_availability.get("all_base_species_before_final_boss") is not True:
        errors.append("generated gameplay seed must preserve all-base-species-before-final-boss")
    if generated.get("pokemon_center_and_mart", {}).get("mart_rules", {}).get("starting_money") != 100000:
        errors.append("generated gameplay seed must preserve starting money 100000")

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
    rival_entry = imports.get("rival_worldlink_registry")
    if rival_entry:
        errors.extend(validate_rival_worldlink_import(rival_entry))
    gameplay_entry = imports.get("gameplay_systems_registry")
    if gameplay_entry:
        errors.extend(validate_gameplay_systems_import(gameplay_entry))

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
