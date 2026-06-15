#!/usr/bin/env python3
"""Validate the PSDK Ruby scaffold for Nexus Red."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "psdk" / "nexus-red" / "project" / "scripts" / "nexus_red" / "000_seed_loader.rb"
RUNTIME_DIR = ROOT / "psdk" / "nexus-red" / "project" / "scripts" / "nexus_red" / "runtime"
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
    "module RegionProgress",
    "ensure_progress",
    "advance_to_next_region",
    "current_region_seed",
    "can_enter_region?",
    "module GameplayOptions",
    "ensure_options",
    "set_difficulty",
    "toggle_option",
    "unlock_qol",
    "rare_candy_mart_available?",
    "module FieldTools",
    "ensure_tools",
    "unlock_tool",
    "has_tool?",
    "can_use_replacement?",
    "expanded_dig_actions",
    "module PokedexAvailability",
    "ensure_pokedex",
    "set_required_species",
    "record_seen",
    "record_caught",
    "readiness_report",
    "pre_final_ready?",
    "module CenterMartServices",
    "ensure_services",
    "use_nurse_service",
    "terminal_available?",
    "mart_inventory",
    "unlock_mart_tier",
    "module EncounterWorld",
    "ensure_world",
    "set_day_phase",
    "set_weather",
    "unlock_fishing_rod",
    "daycare_enabled?",
    "module BattleMechanics",
    "ensure_mechanics",
    "mechanic_enabled?",
    "ai_profile_for",
    "gimmick_status",
    "unlock_gimmick",
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

REQUIRED_RUNTIME_FILES = (
    "seed_data.rb",
    "runtime_state.rb",
    "world_link.rb",
    "rival_progress.rb",
    "companion_progress.rb",
    "faction_war.rb",
    "region_progress.rb",
    "gameplay_options.rb",
    "field_tools.rb",
    "pokedex_availability.rb",
    "center_mart_services.rb",
    "encounter_world.rb",
    "battle_mechanics.rb",
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

journey = NexusRed::RegionProgress.ensure_progress(state)
raise 'expected Kanto current journey region' unless journey['current_region'] == 'kanto'
raise 'expected only Kanto unlocked at start' unless journey['unlocked_regions'] == ['kanto']
raise 'expected no completed regions at start' unless journey['completed_regions'].empty?
raise 'expected current region seed Kanto' unless NexusRed::RegionProgress.current_region_seed(state)['display_name'] == 'Kanto'
raise 'expected Kanto enterable at start' unless NexusRed::RegionProgress.can_enter_region?(state, 'kanto')
raise 'expected Johto locked at start' if NexusRed::RegionProgress.can_enter_region?(state, 'johto')

johto_message = NexusRed::RegionProgress.advance_to_next_region(
  state,
  completion_flag: 'kanto_indigo_league_clear',
  transition_hub: 'New Bark Town',
  area_type: 'route'
)
raise 'expected Johto story unlock immediate delivery' unless johto_message['delivery'] == 'immediate'
raise 'expected current region switches to Johto' unless state['current_region'] == 'johto'
raise 'expected one unlocked region after Johto transition' unless state['region_progress']['unlocked_regions'] == ['johto']
raise 'expected Kanto completed after transition' unless state['region_progress']['completed_regions'] == ['kanto']
raise 'expected region history tracks Kanto and Johto' unless state['region_progress']['region_history'] == %w[kanto johto]
raise 'expected Johto enterable after transition' unless NexusRed::RegionProgress.can_enter_region?(state, 'johto')
raise 'expected Kanto no longer enterable after single-region transition' if NexusRed::RegionProgress.can_enter_region?(state, 'kanto')
raise 'expected transition flag recorded' unless state['region_progress']['latest_transition']['completion_flag'] == 'kanto_indigo_league_clear'

8.times do |index|
  NexusRed::RegionProgress.advance_to_next_region(
    state,
    completion_flag: "chapter_#{index + 2}_clear",
    transition_hub: "region_gate_#{index + 2}",
    area_type: 'route'
  )
end
raise 'expected Nexus Island current final region' unless state['current_region'] == 'nexus_island'
raise 'expected final region unlocked helper' unless NexusRed::RegionProgress.final_region_unlocked?(state)
raise 'expected 9 completed regions before final' unless state['region_progress']['completed_regions'].length == 9
raise 'expected journey not complete before Nexus Island clear' if NexusRed::RegionProgress.journey_complete?(state)

final_message = NexusRed::RegionProgress.complete_current_region(
  state,
  completion_flag: 'giovanni_final_battle_clear',
  area_type: 'story_dungeon'
)
raise 'expected final completion paused in story dungeon' unless final_message['delivery'] == 'paused'
raise 'expected journey complete after Nexus Island clear' unless NexusRed::RegionProgress.journey_complete?(state)
raise 'expected Nexus Island completed at journey end' unless state['region_progress']['completed_regions'].last == 'nexus_island'

options = NexusRed::GameplayOptions.ensure_options(state)
raise 'expected standard gameplay difficulty default' unless options['difficulty_mode'] == 'standard'
raise 'expected standard AI profile' unless options['difficulty_profile']['ai_profile'] == 'smart'
raise 'expected level caps enabled by default' unless NexusRed::GameplayOptions.level_caps_enabled?(state)
raise 'expected starting money runtime option' unless options['starting_money'] == 100000
raise 'expected running shoes start enabled' unless options['unlocked_qol'].include?('running_shoes')
raise 'expected rare candy mart locked before Brock' if NexusRed::GameplayOptions.rare_candy_mart_available?(state)

hard = NexusRed::GameplayOptions.set_difficulty(state, 'hard')
raise 'expected hard difficulty selected' unless hard['difficulty_mode'] == 'hard'
raise 'expected hard cap type' unless hard['difficulty_profile']['cap_type'] == 'hard'
raise 'expected hard AI profile' unless hard['difficulty_profile']['ai_profile'] == 'strong'

repel = NexusRed::GameplayOptions.toggle_option(state, 'infinite_repel_toggle', true)
raise 'expected infinite repel toggle enabled' unless repel['infinite_repel_enabled'] == true
raise 'expected infinite repel unavailable marker absent' if repel['disabled_options'].include?('infinite_repel_toggle')

after_brock = NexusRed::GameplayOptions.unlock_qol(state, 'after_brock')
raise 'expected rare candy mart unlocked after Brock' unless after_brock['unlocked_qol'].include?('rare_candy_mart')
raise 'expected portable PC lite unlocked after Brock' unless after_brock['unlocked_qol'].include?('portable_pc_lite')
raise 'expected rare candy mart available after Brock' unless NexusRed::GameplayOptions.rare_candy_mart_available?(state)

nuzlocke = NexusRed::GameplayOptions.set_difficulty(state, 'nuzlocke')
raise 'expected nuzlocke difficulty selected' unless nuzlocke['difficulty_mode'] == 'nuzlocke'
raise 'expected nuzlocke enabled flag' unless nuzlocke['nuzlocke_enabled'] == true
raise 'expected level caps enforced by nuzlocke' unless nuzlocke['level_caps_enabled'] == true
raise 'expected nuzlocke first encounter rule' unless nuzlocke['nuzlocke_rules'].include?('first_encounter_rule')
raise 'expected nuzlocke item rules copied' unless nuzlocke['difficulty_profile']['item_rules'] == 'configurable_default_banned'

tools = NexusRed::FieldTools.ensure_tools(state)
raise 'expected no field tools at runtime start' unless tools['unlocked_tools'].empty?
raise 'expected trail cutter known replacement' unless tools['known_replacements']['trail_cutter'] == 'Cut'
raise 'expected Trail Cutter missing before unlock' if NexusRed::FieldTools.has_tool?(state, 'trail_cutter')
raise 'expected Cut replacement blocked before Trail Cutter' if NexusRed::FieldTools.can_use_replacement?(state, 'Cut')

trail_message = NexusRed::FieldTools.unlock_tool(
  state,
  'trail_cutter',
  source: 'S.S. Anne Captain',
  area_type: 'route'
)
raise 'expected Trail Cutter unlock immediate delivery' unless trail_message['delivery'] == 'immediate'
raise 'expected Trail Cutter unlocked' unless NexusRed::FieldTools.has_tool?(state, 'trail_cutter')
raise 'expected Cut replacement available with Trail Cutter' unless NexusRed::FieldTools.can_use_replacement?(state, 'Cut')
raise 'expected Surf replacement still blocked' if NexusRed::FieldTools.can_use_replacement?(state, 'Surf')
raise 'expected Trail Cutter unlock source recorded' unless state['field_tools']['tool_sources']['trail_cutter'] == 'S.S. Anne Captain'

dig_message = NexusRed::FieldTools.unlock_tool(
  state,
  'dig_kit',
  source: 'Rock Tunnel field cache',
  area_type: 'cave'
)
raise 'expected Dig Kit unlock paused in cave' unless dig_message['delivery'] == 'paused'
raise 'expected Dig replacement available with Dig Kit' unless NexusRed::FieldTools.can_use_replacement?(state, 'Dig')
raise 'expected expanded Dig actions available' unless NexusRed::FieldTools.expanded_dig_actions(state).include?('find_fossils')

sky_message = NexusRed::FieldTools.unlock_tool(
  state,
  'sky_pass',
  source: 'late Kanto airport pass',
  area_type: 'route'
)
raise 'expected Sky Pass immediate delivery' unless sky_message['delivery'] == 'immediate'
raise 'expected Fly replacement available with Sky Pass' unless NexusRed::FieldTools.can_use_replacement?(state, 'Fly')
raise 'expected expanded Fly actions available' unless NexusRed::FieldTools.expanded_fly_actions(state).include?('story_gated_inter_region_transit')
raise 'expected unknown field tool rejected' unless begin
  NexusRed::FieldTools.unlock_tool(state, 'rocket_warp_glove')
  false
rescue ArgumentError
  true
end

dex = NexusRed::PokedexAvailability.ensure_pokedex(state)
raise 'expected Gen 9 Pokedex scope' unless dex['species_scope'] == 'through_generation_9'
raise 'expected WorldLink Pokedex readiness surface' unless dex['readiness_surface'] == 'WorldLink'
raise 'expected weather availability channel known' unless dex['availability_channels'].include?('weather')
raise 'expected all base species commitment' unless dex['all_base_species_before_final_boss'] == true

NexusRed::PokedexAvailability.set_required_species(state, %w[Bulbasaur Charmander Squirtle])
initial_report = NexusRed::PokedexAvailability.readiness_report(state)
raise 'expected incomplete initial Pokedex readiness' unless initial_report['readiness_status'] == 'incomplete'
raise 'expected three missing required species' unless initial_report['missing_species'] == %w[Bulbasaur Charmander Squirtle]

seen_message = NexusRed::PokedexAvailability.record_seen(
  state,
  'Bulbasaur',
  location: 'Route 1',
  channel: 'wild_grass',
  area_type: 'route'
)
raise 'expected seen message immediate delivery' unless seen_message['delivery'] == 'immediate'
raise 'expected Bulbasaur seen location recorded' unless state['pokedex']['seen_species']['Bulbasaur'].first['location'] == 'Route 1'

caught_message = NexusRed::PokedexAvailability.record_caught(
  state,
  'Bulbasaur',
  location: 'Route 1',
  channel: 'wild_grass',
  area_type: 'route'
)
raise 'expected caught message immediate delivery' unless caught_message['delivery'] == 'immediate'
raise 'expected Bulbasaur caught recorded' unless state['pokedex']['caught_species'].key?('Bulbasaur')
raise 'expected pre-final readiness still incomplete' if NexusRed::PokedexAvailability.pre_final_ready?(state)

hint = NexusRed::PokedexAvailability.register_availability_hint(
  state,
  'Squirtle',
  region: 'kanto',
  channel: 'fishing',
  hint: 'Seen near Route 3 ponds after Old Rod access.',
  area_type: 'route'
)
raise 'expected availability hint immediate delivery' unless hint['delivery'] == 'immediate'
raise 'expected Squirtle hint recorded' unless state['pokedex']['active_hints']['Squirtle'].first['channel'] == 'fishing'

NexusRed::PokedexAvailability.record_caught(state, 'Charmander', location: 'Route 1', channel: 'wild_grass', area_type: 'route')
NexusRed::PokedexAvailability.record_caught(state, 'Squirtle', location: 'Route 3', channel: 'fishing', area_type: 'route')
complete_report = NexusRed::PokedexAvailability.readiness_report(state)
raise 'expected completed Pokedex readiness' unless complete_report['readiness_status'] == 'ready'
raise 'expected all required caught' unless complete_report['caught_count'] == 3
raise 'expected no missing species after catches' unless complete_report['missing_species'].empty?
raise 'expected pre-final readiness true after required catches' unless NexusRed::PokedexAvailability.pre_final_ready?(state)
raise 'expected unknown availability channel rejected' unless begin
  NexusRed::PokedexAvailability.record_seen(state, 'Mew', location: 'Unknown', channel: 'truck_rumor')
  false
rescue ArgumentError
  true
end

services = NexusRed::CenterMartServices.ensure_services(state)
raise 'expected starting money in Center/Mart state' unless services['money'] == 100000
raise 'expected heal team Nurse Joy service available' unless services['nurse_joy_services'].include?('heal_team')
raise 'expected WorldLink terminal available' unless NexusRed::CenterMartServices.terminal_available?(state, 'worldlink_feed')
raise 'expected hyper training terminal unavailable before unlock' if NexusRed::CenterMartServices.terminal_available?(state, 'hyper_training')

heal = NexusRed::CenterMartServices.use_nurse_service(
  state,
  'heal_team',
  location: 'Viridian Pokemon Center',
  area_type: 'route'
)
raise 'expected heal service immediate delivery' unless heal['delivery'] == 'immediate'
raise 'expected heal service recorded' unless state['center_mart']['service_history'].first['service_id'] == 'heal_team'

gift = NexusRed::CenterMartServices.use_nurse_service(
  state,
  'daily_wellness_gift',
  location: 'Viridian Pokemon Center',
  area_type: 'route'
)
raise 'expected daily wellness gift immediate delivery' unless gift['delivery'] == 'immediate'
raise 'expected daily wellness gift flag recorded' unless state['center_mart']['daily_services_claimed'].include?('daily_wellness_gift')

basic_inventory = NexusRed::CenterMartServices.mart_inventory(state, 'viridian')
raise 'expected basic balls immediate in Viridian mart' unless basic_inventory.include?('basic_balls')
raise 'expected core medicine immediate in Viridian mart' unless basic_inventory.include?('core_medicine')
raise 'expected rare candies locked before badge unlock' if basic_inventory.include?('rare_candies')

NexusRed::CenterMartServices.unlock_mart_tier(state, 'after_first_badge')
badge_inventory = NexusRed::CenterMartServices.mart_inventory(state, 'pewter')
raise 'expected rare candies after first badge' unless badge_inventory.include?('rare_candies')

NexusRed::CenterMartServices.unlock_terminal_feature(state, 'hyper_training')
raise 'expected hyper training terminal available after unlock' unless NexusRed::CenterMartServices.terminal_available?(state, 'hyper_training')
celadon_inventory = NexusRed::CenterMartServices.mart_inventory(state, 'celadon')
raise 'expected Celadon specialty mart flag' unless celadon_inventory.include?('specialty_mart')
raise 'expected unknown Nurse Joy service rejected' unless begin
  NexusRed::CenterMartServices.use_nurse_service(state, 'rocket_heal_discount', location: 'Celadon')
  false
rescue ArgumentError
  true
end

world = NexusRed::EncounterWorld.ensure_world(state)
raise 'expected default day phase' unless world['day_phase'] == 'day'
raise 'expected default clear weather' unless world['weather'] == 'clear'
raise 'expected night phase known' unless world['available_day_phases'].include?('night')
raise 'expected thunderstorm weather known' unless world['available_weather'].include?('thunderstorm')
raise 'expected no fishing rods unlocked initially' unless world['unlocked_fishing_rods'].empty?
raise 'expected daycare disabled before unlock' if NexusRed::EncounterWorld.daycare_enabled?(state)
raise 'expected following rollout policy copied' unless world['following_pokemon_policy'] == 'phased_starter_and_favorites_first'

phase_message = NexusRed::EncounterWorld.set_day_phase(
  state,
  'night',
  source: 'Johto time tracker',
  area_type: 'route'
)
raise 'expected day phase update immediate delivery' unless phase_message['delivery'] == 'immediate'
raise 'expected night phase applied' unless state['encounter_world']['day_phase'] == 'night'

weather_message = NexusRed::EncounterWorld.set_weather(
  state,
  'thunderstorm',
  source: 'Vermilion power sabotage',
  area_type: 'route'
)
raise 'expected weather update immediate delivery' unless weather_message['delivery'] == 'immediate'
raise 'expected thunderstorm weather applied' unless state['encounter_world']['weather'] == 'thunderstorm'

rod_message = NexusRed::EncounterWorld.unlock_fishing_rod(
  state,
  'old_rod',
  source: 'Vermilion fishing guru',
  area_type: 'route'
)
raise 'expected Old Rod unlock immediate delivery' unless rod_message['delivery'] == 'immediate'
raise 'expected Old Rod unlocked' unless state['encounter_world']['unlocked_fishing_rods'].include?('old_rod')

NexusRed::EncounterWorld.unlock_daycare(state, location: 'Route 5 Daycare')
raise 'expected daycare enabled after unlock' unless NexusRed::EncounterWorld.daycare_enabled?(state)
NexusRed::EncounterWorld.enable_overworld_pokemon(state, zone: 'Viridian Forest')
raise 'expected overworld Pokemon zone recorded' unless state['encounter_world']['overworld_pokemon_zones'].include?('Viridian Forest')
NexusRed::EncounterWorld.enable_following_pokemon(state, species: 'Pikachu')
raise 'expected following Pokemon species recorded' unless state['encounter_world']['following_pokemon_species'].include?('Pikachu')
raise 'expected invalid weather rejected' unless begin
  NexusRed::EncounterWorld.set_weather(state, 'rocket_smoke')
  false
rescue ArgumentError
  true
end

mechanics_state = NexusRed::RuntimeState.build
mechanics = NexusRed::BattleMechanics.ensure_mechanics(mechanics_state)
raise 'expected physical/special split enabled' unless NexusRed::BattleMechanics.mechanic_enabled?(mechanics_state, 'physical_special_split')
raise 'expected Fairy type enabled' unless NexusRed::BattleMechanics.mechanic_enabled?(mechanics_state, 'fairy_type')
raise 'expected Gen 9 abilities enabled' unless NexusRed::BattleMechanics.mechanic_enabled?(mechanics_state, 'modern_abilities_through_gen_9')
raise 'expected reusable TM list enabled' unless NexusRed::BattleMechanics.mechanic_enabled?(mechanics_state, 'expanded_reusable_tm_list')
raise 'expected standard AI profile smart' unless NexusRed::BattleMechanics.ai_profile_for(mechanics_state, 'standard') == 'smart'
raise 'expected expert AI profile competitive' unless NexusRed::BattleMechanics.ai_profile_for(mechanics_state, 'expert') == 'competitive'

mega_status = NexusRed::BattleMechanics.gimmick_status(mechanics_state, 'mega_evolution')
raise 'expected Mega locked before preview/full unlock' unless mega_status['state'] == 'locked'
raise 'expected Mega full unlock region Kalos' unless mega_status['full_unlock'] == 'kalos'

dynamax_status = NexusRed::BattleMechanics.gimmick_status(mechanics_state, 'dynamax_gigantamax')
raise 'expected Dynamax locked before Hoenn clear' unless dynamax_status['state'] == 'locked'
raise 'expected Dynamax preview after Hoenn' unless dynamax_status['first_preview'] == 'after_hoenn'

NexusRed::RegionProgress.ensure_progress(mechanics_state)
mechanics_state['region_progress']['completed_regions'] = %w[kanto johto hoenn]
tera_preview = NexusRed::BattleMechanics.gimmick_status(mechanics_state, 'terastallization')
raise 'expected Tera preview after Hoenn' unless tera_preview['state'] == 'preview'

NexusRed::BattleMechanics.unlock_gimmick(mechanics_state, 'mega_evolution', mode: 'full', source: 'Kalos Keystone Resonator')
raise 'expected Mega full unlock recorded' unless NexusRed::BattleMechanics.gimmick_status(mechanics_state, 'mega_evolution')['state'] == 'full'
raise 'expected Mega unlock source recorded' unless mechanics_state['battle_mechanics']['gimmick_unlocks']['mega_evolution']['source'] == 'Kalos Keystone Resonator'
raise 'expected unknown battle mechanic false' if NexusRed::BattleMechanics.mechanic_enabled?(mechanics_state, 'shadow_pokemon_mode')
raise 'expected unknown gimmick rejected' unless begin
  NexusRed::BattleMechanics.gimmick_status(mechanics_state, 'fusion_burst')
  false
rescue ArgumentError
  true
end

puts 'Nexus Red Ruby seed loader runtime smoke passed.'
"""


