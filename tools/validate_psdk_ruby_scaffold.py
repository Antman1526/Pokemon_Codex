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
    "module StarterSelection",
    "ensure_selection",
    "available_partners",
    "select_partner",
    "starter_chosen?",
    "rival_assignment",
    "module EarlyMigrationEncounters",
    "ensure_migration",
    "route_target",
    "available_for_route",
    "catchable_species",
    "rare_power_species",
    "next_uncaught_for_route",
    "prepare_map_event_encounter",
    "record_migration_seen",
    "module MapEventBridge",
    "prepare_wild_battle_request",
    "pending_battle_request",
    "consume_pending_battle_request",
    "module RouteMigrationEventAdapter",
    "trigger_route",
    "module WildBattleLauncher",
    "launch_pending_request",
    "execute_pending_request",
    "execute_launch_payload",
    "build_launch_payload",
    "build_psdk_script_lines",
    "species_symbol",
    "psdk_runtime_available?",
    "launch_history",
    "module WildBattleResults",
    "record_result",
    "result_history",
    "last_launch",
    "module PartyStorage",
    "add_species",
    "deposit_species",
    "withdraw_species",
    "swap_species",
    "party_full?",
    "party_species",
    "pc_box_species",
    "module PortablePC",
    "ensure_portable_pc",
    "unlock",
    "unlocked?",
    "open",
    "summary",
    "deposit",
    "withdraw",
    "swap",
    "module FieldHealing",
    "ensure_field_healing",
    "policy",
    "available?",
    "set_party_condition",
    "heal_team",
    "restore_species",
    "module KantoStory",
    "ensure_kanto_story",
    "complete_brock",
    "brock_rewards_applied?",
    "complete_pewter_museum_anomaly",
    "museum_anomaly_cleared?",
    "complete_mt_moon_operation",
    "mt_moon_operation_cleared?",
    "gold_dust_invoice_found?",
    "complete_nugget_bridge_qualifier",
    "nugget_bridge_qualifier_cleared?",
    "complete_misty_battle",
    "misty_battle_cleared?",
    "field_healing_charges_for",
    "module Route1MigrationEvent",
    "module Route2MigrationEvent",
    "module Route3MigrationEvent",
    "trigger",
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
    "starter_selection.rb",
    "early_migration_encounters.rb",
    "map_event_bridge.rb",
    "route_migration_event_adapter.rb",
    "wild_battle_launcher.rb",
    "wild_battle_results.rb",
    "party_storage.rb",
    "portable_pc.rb",
    "field_healing.rb",
    "kanto_story.rb",
    "route1_migration_event.rb",
    "route2_migration_event.rb",
    "route3_migration_event.rb",
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

starter_state = NexusRed::RuntimeState.build
selection = NexusRed::StarterSelection.ensure_selection(starter_state)
raise 'expected 39 available starter partners' unless NexusRed::StarterSelection.available_partners(starter_state).length == 39
raise 'expected starter not chosen initially' if NexusRed::StarterSelection.starter_chosen?(starter_state)
raise 'expected Oak Lab selection map' unless selection['story_context']['map'] == 'Oak Lab'

starter_message = NexusRed::StarterSelection.select_partner(
  starter_state,
  'Bulbasaur',
  source: 'Professor Oak',
  area_type: 'route'
)
raise 'expected starter choice immediate delivery' unless starter_message['delivery'] == 'immediate'
raise 'expected starter chosen flag' unless NexusRed::StarterSelection.starter_chosen?(starter_state)
raise 'expected selected starter species recorded' unless starter_state['starter_selection']['selected_partner']['species'] == 'Bulbasaur'
raise 'expected selected starter added to party' unless starter_state['party_species'].include?('Bulbasaur')
raise 'expected Blue counter pick Charmander' unless NexusRed::StarterSelection.rival_assignment(starter_state, 'blue') == 'Charmander'
raise 'expected Ava priority pick Chikorita' unless NexusRed::StarterSelection.rival_assignment(starter_state, 'ava') == 'Chikorita'
raise 'expected Dax priority pick Cyndaquil' unless NexusRed::StarterSelection.rival_assignment(starter_state, 'dax') == 'Cyndaquil'
raise 'expected starter chosen story flag recorded' unless starter_state['story_flags'].include?('starter_chosen')
raise 'expected repeat starter choice rejected' unless begin
  NexusRed::StarterSelection.select_partner(starter_state, 'Charmander')
  false
rescue ArgumentError
  true
end
raise 'expected unknown starter rejected' unless begin
  NexusRed::StarterSelection.select_partner(NexusRed::RuntimeState.build, 'Missingno')
  false
rescue ArgumentError
  true
end

