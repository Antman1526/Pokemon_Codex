#!/usr/bin/env python3
"""Generate PSDK seed data from the current Nexus Red reference content."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "psdk" / "nexus-red" / "project" / "Data" / "nexus_red_seed" / "import_manifest.json"


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


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


def build_seed_data(manifest: dict) -> dict[str, dict]:
    imports = manifest_imports(manifest)
    return {
        imports["oak_lab_39_first_partner_selector"]["psdk_target"]: build_starter_seed(
            imports["oak_lab_39_first_partner_selector"]
        ),
        imports["routes_1_to_3_migration_encounters"]["psdk_target"]: build_encounter_seed(
            imports["routes_1_to_3_migration_encounters"]
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
