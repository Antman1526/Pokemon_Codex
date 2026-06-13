#!/usr/bin/env python3
"""Validate Pokemon Nexus Red design YAML files."""

from __future__ import annotations

import sys
from pathlib import Path

try:
    import yaml
except ImportError as exc:
    raise SystemExit("PyYAML is required: python3 -m pip install PyYAML") from exc


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data_design"


def load_yaml(path: Path):
    with path.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def validate_required_files() -> list[str]:
    errors: list[str] = []
    required = [
        "region_chapters.yaml",
        "rivals.yaml",
        "starter_pools.yaml",
        "early_encounter_policy.yaml",
        "worldlink_notifications.yaml",
        "boss_progression.yaml",
        "rival_progression_kanto.yaml",
        "kanto_vertical_slice_flags.yaml",
        "red_companion.yaml",
        "availability_channels.yaml",
        "region_activity_rewards.yaml",
    ]
    for name in required:
        if not (DATA_DIR / name).exists():
            errors.append(f"Missing required design data file: {name}")
    return errors


def validate_regions(data) -> list[str]:
    errors: list[str] = []
    regions = data.get("regions", {})
    expected = {
        "kanto",
        "johto",
        "hoenn",
        "sinnoh_hisui",
        "unova",
        "kalos",
        "alola",
        "galar",
        "paldea",
        "world_nexus_championship",
    }
    missing = expected - set(regions)
    if missing:
        errors.append(f"region_chapters.yaml missing regions: {sorted(missing)}")
    for region_id, region in regions.items():
        for field in ("order", "arrival_hub", "exit_destination", "villain_focus", "mechanic_focus"):
            if field not in region:
                errors.append(f"{region_id} missing field: {field}")
    return errors


def validate_rivals(data) -> list[str]:
    errors: list[str] = []
    rivals = data.get("rivals", [])
    if len(rivals) != 10:
        errors.append(f"Expected 10 rivals, found {len(rivals)}")
    seen = set()
    for rival in rivals:
        rival_id = rival.get("rival_id")
        if not rival_id:
            errors.append("Rival missing rival_id")
            continue
        if rival_id in seen:
            errors.append(f"Duplicate rival_id: {rival_id}")
        seen.add(rival_id)
        for field in ("display_name", "role", "team_archetype", "chapter_appearances"):
            if field not in rival:
                errors.append(f"{rival_id} missing field: {field}")
    return errors


def validate_starters(data) -> list[str]:
    errors: list[str] = []
    pools = data.get("starter_pools", {})
    official_count = sum(len(pools.get(region, [])) for region in (
        "kanto",
        "johto",
        "hoenn",
        "sinnoh",
        "unova",
        "kalos",
        "alola",
        "galar",
        "paldea",
    ))
    special_count = len(pools.get("special", []))
    if official_count != 27:
        errors.append(f"Expected 27 official starters, found {official_count}")
    if special_count != 12:
        errors.append(f"Expected 12 special starters, found {special_count}")
    return errors


def validate_encounters(data) -> list[str]:
    errors: list[str] = []
    routes = data.get("routes", {})
    for route_id, route in routes.items():
        total = 0
        for group in route.get("encounter_groups", {}).values():
            total += group.get("target_rate_percent", 0)
        if total != 100:
            errors.append(f"{route_id} encounter target total is {total}, expected 100")
    return errors


def main() -> int:
    errors = validate_required_files()

    for path in sorted(DATA_DIR.glob("*.yaml")):
        try:
            load_yaml(path)
        except Exception as exc:  # noqa: BLE001 - CLI validator should report file failures.
            errors.append(f"{path.name} failed YAML parse: {exc}")

    if not errors:
        errors.extend(validate_regions(load_yaml(DATA_DIR / "region_chapters.yaml")))
        errors.extend(validate_rivals(load_yaml(DATA_DIR / "rivals.yaml")))
        errors.extend(validate_starters(load_yaml(DATA_DIR / "starter_pools.yaml")))
        errors.extend(validate_encounters(load_yaml(DATA_DIR / "early_encounter_policy.yaml")))

    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1

    print("Design data validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
