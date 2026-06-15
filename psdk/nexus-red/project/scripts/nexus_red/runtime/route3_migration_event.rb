# frozen_string_literal: true

module NexusRed
  module Route3MigrationEvent
    EVENT_ID = 'route_3_migration_event'
    ROUTE_ID = 'route_3'

    module_function

    def trigger(state, time: 'any', max_level: nil)
      payload = EarlyMigrationEncounters.prepare_map_event_encounter(
        state,
        ROUTE_ID,
        time: time,
        max_level: max_level,
        channel: 'wild_grass',
        area_type: 'route'
      )
      return MapEventBridge.no_encounter(event_id: EVENT_ID, route_id: ROUTE_ID, reason: 'no_available_migration_encounter') if payload.nil?

      MapEventBridge.prepare_wild_battle_request(
        state,
        event_id: EVENT_ID,
        encounter_payload: payload
      )
    end
  end
end