storage_state = NexusRed::RuntimeState.build
storage_result = NexusRed::PartyStorage.add_species(storage_state, 'Pikachu')
raise 'expected PartyStorage first add to party' unless storage_result['storage'] == 'party'
raise 'expected PartyStorage party_species helper' unless NexusRed::PartyStorage.party_species(storage_state) == ['Pikachu']
raise 'expected PartyStorage party not full' if NexusRed::PartyStorage.party_full?(storage_state)
storage_state['party_species'] = %w[Bulbasaur Charmander Squirtle Pikachu Eevee Ralts]
pc_storage_result = NexusRed::PartyStorage.add_species(storage_state, 'Rockruff')
raise 'expected PartyStorage add to PC when party full' unless pc_storage_result['storage'] == 'pc'
raise 'expected PartyStorage party full helper' unless NexusRed::PartyStorage.party_full?(storage_state)
raise 'expected PartyStorage pc_box_species helper' unless NexusRed::PartyStorage.pc_box_species(storage_state).include?('Rockruff')
deposit_result = NexusRed::PartyStorage.deposit_species(storage_state, 'Pikachu')
raise 'expected PartyStorage deposit status' unless deposit_result['status'] == 'deposited'
raise 'expected deposited species removed from party' if NexusRed::PartyStorage.party_species(storage_state).include?('Pikachu')
raise 'expected deposited species added to PC' unless NexusRed::PartyStorage.pc_box_species(storage_state).include?('Pikachu')
withdraw_result = NexusRed::PartyStorage.withdraw_species(storage_state, 'Rockruff')
raise 'expected PartyStorage withdraw status' unless withdraw_result['status'] == 'withdrawn'
raise 'expected withdrawn species added to party' unless NexusRed::PartyStorage.party_species(storage_state).include?('Rockruff')
raise 'expected withdrawn species removed from PC' if NexusRed::PartyStorage.pc_box_species(storage_state).include?('Rockruff')
swap_result = NexusRed::PartyStorage.swap_species(storage_state, party_species: 'Bulbasaur', pc_species: 'Pikachu')
raise 'expected PartyStorage swap status' unless swap_result['status'] == 'swapped'
raise 'expected swap moved PC species into party' unless NexusRed::PartyStorage.party_species(storage_state).include?('Pikachu')
raise 'expected swap moved party species into PC' unless NexusRed::PartyStorage.pc_box_species(storage_state).include?('Bulbasaur')
missing_deposit = NexusRed::PartyStorage.deposit_species(storage_state, 'Missingno')
raise 'expected missing deposit guarded' unless missing_deposit['status'] == 'missing_from_party'
blocked_withdraw_state = NexusRed::RuntimeState.build
blocked_withdraw_state['party_species'] = %w[Bulbasaur Charmander Squirtle Pikachu Eevee Ralts]
blocked_withdraw_state['pc_box_species'] = ['Rockruff']
blocked_withdraw = NexusRed::PartyStorage.withdraw_species(blocked_withdraw_state, 'Rockruff')
raise 'expected full party withdraw guarded' unless blocked_withdraw['status'] == 'party_full'

portable_state = NexusRed::RuntimeState.build
portable_pc = NexusRed::PortablePC.ensure_portable_pc(portable_state)
raise 'expected PortablePC locked by default' if portable_pc['unlocked']
raise 'expected PortablePC unlocked? false by default' if NexusRed::PortablePC.unlocked?(portable_state)
locked_open = NexusRed::PortablePC.open(portable_state)
raise 'expected locked PortablePC open guarded' unless locked_open['status'] == 'locked'
unlock_pc = NexusRed::PortablePC.unlock(
  portable_state,
  source: 'Brock and Red field kit',
  access_level: 'lite',
  area_type: 'route'
)
raise 'expected PortablePC unlock immediate delivery' unless unlock_pc['delivery'] == 'immediate'
raise 'expected PortablePC unlocked after story source' unless NexusRed::PortablePC.unlocked?(portable_state)
raise 'expected PortablePC source recorded' unless portable_state['portable_pc']['source'] == 'Brock and Red field kit'
raise 'expected PortablePC access level recorded' unless portable_state['portable_pc']['access_level'] == 'lite'
NexusRed::PartyStorage.add_species(portable_state, 'Bulbasaur')
NexusRed::PartyStorage.pc_box_species(portable_state) << 'Pikachu'
pc_summary = NexusRed::PortablePC.summary(portable_state)
raise 'expected PortablePC summary party count' unless pc_summary['party_count'] == 1
raise 'expected PortablePC summary PC count' unless pc_summary['pc_count'] == 1
raise 'expected PortablePC summary party limit' unless pc_summary['party_limit'] == 6
raise 'expected PortablePC summary party not full' if pc_summary['party_full']
opened_pc = NexusRed::PortablePC.open(portable_state)
raise 'expected unlocked PortablePC open status' unless opened_pc['status'] == 'open'
raise 'expected PortablePC opened count recorded' unless portable_state['portable_pc']['opened_count'] == 1
deposit_pc = NexusRed::PortablePC.deposit(portable_state, 'Bulbasaur')
raise 'expected PortablePC deposit forwarded' unless deposit_pc['status'] == 'deposited'
raise 'expected PortablePC last action deposit' unless portable_state['portable_pc']['last_action']['status'] == 'deposited'
withdraw_pc = NexusRed::PortablePC.withdraw(portable_state, 'Bulbasaur')
raise 'expected PortablePC withdraw forwarded' unless withdraw_pc['status'] == 'withdrawn'
swap_pc = NexusRed::PortablePC.swap(portable_state, party_species: 'Bulbasaur', pc_species: 'Pikachu')
raise 'expected PortablePC swap forwarded' unless swap_pc['status'] == 'swapped'
raise 'expected PortablePC swap moved Pikachu to party' unless NexusRed::PartyStorage.party_species(portable_state).include?('Pikachu')
locked_deposit = NexusRed::PortablePC.deposit(NexusRed::RuntimeState.build, 'Bulbasaur')
raise 'expected locked PortablePC deposit guarded' unless locked_deposit['status'] == 'locked'

