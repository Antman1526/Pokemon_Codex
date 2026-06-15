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
    "complete_bill_storage_anomaly",
    "bill_storage_anomaly_cleared?",
    "complete_ss_anne_manifest",
    "ss_anne_manifest_cleared?",
    "rocket_manifest_found?",
    "complete_vermilion_power_sabotage",
    "vermilion_power_sabotage_cleared?",
    "complete_lt_surge_battle",
    "lt_surge_battle_cleared?",
    "complete_route_11_handoff",
    "route_11_handoff_cleared?",
    "complete_diglett_cave_detour",
    "diglett_cave_detour_cleared?",
    "complete_route_2_east_field_lab",
    "route_2_east_field_lab_cleared?",
    "complete_route_9_rock_tunnel_approach",
    "route_9_rock_tunnel_approach_cleared?",
    "complete_rock_tunnel_interior",
    "rock_tunnel_interior_cleared?",
    "complete_lavender_outskirts",
    "lavender_outskirts_cleared?",
    "complete_pokemon_tower_first_floor",
    "pokemon_tower_first_floor_cleared?",
    "complete_route_8_celadon_road",
    "route_8_celadon_road_cleared?",
    "complete_celadon_underground_path",
    "celadon_underground_path_cleared?",
    "complete_celadon_city_arrival",
    "celadon_city_arrival_cleared?",
    "complete_celadon_game_corner_exterior",
    "celadon_game_corner_exterior_cleared?",
    "complete_rocket_game_corner_guard_battle",
    "rocket_game_corner_guard_battle_cleared?",
    "complete_celadon_rocket_hideout_entry",
    "celadon_rocket_hideout_entry_cleared?",
    "complete_celadon_rocket_hideout_b1f",
    "celadon_rocket_hideout_b1f_cleared?",
    "complete_celadon_rocket_hideout_b2f",
    "celadon_rocket_hideout_b2f_cleared?",
    "complete_rocket_hideout_b2f_patrol_battle",
    "rocket_hideout_b2f_patrol_battle_cleared?",
    "storage_anomalies",
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
pre_misty_bill = NexusRed::KantoStory.complete_bill_storage_anomaly(NexusRed::RuntimeState.build)
raise 'expected KantoStory Bill gated before Misty' unless pre_misty_bill['status'] == 'blocked_missing_misty_clear'
bill_clear = NexusRed::KantoStory.complete_bill_storage_anomaly(
  kanto_story_state,
  location: "Bill's House",
  area_type: 'route'
)
raise 'expected KantoStory Bill clear status' unless bill_clear['status'] == 'cleared'
raise 'expected KantoStory Bill event recorded' unless kanto_story_state['kanto_story']['cleared_events'].include?('bill_storage_metadata_anomaly')
raise 'expected KantoStory Bill helper true' unless NexusRed::KantoStory.bill_storage_anomaly_cleared?(kanto_story_state)
raise 'expected KantoStory Bill storage flag' unless kanto_story_state['story_flags'].include?('FLAG_NEXUS_BILL_STORAGE_METADATA_ANOMALY')
raise 'expected KantoStory Route 25 systems flag' unless kanto_story_state['story_flags'].include?('FLAG_NEXUS_ROUTE25_SYSTEMS_HOOK')
raise 'expected KantoStory Bill companion active' unless kanto_story_state['companion_progress']['bill']['active'] == true
raise 'expected KantoStory Bill still not following' if kanto_story_state['companion_progress']['bill']['following']
raise 'expected KantoStory Bill storage intro scene' unless kanto_story_state['companion_progress']['bill']['scene_flags'].include?('storage_intro')
raise 'expected KantoStory Bill Route 25 systems scene' unless kanto_story_state['companion_progress']['bill']['scene_flags'].include?('route_25_systems_hook')
raise 'expected KantoStory Rocket storage probe activity' unless kanto_story_state['faction_progress']['team_rocket']['region_activity']['kanto'].any? { |activity| activity['location'] == "Bill's House" && activity['operation'] == 'storage_metadata_probe' }
raise 'expected KantoStory storage anomaly recorded' unless NexusRed::KantoStory.storage_anomalies(kanto_story_state).any? { |anomaly| anomaly['anomaly_id'] == 'route_25_storage_metadata_echo' && anomaly['source'] == 'Bill' }
raise 'expected KantoStory storage anomaly links PortablePC' unless NexusRed::KantoStory.storage_anomalies(kanto_story_state).first['linked_systems'].include?('portable_pc')
raise 'expected KantoStory Bill story alert immediate' unless kanto_story_state['worldlink_recent_messages'].any? { |message| message['source'] == 'kanto_story' && message['category'] == 'story_alert' && message['text'].include?('Bill') }
raise 'expected KantoStory current act remains Act 3' unless kanto_story_state['kanto_story']['current_act'] == 'act_3_cerulean_to_vermilion'
second_bill_clear = NexusRed::KantoStory.complete_bill_storage_anomaly(kanto_story_state)
raise 'expected KantoStory Bill idempotent guard' unless second_bill_clear['status'] == 'already_cleared'
raise 'expected KantoStory no duplicate Bill history' unless kanto_story_state['kanto_story']['event_history'].count { |event| event['event_id'] == 'bill_storage_metadata_anomaly' } == 1
pre_bill_ss_anne = NexusRed::KantoStory.complete_ss_anne_manifest(NexusRed::RuntimeState.build)
raise 'expected KantoStory S.S. Anne gated before Bill anomaly' unless pre_bill_ss_anne['status'] == 'blocked_missing_bill_anomaly'
ss_anne_clear = NexusRed::KantoStory.complete_ss_anne_manifest(
  kanto_story_state,
  location: 'S.S. Anne',
  area_type: 'route',
  rival_id: 'blue'
)
raise 'expected KantoStory S.S. Anne clear status' unless ss_anne_clear['status'] == 'cleared'
raise 'expected KantoStory S.S. Anne foreign trainer event recorded' unless kanto_story_state['kanto_story']['cleared_events'].include?('ss_anne_foreign_trainers')
raise 'expected KantoStory Blue S.S. Anne battle event recorded' unless kanto_story_state['kanto_story']['cleared_events'].include?('blue_ss_anne_battle')
raise 'expected KantoStory Rocket manifest event recorded' unless kanto_story_state['kanto_story']['cleared_events'].include?('rocket_smuggling_manifest')
raise 'expected KantoStory S.S. Anne helper true' unless NexusRed::KantoStory.ss_anne_manifest_cleared?(kanto_story_state)
raise 'expected KantoStory Rocket manifest helper true' unless NexusRed::KantoStory.rocket_manifest_found?(kanto_story_state)
raise 'expected KantoStory S.S. Anne foreign trainers flag' unless kanto_story_state['story_flags'].include?('FLAG_NEXUS_SS_ANNE_FOREIGN_TRAINERS')
raise 'expected KantoStory Blue S.S. Anne flag' unless kanto_story_state['story_flags'].include?('FLAG_NEXUS_BLUE_SS_ANNE_BATTLE')
raise 'expected KantoStory Rocket manifest flag' unless kanto_story_state['story_flags'].include?('FLAG_NEXUS_ROCKET_SMUGGLING_MANIFEST')
raise 'expected KantoStory Vermilion Surge setup flag' unless kanto_story_state['story_flags'].include?('FLAG_NEXUS_VERMILION_SURGE_SETUP')
raise 'expected KantoStory Rocket smuggling activity' unless kanto_story_state['faction_progress']['team_rocket']['region_activity']['kanto'].any? { |activity| activity['location'] == 'S.S. Anne' && activity['operation'] == 'smuggling_manifest' }
raise 'expected KantoStory Blue S.S. Anne rival clue' unless kanto_story_state['rival_progress']['blue']['latest_activity']['category'] == 'rival_story_clue'
raise 'expected KantoStory Blue S.S. Anne summary' unless kanto_story_state['rival_progress']['blue']['latest_activity']['summary'].include?('S.S. Anne')
raise 'expected KantoStory Misty S.S. Anne scene' unless kanto_story_state['companion_progress']['misty']['scene_flags'].include?('ss_anne_manifest')
raise 'expected KantoStory Red Mt Moon note scene' unless kanto_story_state['companion_progress']['red']['scene_flags'].include?('red_worldlink_mt_moon_note')
raise 'expected KantoStory S.S. Anne story alert immediate' unless kanto_story_state['worldlink_recent_messages'].any? { |message| message['source'] == 'kanto_story' && message['category'] == 'story_alert' && message['text'].include?('S.S. Anne') }
raise 'expected KantoStory S.S. Anne current act remains Act 3' unless kanto_story_state['kanto_story']['current_act'] == 'act_3_cerulean_to_vermilion'
raise 'expected KantoStory S.S. Anne next hook Surge' unless ss_anne_clear['next_hook'] == 'lt_surge_battle'
second_ss_anne_clear = NexusRed::KantoStory.complete_ss_anne_manifest(kanto_story_state)
raise 'expected KantoStory S.S. Anne idempotent guard' unless second_ss_anne_clear['status'] == 'already_cleared'
raise 'expected KantoStory no duplicate S.S. Anne history' unless kanto_story_state['kanto_story']['event_history'].count { |event| event['event_id'] == 'ss_anne_foreign_trainers' } == 1
pre_ss_anne_sabotage = NexusRed::KantoStory.complete_vermilion_power_sabotage(NexusRed::RuntimeState.build)
raise 'expected KantoStory Vermilion sabotage gated before S.S. Anne' unless pre_ss_anne_sabotage['status'] == 'blocked_missing_ss_anne_manifest'
vermilion_sabotage = NexusRed::KantoStory.complete_vermilion_power_sabotage(
  kanto_story_state,
  location: 'Vermilion Power Yard',
  area_type: 'route'
)
raise 'expected KantoStory Vermilion sabotage clear status' unless vermilion_sabotage['status'] == 'cleared'
raise 'expected KantoStory Vermilion sabotage event recorded' unless kanto_story_state['kanto_story']['cleared_events'].include?('vermilion_power_sabotage')
raise 'expected KantoStory Rocket Gas sabotage event recorded' unless kanto_story_state['kanto_story']['cleared_events'].include?('rocket_gas_power_sabotage')
raise 'expected KantoStory Team Gas debut event recorded' unless kanto_story_state['kanto_story']['cleared_events'].include?('team_gas_kanto_debut')
raise 'expected KantoStory Vermilion sabotage helper true' unless NexusRed::KantoStory.vermilion_power_sabotage_cleared?(kanto_story_state)
raise 'expected KantoStory Vermilion sabotage reached flag' unless kanto_story_state['story_flags'].include?('FLAG_NEXUS_VERMILION_POWER_SABOTAGE_REACHED')
raise 'expected KantoStory Rocket Gas sabotage flag' unless kanto_story_state['story_flags'].include?('FLAG_NEXUS_ROCKET_GAS_POWER_SABOTAGE')
raise 'expected KantoStory Team Gas debut flag' unless kanto_story_state['story_flags'].include?('FLAG_NEXUS_TEAM_GAS_KANTO_DEBUT')
raise 'expected KantoStory Red Misty Surge prep flag' unless kanto_story_state['story_flags'].include?('FLAG_NEXUS_RED_MISTY_SURGE_PREP')
raise 'expected KantoStory Bill power grid decode flag' unless kanto_story_state['story_flags'].include?('FLAG_NEXUS_BILL_POWER_GRID_DECODE')
raise 'expected KantoStory Surge gym battle unlocked flag' unless kanto_story_state['story_flags'].include?('FLAG_NEXUS_SURGE_GYM_BATTLE_UNLOCKED')
raise 'expected KantoStory Rocket power break-in activity' unless kanto_story_state['faction_progress']['team_rocket']['region_activity']['kanto'].any? { |activity| activity['location'] == 'Vermilion Power Yard' && activity['operation'] == 'power_room_break_in' }
raise 'expected KantoStory Team Gas power sabotage activity' unless kanto_story_state['faction_progress']['team_gas']['region_activity']['kanto'].any? { |activity| activity['operation'] == 'poison_exhaust_grid_sabotage' }
raise 'expected KantoStory Rocket Team Gas conflict' unless kanto_story_state['faction_progress']['team_rocket']['conflicts'].any? { |conflict| conflict['opponent'] == 'team_gas' && conflict['location'] == 'Vermilion Power Yard' }
raise 'expected KantoStory Red Surge prep scene' unless kanto_story_state['companion_progress']['red']['scene_flags'].include?('surge_prep')
raise 'expected KantoStory Misty Surge prep scene' unless kanto_story_state['companion_progress']['misty']['scene_flags'].include?('surge_prep')
raise 'expected KantoStory Bill power grid scene' unless kanto_story_state['companion_progress']['bill']['scene_flags'].include?('power_grid_decode')
raise 'expected KantoStory Vermilion sabotage story alert immediate' unless kanto_story_state['worldlink_recent_messages'].any? { |message| message['source'] == 'kanto_story' && message['category'] == 'story_alert' && message['text'].include?('Team Gas') }
raise 'expected KantoStory Vermilion sabotage next hook Surge battle' unless vermilion_sabotage['next_hook'] == 'lt_surge_battle'
second_vermilion_sabotage = NexusRed::KantoStory.complete_vermilion_power_sabotage(kanto_story_state)
raise 'expected KantoStory Vermilion sabotage idempotent guard' unless second_vermilion_sabotage['status'] == 'already_cleared'
raise 'expected KantoStory no duplicate Vermilion sabotage history' unless kanto_story_state['kanto_story']['event_history'].count { |event| event['event_id'] == 'vermilion_power_sabotage' } == 1
pre_sabotage_surge = NexusRed::KantoStory.complete_lt_surge_battle(NexusRed::RuntimeState.build)
raise 'expected KantoStory Surge gated before power sabotage' unless pre_sabotage_surge['status'] == 'blocked_missing_vermilion_sabotage'
surge_clear = NexusRed::KantoStory.complete_lt_surge_battle(
  kanto_story_state,
  location: 'Vermilion Gym',
  area_type: 'route'
)
raise 'expected KantoStory Surge clear status' unless surge_clear['status'] == 'cleared'
raise 'expected KantoStory Surge event recorded' unless kanto_story_state['kanto_story']['cleared_events'].include?('lt_surge_battle')
raise 'expected KantoStory Surge helper true' unless NexusRed::KantoStory.lt_surge_battle_cleared?(kanto_story_state)
raise 'expected KantoStory Thunder Badge flag' unless kanto_story_state['story_flags'].include?('thunder_badge_obtained')
raise 'expected KantoStory Nexus Thunder Badge flag' unless kanto_story_state['story_flags'].include?('FLAG_NEXUS_THUNDER_BADGE')
raise 'expected KantoStory Route 11 path flag' unless kanto_story_state['story_flags'].include?('FLAG_NEXUS_ROUTE11_PATH_UNLOCKED')
raise 'expected KantoStory VS Seeker flag' unless kanto_story_state['story_flags'].include?('FLAG_NEXUS_VS_SEEKER_UNLOCKED')
raise 'expected KantoStory Good Rod unlocked after Surge' unless kanto_story_state['encounter_world']['unlocked_fishing_rods'].include?('good_rod')
raise 'expected KantoStory Red post Surge scene' unless kanto_story_state['companion_progress']['red']['scene_flags'].include?('post_surge_route11')
raise 'expected KantoStory Misty Surge respect scene' unless kanto_story_state['companion_progress']['misty']['scene_flags'].include?('surge_respect_scene')
raise 'expected KantoStory Surge story alert immediate' unless kanto_story_state['worldlink_recent_messages'].any? { |message| message['source'] == 'kanto_story' && message['category'] == 'story_alert' && message['text'].include?('Thunder Badge') }
raise 'expected KantoStory current act advances to Act 4 after Surge' unless kanto_story_state['kanto_story']['current_act'] == 'act_4_rock_tunnel_celadon_lavender'
raise 'expected KantoStory Surge next hook Route 11' unless surge_clear['next_hook'] == 'route_11_handoff'
second_surge_clear = NexusRed::KantoStory.complete_lt_surge_battle(kanto_story_state)
raise 'expected KantoStory Surge idempotent guard' unless second_surge_clear['status'] == 'already_cleared'
raise 'expected KantoStory no duplicate Surge history' unless kanto_story_state['kanto_story']['event_history'].count { |event| event['event_id'] == 'lt_surge_battle' } == 1
pre_surge_route_11 = NexusRed::KantoStory.complete_route_11_handoff(NexusRed::RuntimeState.build)
raise 'expected KantoStory Route 11 gated before Surge' unless pre_surge_route_11['status'] == 'blocked_missing_thunder_badge'
route_11_handoff = NexusRed::KantoStory.complete_route_11_handoff(
  kanto_story_state,
  location: 'Route 11',
  area_type: 'route'
)
raise 'expected KantoStory Route 11 clear status' unless route_11_handoff['status'] == 'cleared'
raise 'expected KantoStory Route 11 event recorded' unless kanto_story_state['kanto_story']['cleared_events'].include?('route_11_handoff')
raise 'expected KantoStory Route 11 helper true' unless NexusRed::KantoStory.route_11_handoff_cleared?(kanto_story_state)
raise 'expected KantoStory Route 11 reached flag' unless kanto_story_state['story_flags'].include?('FLAG_NEXUS_ROUTE11_REACHED')
raise 'expected KantoStory Route 11 Red scene flag' unless kanto_story_state['story_flags'].include?('FLAG_NEXUS_RED_ROUTE11_EASTBOUND')
raise 'expected KantoStory Route 11 Misty farewell flag' unless kanto_story_state['story_flags'].include?('FLAG_NEXUS_MISTY_ROUTE11_FAREWELL')
raise 'expected KantoStory Route 11 Bill signal flag' unless kanto_story_state['story_flags'].include?('FLAG_NEXUS_BILL_ROUTE11_SIGNAL_DECODE')
raise 'expected KantoStory Route 11 Rocket Gas fallout flag' unless kanto_story_state['story_flags'].include?('FLAG_NEXUS_ROCKET_GAS_ROUTE11_FALLOUT')
raise 'expected KantoStory Route 11 Snorlax roadblock flag' unless kanto_story_state['story_flags'].include?('FLAG_NEXUS_SNORLAX_ROADBLOCK_TEASED')
raise 'expected KantoStory Route 11 Team Gas fallout activity' unless kanto_story_state['faction_progress']['team_gas']['region_activity']['kanto'].any? { |activity| activity['location'] == 'Route 11' && activity['operation'] == 'route_11_fallout' }
raise 'expected KantoStory Route 11 Rocket blame activity' unless kanto_story_state['faction_progress']['team_rocket']['region_activity']['kanto'].any? { |activity| activity['location'] == 'Route 11' && activity['operation'] == 'post_surge_blame_shift' }
raise 'expected KantoStory Red Route 11 scene' unless kanto_story_state['companion_progress']['red']['scene_flags'].include?('route_11_eastbound')
raise 'expected KantoStory Misty Route 11 farewell scene' unless kanto_story_state['companion_progress']['misty']['scene_flags'].include?('route_11_farewell')
raise 'expected KantoStory Bill Route 11 signal scene' unless kanto_story_state['companion_progress']['bill']['scene_flags'].include?('route_11_signal_decode')
raise 'expected KantoStory Route 11 story alert immediate' unless kanto_story_state['worldlink_recent_messages'].any? { |message| message['source'] == 'kanto_story' && message['category'] == 'story_alert' && message['text'].include?('Snorlax') }
raise 'expected KantoStory Route 11 next hook Diglett' unless route_11_handoff['next_hook'] == 'diglett_cave_detour'
second_route_11_handoff = NexusRed::KantoStory.complete_route_11_handoff(kanto_story_state)
raise 'expected KantoStory Route 11 idempotent guard' unless second_route_11_handoff['status'] == 'already_cleared'
raise 'expected KantoStory no duplicate Route 11 history' unless kanto_story_state['kanto_story']['event_history'].count { |event| event['event_id'] == 'route_11_handoff' } == 1
pre_route_11_diglett = NexusRed::KantoStory.complete_diglett_cave_detour(NexusRed::RuntimeState.build)
raise 'expected KantoStory Diglett Cave gated before Route 11' unless pre_route_11_diglett['status'] == 'blocked_missing_route_11_handoff'
diglett_detour = NexusRed::KantoStory.complete_diglett_cave_detour(
  kanto_story_state,
  location: "Diglett's Cave",
  area_type: 'cave'
)
raise 'expected KantoStory Diglett Cave clear status' unless diglett_detour['status'] == 'cleared'
raise 'expected KantoStory Diglett Cave event recorded' unless kanto_story_state['kanto_story']['cleared_events'].include?('diglett_cave_detour')
raise 'expected KantoStory Diglett Cave helper true' unless NexusRed::KantoStory.diglett_cave_detour_cleared?(kanto_story_state)
raise 'expected KantoStory Diglett Cave reached flag' unless kanto_story_state['story_flags'].include?('FLAG_NEXUS_DIGLETT_CAVE_DETOUR_REACHED')
raise 'expected KantoStory Diglett Cave Red guard flag' unless kanto_story_state['story_flags'].include?('FLAG_NEXUS_RED_DIGLETT_CAVE_GUARD')
raise 'expected KantoStory Diglett Cave Bill relay flag' unless kanto_story_state['story_flags'].include?('FLAG_NEXUS_BILL_DIGLETT_CAVE_RELAY_MAP')
raise 'expected KantoStory Diglett Cave Rocket Gold Dust flag' unless kanto_story_state['story_flags'].include?('FLAG_NEXUS_ROCKET_GOLD_DUST_CAVE_ARGUMENT')
raise 'expected KantoStory Diglett Cave Snorlax confirm flag' unless kanto_story_state['story_flags'].include?('FLAG_NEXUS_SNORLAX_ROUTE12_BLOCK_CONFIRMED')
raise 'expected KantoStory Echo Flute lead flag' unless kanto_story_state['story_flags'].include?('FLAG_NEXUS_ECHO_FLUTE_LEAD_SEEN')
raise 'expected KantoStory Diglett Cave Rocket survey activity' unless kanto_story_state['faction_progress']['team_rocket']['region_activity']['kanto'].any? { |activity| activity['location'] == "Diglett's Cave" && activity['operation'] == 'stolen_cave_survey_crates' }
raise 'expected KantoStory Diglett Cave Gold Dust survey activity' unless kanto_story_state['faction_progress']['team_gold_dust']['region_activity']['kanto'].any? { |activity| activity['location'] == "Diglett's Cave" && activity['operation'] == 'cave_survey_claim' }
raise 'expected KantoStory Diglett Cave Rocket Gold Dust conflict' unless kanto_story_state['faction_progress']['team_rocket']['conflicts'].any? { |conflict| conflict['opponent'] == 'team_gold_dust' && conflict['location'] == "Diglett's Cave" }
raise 'expected KantoStory Red Diglett Cave scene' unless kanto_story_state['companion_progress']['red']['scene_flags'].include?('diglett_cave_guard')
raise 'expected KantoStory Bill Diglett Cave scene' unless kanto_story_state['companion_progress']['bill']['scene_flags'].include?('diglett_cave_relay_map')
raise 'expected KantoStory Diglett Cave story alert paused in cave' unless kanto_story_state['worldlink_paused_messages'].any? { |message| message['source'] == 'kanto_story' && message['category'] == 'story_alert' && message['text'].include?('Echo Flute') }
raise 'expected KantoStory Diglett Cave next hook Route 2 lab' unless diglett_detour['next_hook'] == 'route_2_east_field_lab'
second_diglett_detour = NexusRed::KantoStory.complete_diglett_cave_detour(kanto_story_state)
raise 'expected KantoStory Diglett Cave idempotent guard' unless second_diglett_detour['status'] == 'already_cleared'
raise 'expected KantoStory no duplicate Diglett Cave history' unless kanto_story_state['kanto_story']['event_history'].count { |event| event['event_id'] == 'diglett_cave_detour' } == 1
pre_diglett_lab = NexusRed::KantoStory.complete_route_2_east_field_lab(NexusRed::RuntimeState.build)
raise 'expected KantoStory Route 2 east lab gated before Diglett Cave' unless pre_diglett_lab['status'] == 'blocked_missing_diglett_cave_detour'
route_2_lab = NexusRed::KantoStory.complete_route_2_east_field_lab(
  kanto_story_state,
  location: 'Route 2 East Field Lab',
  area_type: 'route'
)
raise 'expected KantoStory Route 2 east lab clear status' unless route_2_lab['status'] == 'cleared'
raise 'expected KantoStory Route 2 east lab event recorded' unless kanto_story_state['kanto_story']['cleared_events'].include?('route_2_east_field_lab')
raise 'expected KantoStory Route 2 east lab helper true' unless NexusRed::KantoStory.route_2_east_field_lab_cleared?(kanto_story_state)
raise 'expected KantoStory Route 2 east lab reached flag' unless kanto_story_state['story_flags'].include?('FLAG_NEXUS_ROUTE2_EAST_FIELD_LAB_REACHED')
raise 'expected KantoStory Red Route 2 east exit flag' unless kanto_story_state['story_flags'].include?('FLAG_NEXUS_RED_ROUTE2_EAST_EXIT')
raise 'expected KantoStory Bill Echo Flute decoder flag' unless kanto_story_state['story_flags'].include?('FLAG_NEXUS_BILL_ECHO_FLUTE_DECODER')
raise 'expected KantoStory Oak aide field tool brief flag' unless kanto_story_state['story_flags'].include?('FLAG_NEXUS_OAK_AIDE_FIELD_TOOL_BRIEF')
raise 'expected KantoStory Rocket Moonlight sleep signal flag' unless kanto_story_state['story_flags'].include?('FLAG_NEXUS_ROCKET_MOONLIGHT_SLEEP_SIGNAL')
raise 'expected KantoStory Lavender signal path flag' unless kanto_story_state['story_flags'].include?('FLAG_NEXUS_LAVENDER_SIGNAL_PATH_TEASED')
raise 'expected KantoStory Route 9 path unlock flag' unless kanto_story_state['story_flags'].include?('FLAG_NEXUS_ROUTE9_ROCK_TUNNEL_PATH_UNLOCKED')
raise 'expected KantoStory Rocket sleep residue activity' unless kanto_story_state['faction_progress']['team_rocket']['region_activity']['kanto'].any? { |activity| activity['location'] == 'Route 2 East Field Lab' && activity['operation'] == 'sleep_signal_residue' }
raise 'expected KantoStory Moonlight sleep signal activity' unless kanto_story_state['faction_progress']['team_moonlight']['region_activity']['kanto'].any? { |activity| activity['location'] == 'Route 2 East Field Lab' && activity['operation'] == 'lavender_sleep_frequency' }
raise 'expected KantoStory Rocket Moonlight overlap conflict' unless kanto_story_state['faction_progress']['team_rocket']['conflicts'].any? { |conflict| conflict['opponent'] == 'team_moonlight' && conflict['location'] == 'Route 2 East Field Lab' }
raise 'expected KantoStory Red Route 2 east scene' unless kanto_story_state['companion_progress']['red']['scene_flags'].include?('route_2_east_exit')
raise 'expected KantoStory Bill Echo Flute decoder scene' unless kanto_story_state['companion_progress']['bill']['scene_flags'].include?('echo_flute_decoder')
raise 'expected KantoStory Route 2 east lab story alert immediate' unless kanto_story_state['worldlink_recent_messages'].any? { |message| message['source'] == 'kanto_story' && message['category'] == 'story_alert' && message['text'].include?('Rock Tunnel') }
raise 'expected KantoStory Route 2 east lab next hook Route 9' unless route_2_lab['next_hook'] == 'route_9_rock_tunnel_approach'
second_route_2_lab = NexusRed::KantoStory.complete_route_2_east_field_lab(kanto_story_state)
raise 'expected KantoStory Route 2 east lab idempotent guard' unless second_route_2_lab['status'] == 'already_cleared'
raise 'expected KantoStory no duplicate Route 2 east lab history' unless kanto_story_state['kanto_story']['event_history'].count { |event| event['event_id'] == 'route_2_east_field_lab' } == 1
pre_lab_route_9 = NexusRed::KantoStory.complete_route_9_rock_tunnel_approach(NexusRed::RuntimeState.build)
raise 'expected KantoStory Route 9 gated before Route 2 east lab' unless pre_lab_route_9['status'] == 'blocked_missing_route_2_east_lab'
route_9_approach = NexusRed::KantoStory.complete_route_9_rock_tunnel_approach(
  kanto_story_state,
  location: 'Route 9',
  area_type: 'route'
)
raise 'expected KantoStory Route 9 clear status' unless route_9_approach['status'] == 'cleared'
raise 'expected KantoStory Route 9 event recorded' unless kanto_story_state['kanto_story']['cleared_events'].include?('route_9_rock_tunnel_approach')
raise 'expected KantoStory Route 9 helper true' unless NexusRed::KantoStory.route_9_rock_tunnel_approach_cleared?(kanto_story_state)
raise 'expected KantoStory Route 9 reached flag' unless kanto_story_state['story_flags'].include?('FLAG_NEXUS_ROUTE9_ROCK_TUNNEL_APPROACH_REACHED')
raise 'expected KantoStory Red Route 9 trainer lane flag' unless kanto_story_state['story_flags'].include?('FLAG_NEXUS_RED_ROUTE9_TRAINER_LANE')
raise 'expected KantoStory Bill Rock Tunnel darkness warning flag' unless kanto_story_state['story_flags'].include?('FLAG_NEXUS_BILL_ROCK_TUNNEL_DARKNESS_WARNING')
raise 'expected KantoStory Moonlight Route 9 debut flag' unless kanto_story_state['story_flags'].include?('FLAG_NEXUS_TEAM_MOONLIGHT_ROUTE9_DEBUT')
raise 'expected KantoStory Rocket Route 9 cache flag' unless kanto_story_state['story_flags'].include?('FLAG_NEXUS_ROCKET_ROUTE9_SUPPLY_CACHE')
raise 'expected KantoStory Lavender tower signal flag' unless kanto_story_state['story_flags'].include?('FLAG_NEXUS_LAVENDER_TOWER_SIGNAL_CONFIRMED')
raise 'expected KantoStory Rock Tunnel entry unlock flag' unless kanto_story_state['story_flags'].include?('FLAG_NEXUS_ROCK_TUNNEL_ENTRY_UNLOCKED')
raise 'expected KantoStory Moonlight Route 9 activity' unless kanto_story_state['faction_progress']['team_moonlight']['region_activity']['kanto'].any? { |activity| activity['location'] == 'Route 9' && activity['operation'] == 'route_9_sleep_marker' }
raise 'expected KantoStory Rocket Route 9 cache activity' unless kanto_story_state['faction_progress']['team_rocket']['region_activity']['kanto'].any? { |activity| activity['location'] == 'Route 9' && activity['operation'] == 'rock_tunnel_supply_cache' }
raise 'expected KantoStory Rocket Moonlight Route 9 conflict' unless kanto_story_state['faction_progress']['team_rocket']['conflicts'].any? { |conflict| conflict['opponent'] == 'team_moonlight' && conflict['location'] == 'Route 9' }
raise 'expected KantoStory Red Route 9 scene' unless kanto_story_state['companion_progress']['red']['scene_flags'].include?('route_9_trainer_lane')
raise 'expected KantoStory Bill Rock Tunnel warning scene' unless kanto_story_state['companion_progress']['bill']['scene_flags'].include?('rock_tunnel_darkness_warning')
raise 'expected KantoStory Route 9 story alert immediate' unless kanto_story_state['worldlink_recent_messages'].any? { |message| message['source'] == 'kanto_story' && message['category'] == 'story_alert' && message['text'].include?('Lavender') }
raise 'expected KantoStory Route 9 next hook Rock Tunnel' unless route_9_approach['next_hook'] == 'rock_tunnel_interior'
second_route_9_approach = NexusRed::KantoStory.complete_route_9_rock_tunnel_approach(kanto_story_state)
raise 'expected KantoStory Route 9 idempotent guard' unless second_route_9_approach['status'] == 'already_cleared'
raise 'expected KantoStory no duplicate Route 9 history' unless kanto_story_state['kanto_story']['event_history'].count { |event| event['event_id'] == 'route_9_rock_tunnel_approach' } == 1
pre_route_9_rock_tunnel = NexusRed::KantoStory.complete_rock_tunnel_interior(NexusRed::RuntimeState.build)
raise 'expected KantoStory Rock Tunnel gated before Route 9' unless pre_route_9_rock_tunnel['status'] == 'blocked_missing_route_9_approach'
rock_tunnel = NexusRed::KantoStory.complete_rock_tunnel_interior(
  kanto_story_state,
  location: 'Rock Tunnel',
  area_type: 'cave'
)
raise 'expected KantoStory Rock Tunnel clear status' unless rock_tunnel['status'] == 'cleared'
raise 'expected KantoStory Rock Tunnel event recorded' unless kanto_story_state['kanto_story']['cleared_events'].include?('rock_tunnel_interior')
raise 'expected KantoStory Rock Tunnel helper true' unless NexusRed::KantoStory.rock_tunnel_interior_cleared?(kanto_story_state)
raise 'expected KantoStory Rock Tunnel reached flag' unless kanto_story_state['story_flags'].include?('FLAG_NEXUS_ROCK_TUNNEL_INTERIOR_REACHED')
raise 'expected KantoStory Red Rock Tunnel guidance flag' unless kanto_story_state['story_flags'].include?('FLAG_NEXUS_RED_ROCK_TUNNEL_GUIDANCE')
raise 'expected KantoStory Bill Lavender echo trace flag' unless kanto_story_state['story_flags'].include?('FLAG_NEXUS_BILL_LAVENDER_ECHO_TRACE')
raise 'expected KantoStory Moonlight cave pressure flag' unless kanto_story_state['story_flags'].include?('FLAG_NEXUS_TEAM_MOONLIGHT_CAVE_PRESSURE')
raise 'expected KantoStory Rocket dark cache flag' unless kanto_story_state['story_flags'].include?('FLAG_NEXUS_ROCKET_DARK_CACHE')
raise 'expected KantoStory Flash Lantern needed flag' unless kanto_story_state['story_flags'].include?('FLAG_NEXUS_FLASH_LANTERN_NEEDED')
raise 'expected KantoStory Cave Lantern unlock flag' unless kanto_story_state['story_flags'].include?('FLAG_NEXUS_CAVE_LANTERN_UNLOCKED')
raise 'expected KantoStory Lavender exit path unlock flag' unless kanto_story_state['story_flags'].include?('FLAG_NEXUS_LAVENDER_EXIT_PATH_UNLOCKED')
raise 'expected KantoStory Cave Lantern field tool unlocked' unless NexusRed::FieldTools.has_tool?(kanto_story_state, 'cave_lantern')
raise 'expected KantoStory Flash replacement available' unless NexusRed::FieldTools.can_use_replacement?(kanto_story_state, 'Flash')
raise 'expected KantoStory Cave Lantern source recorded' unless kanto_story_state['field_tools']['tool_sources']['cave_lantern'] == 'Rock Tunnel dark cache'
raise 'expected KantoStory Moonlight cave pressure activity' unless kanto_story_state['faction_progress']['team_moonlight']['region_activity']['kanto'].any? { |activity| activity['location'] == 'Rock Tunnel' && activity['operation'] == 'cave_dream_pressure' }
raise 'expected KantoStory Rocket dark cache activity' unless kanto_story_state['faction_progress']['team_rocket']['region_activity']['kanto'].any? { |activity| activity['location'] == 'Rock Tunnel' && activity['operation'] == 'dark_cache_surveillance' }
raise 'expected KantoStory Rocket Moonlight Rock Tunnel conflict' unless kanto_story_state['faction_progress']['team_rocket']['conflicts'].any? { |conflict| conflict['opponent'] == 'team_moonlight' && conflict['location'] == 'Rock Tunnel' }
raise 'expected KantoStory Red Rock Tunnel scene' unless kanto_story_state['companion_progress']['red']['scene_flags'].include?('rock_tunnel_guidance')
raise 'expected KantoStory Bill Lavender echo trace scene' unless kanto_story_state['companion_progress']['bill']['scene_flags'].include?('lavender_echo_trace')
raise 'expected KantoStory Rock Tunnel story alert paused in cave' unless kanto_story_state['worldlink_paused_messages'].any? { |message| message['source'] == 'kanto_story' && message['category'] == 'story_alert' && message['text'].include?('Lavender') }
raise 'expected KantoStory Cave Lantern unlock paused in cave' unless kanto_story_state['worldlink_paused_messages'].any? { |message| message['source'] == 'field_tools' && message['text'].include?('Cave Lantern') }
raise 'expected KantoStory Rock Tunnel next hook Lavender' unless rock_tunnel['next_hook'] == 'lavender_outskirts'
second_rock_tunnel = NexusRed::KantoStory.complete_rock_tunnel_interior(kanto_story_state)
raise 'expected KantoStory Rock Tunnel idempotent guard' unless second_rock_tunnel['status'] == 'already_cleared'
raise 'expected KantoStory no duplicate Rock Tunnel history' unless kanto_story_state['kanto_story']['event_history'].count { |event| event['event_id'] == 'rock_tunnel_interior' } == 1
pre_rock_tunnel_lavender = NexusRed::KantoStory.complete_lavender_outskirts(NexusRed::RuntimeState.build)
raise 'expected KantoStory Lavender gated before Rock Tunnel' unless pre_rock_tunnel_lavender['status'] == 'blocked_missing_rock_tunnel'
lavender_outskirts = NexusRed::KantoStory.complete_lavender_outskirts(
  kanto_story_state,
  location: 'Lavender Outskirts',
  area_type: 'route'
)
raise 'expected KantoStory Lavender clear status' unless lavender_outskirts['status'] == 'cleared'
raise 'expected KantoStory Lavender event recorded' unless kanto_story_state['kanto_story']['cleared_events'].include?('lavender_outskirts')
raise 'expected KantoStory Lavender helper true' unless NexusRed::KantoStory.lavender_outskirts_cleared?(kanto_story_state)
raise 'expected KantoStory Lavender reached flag' unless kanto_story_state['story_flags'].include?('FLAG_NEXUS_LAVENDER_OUTSKIRTS_REACHED')
raise 'expected KantoStory Red Lavender arrival flag' unless kanto_story_state['story_flags'].include?('FLAG_NEXUS_RED_LAVENDER_ARRIVAL')
raise 'expected KantoStory Bill Pokemon Tower signal flag' unless kanto_story_state['story_flags'].include?('FLAG_NEXUS_BILL_POKEMON_TOWER_SIGNAL_DECODE')
raise 'expected KantoStory Moonlight Lavender presence flag' unless kanto_story_state['story_flags'].include?('FLAG_NEXUS_TEAM_MOONLIGHT_LAVENDER_PRESENCE')
raise 'expected KantoStory Rocket Lavender surveillance flag' unless kanto_story_state['story_flags'].include?('FLAG_NEXUS_ROCKET_LAVENDER_SURVEILLANCE')
raise 'expected KantoStory Pokemon Tower signal confirmed flag' unless kanto_story_state['story_flags'].include?('FLAG_NEXUS_POKEMON_TOWER_SIGNAL_CONFIRMED')
raise 'expected KantoStory Pokemon Tower entry unlock flag' unless kanto_story_state['story_flags'].include?('FLAG_NEXUS_POKEMON_TOWER_ENTRY_UNLOCKED')
raise 'expected KantoStory Moonlight Lavender pressure activity' unless kanto_story_state['faction_progress']['team_moonlight']['region_activity']['kanto'].any? { |activity| activity['location'] == 'Lavender Outskirts' && activity['operation'] == 'lavender_grief_pressure' }
raise 'expected KantoStory Rocket Lavender surveillance activity' unless kanto_story_state['faction_progress']['team_rocket']['region_activity']['kanto'].any? { |activity| activity['location'] == 'Lavender Outskirts' && activity['operation'] == 'pokemon_tower_surveillance' }
raise 'expected KantoStory Rocket Moonlight Lavender conflict' unless kanto_story_state['faction_progress']['team_rocket']['conflicts'].any? { |conflict| conflict['opponent'] == 'team_moonlight' && conflict['location'] == 'Lavender Outskirts' }
raise 'expected KantoStory Red Lavender arrival scene' unless kanto_story_state['companion_progress']['red']['scene_flags'].include?('lavender_arrival')
raise 'expected KantoStory Bill Pokemon Tower decode scene' unless kanto_story_state['companion_progress']['bill']['scene_flags'].include?('pokemon_tower_signal_decode')
raise 'expected KantoStory Lavender story alert immediate' unless kanto_story_state['worldlink_recent_messages'].any? { |message| message['source'] == 'kanto_story' && message['category'] == 'story_alert' && message['text'].include?('Pokemon Tower') }
raise 'expected KantoStory Lavender next hook Pokemon Tower' unless lavender_outskirts['next_hook'] == 'pokemon_tower_first_floor'
second_lavender_outskirts = NexusRed::KantoStory.complete_lavender_outskirts(kanto_story_state)
raise 'expected KantoStory Lavender idempotent guard' unless second_lavender_outskirts['status'] == 'already_cleared'
raise 'expected KantoStory no duplicate Lavender history' unless kanto_story_state['kanto_story']['event_history'].count { |event| event['event_id'] == 'lavender_outskirts' } == 1
pre_lavender_tower = NexusRed::KantoStory.complete_pokemon_tower_first_floor(NexusRed::RuntimeState.build)
raise 'expected KantoStory Pokemon Tower gated before Lavender' unless pre_lavender_tower['status'] == 'blocked_missing_lavender_outskirts'
pokemon_tower = NexusRed::KantoStory.complete_pokemon_tower_first_floor(
  kanto_story_state,
  location: 'Pokemon Tower 1F',
  area_type: 'story_dungeon'
)
raise 'expected KantoStory Pokemon Tower clear status' unless pokemon_tower['status'] == 'cleared'
raise 'expected KantoStory Pokemon Tower event recorded' unless kanto_story_state['kanto_story']['cleared_events'].include?('pokemon_tower_first_floor')
raise 'expected KantoStory Pokemon Tower helper true' unless NexusRed::KantoStory.pokemon_tower_first_floor_cleared?(kanto_story_state)
raise 'expected KantoStory Pokemon Tower reached flag' unless kanto_story_state['story_flags'].include?('FLAG_NEXUS_POKEMON_TOWER_FIRST_FLOOR_REACHED')
raise 'expected KantoStory Red Pokemon Tower guard flag' unless kanto_story_state['story_flags'].include?('FLAG_NEXUS_RED_POKEMON_TOWER_GUARD')
raise 'expected KantoStory Bill Tower Echo Flute distortion flag' unless kanto_story_state['story_flags'].include?('FLAG_NEXUS_BILL_TOWER_ECHO_FLUTE_DISTORTION')
raise 'expected KantoStory Moonlight tower pressure flag' unless kanto_story_state['story_flags'].include?('FLAG_NEXUS_TEAM_MOONLIGHT_TOWER_PRESSURE')
raise 'expected KantoStory Rocket tower grunt flag' unless kanto_story_state['story_flags'].include?('FLAG_NEXUS_ROCKET_TOWER_GRUNT')
raise 'expected KantoStory Cubone Mr Fuji thread flag' unless kanto_story_state['story_flags'].include?('FLAG_NEXUS_CUBONE_MR_FUJI_THREAD')
raise 'expected KantoStory Silph Scope need flag' unless kanto_story_state['story_flags'].include?('FLAG_NEXUS_SILPH_SCOPE_NEED_SEEN')
raise 'expected KantoStory tower deeper path locked flag' unless kanto_story_state['story_flags'].include?('FLAG_NEXUS_POKEMON_TOWER_DEEPER_PATH_LOCKED')
raise 'expected KantoStory Route 8 Celadon road unlock flag' unless kanto_story_state['story_flags'].include?('FLAG_NEXUS_ROUTE8_CELADON_ROAD_UNLOCKED')
raise 'expected KantoStory Moonlight tower pressure activity' unless kanto_story_state['faction_progress']['team_moonlight']['region_activity']['kanto'].any? { |activity| activity['location'] == 'Pokemon Tower 1F' && activity['operation'] == 'tower_grief_distortion' }
raise 'expected KantoStory Rocket tower grunt activity' unless kanto_story_state['faction_progress']['team_rocket']['region_activity']['kanto'].any? { |activity| activity['location'] == 'Pokemon Tower 1F' && activity['operation'] == 'tower_grunt_lookout' }
raise 'expected KantoStory Rocket Moonlight tower conflict' unless kanto_story_state['faction_progress']['team_rocket']['conflicts'].any? { |conflict| conflict['opponent'] == 'team_moonlight' && conflict['location'] == 'Pokemon Tower 1F' }
raise 'expected KantoStory Red Pokemon Tower scene' unless kanto_story_state['companion_progress']['red']['scene_flags'].include?('pokemon_tower_guard')
raise 'expected KantoStory Bill Tower distortion scene' unless kanto_story_state['companion_progress']['bill']['scene_flags'].include?('tower_echo_flute_distortion')
raise 'expected KantoStory Pokemon Tower story alert paused in dungeon' unless kanto_story_state['worldlink_paused_messages'].any? { |message| message['source'] == 'kanto_story' && message['category'] == 'story_alert' && message['text'].include?('Silph Scope') }
raise 'expected KantoStory Pokemon Tower next hook Route 8' unless pokemon_tower['next_hook'] == 'route_8_celadon_road'
second_pokemon_tower = NexusRed::KantoStory.complete_pokemon_tower_first_floor(kanto_story_state)
raise 'expected KantoStory Pokemon Tower idempotent guard' unless second_pokemon_tower['status'] == 'already_cleared'
raise 'expected KantoStory no duplicate Pokemon Tower history' unless kanto_story_state['kanto_story']['event_history'].count { |event| event['event_id'] == 'pokemon_tower_first_floor' } == 1
pre_tower_route_8 = NexusRed::KantoStory.complete_route_8_celadon_road(NexusRed::RuntimeState.build)
raise 'expected KantoStory Route 8 gated before Pokemon Tower' unless pre_tower_route_8['status'] == 'blocked_missing_pokemon_tower_first_floor'
route_8_celadon = NexusRed::KantoStory.complete_route_8_celadon_road(
  kanto_story_state,
  location: 'Route 8',
  area_type: 'route',
  rival_id: 'blue'
)
raise 'expected KantoStory Route 8 clear status' unless route_8_celadon['status'] == 'cleared'
raise 'expected KantoStory Route 8 event recorded' unless kanto_story_state['kanto_story']['cleared_events'].include?('route_8_celadon_road')
raise 'expected KantoStory Route 8 helper true' unless NexusRed::KantoStory.route_8_celadon_road_cleared?(kanto_story_state)
raise 'expected KantoStory Route 8 reached flag' unless kanto_story_state['story_flags'].include?('FLAG_NEXUS_ROUTE8_CELADON_ROAD_REACHED')
raise 'expected KantoStory Red Route 8 westbound flag' unless kanto_story_state['story_flags'].include?('FLAG_NEXUS_RED_ROUTE8_WESTBOUND')
raise 'expected KantoStory Bill Silph Scope Celadon trace flag' unless kanto_story_state['story_flags'].include?('FLAG_NEXUS_BILL_SILPH_SCOPE_CELADON_TRACE')
raise 'expected KantoStory Rocket Celadon Game Corner lead flag' unless kanto_story_state['story_flags'].include?('FLAG_NEXUS_ROCKET_CELADON_GAME_CORNER_LEAD')
raise 'expected KantoStory Moonlight Route 8 shadow flag' unless kanto_story_state['story_flags'].include?('FLAG_NEXUS_TEAM_MOONLIGHT_ROUTE8_SHADOW')
raise 'expected KantoStory Underground Path unlock flag' unless kanto_story_state['story_flags'].include?('FLAG_NEXUS_UNDERGROUND_PATH_TO_CELADON_UNLOCKED')
raise 'expected KantoStory Celadon city tease flag' unless kanto_story_state['story_flags'].include?('FLAG_NEXUS_CELADON_CITY_TEASED')
raise 'expected KantoStory Blue Route 8 crossing flag' unless kanto_story_state['story_flags'].include?('FLAG_NEXUS_BLUE_ROUTE8_SILPH_SCOPE_CROSSING')
raise 'expected KantoStory Rocket Game Corner lead activity' unless kanto_story_state['faction_progress']['team_rocket']['region_activity']['kanto'].any? { |activity| activity['location'] == 'Route 8' && activity['operation'] == 'celadon_game_corner_lead' }
raise 'expected KantoStory Moonlight Route 8 shadow activity' unless kanto_story_state['faction_progress']['team_moonlight']['region_activity']['kanto'].any? { |activity| activity['location'] == 'Route 8' && activity['operation'] == 'route_8_dream_shadow' }
raise 'expected KantoStory Rocket Moonlight Route 8 conflict' unless kanto_story_state['faction_progress']['team_rocket']['conflicts'].any? { |conflict| conflict['opponent'] == 'team_moonlight' && conflict['location'] == 'Route 8' }
raise 'expected KantoStory Red Route 8 scene' unless kanto_story_state['companion_progress']['red']['scene_flags'].include?('route_8_westbound')
raise 'expected KantoStory Bill Silph Scope Celadon trace scene' unless kanto_story_state['companion_progress']['bill']['scene_flags'].include?('silph_scope_celadon_trace')
raise 'expected KantoStory Blue Route 8 rival clue' unless kanto_story_state['rival_progress']['blue']['latest_activity']['summary'].include?('Silph Scope')
raise 'expected KantoStory Route 8 story alert immediate' unless kanto_story_state['worldlink_recent_messages'].any? { |message| message['source'] == 'kanto_story' && message['category'] == 'story_alert' && message['text'].include?('Game Corner') }
raise 'expected KantoStory Route 8 next hook Celadon Underground Path' unless route_8_celadon['next_hook'] == 'celadon_underground_path'
second_route_8_celadon = NexusRed::KantoStory.complete_route_8_celadon_road(kanto_story_state)
raise 'expected KantoStory Route 8 idempotent guard' unless second_route_8_celadon['status'] == 'already_cleared'
raise 'expected KantoStory no duplicate Route 8 history' unless kanto_story_state['kanto_story']['event_history'].count { |event| event['event_id'] == 'route_8_celadon_road' } == 1
pre_route_8_underpass = NexusRed::KantoStory.complete_celadon_underground_path(NexusRed::RuntimeState.build)
raise 'expected KantoStory Celadon Underground gated before Route 8' unless pre_route_8_underpass['status'] == 'blocked_missing_route_8_celadon_road'
celadon_underpass = NexusRed::KantoStory.complete_celadon_underground_path(
  kanto_story_state,
  location: 'Celadon Underground Path',
  area_type: 'route'
)
raise 'expected KantoStory Celadon Underground clear status' unless celadon_underpass['status'] == 'cleared'
raise 'expected KantoStory Celadon Underground event recorded' unless kanto_story_state['kanto_story']['cleared_events'].include?('celadon_underground_path')
raise 'expected KantoStory Celadon Underground helper true' unless NexusRed::KantoStory.celadon_underground_path_cleared?(kanto_story_state)
raise 'expected KantoStory Celadon Underground reached flag' unless kanto_story_state['story_flags'].include?('FLAG_NEXUS_CELADON_UNDERGROUND_PATH_REACHED')
raise 'expected KantoStory Red Celadon underpass guard flag' unless kanto_story_state['story_flags'].include?('FLAG_NEXUS_RED_CELADON_UNDERPASS_GUARD')
raise 'expected KantoStory Bill Game Corner signal trace flag' unless kanto_story_state['story_flags'].include?('FLAG_NEXUS_BILL_GAME_CORNER_SIGNAL_TRACE')
raise 'expected KantoStory Rocket underpass smuggler flag' unless kanto_story_state['story_flags'].include?('FLAG_NEXUS_ROCKET_UNDERPASS_SMUGGLER')
raise 'expected KantoStory Moonlight dream poster flag' unless kanto_story_state['story_flags'].include?('FLAG_NEXUS_TEAM_MOONLIGHT_DREAM_POSTER')
raise 'expected KantoStory Silph Scope Game Corner confirmed flag' unless kanto_story_state['story_flags'].include?('FLAG_NEXUS_SILPH_SCOPE_GAME_CORNER_CONFIRMED')
raise 'expected KantoStory Celadon City arrival unlock flag' unless kanto_story_state['story_flags'].include?('FLAG_NEXUS_CELADON_CITY_ARRIVAL_UNLOCKED')
raise 'expected KantoStory Rocket underpass smuggler activity' unless kanto_story_state['faction_progress']['team_rocket']['region_activity']['kanto'].any? { |activity| activity['location'] == 'Celadon Underground Path' && activity['operation'] == 'underpass_smuggler' }
raise 'expected KantoStory Moonlight dream poster activity' unless kanto_story_state['faction_progress']['team_moonlight']['region_activity']['kanto'].any? { |activity| activity['location'] == 'Celadon Underground Path' && activity['operation'] == 'dream_poster_lure' }
raise 'expected KantoStory Rocket Moonlight underpass conflict' unless kanto_story_state['faction_progress']['team_rocket']['conflicts'].any? { |conflict| conflict['opponent'] == 'team_moonlight' && conflict['location'] == 'Celadon Underground Path' }
raise 'expected KantoStory Red Celadon underpass scene' unless kanto_story_state['companion_progress']['red']['scene_flags'].include?('celadon_underpass_guard')
raise 'expected KantoStory Bill Game Corner signal scene' unless kanto_story_state['companion_progress']['bill']['scene_flags'].include?('game_corner_signal_trace')
raise 'expected KantoStory Celadon Underground story alert immediate' unless kanto_story_state['worldlink_recent_messages'].any? { |message| message['source'] == 'kanto_story' && message['category'] == 'story_alert' && message['text'].include?('dream poster') }
raise 'expected KantoStory Celadon Underground next hook city arrival' unless celadon_underpass['next_hook'] == 'celadon_city_arrival'
second_celadon_underpass = NexusRed::KantoStory.complete_celadon_underground_path(kanto_story_state)
raise 'expected KantoStory Celadon Underground idempotent guard' unless second_celadon_underpass['status'] == 'already_cleared'
raise 'expected KantoStory no duplicate Celadon Underground history' unless kanto_story_state['kanto_story']['event_history'].count { |event| event['event_id'] == 'celadon_underground_path' } == 1
pre_underpass_celadon_city = NexusRed::KantoStory.complete_celadon_city_arrival(NexusRed::RuntimeState.build)
raise 'expected KantoStory Celadon City gated before underpass' unless pre_underpass_celadon_city['status'] == 'blocked_missing_celadon_underground_path'
celadon_city = NexusRed::KantoStory.complete_celadon_city_arrival(
  kanto_story_state,
  location: 'Celadon City',
  area_type: 'city'
)
raise 'expected KantoStory Celadon City clear status' unless celadon_city['status'] == 'cleared'
raise 'expected KantoStory Celadon City event recorded' unless kanto_story_state['kanto_story']['cleared_events'].include?('celadon_city_arrival')
raise 'expected KantoStory Celadon City helper true' unless NexusRed::KantoStory.celadon_city_arrival_cleared?(kanto_story_state)
raise 'expected KantoStory Celadon City reached flag' unless kanto_story_state['story_flags'].include?('FLAG_NEXUS_CELADON_CITY_REACHED')
raise 'expected KantoStory Red Celadon city arrival flag' unless kanto_story_state['story_flags'].include?('FLAG_NEXUS_RED_CELADON_CITY_ARRIVAL')
raise 'expected KantoStory Bill Game Corner exterior signal flag' unless kanto_story_state['story_flags'].include?('FLAG_NEXUS_BILL_GAME_CORNER_EXTERIOR_SIGNAL')
raise 'expected KantoStory Rocket Game Corner front flag' unless kanto_story_state['story_flags'].include?('FLAG_NEXUS_ROCKET_GAME_CORNER_FRONT')
raise 'expected KantoStory Moonlight Celadon ad flag' unless kanto_story_state['story_flags'].include?('FLAG_NEXUS_TEAM_MOONLIGHT_CELADON_AD')
raise 'expected KantoStory Erika gym tease flag' unless kanto_story_state['story_flags'].include?('FLAG_NEXUS_ERIKA_GYM_TEASED')
raise 'expected KantoStory Game Corner investigation unlock flag' unless kanto_story_state['story_flags'].include?('FLAG_NEXUS_GAME_CORNER_INVESTIGATION_UNLOCKED')
raise 'expected KantoStory Rocket Game Corner front activity' unless kanto_story_state['faction_progress']['team_rocket']['region_activity']['kanto'].any? { |activity| activity['location'] == 'Celadon City' && activity['operation'] == 'game_corner_public_front' }
raise 'expected KantoStory Moonlight Celadon ad activity' unless kanto_story_state['faction_progress']['team_moonlight']['region_activity']['kanto'].any? { |activity| activity['location'] == 'Celadon City' && activity['operation'] == 'celadon_dream_ad_campaign' }
raise 'expected KantoStory Rocket Moonlight Celadon conflict' unless kanto_story_state['faction_progress']['team_rocket']['conflicts'].any? { |conflict| conflict['opponent'] == 'team_moonlight' && conflict['location'] == 'Celadon City' }
raise 'expected KantoStory Red Celadon city scene' unless kanto_story_state['companion_progress']['red']['scene_flags'].include?('celadon_city_arrival')
raise 'expected KantoStory Bill Game Corner exterior scene' unless kanto_story_state['companion_progress']['bill']['scene_flags'].include?('game_corner_exterior_signal')
raise 'expected KantoStory Celadon City story alert immediate' unless kanto_story_state['worldlink_recent_messages'].any? { |message| message['source'] == 'kanto_story' && message['category'] == 'story_alert' && message['text'].include?('Erika') && message['text'].include?('Game Corner') }
raise 'expected KantoStory Celadon City next hook Game Corner exterior' unless celadon_city['next_hook'] == 'celadon_game_corner_exterior'
second_celadon_city = NexusRed::KantoStory.complete_celadon_city_arrival(kanto_story_state)
raise 'expected KantoStory Celadon City idempotent guard' unless second_celadon_city['status'] == 'already_cleared'
raise 'expected KantoStory no duplicate Celadon City history' unless kanto_story_state['kanto_story']['event_history'].count { |event| event['event_id'] == 'celadon_city_arrival' } == 1
pre_city_game_corner = NexusRed::KantoStory.complete_celadon_game_corner_exterior(NexusRed::RuntimeState.build)
raise 'expected KantoStory Game Corner exterior gated before Celadon City' unless pre_city_game_corner['status'] == 'blocked_missing_celadon_city_arrival'
game_corner_exterior = NexusRed::KantoStory.complete_celadon_game_corner_exterior(
  kanto_story_state,
  location: 'Celadon Game Corner Exterior',
  area_type: 'city'
)
raise 'expected KantoStory Game Corner exterior clear status' unless game_corner_exterior['status'] == 'cleared'
raise 'expected KantoStory Game Corner exterior event recorded' unless kanto_story_state['kanto_story']['cleared_events'].include?('celadon_game_corner_exterior')
raise 'expected KantoStory Game Corner exterior helper true' unless NexusRed::KantoStory.celadon_game_corner_exterior_cleared?(kanto_story_state)
raise 'expected KantoStory Game Corner exterior reached flag' unless kanto_story_state['story_flags'].include?('FLAG_NEXUS_GAME_CORNER_EXTERIOR_REACHED')
raise 'expected KantoStory Red Game Corner door guard flag' unless kanto_story_state['story_flags'].include?('FLAG_NEXUS_RED_GAME_CORNER_DOOR_GUARD')
raise 'expected KantoStory Bill Coin Case signal flag' unless kanto_story_state['story_flags'].include?('FLAG_NEXUS_BILL_COIN_CASE_SIGNAL')
raise 'expected KantoStory Rocket Game Corner guard exposed flag' unless kanto_story_state['story_flags'].include?('FLAG_NEXUS_ROCKET_GAME_CORNER_GUARD_EXPOSED')
raise 'expected KantoStory Moonlight sleep coin flag' unless kanto_story_state['story_flags'].include?('FLAG_NEXUS_TEAM_MOONLIGHT_SLEEP_COIN')
raise 'expected KantoStory Game Corner guard battle unlock flag' unless kanto_story_state['story_flags'].include?('FLAG_NEXUS_GAME_CORNER_GUARD_BATTLE_UNLOCKED')
raise 'expected KantoStory Rocket Game Corner guard activity' unless kanto_story_state['faction_progress']['team_rocket']['region_activity']['kanto'].any? { |activity| activity['location'] == 'Celadon Game Corner Exterior' && activity['operation'] == 'game_corner_public_guard' }
raise 'expected KantoStory Moonlight sleep coin activity' unless kanto_story_state['faction_progress']['team_moonlight']['region_activity']['kanto'].any? { |activity| activity['location'] == 'Celadon Game Corner Exterior' && activity['operation'] == 'sleep_coin_ad_signal' }
raise 'expected KantoStory Rocket Moonlight Game Corner conflict' unless kanto_story_state['faction_progress']['team_rocket']['conflicts'].any? { |conflict| conflict['opponent'] == 'team_moonlight' && conflict['location'] == 'Celadon Game Corner Exterior' }
raise 'expected KantoStory Red Game Corner door scene' unless kanto_story_state['companion_progress']['red']['scene_flags'].include?('game_corner_door_guard')
raise 'expected KantoStory Bill Coin Case scene' unless kanto_story_state['companion_progress']['bill']['scene_flags'].include?('coin_case_signal')
raise 'expected KantoStory Game Corner story alert immediate' unless kanto_story_state['worldlink_recent_messages'].any? { |message| message['source'] == 'kanto_story' && message['category'] == 'story_alert' && message['text'].include?('Coin Case') && message['text'].include?('guard battle') }
raise 'expected KantoStory Game Corner battle hook id' unless game_corner_exterior['battle_hook']['battle_id'] == 'rocket_game_corner_guard'
raise 'expected KantoStory Game Corner next hook guard battle' unless game_corner_exterior['next_hook'] == 'rocket_game_corner_guard_battle'
second_game_corner_exterior = NexusRed::KantoStory.complete_celadon_game_corner_exterior(kanto_story_state)
raise 'expected KantoStory Game Corner exterior idempotent guard' unless second_game_corner_exterior['status'] == 'already_cleared'
raise 'expected KantoStory no duplicate Game Corner exterior history' unless kanto_story_state['kanto_story']['event_history'].count { |event| event['event_id'] == 'celadon_game_corner_exterior' } == 1
pre_exterior_guard = NexusRed::KantoStory.complete_rocket_game_corner_guard_battle(NexusRed::RuntimeState.build)
raise 'expected KantoStory Rocket Game Corner guard gated before exterior' unless pre_exterior_guard['status'] == 'blocked_missing_game_corner_exterior'
guard_battle = NexusRed::KantoStory.complete_rocket_game_corner_guard_battle(
  kanto_story_state,
  location: 'Celadon Game Corner Exterior',
  result: 'placeholder_win',
  area_type: 'city'
)
raise 'expected KantoStory Rocket Game Corner guard clear status' unless guard_battle['status'] == 'cleared'
raise 'expected KantoStory Rocket Game Corner guard battle event recorded' unless kanto_story_state['kanto_story']['cleared_events'].include?('rocket_game_corner_guard_battle')
raise 'expected KantoStory Rocket Game Corner guard helper true' unless NexusRed::KantoStory.rocket_game_corner_guard_battle_cleared?(kanto_story_state)
raise 'expected KantoStory Rocket Game Corner guard battle started flag' unless kanto_story_state['story_flags'].include?('FLAG_NEXUS_ROCKET_GAME_CORNER_GUARD_BATTLE_STARTED')
raise 'expected KantoStory Rocket Game Corner guard battle finished flag' unless kanto_story_state['story_flags'].include?('FLAG_NEXUS_ROCKET_GAME_CORNER_GUARD_BATTLE_FINISHED')
raise 'expected KantoStory Rocket hideout switch lead flag' unless kanto_story_state['story_flags'].include?('FLAG_NEXUS_ROCKET_HIDEOUT_SWITCH_LEAD_SEEN')
raise 'expected KantoStory Game Corner hideout entry unlock flag' unless kanto_story_state['story_flags'].include?('FLAG_NEXUS_GAME_CORNER_HIDEOUT_ENTRY_UNLOCKED')
raise 'expected KantoStory Rocket guard defeat activity' unless kanto_story_state['faction_progress']['team_rocket']['region_activity']['kanto'].any? { |activity| activity['location'] == 'Celadon Game Corner Exterior' && activity['operation'] == 'game_corner_guard_defeated' }
raise 'expected KantoStory Red poster switch scene' unless kanto_story_state['companion_progress']['red']['scene_flags'].include?('game_corner_poster_switch')
raise 'expected KantoStory Rocket guard WorldLink alert immediate' unless kanto_story_state['worldlink_recent_messages'].any? { |message| message['source'] == 'kanto_story' && message['category'] == 'story_alert' && message['text'].include?('poster switch') && message['text'].include?('hideout') }
raise 'expected KantoStory Rocket guard result tracked' unless guard_battle['result'] == 'placeholder_win'
raise 'expected KantoStory Rocket guard next hook hideout entry' unless guard_battle['next_hook'] == 'celadon_rocket_hideout_entry'
second_guard_battle = NexusRed::KantoStory.complete_rocket_game_corner_guard_battle(kanto_story_state)
raise 'expected KantoStory Rocket Game Corner guard idempotent guard' unless second_guard_battle['status'] == 'already_cleared'
raise 'expected KantoStory no duplicate Rocket Game Corner guard history' unless kanto_story_state['kanto_story']['event_history'].count { |event| event['event_id'] == 'rocket_game_corner_guard_battle' } == 1
pre_guard_hideout_entry = NexusRed::KantoStory.complete_celadon_rocket_hideout_entry(NexusRed::RuntimeState.build)
raise 'expected KantoStory Rocket Hideout entry gated before guard battle' unless pre_guard_hideout_entry['status'] == 'blocked_missing_game_corner_guard_battle'
hideout_entry = NexusRed::KantoStory.complete_celadon_rocket_hideout_entry(
  kanto_story_state,
  location: 'Celadon Rocket Hideout Entry',
  area_type: 'villain_hideout'
)
raise 'expected KantoStory Rocket Hideout entry clear status' unless hideout_entry['status'] == 'cleared'
raise 'expected KantoStory Rocket Hideout entry event recorded' unless kanto_story_state['kanto_story']['cleared_events'].include?('celadon_rocket_hideout_entry')
raise 'expected KantoStory Rocket Hideout entry helper true' unless NexusRed::KantoStory.celadon_rocket_hideout_entry_cleared?(kanto_story_state)
raise 'expected KantoStory Rocket Hideout entry reached flag' unless kanto_story_state['story_flags'].include?('FLAG_NEXUS_CELADON_ROCKET_HIDEOUT_ENTRY_REACHED')
raise 'expected KantoStory Red hideout entry watch flag' unless kanto_story_state['story_flags'].include?('FLAG_NEXUS_RED_HIDEOUT_ENTRY_WATCH')
raise 'expected KantoStory Bill hideout elevator signal flag' unless kanto_story_state['story_flags'].include?('FLAG_NEXUS_BILL_HIDEOUT_ELEVATOR_SIGNAL')
raise 'expected KantoStory Rocket Lift Key required flag' unless kanto_story_state['story_flags'].include?('FLAG_NEXUS_ROCKET_LIFT_KEY_REQUIRED')
raise 'expected KantoStory Giovanni hideout command flag' unless kanto_story_state['story_flags'].include?('FLAG_NEXUS_GIOVANNI_HIDEOUT_COMMAND')
raise 'expected KantoStory Moonlight Rocket interference flag' unless kanto_story_state['story_flags'].include?('FLAG_NEXUS_TEAM_MOONLIGHT_ROCKET_INTERFERENCE')
raise 'expected KantoStory Rocket Hideout B1F path unlock flag' unless kanto_story_state['story_flags'].include?('FLAG_NEXUS_ROCKET_HIDEOUT_B1F_PATH_UNLOCKED')
raise 'expected KantoStory Rocket hideout entry activity' unless kanto_story_state['faction_progress']['team_rocket']['region_activity']['kanto'].any? { |activity| activity['location'] == 'Celadon Rocket Hideout Entry' && activity['operation'] == 'hideout_entry_control' }
raise 'expected KantoStory Rocket Lift Key activity' unless kanto_story_state['faction_progress']['team_rocket']['region_activity']['kanto'].any? { |activity| activity['location'] == 'Celadon Rocket Hideout Entry' && activity['operation'] == 'lift_key_barrier' }
raise 'expected KantoStory Moonlight Rocket interference activity' unless kanto_story_state['faction_progress']['team_moonlight']['region_activity']['kanto'].any? { |activity| activity['location'] == 'Celadon Rocket Hideout Entry' && activity['operation'] == 'rocket_signal_interference' }
raise 'expected KantoStory Rocket Moonlight hideout conflict' unless kanto_story_state['faction_progress']['team_rocket']['conflicts'].any? { |conflict| conflict['opponent'] == 'team_moonlight' && conflict['location'] == 'Celadon Rocket Hideout Entry' }
raise 'expected KantoStory Red hideout entry scene' unless kanto_story_state['companion_progress']['red']['scene_flags'].include?('hideout_entry_watch')
raise 'expected KantoStory Bill hideout elevator scene' unless kanto_story_state['companion_progress']['bill']['scene_flags'].include?('hideout_elevator_signal')
raise 'expected KantoStory Rocket Hideout entry story alert paused' unless kanto_story_state['worldlink_paused_messages'].any? { |message| message['source'] == 'kanto_story' && message['category'] == 'story_alert' && message['text'].include?('Lift Key') && message['text'].include?('Giovanni') }
raise 'expected KantoStory Rocket Hideout entry next hook B1F' unless hideout_entry['next_hook'] == 'celadon_rocket_hideout_b1f'
second_hideout_entry = NexusRed::KantoStory.complete_celadon_rocket_hideout_entry(kanto_story_state)
raise 'expected KantoStory Rocket Hideout entry idempotent guard' unless second_hideout_entry['status'] == 'already_cleared'
raise 'expected KantoStory no duplicate Rocket Hideout entry history' unless kanto_story_state['kanto_story']['event_history'].count { |event| event['event_id'] == 'celadon_rocket_hideout_entry' } == 1
pre_entry_b1f = NexusRed::KantoStory.complete_celadon_rocket_hideout_b1f(NexusRed::RuntimeState.build)
raise 'expected KantoStory Rocket Hideout B1F gated before entry' unless pre_entry_b1f['status'] == 'blocked_missing_rocket_hideout_entry'
hideout_b1f = NexusRed::KantoStory.complete_celadon_rocket_hideout_b1f(
  kanto_story_state,
  location: 'Celadon Rocket Hideout B1F',
  area_type: 'villain_hideout'
)
raise 'expected KantoStory Rocket Hideout B1F clear status' unless hideout_b1f['status'] == 'cleared'
raise 'expected KantoStory Rocket Hideout B1F event recorded' unless kanto_story_state['kanto_story']['cleared_events'].include?('celadon_rocket_hideout_b1f')
raise 'expected KantoStory Rocket Hideout B1F helper true' unless NexusRed::KantoStory.celadon_rocket_hideout_b1f_cleared?(kanto_story_state)
raise 'expected KantoStory Rocket Hideout B1F reached flag' unless kanto_story_state['story_flags'].include?('FLAG_NEXUS_CELADON_ROCKET_HIDEOUT_B1F_REACHED')
raise 'expected KantoStory Red hideout B1F maze guard flag' unless kanto_story_state['story_flags'].include?('FLAG_NEXUS_RED_HIDEOUT_B1F_MAZE_GUARD')
raise 'expected KantoStory Bill Silph Scope machine trace flag' unless kanto_story_state['story_flags'].include?('FLAG_NEXUS_BILL_SILPH_SCOPE_MACHINE_TRACE')
raise 'expected KantoStory Rocket spinner maze flag' unless kanto_story_state['story_flags'].include?('FLAG_NEXUS_ROCKET_SPINNER_MAZE')
raise 'expected KantoStory Gold Dust hideout infiltration flag' unless kanto_story_state['story_flags'].include?('FLAG_NEXUS_GOLD_DUST_HIDEOUT_INFILTRATION')
raise 'expected KantoStory Moonlight hideout signal bleed flag' unless kanto_story_state['story_flags'].include?('FLAG_NEXUS_TEAM_MOONLIGHT_HIDEOUT_SIGNAL_BLEED')
raise 'expected KantoStory Lift Key deeper trail flag' unless kanto_story_state['story_flags'].include?('FLAG_NEXUS_LIFT_KEY_DEEPER_TRAIL')
raise 'expected KantoStory Rocket Hideout B2F path unlock flag' unless kanto_story_state['story_flags'].include?('FLAG_NEXUS_ROCKET_HIDEOUT_B2F_PATH_UNLOCKED')
raise 'expected KantoStory Rocket spinner maze activity' unless kanto_story_state['faction_progress']['team_rocket']['region_activity']['kanto'].any? { |activity| activity['location'] == 'Celadon Rocket Hideout B1F' && activity['operation'] == 'spinner_maze_control' }
raise 'expected KantoStory Rocket Silph Scope machine activity' unless kanto_story_state['faction_progress']['team_rocket']['region_activity']['kanto'].any? { |activity| activity['location'] == 'Celadon Rocket Hideout B1F' && activity['operation'] == 'silph_scope_machine_trace' }
raise 'expected KantoStory Gold Dust hideout infiltration activity' unless kanto_story_state['faction_progress']['team_gold_dust']['region_activity']['kanto'].any? { |activity| activity['location'] == 'Celadon Rocket Hideout B1F' && activity['operation'] == 'hideout_coin_cache_infiltration' }
raise 'expected KantoStory Moonlight hideout signal bleed activity' unless kanto_story_state['faction_progress']['team_moonlight']['region_activity']['kanto'].any? { |activity| activity['location'] == 'Celadon Rocket Hideout B1F' && activity['operation'] == 'hideout_signal_bleed' }
raise 'expected KantoStory Rocket Gold Dust B1F conflict' unless kanto_story_state['faction_progress']['team_rocket']['conflicts'].any? { |conflict| conflict['opponent'] == 'team_gold_dust' && conflict['location'] == 'Celadon Rocket Hideout B1F' }
raise 'expected KantoStory Rocket Moonlight B1F conflict' unless kanto_story_state['faction_progress']['team_rocket']['conflicts'].any? { |conflict| conflict['opponent'] == 'team_moonlight' && conflict['location'] == 'Celadon Rocket Hideout B1F' }
raise 'expected KantoStory Red hideout B1F scene' unless kanto_story_state['companion_progress']['red']['scene_flags'].include?('hideout_b1f_maze_guard')
raise 'expected KantoStory Bill Silph Scope machine trace scene' unless kanto_story_state['companion_progress']['bill']['scene_flags'].include?('silph_scope_machine_trace')
raise 'expected KantoStory Rocket Hideout B1F story alert paused' unless kanto_story_state['worldlink_paused_messages'].any? { |message| message['source'] == 'kanto_story' && message['category'] == 'story_alert' && message['text'].include?('Gold Dust') && message['text'].include?('B2F') }
raise 'expected KantoStory Rocket Hideout B1F next hook B2F' unless hideout_b1f['next_hook'] == 'celadon_rocket_hideout_b2f'
second_hideout_b1f = NexusRed::KantoStory.complete_celadon_rocket_hideout_b1f(kanto_story_state)
raise 'expected KantoStory Rocket Hideout B1F idempotent guard' unless second_hideout_b1f['status'] == 'already_cleared'
raise 'expected KantoStory no duplicate Rocket Hideout B1F history' unless kanto_story_state['kanto_story']['event_history'].count { |event| event['event_id'] == 'celadon_rocket_hideout_b1f' } == 1
pre_b1f_b2f = NexusRed::KantoStory.complete_celadon_rocket_hideout_b2f(NexusRed::RuntimeState.build)
raise 'expected KantoStory Rocket Hideout B2F gated before B1F' unless pre_b1f_b2f['status'] == 'blocked_missing_rocket_hideout_b1f'
hideout_b2f = NexusRed::KantoStory.complete_celadon_rocket_hideout_b2f(
  kanto_story_state,
  location: 'Celadon Rocket Hideout B2F',
  area_type: 'villain_hideout'
)
raise 'expected KantoStory Rocket Hideout B2F clear status' unless hideout_b2f['status'] == 'cleared'
raise 'expected KantoStory Rocket Hideout B2F event recorded' unless kanto_story_state['kanto_story']['cleared_events'].include?('celadon_rocket_hideout_b2f')
raise 'expected KantoStory Rocket Hideout B2F helper true' unless NexusRed::KantoStory.celadon_rocket_hideout_b2f_cleared?(kanto_story_state)
raise 'expected KantoStory Rocket Hideout B2F reached flag' unless kanto_story_state['story_flags'].include?('FLAG_NEXUS_CELADON_ROCKET_HIDEOUT_B2F_REACHED')
raise 'expected KantoStory Red hideout B2F patrol warning flag' unless kanto_story_state['story_flags'].include?('FLAG_NEXUS_RED_HIDEOUT_B2F_PATROL_WARNING')
raise 'expected KantoStory Bill stolen Silph Scope crate flag' unless kanto_story_state['story_flags'].include?('FLAG_NEXUS_BILL_STOLEN_SILPH_SCOPE_CRATE')
raise 'expected KantoStory Rocket B2F patrol battle unlock flag' unless kanto_story_state['story_flags'].include?('FLAG_NEXUS_ROCKET_HIDEOUT_B2F_PATROL_BATTLE_UNLOCKED')
raise 'expected KantoStory Rocket Gold Dust B2F conflict flag' unless kanto_story_state['story_flags'].include?('FLAG_NEXUS_ROCKET_GOLD_DUST_B2F_CONFLICT')
raise 'expected KantoStory Moonlight control room interference flag' unless kanto_story_state['story_flags'].include?('FLAG_NEXUS_TEAM_MOONLIGHT_CONTROL_ROOM_INTERFERENCE')
raise 'expected KantoStory Lift Key B3F route flag' unless kanto_story_state['story_flags'].include?('FLAG_NEXUS_LIFT_KEY_B3F_ROUTE')
raise 'expected KantoStory Rocket B2F patrol activity' unless kanto_story_state['faction_progress']['team_rocket']['region_activity']['kanto'].any? { |activity| activity['location'] == 'Celadon Rocket Hideout B2F' && activity['operation'] == 'b2f_patrol_line' }
raise 'expected KantoStory Rocket stolen Silph Scope crate activity' unless kanto_story_state['faction_progress']['team_rocket']['region_activity']['kanto'].any? { |activity| activity['location'] == 'Celadon Rocket Hideout B2F' && activity['operation'] == 'stolen_silph_scope_crate' }
raise 'expected KantoStory Gold Dust B2F conflict activity' unless kanto_story_state['faction_progress']['team_gold_dust']['region_activity']['kanto'].any? { |activity| activity['location'] == 'Celadon Rocket Hideout B2F' && activity['operation'] == 'b2f_ledger_breach' }
raise 'expected KantoStory Moonlight control room activity' unless kanto_story_state['faction_progress']['team_moonlight']['region_activity']['kanto'].any? { |activity| activity['location'] == 'Celadon Rocket Hideout B2F' && activity['operation'] == 'control_room_interference' }
raise 'expected KantoStory Rocket Gold Dust B2F conflict' unless kanto_story_state['faction_progress']['team_rocket']['conflicts'].any? { |conflict| conflict['opponent'] == 'team_gold_dust' && conflict['location'] == 'Celadon Rocket Hideout B2F' }
raise 'expected KantoStory Rocket Moonlight B2F conflict' unless kanto_story_state['faction_progress']['team_rocket']['conflicts'].any? { |conflict| conflict['opponent'] == 'team_moonlight' && conflict['location'] == 'Celadon Rocket Hideout B2F' }
raise 'expected KantoStory Red hideout B2F scene' unless kanto_story_state['companion_progress']['red']['scene_flags'].include?('hideout_b2f_patrol_warning')
raise 'expected KantoStory Bill stolen Silph Scope crate scene' unless kanto_story_state['companion_progress']['bill']['scene_flags'].include?('stolen_silph_scope_crate')
raise 'expected KantoStory Rocket Hideout B2F story alert paused' unless kanto_story_state['worldlink_paused_messages'].any? { |message| message['source'] == 'kanto_story' && message['category'] == 'story_alert' && message['text'].include?('Silph Scope crate') && message['text'].include?('B3F') }
raise 'expected KantoStory Rocket Hideout B2F battle hook id' unless hideout_b2f['battle_hook']['battle_id'] == 'rocket_hideout_b2f_patrol'
raise 'expected KantoStory Rocket Hideout B2F next hook patrol battle' unless hideout_b2f['next_hook'] == 'rocket_hideout_b2f_patrol_battle'
second_hideout_b2f = NexusRed::KantoStory.complete_celadon_rocket_hideout_b2f(kanto_story_state)
raise 'expected KantoStory Rocket Hideout B2F idempotent guard' unless second_hideout_b2f['status'] == 'already_cleared'
raise 'expected KantoStory no duplicate Rocket Hideout B2F history' unless kanto_story_state['kanto_story']['event_history'].count { |event| event['event_id'] == 'celadon_rocket_hideout_b2f' } == 1

