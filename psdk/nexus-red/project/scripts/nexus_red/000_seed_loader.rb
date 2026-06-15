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
end

if defined?(PFM::GameState)
  class PFM::GameState
    attr_accessor :nexus_red

    on_player_initialize(:nexus_red) { @nexus_red = NexusRed::RuntimeState.build }
    on_expand_global_variables(:nexus_red) { @nexus_red ||= NexusRed::RuntimeState.build }
  end
end