healing_state = NexusRed::RuntimeState.build
field_healing = NexusRed::FieldHealing.ensure_field_healing(healing_state)
raise 'expected FieldHealing locked by default' if field_healing['unlocked']
raise 'expected standard FieldHealing policy limited' unless NexusRed::FieldHealing.policy(healing_state) == 'limited'
raise 'expected FieldHealing unavailable before unlock' if NexusRed::FieldHealing.available?(healing_state, area_type: 'route')
locked_heal = NexusRed::FieldHealing.heal_team(healing_state, location: 'Route 1', area_type: 'route')
raise 'expected locked FieldHealing guarded' unless locked_heal['status'] == 'locked'
unlock_healing = NexusRed::FieldHealing.unlock(
  healing_state,
  source: 'Mom and Brock care kit',
  charges: 2,
  area_type: 'route'
)
raise 'expected FieldHealing unlock immediate delivery' unless unlock_healing['delivery'] == 'immediate'
raise 'expected FieldHealing source recorded' unless healing_state['field_healing']['source'] == 'Mom and Brock care kit'
raise 'expected FieldHealing charges recorded' unless healing_state['field_healing']['charges'] == 2
NexusRed::PartyStorage.add_species(healing_state, 'Bulbasaur')
NexusRed::PartyStorage.add_species(healing_state, 'Charmander')
NexusRed::FieldHealing.set_party_condition(healing_state, 'Bulbasaur', hp_percent: 35, status: 'poison')
NexusRed::FieldHealing.set_party_condition(healing_state, 'Charmander', hp_percent: 1, status: 'faint')
heal_team = NexusRed::FieldHealing.heal_team(healing_state, location: 'Viridian Outskirts', area_type: 'route')
raise 'expected FieldHealing heal recorded' unless heal_team['status'] == 'healed'
raise 'expected FieldHealing standard charge consumed' unless heal_team['charges_remaining'] == 1
raise 'expected Bulbasaur restored by field heal' unless healing_state['party_conditions']['Bulbasaur'] == { 'hp_percent' => 100, 'status' => 'ok' }
raise 'expected FieldHealing usage history recorded' unless healing_state['field_healing']['usage_history'].first['location'] == 'Viridian Outskirts'
NexusRed::FieldHealing.set_party_condition(healing_state, 'Bulbasaur', hp_percent: 50, status: 'burn')
restore_one = NexusRed::FieldHealing.restore_species(healing_state, 'Bulbasaur', location: 'Route 2', area_type: 'route')
raise 'expected FieldHealing single restore recorded' unless restore_one['status'] == 'restored'
raise 'expected FieldHealing final charge consumed' unless restore_one['charges_remaining'] == 0
no_charge_heal = NexusRed::FieldHealing.heal_team(healing_state, location: 'Route 2', area_type: 'route')
raise 'expected FieldHealing no-charge guard' unless no_charge_heal['status'] == 'no_charges'
casual_healing_state = NexusRed::RuntimeState.build
NexusRed::GameplayOptions.set_difficulty(casual_healing_state, 'casual')
NexusRed::FieldHealing.unlock(casual_healing_state, source: 'Casual field kit', charges: 0, area_type: 'route')
NexusRed::PartyStorage.add_species(casual_healing_state, 'Squirtle')
casual_heal = NexusRed::FieldHealing.heal_team(casual_healing_state, location: 'Pallet Town', area_type: 'route')
raise 'expected casual FieldHealing full policy' unless casual_heal['policy'] == 'full'
raise 'expected casual FieldHealing no charge requirement' unless casual_heal['charges_remaining'] == 0
expert_healing_state = NexusRed::RuntimeState.build
NexusRed::GameplayOptions.set_difficulty(expert_healing_state, 'expert')
NexusRed::FieldHealing.unlock(expert_healing_state, source: 'Expert care kit', charges: 1, area_type: 'route')
raise 'expected expert FieldHealing route available' unless NexusRed::FieldHealing.available?(expert_healing_state, area_type: 'route')
restricted_heal = NexusRed::FieldHealing.heal_team(expert_healing_state, location: 'Mt. Moon', area_type: 'cave')
raise 'expected restricted FieldHealing cave guard' unless restricted_heal['status'] == 'restricted_area'