def validate() -> list[str]:
    errors: list[str] = []
    if not SCRIPT.exists():
        return [f"missing Ruby seed loader: {SCRIPT.relative_to(ROOT)}"]
    if not README.exists():
        errors.append(f"missing Ruby scaffold README: {README.relative_to(ROOT)}")

    if not RUNTIME_DIR.exists():
        errors.append(f"missing Ruby runtime directory: {RUNTIME_DIR.relative_to(ROOT)}")

    runtime_files = [RUNTIME_DIR / filename for filename in REQUIRED_RUNTIME_FILES]
    for runtime_file in runtime_files:
        if not runtime_file.exists():
            errors.append(f"missing Ruby runtime file: {runtime_file.relative_to(ROOT)}")

    content = SCRIPT.read_text(encoding="utf-8")
    for runtime_file in runtime_files:
        if runtime_file.exists():
            content += "\n" + runtime_file.read_text(encoding="utf-8")

    for marker in REQUIRED_MARKERS:
        if marker not in content:
            errors.append(f"Ruby scaffold missing marker: {marker}")
    for filename in REQUIRED_REGISTRY_FILES:
        if filename not in content:
            errors.append(f"Ruby scaffold missing registry file: {filename}")

    for ruby_file in [SCRIPT, *runtime_files]:
        if not ruby_file.exists():
            continue
        result = subprocess.run(
            ["ruby", "-c", str(ruby_file)],
            cwd=ROOT,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            check=False,
        )
        if result.returncode != 0:
            errors.append(f"Ruby syntax check failed for {ruby_file.relative_to(ROOT)}:\n{result.stdout}")

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
