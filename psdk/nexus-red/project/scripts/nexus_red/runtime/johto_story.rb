# frozen_string_literal: true

module NexusRed
  module JohtoStory
    NEW_BARK_ARRIVAL_EVENT_ID = 'johto_new_bark_arrival'
    ELM_WORLD_CIRCUIT_REGISTRATION_EVENT_ID = 'elm_world_circuit_registration'
    RED_JOHTO_COMPANION_ACTIVE_EVENT_ID = 'red_johto_companion_active'
    SILVER_WORLDLINK_TEASE_EVENT_ID = 'silver_worldlink_tease'
    ROCKET_JOHTO_RADIO_PROBE_EVENT_ID = 'rocket_johto_radio_probe'
    GOLD_DUST_RUINS_BUYER_EVENT_ID = 'gold_dust_ruins_buyer'
    MOONLIGHT_TOWER_ECHO_EVENT_ID = 'moonlight_tower_echo'
    NEXUS_ORDER_JOHTO_TOWER_STATIC_EVENT_ID = 'nexus_order_johto_tower_static_hidden'
    VIOLET_CITY_PATH_UNLOCKED_EVENT_ID = 'violet_city_path_unlocked'
    VIOLET_CITY_PATH_EVENT_ID = 'violet_city_path'
    CHERRYGROVE_WORLDLINK_CHECKPOINT_EVENT_ID = 'cherrygrove_worldlink_checkpoint'
    RED_JOHTO_ROUTE_TRAINING_EVENT_ID = 'red_johto_route_training'
    SILVER_ROUTE29_PRESSURE_EVENT_ID = 'silver_route29_pressure'
    ROCKET_JOHTO_RADIO_RELAY_EVENT_ID = 'rocket_johto_radio_relay'
    GOLD_DUST_DARK_CAVE_BUYER_EVENT_ID = 'gold_dust_dark_cave_buyer'
    MOONLIGHT_SPROUT_TOWER_ECHO_EVENT_ID = 'moonlight_sprout_tower_echo'
    NEXUS_ORDER_SPROUT_TOWER_STATIC_EVENT_ID = 'nexus_order_sprout_tower_static_hidden'
    SPROUT_TOWER_PATH_EVENT_ID = 'sprout_tower_path_unlocked'
    FALKNER_GYM_TEASE_EVENT_ID = 'falkner_gym_teased'

    module_function

    def ensure_johto_story(state)
      state['johto_story'] ||= {
        'current_act' => 'act_1_new_bark_to_violet',
        'cleared_events' => [],
        'event_history' => [],
        'latest_event' => nil
      }
    end

    def complete_new_bark_arrival(state, location: 'New Bark Town', area_type: 'town')
      story = ensure_johto_story(state)
      return { 'status' => 'blocked_missing_johto_region_unlock', 'event_id' => NEW_BARK_ARRIVAL_EVENT_ID } unless johto_unlocked?(state)
      return { 'status' => 'already_cleared', 'event_id' => NEW_BARK_ARRIVAL_EVENT_ID } if new_bark_arrival_cleared?(state)

      state['active_companion'] = 'red'

      add_story_flag(state, 'FLAG_NEXUS_JOHTO_NEW_BARK_ARRIVAL')
      add_story_flag(state, 'FLAG_NEXUS_ELM_WORLD_CIRCUIT_REGISTRATION')
      add_story_flag(state, 'FLAG_NEXUS_RED_JOHTO_COMPANION_ACTIVE')
      add_story_flag(state, 'FLAG_NEXUS_SILVER_WORLDLINK_TEASE')
      add_story_flag(state, 'FLAG_NEXUS_ROCKET_JOHTO_RADIO_PROBE')
      add_story_flag(state, 'FLAG_NEXUS_GOLD_DUST_RUINS_BUYER')
      add_story_flag(state, 'FLAG_NEXUS_MOONLIGHT_TOWER_ECHO')
      add_story_flag(state, 'FLAG_NEXUS_NEXUS_ORDER_JOHTO_TOWER_STATIC')
      add_story_flag(state, 'FLAG_NEXUS_VIOLET_CITY_PATH_UNLOCKED')

      [
        NEW_BARK_ARRIVAL_EVENT_ID,
        ELM_WORLD_CIRCUIT_REGISTRATION_EVENT_ID,
        RED_JOHTO_COMPANION_ACTIVE_EVENT_ID,
        SILVER_WORLDLINK_TEASE_EVENT_ID,
        ROCKET_JOHTO_RADIO_PROBE_EVENT_ID,
        GOLD_DUST_RUINS_BUYER_EVENT_ID,
        MOONLIGHT_TOWER_ECHO_EVENT_ID,
        NEXUS_ORDER_JOHTO_TOWER_STATIC_EVENT_ID,
        VIOLET_CITY_PATH_UNLOCKED_EVENT_ID
      ].each { |event_id| mark_cleared_event(story, event_id) }

      CompanionProgress.activate_companion(
        state,
        'red',
        location: location,
        reason: 'Antman and Red are entering the World Circuit together',
        following: true,
        area_type: area_type
      )
      CompanionProgress.record_scene(
        state,
        'red',
        'johto_first_steps',
        location: location,
        summary: 'Red steps into New Bark with Antman and says Johto feels older, quieter, and more dangerous than Kanto.',
        area_type: area_type
      )
      CompanionProgress.record_scene(
        state,
        'bill',
        'johto_worldlink_route_check',
        location: location,
        summary: "Bill syncs the passport route data and confirms the Johto tower echo matches Lance's warning.",
        area_type: area_type
      )

      record_rival_story_clue(
        state,
        'silver',
        location,
        'Silver was seen near New Bark after Professor Elm logged a World Circuit registration anomaly.',
        area_type
      )

      FactionWar.record_activity(
        state,
        'team_rocket',
        'johto',
        location,
        'radio_probe_remnants',
        threat_delta: 1,
        area_type: area_type
      )
      FactionWar.record_activity(
        state,
        'team_gold_dust',
        'johto',
        location,
        'ruins_relic_buyer_arrival',
        threat_delta: 1,
        area_type: area_type
      )
      FactionWar.record_activity(
        state,
        'team_moonlight',
        'johto',
        location,
        'tower_echo_dream_static',
        threat_delta: 1,
        area_type: area_type
      )
      FactionWar.record_activity(
        state,
        'nexus_order',
        'johto',
        location,
        'johto_tower_static_hidden',
        threat_delta: 0,
        area_type: area_type
      )
      FactionWar.record_conflict(
        state,
        'team_rocket',
        'team_gold_dust',
        location,
        'Rocket remnants and Gold Dust buyers argue over who gets the first Johto relic lead.',
        intensity: 2,
        area_type: area_type
      )

      event = new_bark_arrival_event_result(location)
      story['event_history'] << event
      story['latest_event'] = event

      WorldLink.queue_message(
        state,
        'story_alert',
        'New Bark opens Johto for Antman and Red: Professor Elm confirms the passport, Silver vanishes toward the routes, and Rocket argues with Gold Dust over the first relic lead.',
        source: 'johto_story',
        area_type: area_type
      )

      event
    end

    def new_bark_arrival_cleared?(state)
      ensure_johto_story(state)['event_history'].any? { |event| event['event_id'] == NEW_BARK_ARRIVAL_EVENT_ID }
    end

    def johto_unlocked?(state)
      state['current_region'] == 'johto' || RegionProgress.can_enter_region?(state, 'johto')
    end

    def add_story_flag(state, flag)
      state['story_flags'] ||= []
      state['story_flags'] << flag unless state['story_flags'].include?(flag)
    end

    def mark_cleared_event(story, event_id)
      story['cleared_events'] << event_id unless story['cleared_events'].include?(event_id)
    end

    def record_rival_story_clue(state, rival_id, location, summary, area_type, region: nil)
      rival = RivalProgress.ensure_rival(state, rival_id)
      rival['current_region'] = region.to_s unless region.nil?
      activity = {
        'category' => 'rival_story_clue',
        'location' => location.to_s,
        'summary' => summary.to_s
      }
      RivalProgress.record_activity(rival, activity)
      WorldLink.queue_message(state, activity['category'], activity['summary'], source: rival['rival_id'], area_type: area_type)
    end

    def new_bark_arrival_event_result(location)
      {
        'status' => 'cleared',
        'event_id' => NEW_BARK_ARRIVAL_EVENT_ID,
        'location' => location.to_s,
        'region' => 'johto',
        'current_act' => 'act_1_new_bark_to_violet',
        'professor' => 'Elm',
        'companions' => %w[red bill],
        'rivals' => %w[silver],
        'factions' => %w[team_rocket team_gold_dust team_moonlight nexus_order],
        'linked_events' => [
          ELM_WORLD_CIRCUIT_REGISTRATION_EVENT_ID,
          RED_JOHTO_COMPANION_ACTIVE_EVENT_ID,
          SILVER_WORLDLINK_TEASE_EVENT_ID,
          ROCKET_JOHTO_RADIO_PROBE_EVENT_ID,
          GOLD_DUST_RUINS_BUYER_EVENT_ID,
          MOONLIGHT_TOWER_ECHO_EVENT_ID,
          NEXUS_ORDER_JOHTO_TOWER_STATIC_EVENT_ID,
          VIOLET_CITY_PATH_UNLOCKED_EVENT_ID
        ],
        'arrival_state' => 'johto_world_circuit_registered',
        'tower_signal' => 'johto_tower_echo_active',
        'hidden_meta_signal' => 'nexus_order_johto_tower_static_unrevealed',
        'unlocks' => %w[elm_world_circuit_registration violet_city_path silver_worldlink_tease johto_tower_echo],
        'next_hook' => 'violet_city_path'
      }
    end

    def complete_violet_city_path(state, location: 'Route 29 / Cherrygrove Road', area_type: 'route')
      story = ensure_johto_story(state)
      return { 'status' => 'blocked_missing_johto_region_unlock', 'event_id' => VIOLET_CITY_PATH_EVENT_ID } unless johto_unlocked?(state)
      return { 'status' => 'blocked_missing_new_bark_arrival', 'event_id' => VIOLET_CITY_PATH_EVENT_ID } unless new_bark_arrival_cleared?(state)
      return { 'status' => 'already_cleared', 'event_id' => VIOLET_CITY_PATH_EVENT_ID } if violet_city_path_cleared?(state)

      add_story_flag(state, 'FLAG_NEXUS_JOHTO_VIOLET_CITY_PATH')
      add_story_flag(state, 'FLAG_NEXUS_CHERRYGROVE_WORLDLINK_CHECKPOINT')
      add_story_flag(state, 'FLAG_NEXUS_RED_JOHTO_ROUTE_TRAINING')
      add_story_flag(state, 'FLAG_NEXUS_SILVER_ROUTE29_PRESSURE')
      add_story_flag(state, 'FLAG_NEXUS_ROCKET_JOHTO_RADIO_RELAY')
      add_story_flag(state, 'FLAG_NEXUS_GOLD_DUST_DARK_CAVE_BUYER')
      add_story_flag(state, 'FLAG_NEXUS_MOONLIGHT_SPROUT_TOWER_ECHO')
      add_story_flag(state, 'FLAG_NEXUS_SPROUT_TOWER_PATH_UNLOCKED')
      add_story_flag(state, 'FLAG_NEXUS_FALKNER_GYM_TEASED')

      [
        VIOLET_CITY_PATH_EVENT_ID,
        CHERRYGROVE_WORLDLINK_CHECKPOINT_EVENT_ID,
        RED_JOHTO_ROUTE_TRAINING_EVENT_ID,
        SILVER_ROUTE29_PRESSURE_EVENT_ID,
        ROCKET_JOHTO_RADIO_RELAY_EVENT_ID,
        GOLD_DUST_DARK_CAVE_BUYER_EVENT_ID,
        MOONLIGHT_SPROUT_TOWER_ECHO_EVENT_ID,
        NEXUS_ORDER_SPROUT_TOWER_STATIC_EVENT_ID,
        SPROUT_TOWER_PATH_EVENT_ID,
        FALKNER_GYM_TEASE_EVENT_ID
      ].each { |event_id| mark_cleared_event(story, event_id) }

      CompanionProgress.record_scene(
        state,
        'red',
        'johto_route_29_training',
        location: 'Route 29',
        summary: 'Red slows the pace on Route 29, helping Antman read Johto terrain instead of rushing toward the next badge.',
        area_type: area_type
      )
      CompanionProgress.record_scene(
        state,
        'bill',
        'cherrygrove_worldlink_checkpoint',
        location: 'Cherrygrove City',
        summary: 'Bill confirms the Cherrygrove WorldLink checkpoint is catching old Rocket radio noise under the new passport signal.',
        area_type: area_type
      )

      record_rival_story_clue(
        state,
        'silver',
        'Route 29',
        'Silver pressured a trainer on Route 29, then cut toward Cherrygrove before anyone could ask why he is shadowing Antman.',
        area_type,
        region: 'johto'
      )

      FactionWar.record_activity(
        state,
        'team_rocket',
        'johto',
        'Cherrygrove Relay Shed',
        'radio_relay_rebuild',
        threat_delta: 1,
        area_type: area_type
      )
      FactionWar.record_activity(
        state,
        'team_gold_dust',
        'johto',
        'Dark Cave Approach',
        'dark_cave_relic_buyer',
        threat_delta: 1,
        area_type: area_type
      )
      FactionWar.record_activity(
        state,
        'team_moonlight',
        'johto',
        'Sprout Tower Grounds',
        'sprout_tower_dream_echo',
        threat_delta: 1,
        area_type: area_type
      )
      FactionWar.record_activity(
        state,
        'nexus_order',
        'johto',
        'Sprout Tower Roots',
        'sprout_tower_root_static_hidden',
        threat_delta: 0,
        area_type: area_type
      )
      FactionWar.record_conflict(
        state,
        'team_rocket',
        'team_moonlight',
        'Cherrygrove Relay Shed',
        'Rocket radio engineers blame Moonlight dream static for corrupting the Johto relay rebuild.',
        intensity: 1,
        area_type: area_type
      )

      story['current_act'] = 'act_2_violet_city_and_sprout_tower'
      event = violet_city_path_event_result(location)
      story['event_history'] << event
      story['latest_event'] = event

      WorldLink.queue_message(
        state,
        'story_alert',
        'Violet City is open: Red trains Antman on Route 29, Silver shadows the road, Rocket rebuilds a radio relay, and Moonlight static leaks from Sprout Tower.',
        source: 'johto_story',
        area_type: area_type
      )

      event
    end

    def violet_city_path_cleared?(state)
      ensure_johto_story(state)['event_history'].any? { |event| event['event_id'] == VIOLET_CITY_PATH_EVENT_ID }
    end

    def violet_city_path_event_result(location)
      {
        'status' => 'cleared',
        'event_id' => VIOLET_CITY_PATH_EVENT_ID,
        'location' => location.to_s,
        'region' => 'johto',
        'current_act' => 'act_2_violet_city_and_sprout_tower',
        'route_chain' => ['New Bark Town', 'Route 29', 'Cherrygrove City', 'Route 30', 'Violet City'],
        'companions' => %w[red bill],
        'rivals' => %w[silver],
        'factions' => %w[team_rocket team_gold_dust team_moonlight nexus_order],
        'linked_events' => [
          CHERRYGROVE_WORLDLINK_CHECKPOINT_EVENT_ID,
          RED_JOHTO_ROUTE_TRAINING_EVENT_ID,
          SILVER_ROUTE29_PRESSURE_EVENT_ID,
          ROCKET_JOHTO_RADIO_RELAY_EVENT_ID,
          GOLD_DUST_DARK_CAVE_BUYER_EVENT_ID,
          MOONLIGHT_SPROUT_TOWER_ECHO_EVENT_ID,
          NEXUS_ORDER_SPROUT_TOWER_STATIC_EVENT_ID,
          SPROUT_TOWER_PATH_EVENT_ID,
          FALKNER_GYM_TEASE_EVENT_ID
        ],
        'gym_leader_tease' => 'Falkner',
        'tower_signal' => 'sprout_tower_echo_active',
        'hidden_meta_signal' => 'nexus_order_sprout_tower_root_static_unrevealed',
        'unlocks' => %w[violet_city_services sprout_tower_entry falkner_gym_tease dark_cave_rumor],
        'next_hook' => 'sprout_tower_entry'
      }
    end
  end
end