kanto_story_state = NexusRed::RuntimeState.build
kanto_story = NexusRed::KantoStory.ensure_kanto_story(kanto_story_state)
raise 'expected KantoStory act 1 default' unless kanto_story['current_act'] == 'act_1_pallet_to_pewter'
raise 'expected Brock rewards not applied by default' if NexusRed::KantoStory.brock_rewards_applied?(kanto_story_state)
brock_clear = NexusRed::KantoStory.complete_brock(
  kanto_story_state,
  location: 'Pewter Gym',
  area_type: 'route'
)
raise 'expected KantoStory Brock reward applied status' unless brock_clear['status'] == 'applied'
raise 'expected KantoStory Brock flag recorded' unless kanto_story_state['story_flags'].include?('boulder_badge_obtained')
raise 'expected KantoStory Nexus Boulder flag recorded' unless kanto_story_state['story_flags'].include?('FLAG_NEXUS_BOULDER_BADGE')
raise 'expected KantoStory Pewter Rocket alert flag recorded' unless kanto_story_state['story_flags'].include?('FLAG_NEXUS_PEWTER_ROCKET_ALERT')
raise 'expected KantoStory after Brock QoL tier recorded' unless kanto_story_state['gameplay_options']['latest_qol_unlock'] == 'after_brock'
raise 'expected KantoStory portable PC lite QoL' unless kanto_story_state['gameplay_options']['unlocked_qol'].include?('portable_pc_lite')
raise 'expected KantoStory rare candy mart unlocked' unless NexusRed::GameplayOptions.rare_candy_mart_available?(kanto_story_state)
raise 'expected KantoStory Pewter mart rare candies' unless NexusRed::CenterMartServices.mart_inventory(kanto_story_state, 'pewter').include?('rare_candies')
raise 'expected KantoStory PortablePC unlocked' unless NexusRed::PortablePC.unlocked?(kanto_story_state)
raise 'expected KantoStory PortablePC lite access' unless kanto_story_state['portable_pc']['access_level'] == 'lite'
raise 'expected KantoStory FieldHealing unlocked' unless NexusRed::FieldHealing.available?(kanto_story_state, area_type: 'route')
raise 'expected KantoStory standard field healing charges' unless kanto_story_state['field_healing']['charges'] == 3
raise 'expected KantoStory Red scene recorded' unless kanto_story_state['companion_progress']['red']['scene_flags'].include?('post_brock_field_kit')
raise 'expected KantoStory Brock scene recorded' unless kanto_story_state['companion_progress']['brock']['scene_flags'].include?('post_gym_respect')
raise 'expected KantoStory Brock rewards applied helper' unless NexusRed::KantoStory.brock_rewards_applied?(kanto_story_state)
second_brock_clear = NexusRed::KantoStory.complete_brock(kanto_story_state, location: 'Pewter Gym', area_type: 'route')
raise 'expected KantoStory Brock rewards idempotent guard' unless second_brock_clear['status'] == 'already_applied'
raise 'expected KantoStory no duplicate reward history' unless kanto_story_state['kanto_story']['reward_history'].length == 1
pre_brock_museum = NexusRed::KantoStory.complete_pewter_museum_anomaly(NexusRed::RuntimeState.build)
raise 'expected KantoStory museum gated before Brock' unless pre_brock_museum['status'] == 'blocked_missing_boulder_badge'
museum_clear = NexusRed::KantoStory.complete_pewter_museum_anomaly(
  kanto_story_state,
  location: 'Pewter Museum Service Tunnel',
  area_type: 'villain_hideout',
  partner_id: 'red'
)
raise 'expected KantoStory museum clear status' unless museum_clear['status'] == 'cleared'
raise 'expected KantoStory museum flag recorded' unless kanto_story_state['story_flags'].include?('FLAG_NEXUS_MUSEUM_ROCKET_EVENT_DONE')
raise 'expected KantoStory museum cleared event recorded' unless kanto_story_state['kanto_story']['cleared_events'].include?('pewter_rocket_fossil_scan_theft')
raise 'expected KantoStory museum helper true' unless NexusRed::KantoStory.museum_anomaly_cleared?(kanto_story_state)
raise 'expected KantoStory Rocket activity recorded' unless kanto_story_state['faction_progress']['team_rocket']['region_activity']['kanto'].any? { |activity| activity['location'] == 'Pewter Museum Service Tunnel' && activity['operation'] == 'fossil_scan_theft' }
raise 'expected KantoStory Phoenix conflict recorded' unless kanto_story_state['faction_progress']['team_rocket']['conflicts'].any? { |conflict| conflict['opponent'] == 'team_phoenix' && conflict['location'] == 'Pewter Museum Service Tunnel' }
raise 'expected KantoStory Phoenix foreshadowed' unless kanto_story_state['faction_progress']['team_phoenix']['conflicts'].any? { |conflict| conflict['opponent'] == 'team_rocket' }
raise 'expected KantoStory Red museum backup scene' unless kanto_story_state['companion_progress']['red']['scene_flags'].include?('pewter_museum_backup')
raise 'expected KantoStory museum WorldLink paused in hideout' unless kanto_story_state['worldlink_paused_messages'].any? { |message| message['source'] == 'kanto_story' && message['category'] == 'story_alert' }
second_museum_clear = NexusRed::KantoStory.complete_pewter_museum_anomaly(kanto_story_state)
raise 'expected KantoStory museum clear idempotent guard' unless second_museum_clear['status'] == 'already_cleared'
raise 'expected KantoStory no duplicate museum history' unless kanto_story_state['kanto_story']['event_history'].count { |event| event['event_id'] == 'pewter_rocket_fossil_scan_theft' } == 1
pre_museum_mt_moon = NexusRed::KantoStory.complete_mt_moon_operation(NexusRed::RuntimeState.build)
raise 'expected KantoStory Mt Moon gated before museum clue' unless pre_museum_mt_moon['status'] == 'blocked_missing_museum_clue'
mt_moon_clear = NexusRed::KantoStory.complete_mt_moon_operation(
  kanto_story_state,
  location: 'Mt. Moon Depths',
  area_type: 'cave',
  rival_id: 'ava'
)
raise 'expected KantoStory Mt Moon clear status' unless mt_moon_clear['status'] == 'cleared'
raise 'expected KantoStory Mt Moon operation event recorded' unless kanto_story_state['kanto_story']['cleared_events'].include?('mt_moon_rocket_moon_stone_operation')
raise 'expected KantoStory Gold Dust invoice event recorded' unless kanto_story_state['kanto_story']['cleared_events'].include?('gold_dust_invoice_hint')
raise 'expected KantoStory Ava Clefairy notes event recorded' unless kanto_story_state['kanto_story']['cleared_events'].include?('ava_clefairy_night_notes')
raise 'expected KantoStory Mt Moon helper true' unless NexusRed::KantoStory.mt_moon_operation_cleared?(kanto_story_state)
raise 'expected KantoStory Gold Dust invoice helper true' unless NexusRed::KantoStory.gold_dust_invoice_found?(kanto_story_state)
raise 'expected KantoStory Rocket Mt Moon activity recorded' unless kanto_story_state['faction_progress']['team_rocket']['region_activity']['kanto'].any? { |activity| activity['location'] == 'Mt. Moon Depths' && activity['operation'] == 'moon_stone_extraction' }
raise 'expected KantoStory Gold Dust invoice activity recorded' unless kanto_story_state['faction_progress']['team_gold_dust']['region_activity']['kanto'].any? { |activity| activity['operation'] == 'invoice_laundering_hint' }
raise 'expected KantoStory Rocket Gold Dust conflict recorded' unless kanto_story_state['faction_progress']['team_rocket']['conflicts'].any? { |conflict| conflict['opponent'] == 'team_gold_dust' && conflict['location'] == 'Mt. Moon Depths' }
raise 'expected KantoStory Ava Mt Moon rival clue recorded' unless kanto_story_state['rival_progress']['ava']['latest_activity']['category'] == 'rival_story_clue'
raise 'expected KantoStory Ava Clefairy note summary' unless kanto_story_state['rival_progress']['ava']['latest_activity']['summary'].include?('Clefairy')
raise 'expected KantoStory Mt Moon story alert paused in cave' unless kanto_story_state['worldlink_paused_messages'].any? { |message| message['source'] == 'kanto_story' && message['category'] == 'story_alert' && message['text'].include?('Mt. Moon') }
second_mt_moon_clear = NexusRed::KantoStory.complete_mt_moon_operation(kanto_story_state)
raise 'expected KantoStory Mt Moon idempotent guard' unless second_mt_moon_clear['status'] == 'already_cleared'
raise 'expected KantoStory no duplicate Mt Moon history' unless kanto_story_state['kanto_story']['event_history'].count { |event| event['event_id'] == 'mt_moon_rocket_moon_stone_operation' } == 1
pre_mt_moon_bridge = NexusRed::KantoStory.complete_nugget_bridge_qualifier(NexusRed::RuntimeState.build)
raise 'expected KantoStory Nugget Bridge gated before Mt Moon' unless pre_mt_moon_bridge['status'] == 'blocked_missing_mt_moon_clear'
nugget_bridge = NexusRed::KantoStory.complete_nugget_bridge_qualifier(
  kanto_story_state,
  location: 'Nugget Bridge',
  area_type: 'route',
  rival_ids: %w[blue ava dax]
)
raise 'expected KantoStory Nugget Bridge clear status' unless nugget_bridge['status'] == 'cleared'
raise 'expected KantoStory Nugget Bridge event recorded' unless kanto_story_state['kanto_story']['cleared_events'].include?('nugget_bridge_world_circuit_qualifier')
raise 'expected KantoStory Nugget Bridge helper true' unless NexusRed::KantoStory.nugget_bridge_qualifier_cleared?(kanto_story_state)
raise 'expected KantoStory World Circuit flag' unless kanto_story_state['story_flags'].include?('FLAG_NEXUS_NUGGET_BRIDGE_WORLD_CIRCUIT')
raise 'expected KantoStory Cerulean crisis flag' unless kanto_story_state['story_flags'].include?('FLAG_NEXUS_CERULEAN_BRIDGE_CRISIS_DONE')
raise 'expected KantoStory Rocket bridge activity recorded' unless kanto_story_state['faction_progress']['team_rocket']['region_activity']['kanto'].any? { |activity| activity['location'] == 'Nugget Bridge' && activity['operation'] == 'bridge_recruitment_probe' }
raise 'expected KantoStory Blue qualifier update' unless kanto_story_state['rival_progress']['blue']['latest_activity']['category'] == 'rival_story_clue'
raise 'expected KantoStory Dax qualifier update' unless kanto_story_state['rival_progress']['dax']['latest_activity']['summary'].include?('World Circuit')
raise 'expected KantoStory Misty activated' unless kanto_story_state['companion_progress']['misty']['active'] == true
raise 'expected KantoStory Misty not following before Route 25' if kanto_story_state['companion_progress']['misty']['following']
raise 'expected KantoStory Misty bridge scene' unless kanto_story_state['companion_progress']['misty']['scene_flags'].include?('cerulean_bridge_crisis')
raise 'expected KantoStory current act remains Act 2 before Misty battle' unless kanto_story_state['kanto_story']['current_act'] == 'act_2_pewter_to_cerulean'
raise 'expected KantoStory Nugget Bridge story alert immediate' unless kanto_story_state['worldlink_recent_messages'].any? { |message| message['source'] == 'kanto_story' && message['category'] == 'story_alert' && message['text'].include?('Nugget Bridge') }
second_nugget_bridge = NexusRed::KantoStory.complete_nugget_bridge_qualifier(kanto_story_state)
raise 'expected KantoStory Nugget Bridge idempotent guard' unless second_nugget_bridge['status'] == 'already_cleared'
raise 'expected KantoStory no duplicate Nugget Bridge history' unless kanto_story_state['kanto_story']['event_history'].count { |event| event['event_id'] == 'nugget_bridge_world_circuit_qualifier' } == 1
pre_bridge_misty = NexusRed::KantoStory.complete_misty_battle(NexusRed::RuntimeState.build)
raise 'expected KantoStory Misty gated before Nugget Bridge' unless pre_bridge_misty['status'] == 'blocked_missing_nugget_bridge_clear'
misty_clear = NexusRed::KantoStory.complete_misty_battle(
  kanto_story_state,
  gym_location: 'Cerulean Gym',
  join_location: 'Route 25',
  area_type: 'route'
)
raise 'expected KantoStory Misty clear status' unless misty_clear['status'] == 'cleared'
raise 'expected KantoStory Misty battle event recorded' unless kanto_story_state['kanto_story']['cleared_events'].include?('misty_battle')
raise 'expected KantoStory Misty helper true' unless NexusRed::KantoStory.misty_battle_cleared?(kanto_story_state)
raise 'expected KantoStory Cascade Badge flag' unless kanto_story_state['story_flags'].include?('cascade_badge_obtained')
raise 'expected KantoStory Nexus Cascade flag' unless kanto_story_state['story_flags'].include?('FLAG_NEXUS_CASCADE_BADGE')
raise 'expected KantoStory Route 25 Misty companion flag' unless kanto_story_state['story_flags'].include?('FLAG_NEXUS_MISTY_ROUTE25_COMPANION')
raise 'expected KantoStory rematch board tier flag' unless kanto_story_state['story_flags'].include?('FLAG_NEXUS_REMATCH_BOARD_TIER_1')
raise 'expected KantoStory Old Rod unlocked after Misty' unless kanto_story_state['encounter_world']['unlocked_fishing_rods'].include?('old_rod')
raise 'expected KantoStory Misty following after Route 25' unless kanto_story_state['companion_progress']['misty']['following'] == true
raise 'expected KantoStory Misty post gym scene' unless kanto_story_state['companion_progress']['misty']['scene_flags'].include?('post_gym_respect')
raise 'expected KantoStory Misty Route 25 scene' unless kanto_story_state['companion_progress']['misty']['scene_flags'].include?('route_25_companion_entry')
raise 'expected KantoStory current act advances to Act 3' unless kanto_story_state['kanto_story']['current_act'] == 'act_3_cerulean_to_vermilion'
raise 'expected KantoStory Misty story alert immediate' unless kanto_story_state['worldlink_recent_messages'].any? { |message| message['source'] == 'kanto_story' && message['category'] == 'story_alert' && message['text'].include?('Misty') }
second_misty_clear = NexusRed::KantoStory.complete_misty_battle(kanto_story_state)
raise 'expected KantoStory Misty idempotent guard' unless second_misty_clear['status'] == 'already_cleared'
raise 'expected KantoStory no duplicate Misty history' unless kanto_story_state['kanto_story']['event_history'].count { |event| event['event_id'] == 'misty_battle' } == 1
casual_kanto_state = NexusRed::RuntimeState.build
NexusRed::GameplayOptions.set_difficulty(casual_kanto_state, 'casual')
raise 'expected KantoStory casual field healing charge recommendation zero' unless NexusRed::KantoStory.field_healing_charges_for(casual_kanto_state) == 0
expert_kanto_state = NexusRed::RuntimeState.build
NexusRed::GameplayOptions.set_difficulty(expert_kanto_state, 'expert')
raise 'expected KantoStory expert field healing charge recommendation one' unless NexusRed::KantoStory.field_healing_charges_for(expert_kanto_state) == 1

