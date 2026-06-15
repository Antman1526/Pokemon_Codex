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
    SPROUT_TOWER_ENTRY_EVENT_ID = 'sprout_tower_entry'
    ELDER_LI_TOWER_TRIAL_EVENT_ID = 'elder_li_tower_trial'
    RED_SPROUT_TOWER_RESPECT_EVENT_ID = 'red_sprout_tower_respect'
    BROCK_SPROUT_TOWER_LORE_EVENT_ID = 'brock_sprout_tower_lore'
    SILVER_SAGE_CONFLICT_EVENT_ID = 'silver_sage_conflict'
    MOONLIGHT_SPROUT_TOWER_RITUAL_EVENT_ID = 'moonlight_sprout_tower_ritual'
    ROCKET_BELLSPROUT_RADIO_ANTENNA_EVENT_ID = 'rocket_bellsprout_radio_antenna'
    GOLD_DUST_TOWER_RELIC_OFFER_EVENT_ID = 'gold_dust_tower_relic_offer'
    NEXUS_ORDER_SPROUT_ROOT_STATIC_EVENT_ID = 'nexus_order_sprout_root_static_hidden'
    FALKNER_ZEPHYR_BADGE_PREP_EVENT_ID = 'falkner_zephyr_badge_prep_unlocked'
    FALKNER_ZEPHYR_BADGE_PREP_MAIN_EVENT_ID = 'falkner_zephyr_badge_prep'
    FALKNER_WIND_DOJO_TRAINING_EVENT_ID = 'falkner_wind_dojo_training'
    RED_FALKNER_PREP_EVENT_ID = 'red_falkner_prep'
    BROCK_FLYING_COUNTER_ADVICE_EVENT_ID = 'brock_flying_counter_advice'
    BILL_GYM_ROOF_SIGNAL_SCAN_EVENT_ID = 'bill_gym_roof_signal_scan'
    SILVER_VIOLET_GYM_PRESSURE_EVENT_ID = 'silver_violet_gym_pressure'
    MOONLIGHT_ZEPHYR_DRAFT_EVENT_ID = 'moonlight_zephyr_draft'
    ROCKET_GYM_ROOF_RELAY_EVENT_ID = 'rocket_gym_roof_relay'
    GOLD_DUST_FEATHER_CHARM_MARKET_EVENT_ID = 'gold_dust_feather_charm_market'
    NEXUS_ORDER_ZEPHYR_AIR_CURRENT_EVENT_ID = 'nexus_order_zephyr_air_current_static_hidden'
    ZEPHYR_BADGE_BATTLE_UNLOCKED_EVENT_ID = 'zephyr_badge_battle_unlocked'

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

    def complete_sprout_tower_entry(state, location: 'Sprout Tower', area_type: 'ruins')
      story = ensure_johto_story(state)
      return { 'status' => 'blocked_missing_johto_region_unlock', 'event_id' => SPROUT_TOWER_ENTRY_EVENT_ID } unless johto_unlocked?(state)
      return { 'status' => 'blocked_missing_violet_city_path', 'event_id' => SPROUT_TOWER_ENTRY_EVENT_ID } unless violet_city_path_cleared?(state)
      return { 'status' => 'already_cleared', 'event_id' => SPROUT_TOWER_ENTRY_EVENT_ID } if sprout_tower_entry_cleared?(state)

      add_story_flag(state, 'FLAG_NEXUS_SPROUT_TOWER_ENTRY')
      add_story_flag(state, 'FLAG_NEXUS_ELDER_LI_TOWER_TRIAL')
      add_story_flag(state, 'FLAG_NEXUS_RED_SPROUT_TOWER_RESPECT')
      add_story_flag(state, 'FLAG_NEXUS_BROCK_SPROUT_TOWER_LORE')
      add_story_flag(state, 'FLAG_NEXUS_SILVER_SAGE_CONFLICT')
      add_story_flag(state, 'FLAG_NEXUS_MOONLIGHT_SPROUT_TOWER_RITUAL')
      add_story_flag(state, 'FLAG_NEXUS_ROCKET_BELLSPROUT_RADIO_ANTENNA')
      add_story_flag(state, 'FLAG_NEXUS_GOLD_DUST_TOWER_RELIC_OFFER')
      add_story_flag(state, 'FLAG_NEXUS_NEXUS_ORDER_SPROUT_ROOT_STATIC')
      add_story_flag(state, 'FLAG_NEXUS_FALKNER_ZEPHYR_PREP_UNLOCKED')

      [
        SPROUT_TOWER_ENTRY_EVENT_ID,
        ELDER_LI_TOWER_TRIAL_EVENT_ID,
        RED_SPROUT_TOWER_RESPECT_EVENT_ID,
        BROCK_SPROUT_TOWER_LORE_EVENT_ID,
        SILVER_SAGE_CONFLICT_EVENT_ID,
        MOONLIGHT_SPROUT_TOWER_RITUAL_EVENT_ID,
        ROCKET_BELLSPROUT_RADIO_ANTENNA_EVENT_ID,
        GOLD_DUST_TOWER_RELIC_OFFER_EVENT_ID,
        NEXUS_ORDER_SPROUT_ROOT_STATIC_EVENT_ID,
        FALKNER_ZEPHYR_BADGE_PREP_EVENT_ID
      ].each { |event_id| mark_cleared_event(story, event_id) }

      CompanionProgress.record_scene(
        state,
        'red',
        'sprout_tower_respect',
        location: location,
        summary: 'Red tells Antman that Sprout Tower is not a shortcut to Falkner; it is Johto asking whether a trainer can slow down and listen.',
        area_type: area_type
      )
      CompanionProgress.record_scene(
        state,
        'brock',
        'sprout_tower_lore',
        location: location,
        summary: 'Brock explains how old Johto towers were built as living lessons instead of simple battle halls.',
        area_type: area_type
      )
      CompanionProgress.record_scene(
        state,
        'bill',
        'sprout_tower_root_scan',
        location: location,
        summary: 'Bill traces the tower sway into a deep root signal that looks older than Rocket radio and cleaner than Moonlight dream static.',
        area_type: area_type
      )

      record_rival_story_clue(
        state,
        'silver',
        location,
        'Silver rejected Elder Li at Sprout Tower, calling the sage trial a waste before chasing the same hidden signal Antman found.',
        area_type,
        region: 'johto'
      )

      FactionWar.record_activity(
        state,
        'team_moonlight',
        'johto',
        location,
        'sprout_tower_dream_ritual',
        threat_delta: 2,
        area_type: area_type
      )
      FactionWar.record_activity(
        state,
        'team_rocket',
        'johto',
        location,
        'bellsprout_radio_antenna',
        threat_delta: 1,
        area_type: area_type
      )
      FactionWar.record_activity(
        state,
        'team_gold_dust',
        'johto',
        location,
        'tower_relic_purchase_offer',
        threat_delta: 1,
        area_type: area_type
      )
      FactionWar.record_activity(
        state,
        'nexus_order',
        'johto',
        location,
        'sprout_tower_deep_root_static_hidden',
        threat_delta: 0,
        area_type: area_type
      )
      FactionWar.record_conflict(
        state,
        'team_rocket',
        'team_moonlight',
        location,
        'Rocket antenna work disturbs Moonlight ritual static under Elder Li\'s tower trial.',
        intensity: 2,
        area_type: area_type
      )

      story['current_act'] = 'act_3_falkner_zephyr_badge'
      event = sprout_tower_entry_event_result(location)
      story['event_history'] << event
      story['latest_event'] = event

      WorldLink.queue_message(
        state,
        'story_alert',
        'Sprout Tower shifts under Antman and Red: Elder Li starts the sage trial, Silver storms ahead, Moonlight ritual static rises, and Rocket antenna parts are hidden in the beams.',
        source: 'johto_story',
        area_type: area_type
      )

      event
    end

    def sprout_tower_entry_cleared?(state)
      ensure_johto_story(state)['event_history'].any? { |event| event['event_id'] == SPROUT_TOWER_ENTRY_EVENT_ID }
    end

    def sprout_tower_entry_event_result(location)
      {
        'status' => 'cleared',
        'event_id' => SPROUT_TOWER_ENTRY_EVENT_ID,
        'location' => location.to_s,
        'region' => 'johto',
        'current_act' => 'act_3_falkner_zephyr_badge',
        'elder' => 'Elder Li',
        'trial_type' => 'sage_tower_trial',
        'companions' => %w[red brock bill],
        'rivals' => %w[silver],
        'factions' => %w[team_rocket team_gold_dust team_moonlight nexus_order],
        'linked_events' => [
          ELDER_LI_TOWER_TRIAL_EVENT_ID,
          RED_SPROUT_TOWER_RESPECT_EVENT_ID,
          BROCK_SPROUT_TOWER_LORE_EVENT_ID,
          SILVER_SAGE_CONFLICT_EVENT_ID,
          MOONLIGHT_SPROUT_TOWER_RITUAL_EVENT_ID,
          ROCKET_BELLSPROUT_RADIO_ANTENNA_EVENT_ID,
          GOLD_DUST_TOWER_RELIC_OFFER_EVENT_ID,
          NEXUS_ORDER_SPROUT_ROOT_STATIC_EVENT_ID,
          FALKNER_ZEPHYR_BADGE_PREP_EVENT_ID
        ],
        'gym_leader_tease' => 'Falkner',
        'tower_signal' => 'sprout_tower_root_static_active',
        'hidden_meta_signal' => 'nexus_order_sprout_tower_root_static_unrevealed',
        'unlocks' => %w[falkner_zephyr_badge_prep violet_gym_access elder_li_rematch_lead],
        'next_hook' => 'falkner_zephyr_badge_prep'
      }
    end

    def complete_falkner_zephyr_badge_prep(state, location: 'Violet Gym Aerie', area_type: 'town')
      story = ensure_johto_story(state)
      return { 'status' => 'blocked_missing_johto_region_unlock', 'event_id' => FALKNER_ZEPHYR_BADGE_PREP_MAIN_EVENT_ID } unless johto_unlocked?(state)
      return { 'status' => 'blocked_missing_sprout_tower_entry', 'event_id' => FALKNER_ZEPHYR_BADGE_PREP_MAIN_EVENT_ID } unless sprout_tower_entry_cleared?(state)
      return { 'status' => 'already_cleared', 'event_id' => FALKNER_ZEPHYR_BADGE_PREP_MAIN_EVENT_ID } if falkner_zephyr_badge_prep_cleared?(state)

      add_story_flag(state, 'FLAG_NEXUS_FALKNER_ZEPHYR_BADGE_PREP')
      add_story_flag(state, 'FLAG_NEXUS_FALKNER_WIND_DOJO_TRAINING')
      add_story_flag(state, 'FLAG_NEXUS_RED_FALKNER_PREP')
      add_story_flag(state, 'FLAG_NEXUS_BROCK_FLYING_COUNTER_ADVICE')
      add_story_flag(state, 'FLAG_NEXUS_BILL_GYM_ROOF_SIGNAL_SCAN')
      add_story_flag(state, 'FLAG_NEXUS_SILVER_VIOLET_GYM_PRESSURE')
      add_story_flag(state, 'FLAG_NEXUS_MOONLIGHT_ZEPHYR_DRAFT')
      add_story_flag(state, 'FLAG_NEXUS_ROCKET_GYM_ROOF_RELAY')
      add_story_flag(state, 'FLAG_NEXUS_GOLD_DUST_FEATHER_CHARM_MARKET')
      add_story_flag(state, 'FLAG_NEXUS_ZEPHYR_BADGE_BATTLE_UNLOCKED')

      [
        FALKNER_ZEPHYR_BADGE_PREP_MAIN_EVENT_ID,
        FALKNER_WIND_DOJO_TRAINING_EVENT_ID,
        RED_FALKNER_PREP_EVENT_ID,
        BROCK_FLYING_COUNTER_ADVICE_EVENT_ID,
        BILL_GYM_ROOF_SIGNAL_SCAN_EVENT_ID,
        SILVER_VIOLET_GYM_PRESSURE_EVENT_ID,
        MOONLIGHT_ZEPHYR_DRAFT_EVENT_ID,
        ROCKET_GYM_ROOF_RELAY_EVENT_ID,
        GOLD_DUST_FEATHER_CHARM_MARKET_EVENT_ID,
        NEXUS_ORDER_ZEPHYR_AIR_CURRENT_EVENT_ID,
        ZEPHYR_BADGE_BATTLE_UNLOCKED_EVENT_ID
      ].each { |event_id| mark_cleared_event(story, event_id) }

      CompanionProgress.record_scene(
        state,
        'red',
        'falkner_wind_prep',
        location: location,
        summary: 'Red runs Antman through patient wind reads before the first Johto gym, then steps back so the badge battle stays solo.',
        area_type: area_type
      )
      CompanionProgress.record_scene(
        state,
        'brock',
        'flying_counter_advice',
        location: location,
        summary: 'Brock turns Falkner prep into practical counterplay: sturdy positioning, rock coverage, electric timing, and not chasing birds into bad trades.',
        area_type: area_type
      )
      CompanionProgress.record_scene(
        state,
        'bill',
        'violet_gym_roof_signal_scan',
        location: location,
        summary: 'Bill finds the gym roof currents are carrying the same tower-root signal that Moonlight and Rocket keep contaminating.',
        area_type: area_type
      )

      record_rival_story_clue(
        state,
        'silver',
        location,
        'Silver watched Falkner from the Violet Gym rafters, irritated that Antman is earning respect instead of forcing shortcuts.',
        area_type,
        region: 'johto'
      )

      FactionWar.record_activity(
        state,
        'team_moonlight',
        'johto',
        location,
        'zephyr_draft_dream_static',
        threat_delta: 1,
        area_type: area_type
      )
      FactionWar.record_activity(
        state,
        'team_rocket',
        'johto',
        location,
        'violet_gym_roof_relay',
        threat_delta: 1,
        area_type: area_type
      )
      FactionWar.record_activity(
        state,
        'team_gold_dust',
        'johto',
        location,
        'feather_charm_market',
        threat_delta: 1,
        area_type: area_type
      )
      FactionWar.record_activity(
        state,
        'nexus_order',
        'johto',
        location,
        'zephyr_air_current_static_hidden',
        threat_delta: 0,
        area_type: area_type
      )
      FactionWar.record_conflict(
        state,
        'team_rocket',
        'team_moonlight',
        location,
        'Rocket roof relay signals break apart in Moonlight zephyr-draft static above Falkner\'s gym.',
        intensity: 1,
        area_type: area_type
      )

      story['current_act'] = 'act_3_falkner_zephyr_badge'
      event = falkner_zephyr_badge_prep_event_result(location)
      story['event_history'] << event
      story['latest_event'] = event

      WorldLink.queue_message(
        state,
        'story_alert',
        'Falkner opens the Zephyr Badge trial: Red and Brock prep Antman outside the gym while Bill tracks roof-current static before the solo battle.',
        source: 'johto_story',
        area_type: area_type
      )

      event
    end

    def falkner_zephyr_badge_prep_cleared?(state)
      ensure_johto_story(state)['event_history'].any? { |event| event['event_id'] == FALKNER_ZEPHYR_BADGE_PREP_MAIN_EVENT_ID }
    end

    def falkner_zephyr_badge_prep_event_result(location)
      {
        'status' => 'cleared',
        'event_id' => FALKNER_ZEPHYR_BADGE_PREP_MAIN_EVENT_ID,
        'location' => location.to_s,
        'region' => 'johto',
        'current_act' => 'act_3_falkner_zephyr_badge',
        'gym_leader' => 'Falkner',
        'badge' => 'Zephyr Badge',
        'level_cap' => 16,
        'companions' => %w[red brock bill],
        'rivals' => %w[silver],
        'factions' => %w[team_rocket team_gold_dust team_moonlight nexus_order],
        'linked_events' => [
          FALKNER_WIND_DOJO_TRAINING_EVENT_ID,
          RED_FALKNER_PREP_EVENT_ID,
          BROCK_FLYING_COUNTER_ADVICE_EVENT_ID,
          BILL_GYM_ROOF_SIGNAL_SCAN_EVENT_ID,
          SILVER_VIOLET_GYM_PRESSURE_EVENT_ID,
          MOONLIGHT_ZEPHYR_DRAFT_EVENT_ID,
          ROCKET_GYM_ROOF_RELAY_EVENT_ID,
          GOLD_DUST_FEATHER_CHARM_MARKET_EVENT_ID,
          NEXUS_ORDER_ZEPHYR_AIR_CURRENT_EVENT_ID,
          ZEPHYR_BADGE_BATTLE_UNLOCKED_EVENT_ID
        ],
        'battle_hook' => {
          'battle_id' => 'falkner_zephyr_badge_battle',
          'battle_type' => 'johto_gym_leader_falkner',
          'location' => 'Violet Gym',
          'level_cap' => 16,
          'companion_rule' => 'no_companion_assist_in_gym_battle',
          'standard_team' => [
            { 'species' => 'Hoothoot', 'level' => 13, 'role' => 'sleep_pressure' },
            { 'species' => 'Pidgey', 'level' => 14, 'role' => 'speed_intro' },
            { 'species' => 'Pidgeotto', 'level' => 16, 'role' => 'ace' }
          ]
        },
        'hidden_meta_signal' => 'nexus_order_zephyr_air_current_static_unrevealed',
        'unlocks' => %w[zephyr_badge_battle violet_gym_air_current_trial falkner_rematch_seed],
        'next_hook' => 'falkner_zephyr_badge_battle'
      }
    end
  end
end
