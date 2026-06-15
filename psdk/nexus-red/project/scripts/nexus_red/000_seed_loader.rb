# frozen_string_literal: true

require_relative 'runtime/seed_data'
require_relative 'runtime/runtime_state'
require_relative 'runtime/world_link'
require_relative 'runtime/rival_progress'
require_relative 'runtime/companion_progress'
require_relative 'runtime/faction_war'
require_relative 'runtime/region_progress'
require_relative 'runtime/gameplay_options'
require_relative 'runtime/field_tools'
require_relative 'runtime/pokedex_availability'
require_relative 'runtime/center_mart_services'
require_relative 'runtime/encounter_world'
require_relative 'runtime/battle_mechanics'
require_relative 'runtime/starter_selection'
require_relative 'runtime/early_migration_encounters'
require_relative 'runtime/map_event_bridge'
require_relative 'runtime/route1_migration_event'

if defined?(PFM::GameState)
  class PFM::GameState
    attr_accessor :nexus_red

    on_player_initialize(:nexus_red) { @nexus_red = NexusRed::RuntimeState.build }
    on_expand_global_variables(:nexus_red) { @nexus_red ||= NexusRed::RuntimeState.build }
  end
end