migration_state = NexusRed::RuntimeState.build
migration = NexusRed::EarlyMigrationEncounters.ensure_migration(migration_state)
raise 'expected pre-Brock migration level cap context' unless migration['level_cap_context'] == 'pre_brock'
raise 'expected three route targets in migration runtime' unless migration['route_targets'].length == 3
raise 'expected Route 1 target helper' unless NexusRed::EarlyMigrationEncounters.route_target('route_1')['display_name'] == 'Route 1'
raise 'expected unknown route target nil' unless NexusRed::EarlyMigrationEncounters.route_target('route_99').nil?
raise 'expected starter gate before migration encounters' unless NexusRed::EarlyMigrationEncounters.available_for_route(migration_state, 'route_1').empty?
NexusRed::StarterSelection.select_partner(migration_state, 'Bulbasaur')
route_1_morning = NexusRed::EarlyMigrationEncounters.available_for_route(
  migration_state,
  'route_1',
  time: 'morning',
  max_level: 5
)
raise 'expected Route 1 morning Bulbasaur encounter' unless route_1_morning.any? { |encounter| encounter['species'] == 'Bulbasaur' }
raise 'expected Route 1 morning excludes Charmander day slot' if route_1_morning.any? { |encounter| encounter['species'] == 'Charmander' }
raise 'expected Route 2 gated before forest gate' unless NexusRed::EarlyMigrationEncounters.available_for_route(migration_state, 'route_2').empty?
raise 'expected Route 1 catchable species includes Rockruff' unless NexusRed::EarlyMigrationEncounters.catchable_species(migration_state, 'route_1').include?('Rockruff')
raise 'expected Route 2 catchable species includes Dratini' unless NexusRed::EarlyMigrationEncounters.catchable_species(migration_state, 'route_2').include?('Dratini')
raise 'expected Route 3 catchable species includes Kubfu' unless NexusRed::EarlyMigrationEncounters.catchable_species(migration_state, 'route_3').include?('Kubfu')
raise 'expected rare power species across early routes' unless NexusRed::EarlyMigrationEncounters.rare_power_species(migration_state) == %w[Dratini Larvitar Kubfu]
story_flags = migration_state['story_flags']
story_flags << 'route_2_forest_gate_reached'
story_flags << 'boulder_badge_obtained'
raise 'expected Route 2 night Dratini available after forest gate' unless NexusRed::EarlyMigrationEncounters.available_for_route(migration_state, 'route_2', time: 'night').any? { |encounter| encounter['species'] == 'Dratini' }
raise 'expected Route 3 day Kubfu available after Boulder Badge' unless NexusRed::EarlyMigrationEncounters.available_for_route(migration_state, 'route_3', time: 'day').any? { |encounter| encounter['species'] == 'Kubfu' }
raise 'expected over-level migration encounters filtered out' unless NexusRed::EarlyMigrationEncounters.available_for_route(migration_state, 'route_3', max_level: 6).none? { |encounter| encounter['species'] == 'Grookey' }

