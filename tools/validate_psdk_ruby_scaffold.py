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
    "module RivalProgress",
    "ensure_rival",
    "record_badge",
    "record_capture",
    "record_region_entry",
    "module CompanionProgress",
    "ensure_companion",
    "activate_companion",
    "record_scene",
    "tag_battle_ready?",
    "module FactionWar",
    "ensure_faction",
    "record_activity",
    "record_conflict",
    "reveal_hidden_faction",
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
raise 'expected helper 39 starter species' unless NexusRed::SeedData.starter_species.length == 39
raise 'expected Bulbasaur first starter helper' unless NexusRed::SeedData.starter_species.first == 'Bulbasaur'
raise 'expected Ralts final starter helper' unless NexusRed::SeedData.starter_species.last == 'Ralts'
raise 'expected Blue counter helper for Bulbasaur' unless NexusRed::SeedData.blue_counter_for('Bulbasaur') == 'Charmander'

route_targets = NexusRed::SeedData.early_encounters['route_targets']
raise 'expected 3 early route targets' unless route_targets.length == 3
route_targets.each do |route_id, route|
  raise "#{route_id} expected 13 encounters" unless route['encounters'].length == 13
end
raise 'expected route_1 helper encounters' unless NexusRed::SeedData.encounters_for_route('route_1').length == 13
raise 'expected route_3 helper to include Kubfu' unless NexusRed::SeedData.encounters_for_route('route_3').any? { |encounter| encounter['species'] == 'Kubfu' }

regions = NexusRed::SeedData.regions['region_unlocks'].map { |region| region['region_id'] }
raise 'expected Kanto first' unless regions.first == 'kanto'
raise 'expected Nexus Island final' unless regions.last == 'nexus_island'
raise 'expected 10 regions' unless regions.length == 10
raise 'expected region_order helper' unless NexusRed::SeedData.region_order == regions
raise 'expected final_region helper' unless NexusRed::SeedData.final_region == 'nexus_island'

factions = NexusRed::SeedData.factions
raise 'expected Team Rocket primary antagonist' unless factions['primary_antagonist'] == 'team_rocket'
raise 'expected Nexus Order hidden meta villain' unless factions['hidden_meta_villain'] == 'nexus_order'
raise 'expected 9 custom factions' unless factions['factions'].length == 9
raise 'expected primary_faction helper' unless NexusRed::SeedData.primary_faction == 'team_rocket'
raise 'expected hidden_meta_villain helper' unless NexusRed::SeedData.hidden_meta_villain == 'nexus_order'

companions = NexusRed::SeedData.companions
raise 'expected Red primary companion' unless companions['primary_companion'] == 'red'
raise 'expected 7 companions' unless companions['companions'].length == 7
raise 'expected red_primary_companion? helper' unless NexusRed::SeedData.red_primary_companion?
raise 'expected companion_ids helper' unless NexusRed::SeedData.companion_ids == %w[red ash misty brock blue may bill]

rivals = NexusRed::SeedData.rivals_worldlink
raise 'expected 10 rivals' unless rivals['rivals'].length == 10
raise 'expected Blue/Ava/Dax starting rivals' unless rivals['starting_rivals'] == %w[blue ava dax]
raise 'expected rival_ids helper' unless NexusRed::SeedData.rival_ids.length == 10
raise 'expected starting_rival_ids helper' unless NexusRed::SeedData.starting_rival_ids == %w[blue ava dax]
pause = rivals['worldlink_settings']['delivery_rules']['pause_and_digest']
raise 'expected cave WorldLink pause' unless pause.include?('cave')
raise 'expected villain hideout WorldLink pause' unless pause.include?('villain_hideout')
raise 'expected worldlink_paused_area? cave helper' unless NexusRed::SeedData.worldlink_paused_area?('cave')
raise 'expected worldlink_paused_area? safe route false' if NexusRed::SeedData.worldlink_paused_area?('route')

systems = NexusRed::SeedData.gameplay_systems
raise 'expected Gen 9 species scope' unless systems['pokedex_and_availability']['species_scope'] == 'through_generation_9'
raise 'expected all base species before final boss' unless systems['pokedex_and_availability']['all_base_species_before_final_boss'] == true
raise 'expected starting money 100000' unless systems['pokemon_center_and_mart']['mart_rules']['starting_money'] == 100000
raise 'expected all_base_species_before_final_boss? helper' unless NexusRed::SeedData.all_base_species_before_final_boss?
raise 'expected starting_money helper' unless NexusRed::SeedData.starting_money == 100000
raise 'expected gameplay_option_available? level caps helper' unless NexusRed::SeedData.gameplay_option_available?('level_caps')

