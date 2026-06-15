# frozen_string_literal: true

module NexusRed
  module RouteMigrationEventAdapter
    module_function

    def trigger_route(state, event_id:, route_id:, time: 'any', max_level: nil, channel: 'wild_grass', area_type: 'route')
      payload = EarlyMigrationEncounters.prepare_map_event_encounter(
        state,
        route_id,
        time: time,
        max_level: max_level,
        channel: channel,
        area_type: area_type
      )
      return MapEventBridge.no_encounter(event_id: event_id, route_id: route_id, reason: 'no_available_migration_encounter') if payload.nil?

      MapEventBridge.prepare_wild_battle_request(
        state,
        event_id: event_id,
        encounter_payload: payload
      )
    end
  end
end