event_state = NexusRed::RuntimeState.build
NexusRed::StarterSelection.select_partner(event_state, 'Bulbasaur')
event_payload = NexusRed::EarlyMigrationEncounters.prepare_map_event_encounter(
  event_state,
  'route_1',
  time: 'morning',
  max_level: 5
)
raise 'expected map event payload for Route 1 migration' if event_payload.nil?
raise 'expected map event payload species Bulbasaur' unless event_payload['species'] == 'Bulbasaur'
raise 'expected map event PSDK species key' unless event_payload['psdk_species_key'] == 'BULBASAUR'
raise 'expected map event route id' unless event_payload['route_id'] == 'route_1'
raise 'expected map event map id' unless event_payload['psdk_map_id'] == 'kanto_route_1'
raise 'expected map event channel wild grass' unless event_payload['channel'] == 'wild_grass'
raise 'expected migration seen entry recorded' unless event_state['pokedex']['seen_species']['Bulbasaur'].first['location'] == 'Route 1'
raise 'expected migration seen WorldLink message' unless event_state['worldlink_recent_messages'].any? { |message| message['category'] == 'pokedex_update' && message['text'].include?('Bulbasaur') }
NexusRed::PokedexAvailability.record_caught(event_state, 'Bulbasaur', location: 'Route 1', channel: 'wild_grass', area_type: 'route')
next_payload = NexusRed::EarlyMigrationEncounters.prepare_map_event_encounter(
  event_state,
  'route_1',
  time: 'morning',
  max_level: 5
)
raise 'expected caught migration species skipped' unless next_payload['species'] == 'Chikorita'

blocked_route_1_state = NexusRed::RuntimeState.build
blocked_route_1_request = NexusRed::Route1MigrationEvent.trigger(blocked_route_1_state, time: 'morning', max_level: 5)
raise 'expected Route 1 migration event gated before starter choice' unless blocked_route_1_request['status'] == 'no_encounter'
raise 'expected no pending battle before Route 1 migration unlock' unless NexusRed::MapEventBridge.pending_battle_request(blocked_route_1_state).nil?