state = NexusRed::RuntimeState.build
raise 'expected kanto runtime region' unless state['current_region'] == 'kanto'
raise 'expected Red active companion' unless state['active_companion'] == 'red'
raise 'expected standard difficulty' unless state['gameplay_options']['difficulty_mode'] == 'standard'

first_message = NexusRed::WorldLink.queue_message(
  state,
  'rival_badge',
  'Blue defeated Brock and earned the Boulder Badge.',
  source: 'blue',
  area_type: 'route'
)
raise 'expected immediate WorldLink message delivery' unless first_message['delivery'] == 'immediate'
raise 'expected one recent WorldLink message' unless state['worldlink_recent_messages'].length == 1
raise 'expected unread count after immediate message' unless state['worldlink_unread_count'] == 1

paused_message = NexusRed::WorldLink.queue_message(
  state,
  'rival_capture',
  'Ava caught a rare Gastly in Mt. Moon.',
  source: 'ava',
  area_type: 'cave'
)
raise 'expected paused WorldLink delivery in cave' unless paused_message['delivery'] == 'paused'
raise 'expected paused queue to hold dungeon update' unless state['worldlink_paused_messages'].length == 1
raise 'expected recent messages unchanged while paused' unless state['worldlink_recent_messages'].length == 1

digest = NexusRed::WorldLink.release_digest(state)
raise 'expected digest release title' unless digest['title'] == 'While You Were Away'
raise 'expected one digest item' unless digest['items'].length == 1
raise 'expected paused queue cleared after digest' unless state['worldlink_paused_messages'].empty?
raise 'expected digest message moved into recent feed' unless state['worldlink_recent_messages'].length == 2
raise 'expected unread count after digest' unless state['worldlink_unread_count'] == 2

NexusRed::WorldLink.mark_all_read(state)
raise 'expected WorldLink unread count cleared' unless state['worldlink_unread_count'] == 0

rival = NexusRed::RivalProgress.ensure_rival(state, 'blue')
raise 'expected Blue rival progress initialized' unless rival['display_name'] == 'Blue Oak'
raise 'expected Blue current region default' unless rival['current_region'] == 'kanto'
raise 'expected Blue relationship defaults copied' unless rival['relationship']['rivalry'] == 90
raise 'expected Blue empty badge list' unless rival['badges'].empty?
raise 'expected Blue empty capture list' unless rival['captures'].empty?

badge_message = NexusRed::RivalProgress.record_badge(
  state,
  'blue',
  'Brock',
  'Boulder Badge',
  location: 'Pewter Gym',
  area_type: 'route'
)
raise 'expected rival badge immediate WorldLink delivery' unless badge_message['delivery'] == 'immediate'
raise 'expected Blue badge count updated' unless state['rival_progress']['blue']['badge_count'] == 1
raise 'expected Blue badge recorded' unless state['rival_progress']['blue']['badges'].first['badge'] == 'Boulder Badge'
raise 'expected Blue latest badge activity' unless state['rival_progress']['blue']['latest_activity']['category'] == 'rival_badge'
raise 'expected WorldLink badge source Blue' unless state['worldlink_recent_messages'].last['source'] == 'blue'

capture_message = NexusRed::RivalProgress.record_capture(
  state,
  'ava',
  'Gastly',
  'Mt. Moon',
  rare: true,
  area_type: 'cave'
)
raise 'expected rare rival capture paused in cave' unless capture_message['delivery'] == 'paused'
raise 'expected Ava capture recorded' unless state['rival_progress']['ava']['captures'].first['species'] == 'Gastly'
raise 'expected Ava rare capture category' unless state['rival_progress']['ava']['latest_activity']['category'] == 'rival_rare_capture'
raise 'expected paused rival capture held for digest' unless state['worldlink_paused_messages'].length == 1

region_message = NexusRed::RivalProgress.record_region_entry(
  state,
  'dax',
  'johto',
  hub: 'New Bark Town',
  objective: 'tracking Rocket radio chatter',
  area_type: 'route'
)
raise 'expected rival region entry immediate delivery' unless region_message['delivery'] == 'immediate'
raise 'expected Dax current region updated' unless state['rival_progress']['dax']['current_region'] == 'johto'
raise 'expected Dax latest region objective' unless state['rival_progress']['dax']['latest_activity']['objective'] == 'tracking Rocket radio chatter'

rival_digest = NexusRed::WorldLink.release_digest(state)
raise 'expected rival digest item released' unless rival_digest['items'].length == 1
raise 'expected rival progress tracks three rivals' unless state['rival_progress'].keys.sort == %w[ava blue dax]

red = NexusRed::CompanionProgress.ensure_companion(state, 'red')
raise 'expected Red companion progress initialized' unless red['display_name'] == 'Red'
raise 'expected Red active by default' unless red['active'] == true
raise 'expected Red follows by default' unless red['following'] == true
raise 'expected Red tag battle ready' unless NexusRed::CompanionProgress.tag_battle_ready?(state, 'red')
raise 'expected Red blocked from gym partner role' if NexusRed::CompanionProgress.tag_battle_ready?(state, 'red', context: 'gym_battle')

