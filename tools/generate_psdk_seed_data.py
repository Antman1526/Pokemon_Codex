#!/usr/bin/env python3
"""Generate PSDK seed data from the current Nexus Red reference content."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "psdk" / "nexus-red" / "project" / "Data" / "nexus_red_seed" / "import_manifest.json"


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def read_yaml(path: Path):
    with path.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def write_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")


def manifest_imports(manifest: dict) -> dict[str, dict]:
    return {entry["id"]: entry for entry in manifest.get("imports", [])}


def build_starter_seed(entry: dict) -> dict:
    source = read_json(ROOT / entry["source_path"])
    starters = source["starters"]
    return {
        "schema_version": 1,
        "seed_type": "psdk_oak_lab_first_partner_selector",
        "source_import_id": entry["id"],
        "source_path": entry["source_path"],
        "story_context": entry["story_context"],
        "selection_rules": {
            "required_selectable_count": entry["required_selectable_count"],
            "required_official_count": entry["required_official_count"],
            "required_special_count": entry["required_special_count"],
            "preserve_rules": entry["preserve_rules"],
            "on_confirm": [
                "set_flag:starter_chosen",
                "add_selected_species_to_party",
                "assign_blue_counter_pick",
                "assign_ava_priority_pick",
                "assign_dax_priority_pick",
                "queue_worldlink_starter_notifications",
            ],
        },
        "selectable_partners": [
            {
                "slot": index + 1,
                "species": starter["species"],
                "origin_region": starter["origin_region"],
                "tags": starter.get("tags", []),
                "psdk_species_key": starter["species"].upper(),
            }
            for index, starter in enumerate(starters)
        ],
        "blue_counter_rules": source["blue_counter_rules"],
        "ava_priority_pool": source["ava_priority_pool"],
        "ava_fallback": source["ava_fallback"],
        "dax_priority_pool": source["dax_priority_pool"],
        "dax_fallback": source["dax_fallback"],
    }


def build_encounter_seed(entry: dict) -> dict:
    source = read_json(ROOT / entry["source_path"])
    grouped: dict[str, list[dict]] = {route_id: [] for route_id in entry["required_routes"]}
    for encounter in source["encounters"]:
        grouped.setdefault(encounter["route_id"], []).append(
            {
                "id": encounter["id"],
                "species": encounter["species"],
                "psdk_species_key": encounter["species"].upper(),
                "level": encounter["level"],
                "weight": encounter["weight"],
                "time": encounter["time"],
                "tags": encounter.get("tags", []),
            }
        )

    return {
        "schema_version": 1,
        "seed_type": "psdk_routes_1_to_3_migration_encounters",
        "source_import_id": entry["id"],
        "source_path": entry["source_path"],
        "level_cap_context": entry["level_cap_context"],
        "allowed_level_range": entry["allowed_level_range"],
        "preserve_rules": entry["preserve_rules"],
        "route_targets": {
            route_id: {
                **entry["route_targets"][route_id],
                "encounters": grouped.get(route_id, []),
            }
            for route_id in entry["required_routes"]
        },
    }


def build_region_seed(entry: dict) -> dict:
    source = read_json(ROOT / entry["source_path"])
    regions = sorted(source["regions"], key=lambda item: item["order"])
    return {
        "schema_version": 1,
        "seed_type": "psdk_world_region_progression_spine",
        "source_import_id": entry["id"],
        "source_path": entry["source_path"],
        "current_region": source["current_region"],
        "final_region": source["final_region"],
        "preserve_rules": entry["preserve_rules"],
        "region_unlocks": [
            {
                "order": region["order"],
                "region_id": region["id"],
                "display_name": region["display_name"],
                "theme": region["theme"],
                "unlock_mode": "main_story_progression",
                "worldlink_travel_mode": "story_gated_single_region",
            }
            for region in regions
        ],
    }


def build_faction_seed(entry: dict) -> dict:
    source = read_json(ROOT / entry["source_path"])
    return {
        "schema_version": 1,
        "seed_type": "psdk_custom_faction_war_registry",
        "source_import_id": entry["id"],
        "source_path": entry["source_path"],
        "primary_antagonist": source["primary_antagonist"],
        "hidden_meta_villain": source["hidden_meta_villain"],
        "dropped_active_canonical_factions": entry["dropped_active_canonical_factions"],
        "preserve_rules": entry["preserve_rules"],
        "factions": [
            {
                "faction_id": faction["id"],
                "display_name": faction["display_name"],
                "leader": faction["leader"],
                "role": faction["role"],
                "active_enemy_faction": True,
            }
            for faction in source["factions"]
        ],
    }


def build_companion_seed(entry: dict) -> dict:
    source = read_json(ROOT / entry["source_path"])
    return {
        "schema_version": 1,
        "seed_type": "psdk_core_companion_registry",
        "source_import_id": entry["id"],
        "source_path": entry["source_path"],
        "primary_companion": source["primary_companion"],
        "preserve_rules": entry["preserve_rules"],
        "companions": [
            {
                "companion_id": companion["id"],
                "display_name": companion["display_name"],
                "role": companion["role"],
                "active_from": companion["active_from"],
                "tag_battle_eligible": companion["id"] != "bill",
                "gym_battle_partner": False,
            }
            for companion in source["companions"]
        ],
    }


def build_rival_worldlink_seed(entry: dict) -> dict:
    rivals = read_yaml(ROOT / entry["source_path"])
    notifications = read_yaml(ROOT / "data_design" / "worldlink_notifications.yaml")
    schema = read_yaml(ROOT / "data_design" / "worldlink_schema.yaml")
    kanto_progression = read_yaml(ROOT / "data_design" / "rival_progression_kanto.yaml")
    opening_feed = read_json(ROOT / "native" / "nexus-red" / "content" / "worldlink" / "opening_feed.json")

    return {
        "schema_version": 1,
        "seed_type": "psdk_rival_worldlink_registry",
        "source_import_id": entry["id"],
        "source_path": entry["source_path"],
        "extra_source_paths": entry.get("extra_source_paths", []),
        "required_rival_count": entry["required_rival_count"],
        "starting_rivals": entry["starting_rivals"],
        "signature_rival": entry["signature_rival"],
        "preserve_rules": entry["preserve_rules"],
        "worldlink_settings": {
            "unlock_timing": schema["worldlink"]["unlock_timing"],
            "default_notification_mode": schema["worldlink"]["default_notification_mode"],
            "recent_message_capacity": schema["worldlink"]["target_recent_message_capacity"],
            "notification_modes": schema["notification_modes"],
            "delivery_rules": schema["delivery_rules"],
            "digest": schema["digest"],
        },
        "required_notification_categories": {
            category_id: notifications["categories"][category_id]
            for category_id in entry["required_notification_categories"]
        },
        "rivals": [
            {
                "rival_id": rival["rival_id"],
                "display_name": rival["display_name"],
                "origin_region": rival["origin_region"],
                "role": rival["role"],
                "starting_status": rival["starting_status"],
                "starter_policy": rival["starter_policy"],
                "personality": rival["personality"],
                "team_archetype": rival["team_archetype"],
                "relationship_defaults": rival["relationship_defaults"],
                "chapter_appearances": rival["chapter_appearances"],
                "notification_behavior": rival["notification_behavior"],
                "worldlink_visible": True,
            }
            for rival in rivals["rivals"]
        ],
        "kanto_progression_bands": kanto_progression["progression_bands"],
        "opening_feed": opening_feed["feed"],
    }


def build_gameplay_systems_seed(entry: dict) -> dict:
    source = read_yaml(ROOT / entry["source_path"])
    availability = read_yaml(ROOT / "data_design" / "availability_channels.yaml")
    boss_progression = read_yaml(ROOT / "data_design" / "boss_progression.yaml")
    activity_rewards = read_yaml(ROOT / "data_design" / "region_activity_rewards.yaml")
    return {
        "schema_version": 1,
        "seed_type": "psdk_gameplay_systems_registry",
        "source_import_id": entry["id"],
        "source_path": entry["source_path"],
        "extra_source_paths": entry.get("extra_source_paths", []),
        "system_profile": source["system_profile"],
        "battle_mechanics": source["battle_mechanics"],
        "qol_systems": source["qol_systems"],
        "difficulty_modes": source["difficulty_modes"],
        "field_tools": source["field_tools"],
        "encounter_world_systems": source["encounter_world_systems"],
        "pokedex_and_availability": source["pokedex_and_availability"],
        "pokemon_center_and_mart": source["pokemon_center_and_mart"],
        "availability_goal": availability["availability_goal"],
        "availability_channels": availability["channels"],
        "regional_activity_rewards": activity_rewards.get("regions", activity_rewards),
        "boss_difficulty_modes": boss_progression["difficulty_modes"],
        "manifest_requirements": {
            "required_battle_mechanics": entry["required_battle_mechanics"],
            "required_qol_systems": entry["required_qol_systems"],
            "required_availability_commitments": entry["required_availability_commitments"],
            "preserve_rules": entry["preserve_rules"],
        },
    }


def build_seed_data(manifest: dict) -> dict[str, dict]:
    imports = manifest_imports(manifest)
    return {
        imports["oak_lab_39_first_partner_selector"]["psdk_target"]: build_starter_seed(
            imports["oak_lab_39_first_partner_selector"]
        ),
        imports["routes_1_to_3_migration_encounters"]["psdk_target"]: build_encounter_seed(
            imports["routes_1_to_3_migration_encounters"]
        ),
        imports["world_region_progression_spine"]["psdk_target"]: build_region_seed(
            imports["world_region_progression_spine"]
        ),
        imports["custom_faction_war_registry"]["psdk_target"]: build_faction_seed(
            imports["custom_faction_war_registry"]
        ),
        imports["core_companion_registry"]["psdk_target"]: build_companion_seed(
            imports["core_companion_registry"]
        ),
        imports["rival_worldlink_registry"]["psdk_target"]: build_rival_worldlink_seed(
            imports["rival_worldlink_registry"]
        ),
        imports["gameplay_systems_registry"]["psdk_target"]: build_gameplay_systems_seed(
            imports["gameplay_systems_registry"]
        ),
    }


def check_outputs(seed_data: dict[str, dict]) -> list[str]:
    errors: list[str] = []
    for relative_path, expected in seed_data.items():
        path = ROOT / "psdk" / "nexus-red" / relative_path
        if not path.exists():
            errors.append(f"missing generated seed file: {path.relative_to(ROOT)}")
            continue
        actual = read_json(path)
        if actual != expected:
            errors.append(f"generated seed file is stale: {path.relative_to(ROOT)}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="verify generated files are current without writing")
    args = parser.parse_args()

    manifest = read_json(MANIFEST)
    seed_data = build_seed_data(manifest)
    if args.check:
        errors = check_outputs(seed_data)
        if errors:
            print("PSDK seed data generation check failed:")
            for error in errors:
                print(f"- {error}")
            return 1
        print("PSDK seed data generation check passed.")
        return 0

    for relative_path, data in seed_data.items():
        write_json(ROOT / "psdk" / "nexus-red" / relative_path, data)
    print("Generated PSDK seed data files.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