route_1_event_state = NexusRed::RuntimeState.build
NexusRed::StarterSelection.select_partner(route_1_event_state, 'Bulbasaur')
route_1_request = NexusRed::Route1MigrationEvent.trigger(route_1_event_state, time: 'morning', max_level: 5)
raise 'expected Route 1 migration battle request prepared' unless route_1_request['status'] == 'prepared'
raise 'expected Route 1 migration battle request kind' unless route_1_request['kind'] == 'wild_migration'
raise 'expected Route 1 migration battle request species' unless route_1_request['species'] == 'Bulbasaur'
raise 'expected Route 1 migration battle request map id' unless route_1_request['psdk_map_id'] == 'kanto_route_1'
raise 'expected pending battle request stored' unless NexusRed::MapEventBridge.pending_battle_request(route_1_event_state) == route_1_request
raise 'expected Route 1 event history recorded' unless route_1_event_state['map_event_history'].any? { |event| event['event_id'] == 'route_1_migration_event' && event['species'] == 'Bulbasaur' }
consumed_request = NexusRed::MapEventBridge.consume_pending_battle_request(route_1_event_state)
raise 'expected consumed request to match pending request' unless consumed_request == route_1_request
raise 'expected pending battle request cleared after consume' unless NexusRed::MapEventBridge.pending_battle_request(route_1_event_state).nil?
NexusRed::PokedexAvailability.record_caught(route_1_event_state, 'Bulbasaur', location: 'Route 1', channel: 'wild_grass', area_type: 'route')
second_route_1_request = NexusRed::Route1MigrationEvent.trigger(route_1_event_state, time: 'morning', max_level: 5)
raise 'expected Route 1 migration adapter skips caught Bulbasaur' unless second_route_1_request['species'] == 'Chikorita'
no_pending_launch = NexusRed::WildBattleLauncher.launch_pending_request(NexusRed::RuntimeState.build)
raise 'expected no-op launch status without pending request' unless no_pending_launch['status'] == 'no_pending_battle'
route_1_launch_state = NexusRed::RuntimeState.build
NexusRed::StarterSelection.select_partner(route_1_launch_state, 'Bulbasaur')
NexusRed::Route1MigrationEvent.trigger(route_1_launch_state, time: 'morning', max_level: 5)
launch_payload = NexusRed::WildBattleLauncher.launch_pending_request(route_1_launch_state)
raise 'expected wild battle launch status prepared' unless launch_payload['status'] == 'launch_prepared'
raise 'expected wild battle launch consumes pending request' unless NexusRed::MapEventBridge.pending_battle_request(route_1_launch_state).nil?
raise 'expected wild battle launch species key' unless launch_payload['species_key'] == 'BULBASAUR'
raise 'expected wild battle launch level' unless launch_payload['level'] == 4
raise 'expected wild battle launch source event id' unless launch_payload['source_event_id'] == 'route_1_migration_event'
raise 'expected wild battle launch command family' unless launch_payload['psdk_command_family'] == 'wild_battle'
raise 'expected wild battle launch PSDK BattleInfo strategy' unless launch_payload['psdk_binding_strategy'] == 'battle_info_wild_party'
raise 'expected wild battle launch species symbol' unless launch_payload['psdk_species_symbol'] == 'bulbasaur'
raise 'expected scaffold PSDK runtime unavailable in smoke test' if launch_payload['psdk_runtime_available']
raise 'expected wild battle launch script initializes BattleInfo' unless launch_payload['psdk_script_lines'].include?('bi = Battle::Logic::BattleInfo.new')
raise 'expected wild battle launch script feeds player party' unless launch_payload['psdk_script_lines'].include?('bi.add_party(0, *bi.player_basic_info)')
raise 'expected wild battle launch script generates wild Pokemon' unless launch_payload['psdk_script_lines'].include?('party << PFM::Pokemon.generate_from_hash(id: :bulbasaur, level: 4)')
raise 'expected wild battle launch script feeds wild party' unless launch_payload['psdk_script_lines'].include?('bi.add_party(1, party)')
raise 'expected wild battle launch script calls Battle Scene' unless launch_payload['psdk_script_lines'].include?('$scene.call_scene(Battle::Scene, bi)')
raise 'expected WildBattleLauncher species symbol helper' unless NexusRed::WildBattleLauncher.species_symbol('BULBASAUR') == 'bulbasaur'
raise 'expected wild battle launch history recorded' unless NexusRed::WildBattleLauncher.launch_history(route_1_launch_state).last == launch_payload
capture_result = NexusRed::WildBattleResults.record_result(route_1_launch_state, outcome: 'caught')
raise 'expected captured battle result status' unless capture_result['status'] == 'recorded'
raise 'expected captured battle result outcome' unless capture_result['outcome'] == 'caught'
raise 'expected captured battle result species' unless capture_result['species'] == 'Bulbasaur'
raise 'expected captured battle result stored in party' unless capture_result['storage'] == 'party'
raise 'expected captured battle result recorded in history' unless NexusRed::WildBattleResults.result_history(route_1_launch_state).last == capture_result
raise 'expected captured species in Pokedex caught state' unless route_1_launch_state['pokedex']['caught_species'].key?('Bulbasaur')
raise 'expected captured species added to party' unless route_1_launch_state['party_species'].include?('Bulbasaur')
next_after_capture = NexusRed::Route1MigrationEvent.trigger(route_1_launch_state, time: 'morning', max_level: 5)
raise 'expected Route 1 migration result handler advances to Chikorita after caught Bulbasaur' unless next_after_capture['species'] == 'Chikorita'
full_party_state = NexusRed::RuntimeState.build
full_party_state['party_species'] = %w[Charmander Squirtle Pikachu Eevee Ralts Rockruff]
full_party_state['story_flags'] = ['starter_chosen']
NexusRed::Route1MigrationEvent.trigger(full_party_state, time: 'morning', max_level: 5)
NexusRed::WildBattleLauncher.launch_pending_request(full_party_state)
pc_capture_result = NexusRed::WildBattleResults.record_result(full_party_state, outcome: 'caught')
raise 'expected full-party capture stored in PC' unless pc_capture_result['storage'] == 'pc'
raise 'expected PC box species initialized' unless full_party_state['pc_box_species'].include?('Bulbasaur')
raise 'expected full party length unchanged' unless full_party_state['party_species'].length == 6
seen_result_state = NexusRed::RuntimeState.build
NexusRed::StarterSelection.select_partner(seen_result_state, 'Bulbasaur')
NexusRed::Route1MigrationEvent.trigger(seen_result_state, time: 'morning', max_level: 5)
NexusRed::WildBattleLauncher.launch_pending_request(seen_result_state)
seen_result = NexusRed::WildBattleResults.record_result(seen_result_state, outcome: 'fled')
raise 'expected non-capture battle result recorded' unless seen_result['status'] == 'recorded'
raise 'expected non-capture result not caught' if seen_result_state['pokedex']['caught_species'].key?('Bulbasaur')
no_launch_result = NexusRed::WildBattleResults.record_result(NexusRed::RuntimeState.build, outcome: 'caught')
raise 'expected no launch result guarded' unless no_launch_result['status'] == 'no_launch'

