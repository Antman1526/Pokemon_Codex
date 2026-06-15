# frozen_string_literal: true

module NexusRed
  module EncounterWorld
    module_function

    def ensure_world(state)
      state['encounter_world'] ||= build_world
    end

    def set_day_phase(state, phase, source: 'system', area_type: 'route')
      world = ensure_world(state)
      selected = phase.to_s
      raise ArgumentError, "Unknown Nexus Red day phase: #{phase}" unless world['available_day_phases'].include?(selected)

      world['day_phase'] = selected
      world['latest_update'] = {
        'kind' => 'day_phase',
        'value' => selected,
        'source' => source.to_s
      }
      WorldLink.queue_message(
        state,
        'world_state',
        "Day phase changed to #{selected} via #{source}.",
        source: 'encounter_world',
        area_type: area_type
      )
    end

    def set_weather(state, weather, source: 'system', area_type: 'route')
      world = ensure_world(state)
      selected = weather.to_s
      raise ArgumentError, "Unknown Nexus Red weather: #{weather}" unless world['available_weather'].include?(selected)

      world['weather'] = selected
      world['latest_update'] = {
        'kind' => 'weather',
        'value' => selected,
        'source' => source.to_s
      }
      WorldLink.queue_message(
        state,
        'world_state',
        "Weather changed to #{selected} via #{source}.",
        source: 'encounter_world',
        area_type: area_type
      )
    end

    def unlock_fishing_rod(state, rod_id, source:, area_type: 'route')
      world = ensure_world(state)
      rod = rod_id.to_s
      raise ArgumentError, "Unknown Nexus Red fishing rod: #{rod_id}" unless world['available_fishing_rods'].include?(rod)

      world['unlocked_fishing_rods'] << rod unless world['unlocked_fishing_rods'].include?(rod)
      WorldLink.queue_message(
        state,
        'story_unlock',
        "#{rod} unlocked from #{source}.",
        source: 'encounter_world',
        area_type: area_type
      )
    end

    def unlock_daycare(state, location:)
      world = ensure_world(state)
      world['daycare_enabled'] = true
      world['daycare_location'] = location.to_s
      world
    end

    def daycare_enabled?(state)
      ensure_world(state)['daycare_enabled'] == true
    end

    def enable_overworld_pokemon(state, zone:)
      world = ensure_world(state)
      zone_name = zone.to_s
      world['overworld_pokemon_zones'] << zone_name unless world['overworld_pokemon_zones'].include?(zone_name)
      world
    end

    def enable_following_pokemon(state, species:)
      world = ensure_world(state)
      species_name = species.to_s
      world['following_pokemon_species'] << species_name unless world['following_pokemon_species'].include?(species_name)
      world
    end

    def build_world
      seed = encounter_seed
      {
        'day_phase' => 'day',
        'weather' => 'clear',
        'available_day_phases' => seed['day_phases'].dup,
        'available_weather' => seed['weather_types'].dup,
        'available_fishing_rods' => seed['fishing_rods'].dup,
        'unlocked_fishing_rods' => [],
        'daycare_enabled' => false,
        'daycare_location' => nil,
        'overworld_pokemon_policy' => seed['overworld_pokemon'],
        'following_pokemon_policy' => seed['following_pokemon'],
        'overworld_pokemon_zones' => [],
        'following_pokemon_species' => [],
        'latest_update' => nil
      }
    end

    def encounter_seed
      SeedData.gameplay_systems['encounter_world_systems']
    end
  end
end
