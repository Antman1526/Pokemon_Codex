# frozen_string_literal: true

module NexusRed
  module WildBattleResults
    module_function

    def record_result(state, outcome:, area_type: 'route')
      launch = last_launch(state)
      return { 'status' => 'no_launch', 'outcome' => outcome.to_s } if launch.nil?

      result = {
        'status' => 'recorded',
        'outcome' => outcome.to_s,
        'source_event_id' => launch['source_event_id'],
        'route_id' => launch['route_id'],
        'route_name' => launch['route_name'],
        'species' => launch['species'],
        'species_key' => launch['species_key'],
        'level' => launch['level'],
        'channel' => launch['channel'],
        'encounter_id' => launch['encounter_id']
      }
      result_history(state) << result
      state['last_wild_battle_result'] = result

      if result['outcome'] == 'caught'
        result['storage'] = PartyStorage.add_species(state, result['species'])['storage']
        PokedexAvailability.record_caught(
          state,
          result['species'],
          location: result['route_name'],
          channel: result['channel'],
          area_type: area_type
        )
      end

      result
    end

    def result_history(state)
      state['wild_battle_result_history'] ||= []
    end

    def last_launch(state)
      state['last_wild_battle_launch']
    end
  end
end