stub_route_1_state = NexusRed::RuntimeState.build
NexusRed::StarterSelection.select_partner(stub_route_1_state, 'Bulbasaur')
NexusRed::Route1MigrationEvent.trigger(stub_route_1_state, time: 'morning', max_level: 5)
module Battle
  class Scene
  end

  module Logic
    class BattleInfo
      attr_reader :added_parties

      def initialize
        @added_parties = []
      end

      def player_basic_info
        [[:player_party], 'Antman', 'Trainer', 'antman_battler', :bag, 0, 1]
      end

      def add_party(bank, *args)
        @added_parties << [bank, args]
      end
    end
  end
end

module PFM
  class Pokemon
    class << self
      attr_reader :generated_hashes
    end

    @generated_hashes = []

    def self.generate_from_hash(hash)
      @generated_hashes << hash
      { generated_pokemon: hash }
    end
  end
end

class NexusRedStubScene
  attr_reader :calls

  def initialize
    @calls = []
  end

  def call_scene(scene_class, battle_info)
    @calls << [scene_class, battle_info]
  end
end

$scene = NexusRedStubScene.new
executed_payload = NexusRed::WildBattleLauncher.execute_pending_request(stub_route_1_state)
raise 'expected stub PSDK runtime available' unless executed_payload['psdk_runtime_available']
raise 'expected execute status when PSDK runtime available' unless executed_payload['status'] == 'battle_scene_called'
raise 'expected generated Bulbasaur hash' unless PFM::Pokemon.generated_hashes.last == { id: :bulbasaur, level: 4 }
raise 'expected Battle Scene called once' unless $scene.calls.length == 1
raise 'expected Battle Scene class passed' unless $scene.calls.first.first == Battle::Scene
stub_battle_info = $scene.calls.first.last
raise 'expected player party added to bank 0' unless stub_battle_info.added_parties.first.first == 0
raise 'expected wild party added to bank 1' unless stub_battle_info.added_parties.last.first == 1
raise 'expected executed launch history recorded' unless NexusRed::WildBattleLauncher.launch_history(stub_route_1_state).last == executed_payload
Object.send(:remove_const, :Battle)
Object.send(:remove_const, :PFM)
Object.send(:remove_const, :NexusRedStubScene)
$scene = nil

route_2_event_state = NexusRed::RuntimeState.build
NexusRed::StarterSelection.select_partner(route_2_event_state, 'Bulbasaur')
blocked_route_2_request = NexusRed::Route2MigrationEvent.trigger(route_2_event_state, time: 'morning', max_level: 6)
raise 'expected Route 2 migration event gated before forest gate' unless blocked_route_2_request['status'] == 'no_encounter'
route_2_event_state['story_flags'] << 'route_2_forest_gate_reached'
route_2_request = NexusRed::Route2MigrationEvent.trigger(route_2_event_state, time: 'morning', max_level: 6)
raise 'expected Route 2 migration battle request prepared' unless route_2_request['status'] == 'prepared'
raise 'expected Route 2 migration battle request species' unless route_2_request['species'] == 'Treecko'
raise 'expected Route 2 migration battle request map id' unless route_2_request['psdk_map_id'] == 'kanto_route_2_forest_gate'
raise 'expected Route 2 event history recorded' unless route_2_event_state['map_event_history'].any? { |event| event['event_id'] == 'route_2_migration_event' && event['species'] == 'Treecko' }
direct_route_2_state = NexusRed::RuntimeState.build
NexusRed::StarterSelection.select_partner(direct_route_2_state, 'Bulbasaur')
direct_route_2_state['story_flags'] << 'route_2_forest_gate_reached'
direct_route_2_request = NexusRed::RouteMigrationEventAdapter.trigger_route(
  direct_route_2_state,
  event_id: 'route_2_direct_migration_event',
  route_id: 'route_2',
  time: 'morning',
  max_level: 6
)
raise 'expected shared route migration adapter to prepare Route 2' unless direct_route_2_request['status'] == 'prepared'
raise 'expected shared route migration adapter event id' unless direct_route_2_request['event_id'] == 'route_2_direct_migration_event'
raise 'expected shared route migration adapter species Treecko' unless direct_route_2_request['species'] == 'Treecko'

route_3_event_state = NexusRed::RuntimeState.build
NexusRed::StarterSelection.select_partner(route_3_event_state, 'Bulbasaur')
blocked_route_3_request = NexusRed::Route3MigrationEvent.trigger(route_3_event_state, time: 'morning', max_level: 7)
raise 'expected Route 3 migration event gated before Boulder Badge' unless blocked_route_3_request['status'] == 'no_encounter'
route_3_event_state['story_flags'] << 'boulder_badge_obtained'
route_3_request = NexusRed::Route3MigrationEvent.trigger(route_3_event_state, time: 'morning', max_level: 7)
raise 'expected Route 3 migration battle request prepared' unless route_3_request['status'] == 'prepared'
raise 'expected Route 3 migration battle request species' unless route_3_request['species'] == 'Chespin'
raise 'expected Route 3 migration battle request map id' unless route_3_request['psdk_map_id'] == 'kanto_route_3'
raise 'expected Route 3 event history recorded' unless route_3_event_state['map_event_history'].any? { |event| event['event_id'] == 'route_3_migration_event' && event['species'] == 'Chespin' }

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