misty_message = NexusRed::CompanionProgress.activate_companion(
  state,
  'misty',
  location: 'Route 25',
  reason: 'joined after the Cerulean bridge crisis',
  following: true,
  area_type: 'route'
)
raise 'expected Misty activation immediate delivery' unless misty_message['delivery'] == 'immediate'
raise 'expected Misty active companion progress' unless state['companion_progress']['misty']['active'] == true
raise 'expected Misty following state' unless state['companion_progress']['misty']['following'] == true
raise 'expected Misty active from Kanto' unless state['companion_progress']['misty']['active_from'] == 'kanto'

scene_message = NexusRed::CompanionProgress.record_scene(
  state,
  'red',
  'route_1_training',
  location: 'Route 1',
  summary: 'Red warmed up Antman before Viridian.',
  area_type: 'route'
)
raise 'expected companion scene immediate delivery' unless scene_message['delivery'] == 'immediate'
raise 'expected Red route scene recorded' unless state['companion_progress']['red']['scene_flags'].include?('route_1_training')
raise 'expected Red latest scene activity' unless state['companion_progress']['red']['latest_activity']['scene_id'] == 'route_1_training'

bill = NexusRed::CompanionProgress.ensure_companion(state, 'bill')
raise 'expected Bill initialized as support companion' unless bill['display_name'] == 'Bill'
raise 'expected Bill not tag battle ready' if NexusRed::CompanionProgress.tag_battle_ready?(state, 'bill')
raise 'expected active companion remains Red' unless state['active_companion'] == 'red'

rocket = NexusRed::FactionWar.ensure_faction(state, 'team_rocket')
raise 'expected Team Rocket faction progress initialized' unless rocket['display_name'] == 'Team Rocket'
raise 'expected Giovanni as Rocket leader' unless rocket['leader'] == 'Giovanni'
raise 'expected Team Rocket visible as primary faction' unless rocket['revealed'] == true
raise 'expected Rocket starts with zero threat' unless rocket['threat_level'] == 0

activity_message = NexusRed::FactionWar.record_activity(
  state,
  'team_rocket',
  'kanto',
  'Viridian City',
  'stolen parcel route surveillance',
  threat_delta: 2,
  area_type: 'route'
)
raise 'expected faction activity immediate delivery' unless activity_message['delivery'] == 'immediate'
raise 'expected Rocket threat increased' unless state['faction_progress']['team_rocket']['threat_level'] == 2
raise 'expected Rocket region activity recorded' unless state['faction_progress']['team_rocket']['region_activity']['kanto'].first['location'] == 'Viridian City'
raise 'expected Rocket latest villain alert' unless state['faction_progress']['team_rocket']['latest_activity']['category'] == 'villain_alert'

conflict_message = NexusRed::FactionWar.record_conflict(
  state,
  'team_rocket',
  'team_gold_dust',
  'mt_moon',
  'fossil scan data theft',
  intensity: 3,
  area_type: 'cave'
)
raise 'expected faction conflict paused in cave' unless conflict_message['delivery'] == 'paused'
raise 'expected Rocket conflict recorded' unless state['faction_progress']['team_rocket']['conflicts'].first['opponent'] == 'team_gold_dust'
raise 'expected Gold Dust conflict mirror recorded' unless state['faction_progress']['team_gold_dust']['conflicts'].first['opponent'] == 'team_rocket'
raise 'expected faction conflict held for digest' unless state['worldlink_paused_messages'].length == 1

order = NexusRed::FactionWar.ensure_faction(state, 'nexus_order')
raise 'expected Nexus Order hidden by default' unless order['revealed'] == false
reveal_message = NexusRed::FactionWar.reveal_hidden_faction(
  state,
  'nexus_order',
  'sinnoh_hisui',
  'Spear Pillar distortion',
  area_type: 'ruins'
)
raise 'expected Nexus Order reveal paused in ruins' unless reveal_message['delivery'] == 'paused'
raise 'expected Nexus Order revealed after reveal call' unless state['faction_progress']['nexus_order']['revealed'] == true
raise 'expected Nexus Order reveal region recorded' unless state['faction_progress']['nexus_order']['latest_activity']['region'] == 'sinnoh_hisui'

faction_digest = NexusRed::WorldLink.release_digest(state)
raise 'expected faction digest releases conflict and reveal' unless faction_digest['items'].length == 2
raise 'expected faction progress tracks Rocket, Gold Dust, and Nexus Order' unless state['faction_progress'].keys.sort == %w[nexus_order team_gold_dust team_rocket]

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
