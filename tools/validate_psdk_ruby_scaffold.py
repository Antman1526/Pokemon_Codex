#!/usr/bin/env python3
"""Validate the PSDK Ruby scaffold for Nexus Red."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "psdk" / "nexus-red" / "project" / "scripts" / "nexus_red" / "000_seed_loader.rb"
README = ROOT / "psdk" / "nexus-red" / "project" / "scripts" / "nexus_red" / "README.md"

REQUIRED_MARKERS = (
    "module NexusRed",
    "module SeedData",
    "starter_selector",
    "early_encounters",
    "regions",
    "factions",
    "companions",
    "rivals_worldlink",
    "gameplay_systems",
    "RuntimeState",
    "PFM::GameState",
    "on_player_initialize(:nexus_red)",
    "on_expand_global_variables(:nexus_red)",
)

REQUIRED_REGISTRY_FILES = (
    "oak_lab_first_partner_selector.json",
    "routes_1_to_3_migration_encounters.json",
    "world_region_progression_spine.json",
    "custom_faction_war_registry.json",
    "core_companion_registry.json",
    "rival_worldlink_registry.json",
    "gameplay_systems_registry.json",
)

RUNTIME_SMOKE = r"""
require './scripts/nexus_red/000_seed_loader'

all = NexusRed::SeedData.all
raise 'expected 7 registries' unless all.length == 7
raise 'expected 39 selectable partners' unless NexusRed::SeedData.starter_selector['selectable_partners'].length == 39

route_targets = NexusRed::SeedData.early_encounters['route_targets']
raise 'expected 3 early route targets' unless route_targets.length == 3
route_targets.each do |route_id, route|
  raise "#{route_id} expected 13 encounters" unless route['encounters'].length == 13
end

regions = NexusRed::SeedData.regions['region_unlocks'].map { |region| region['region_id'] }
raise 'expected Kanto first' unless regions.first == 'kanto'
raise 'expected Nexus Island final' unless regions.last == 'nexus_island'
raise 'expected 10 regions' unless regions.length == 10

factions = NexusRed::SeedData.factions
raise 'expected Team Rocket primary antagonist' unless factions['primary_antagonist'] == 'team_rocket'
raise 'expected Nexus Order hidden meta villain' unless factions['hidden_meta_villain'] == 'nexus_order'
raise 'expected 9 custom factions' unless factions['factions'].length == 9

companions = NexusRed::SeedData.companions
raise 'expected Red primary companion' unless companions['primary_companion'] == 'red'
raise 'expected 7 companions' unless companions['companions'].length == 7

rivals = NexusRed::SeedData.rivals_worldlink
raise 'expected 10 rivals' unless rivals['rivals'].length == 10
raise 'expected Blue/Ava/Dax starting rivals' unless rivals['starting_rivals'] == %w[blue ava dax]
pause = rivals['worldlink_settings']['delivery_rules']['pause_and_digest']
raise 'expected cave WorldLink pause' unless pause.include?('cave')
raise 'expected villain hideout WorldLink pause' unless pause.include?('villain_hideout')

systems = NexusRed::SeedData.gameplay_systems
raise 'expected Gen 9 species scope' unless systems['pokedex_and_availability']['species_scope'] == 'through_generation_9'
raise 'expected all base species before final boss' unless systems['pokedex_and_availability']['all_base_species_before_final_boss'] == true
raise 'expected starting money 100000' unless systems['pokemon_center_and_mart']['mart_rules']['starting_money'] == 100000

state = NexusRed::RuntimeState.build
raise 'expected kanto runtime region' unless state['current_region'] == 'kanto'
raise 'expected Red active companion' unless state['active_companion'] == 'red'
raise 'expected standard difficulty' unless state['gameplay_options']['difficulty_mode'] == 'standard'

puts 'Nexus Red Ruby seed loader runtime smoke passed.'
"""


def validate() -> list[str]:
    errors: list[str] = []
    if not SCRIPT.exists():
        return [f"missing Ruby seed loader: {SCRIPT.relative_to(ROOT)}"]
    if not README.exists():
        errors.append(f"missing Ruby scaffold README: {README.relative_to(ROOT)}")

    content = SCRIPT.read_text(encoding="utf-8")
    for marker in REQUIRED_MARKERS:
        if marker not in content:
            errors.append(f"Ruby seed loader missing marker: {marker}")
    for filename in REQUIRED_REGISTRY_FILES:
        if filename not in content:
            errors.append(f"Ruby seed loader missing registry file: {filename}")

    result = subprocess.run(
        ["ruby", "-c", str(SCRIPT)],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    if result.returncode != 0:
        errors.append("Ruby syntax check failed:\n" + result.stdout)

    runtime = subprocess.run(
        ["ruby", "-e", RUNTIME_SMOKE],
        cwd=ROOT / "psdk" / "nexus-red" / "project",
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    if runtime.returncode != 0:
        errors.append("Ruby runtime smoke check failed:\n" + runtime.stdout)

    if README.exists():
        readme = README.read_text(encoding="utf-8")
        for marker in ("000_seed_loader.rb", "Data/nexus_red_seed/generated", "generate_psdk_seed_data.py", "runtime smoke"):
            if marker not in readme:
                errors.append(f"Ruby scaffold README missing marker: {marker}")

    return errors


def main() -> int:
    errors = validate()
    if errors:
        print("PSDK Ruby scaffold validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print("PSDK Ruby scaffold validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
