# frozen_string_literal: true

module NexusRed
  module PokedexAvailability
    module_function

    def ensure_pokedex(state)
      state['pokedex'] ||= build_pokedex
    end

    def set_required_species(state, species_list)
      dex = ensure_pokedex(state)
      dex['required_species'] = species_list.map(&:to_s).uniq
      dex
    end

    def record_seen(state, species, location:, channel:, area_type: 'route')
      dex = ensure_pokedex(state)
      validate_channel!(channel)
      entry = species_location_entry(location, channel)
      dex['seen_species'][species.to_s] ||= []
      dex['seen_species'][species.to_s] << entry

      WorldLink.queue_message(
        state,
        'pokedex_update',
        "#{species} was seen at #{location} through #{channel}.",
        source: 'pokedex',
        area_type: area_type
      )
    end

    def record_caught(state, species, location:, channel:, area_type: 'route')
      dex = ensure_pokedex(state)
      validate_channel!(channel)
      entry = species_location_entry(location, channel)
      dex['seen_species'][species.to_s] ||= []
      dex['seen_species'][species.to_s] << entry
      dex['caught_species'][species.to_s] ||= []
      dex['caught_species'][species.to_s] << entry

      WorldLink.queue_message(
        state,
        'pokedex_update',
        "#{species} was caught at #{location}. Pokédex readiness updated.",
        source: 'pokedex',
        area_type: area_type
      )
    end

    def register_availability_hint(state, species, region:, channel:, hint:, area_type: 'route')
      dex = ensure_pokedex(state)
      validate_channel!(channel)
      hint_entry = {
        'species' => species.to_s,
        'region' => region.to_s,
        'channel' => channel.to_s,
        'hint' => hint.to_s
      }
      dex['active_hints'][species.to_s] ||= []
      dex['active_hints'][species.to_s] << hint_entry

      WorldLink.queue_message(
        state,
        'pokedex_hint',
        "#{species} availability hint: #{hint}",
        source: 'pokedex',
        area_type: area_type
      )
    end

    def readiness_report(state)
      dex = ensure_pokedex(state)
      missing = dex['required_species'].reject { |species| dex['caught_species'].key?(species) }
      {
        'species_scope' => dex['species_scope'],
        'caught_count' => dex['caught_species'].length,
        'seen_count' => dex['seen_species'].length,
        'required_count' => dex['required_species'].length,
        'missing_species' => missing,
        'readiness_status' => missing.empty? ? 'ready' : 'incomplete',
        'all_base_species_before_final_boss' => dex['all_base_species_before_final_boss']
      }
    end

    def pre_final_ready?(state)
      readiness_report(state)['readiness_status'] == 'ready'
    end

    def build_pokedex
      policy = SeedData.gameplay_systems['pokedex_and_availability']
      {
        'species_scope' => policy['species_scope'],
        'readiness_surface' => policy['readiness_surface'],
        'readiness_interaction' => policy['readiness_interaction'],
        'all_base_species_before_final_boss' => policy['all_base_species_before_final_boss'] == true,
        'postgame_required_for_base_species' => policy['postgame_required_for_base_species'] == true,
        'availability_channels' => policy['availability_channels'].dup,
        'pokedex_fields' => policy['pokedex_fields'].dup,
        'required_species' => [],
        'seen_species' => {},
        'caught_species' => {},
        'active_hints' => {}
      }
    end

    def species_location_entry(location, channel)
      {
        'location' => location.to_s,
        'channel' => channel.to_s
      }
    end

    def validate_channel!(channel)
      return if SeedData.gameplay_systems['availability_channels'].key?(channel.to_s)

      raise ArgumentError, "Unknown Nexus Red availability channel: #{channel}"
    end
  end
end
