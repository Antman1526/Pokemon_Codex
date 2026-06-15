# frozen_string_literal: true

module NexusRed
  module Route2MigrationEvent
    EVENT_ID = 'route_2_migration_event'
    ROUTE_ID = 'route_2'

    module_function

    def trigger(state, time: 'any', max_level: nil)
      RouteMigrationEventAdapter.trigger_route(
        state,
        event_id: EVENT_ID,
        route_id: ROUTE_ID,
        time: time,
        max_level: max_level
      )
    end
  end
end