pre_b2f_patrol = NexusRed::KantoStory.complete_rocket_hideout_b2f_patrol_battle(NexusRed::RuntimeState.build)
raise 'expected KantoStory Rocket Hideout B2F patrol gated before B2F' unless pre_b2f_patrol['status'] == 'blocked_missing_rocket_hideout_b2f'
b2f_patrol = NexusRed::KantoStory.complete_rocket_hideout_b2f_patrol_battle(
  kanto_story_state,
  location: 'Celadon Rocket Hideout B2F',
  result: 'placeholder_win',
  area_type: 'villain_hideout'
)
raise 'expected KantoStory Rocket Hideout B2F patrol clear status' unless b2f_patrol['status'] == 'cleared'
raise 'expected KantoStory Rocket Hideout B2F patrol event recorded' unless kanto_story_state['kanto_story']['cleared_events'].include?('rocket_hideout_b2f_patrol_battle')
raise 'expected KantoStory Rocket Hideout B2F patrol helper true' unless NexusRed::KantoStory.rocket_hideout_b2f_patrol_battle_cleared?(kanto_story_state)
raise 'expected KantoStory Rocket Hideout B2F patrol started flag' unless kanto_story_state['story_flags'].include?('FLAG_NEXUS_ROCKET_HIDEOUT_B2F_PATROL_BATTLE_STARTED')
raise 'expected KantoStory Rocket Hideout B2F patrol finished flag' unless kanto_story_state['story_flags'].include?('FLAG_NEXUS_ROCKET_HIDEOUT_B2F_PATROL_BATTLE_FINISHED')
raise 'expected KantoStory Rocket Hideout B3F path unlock flag' unless kanto_story_state['story_flags'].include?('FLAG_NEXUS_ROCKET_HIDEOUT_B3F_PATH_UNLOCKED')
raise 'expected KantoStory Rocket B2F patrol defeated activity' unless kanto_story_state['faction_progress']['team_rocket']['region_activity']['kanto'].any? { |activity| activity['location'] == 'Celadon Rocket Hideout B2F' && activity['operation'] == 'b2f_patrol_defeated' }
raise 'expected KantoStory Red B3F route scene' unless kanto_story_state['companion_progress']['red']['scene_flags'].include?('hideout_b3f_route_opened')
raise 'expected KantoStory Rocket Hideout B2F patrol story alert paused' unless kanto_story_state['worldlink_paused_messages'].any? { |message| message['source'] == 'kanto_story' && message['category'] == 'story_alert' && message['text'].include?('B2F patrol') && message['text'].include?('B3F') }
raise 'expected KantoStory Rocket B2F patrol result tracked' unless b2f_patrol['result'] == 'placeholder_win'
raise 'expected KantoStory Rocket B2F patrol next hook B3F' unless b2f_patrol['next_hook'] == 'celadon_rocket_hideout_b3f'
second_b2f_patrol = NexusRed::KantoStory.complete_rocket_hideout_b2f_patrol_battle(kanto_story_state)
raise 'expected KantoStory Rocket Hideout B2F patrol idempotent guard' unless second_b2f_patrol['status'] == 'already_cleared'
raise 'expected KantoStory no duplicate Rocket Hideout B2F patrol history' unless kanto_story_state['kanto_story']['event_history'].count { |event| event['event_id'] == 'rocket_hideout_b2f_patrol_battle' } == 1
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
