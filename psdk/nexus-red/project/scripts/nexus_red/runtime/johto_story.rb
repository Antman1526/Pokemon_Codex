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
    FALKNER_ZEPHYR_BADGE_BATTLE_EVENT_ID = 'falkner_zephyr_badge_battle'
    ZEPHYR_BADGE_OBTAINED_EVENT_ID = 'zephyr_badge_obtained'
    RED_POST_FALKNER_EVENT_ID = 'red_post_falkner'
    BROCK_POST_FALKNER_EVENT_ID = 'brock_post_falkner'
    BILL_ZEPHYR_SIGNAL_DECODED_EVENT_ID = 'bill_zephyr_signal_decoded'
    SILVER_ZEPHYR_BADGE_RACE_EVENT_ID = 'silver_zephyr_badge_race'
    ROCKET_UNION_CAVE_LEAD_EVENT_ID = 'rocket_union_cave_lead'
    MOONLIGHT_ZEPHYR_RETREAT_EVENT_ID = 'moonlight_zephyr_retreat'
    GOLD_DUST_ZEPHYR_BETTING_EVENT_ID = 'gold_dust_zephyr_badge_betting'
    NEXUS_ORDER_ZEPHYR_BADGE_RESONANCE_EVENT_ID = 'nexus_order_zephyr_badge_resonance_hidden'
    UNION_CAVE_ROAD_EVENT_ID = 'union_cave_road_unlocked'
    AZALEA_SLOWPOKE_WELL_LEAD_EVENT_ID = 'azalea_slowpoke_well_lead'
    UNION_CAVE_ROAD_MAIN_EVENT_ID = 'union_cave_road'
    RED_UNION_CAVE_TRAVEL_EVENT_ID = 'red_union_cave_travel'
    BROCK_UNION_CAVE_SURVIVAL_EVENT_ID = 'brock_union_cave_survival'
    BILL_UNION_CAVE_RADIO_SCAN_EVENT_ID = 'bill_union_cave_radio_scan'
    SILVER_UNION_CAVE_AMBUSH_EVENT_ID = 'silver_union_cave_ambush'
    ROCKET_SLOWPOKE_WELL_SUPPLY_EVENT_ID = 'rocket_slowpoke_well_supply_line'
    GOLD_DUST_UNION_CAVE_RELIC_EVENT_ID = 'gold_dust_union_cave_relic_auction'
    MOONLIGHT_UNION_CAVE_ECHO_EVENT_ID = 'moonlight_union_cave_echo'
    NEXUS_ORDER_UNION_CAVE_FAULT_EVENT_ID = 'nexus_order_union_cave_fault_line_hidden'
    AZALEA_TOWN_UNLOCKED_EVENT_ID = 'azalea_town_unlocked'
    SLOWPOKE_WELL_CRISIS_UNLOCKED_EVENT_ID = 'slowpoke_well_crisis_unlocked'
    KURT_APRICORN_LEAD_EVENT_ID = 'kurt_apricorn_lead'
    SLOWPOKE_WELL_CRISIS_EVENT_ID = 'slowpoke_well_crisis'
    KURT_SLOWPOKE_WELL_RESCUE_EVENT_ID = 'kurt_slowpoke_well_rescue'
    RED_SLOWPOKE_WELL_RAID_EVENT_ID = 'red_slowpoke_well_raid'
    BROCK_SLOWPOKE_CARE_EVENT_ID = 'brock_slowpoke_care'
    BILL_ROCKET_RADIO_CORE_EVENT_ID = 'bill_rocket_radio_core'
    ROCKET_SLOWPOKE_TAIL_RING_EVENT_ID = 'rocket_slowpoke_tail_ring'
    GOLD_DUST_APRICORN_MARKET_EVENT_ID = 'gold_dust_apricorn_black_market'
    MOONLIGHT_SLOWPOKE_WELL_ECHO_EVENT_ID = 'moonlight_slowpoke_well_echo'
    NEXUS_ORDER_SLOWPOKE_WELL_PULSE_EVENT_ID = 'nexus_order_slowpoke_well_pulse_hidden'
    AZALEA_SERVICES_RESTORED_EVENT_ID = 'azalea_services_restored'
    BUGSY_HIVE_BADGE_PREP_EVENT_ID = 'bugsy_hive_badge_prep_unlocked'
    BUGSY_HIVE_BADGE_PREP_MAIN_EVENT_ID = 'bugsy_hive_badge_prep'
    RED_BUGSY_PREP_EVENT_ID = 'red_bugsy_prep'
    BROCK_BUG_COUNTER_ADVICE_EVENT_ID = 'brock_bug_counter_advice'
    BILL_DREAM_SPORE_SCAN_EVENT_ID = 'bill_dream_spore_scan'
    BUGSY_GYM_SCOUTING_EVENT_ID = 'bugsy_gym_scouting'
    MOONLIGHT_BUGSY_DREAM_SPORE_EVENT_ID = 'moonlight_bugsy_dream_spore'
    ROCKET_AZALEA_RETREAT_BURST_EVENT_ID = 'rocket_azalea_retreat_radio_burst'
    GOLD_DUST_HIVE_CHARM_MARKET_EVENT_ID = 'gold_dust_hive_badge_charm_market'
    NEXUS_ORDER_HIVE_PATTERN_EVENT_ID = 'nexus_order_hive_pattern_signal_hidden'
    BUGSY_HIVE_BADGE_BATTLE_UNLOCKED_EVENT_ID = 'bugsy_hive_badge_battle_unlocked'
    BUGSY_HIVE_BADGE_BATTLE_EVENT_ID = 'bugsy_hive_badge_battle'
    HIVE_BADGE_OBTAINED_EVENT_ID = 'hive_badge_obtained'
    RED_POST_BUGSY_EVENT_ID = 'red_post_bugsy'
    BROCK_POST_BUGSY_EVENT_ID = 'brock_post_bugsy'
    BILL_HIVE_SIGNAL_DECODED_EVENT_ID = 'bill_hive_signal_decoded'
    SILVER_ILEX_FOREST_RACE_EVENT_ID = 'silver_ilex_forest_race'
    MOONLIGHT_DREAM_SPORE_COLLAPSE_EVENT_ID = 'moonlight_dream_spore_collapse'
    ROCKET_ILEX_RETREAT_EVENT_ID = 'rocket_ilex_cut_through_retreat'
    GOLD_DUST_ILEX_RELIC_BID_EVENT_ID = 'gold_dust_ilex_charcoal_relic_bid'
    NEXUS_ORDER_HIVE_BADGE_PATTERN_EVENT_ID = 'nexus_order_hive_badge_pattern_hidden'
    ILEX_FOREST_PATH_UNLOCKED_EVENT_ID = 'ilex_forest_path_unlocked'
    ILEX_FOREST_PATH_EVENT_ID = 'ilex_forest_path'
    RED_ILEX_FOREST_GUIDE_EVENT_ID = 'red_ilex_forest_guide'
    BROCK_ILEX_FOREST_FIELD_CARE_EVENT_ID = 'brock_ilex_forest_field_care'
    BILL_ILEX_RELAY_TRACE_EVENT_ID = 'bill_ilex_relay_trace'
    FARFETCHD_FIELD_TOOL_LEAD_EVENT_ID = 'farfetchd_field_tool_lead'
    TRAIL_CUTTER_ILEX_LEAD_EVENT_ID = 'trail_cutter_ilex_lead'
    SILVER_ILEX_SHORTCUT_PRESSURE_EVENT_ID = 'silver_ilex_shortcut_pressure'
    ROCKET_ILEX_RETREAT_CACHE_EVENT_ID = 'rocket_ilex_retreat_cache'
    GOLD_DUST_CHARCOAL_RELIC_EVENT_ID = 'gold_dust_charcoal_relic_bid'
    MOONLIGHT_ILEX_RESIDUE_EVENT_ID = 'moonlight_ilex_residue'
    NEXUS_ORDER_ILEX_SHRINE_PATTERN_EVENT_ID = 'nexus_order_ilex_shrine_pattern_hidden'
    GOLDENROD_ROAD_UNLOCKED_EVENT_ID = 'goldenrod_road_unlocked'
    GOLDENROD_ROAD_EVENT_ID = 'goldenrod_road'
    ROUTE34_DAYCARE_OPENED_EVENT_ID = 'route_34_daycare_opened'
    GOLDENROD_CITY_ARRIVAL_EVENT_ID = 'goldenrod_city_arrival'
    GOLDENROD_RADIO_TOWER_TEASE_EVENT_ID = 'goldenrod_radio_tower_tease'
    WHITNEY_GYM_TEASE_EVENT_ID = 'whitney_gym_tease'
    RED_GOLDENROD_ROAD_TRAINING_EVENT_ID = 'red_goldenrod_road_training'
    BROCK_ROUTE34_DAYCARE_ADVICE_EVENT_ID = 'brock_route34_daycare_advice'
    BILL_GOLDENROD_SIGNAL_SCAN_EVENT_ID = 'bill_goldenrod_signal_scan'
    BLUE_GOLDENROD_STANDINGS_EVENT_ID = 'blue_goldenrod_standings_ping'
    AVA_ROUTE34_DAYCARE_RESEARCH_EVENT_ID = 'ava_route34_daycare_research'
    SILVER_GOLDENROD_PRESSURE_EVENT_ID = 'silver_goldenrod_pressure'
    ROCKET_GOLDENROD_RADIO_SHADOW_EVENT_ID = 'rocket_goldenrod_radio_tower_shadow'
    GOLD_DUST_GOLDENROD_COIN_MARKET_EVENT_ID = 'gold_dust_goldenrod_coin_market'
    TEAM_GAS_GOLDENROD_UNDERGROUND_EVENT_ID = 'team_gas_goldenrod_underground_vent_probe'
    MOONLIGHT_GOLDENROD_RADIO_JINGLE_EVENT_ID = 'moonlight_goldenrod_radio_sleep_jingle'
    NEXUS_ORDER_GOLDENROD_FREQUENCY_EVENT_ID = 'nexus_order_goldenrod_frequency_hidden'
    WHITNEY_PLAIN_BADGE_PREP_UNLOCKED_EVENT_ID = 'whitney_plain_badge_prep_unlocked'
    WHITNEY_PLAIN_BADGE_PREP_EVENT_ID = 'whitney_plain_badge_prep'
    WHITNEY_ROLLOUT_COUNTER_TRAINING_EVENT_ID = 'whitney_rollout_counter_training'
    RED_WHITNEY_PREP_EVENT_ID = 'red_whitney_prep'
    BROCK_WHITNEY_COUNTER_ADVICE_EVENT_ID = 'brock_whitney_counter_advice'
    BILL_RADIO_TOWER_BADGE_SCAN_EVENT_ID = 'bill_radio_tower_badge_scan'
    BLUE_MILTANK_WARNING_EVENT_ID = 'blue_miltank_warning'
    SILVER_WHITNEY_PRESSURE_EVENT_ID = 'silver_whitney_pressure'
    ROCKET_PLAIN_BADGE_RADIO_SYNC_EVENT_ID = 'rocket_plain_badge_radio_sync'
    GOLD_DUST_WHITNEY_BETTING_EVENT_ID = 'gold_dust_whitney_match_betting_ring'
    TEAM_GAS_GYM_BASEMENT_PRESSURE_EVENT_ID = 'team_gas_gym_basement_vent_pressure'
    MOONLIGHT_PLAIN_BADGE_JINGLE_EVENT_ID = 'moonlight_plain_badge_sleep_jingle'
    NEXUS_ORDER_PLAIN_BADGE_FREQUENCY_EVENT_ID = 'nexus_order_plain_badge_frequency_hidden'
    WHITNEY_PLAIN_BADGE_BATTLE_UNLOCKED_EVENT_ID = 'whitney_plain_badge_battle_unlocked'
    WHITNEY_PLAIN_BADGE_BATTLE_EVENT_ID = 'whitney_plain_badge_battle'
    PLAIN_BADGE_OBTAINED_EVENT_ID = 'plain_badge_obtained'
    RED_POST_WHITNEY_EVENT_ID = 'red_post_whitney'
    BROCK_POST_WHITNEY_EVENT_ID = 'brock_post_whitney'
    BILL_PLAIN_BADGE_SIGNAL_DECODED_EVENT_ID = 'bill_plain_badge_signal_decoded'
    BLUE_POST_WHITNEY_RESPECT_EVENT_ID = 'blue_post_whitney_respect'
    SILVER_RADIO_TOWER_RACE_EVENT_ID = 'silver_radio_tower_race'
    ROCKET_RADIO_TOWER_TAKEOVER_STAGING_EVENT_ID = 'rocket_radio_tower_takeover_staging'
    GOLD_DUST_WHITNEY_MATCH_PAYOUTS_EVENT_ID = 'gold_dust_whitney_match_payouts'
    TEAM_GAS_UNDERGROUND_EXHAUST_LEAK_EVENT_ID = 'team_gas_underground_exhaust_leak'
    MOONLIGHT_PLAIN_BADGE_JINGLE_COLLAPSE_EVENT_ID = 'moonlight_plain_badge_jingle_collapse'
    NEXUS_ORDER_PLAIN_BADGE_RESONANCE_EVENT_ID = 'nexus_order_plain_badge_resonance_hidden'
    GOLDENROD_RADIO_TOWER_CRISIS_UNLOCKED_EVENT_ID = 'goldenrod_radio_tower_crisis_unlocked'
    GOLDENROD_RADIO_TOWER_SHADOW_EVENT_ID = 'goldenrod_radio_tower_shadow'
    RADIO_TOWER_LOCKDOWN_EVENT_ID = 'radio_tower_lockdown'
    RED_RADIO_TOWER_ENTRY_EVENT_ID = 'red_radio_tower_entry_guard'
    BLUE_RADIO_TOWER_CROWD_CONTROL_EVENT_ID = 'blue_radio_tower_crowd_control'
    BILL_BROADCAST_JAM_EVENT_ID = 'bill_broadcast_jam_decode'
    SILVER_RADIO_TOWER_SIDE_DOOR_EVENT_ID = 'silver_radio_tower_side_door'
    AVA_GOLDENROD_BROADCAST_CLUE_EVENT_ID = 'ava_goldenrod_broadcast_clue'
    ROCKET_RADIO_TOWER_LOBBY_TAKEOVER_EVENT_ID = 'rocket_radio_tower_lobby_takeover'
    GOLD_DUST_RADIO_TOWER_AD_BUY_EVENT_ID = 'gold_dust_radio_tower_ad_buy_laundering'
    TEAM_GAS_RADIO_TOWER_GENERATOR_EVENT_ID = 'team_gas_radio_tower_generator_vent_pressure'
    MOONLIGHT_BROADCAST_HYPNOSIS_EVENT_ID = 'moonlight_broadcast_hypnosis_leak'
    NEXUS_ORDER_RADIO_TRANSMITTER_PATTERN_EVENT_ID = 'nexus_order_radio_tower_transmitter_pattern_hidden'
    RADIO_TOWER_LOBBY_BATTLE_UNLOCKED_EVENT_ID = 'radio_tower_lobby_battle_unlocked'
    GOLDENROD_UNDERGROUND_WAREHOUSE_LEAD_EVENT_ID = 'goldenrod_underground_warehouse_lead'
    RADIO_TOWER_LOBBY_BATTLE_EVENT_ID = 'radio_tower_lobby_battle'
    RADIO_TOWER_LOBBY_CLEARED_EVENT_ID = 'radio_tower_lobby_cleared'
    RED_BLUE_RADIO_TOWER_TAG_EVENT_ID = 'red_blue_radio_tower_tag'
    BILL_LOBBY_SIGNAL_CACHE_EVENT_ID = 'bill_lobby_signal_cache'
    SILVER_UNDERGROUND_WAREHOUSE_RACE_EVENT_ID = 'silver_underground_warehouse_race'
    AVA_ROCKET_BROADCAST_ARCHIVE_EVENT_ID = 'ava_rocket_broadcast_archive'
    ROCKET_EXECUTIVE_ELEVATOR_LOCK_EVENT_ID = 'rocket_executive_elevator_lock'
    GOLD_DUST_AD_LEDGER_DROP_EVENT_ID = 'gold_dust_ad_ledger_drop'
    TEAM_GAS_GENERATOR_SMOKE_EVENT_ID = 'team_gas_generator_smoke'
    MOONLIGHT_LOBBY_SIGNAL_FADE_EVENT_ID = 'moonlight_lobby_signal_fade'
    NEXUS_ORDER_ELEVATOR_PATTERN_EVENT_ID = 'nexus_order_elevator_pattern_hidden'
    GOLDENROD_UNDERGROUND_WAREHOUSE_UNLOCKED_EVENT_ID = 'goldenrod_underground_warehouse_unlocked'
    GOLDENROD_UNDERGROUND_WAREHOUSE_EVENT_ID = 'goldenrod_underground_warehouse'
    WAREHOUSE_SWITCH_ROOM_EVENT_ID = 'warehouse_switch_room'
    RED_WAREHOUSE_BACKUP_EVENT_ID = 'red_warehouse_backup'
    BLUE_RADIO_TOWER_LOBBY_HOLD_EVENT_ID = 'blue_radio_tower_lobby_hold'
    BILL_DIRECTOR_CARD_TRACE_EVENT_ID = 'bill_director_card_trace'
    SILVER_WAREHOUSE_RIVAL_CLASH_EVENT_ID = 'silver_warehouse_rival_clash'
    AVA_UNDERGROUND_LEDGER_DECODE_EVENT_ID = 'ava_underground_ledger_decode'
    ROCKET_DIRECTOR_CARD_THEFT_EVENT_ID = 'rocket_director_card_theft'
    GOLD_DUST_WAREHOUSE_LEDGER_GRAB_EVENT_ID = 'gold_dust_warehouse_ledger_grab'
    TEAM_GAS_SWITCH_ROOM_FUMES_EVENT_ID = 'team_gas_switch_room_fumes'
    MOONLIGHT_BASEMENT_SIGNAL_RELAY_EVENT_ID = 'moonlight_basement_signal_relay'
    NEXUS_ORDER_BASEMENT_GRID_EVENT_ID = 'nexus_order_basement_grid_hidden'
    RADIO_TOWER_DIRECTOR_RESCUE_UNLOCKED_EVENT_ID = 'radio_tower_director_rescue_unlocked'
    RADIO_TOWER_DIRECTOR_RESCUE_EVENT_ID = 'radio_tower_director_rescue'
    RADIO_TOWER_DIRECTOR_SAFE_EVENT_ID = 'radio_tower_director_safe'
    CARD_KEY_SHUTTER_UNLOCK_EVENT_ID = 'card_key_shutter_unlock'
    RED_DIRECTOR_RESCUE_GUARD_EVENT_ID = 'red_director_rescue_guard'
    BLUE_REJOINS_TOWER_CLIMB_EVENT_ID = 'blue_rejoins_tower_climb'
    BILL_TRANSMITTER_KEY_DECODE_EVENT_ID = 'bill_transmitter_key_decode'
    SILVER_EXECUTIVE_STAIRS_PRESSURE_EVENT_ID = 'silver_executive_stairs_pressure'
    AVA_DIRECTOR_TESTIMONY_UPLOAD_EVENT_ID = 'ava_director_testimony_upload'
    ROCKET_DIRECTOR_IMPERSONATION_CONFIRMED_EVENT_ID = 'rocket_director_impersonation_confirmed'
    GOLD_DUST_RANSOM_LEDGER_EVENT_ID = 'gold_dust_ransom_ledger_recovered'
    TEAM_GAS_TRANSMITTER_COOLANT_EVENT_ID = 'team_gas_transmitter_coolant_pressure'
    MOONLIGHT_DIRECTOR_VOICEPRINT_EVENT_ID = 'moonlight_director_voiceprint_echo'
    NEXUS_ORDER_DIRECTOR_SIGNAL_MASK_EVENT_ID = 'nexus_order_director_signal_mask_hidden'
    RADIO_TOWER_EXECUTIVE_FLOOR_UNLOCKED_EVENT_ID = 'radio_tower_executive_floor_unlocked'
    RADIO_TOWER_EXECUTIVE_FLOOR_EVENT_ID = 'radio_tower_executive_floor'
    RADIO_TOWER_ADMIN_GAUNTLET_EVENT_ID = 'radio_tower_admin_gauntlet'
    RED_BLUE_EXECUTIVE_TAG_EVENT_ID = 'red_blue_executive_tag'
    BILL_TRANSMITTER_ADMIN_TRACE_EVENT_ID = 'bill_transmitter_admin_trace'
    SILVER_ROCKET_ADMIN_CHALLENGE_EVENT_ID = 'silver_rocket_admin_challenge'
    AVA_EXECUTIVE_SIGNAL_ARCHIVE_EVENT_ID = 'ava_executive_signal_archive'
    ROCKET_EXECUTIVE_BROADCAST_COMMAND_EVENT_ID = 'rocket_executive_broadcast_command'
    GOLD_DUST_EXECUTIVE_PAYOUT_LEDGER_EVENT_ID = 'gold_dust_executive_payout_ledger'
    TEAM_GAS_TRANSMITTER_OVERHEAT_EVENT_ID = 'team_gas_transmitter_overheat'
    MOONLIGHT_EXECUTIVE_VOICE_LOOP_EVENT_ID = 'moonlight_executive_voice_loop'
    NEXUS_ORDER_EXECUTIVE_SIGNAL_LATTICE_EVENT_ID = 'nexus_order_executive_signal_lattice_hidden'
    RADIO_TOWER_TRANSMITTER_SHUTDOWN_UNLOCKED_EVENT_ID = 'radio_tower_transmitter_shutdown_unlocked'

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

    def complete_falkner_zephyr_badge_battle(state, location: 'Violet Gym', result: 'won', area_type: 'gym')
      story = ensure_johto_story(state)
      return { 'status' => 'blocked_missing_johto_region_unlock', 'event_id' => FALKNER_ZEPHYR_BADGE_BATTLE_EVENT_ID } unless johto_unlocked?(state)
      return { 'status' => 'blocked_missing_falkner_zephyr_badge_prep', 'event_id' => FALKNER_ZEPHYR_BADGE_BATTLE_EVENT_ID } unless falkner_zephyr_badge_prep_cleared?(state)
      return { 'status' => 'already_cleared', 'event_id' => FALKNER_ZEPHYR_BADGE_BATTLE_EVENT_ID } if falkner_zephyr_badge_battle_cleared?(state)

      add_story_flag(state, 'zephyr_badge_obtained')
      add_story_flag(state, 'FLAG_NEXUS_ZEPHYR_BADGE')
      add_story_flag(state, 'FLAG_NEXUS_FALKNER_BATTLE_STARTED')
      add_story_flag(state, 'FLAG_NEXUS_FALKNER_BATTLE_FINISHED')
      add_story_flag(state, 'FLAG_NEXUS_RED_POST_FALKNER')
      add_story_flag(state, 'FLAG_NEXUS_BROCK_POST_FALKNER')
      add_story_flag(state, 'FLAG_NEXUS_BILL_ZEPHYR_SIGNAL_DECODED')
      add_story_flag(state, 'FLAG_NEXUS_UNION_CAVE_ROAD_UNLOCKED')
      add_story_flag(state, 'FLAG_NEXUS_AZALEA_SLOWPOKE_WELL_LEAD')
      add_story_flag(state, 'FLAG_NEXUS_ROCKET_UNION_CAVE_LEAD')

      [
        FALKNER_ZEPHYR_BADGE_BATTLE_EVENT_ID,
        ZEPHYR_BADGE_OBTAINED_EVENT_ID,
        RED_POST_FALKNER_EVENT_ID,
        BROCK_POST_FALKNER_EVENT_ID,
        BILL_ZEPHYR_SIGNAL_DECODED_EVENT_ID,
        SILVER_ZEPHYR_BADGE_RACE_EVENT_ID,
        ROCKET_UNION_CAVE_LEAD_EVENT_ID,
        MOONLIGHT_ZEPHYR_RETREAT_EVENT_ID,
        GOLD_DUST_ZEPHYR_BETTING_EVENT_ID,
        NEXUS_ORDER_ZEPHYR_BADGE_RESONANCE_EVENT_ID,
        UNION_CAVE_ROAD_EVENT_ID,
        AZALEA_SLOWPOKE_WELL_LEAD_EVENT_ID
      ].each { |event_id| mark_cleared_event(story, event_id) }

      CompanionProgress.record_scene(
        state,
        'red',
        'post_falkner_respect',
        location: location,
        summary: 'Red congratulates Antman after the Zephyr Badge, quietly proud that the first Johto badge was earned without help in the gym.',
        area_type: area_type
      )
      CompanionProgress.record_scene(
        state,
        'brock',
        'post_falkner_counter_review',
        location: location,
        summary: 'Brock reviews the Falkner battle and points Antman toward the longer road through Union Cave.',
        area_type: area_type
      )
      CompanionProgress.record_scene(
        state,
        'bill',
        'zephyr_signal_decode',
        location: location,
        summary: 'Bill decodes the Zephyr Badge resonance and finds Rocket radio parts moving toward Union Cave and Azalea.',
        area_type: area_type
      )

      record_rival_story_clue(
        state,
        'silver',
        location,
        'Silver saw Antman earn the Zephyr Badge and left Violet furious, racing toward Union Cave instead of congratulating anyone.',
        area_type,
        region: 'johto'
      )

      FactionWar.record_activity(
        state,
        'team_rocket',
        'johto',
        'Union Cave Road',
        'union_cave_radio_parts_route',
        threat_delta: 1,
        area_type: area_type
      )
      FactionWar.record_activity(
        state,
        'team_moonlight',
        'johto',
        location,
        'zephyr_dream_static_retreat',
        threat_delta: 1,
        area_type: area_type
      )
      FactionWar.record_activity(
        state,
        'team_gold_dust',
        'johto',
        location,
        'zephyr_badge_betting_market',
        threat_delta: 1,
        area_type: area_type
      )
      FactionWar.record_activity(
        state,
        'nexus_order',
        'johto',
        location,
        'zephyr_badge_resonance_hidden',
        threat_delta: 0,
        area_type: area_type
      )

      story['current_act'] = 'act_4_azalea_and_slowpoke_well'
      event = falkner_zephyr_badge_battle_event_result(location, result)
      story['event_history'] << event
      story['latest_event'] = event

      WorldLink.queue_message(
        state,
        'story_alert',
        'Antman earned the Zephyr Badge. Union Cave opens toward Azalea, and Bill sees Rocket radio parts moving near the Slowpoke Well lead.',
        source: 'johto_story',
        area_type: area_type
      )

      event
    end

    def falkner_zephyr_badge_battle_cleared?(state)
      ensure_johto_story(state)['event_history'].any? { |event| event['event_id'] == FALKNER_ZEPHYR_BADGE_BATTLE_EVENT_ID }
    end

    def falkner_zephyr_badge_battle_event_result(location, result)
      {
        'status' => 'cleared',
        'event_id' => FALKNER_ZEPHYR_BADGE_BATTLE_EVENT_ID,
        'battle_id' => FALKNER_ZEPHYR_BADGE_BATTLE_EVENT_ID,
        'location' => location.to_s,
        'region' => 'johto',
        'current_act' => 'act_4_azalea_and_slowpoke_well',
        'result' => result.to_s,
        'gym_leader' => 'Falkner',
        'badge' => 'Zephyr Badge',
        'level_cap' => 16,
        'companion_rule' => 'no_companion_assist_in_gym_battle',
        'companions' => %w[red brock bill],
        'rivals' => %w[silver],
        'factions' => %w[team_rocket team_gold_dust team_moonlight nexus_order],
        'linked_events' => [
          ZEPHYR_BADGE_OBTAINED_EVENT_ID,
          RED_POST_FALKNER_EVENT_ID,
          BROCK_POST_FALKNER_EVENT_ID,
          BILL_ZEPHYR_SIGNAL_DECODED_EVENT_ID,
          SILVER_ZEPHYR_BADGE_RACE_EVENT_ID,
          ROCKET_UNION_CAVE_LEAD_EVENT_ID,
          MOONLIGHT_ZEPHYR_RETREAT_EVENT_ID,
          GOLD_DUST_ZEPHYR_BETTING_EVENT_ID,
          NEXUS_ORDER_ZEPHYR_BADGE_RESONANCE_EVENT_ID,
          UNION_CAVE_ROAD_EVENT_ID,
          AZALEA_SLOWPOKE_WELL_LEAD_EVENT_ID
        ],
        'hidden_meta_signal' => 'nexus_order_zephyr_badge_resonance_unrevealed',
        'unlocks' => %w[union_cave_road azalea_slowpoke_well_lead johto_rematch_board_tier_1],
        'next_hook' => 'union_cave_road'
      }
    end

    def complete_union_cave_road(state, location: 'Union Cave', area_type: 'cave')
      story = ensure_johto_story(state)
      return { 'status' => 'blocked_missing_johto_region_unlock', 'event_id' => UNION_CAVE_ROAD_MAIN_EVENT_ID } unless johto_unlocked?(state)
      return { 'status' => 'blocked_missing_falkner_zephyr_badge_battle', 'event_id' => UNION_CAVE_ROAD_MAIN_EVENT_ID } unless falkner_zephyr_badge_battle_cleared?(state)
      return { 'status' => 'already_cleared', 'event_id' => UNION_CAVE_ROAD_MAIN_EVENT_ID } if union_cave_road_cleared?(state)

      add_story_flag(state, 'FLAG_NEXUS_UNION_CAVE_ROAD')
      add_story_flag(state, 'FLAG_NEXUS_RED_UNION_CAVE_TRAVEL')
      add_story_flag(state, 'FLAG_NEXUS_BROCK_UNION_CAVE_SURVIVAL')
      add_story_flag(state, 'FLAG_NEXUS_BILL_UNION_CAVE_RADIO_SCAN')
      add_story_flag(state, 'FLAG_NEXUS_SILVER_UNION_CAVE_AMBUSH')
      add_story_flag(state, 'FLAG_NEXUS_ROCKET_SLOWPOKE_WELL_SUPPLY_LINE')
      add_story_flag(state, 'FLAG_NEXUS_GOLD_DUST_UNION_CAVE_RELIC_AUCTION')
      add_story_flag(state, 'FLAG_NEXUS_MOONLIGHT_UNION_CAVE_ECHO')
      add_story_flag(state, 'FLAG_NEXUS_NEXUS_ORDER_UNION_CAVE_FAULT_LINE')
      add_story_flag(state, 'FLAG_NEXUS_AZALEA_TOWN_UNLOCKED')
      add_story_flag(state, 'FLAG_NEXUS_SLOWPOKE_WELL_CRISIS_UNLOCKED')
      add_story_flag(state, 'FLAG_NEXUS_KURT_APRICORN_LEAD')

      [
        UNION_CAVE_ROAD_MAIN_EVENT_ID,
        RED_UNION_CAVE_TRAVEL_EVENT_ID,
        BROCK_UNION_CAVE_SURVIVAL_EVENT_ID,
        BILL_UNION_CAVE_RADIO_SCAN_EVENT_ID,
        SILVER_UNION_CAVE_AMBUSH_EVENT_ID,
        ROCKET_SLOWPOKE_WELL_SUPPLY_EVENT_ID,
        GOLD_DUST_UNION_CAVE_RELIC_EVENT_ID,
        MOONLIGHT_UNION_CAVE_ECHO_EVENT_ID,
        NEXUS_ORDER_UNION_CAVE_FAULT_EVENT_ID,
        AZALEA_TOWN_UNLOCKED_EVENT_ID,
        SLOWPOKE_WELL_CRISIS_UNLOCKED_EVENT_ID,
        KURT_APRICORN_LEAD_EVENT_ID
      ].each { |event_id| mark_cleared_event(story, event_id) }

      CompanionProgress.record_scene(
        state,
        'red',
        'union_cave_travel',
        location: location,
        summary: 'Red keeps pace beside Antman through Union Cave, reminding him that Johto rewards trainers who listen before they charge ahead.',
        area_type: area_type
      )
      CompanionProgress.record_scene(
        state,
        'brock',
        'union_cave_survival',
        location: location,
        summary: 'Brock turns Union Cave into a field lesson on water pockets, rockfall paths, and why Azalea will need supplies before a long crisis.',
        area_type: area_type
      )
      CompanionProgress.record_scene(
        state,
        'bill',
        'union_cave_radio_scan',
        location: location,
        summary: 'Bill tracks Rocket radio parts through Union Cave and confirms the signal runs toward Azalea and Slowpoke Well.',
        area_type: area_type
      )

      record_rival_story_clue(
        state,
        'silver',
        location,
        'Silver ambushed Antman near the Union Cave exit, furious that Red and Brock keep turning hard roads into lessons.',
        area_type,
        region: 'johto'
      )
      state.dig('rival_progress', 'silver', 'latest_activity')['battle_hook'] = {
        'battle_id' => SILVER_UNION_CAVE_AMBUSH_EVENT_ID,
        'battle_type' => 'johto_rival_silver',
        'location' => location.to_s,
        'level_cap' => 18,
        'theme' => 'speed_and_spite'
      }

      FactionWar.record_activity(
        state,
        'team_rocket',
        'johto',
        'Slowpoke Well Supply Line',
        'slowpoke_well_supply_line',
        threat_delta: 2,
        area_type: area_type
      )
      FactionWar.record_activity(
        state,
        'team_gold_dust',
        'johto',
        location,
        'union_cave_relic_auction',
        threat_delta: 1,
        area_type: area_type
      )
      FactionWar.record_activity(
        state,
        'team_moonlight',
        'johto',
        location,
        'union_cave_dream_echo',
        threat_delta: 1,
        area_type: area_type
      )
      FactionWar.record_activity(
        state,
        'nexus_order',
        'johto',
        location,
        'union_cave_fault_line_hidden',
        threat_delta: 0,
        area_type: area_type
      )
      FactionWar.record_conflict(
        state,
        'team_rocket',
        'team_gold_dust',
        location,
        'Rocket radio crates and Gold Dust relic buyers collide under Union Cave while Moonlight static makes both sides paranoid.',
        intensity: 2,
        area_type: area_type
      )

      story['current_act'] = 'act_5_azalea_slowpoke_well_crisis'
      event = union_cave_road_event_result(location)
      story['event_history'] << event
      story['latest_event'] = event

      WorldLink.queue_message(
        state,
        'story_alert',
        'Union Cave opens the road to Azalea: Red keeps Antman steady, Silver attacks near the exit, and Bill traces Rocket supplies into the Slowpoke Well crisis.',
        source: 'johto_story',
        area_type: area_type
      )

      event
    end

    def union_cave_road_cleared?(state)
      ensure_johto_story(state)['event_history'].any? { |event| event['event_id'] == UNION_CAVE_ROAD_MAIN_EVENT_ID }
    end

    def union_cave_road_event_result(location)
      {
        'status' => 'cleared',
        'event_id' => UNION_CAVE_ROAD_MAIN_EVENT_ID,
        'location' => location.to_s,
        'region' => 'johto',
        'current_act' => 'act_5_azalea_slowpoke_well_crisis',
        'route_chain' => ['Violet City', 'Route 32', 'Union Cave', 'Route 33', 'Azalea Town'],
        'companions' => %w[red brock bill],
        'rivals' => %w[silver],
        'factions' => %w[team_rocket team_gold_dust team_moonlight nexus_order],
        'linked_events' => [
          RED_UNION_CAVE_TRAVEL_EVENT_ID,
          BROCK_UNION_CAVE_SURVIVAL_EVENT_ID,
          BILL_UNION_CAVE_RADIO_SCAN_EVENT_ID,
          SILVER_UNION_CAVE_AMBUSH_EVENT_ID,
          ROCKET_SLOWPOKE_WELL_SUPPLY_EVENT_ID,
          GOLD_DUST_UNION_CAVE_RELIC_EVENT_ID,
          MOONLIGHT_UNION_CAVE_ECHO_EVENT_ID,
          NEXUS_ORDER_UNION_CAVE_FAULT_EVENT_ID,
          AZALEA_TOWN_UNLOCKED_EVENT_ID,
          SLOWPOKE_WELL_CRISIS_UNLOCKED_EVENT_ID,
          KURT_APRICORN_LEAD_EVENT_ID
        ],
        'battle_hooks' => [
          {
            'battle_id' => SILVER_UNION_CAVE_AMBUSH_EVENT_ID,
            'battle_type' => 'johto_rival_silver',
            'location' => location.to_s,
            'level_cap' => 18,
            'theme' => 'speed_and_spite'
          }
        ],
        'hidden_meta_signal' => 'nexus_order_union_cave_fault_line_unrevealed',
        'unlocks' => %w[azalea_town slowpoke_well_crisis kurt_apricorn_lead route_33],
        'next_hook' => 'slowpoke_well_crisis'
      }
    end

    def complete_slowpoke_well_crisis(state, location: 'Slowpoke Well', result: 'rocket_forced_out', area_type: 'villain_hideout')
      story = ensure_johto_story(state)
      return { 'status' => 'blocked_missing_johto_region_unlock', 'event_id' => SLOWPOKE_WELL_CRISIS_EVENT_ID } unless johto_unlocked?(state)
      return { 'status' => 'blocked_missing_union_cave_road', 'event_id' => SLOWPOKE_WELL_CRISIS_EVENT_ID } unless union_cave_road_cleared?(state)
      return { 'status' => 'already_cleared', 'event_id' => SLOWPOKE_WELL_CRISIS_EVENT_ID } if slowpoke_well_crisis_cleared?(state)

      add_story_flag(state, 'FLAG_NEXUS_SLOWPOKE_WELL_CRISIS')
      add_story_flag(state, 'FLAG_NEXUS_KURT_SLOWPOKE_WELL_RESCUE')
      add_story_flag(state, 'FLAG_NEXUS_RED_SLOWPOKE_WELL_RAID')
      add_story_flag(state, 'FLAG_NEXUS_BROCK_SLOWPOKE_CARE')
      add_story_flag(state, 'FLAG_NEXUS_BILL_ROCKET_RADIO_CORE')
      add_story_flag(state, 'FLAG_NEXUS_ROCKET_SLOWPOKE_TAIL_RING')
      add_story_flag(state, 'FLAG_NEXUS_GOLD_DUST_APRICORN_BLACK_MARKET')
      add_story_flag(state, 'FLAG_NEXUS_MOONLIGHT_SLOWPOKE_WELL_ECHO')
      add_story_flag(state, 'FLAG_NEXUS_NEXUS_ORDER_SLOWPOKE_WELL_PULSE')
      add_story_flag(state, 'FLAG_NEXUS_AZALEA_SERVICES_RESTORED')
      add_story_flag(state, 'FLAG_NEXUS_BUGSY_HIVE_BADGE_PREP_UNLOCKED')

      [
        SLOWPOKE_WELL_CRISIS_EVENT_ID,
        KURT_SLOWPOKE_WELL_RESCUE_EVENT_ID,
        RED_SLOWPOKE_WELL_RAID_EVENT_ID,
        BROCK_SLOWPOKE_CARE_EVENT_ID,
        BILL_ROCKET_RADIO_CORE_EVENT_ID,
        ROCKET_SLOWPOKE_TAIL_RING_EVENT_ID,
        GOLD_DUST_APRICORN_MARKET_EVENT_ID,
        MOONLIGHT_SLOWPOKE_WELL_ECHO_EVENT_ID,
        NEXUS_ORDER_SLOWPOKE_WELL_PULSE_EVENT_ID,
        AZALEA_SERVICES_RESTORED_EVENT_ID,
        BUGSY_HIVE_BADGE_PREP_EVENT_ID
      ].each { |event_id| mark_cleared_event(story, event_id) }

      CompanionProgress.record_scene(
        state,
        'red',
        'slowpoke_well_raid',
        location: location,
        summary: 'Red enters Slowpoke Well with Antman as backup, then lets Antman lead the raid against Rocket.',
        area_type: area_type
      )
      CompanionProgress.record_scene(
        state,
        'brock',
        'slowpoke_care',
        location: location,
        summary: 'Brock stabilizes injured Slowpoke and turns the rescue into a lesson about caring for Pokemon after the battle ends.',
        area_type: area_type
      )
      CompanionProgress.record_scene(
        state,
        'bill',
        'rocket_radio_core_decode',
        location: location,
        summary: 'Bill cracks Rocket radio core traffic inside Slowpoke Well and confirms the Johto operation is not isolated.',
        area_type: area_type
      )

      record_rival_story_clue(
        state,
        'silver',
        'Azalea Town',
        'Silver refused to thank anyone after Slowpoke Well and turned toward Bugsy, chasing strength before understanding why Rocket ran.',
        area_type,
        region: 'johto'
      )

      FactionWar.record_activity(
        state,
        'team_rocket',
        'johto',
        location,
        'slowpoke_tail_ring',
        threat_delta: 3,
        area_type: area_type
      )
      FactionWar.record_activity(
        state,
        'team_gold_dust',
        'johto',
        'Azalea Apricorn Market',
        'apricorn_black_market',
        threat_delta: 1,
        area_type: area_type
      )
      FactionWar.record_activity(
        state,
        'team_moonlight',
        'johto',
        location,
        'slowpoke_well_dream_echo',
        threat_delta: 1,
        area_type: area_type
      )
      FactionWar.record_activity(
        state,
        'nexus_order',
        'johto',
        location,
        'slowpoke_well_pulse_hidden',
        threat_delta: 0,
        area_type: area_type
      )
      FactionWar.record_conflict(
        state,
        'team_rocket',
        'team_gold_dust',
        location,
        'Rocket tail profits and Gold Dust apricorn buyers collide after Kurt exposes both markets.',
        intensity: 2,
        area_type: area_type
      )

      story['current_act'] = 'act_6_bugsy_hive_badge'
      event = slowpoke_well_crisis_event_result(location, result)
      story['event_history'] << event
      story['latest_event'] = event

      WorldLink.queue_message(
        state,
        'story_alert',
        'Slowpoke Well is saved: Kurt exposes the Rocket tail ring, Red and Brock keep Antman focused, Bill finds a radio core, and Bugsy opens the Hive Badge prep.',
        source: 'johto_story',
        area_type: area_type
      )

      event
    end

    def slowpoke_well_crisis_cleared?(state)
      ensure_johto_story(state)['event_history'].any? { |event| event['event_id'] == SLOWPOKE_WELL_CRISIS_EVENT_ID }
    end

    def slowpoke_well_crisis_event_result(location, result)
      {
        'status' => 'cleared',
        'event_id' => SLOWPOKE_WELL_CRISIS_EVENT_ID,
        'location' => location.to_s,
        'region' => 'johto',
        'current_act' => 'act_6_bugsy_hive_badge',
        'result' => result.to_s,
        'local_allies' => %w[kurt],
        'companions' => %w[red brock bill],
        'rivals' => %w[silver],
        'factions' => %w[team_rocket team_gold_dust team_moonlight nexus_order],
        'linked_events' => [
          KURT_SLOWPOKE_WELL_RESCUE_EVENT_ID,
          RED_SLOWPOKE_WELL_RAID_EVENT_ID,
          BROCK_SLOWPOKE_CARE_EVENT_ID,
          BILL_ROCKET_RADIO_CORE_EVENT_ID,
          ROCKET_SLOWPOKE_TAIL_RING_EVENT_ID,
          GOLD_DUST_APRICORN_MARKET_EVENT_ID,
          MOONLIGHT_SLOWPOKE_WELL_ECHO_EVENT_ID,
          NEXUS_ORDER_SLOWPOKE_WELL_PULSE_EVENT_ID,
          AZALEA_SERVICES_RESTORED_EVENT_ID,
          BUGSY_HIVE_BADGE_PREP_EVENT_ID
        ],
        'villain_result' => 'rocket_retreats_but_radio_core_survives',
        'hidden_meta_signal' => 'nexus_order_slowpoke_well_pulse_unrevealed',
        'unlocks' => %w[bugsy_hive_badge_prep kurt_apricorn_shop azalea_services_restored slowpoke_well_rematch_seed],
        'next_hook' => 'bugsy_hive_badge_prep'
      }
    end

    def complete_bugsy_hive_badge_prep(state, location: 'Azalea Gym Grove', area_type: 'town')
      story = ensure_johto_story(state)
      return { 'status' => 'blocked_missing_johto_region_unlock', 'event_id' => BUGSY_HIVE_BADGE_PREP_MAIN_EVENT_ID } unless johto_unlocked?(state)
      return { 'status' => 'blocked_missing_slowpoke_well_crisis', 'event_id' => BUGSY_HIVE_BADGE_PREP_MAIN_EVENT_ID } unless slowpoke_well_crisis_cleared?(state)
      return { 'status' => 'already_cleared', 'event_id' => BUGSY_HIVE_BADGE_PREP_MAIN_EVENT_ID } if bugsy_hive_badge_prep_cleared?(state)

      add_story_flag(state, 'FLAG_NEXUS_BUGSY_HIVE_BADGE_PREP')
      add_story_flag(state, 'FLAG_NEXUS_RED_BUGSY_PREP')
      add_story_flag(state, 'FLAG_NEXUS_BROCK_BUG_COUNTER_ADVICE')
      add_story_flag(state, 'FLAG_NEXUS_BILL_DREAM_SPORE_SCAN')
      add_story_flag(state, 'FLAG_NEXUS_BUGSY_GYM_SCOUTING')
      add_story_flag(state, 'FLAG_NEXUS_MOONLIGHT_BUGSY_DREAM_SPORE')
      add_story_flag(state, 'FLAG_NEXUS_ROCKET_AZALEA_RETREAT_RADIO_BURST')
      add_story_flag(state, 'FLAG_NEXUS_GOLD_DUST_HIVE_BADGE_CHARM_MARKET')
      add_story_flag(state, 'FLAG_NEXUS_NEXUS_ORDER_HIVE_PATTERN_SIGNAL')
      add_story_flag(state, 'FLAG_NEXUS_BUGSY_HIVE_BADGE_BATTLE_UNLOCKED')

      [
        BUGSY_HIVE_BADGE_PREP_MAIN_EVENT_ID,
        RED_BUGSY_PREP_EVENT_ID,
        BROCK_BUG_COUNTER_ADVICE_EVENT_ID,
        BILL_DREAM_SPORE_SCAN_EVENT_ID,
        BUGSY_GYM_SCOUTING_EVENT_ID,
        MOONLIGHT_BUGSY_DREAM_SPORE_EVENT_ID,
        ROCKET_AZALEA_RETREAT_BURST_EVENT_ID,
        GOLD_DUST_HIVE_CHARM_MARKET_EVENT_ID,
        NEXUS_ORDER_HIVE_PATTERN_EVENT_ID,
        BUGSY_HIVE_BADGE_BATTLE_UNLOCKED_EVENT_ID
      ].each { |event_id| mark_cleared_event(story, event_id) }

      CompanionProgress.record_scene(
        state,
        'red',
        'bugsy_prep_focus',
        location: location,
        summary: 'Red helps Antman reset after Slowpoke Well, then steps back so Bugsy remains a true solo gym challenge.',
        area_type: area_type
      )
      CompanionProgress.record_scene(
        state,
        'brock',
        'bug_counter_advice',
        location: location,
        summary: 'Brock turns Bugsy prep into practical bug-type counterplay: status control, flying pressure, fire timing, and not underestimating Scyther.',
        area_type: area_type
      )
      CompanionProgress.record_scene(
        state,
        'bill',
        'azalea_dream_spore_scan',
        location: location,
        summary: 'Bill scans dream-spore residue around Azalea Gym and proves Moonlight is trying to make the classic bug gym feel wrong.',
        area_type: area_type
      )

      record_rival_story_clue(
        state,
        'silver',
        location,
        'Silver paced outside Azalea Gym, impatient to test Bugsy before Antman and irritated that everyone keeps studying the dream-spore anomaly.',
        area_type,
        region: 'johto'
      )

      FactionWar.record_activity(
        state,
        'team_moonlight',
        'johto',
        location,
        'bugsy_dream_spore_anomaly',
        threat_delta: 2,
        area_type: area_type
      )
      FactionWar.record_activity(
        state,
        'team_rocket',
        'johto',
        'Azalea Back Road',
        'azalea_retreat_radio_burst',
        threat_delta: 1,
        area_type: area_type
      )
      FactionWar.record_activity(
        state,
        'team_gold_dust',
        'johto',
        location,
        'hive_badge_charm_market',
        threat_delta: 1,
        area_type: area_type
      )
      FactionWar.record_activity(
        state,
        'nexus_order',
        'johto',
        location,
        'hive_pattern_signal_hidden',
        threat_delta: 0,
        area_type: area_type
      )
      FactionWar.record_conflict(
        state,
        'team_rocket',
        'team_moonlight',
        location,
        'Rocket retreat traffic scrambles in Moonlight dream-spore interference around Bugsy\'s grove.',
        intensity: 1,
        area_type: area_type
      )

      story['current_act'] = 'act_6_bugsy_hive_badge'
      event = bugsy_hive_badge_prep_event_result(location)
      story['event_history'] << event
      story['latest_event'] = event

      WorldLink.queue_message(
        state,
        'story_alert',
        'Bugsy opens the Hive Badge prep: Red steadies Antman, Brock reviews bug counters, and Bill confirms Moonlight dream-spore residue around Azalea Gym.',
        source: 'johto_story',
        area_type: area_type
      )

      event
    end

    def bugsy_hive_badge_prep_cleared?(state)
      ensure_johto_story(state)['event_history'].any? { |event| event['event_id'] == BUGSY_HIVE_BADGE_PREP_MAIN_EVENT_ID }
    end

    def bugsy_hive_badge_prep_event_result(location)
      {
        'status' => 'cleared',
        'event_id' => BUGSY_HIVE_BADGE_PREP_MAIN_EVENT_ID,
        'location' => location.to_s,
        'region' => 'johto',
        'current_act' => 'act_6_bugsy_hive_badge',
        'gym_leader' => 'Bugsy',
        'badge' => 'Hive Badge',
        'level_cap' => 22,
        'companions' => %w[red brock bill],
        'rivals' => %w[silver],
        'factions' => %w[team_rocket team_gold_dust team_moonlight nexus_order],
        'linked_events' => [
          RED_BUGSY_PREP_EVENT_ID,
          BROCK_BUG_COUNTER_ADVICE_EVENT_ID,
          BILL_DREAM_SPORE_SCAN_EVENT_ID,
          BUGSY_GYM_SCOUTING_EVENT_ID,
          MOONLIGHT_BUGSY_DREAM_SPORE_EVENT_ID,
          ROCKET_AZALEA_RETREAT_BURST_EVENT_ID,
          GOLD_DUST_HIVE_CHARM_MARKET_EVENT_ID,
          NEXUS_ORDER_HIVE_PATTERN_EVENT_ID,
          BUGSY_HIVE_BADGE_BATTLE_UNLOCKED_EVENT_ID
        ],
        'battle_hook' => {
          'battle_id' => 'bugsy_hive_badge_battle',
          'battle_type' => 'johto_gym_leader_bugsy',
          'location' => 'Azalea Gym',
          'level_cap' => 22,
          'companion_rule' => 'no_companion_assist_in_gym_battle',
          'standard_team' => [
            { 'species' => 'Spinarak', 'level' => 18, 'role' => 'web_status_intro' },
            { 'species' => 'Metapod', 'level' => 18, 'role' => 'bulk_setup' },
            { 'species' => 'Heracross', 'level' => 20, 'role' => 'azalea_power_hint' },
            { 'species' => 'Scyther', 'level' => 22, 'role' => 'ace' }
          ]
        },
        'anomaly' => 'moonlight_dream_spore_residue',
        'hidden_meta_signal' => 'nexus_order_hive_pattern_signal_unrevealed',
        'unlocks' => %w[bugsy_hive_badge_battle azalea_gym_services bugsy_rematch_seed],
        'next_hook' => 'bugsy_hive_badge_battle'
      }
    end

    def complete_bugsy_hive_badge_battle(state, location: 'Azalea Gym', result: 'won', area_type: 'gym')
      story = ensure_johto_story(state)
      return { 'status' => 'blocked_missing_johto_region_unlock', 'event_id' => BUGSY_HIVE_BADGE_BATTLE_EVENT_ID } unless johto_unlocked?(state)
      return { 'status' => 'blocked_missing_bugsy_hive_badge_prep', 'event_id' => BUGSY_HIVE_BADGE_BATTLE_EVENT_ID } unless bugsy_hive_badge_prep_cleared?(state)
      return { 'status' => 'already_cleared', 'event_id' => BUGSY_HIVE_BADGE_BATTLE_EVENT_ID } if bugsy_hive_badge_battle_cleared?(state)

      add_story_flag(state, 'hive_badge_obtained')
      add_story_flag(state, 'FLAG_NEXUS_HIVE_BADGE')
      add_story_flag(state, 'FLAG_NEXUS_BUGSY_BATTLE_STARTED')
      add_story_flag(state, 'FLAG_NEXUS_BUGSY_BATTLE_FINISHED')
      add_story_flag(state, 'FLAG_NEXUS_RED_POST_BUGSY')
      add_story_flag(state, 'FLAG_NEXUS_BROCK_POST_BUGSY')
      add_story_flag(state, 'FLAG_NEXUS_BILL_HIVE_SIGNAL_DECODED')
      add_story_flag(state, 'FLAG_NEXUS_ILEX_FOREST_PATH_UNLOCKED')

      [
        BUGSY_HIVE_BADGE_BATTLE_EVENT_ID,
        HIVE_BADGE_OBTAINED_EVENT_ID,
        RED_POST_BUGSY_EVENT_ID,
        BROCK_POST_BUGSY_EVENT_ID,
        BILL_HIVE_SIGNAL_DECODED_EVENT_ID,
        SILVER_ILEX_FOREST_RACE_EVENT_ID,
        MOONLIGHT_DREAM_SPORE_COLLAPSE_EVENT_ID,
        ROCKET_ILEX_RETREAT_EVENT_ID,
        GOLD_DUST_ILEX_RELIC_BID_EVENT_ID,
        NEXUS_ORDER_HIVE_BADGE_PATTERN_EVENT_ID,
        ILEX_FOREST_PATH_UNLOCKED_EVENT_ID
      ].each { |event_id| mark_cleared_event(story, event_id) }

      CompanionProgress.record_scene(
        state,
        'red',
        'post_bugsy_respect',
        location: location,
        summary: 'Red congratulates Antman on the Hive Badge and notes that beating Bugsy cleanly matters more than rushing through Johto.',
        area_type: area_type
      )
      CompanionProgress.record_scene(
        state,
        'brock',
        'post_bugsy_recovery_review',
        location: location,
        summary: 'Brock reviews the Bugsy battle recovery plan and checks that the dream-spore residue did not cling to the party.',
        area_type: area_type
      )
      CompanionProgress.record_scene(
        state,
        'bill',
        'hive_signal_decode',
        location: location,
        summary: 'Bill decodes the Hive Badge pattern and finds the next clean signal running through Ilex Forest toward Goldenrod.',
        area_type: area_type
      )

      record_rival_story_clue(
        state,
        'silver',
        location,
        'Silver saw Antman earn the Hive Badge and cut into Ilex Forest first, trying to turn the next road into a race.',
        area_type,
        region: 'johto'
      )

      FactionWar.record_activity(
        state,
        'team_moonlight',
        'johto',
        location,
        'dream_spore_residue_collapse',
        threat_delta: 1,
        area_type: area_type
      )
      FactionWar.record_activity(
        state,
        'team_rocket',
        'johto',
        'Ilex Forest Cut-Through',
        'ilex_cut_through_retreat',
        threat_delta: 1,
        area_type: area_type
      )
      FactionWar.record_activity(
        state,
        'team_gold_dust',
        'johto',
        'Ilex Charcoal Kiln',
        'ilex_charcoal_relic_bid',
        threat_delta: 1,
        area_type: area_type
      )
      FactionWar.record_activity(
        state,
        'nexus_order',
        'johto',
        location,
        'hive_badge_pattern_hidden',
        threat_delta: 0,
        area_type: area_type
      )

      story['current_act'] = 'act_7_ilex_forest_and_goldenrod_road'
      event = bugsy_hive_badge_battle_event_result(location, result)
      story['event_history'] << event
      story['latest_event'] = event

      WorldLink.queue_message(
        state,
        'story_alert',
        'Antman earned the Hive Badge. Red stays beside him, Bill points the next signal into Ilex Forest, and Silver is already turning the forest road into a race.',
        source: 'johto_story',
        area_type: area_type
      )

      event
    end

    def bugsy_hive_badge_battle_cleared?(state)
      ensure_johto_story(state)['event_history'].any? { |event| event['event_id'] == BUGSY_HIVE_BADGE_BATTLE_EVENT_ID }
    end

    def bugsy_hive_badge_battle_event_result(location, result)
      {
        'status' => 'cleared',
        'event_id' => BUGSY_HIVE_BADGE_BATTLE_EVENT_ID,
        'battle_id' => BUGSY_HIVE_BADGE_BATTLE_EVENT_ID,
        'location' => location.to_s,
        'region' => 'johto',
        'current_act' => 'act_7_ilex_forest_and_goldenrod_road',
        'result' => result.to_s,
        'gym_leader' => 'Bugsy',
        'badge' => 'Hive Badge',
        'level_cap' => 22,
        'companion_rule' => 'no_companion_assist_in_gym_battle',
        'companions' => %w[red brock bill],
        'rivals' => %w[silver],
        'factions' => %w[team_rocket team_gold_dust team_moonlight nexus_order],
        'linked_events' => [
          HIVE_BADGE_OBTAINED_EVENT_ID,
          RED_POST_BUGSY_EVENT_ID,
          BROCK_POST_BUGSY_EVENT_ID,
          BILL_HIVE_SIGNAL_DECODED_EVENT_ID,
          SILVER_ILEX_FOREST_RACE_EVENT_ID,
          MOONLIGHT_DREAM_SPORE_COLLAPSE_EVENT_ID,
          ROCKET_ILEX_RETREAT_EVENT_ID,
          GOLD_DUST_ILEX_RELIC_BID_EVENT_ID,
          NEXUS_ORDER_HIVE_BADGE_PATTERN_EVENT_ID,
          ILEX_FOREST_PATH_UNLOCKED_EVENT_ID
        ],
        'hidden_meta_signal' => 'nexus_order_hive_badge_pattern_unrevealed',
        'unlocks' => %w[ilex_forest_path bugsy_rematch_board_tier_1 cut_field_tool_lead],
        'next_hook' => 'ilex_forest_path'
      }
    end

    def complete_ilex_forest_path(state, location: 'Ilex Forest', area_type: 'forest')
      story = ensure_johto_story(state)
      return { 'status' => 'blocked_missing_johto_region_unlock', 'event_id' => ILEX_FOREST_PATH_EVENT_ID } unless johto_unlocked?(state)
      return { 'status' => 'blocked_missing_bugsy_hive_badge_battle', 'event_id' => ILEX_FOREST_PATH_EVENT_ID } unless bugsy_hive_badge_battle_cleared?(state)
      return { 'status' => 'already_cleared', 'event_id' => ILEX_FOREST_PATH_EVENT_ID } if ilex_forest_path_cleared?(state)

      add_story_flag(state, 'FLAG_NEXUS_ILEX_FOREST_PATH')
      add_story_flag(state, 'FLAG_NEXUS_RED_ILEX_FOREST_GUIDE')
      add_story_flag(state, 'FLAG_NEXUS_BROCK_ILEX_FOREST_FIELD_CARE')
      add_story_flag(state, 'FLAG_NEXUS_BILL_ILEX_RELAY_TRACE')
      add_story_flag(state, 'FLAG_NEXUS_FARFETCHD_FIELD_TOOL_LEAD')
      add_story_flag(state, 'FLAG_NEXUS_TRAIL_CUTTER_ILEX_LEAD')
      add_story_flag(state, 'FLAG_NEXUS_SILVER_ILEX_SHORTCUT_PRESSURE')
      add_story_flag(state, 'FLAG_NEXUS_ROCKET_ILEX_RETREAT_CACHE')
      add_story_flag(state, 'FLAG_NEXUS_GOLD_DUST_CHARCOAL_RELIC_BID')
      add_story_flag(state, 'FLAG_NEXUS_MOONLIGHT_ILEX_RESIDUE')
      add_story_flag(state, 'FLAG_NEXUS_NEXUS_ORDER_ILEX_SHRINE_PATTERN')
      add_story_flag(state, 'FLAG_NEXUS_GOLDENROD_ROAD_UNLOCKED')

      [
        ILEX_FOREST_PATH_EVENT_ID,
        RED_ILEX_FOREST_GUIDE_EVENT_ID,
        BROCK_ILEX_FOREST_FIELD_CARE_EVENT_ID,
        BILL_ILEX_RELAY_TRACE_EVENT_ID,
        FARFETCHD_FIELD_TOOL_LEAD_EVENT_ID,
        TRAIL_CUTTER_ILEX_LEAD_EVENT_ID,
        SILVER_ILEX_SHORTCUT_PRESSURE_EVENT_ID,
        ROCKET_ILEX_RETREAT_CACHE_EVENT_ID,
        GOLD_DUST_CHARCOAL_RELIC_EVENT_ID,
        MOONLIGHT_ILEX_RESIDUE_EVENT_ID,
        NEXUS_ORDER_ILEX_SHRINE_PATTERN_EVENT_ID,
        GOLDENROD_ROAD_UNLOCKED_EVENT_ID
      ].each { |event_id| mark_cleared_event(story, event_id) }

      CompanionProgress.record_scene(
        state,
        'red',
        'ilex_forest_guide',
        location: location,
        summary: 'Red walks the Ilex Forest trail with Antman, teaching him to slow down, listen for Farfetchd wingbeats, and read the old shrine path before chasing Silver.',
        area_type: area_type
      )
      CompanionProgress.record_scene(
        state,
        'brock',
        'ilex_field_care',
        location: location,
        summary: 'Brock checks the party after the forest maze, explains why charcoal kilns matter to Johto families, and points out where Rocket crates scraped the moss.',
        area_type: area_type
      )
      CompanionProgress.record_scene(
        state,
        'bill',
        'ilex_relay_trace',
        location: location,
        summary: 'Bill traces the Hive Badge signal through the Ilex shrine roots and warns that the clean relay line continues toward Route 34 and Goldenrod.',
        area_type: area_type
      )

      record_rival_story_clue(
        state,
        'silver',
        location,
        'Silver forced a shortcut through Ilex Forest and was last seen sprinting toward Goldenrod, angry that Antman is still solving the forest instead of rushing it.',
        area_type,
        region: 'johto'
      )

      FactionWar.record_activity(
        state,
        'team_rocket',
        'johto',
        'Ilex Forest Cut-Through',
        'ilex_retreat_cache',
        threat_delta: 1,
        area_type: area_type
      )
      FactionWar.record_activity(
        state,
        'team_gold_dust',
        'johto',
        'Ilex Charcoal Kiln',
        'charcoal_relic_bid',
        threat_delta: 1,
        area_type: area_type
      )
      FactionWar.record_activity(
        state,
        'team_moonlight',
        'johto',
        location,
        'ilex_dream_spore_residue',
        threat_delta: 1,
        area_type: area_type
      )
      FactionWar.record_activity(
        state,
        'nexus_order',
        'johto',
        'Ilex Forest Shrine',
        'ilex_shrine_pattern_hidden',
        threat_delta: 0,
        area_type: area_type
      )
      FactionWar.record_conflict(
        state,
        'team_rocket',
        'team_gold_dust',
        'Ilex Forest',
        'Rocket retreat crates and Gold Dust charcoal relic bids collide under the forest canopy.',
        intensity: 2,
        area_type: area_type
      )

      story['current_act'] = 'act_8_goldenrod_road_and_radio_shadow'
      event = ilex_forest_path_event_result(location)
      story['event_history'] << event
      story['latest_event'] = event

      WorldLink.queue_message(
        state,
        'story_alert',
        'Ilex Forest opens the long road from Azalea to Goldenrod: Red guides Antman through the shrine path, a Farfetchd chase points to the Trail Cutter lead, and Silver is already pressing Route 34.',
        source: 'johto_story',
        area_type: area_type
      )

      event
    end

    def ilex_forest_path_cleared?(state)
      ensure_johto_story(state)['event_history'].any? { |event| event['event_id'] == ILEX_FOREST_PATH_EVENT_ID }
    end

    def ilex_forest_path_event_result(location)
      {
        'status' => 'cleared',
        'event_id' => ILEX_FOREST_PATH_EVENT_ID,
        'location' => location.to_s,
        'region' => 'johto',
        'current_act' => 'act_8_goldenrod_road_and_radio_shadow',
        'route_chain' => ['Azalea Town', 'Ilex Forest', 'Route 34', 'Goldenrod City'],
        'companions' => %w[red brock bill],
        'rivals' => %w[silver],
        'factions' => %w[team_rocket team_gold_dust team_moonlight nexus_order],
        'linked_events' => [
          RED_ILEX_FOREST_GUIDE_EVENT_ID,
          BROCK_ILEX_FOREST_FIELD_CARE_EVENT_ID,
          BILL_ILEX_RELAY_TRACE_EVENT_ID,
          FARFETCHD_FIELD_TOOL_LEAD_EVENT_ID,
          TRAIL_CUTTER_ILEX_LEAD_EVENT_ID,
          SILVER_ILEX_SHORTCUT_PRESSURE_EVENT_ID,
          ROCKET_ILEX_RETREAT_CACHE_EVENT_ID,
          GOLD_DUST_CHARCOAL_RELIC_EVENT_ID,
          MOONLIGHT_ILEX_RESIDUE_EVENT_ID,
          NEXUS_ORDER_ILEX_SHRINE_PATTERN_EVENT_ID,
          GOLDENROD_ROAD_UNLOCKED_EVENT_ID
        ],
        'field_tool_lead' => 'trail_cutter_farfetchd_route',
        'local_event' => 'farfetchd_chase',
        'hidden_meta_signal' => 'nexus_order_ilex_shrine_pattern_unrevealed',
        'unlocks' => %w[goldenrod_road route_34_daycare_lead trail_cutter_farfetchd_lead ilex_shrine_rumor],
        'next_hook' => 'goldenrod_road'
      }
    end

    def complete_goldenrod_road(state, location: 'Route 34', area_type: 'route')
      story = ensure_johto_story(state)
      return { 'status' => 'blocked_missing_johto_region_unlock', 'event_id' => GOLDENROD_ROAD_EVENT_ID } unless johto_unlocked?(state)
      return { 'status' => 'blocked_missing_ilex_forest_path', 'event_id' => GOLDENROD_ROAD_EVENT_ID } unless ilex_forest_path_cleared?(state)
      return { 'status' => 'already_cleared', 'event_id' => GOLDENROD_ROAD_EVENT_ID } if goldenrod_road_cleared?(state)

      add_story_flag(state, 'FLAG_NEXUS_GOLDENROD_ROAD')
      add_story_flag(state, 'FLAG_NEXUS_ROUTE34_DAYCARE_UNLOCKED')
      add_story_flag(state, 'FLAG_NEXUS_GOLDENROD_CITY_ARRIVAL')
      add_story_flag(state, 'FLAG_NEXUS_GOLDENROD_RADIO_TOWER_TEASE')
      add_story_flag(state, 'FLAG_NEXUS_WHITNEY_GYM_TEASE')
      add_story_flag(state, 'FLAG_NEXUS_WHITNEY_PLAIN_BADGE_PREP_UNLOCKED')
      add_story_flag(state, 'FLAG_NEXUS_RED_GOLDENROD_ROAD_TRAINING')
      add_story_flag(state, 'FLAG_NEXUS_BROCK_ROUTE34_DAYCARE_ADVICE')
      add_story_flag(state, 'FLAG_NEXUS_BILL_GOLDENROD_SIGNAL_SCAN')
      add_story_flag(state, 'FLAG_NEXUS_ROCKET_GOLDENROD_RADIO_SHADOW')
      add_story_flag(state, 'FLAG_NEXUS_GOLD_DUST_GOLDENROD_COIN_MARKET')
      add_story_flag(state, 'FLAG_NEXUS_TEAM_GAS_GOLDENROD_UNDERGROUND')
      add_story_flag(state, 'FLAG_NEXUS_MOONLIGHT_GOLDENROD_RADIO_JINGLE')
      add_story_flag(state, 'FLAG_NEXUS_NEXUS_ORDER_GOLDENROD_FREQUENCY')

      [
        GOLDENROD_ROAD_EVENT_ID,
        ROUTE34_DAYCARE_OPENED_EVENT_ID,
        GOLDENROD_CITY_ARRIVAL_EVENT_ID,
        GOLDENROD_RADIO_TOWER_TEASE_EVENT_ID,
        WHITNEY_GYM_TEASE_EVENT_ID,
        RED_GOLDENROD_ROAD_TRAINING_EVENT_ID,
        BROCK_ROUTE34_DAYCARE_ADVICE_EVENT_ID,
        BILL_GOLDENROD_SIGNAL_SCAN_EVENT_ID,
        BLUE_GOLDENROD_STANDINGS_EVENT_ID,
        AVA_ROUTE34_DAYCARE_RESEARCH_EVENT_ID,
        SILVER_GOLDENROD_PRESSURE_EVENT_ID,
        ROCKET_GOLDENROD_RADIO_SHADOW_EVENT_ID,
        GOLD_DUST_GOLDENROD_COIN_MARKET_EVENT_ID,
        TEAM_GAS_GOLDENROD_UNDERGROUND_EVENT_ID,
        MOONLIGHT_GOLDENROD_RADIO_JINGLE_EVENT_ID,
        NEXUS_ORDER_GOLDENROD_FREQUENCY_EVENT_ID,
        WHITNEY_PLAIN_BADGE_PREP_UNLOCKED_EVENT_ID
      ].each { |event_id| mark_cleared_event(story, event_id) }

      EncounterWorld.unlock_daycare(state, location: 'Route 34 Daycare')
      CenterMartServices.unlock_terminal_feature(state, 'daycare_remote_check')
      CenterMartServices.unlock_mart_tier(state, 'goldenrod_specialty')

      CompanionProgress.record_scene(
        state,
        'red',
        'goldenrod_road_training',
        location: location,
        summary: 'Red slows Antman down on Route 34, turning the busy trainer lane into a warm training walk before the pressure of Goldenrod City.',
        area_type: area_type
      )
      CompanionProgress.record_scene(
        state,
        'brock',
        'route34_daycare_breeding_advice',
        location: 'Route 34 Daycare',
        summary: 'Brock explains breeding, eggs, and responsible daycare use while making sure Antman treats the Route 34 Daycare as more than a shortcut to power.',
        area_type: area_type
      )
      CompanionProgress.record_scene(
        state,
        'bill',
        'goldenrod_signal_scan',
        location: 'Goldenrod City',
        summary: 'Bill scans Goldenrod Radio Tower and finds the Ilex shrine relay turning into a stronger citywide broadcast shadow.',
        area_type: area_type
      )

      record_rival_story_clue(
        state,
        'silver',
        'Goldenrod Gym Plaza',
        'Silver reached Goldenrod ahead of Antman and is pressuring Whitney for a fast Plain Badge challenge.',
        area_type,
        region: 'johto'
      )
      record_rival_story_clue(
        state,
        'blue',
        'Goldenrod Station',
        'Blue checked the Goldenrod standings board and warned that Johto trainers punish sloppy teams harder than Kanto did.',
        area_type,
        region: 'johto'
      )
      record_rival_story_clue(
        state,
        'ava',
        'Route 34 Daycare',
        'Ava uploaded daycare research notes from Route 34, flagging egg moves and rare lineage rumors for WorldLink.',
        area_type,
        region: 'johto'
      )

      FactionWar.record_activity(
        state,
        'team_rocket',
        'johto',
        'Goldenrod Radio Tower',
        'goldenrod_radio_tower_shadow',
        threat_delta: 1,
        area_type: area_type
      )
      FactionWar.record_activity(
        state,
        'team_gold_dust',
        'johto',
        'Goldenrod Game Corner',
        'goldenrod_coin_market',
        threat_delta: 1,
        area_type: area_type
      )
      FactionWar.record_activity(
        state,
        'team_gas',
        'johto',
        'Goldenrod Underground',
        'underground_vent_probe',
        threat_delta: 1,
        area_type: area_type
      )
      FactionWar.record_activity(
        state,
        'team_moonlight',
        'johto',
        'Goldenrod Radio Tower',
        'radio_sleep_jingle',
        threat_delta: 1,
        area_type: area_type
      )
      FactionWar.record_activity(
        state,
        'nexus_order',
        'johto',
        'Goldenrod Radio Tower',
        'goldenrod_frequency_hidden',
        threat_delta: 0,
        area_type: area_type
      )
      FactionWar.record_conflict(
        state,
        'team_rocket',
        'team_gold_dust',
        'Goldenrod Game Corner',
        'Rocket broadcast money and Gold Dust coin-market laundering overlap before either side is ready to show its hand.',
        intensity: 2,
        area_type: area_type
      )
      FactionWar.record_conflict(
        state,
        'team_gas',
        'team_rocket',
        'Goldenrod Underground',
        'Team Gas vent probes interrupt Rocket cable taps below the city.',
        intensity: 2,
        area_type: area_type
      )

      story['current_act'] = 'act_9_goldenrod_hub_and_plain_badge'
      event = goldenrod_road_event_result(location)
      story['event_history'] << event
      story['latest_event'] = event

      WorldLink.queue_message(
        state,
        'story_alert',
        'Goldenrod opens as a real Johto hub: Route 34 daycare is online, Red keeps Antman grounded, Whitney is waiting, and Radio Tower static hints that Rocket is moving again.',
        source: 'johto_story',
        area_type: area_type
      )

      event
    end

    def goldenrod_road_cleared?(state)
      ensure_johto_story(state)['event_history'].any? { |event| event['event_id'] == GOLDENROD_ROAD_EVENT_ID }
    end

    def goldenrod_road_event_result(location)
      {
        'status' => 'cleared',
        'event_id' => GOLDENROD_ROAD_EVENT_ID,
        'location' => location.to_s,
        'region' => 'johto',
        'current_act' => 'act_9_goldenrod_hub_and_plain_badge',
        'route_chain' => ['Ilex Forest Gate', 'Route 34', 'Route 34 Daycare', 'Goldenrod City'],
        'companions' => %w[red brock bill],
        'rivals' => %w[blue ava silver],
        'factions' => %w[team_rocket team_gold_dust team_gas team_moonlight nexus_order],
        'linked_events' => [
          ROUTE34_DAYCARE_OPENED_EVENT_ID,
          GOLDENROD_CITY_ARRIVAL_EVENT_ID,
          GOLDENROD_RADIO_TOWER_TEASE_EVENT_ID,
          WHITNEY_GYM_TEASE_EVENT_ID,
          RED_GOLDENROD_ROAD_TRAINING_EVENT_ID,
          BROCK_ROUTE34_DAYCARE_ADVICE_EVENT_ID,
          BILL_GOLDENROD_SIGNAL_SCAN_EVENT_ID,
          BLUE_GOLDENROD_STANDINGS_EVENT_ID,
          AVA_ROUTE34_DAYCARE_RESEARCH_EVENT_ID,
          SILVER_GOLDENROD_PRESSURE_EVENT_ID,
          ROCKET_GOLDENROD_RADIO_SHADOW_EVENT_ID,
          GOLD_DUST_GOLDENROD_COIN_MARKET_EVENT_ID,
          TEAM_GAS_GOLDENROD_UNDERGROUND_EVENT_ID,
          MOONLIGHT_GOLDENROD_RADIO_JINGLE_EVENT_ID,
          NEXUS_ORDER_GOLDENROD_FREQUENCY_EVENT_ID,
          WHITNEY_PLAIN_BADGE_PREP_UNLOCKED_EVENT_ID
        ],
        'hub_services' => %w[route_34_daycare goldenrod_specialty_mart daycare_remote_check],
        'hidden_meta_signal' => 'nexus_order_goldenrod_frequency_unrevealed',
        'unlocks' => %w[route_34_daycare daycare_remote_check goldenrod_specialty_mart whitney_plain_badge_prep radio_tower_shadow_lead],
        'secondary_hook' => 'goldenrod_radio_tower_shadow',
        'next_hook' => 'whitney_plain_badge_prep'
      }
    end

    def complete_whitney_plain_badge_prep(state, location: 'Goldenrod Gym Plaza', area_type: 'town')
      story = ensure_johto_story(state)
      return { 'status' => 'blocked_missing_johto_region_unlock', 'event_id' => WHITNEY_PLAIN_BADGE_PREP_EVENT_ID } unless johto_unlocked?(state)
      return { 'status' => 'blocked_missing_goldenrod_road', 'event_id' => WHITNEY_PLAIN_BADGE_PREP_EVENT_ID } unless goldenrod_road_cleared?(state)
      return { 'status' => 'already_cleared', 'event_id' => WHITNEY_PLAIN_BADGE_PREP_EVENT_ID } if whitney_plain_badge_prep_cleared?(state)

      add_story_flag(state, 'FLAG_NEXUS_WHITNEY_PLAIN_BADGE_PREP')
      add_story_flag(state, 'FLAG_NEXUS_WHITNEY_ROLLOUT_COUNTER_TRAINING')
      add_story_flag(state, 'FLAG_NEXUS_RED_WHITNEY_PREP')
      add_story_flag(state, 'FLAG_NEXUS_BROCK_WHITNEY_COUNTER_ADVICE')
      add_story_flag(state, 'FLAG_NEXUS_BILL_RADIO_TOWER_BADGE_SCAN')
      add_story_flag(state, 'FLAG_NEXUS_BLUE_MILTANK_WARNING')
      add_story_flag(state, 'FLAG_NEXUS_SILVER_WHITNEY_PRESSURE')
      add_story_flag(state, 'FLAG_NEXUS_ROCKET_PLAIN_BADGE_RADIO_SYNC')
      add_story_flag(state, 'FLAG_NEXUS_GOLD_DUST_WHITNEY_BETTING')
      add_story_flag(state, 'FLAG_NEXUS_TEAM_GAS_GYM_BASEMENT_PRESSURE')
      add_story_flag(state, 'FLAG_NEXUS_MOONLIGHT_PLAIN_BADGE_JINGLE')
      add_story_flag(state, 'FLAG_NEXUS_NEXUS_ORDER_PLAIN_BADGE_FREQUENCY')
      add_story_flag(state, 'FLAG_NEXUS_WHITNEY_PLAIN_BADGE_BATTLE_UNLOCKED')

      [
        WHITNEY_PLAIN_BADGE_PREP_EVENT_ID,
        WHITNEY_ROLLOUT_COUNTER_TRAINING_EVENT_ID,
        RED_WHITNEY_PREP_EVENT_ID,
        BROCK_WHITNEY_COUNTER_ADVICE_EVENT_ID,
        BILL_RADIO_TOWER_BADGE_SCAN_EVENT_ID,
        BLUE_MILTANK_WARNING_EVENT_ID,
        SILVER_WHITNEY_PRESSURE_EVENT_ID,
        ROCKET_PLAIN_BADGE_RADIO_SYNC_EVENT_ID,
        GOLD_DUST_WHITNEY_BETTING_EVENT_ID,
        TEAM_GAS_GYM_BASEMENT_PRESSURE_EVENT_ID,
        MOONLIGHT_PLAIN_BADGE_JINGLE_EVENT_ID,
        NEXUS_ORDER_PLAIN_BADGE_FREQUENCY_EVENT_ID,
        WHITNEY_PLAIN_BADGE_BATTLE_UNLOCKED_EVENT_ID
      ].each { |event_id| mark_cleared_event(story, event_id) }

      CompanionProgress.record_scene(
        state,
        'red',
        'whitney_prep_focus',
        location: location,
        summary: 'Red warms up with Antman outside Goldenrod Gym and reminds him that Whitney is a real wall because confidence breaks faster than HP.',
        area_type: area_type
      )
      CompanionProgress.record_scene(
        state,
        'brock',
        'rollout_counter_advice',
        location: location,
        summary: 'Brock drills Rollout counterplay, status timing, and switching discipline so Antman can answer Miltank without relying on brute force.',
        area_type: area_type
      )
      CompanionProgress.record_scene(
        state,
        'bill',
        'radio_tower_badge_scan',
        location: 'Goldenrod Radio Tower',
        summary: 'Bill notices the Radio Tower static pulsing whenever Whitney tests her Plain Badge broadcast spot, tying the gym challenge to the city signal.',
        area_type: area_type
      )

      record_rival_story_clue(
        state,
        'silver',
        'Goldenrod Gym',
        'Silver challenged Whitney too quickly, got checked by the Plain Badge wall, and stormed out toward the Radio Tower crowd.',
        area_type,
        region: 'johto'
      )
      record_rival_story_clue(
        state,
        'blue',
        'Goldenrod Department Store',
        'Blue sent a blunt WorldLink warning: respect Miltank, carry a real answer, and do not let Rollout stack for free.',
        area_type,
        region: 'johto'
      )

      FactionWar.record_activity(
        state,
        'team_rocket',
        'johto',
        'Goldenrod Radio Tower',
        'plain_badge_radio_sync',
        threat_delta: 1,
        area_type: area_type
      )
      FactionWar.record_activity(
        state,
        'team_gold_dust',
        'johto',
        'Goldenrod Game Corner',
        'whitney_match_betting_ring',
        threat_delta: 1,
        area_type: area_type
      )
      FactionWar.record_activity(
        state,
        'team_gas',
        'johto',
        'Goldenrod Gym Basement',
        'gym_basement_vent_pressure',
        threat_delta: 1,
        area_type: area_type
      )
      FactionWar.record_activity(
        state,
        'team_moonlight',
        'johto',
        'Goldenrod Radio Tower',
        'plain_badge_sleep_jingle',
        threat_delta: 1,
        area_type: area_type
      )
      FactionWar.record_activity(
        state,
        'nexus_order',
        'johto',
        'Goldenrod Radio Tower',
        'plain_badge_frequency_hidden',
        threat_delta: 0,
        area_type: area_type
      )
      FactionWar.record_conflict(
        state,
        'team_rocket',
        'team_moonlight',
        'Goldenrod Radio Tower',
        'Rocket badge-frequency sync is distorted by Moonlight sleep-jingle interference before Whitney opens the gym floor.',
        intensity: 2,
        area_type: area_type
      )

      story['current_act'] = 'act_10_whitney_plain_badge_challenge'
      event = whitney_plain_badge_prep_event_result(location)
      story['event_history'] << event
      story['latest_event'] = event

      WorldLink.queue_message(
        state,
        'story_alert',
        'Whitney opens the Plain Badge challenge: Red steadies Antman, Brock drills Miltank answers, and Bill catches Radio Tower static pulsing under the gym hype.',
        source: 'johto_story',
        area_type: area_type
      )

      event
    end

    def whitney_plain_badge_prep_cleared?(state)
      ensure_johto_story(state)['event_history'].any? { |event| event['event_id'] == WHITNEY_PLAIN_BADGE_PREP_EVENT_ID }
    end

    def whitney_plain_badge_prep_event_result(location)
      {
        'status' => 'cleared',
        'event_id' => WHITNEY_PLAIN_BADGE_PREP_EVENT_ID,
        'location' => location.to_s,
        'region' => 'johto',
        'current_act' => 'act_10_whitney_plain_badge_challenge',
        'gym_leader' => 'Whitney',
        'badge' => 'Plain Badge',
        'level_cap' => 26,
        'companions' => %w[red brock bill],
        'rivals' => %w[blue silver],
        'factions' => %w[team_rocket team_gold_dust team_gas team_moonlight nexus_order],
        'linked_events' => [
          WHITNEY_ROLLOUT_COUNTER_TRAINING_EVENT_ID,
          RED_WHITNEY_PREP_EVENT_ID,
          BROCK_WHITNEY_COUNTER_ADVICE_EVENT_ID,
          BILL_RADIO_TOWER_BADGE_SCAN_EVENT_ID,
          BLUE_MILTANK_WARNING_EVENT_ID,
          SILVER_WHITNEY_PRESSURE_EVENT_ID,
          ROCKET_PLAIN_BADGE_RADIO_SYNC_EVENT_ID,
          GOLD_DUST_WHITNEY_BETTING_EVENT_ID,
          TEAM_GAS_GYM_BASEMENT_PRESSURE_EVENT_ID,
          MOONLIGHT_PLAIN_BADGE_JINGLE_EVENT_ID,
          NEXUS_ORDER_PLAIN_BADGE_FREQUENCY_EVENT_ID,
          WHITNEY_PLAIN_BADGE_BATTLE_UNLOCKED_EVENT_ID
        ],
        'battle_hook' => {
          'battle_id' => 'whitney_plain_badge_battle',
          'leader' => 'Whitney',
          'level_cap' => 26,
          'companion_rule' => 'no_companion_assist_in_gym_battle',
          'standard_team' => [
            { 'species' => 'Clefairy', 'level' => 24, 'role' => 'support' },
            { 'species' => 'Miltank', 'level' => 26, 'role' => 'ace' }
          ],
          'hard_team' => [
            { 'species' => 'Clefairy', 'level' => 25, 'role' => 'support' },
            { 'species' => 'Lopunny', 'level' => 25, 'role' => 'speed_control' },
            { 'species' => 'Miltank', 'level' => 26, 'role' => 'ace' }
          ]
        },
        'hidden_meta_signal' => 'nexus_order_plain_badge_frequency_unrevealed',
        'unlocks' => %w[whitney_plain_badge_battle goldenrod_gym_services rollout_counter_training],
        'next_hook' => 'whitney_plain_badge_battle'
      }
    end

    def complete_whitney_plain_badge_battle(state, location: 'Goldenrod Gym', result: 'won', area_type: 'gym')
      story = ensure_johto_story(state)
      return { 'status' => 'blocked_missing_johto_region_unlock', 'event_id' => WHITNEY_PLAIN_BADGE_BATTLE_EVENT_ID } unless johto_unlocked?(state)
      return { 'status' => 'blocked_missing_whitney_plain_badge_prep', 'event_id' => WHITNEY_PLAIN_BADGE_BATTLE_EVENT_ID } unless whitney_plain_badge_prep_cleared?(state)
      return { 'status' => 'already_cleared', 'event_id' => WHITNEY_PLAIN_BADGE_BATTLE_EVENT_ID } if whitney_plain_badge_battle_cleared?(state)

      add_story_flag(state, 'plain_badge_obtained')
      add_story_flag(state, 'FLAG_NEXUS_PLAIN_BADGE')
      add_story_flag(state, 'FLAG_NEXUS_WHITNEY_BATTLE_STARTED')
      add_story_flag(state, 'FLAG_NEXUS_WHITNEY_BATTLE_FINISHED')
      add_story_flag(state, 'FLAG_NEXUS_RED_POST_WHITNEY')
      add_story_flag(state, 'FLAG_NEXUS_BROCK_POST_WHITNEY')
      add_story_flag(state, 'FLAG_NEXUS_BILL_PLAIN_BADGE_SIGNAL_DECODED')
      add_story_flag(state, 'FLAG_NEXUS_BLUE_POST_WHITNEY_RESPECT')
      add_story_flag(state, 'FLAG_NEXUS_SILVER_RADIO_TOWER_RACE')
      add_story_flag(state, 'FLAG_NEXUS_ROCKET_RADIO_TOWER_TAKEOVER_STAGING')
      add_story_flag(state, 'FLAG_NEXUS_GOLD_DUST_WHITNEY_MATCH_PAYOUTS')
      add_story_flag(state, 'FLAG_NEXUS_TEAM_GAS_UNDERGROUND_EXHAUST_LEAK')
      add_story_flag(state, 'FLAG_NEXUS_MOONLIGHT_PLAIN_BADGE_JINGLE_COLLAPSE')
      add_story_flag(state, 'FLAG_NEXUS_NEXUS_ORDER_PLAIN_BADGE_RESONANCE')
      add_story_flag(state, 'FLAG_NEXUS_GOLDENROD_RADIO_TOWER_CRISIS_UNLOCKED')

      [
        WHITNEY_PLAIN_BADGE_BATTLE_EVENT_ID,
        PLAIN_BADGE_OBTAINED_EVENT_ID,
        RED_POST_WHITNEY_EVENT_ID,
        BROCK_POST_WHITNEY_EVENT_ID,
        BILL_PLAIN_BADGE_SIGNAL_DECODED_EVENT_ID,
        BLUE_POST_WHITNEY_RESPECT_EVENT_ID,
        SILVER_RADIO_TOWER_RACE_EVENT_ID,
        ROCKET_RADIO_TOWER_TAKEOVER_STAGING_EVENT_ID,
        GOLD_DUST_WHITNEY_MATCH_PAYOUTS_EVENT_ID,
        TEAM_GAS_UNDERGROUND_EXHAUST_LEAK_EVENT_ID,
        MOONLIGHT_PLAIN_BADGE_JINGLE_COLLAPSE_EVENT_ID,
        NEXUS_ORDER_PLAIN_BADGE_RESONANCE_EVENT_ID,
        GOLDENROD_RADIO_TOWER_CRISIS_UNLOCKED_EVENT_ID
      ].each { |event_id| mark_cleared_event(story, event_id) }

      CompanionProgress.record_scene(
        state,
        'red',
        'post_whitney_respect',
        location: location,
        summary: 'Red congratulates Antman after the Plain Badge and says the real win was staying calm when Whitney turned the battle emotional.',
        area_type: area_type
      )
      CompanionProgress.record_scene(
        state,
        'brock',
        'post_whitney_recovery_review',
        location: location,
        summary: 'Brock reviews the Miltank answer plan, checks the party after Rollout pressure, and points Antman back toward the Radio Tower static.',
        area_type: area_type
      )
      CompanionProgress.record_scene(
        state,
        'bill',
        'plain_badge_signal_decode',
        location: 'Goldenrod Radio Tower',
        summary: 'Bill decodes the Plain Badge resonance and confirms the Radio Tower shadow is no longer background noise.',
        area_type: area_type
      )

      record_rival_story_clue(
        state,
        'silver',
        'Goldenrod Radio Tower',
        'Silver saw Antman win the Plain Badge and bolted toward the Radio Tower, furious that the city signal reacted to the badge.',
        area_type,
        region: 'johto'
      )
      record_rival_story_clue(
        state,
        'blue',
        'Goldenrod Gym',
        'Blue admitted Whitney was a real test, then warned Antman that the Radio Tower crowd is moving wrong.',
        area_type,
        region: 'johto'
      )

      FactionWar.record_activity(
        state,
        'team_rocket',
        'johto',
        'Goldenrod Radio Tower',
        'radio_tower_takeover_staging',
        threat_delta: 2,
        area_type: area_type
      )
      FactionWar.record_activity(
        state,
        'team_gold_dust',
        'johto',
        'Goldenrod Game Corner',
        'whitney_match_payouts',
        threat_delta: 1,
        area_type: area_type
      )
      FactionWar.record_activity(
        state,
        'team_gas',
        'johto',
        'Goldenrod Underground',
        'underground_exhaust_leak',
        threat_delta: 1,
        area_type: area_type
      )
      FactionWar.record_activity(
        state,
        'team_moonlight',
        'johto',
        'Goldenrod Radio Tower',
        'plain_badge_jingle_collapse',
        threat_delta: 1,
        area_type: area_type
      )
      FactionWar.record_activity(
        state,
        'nexus_order',
        'johto',
        'Goldenrod Radio Tower',
        'plain_badge_resonance_hidden',
        threat_delta: 0,
        area_type: area_type
      )
      FactionWar.record_conflict(
        state,
        'team_rocket',
        'team_gas',
        'Goldenrod Underground',
        'Rocket takeover staging pulls too much power through the underground and triggers Team Gas exhaust leaks.',
        intensity: 2,
        area_type: area_type
      )

      story['current_act'] = 'act_11_goldenrod_radio_tower_shadow'
      event = whitney_plain_badge_battle_event_result(location, result)
      story['event_history'] << event
      story['latest_event'] = event

      WorldLink.queue_message(
        state,
        'story_alert',
        'Antman earned the Plain Badge. Red stays close, Bill confirms the Radio Tower signal is active, and Goldenrod shifts from gym pressure to Rocket crisis.',
        source: 'johto_story',
        area_type: area_type
      )

      event
    end

    def whitney_plain_badge_battle_cleared?(state)
      ensure_johto_story(state)['event_history'].any? { |event| event['event_id'] == WHITNEY_PLAIN_BADGE_BATTLE_EVENT_ID }
    end

    def whitney_plain_badge_battle_event_result(location, result)
      {
        'status' => 'cleared',
        'event_id' => WHITNEY_PLAIN_BADGE_BATTLE_EVENT_ID,
        'battle_id' => WHITNEY_PLAIN_BADGE_BATTLE_EVENT_ID,
        'location' => location.to_s,
        'region' => 'johto',
        'current_act' => 'act_11_goldenrod_radio_tower_shadow',
        'result' => result.to_s,
        'gym_leader' => 'Whitney',
        'badge' => 'Plain Badge',
        'level_cap' => 26,
        'companion_rule' => 'no_companion_assist_in_gym_battle',
        'companions' => %w[red brock bill],
        'rivals' => %w[blue silver],
        'factions' => %w[team_rocket team_gold_dust team_gas team_moonlight nexus_order],
        'linked_events' => [
          PLAIN_BADGE_OBTAINED_EVENT_ID,
          RED_POST_WHITNEY_EVENT_ID,
          BROCK_POST_WHITNEY_EVENT_ID,
          BILL_PLAIN_BADGE_SIGNAL_DECODED_EVENT_ID,
          BLUE_POST_WHITNEY_RESPECT_EVENT_ID,
          SILVER_RADIO_TOWER_RACE_EVENT_ID,
          ROCKET_RADIO_TOWER_TAKEOVER_STAGING_EVENT_ID,
          GOLD_DUST_WHITNEY_MATCH_PAYOUTS_EVENT_ID,
          TEAM_GAS_UNDERGROUND_EXHAUST_LEAK_EVENT_ID,
          MOONLIGHT_PLAIN_BADGE_JINGLE_COLLAPSE_EVENT_ID,
          NEXUS_ORDER_PLAIN_BADGE_RESONANCE_EVENT_ID,
          GOLDENROD_RADIO_TOWER_CRISIS_UNLOCKED_EVENT_ID
        ],
        'hidden_meta_signal' => 'nexus_order_plain_badge_resonance_unrevealed',
        'unlocks' => %w[goldenrod_radio_tower_shadow whitney_rematch_board_tier_1 attract_tm_lead],
        'next_hook' => 'goldenrod_radio_tower_shadow'
      }
    end

    def complete_goldenrod_radio_tower_shadow(state, location: 'Goldenrod Radio Tower', area_type: 'villain_hideout')
      story = ensure_johto_story(state)
      return { 'status' => 'blocked_missing_johto_region_unlock', 'event_id' => GOLDENROD_RADIO_TOWER_SHADOW_EVENT_ID } unless johto_unlocked?(state)
      return { 'status' => 'blocked_missing_whitney_plain_badge_battle', 'event_id' => GOLDENROD_RADIO_TOWER_SHADOW_EVENT_ID } unless whitney_plain_badge_battle_cleared?(state)
      return { 'status' => 'already_cleared', 'event_id' => GOLDENROD_RADIO_TOWER_SHADOW_EVENT_ID } if goldenrod_radio_tower_shadow_cleared?(state)

      add_story_flag(state, 'FLAG_NEXUS_GOLDENROD_RADIO_TOWER_SHADOW')
      add_story_flag(state, 'FLAG_NEXUS_RADIO_TOWER_LOCKDOWN')
      add_story_flag(state, 'FLAG_NEXUS_RED_RADIO_TOWER_ENTRY')
      add_story_flag(state, 'FLAG_NEXUS_BLUE_RADIO_TOWER_CROWD_CONTROL')
      add_story_flag(state, 'FLAG_NEXUS_BILL_BROADCAST_JAM_DECODE')
      add_story_flag(state, 'FLAG_NEXUS_SILVER_RADIO_TOWER_SIDE_DOOR')
      add_story_flag(state, 'FLAG_NEXUS_AVA_GOLDENROD_BROADCAST_CLUE')
      add_story_flag(state, 'FLAG_NEXUS_ROCKET_RADIO_TOWER_LOBBY_TAKEOVER')
      add_story_flag(state, 'FLAG_NEXUS_GOLD_DUST_RADIO_TOWER_AD_BUY')
      add_story_flag(state, 'FLAG_NEXUS_TEAM_GAS_RADIO_TOWER_GENERATOR')
      add_story_flag(state, 'FLAG_NEXUS_MOONLIGHT_BROADCAST_HYPNOSIS')
      add_story_flag(state, 'FLAG_NEXUS_NEXUS_ORDER_RADIO_TRANSMITTER_PATTERN')
      add_story_flag(state, 'FLAG_NEXUS_RADIO_TOWER_LOBBY_BATTLE_UNLOCKED')
      add_story_flag(state, 'FLAG_NEXUS_GOLDENROD_UNDERGROUND_WAREHOUSE_LEAD')

      [
        GOLDENROD_RADIO_TOWER_SHADOW_EVENT_ID,
        RADIO_TOWER_LOCKDOWN_EVENT_ID,
        RED_RADIO_TOWER_ENTRY_EVENT_ID,
        BLUE_RADIO_TOWER_CROWD_CONTROL_EVENT_ID,
        BILL_BROADCAST_JAM_EVENT_ID,
        SILVER_RADIO_TOWER_SIDE_DOOR_EVENT_ID,
        AVA_GOLDENROD_BROADCAST_CLUE_EVENT_ID,
        ROCKET_RADIO_TOWER_LOBBY_TAKEOVER_EVENT_ID,
        GOLD_DUST_RADIO_TOWER_AD_BUY_EVENT_ID,
        TEAM_GAS_RADIO_TOWER_GENERATOR_EVENT_ID,
        MOONLIGHT_BROADCAST_HYPNOSIS_EVENT_ID,
        NEXUS_ORDER_RADIO_TRANSMITTER_PATTERN_EVENT_ID,
        RADIO_TOWER_LOBBY_BATTLE_UNLOCKED_EVENT_ID,
        GOLDENROD_UNDERGROUND_WAREHOUSE_LEAD_EVENT_ID
      ].each { |event_id| mark_cleared_event(story, event_id) }

      CompanionProgress.record_scene(
        state,
        'red',
        'radio_tower_entry_guard',
        location: location,
        summary: 'Red steps in front of Antman at the Radio Tower doors, not to take over, but to make sure the first Rocket rush does not split the team.',
        area_type: area_type
      )
      CompanionProgress.record_scene(
        state,
        'blue',
        'radio_tower_crowd_control',
        location: 'Goldenrod Radio Tower Lobby',
        summary: 'Blue drops the rivalry act long enough to move civilians out of the lobby while daring Rocket to try him first.',
        area_type: area_type
      )
      CompanionProgress.record_scene(
        state,
        'bill',
        'broadcast_jam_decode',
        location: location,
        summary: 'Bill reads the jammed broadcast and confirms the tower signal is being split between Rocket orders, Moonlight hypnosis, and a hidden transmitter pattern.',
        area_type: area_type
      )

      record_rival_story_clue(
        state,
        'silver',
        'Goldenrod Radio Tower Side Door',
        'Silver slipped through a Radio Tower side door after the lockdown, chasing Rocket without waiting for Antman or Red.',
        area_type,
        region: 'johto'
      )
      record_rival_story_clue(
        state,
        'ava',
        'Goldenrod Station',
        'Ava caught a Goldenrod broadcast clue from the station feed and warned WorldLink that the public tower audio is being rewritten live.',
        area_type,
        region: 'johto'
      )

      FactionWar.record_activity(
        state,
        'team_rocket',
        'johto',
        'Goldenrod Radio Tower Lobby',
        'radio_tower_lobby_takeover',
        threat_delta: 2,
        area_type: area_type
      )
      FactionWar.record_activity(
        state,
        'team_gold_dust',
        'johto',
        'Goldenrod Radio Tower Ad Office',
        'radio_tower_ad_buy_laundering',
        threat_delta: 1,
        area_type: area_type
      )
      FactionWar.record_activity(
        state,
        'team_gas',
        'johto',
        'Goldenrod Radio Tower Generator Room',
        'radio_tower_generator_vent_pressure',
        threat_delta: 1,
        area_type: area_type
      )
      FactionWar.record_activity(
        state,
        'team_moonlight',
        'johto',
        'Goldenrod Radio Tower Broadcast Booth',
        'broadcast_hypnosis_leak',
        threat_delta: 1,
        area_type: area_type
      )
      FactionWar.record_activity(
        state,
        'nexus_order',
        'johto',
        'Goldenrod Radio Tower Transmitter',
        'radio_tower_transmitter_pattern_hidden',
        threat_delta: 0,
        area_type: area_type
      )
      FactionWar.record_conflict(
        state,
        'team_rocket',
        'team_gold_dust',
        'Goldenrod Radio Tower Lobby',
        'Rocket takeover crews catch Gold Dust laundering ad buys through the same tower accounts.',
        intensity: 2,
        area_type: area_type
      )
      FactionWar.record_conflict(
        state,
        'team_gas',
        'team_moonlight',
        'Goldenrod Radio Tower Generator Room',
        'Team Gas vent pressure destabilizes Moonlight broadcast hypnosis under the tower.',
        intensity: 2,
        area_type: area_type
      )

      story['current_act'] = 'act_12_radio_tower_lockdown'
      event = goldenrod_radio_tower_shadow_event_result(location)
      story['event_history'] << event
      story['latest_event'] = event

      WorldLink.queue_message(
        state,
        'story_alert',
        'Goldenrod Radio Tower is under Rocket lockdown. Red and Blue hold the lobby, Bill is tracing the broadcast jam, and the underground warehouse lead just became urgent.',
        source: 'johto_story',
        area_type: area_type
      )

      event
    end

    def goldenrod_radio_tower_shadow_cleared?(state)
      ensure_johto_story(state)['event_history'].any? { |event| event['event_id'] == GOLDENROD_RADIO_TOWER_SHADOW_EVENT_ID }
    end

    def goldenrod_radio_tower_shadow_event_result(location)
      {
        'status' => 'cleared',
        'event_id' => GOLDENROD_RADIO_TOWER_SHADOW_EVENT_ID,
        'location' => location.to_s,
        'region' => 'johto',
        'current_act' => 'act_12_radio_tower_lockdown',
        'route_chain' => ['Goldenrod Gym', 'Goldenrod Radio Tower Lobby', 'Goldenrod Underground Warehouse Lead'],
        'companions' => %w[red blue bill],
        'rivals' => %w[ava silver],
        'factions' => %w[team_rocket team_gold_dust team_gas team_moonlight nexus_order],
        'linked_events' => [
          RADIO_TOWER_LOCKDOWN_EVENT_ID,
          RED_RADIO_TOWER_ENTRY_EVENT_ID,
          BLUE_RADIO_TOWER_CROWD_CONTROL_EVENT_ID,
          BILL_BROADCAST_JAM_EVENT_ID,
          SILVER_RADIO_TOWER_SIDE_DOOR_EVENT_ID,
          AVA_GOLDENROD_BROADCAST_CLUE_EVENT_ID,
          ROCKET_RADIO_TOWER_LOBBY_TAKEOVER_EVENT_ID,
          GOLD_DUST_RADIO_TOWER_AD_BUY_EVENT_ID,
          TEAM_GAS_RADIO_TOWER_GENERATOR_EVENT_ID,
          MOONLIGHT_BROADCAST_HYPNOSIS_EVENT_ID,
          NEXUS_ORDER_RADIO_TRANSMITTER_PATTERN_EVENT_ID,
          RADIO_TOWER_LOBBY_BATTLE_UNLOCKED_EVENT_ID,
          GOLDENROD_UNDERGROUND_WAREHOUSE_LEAD_EVENT_ID
        ],
        'battle_hook' => {
          'battle_id' => 'radio_tower_lobby_battle',
          'level_cap' => 28,
          'companion_rule' => 'red_and_blue_tag_allowed_outside_gym',
          'enemy_trainers' => %w[rocket_signal_grunt_pair],
          'enemy_team_theme' => %w[poison electric normal]
        },
        'hidden_meta_signal' => 'nexus_order_radio_transmitter_pattern_unrevealed',
        'unlocks' => %w[radio_tower_lobby_battle goldenrod_underground_warehouse_lead radio_tower_digest_after_exit],
        'next_hook' => 'radio_tower_lobby_battle'
      }
    end

    def complete_radio_tower_lobby_battle(state, location: 'Goldenrod Radio Tower Lobby', result: 'won', area_type: 'villain_hideout')
      story = ensure_johto_story(state)
      return { 'status' => 'blocked_missing_johto_region_unlock', 'event_id' => RADIO_TOWER_LOBBY_BATTLE_EVENT_ID } unless johto_unlocked?(state)
      return { 'status' => 'blocked_missing_goldenrod_radio_tower_shadow', 'event_id' => RADIO_TOWER_LOBBY_BATTLE_EVENT_ID } unless goldenrod_radio_tower_shadow_cleared?(state)
      return { 'status' => 'already_cleared', 'event_id' => RADIO_TOWER_LOBBY_BATTLE_EVENT_ID } if radio_tower_lobby_battle_cleared?(state)

      add_story_flag(state, 'FLAG_NEXUS_RADIO_TOWER_LOBBY_BATTLE_STARTED')
      add_story_flag(state, 'FLAG_NEXUS_RADIO_TOWER_LOBBY_BATTLE_FINISHED')
      add_story_flag(state, 'FLAG_NEXUS_RADIO_TOWER_LOBBY_CLEARED')
      add_story_flag(state, 'FLAG_NEXUS_RED_BLUE_RADIO_TOWER_TAG')
      add_story_flag(state, 'FLAG_NEXUS_BILL_LOBBY_SIGNAL_CACHE')
      add_story_flag(state, 'FLAG_NEXUS_SILVER_UNDERGROUND_WAREHOUSE_RACE')
      add_story_flag(state, 'FLAG_NEXUS_AVA_ROCKET_BROADCAST_ARCHIVE')
      add_story_flag(state, 'FLAG_NEXUS_ROCKET_EXECUTIVE_ELEVATOR_LOCK')
      add_story_flag(state, 'FLAG_NEXUS_GOLD_DUST_AD_LEDGER_DROP')
      add_story_flag(state, 'FLAG_NEXUS_TEAM_GAS_GENERATOR_SMOKE')
      add_story_flag(state, 'FLAG_NEXUS_MOONLIGHT_LOBBY_SIGNAL_FADE')
      add_story_flag(state, 'FLAG_NEXUS_NEXUS_ORDER_ELEVATOR_PATTERN')
      add_story_flag(state, 'FLAG_NEXUS_GOLDENROD_UNDERGROUND_WAREHOUSE_UNLOCKED')

      [
        RADIO_TOWER_LOBBY_BATTLE_EVENT_ID,
        RADIO_TOWER_LOBBY_CLEARED_EVENT_ID,
        RED_BLUE_RADIO_TOWER_TAG_EVENT_ID,
        BILL_LOBBY_SIGNAL_CACHE_EVENT_ID,
        SILVER_UNDERGROUND_WAREHOUSE_RACE_EVENT_ID,
        AVA_ROCKET_BROADCAST_ARCHIVE_EVENT_ID,
        ROCKET_EXECUTIVE_ELEVATOR_LOCK_EVENT_ID,
        GOLD_DUST_AD_LEDGER_DROP_EVENT_ID,
        TEAM_GAS_GENERATOR_SMOKE_EVENT_ID,
        MOONLIGHT_LOBBY_SIGNAL_FADE_EVENT_ID,
        NEXUS_ORDER_ELEVATOR_PATTERN_EVENT_ID,
        GOLDENROD_UNDERGROUND_WAREHOUSE_UNLOCKED_EVENT_ID
      ].each { |event_id| mark_cleared_event(story, event_id) }

      CompanionProgress.record_scene(
        state,
        'red',
        'radio_tower_lobby_tag_cleanup',
        location: location,
        summary: 'Red battles beside Antman long enough to break the Rocket lobby line, then points the team toward the underground route instead of celebrating.',
        area_type: area_type
      )
      CompanionProgress.record_scene(
        state,
        'blue',
        'radio_tower_lobby_tag_cleanup',
        location: location,
        summary: 'Blue covers the exit after the tag battle, calling the win sloppy but admitting Antman and Red opened the only path Rocket did not expect.',
        area_type: area_type
      )
      CompanionProgress.record_scene(
        state,
        'bill',
        'lobby_signal_cache',
        location: location,
        summary: 'Bill copies the lobby transmitter cache and finds elevator lock data pointing below Goldenrod instead of up the tower.',
        area_type: area_type
      )

      record_rival_story_clue(
        state,
        'silver',
        'Goldenrod Underground Warehouse',
        'Silver raced toward the Underground Warehouse after the Rocket lobby battle, chasing the executive elevator lock before Antman could question him.',
        area_type,
        region: 'johto'
      )
      record_rival_story_clue(
        state,
        'ava',
        'Goldenrod Radio Tower Archive',
        'Ava recovered a broadcast archive from Goldenrod that proves Rocket edited the public signal after the lobby fight.',
        area_type,
        region: 'johto'
      )

      FactionWar.record_activity(
        state,
        'team_rocket',
        'johto',
        'Goldenrod Radio Tower Elevator',
        'executive_elevator_lock',
        threat_delta: 2,
        area_type: area_type
      )
      FactionWar.record_activity(
        state,
        'team_gold_dust',
        'johto',
        'Goldenrod Radio Tower Ad Office',
        'ad_ledger_drop',
        threat_delta: 1,
        area_type: area_type
      )
      FactionWar.record_activity(
        state,
        'team_gas',
        'johto',
        'Goldenrod Radio Tower Generator Room',
        'generator_smoke_leak',
        threat_delta: 1,
        area_type: area_type
      )
      FactionWar.record_activity(
        state,
        'team_moonlight',
        'johto',
        'Goldenrod Radio Tower Lobby',
        'lobby_signal_fade',
        threat_delta: 1,
        area_type: area_type
      )
      FactionWar.record_activity(
        state,
        'nexus_order',
        'johto',
        'Goldenrod Radio Tower Elevator',
        'elevator_pattern_hidden',
        threat_delta: 0,
        area_type: area_type
      )
      FactionWar.record_conflict(
        state,
        'team_rocket',
        'team_gas',
        'Goldenrod Radio Tower Generator Room',
        'Rocket locks the executive elevator while Team Gas smoke from the generator room threatens to expose both operations.',
        intensity: 2,
        area_type: area_type
      )

      story['current_act'] = 'act_13_goldenrod_underground_warehouse'
      event = radio_tower_lobby_battle_event_result(location, result)
      story['event_history'] << event
      story['latest_event'] = event

      WorldLink.queue_message(
        state,
        'story_alert',
        'The Radio Tower lobby battle is won, but Rocket sealed the elevator and the Underground Warehouse is now the only live lead.',
        source: 'johto_story',
        area_type: area_type
      )

      event
    end

    def radio_tower_lobby_battle_cleared?(state)
      ensure_johto_story(state)['event_history'].any? { |event| event['event_id'] == RADIO_TOWER_LOBBY_BATTLE_EVENT_ID }
    end

    def radio_tower_lobby_battle_event_result(location, result)
      {
        'status' => 'cleared',
        'event_id' => RADIO_TOWER_LOBBY_BATTLE_EVENT_ID,
        'battle_id' => 'radio_tower_lobby_battle',
        'location' => location.to_s,
        'region' => 'johto',
        'current_act' => 'act_13_goldenrod_underground_warehouse',
        'result' => result.to_s,
        'companion_rule' => 'red_and_blue_tag_allowed_outside_gym',
        'companions' => %w[red blue bill],
        'rivals' => %w[ava silver],
        'factions' => %w[team_rocket team_gold_dust team_gas team_moonlight nexus_order],
        'linked_events' => [
          RADIO_TOWER_LOBBY_CLEARED_EVENT_ID,
          RED_BLUE_RADIO_TOWER_TAG_EVENT_ID,
          BILL_LOBBY_SIGNAL_CACHE_EVENT_ID,
          SILVER_UNDERGROUND_WAREHOUSE_RACE_EVENT_ID,
          AVA_ROCKET_BROADCAST_ARCHIVE_EVENT_ID,
          ROCKET_EXECUTIVE_ELEVATOR_LOCK_EVENT_ID,
          GOLD_DUST_AD_LEDGER_DROP_EVENT_ID,
          TEAM_GAS_GENERATOR_SMOKE_EVENT_ID,
          MOONLIGHT_LOBBY_SIGNAL_FADE_EVENT_ID,
          NEXUS_ORDER_ELEVATOR_PATTERN_EVENT_ID,
          GOLDENROD_UNDERGROUND_WAREHOUSE_UNLOCKED_EVENT_ID
        ],
        'route_chain' => ['Goldenrod Radio Tower Lobby', 'Goldenrod Underground', 'Goldenrod Underground Warehouse'],
        'hidden_meta_signal' => 'nexus_order_elevator_pattern_unrevealed',
        'unlocks' => %w[goldenrod_underground_warehouse rocket_elevator_lock_clue radio_tower_digest_after_exit],
        'next_hook' => 'goldenrod_underground_warehouse'
      }
    end

    def complete_goldenrod_underground_warehouse(state, location: 'Goldenrod Underground Warehouse', area_type: 'villain_hideout')
      story = ensure_johto_story(state)
      return { 'status' => 'blocked_missing_johto_region_unlock', 'event_id' => GOLDENROD_UNDERGROUND_WAREHOUSE_EVENT_ID } unless johto_unlocked?(state)
      return { 'status' => 'blocked_missing_radio_tower_lobby_battle', 'event_id' => GOLDENROD_UNDERGROUND_WAREHOUSE_EVENT_ID } unless radio_tower_lobby_battle_cleared?(state)
      return { 'status' => 'already_cleared', 'event_id' => GOLDENROD_UNDERGROUND_WAREHOUSE_EVENT_ID } if goldenrod_underground_warehouse_cleared?(state)

      add_story_flag(state, 'FLAG_NEXUS_GOLDENROD_UNDERGROUND_WAREHOUSE')
      add_story_flag(state, 'FLAG_NEXUS_WAREHOUSE_SWITCH_ROOM')
      add_story_flag(state, 'FLAG_NEXUS_RED_WAREHOUSE_BACKUP')
      add_story_flag(state, 'FLAG_NEXUS_BLUE_RADIO_TOWER_LOBBY_HOLD')
      add_story_flag(state, 'FLAG_NEXUS_BILL_DIRECTOR_CARD_TRACE')
      add_story_flag(state, 'FLAG_NEXUS_SILVER_WAREHOUSE_RIVAL_CLASH')
      add_story_flag(state, 'FLAG_NEXUS_AVA_UNDERGROUND_LEDGER_DECODE')
      add_story_flag(state, 'FLAG_NEXUS_ROCKET_DIRECTOR_CARD_THEFT')
      add_story_flag(state, 'FLAG_NEXUS_GOLD_DUST_WAREHOUSE_LEDGER_GRAB')
      add_story_flag(state, 'FLAG_NEXUS_TEAM_GAS_SWITCH_ROOM_FUMES')
      add_story_flag(state, 'FLAG_NEXUS_MOONLIGHT_BASEMENT_SIGNAL_RELAY')
      add_story_flag(state, 'FLAG_NEXUS_NEXUS_ORDER_BASEMENT_GRID')
      add_story_flag(state, 'FLAG_NEXUS_RADIO_TOWER_DIRECTOR_RESCUE_UNLOCKED')

      [
        GOLDENROD_UNDERGROUND_WAREHOUSE_EVENT_ID,
        WAREHOUSE_SWITCH_ROOM_EVENT_ID,
        RED_WAREHOUSE_BACKUP_EVENT_ID,
        BLUE_RADIO_TOWER_LOBBY_HOLD_EVENT_ID,
        BILL_DIRECTOR_CARD_TRACE_EVENT_ID,
        SILVER_WAREHOUSE_RIVAL_CLASH_EVENT_ID,
        AVA_UNDERGROUND_LEDGER_DECODE_EVENT_ID,
        ROCKET_DIRECTOR_CARD_THEFT_EVENT_ID,
        GOLD_DUST_WAREHOUSE_LEDGER_GRAB_EVENT_ID,
        TEAM_GAS_SWITCH_ROOM_FUMES_EVENT_ID,
        MOONLIGHT_BASEMENT_SIGNAL_RELAY_EVENT_ID,
        NEXUS_ORDER_BASEMENT_GRID_EVENT_ID,
        RADIO_TOWER_DIRECTOR_RESCUE_UNLOCKED_EVENT_ID
      ].each { |event_id| mark_cleared_event(story, event_id) }

      CompanionProgress.record_scene(
        state,
        'red',
        'warehouse_backup',
        location: location,
        summary: 'Red stays close in the Underground Warehouse, letting Antman lead the switch room while he cuts off Rocket escape routes.',
        area_type: area_type
      )
      CompanionProgress.record_scene(
        state,
        'blue',
        'radio_tower_lobby_hold',
        location: 'Goldenrod Radio Tower Lobby',
        summary: 'Blue holds the Radio Tower lobby alone, forcing Rocket to keep splitting grunts between the tower and the warehouse.',
        area_type: area_type
      )
      CompanionProgress.record_scene(
        state,
        'bill',
        'director_card_trace',
        location: location,
        summary: 'Bill traces the stolen Director Card Key through the warehouse locks and marks the route back into the Radio Tower upper floors.',
        area_type: area_type
      )

      record_rival_story_clue(
        state,
        'silver',
        location,
        'Silver clashed with Rocket in the Warehouse switch room, furious that their stolen Director Card Key slowed his own chase.',
        area_type,
        region: 'johto'
      )
      record_rival_story_clue(
        state,
        'ava',
        'Goldenrod Underground Ledger Room',
        'Ava decoded an Underground ledger that ties Gold Dust ad money to Rocket warehouse access.',
        area_type,
        region: 'johto'
      )

      FactionWar.record_activity(
        state,
        'team_rocket',
        'johto',
        location,
        'director_card_theft',
        threat_delta: 2,
        area_type: area_type
      )
      FactionWar.record_activity(
        state,
        'team_gold_dust',
        'johto',
        'Goldenrod Underground Warehouse Vault',
        'warehouse_ledger_grab',
        threat_delta: 1,
        area_type: area_type
      )
      FactionWar.record_activity(
        state,
        'team_gas',
        'johto',
        'Goldenrod Underground Switch Room',
        'switch_room_fumes',
        threat_delta: 1,
        area_type: area_type
      )
      FactionWar.record_activity(
        state,
        'team_moonlight',
        'johto',
        'Goldenrod Underground Relay Alcove',
        'basement_signal_relay',
        threat_delta: 1,
        area_type: area_type
      )
      FactionWar.record_activity(
        state,
        'nexus_order',
        'johto',
        'Goldenrod Underground Grid',
        'basement_grid_hidden',
        threat_delta: 0,
        area_type: area_type
      )
      FactionWar.record_conflict(
        state,
        'team_rocket',
        'team_gold_dust',
        'Goldenrod Underground Warehouse Vault',
        'Rocket wants the stolen Director Card Key kept quiet while Gold Dust tries to steal the payment ledger.',
        intensity: 2,
        area_type: area_type
      )
      FactionWar.record_conflict(
        state,
        'team_gas',
        'team_moonlight',
        'Goldenrod Underground Switch Room',
        'Team Gas fumes scramble Moonlight basement relay timing and expose the switch puzzle pattern.',
        intensity: 2,
        area_type: area_type
      )

      story['current_act'] = 'act_14_radio_tower_director_rescue'
      event = goldenrod_underground_warehouse_event_result(location)
      story['event_history'] << event
      story['latest_event'] = event

      WorldLink.queue_message(
        state,
        'story_alert',
        'The Underground Warehouse confirms Rocket stole the Director Card Key, and the Radio Tower Director rescue route is now open.',
        source: 'johto_story',
        area_type: area_type
      )

      event
    end

    def goldenrod_underground_warehouse_cleared?(state)
      ensure_johto_story(state)['event_history'].any? { |event| event['event_id'] == GOLDENROD_UNDERGROUND_WAREHOUSE_EVENT_ID }
    end

    def goldenrod_underground_warehouse_event_result(location)
      {
        'status' => 'cleared',
        'event_id' => GOLDENROD_UNDERGROUND_WAREHOUSE_EVENT_ID,
        'location' => location.to_s,
        'region' => 'johto',
        'current_act' => 'act_14_radio_tower_director_rescue',
        'route_chain' => ['Goldenrod Underground', 'Goldenrod Underground Warehouse', 'Radio Tower Director Rescue'],
        'companions' => %w[red blue bill],
        'rivals' => %w[ava silver],
        'factions' => %w[team_rocket team_gold_dust team_gas team_moonlight nexus_order],
        'linked_events' => [
          WAREHOUSE_SWITCH_ROOM_EVENT_ID,
          RED_WAREHOUSE_BACKUP_EVENT_ID,
          BLUE_RADIO_TOWER_LOBBY_HOLD_EVENT_ID,
          BILL_DIRECTOR_CARD_TRACE_EVENT_ID,
          SILVER_WAREHOUSE_RIVAL_CLASH_EVENT_ID,
          AVA_UNDERGROUND_LEDGER_DECODE_EVENT_ID,
          ROCKET_DIRECTOR_CARD_THEFT_EVENT_ID,
          GOLD_DUST_WAREHOUSE_LEDGER_GRAB_EVENT_ID,
          TEAM_GAS_SWITCH_ROOM_FUMES_EVENT_ID,
          MOONLIGHT_BASEMENT_SIGNAL_RELAY_EVENT_ID,
          NEXUS_ORDER_BASEMENT_GRID_EVENT_ID,
          RADIO_TOWER_DIRECTOR_RESCUE_UNLOCKED_EVENT_ID
        ],
        'recovered_items' => ['Director Card Key', 'Rocket Elevator Route'],
        'battle_hook' => {
          'battle_id' => 'warehouse_switch_room_battle',
          'level_cap' => 29,
          'companion_rule' => 'red_tag_allowed_blue_holds_lobby',
          'enemy_trainers' => %w[rocket_warehouse_guard gold_dust_ledger_thief],
          'enemy_team_theme' => %w[normal poison steel dark]
        },
        'hidden_meta_signal' => 'nexus_order_basement_grid_unrevealed',
        'unlocks' => %w[radio_tower_director_rescue director_card_key rocket_elevator_route warehouse_digest_after_exit],
        'next_hook' => 'radio_tower_director_rescue'
      }
    end

    def complete_radio_tower_director_rescue(state, location: 'Goldenrod Underground Holding Room', area_type: 'villain_hideout')
      story = ensure_johto_story(state)
      return { 'status' => 'blocked_missing_johto_region_unlock', 'event_id' => RADIO_TOWER_DIRECTOR_RESCUE_EVENT_ID } unless johto_unlocked?(state)
      return { 'status' => 'blocked_missing_goldenrod_underground_warehouse', 'event_id' => RADIO_TOWER_DIRECTOR_RESCUE_EVENT_ID } unless goldenrod_underground_warehouse_cleared?(state)
      return { 'status' => 'already_cleared', 'event_id' => RADIO_TOWER_DIRECTOR_RESCUE_EVENT_ID } if radio_tower_director_rescue_cleared?(state)

      add_story_flag(state, 'FLAG_NEXUS_RADIO_TOWER_DIRECTOR_RESCUE')
      add_story_flag(state, 'FLAG_NEXUS_RADIO_TOWER_DIRECTOR_SAFE')
      add_story_flag(state, 'FLAG_NEXUS_CARD_KEY_SHUTTER_UNLOCK')
      add_story_flag(state, 'FLAG_NEXUS_RED_DIRECTOR_RESCUE_GUARD')
      add_story_flag(state, 'FLAG_NEXUS_BLUE_REJOINS_TOWER_CLIMB')
      add_story_flag(state, 'FLAG_NEXUS_BILL_TRANSMITTER_KEY_DECODE')
      add_story_flag(state, 'FLAG_NEXUS_SILVER_EXECUTIVE_STAIRS_PRESSURE')
      add_story_flag(state, 'FLAG_NEXUS_AVA_DIRECTOR_TESTIMONY_UPLOAD')
      add_story_flag(state, 'FLAG_NEXUS_ROCKET_DIRECTOR_IMPERSONATION_CONFIRMED')
      add_story_flag(state, 'FLAG_NEXUS_GOLD_DUST_RANSOM_LEDGER_RECOVERED')
      add_story_flag(state, 'FLAG_NEXUS_TEAM_GAS_TRANSMITTER_COOLANT_PRESSURE')
      add_story_flag(state, 'FLAG_NEXUS_MOONLIGHT_DIRECTOR_VOICEPRINT_ECHO')
      add_story_flag(state, 'FLAG_NEXUS_NEXUS_ORDER_DIRECTOR_SIGNAL_MASK')
      add_story_flag(state, 'FLAG_NEXUS_RADIO_TOWER_EXECUTIVE_FLOOR_UNLOCKED')

      [
        RADIO_TOWER_DIRECTOR_RESCUE_EVENT_ID,
        RADIO_TOWER_DIRECTOR_SAFE_EVENT_ID,
        CARD_KEY_SHUTTER_UNLOCK_EVENT_ID,
        RED_DIRECTOR_RESCUE_GUARD_EVENT_ID,
        BLUE_REJOINS_TOWER_CLIMB_EVENT_ID,
        BILL_TRANSMITTER_KEY_DECODE_EVENT_ID,
        SILVER_EXECUTIVE_STAIRS_PRESSURE_EVENT_ID,
        AVA_DIRECTOR_TESTIMONY_UPLOAD_EVENT_ID,
        ROCKET_DIRECTOR_IMPERSONATION_CONFIRMED_EVENT_ID,
        GOLD_DUST_RANSOM_LEDGER_EVENT_ID,
        TEAM_GAS_TRANSMITTER_COOLANT_EVENT_ID,
        MOONLIGHT_DIRECTOR_VOICEPRINT_EVENT_ID,
        NEXUS_ORDER_DIRECTOR_SIGNAL_MASK_EVENT_ID,
        RADIO_TOWER_EXECUTIVE_FLOOR_UNLOCKED_EVENT_ID
      ].each { |event_id| mark_cleared_event(story, event_id) }

      CompanionProgress.record_scene(
        state,
        'red',
        'director_rescue_guard',
        location: location,
        summary: 'Red guards the rescued Director while Antman takes the Card Key route back toward the Radio Tower shutter.',
        area_type: area_type
      )
      CompanionProgress.record_scene(
        state,
        'blue',
        'rejoins_tower_climb',
        location: 'Goldenrod Radio Tower Shutter',
        summary: 'Blue rejoins Antman and Red at the shutter, admitting the lobby is clear enough for the climb to become personal again.',
        area_type: area_type
      )
      CompanionProgress.record_scene(
        state,
        'bill',
        'transmitter_key_decode',
        location: location,
        summary: 'Bill decodes the Director testimony and confirms the Card Key opens a route toward Rocket orders inside the transmitter level.',
        area_type: area_type
      )

      record_rival_story_clue(
        state,
        'silver',
        'Goldenrod Radio Tower Executive Stairs',
        'Silver was seen forcing his way toward the executive stairs after learning Rocket used a fake Director voiceprint.',
        area_type,
        region: 'johto'
      )
      record_rival_story_clue(
        state,
        'ava',
        'Goldenrod Station Upload Kiosk',
        'Ava uploaded Director testimony from Goldenrod, warning WorldLink that Rocket impersonated the tower staff.',
        area_type,
        region: 'johto'
      )

      FactionWar.record_activity(
        state,
        'team_rocket',
        'johto',
        location,
        'director_impersonation_confirmed',
        threat_delta: 2,
        area_type: area_type
      )
      FactionWar.record_activity(
        state,
        'team_gold_dust',
        'johto',
        'Goldenrod Underground Holding Room',
        'ransom_ledger_recovered',
        threat_delta: 1,
        area_type: area_type
      )
      FactionWar.record_activity(
        state,
        'team_gas',
        'johto',
        'Goldenrod Radio Tower Transmitter Coolant',
        'transmitter_coolant_pressure',
        threat_delta: 1,
        area_type: area_type
      )
      FactionWar.record_activity(
        state,
        'team_moonlight',
        'johto',
        'Goldenrod Radio Tower Broadcast Booth',
        'director_voiceprint_echo',
        threat_delta: 1,
        area_type: area_type
      )
      FactionWar.record_activity(
        state,
        'nexus_order',
        'johto',
        'Goldenrod Radio Tower Director Signal',
        'director_signal_mask_hidden',
        threat_delta: 0,
        area_type: area_type
      )
      FactionWar.record_conflict(
        state,
        'team_rocket',
        'team_moonlight',
        'Goldenrod Radio Tower Broadcast Booth',
        'Rocket confirms the fake Director broadcast while Moonlight voiceprint echoes begin drifting out of their control.',
        intensity: 2,
        area_type: area_type
      )
      FactionWar.record_conflict(
        state,
        'team_rocket',
        'team_gold_dust',
        'Goldenrod Underground Holding Room',
        'Rocket tries to erase the ransom ledger while Gold Dust wants proof of who paid for the Director kidnapping.',
        intensity: 2,
        area_type: area_type
      )

      story['current_act'] = 'act_15_radio_tower_executive_floor'
      event = radio_tower_director_rescue_event_result(location)
      story['event_history'] << event
      story['latest_event'] = event

      WorldLink.queue_message(
        state,
        'story_alert',
        'The Director is safe, the Card Key opens the Radio Tower shutter, and Rocket executives are exposed on the upper floors.',
        source: 'johto_story',
        area_type: area_type
      )

      event
    end

    def radio_tower_director_rescue_cleared?(state)
      ensure_johto_story(state)['event_history'].any? { |event| event['event_id'] == RADIO_TOWER_DIRECTOR_RESCUE_EVENT_ID }
    end

    def radio_tower_director_rescue_event_result(location)
      {
        'status' => 'cleared',
        'event_id' => RADIO_TOWER_DIRECTOR_RESCUE_EVENT_ID,
        'location' => location.to_s,
        'region' => 'johto',
        'current_act' => 'act_15_radio_tower_executive_floor',
        'route_chain' => ['Goldenrod Underground Holding Room', 'Radio Tower Shutter', 'Radio Tower Executive Floor'],
        'companions' => %w[red blue bill],
        'rivals' => %w[ava silver],
        'factions' => %w[team_rocket team_gold_dust team_gas team_moonlight nexus_order],
        'linked_events' => [
          RADIO_TOWER_DIRECTOR_SAFE_EVENT_ID,
          CARD_KEY_SHUTTER_UNLOCK_EVENT_ID,
          RED_DIRECTOR_RESCUE_GUARD_EVENT_ID,
          BLUE_REJOINS_TOWER_CLIMB_EVENT_ID,
          BILL_TRANSMITTER_KEY_DECODE_EVENT_ID,
          SILVER_EXECUTIVE_STAIRS_PRESSURE_EVENT_ID,
          AVA_DIRECTOR_TESTIMONY_UPLOAD_EVENT_ID,
          ROCKET_DIRECTOR_IMPERSONATION_CONFIRMED_EVENT_ID,
          GOLD_DUST_RANSOM_LEDGER_EVENT_ID,
          TEAM_GAS_TRANSMITTER_COOLANT_EVENT_ID,
          MOONLIGHT_DIRECTOR_VOICEPRINT_EVENT_ID,
          NEXUS_ORDER_DIRECTOR_SIGNAL_MASK_EVENT_ID,
          RADIO_TOWER_EXECUTIVE_FLOOR_UNLOCKED_EVENT_ID
        ],
        'recovered_items' => ['Card Key', 'Director Testimony', 'Tower Shutter Route'],
        'battle_hook' => {
          'battle_id' => 'radio_tower_shutter_admin_battle',
          'level_cap' => 30,
          'companion_rule' => 'red_and_blue_tag_allowed_outside_gym',
          'enemy_trainers' => %w[rocket_shutter_admin moonlight_voiceprint_agent],
          'enemy_team_theme' => %w[poison dark psychic normal]
        },
        'hidden_meta_signal' => 'nexus_order_director_signal_mask_unrevealed',
        'unlocks' => %w[radio_tower_executive_floor card_key_shutter director_testimony tower_upper_floor_digest],
        'next_hook' => 'radio_tower_executive_floor'
      }
    end

    def complete_radio_tower_executive_floor(state, location: 'Goldenrod Radio Tower Executive Floor', result: 'won', area_type: 'villain_hideout')
      story = ensure_johto_story(state)
      return { 'status' => 'blocked_missing_johto_region_unlock', 'event_id' => RADIO_TOWER_EXECUTIVE_FLOOR_EVENT_ID } unless johto_unlocked?(state)
      return { 'status' => 'blocked_missing_radio_tower_director_rescue', 'event_id' => RADIO_TOWER_EXECUTIVE_FLOOR_EVENT_ID } unless radio_tower_director_rescue_cleared?(state)
      return { 'status' => 'already_cleared', 'event_id' => RADIO_TOWER_EXECUTIVE_FLOOR_EVENT_ID } if radio_tower_executive_floor_cleared?(state)

      add_story_flag(state, 'FLAG_NEXUS_RADIO_TOWER_EXECUTIVE_FLOOR')
      add_story_flag(state, 'FLAG_NEXUS_RADIO_TOWER_ADMIN_GAUNTLET')
      add_story_flag(state, 'FLAG_NEXUS_RED_BLUE_EXECUTIVE_TAG')
      add_story_flag(state, 'FLAG_NEXUS_BILL_TRANSMITTER_ADMIN_TRACE')
      add_story_flag(state, 'FLAG_NEXUS_SILVER_ROCKET_ADMIN_CHALLENGE')
      add_story_flag(state, 'FLAG_NEXUS_AVA_EXECUTIVE_SIGNAL_ARCHIVE')
      add_story_flag(state, 'FLAG_NEXUS_ROCKET_EXECUTIVE_BROADCAST_COMMAND')
      add_story_flag(state, 'FLAG_NEXUS_GOLD_DUST_EXECUTIVE_PAYOUT_LEDGER')
      add_story_flag(state, 'FLAG_NEXUS_TEAM_GAS_TRANSMITTER_OVERHEAT')
      add_story_flag(state, 'FLAG_NEXUS_MOONLIGHT_EXECUTIVE_VOICE_LOOP')
      add_story_flag(state, 'FLAG_NEXUS_NEXUS_ORDER_EXECUTIVE_SIGNAL_LATTICE')
      add_story_flag(state, 'FLAG_NEXUS_RADIO_TOWER_TRANSMITTER_SHUTDOWN_UNLOCKED')

      [
        RADIO_TOWER_EXECUTIVE_FLOOR_EVENT_ID,
        RADIO_TOWER_ADMIN_GAUNTLET_EVENT_ID,
        RED_BLUE_EXECUTIVE_TAG_EVENT_ID,
        BILL_TRANSMITTER_ADMIN_TRACE_EVENT_ID,
        SILVER_ROCKET_ADMIN_CHALLENGE_EVENT_ID,
        AVA_EXECUTIVE_SIGNAL_ARCHIVE_EVENT_ID,
        ROCKET_EXECUTIVE_BROADCAST_COMMAND_EVENT_ID,
        GOLD_DUST_EXECUTIVE_PAYOUT_LEDGER_EVENT_ID,
        TEAM_GAS_TRANSMITTER_OVERHEAT_EVENT_ID,
        MOONLIGHT_EXECUTIVE_VOICE_LOOP_EVENT_ID,
        NEXUS_ORDER_EXECUTIVE_SIGNAL_LATTICE_EVENT_ID,
        RADIO_TOWER_TRANSMITTER_SHUTDOWN_UNLOCKED_EVENT_ID
      ].each { |event_id| mark_cleared_event(story, event_id) }

      CompanionProgress.record_scene(
        state,
        'red',
        'executive_floor_tag_support',
        location: location,
        summary: 'Red fights beside Antman on the executive floor, keeping Rocket admins from turning the tower climb into a hostage wall.',
        area_type: area_type
      )
      CompanionProgress.record_scene(
        state,
        'blue',
        'executive_floor_tag_support',
        location: location,
        summary: 'Blue drops the rivalry long enough to tag in against Rocket admins, then warns Antman the transmitter room is the real trap.',
        area_type: area_type
      )
      CompanionProgress.record_scene(
        state,
        'bill',
        'transmitter_admin_trace',
        location: location,
        summary: 'Bill traces admin command codes from the executive floor into a transmitter shutdown path above the broadcast booth.',
        area_type: area_type
      )

      record_rival_story_clue(
        state,
        'silver',
        location,
        'Silver challenged a Rocket admin on the executive floor, furious that the broadcast orders still pointed back to Giovanni.',
        area_type,
        region: 'johto'
      )
      record_rival_story_clue(
        state,
        'ava',
        'Goldenrod Radio Tower Signal Archive',
        'Ava captured an executive signal archive from Goldenrod before Rocket could wipe the admin command records.',
        area_type,
        region: 'johto'
      )

      FactionWar.record_activity(
        state,
        'team_rocket',
        'johto',
        location,
        'executive_broadcast_command',
        threat_delta: 3,
        area_type: area_type
      )
      FactionWar.record_activity(
        state,
        'team_gold_dust',
        'johto',
        'Goldenrod Radio Tower Executive Accounts',
        'executive_payout_ledger',
        threat_delta: 1,
        area_type: area_type
      )
      FactionWar.record_activity(
        state,
        'team_gas',
        'johto',
        'Goldenrod Radio Tower Transmitter Hall',
        'transmitter_overheat',
        threat_delta: 1,
        area_type: area_type
      )
      FactionWar.record_activity(
        state,
        'team_moonlight',
        'johto',
        'Goldenrod Radio Tower Broadcast Booth',
        'executive_voice_loop',
        threat_delta: 1,
        area_type: area_type
      )
      FactionWar.record_activity(
        state,
        'nexus_order',
        'johto',
        'Goldenrod Radio Tower Signal Lattice',
        'executive_signal_lattice_hidden',
        threat_delta: 0,
        area_type: area_type
      )
      FactionWar.record_conflict(
        state,
        'team_rocket',
        'team_gold_dust',
        location,
        'Rocket admins try to erase payout records while Gold Dust collectors demand their cut of the broadcast takeover.',
        intensity: 2,
        area_type: area_type
      )
      FactionWar.record_conflict(
        state,
        'team_gas',
        'team_moonlight',
        'Goldenrod Radio Tower Transmitter Hall',
        'Team Gas transmitter overheat breaks Moonlight voice loops loose from the executive broadcast script.',
        intensity: 2,
        area_type: area_type
      )

      story['current_act'] = 'act_16_radio_tower_transmitter_shutdown'
      event = radio_tower_executive_floor_event_result(location, result)
      story['event_history'] << event
      story['latest_event'] = event

      WorldLink.queue_message(
        state,
        'story_alert',
        'Rocket admins are beaten on the executive floor, but the transmitter is still carrying their command signal above Goldenrod.',
        source: 'johto_story',
        area_type: area_type
      )

      event
    end

    def radio_tower_executive_floor_cleared?(state)
      ensure_johto_story(state)['event_history'].any? { |event| event['event_id'] == RADIO_TOWER_EXECUTIVE_FLOOR_EVENT_ID }
    end

    def radio_tower_executive_floor_event_result(location, result)
      {
        'status' => 'cleared',
        'event_id' => RADIO_TOWER_EXECUTIVE_FLOOR_EVENT_ID,
        'battle_id' => 'radio_tower_executive_floor',
        'location' => location.to_s,
        'region' => 'johto',
        'current_act' => 'act_16_radio_tower_transmitter_shutdown',
        'result' => result.to_s,
        'route_chain' => ['Radio Tower Shutter', 'Radio Tower Executive Floor', 'Radio Tower Transmitter Hall'],
        'companions' => %w[red blue bill],
        'rivals' => %w[ava silver],
        'factions' => %w[team_rocket team_gold_dust team_gas team_moonlight nexus_order],
        'linked_events' => [
          RADIO_TOWER_ADMIN_GAUNTLET_EVENT_ID,
          RED_BLUE_EXECUTIVE_TAG_EVENT_ID,
          BILL_TRANSMITTER_ADMIN_TRACE_EVENT_ID,
          SILVER_ROCKET_ADMIN_CHALLENGE_EVENT_ID,
          AVA_EXECUTIVE_SIGNAL_ARCHIVE_EVENT_ID,
          ROCKET_EXECUTIVE_BROADCAST_COMMAND_EVENT_ID,
          GOLD_DUST_EXECUTIVE_PAYOUT_LEDGER_EVENT_ID,
          TEAM_GAS_TRANSMITTER_OVERHEAT_EVENT_ID,
          MOONLIGHT_EXECUTIVE_VOICE_LOOP_EVENT_ID,
          NEXUS_ORDER_EXECUTIVE_SIGNAL_LATTICE_EVENT_ID,
          RADIO_TOWER_TRANSMITTER_SHUTDOWN_UNLOCKED_EVENT_ID
        ],
        'battle_hook' => {
          'battle_id' => 'radio_tower_admin_gauntlet',
          'level_cap' => 31,
          'companion_rule' => 'red_and_blue_tag_allowed_outside_gym',
          'enemy_trainers' => %w[rocket_broadcast_admin rocket_signal_admin],
          'enemy_team_theme' => %w[poison dark electric normal]
        },
        'hidden_meta_signal' => 'nexus_order_executive_signal_lattice_unrevealed',
        'unlocks' => %w[radio_tower_transmitter_shutdown admin_command_codes executive_floor_digest_after_exit],
        'next_hook' => 'radio_tower_transmitter_shutdown'
      }
    end
  end
end
