# frozen_string_literal: true

module NexusRed
  module EarlyMigrationEncounters
    module_function

    def ensure_migration(state)
      state['early_migration_encounters'] ||= build_migration
    end

    def route_target(route_id)
      SeedData.early_encounters['route_targets'][route_id.to_s]
    end

    def available_for_route(state, route_id, time: 'any', max_level: nil)
      ensure_migration(state)
      route = route_target(route_id)
      return [] if route.nil? || !story_unlocked?(state, route)

      route['encounters'].select do |encounter|
        time_matches?(encounter, time) && level_allowed?(encounter, max_level)
      end
    end

    def catchable_species(state, route_id)
      ensure_migration(state)
      route = route_target(route_id)
      return [] if route.nil?

      route['encounters'].map { |encounter| encounter['species'] }
    end

    def rare_power_species(state)
      ensure_migration(state)['route_targets'].values
        .flat_map { |route| route['encounters'] }
        .select { |encounter| encounter['tags'].include?('high_power') }
        .map { |encounter| encounter['species'] }
        .uniq
    end

    def build_migration
      seed = SeedData.early_encounters
      {
        'level_cap_context' => seed['level_cap_context'],
        'allowed_level_range' => seed['allowed_level_range'].dup,
        'preserve_rules' => seed['preserve_rules'].dup,
        'route_targets' => seed['route_targets']
      }
    end

    def story_unlocked?(state, route)
      unlock_flag = route['story_unlock']
      unlock_flag.nil? || (state['story_flags'] || []).include?(unlock_flag)
    end

    def time_matches?(encounter, requested_time)
      selected = requested_time.to_s
      return true if selected == 'any'

      encounter['time'] == 'any' || encounter['time'] == selected
    end

    def level_allowed?(encounter, max_level)
      max_level.nil? || encounter['level'].to_i <= max_level.to_i
    end
  end
end
