# frozen_string_literal: true

module NexusRed
  module MapEventBridge
    module_function

    def prepare_wild_battle_request(state, event_id:, encounter_payload:)
      request = {
        'status' => 'prepared',
        'kind' => 'wild_migration',
        'event_id' => event_id.to_s,
        'route_id' => encounter_payload['route_id'],
        'route_name' => encounter_payload['route_name'],
        'psdk_map_id' => encounter_payload['psdk_map_id'],
        'species' => encounter_payload['species'],
        'psdk_species_key' => encounter_payload['psdk_species_key'],
        'level' => encounter_payload['level'],
        'channel' => encounter_payload['channel'],
        'encounter_id' => encounter_payload['encounter_id'],
        'tags' => encounter_payload['tags'].dup
      }
      state['pending_psdk_battle_request'] = request
      record_map_event(state, request)
      request
    end

    def pending_battle_request(state)
      state['pending_psdk_battle_request']
    end

    def consume_pending_battle_request(state)
      request = state['pending_psdk_battle_request']
      state['pending_psdk_battle_request'] = nil
      request
    end

    def no_encounter(event_id:, route_id:, reason:)
      {
        'status' => 'no_encounter',
        'kind' => 'wild_migration',
        'event_id' => event_id.to_s,
        'route_id' => route_id.to_s,
        'reason' => reason.to_s
      }
    end

    def record_map_event(state, request)
      state['map_event_history'] ||= []
      state['map_event_history'] << {
        'event_id' => request['event_id'],
        'kind' => request['kind'],
        'route_id' => request['route_id'],
        'species' => request['species'],
        'status' => request['status']
      }
    end
  end
end
