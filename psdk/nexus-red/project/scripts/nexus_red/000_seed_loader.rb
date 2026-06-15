# frozen_string_literal: true

require 'json'

module NexusRed
  module SeedData
    REGISTRY_FILES = {
      starter_selector: 'oak_lab_first_partner_selector.json',
      early_encounters: 'routes_1_to_3_migration_encounters.json',
      regions: 'world_region_progression_spine.json',
      factions: 'custom_faction_war_registry.json',
      companions: 'core_companion_registry.json',
      rivals_worldlink: 'rival_worldlink_registry.json',
      gameplay_systems: 'gameplay_systems_registry.json'
    }.freeze

    module_function

    def root_path
      @root_path ||= locate_project_root
    end

    def generated_path
      File.join(root_path, 'Data', 'nexus_red_seed', 'generated')
    end

    def registry(name)
      key = name.to_sym
      filename = REGISTRY_FILES.fetch(key) { raise ArgumentError, "Unknown Nexus Red registry: #{name}" }
      read_json(File.join(generated_path, filename))
    end

    def starter_selector
      registry(:starter_selector)
    end

    def early_encounters
      registry(:early_encounters)
    end

    def regions
      registry(:regions)
    end

    def factions
      registry(:factions)
    end

    def companions
      registry(:companions)
    end

    def rivals_worldlink
      registry(:rivals_worldlink)
    end

    def gameplay_systems
      registry(:gameplay_systems)
    end

    def all
      REGISTRY_FILES.keys.each_with_object({}) { |key, acc| acc[key] = registry(key) }
    end

    def starter_species
      starter_selector['selectable_partners'].map { |partner| partner['species'] }
    end

    def blue_counter_for(species)
      starter_selector['blue_counter_rules'][species.to_s]
    end

    def encounters_for_route(route_id)
      route = early_encounters['route_targets'][route_id.to_s]
      route ? route['encounters'] : []
    end

    def region_order
      regions['region_unlocks'].map { |region| region['region_id'] }
    end

    def final_region
      regions['final_region']
    end

    def primary_faction
      factions['primary_antagonist']
    end

    def hidden_meta_villain
      factions['hidden_meta_villain']
    end

    def red_primary_companion?
      companions['primary_companion'] == 'red'
    end

    def companion_ids
      companions['companions'].map { |companion| companion['companion_id'] }
    end

    def rival_ids
      rivals_worldlink['rivals'].map { |rival| rival['rival_id'] }
    end

    def starting_rival_ids
      rivals_worldlink['starting_rivals']
    end

    def worldlink_paused_area?(area_type)
      pause_list = rivals_worldlink.dig('worldlink_settings', 'delivery_rules', 'pause_and_digest') || []
      pause_list.include?(area_type.to_s)
    end

    def all_base_species_before_final_boss?
      gameplay_systems.dig('pokedex_and_availability', 'all_base_species_before_final_boss') == true
    end

    def starting_money
      gameplay_systems.dig('pokemon_center_and_mart', 'mart_rules', 'starting_money')
    end

    def gameplay_option_available?(option_id)
      gameplay_systems.dig('qol_systems', 'must_have').include?(option_id.to_s)
    end

    def read_json(path)
      JSON.parse(File.read(path))
    rescue Errno::ENOENT
      raise "Missing Nexus Red seed registry: #{path}"
    rescue JSON::ParserError => e
      raise "Invalid Nexus Red seed JSON #{path}: #{e.message}"
    end

    def locate_project_root
      candidates = [
        Dir.pwd,
        File.expand_path('../..', __dir__),
        File.expand_path('../../..', __dir__)
      ]
      candidates.find { |path| File.exist?(File.join(path, 'Data', 'nexus_red_seed', 'import_manifest.json')) } || Dir.pwd
    end
  end

  module RuntimeState
    module_function

    def build
      {
        'current_region' => 'kanto',
        'active_companion' => 'red',
        'worldlink_unlocked' => false,
        'worldlink_unread_count' => 0,
        'worldlink_recent_messages' => [],
        'worldlink_paused_messages' => [],
        'rival_progress' => {},
        'companion_progress' => {},
        'faction_progress' => {},
        'gameplay_options' => {
          'difficulty_mode' => 'standard',
          'level_caps_enabled' => true,
          'infinite_repel_enabled' => false,
          'nuzlocke_enabled' => false
        }
      }
    end
  end

  module WorldLink
    module_function

    def queue_message(state, category, text, source: 'system', area_type: 'route')
      message = build_message(state, category, text, source, area_type)
      if SeedData.worldlink_paused_area?(area_type)
        state['worldlink_paused_messages'] << message
        message['delivery'] = 'paused'
      else
        push_recent_message(state, message)
        message['delivery'] = 'immediate'
      end
      message
    end

    def release_digest(state)
      messages = state['worldlink_paused_messages']
      digest = {
        'title' => 'While You Were Away',
        'items' => messages.dup
      }
      messages.each { |message| push_recent_message(state, message.merge('delivery' => 'digest')) }
      state['worldlink_paused_messages'] = []
      digest
    end

    def mark_all_read(state)
      state['worldlink_unread_count'] = 0
      state['worldlink_recent_messages'].each { |message| message['read'] = true }
      state['worldlink_paused_messages'].each { |message| message['read'] = true }
    end

    def build_message(state, category, text, source, area_type)
      {
        'id' => format('wl_%04d', next_message_index(state)),
        'category' => category.to_s,
        'source' => source.to_s,
        'area_type' => area_type.to_s,
        'text' => text.to_s,
        'read' => false
      }
    end

    def next_message_index(state)
      state['worldlink_message_index'] ||= 0
      state['worldlink_message_index'] += 1
    end

    def push_recent_message(state, message)
      capacity = SeedData.rivals_worldlink.dig('worldlink_settings', 'recent_message_capacity') || 32
      state['worldlink_recent_messages'] << message
      state['worldlink_recent_messages'].shift while state['worldlink_recent_messages'].length > capacity
      state['worldlink_unread_count'] += 1 unless message['read']
    end
  end
end

if defined?(PFM::GameState)
  class PFM::GameState
    attr_accessor :nexus_red

    on_player_initialize(:nexus_red) { @nexus_red = NexusRed::RuntimeState.build }
    on_expand_global_variables(:nexus_red) { @nexus_red ||= NexusRed::RuntimeState.build }
  end
end
