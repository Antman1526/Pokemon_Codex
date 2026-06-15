# frozen_string_literal: true

module NexusRed
  module KantoStory
    BROCK_REWARD_ID = 'brock_red_field_kit'
    MUSEUM_EVENT_ID = 'pewter_rocket_fossil_scan_theft'
    MT_MOON_EVENT_ID = 'mt_moon_rocket_moon_stone_operation'
    GOLD_DUST_INVOICE_EVENT_ID = 'gold_dust_invoice_hint'
    AVA_CLEFAIRY_EVENT_ID = 'ava_clefairy_night_notes'
    NUGGET_BRIDGE_EVENT_ID = 'nugget_bridge_world_circuit_qualifier'
    MISTY_EVENT_ID = 'misty_battle'
    BILL_EVENT_ID = 'bill_storage_metadata_anomaly'
    BILL_STORAGE_ANOMALY_ID = 'route_25_storage_metadata_echo'
    SS_ANNE_EVENT_ID = 'ss_anne_foreign_trainers'
    BLUE_SS_ANNE_EVENT_ID = 'blue_ss_anne_battle'
    ROCKET_MANIFEST_EVENT_ID = 'rocket_smuggling_manifest'
    VERMILION_POWER_EVENT_ID = 'vermilion_power_sabotage'
    ROCKET_GAS_POWER_EVENT_ID = 'rocket_gas_power_sabotage'
    TEAM_GAS_DEBUT_EVENT_ID = 'team_gas_kanto_debut'
    BILL_POWER_GRID_EVENT_ID = 'bill_power_grid_decode'
    LT_SURGE_EVENT_ID = 'lt_surge_battle'
    ROUTE_11_EVENT_ID = 'route_11_handoff'
    DIGLETT_CAVE_EVENT_ID = 'diglett_cave_detour'
    ROCKET_GOLD_DUST_CAVE_EVENT_ID = 'rocket_gold_dust_cave_argument'
    ROUTE_2_EAST_LAB_EVENT_ID = 'route_2_east_field_lab'
    ROCKET_MOONLIGHT_SLEEP_EVENT_ID = 'rocket_moonlight_sleep_signal'
    ROUTE_9_EVENT_ID = 'route_9_rock_tunnel_approach'
    TEAM_MOONLIGHT_ROUTE_9_EVENT_ID = 'team_moonlight_route_9_debut'
    ROCKET_ROUTE_9_CACHE_EVENT_ID = 'rocket_route_9_supply_cache'
    ROCK_TUNNEL_EVENT_ID = 'rock_tunnel_interior'
    BILL_LAVENDER_ECHO_EVENT_ID = 'bill_lavender_echo_trace'
    TEAM_MOONLIGHT_CAVE_EVENT_ID = 'team_moonlight_cave_pressure'
    ROCKET_DARK_CACHE_EVENT_ID = 'rocket_dark_cache'
    FLASH_LANTERN_EVENT_ID = 'flash_lantern_needed'
    LAVENDER_EXIT_EVENT_ID = 'lavender_exit_path_unlocked'

    module_function

    def ensure_kanto_story(state)
      state['kanto_story'] ||= {
        'current_act' => 'act_1_pallet_to_pewter',
        'cleared_events' => [],
        'event_history' => [],
        'reward_history' => [],
        'latest_reward' => nil
      }
    end

    def complete_brock(state, location: 'Pewter Gym', area_type: 'route')
      story = ensure_kanto_story(state)
      return already_applied_result(state) if brock_rewards_applied?(state)

      add_story_flag(state, 'boulder_badge_obtained')
      add_story_flag(state, 'FLAG_NEXUS_BOULDER_BADGE')
      add_story_flag(state, 'FLAG_NEXUS_PEWTER_ROCKET_ALERT')
      mark_cleared_event(story, 'brock_battle')

      GameplayOptions.unlock_qol(state, 'after_brock')
      CenterMartServices.unlock_mart_tier(state, 'after_first_badge')
      PortablePC.unlock(state, source: 'Brock and Red field kit', access_level: 'lite', area_type: area_type)
      FieldHealing.unlock(
        state,
        source: 'Mom and Brock care kit',
        charges: field_healing_charges_for(state),
        area_type: area_type
      )
      CompanionProgress.record_scene(
        state,
        'red',
        'post_brock_field_kit',
        location: location,
        summary: 'Red helps Antman tune the field kit after the Boulder Badge.',
        area_type: area_type
      )
      CompanionProgress.record_scene(
        state,
        'brock',
        'post_gym_respect',
        location: location,
        summary: 'Brock respects Antman as a traveling Trainer and offers practical care advice.',
        area_type: area_type
      )

      story['current_act'] = 'act_2_pewter_to_cerulean'
      reward = reward_result(state, location)
      story['reward_history'] << reward
      story['latest_reward'] = reward
      reward
    end

    def brock_rewards_applied?(state)
      ensure_kanto_story(state)['reward_history'].any? { |reward| reward['reward_id'] == BROCK_REWARD_ID }
    end

    def complete_pewter_museum_anomaly(state, location: 'Pewter Museum Service Tunnel', area_type: 'villain_hideout', partner_id: 'red')
      story = ensure_kanto_story(state)
      return { 'status' => 'blocked_missing_boulder_badge', 'event_id' => MUSEUM_EVENT_ID } unless has_story_flag?(state, 'boulder_badge_obtained')
      return { 'status' => 'already_cleared', 'event_id' => MUSEUM_EVENT_ID } if museum_anomaly_cleared?(state)

      add_story_flag(state, 'FLAG_NEXUS_MUSEUM_ROCKET_EVENT_DONE')
      mark_cleared_event(story, MUSEUM_EVENT_ID)
      FactionWar.record_activity(
        state,
        'team_rocket',
        'kanto',
        location,
        'fossil_scan_theft',
        threat_delta: 2,
        area_type: area_type
      )
      FactionWar.record_conflict(
        state,
        'team_rocket',
        'team_phoenix',
        location,
        'stolen fossil scanner carries a burnt resurrection cipher',
        intensity: 1,
        area_type: area_type
      )
      CompanionProgress.record_scene(
        state,
        partner_id,
        'pewter_museum_backup',
        location: location,
        summary: "#{companion_display_name(partner_id)} covers Antman during the museum service tunnel raid.",
        area_type: area_type
      )
      WorldLink.queue_message(
        state,
        'story_alert',
        'The Pewter fossil scanner exposed a Rocket theft and a burnt cipher tied to a future faction.',
        source: 'kanto_story',
        area_type: area_type
      )

      event = museum_event_result(location, partner_id)
      story['event_history'] << event
      story['latest_event'] = event
      event
    end

    def museum_anomaly_cleared?(state)
      ensure_kanto_story(state)['event_history'].any? { |event| event['event_id'] == MUSEUM_EVENT_ID }
    end

    def complete_mt_moon_operation(state, location: 'Mt. Moon Depths', area_type: 'cave', rival_id: 'ava')
      story = ensure_kanto_story(state)
      return { 'status' => 'blocked_missing_museum_clue', 'event_id' => MT_MOON_EVENT_ID } unless museum_anomaly_cleared?(state)
      return { 'status' => 'already_cleared', 'event_id' => MT_MOON_EVENT_ID } if mt_moon_operation_cleared?(state)

      add_story_flag(state, 'FLAG_NEXUS_MT_MOON_ROCKET_OPERATION_DONE')
      add_story_flag(state, 'FLAG_NEXUS_GOLD_DUST_INVOICE_HINT')
      mark_cleared_event(story, MT_MOON_EVENT_ID)
      mark_cleared_event(story, GOLD_DUST_INVOICE_EVENT_ID)
      mark_cleared_event(story, AVA_CLEFAIRY_EVENT_ID)
      FactionWar.record_activity(
        state,
        'team_rocket',
        'kanto',
        location,
        'moon_stone_extraction',
        threat_delta: 2,
        area_type: area_type
      )
      FactionWar.record_activity(
        state,
        'team_gold_dust',
        'kanto',
        location,
        'invoice_laundering_hint',
        threat_delta: 1,
        area_type: area_type
      )
      FactionWar.record_conflict(
        state,
        'team_rocket',
        'team_gold_dust',
        location,
        'Moon Stone extraction invoice double-cross',
        intensity: 2,
        area_type: area_type
      )
      record_rival_story_clue(
        state,
        rival_id,
        location,
        'Ava found Clefairy night notes beside a gold-stamped invoice.',
        area_type
      )
      WorldLink.queue_message(
        state,
        'story_alert',
        'Mt. Moon linked Rocket Moon Stone extraction to a gold-stamped invoice trail.',
        source: 'kanto_story',
        area_type: area_type
      )

      event = mt_moon_event_result(location, rival_id)
      story['event_history'] << event
      story['latest_event'] = event
      event
    end

    def mt_moon_operation_cleared?(state)
      ensure_kanto_story(state)['event_history'].any? { |event| event['event_id'] == MT_MOON_EVENT_ID }
    end

    def gold_dust_invoice_found?(state)
      ensure_kanto_story(state)['cleared_events'].include?(GOLD_DUST_INVOICE_EVENT_ID)
    end

    def complete_nugget_bridge_qualifier(state, location: 'Nugget Bridge', area_type: 'route', rival_ids: %w[blue ava dax])
      story = ensure_kanto_story(state)
      return { 'status' => 'blocked_missing_mt_moon_clear', 'event_id' => NUGGET_BRIDGE_EVENT_ID } unless mt_moon_operation_cleared?(state)
      return { 'status' => 'already_cleared', 'event_id' => NUGGET_BRIDGE_EVENT_ID } if nugget_bridge_qualifier_cleared?(state)

      add_story_flag(state, 'FLAG_NEXUS_NUGGET_BRIDGE_WORLD_CIRCUIT')
      add_story_flag(state, 'FLAG_NEXUS_CERULEAN_BRIDGE_CRISIS_DONE')
      mark_cleared_event(story, NUGGET_BRIDGE_EVENT_ID)
      FactionWar.record_activity(
        state,
        'team_rocket',
        'kanto',
        location,
        'bridge_recruitment_probe',
        threat_delta: 1,
        area_type: area_type
      )
      rival_ids.each do |rival_id|
        record_rival_story_clue(
          state,
          rival_id,
          location,
          "#{rival_display_name(rival_id)} cleared the Nugget Bridge World Circuit qualifier.",
          area_type
        )
      end
      CompanionProgress.activate_companion(
        state,
        'misty',
        location: 'Cerulean City',
        reason: 'she is investigating the bridge crisis before the gym battle',
        following: false,
        area_type: area_type
      )
      CompanionProgress.record_scene(
        state,
        'misty',
        'cerulean_bridge_crisis',
        location: location,
        summary: 'Misty challenges Antman to prove the bridge crisis is handled before Route 25.',
        area_type: area_type
      )
      WorldLink.queue_message(
        state,
        'story_alert',
        "Nugget Bridge became Antman's first World Circuit qualifier and exposed a Rocket recruitment probe.",
        source: 'kanto_story',
        area_type: area_type
      )

      event = nugget_bridge_event_result(location, rival_ids)
      story['event_history'] << event
      story['latest_event'] = event
      event
    end

    def nugget_bridge_qualifier_cleared?(state)
      ensure_kanto_story(state)['event_history'].any? { |event| event['event_id'] == NUGGET_BRIDGE_EVENT_ID }
    end

    def complete_misty_battle(state, gym_location: 'Cerulean Gym', join_location: 'Route 25', area_type: 'route')
      story = ensure_kanto_story(state)
      return { 'status' => 'blocked_missing_nugget_bridge_clear', 'event_id' => MISTY_EVENT_ID } unless nugget_bridge_qualifier_cleared?(state)
      return { 'status' => 'already_cleared', 'event_id' => MISTY_EVENT_ID } if misty_battle_cleared?(state)

      add_story_flag(state, 'cascade_badge_obtained')
      add_story_flag(state, 'FLAG_NEXUS_CASCADE_BADGE')
      add_story_flag(state, 'FLAG_NEXUS_MISTY_ROUTE25_COMPANION')
      add_story_flag(state, 'FLAG_NEXUS_REMATCH_BOARD_TIER_1')
      mark_cleared_event(story, MISTY_EVENT_ID)
      EncounterWorld.unlock_fishing_rod(state, 'old_rod', source: 'Misty Route 25 camp', area_type: area_type)
      CompanionProgress.record_scene(
        state,
        'misty',
        'post_gym_respect',
        location: gym_location,
        summary: 'Misty accepts Antman as a serious challenger after the Cascade Badge battle.',
        area_type: area_type
      )
      CompanionProgress.activate_companion(
        state,
        'misty',
        location: join_location,
        reason: 'joined Antman after the Route 25 scene',
        following: true,
        area_type: area_type
      )
      CompanionProgress.record_scene(
        state,
        'misty',
        'route_25_companion_entry',
        location: join_location,
        summary: 'Misty joins Antman as a recurring travel companion on Route 25.',
        area_type: area_type
      )
      WorldLink.queue_message(
        state,
        'story_alert',
        'Misty joined the travel party after the Cascade Badge and Route 25 scene.',
        source: 'kanto_story',
        area_type: area_type
      )

      story['current_act'] = 'act_3_cerulean_to_vermilion'
      event = misty_event_result(gym_location, join_location)
      story['event_history'] << event
      story['latest_event'] = event
      event
    end

    def misty_battle_cleared?(state)
      ensure_kanto_story(state)['event_history'].any? { |event| event['event_id'] == MISTY_EVENT_ID }
    end

    def complete_bill_storage_anomaly(state, location: "Bill's House", area_type: 'route')
      story = ensure_kanto_story(state)
      return { 'status' => 'blocked_missing_misty_clear', 'event_id' => BILL_EVENT_ID } unless misty_battle_cleared?(state)
      return { 'status' => 'already_cleared', 'event_id' => BILL_EVENT_ID } if bill_storage_anomaly_cleared?(state)

      add_story_flag(state, 'FLAG_NEXUS_BILL_STORAGE_METADATA_ANOMALY')
      add_story_flag(state, 'FLAG_NEXUS_ROUTE25_SYSTEMS_HOOK')
      mark_cleared_event(story, BILL_EVENT_ID)
      CompanionProgress.activate_companion(
        state,
        'bill',
        location: location,
        reason: 'decoded an impossible storage metadata echo',
        following: false,
        area_type: area_type
      )
      CompanionProgress.record_scene(
        state,
        'bill',
        'storage_intro',
        location: location,
        summary: 'Bill shows Antman how the storage network is carrying impossible route metadata.',
        area_type: area_type
      )
      CompanionProgress.record_scene(
        state,
        'bill',
        'route_25_systems_hook',
        location: location,
        summary: 'Bill links Route 25 storage echoes to the wider region network mystery.',
        area_type: area_type
      )
      FactionWar.record_activity(
        state,
        'team_rocket',
        'kanto',
        location,
        'storage_metadata_probe',
        threat_delta: 1,
        area_type: area_type
      )
      anomaly = storage_anomaly_result(location)
      storage_anomalies(state) << anomaly
      WorldLink.queue_message(
        state,
        'story_alert',
        'Bill found a storage metadata echo that points beyond Kanto.',
        source: 'kanto_story',
        area_type: area_type
      )

      event = bill_event_result(location, anomaly)
      story['event_history'] << event
      story['latest_event'] = event
      event
    end

    def bill_storage_anomaly_cleared?(state)
      ensure_kanto_story(state)['event_history'].any? { |event| event['event_id'] == BILL_EVENT_ID }
    end

    def complete_ss_anne_manifest(state, location: 'S.S. Anne', area_type: 'route', rival_id: 'blue')
      story = ensure_kanto_story(state)
      return { 'status' => 'blocked_missing_bill_anomaly', 'event_id' => SS_ANNE_EVENT_ID } unless bill_storage_anomaly_cleared?(state)
      return { 'status' => 'already_cleared', 'event_id' => SS_ANNE_EVENT_ID } if ss_anne_manifest_cleared?(state)

      add_story_flag(state, 'FLAG_NEXUS_SS_ANNE_FOREIGN_TRAINERS')
      add_story_flag(state, 'FLAG_NEXUS_BLUE_SS_ANNE_BATTLE')
      add_story_flag(state, 'FLAG_NEXUS_ROCKET_SMUGGLING_MANIFEST')
      add_story_flag(state, 'FLAG_NEXUS_VERMILION_SURGE_SETUP')
      mark_cleared_event(story, SS_ANNE_EVENT_ID)
      mark_cleared_event(story, BLUE_SS_ANNE_EVENT_ID)
      mark_cleared_event(story, ROCKET_MANIFEST_EVENT_ID)
      FactionWar.record_activity(
        state,
        'team_rocket',
        'kanto',
        location,
        'smuggling_manifest',
        threat_delta: 2,
        area_type: area_type
      )
      record_rival_story_clue(
        state,
        rival_id,
        location,
        "#{rival_display_name(rival_id)} challenged Antman aboard the S.S. Anne and found the Rocket smuggling manifest.",
        area_type
      )
      CompanionProgress.record_scene(
        state,
        'misty',
        'ss_anne_manifest',
        location: location,
        summary: 'Misty spots tide-route inconsistencies in the manifest.',
        area_type: area_type
      )
      CompanionProgress.record_scene(
        state,
        'red',
        'red_worldlink_mt_moon_note',
        location: location,
        summary: 'Red matches the S.S. Anne manifest against the old Mt. Moon note.',
        area_type: area_type
      )
      WorldLink.queue_message(
        state,
        'story_alert',
        'S.S. Anne linked foreign Trainer traffic to a Rocket smuggling manifest bound for Vermilion.',
        source: 'kanto_story',
        area_type: area_type
      )

      event = ss_anne_event_result(location, rival_id)
      story['event_history'] << event
      story['latest_event'] = event
      event
    end

    def ss_anne_manifest_cleared?(state)
      ensure_kanto_story(state)['event_history'].any? { |event| event['event_id'] == SS_ANNE_EVENT_ID }
    end

    def rocket_manifest_found?(state)
      ensure_kanto_story(state)['cleared_events'].include?(ROCKET_MANIFEST_EVENT_ID)
    end

    def complete_vermilion_power_sabotage(state, location: 'Vermilion Power Yard', area_type: 'route')
      story = ensure_kanto_story(state)
      return { 'status' => 'blocked_missing_ss_anne_manifest', 'event_id' => VERMILION_POWER_EVENT_ID } unless ss_anne_manifest_cleared?(state)
      return { 'status' => 'already_cleared', 'event_id' => VERMILION_POWER_EVENT_ID } if vermilion_power_sabotage_cleared?(state)

      add_story_flag(state, 'FLAG_NEXUS_VERMILION_POWER_SABOTAGE_REACHED')
      add_story_flag(state, 'FLAG_NEXUS_ROCKET_GAS_POWER_SABOTAGE')
      add_story_flag(state, 'FLAG_NEXUS_TEAM_GAS_KANTO_DEBUT')
      add_story_flag(state, 'FLAG_NEXUS_RED_MISTY_SURGE_PREP')
      add_story_flag(state, 'FLAG_NEXUS_BILL_POWER_GRID_DECODE')
      add_story_flag(state, 'FLAG_NEXUS_SURGE_GYM_BATTLE_UNLOCKED')
      mark_cleared_event(story, VERMILION_POWER_EVENT_ID)
      mark_cleared_event(story, ROCKET_GAS_POWER_EVENT_ID)
      mark_cleared_event(story, TEAM_GAS_DEBUT_EVENT_ID)
      mark_cleared_event(story, BILL_POWER_GRID_EVENT_ID)
      FactionWar.record_activity(
        state,
        'team_rocket',
        'kanto',
        location,
        'power_room_break_in',
        threat_delta: 1,
        area_type: area_type
      )
      FactionWar.record_activity(
        state,
        'team_gas',
        'kanto',
        location,
        'poison_exhaust_grid_sabotage',
        threat_delta: 2,
        area_type: area_type
      )
      FactionWar.record_conflict(
        state,
        'team_rocket',
        'team_gas',
        location,
        'Rocket opened the power room, but Team Gas poisoned the grid and stole the operation',
        intensity: 2,
        area_type: area_type
      )
      CompanionProgress.record_scene(
        state,
        'red',
        'surge_prep',
        location: location,
        summary: 'Red trains Antman on clean switching before Surge.',
        area_type: area_type
      )
      CompanionProgress.record_scene(
        state,
        'misty',
        'surge_prep',
        location: location,
        summary: 'Misty clears harbor vents and drills paralysis counterplay.',
        area_type: area_type
      )
      CompanionProgress.record_scene(
        state,
        'bill',
        'power_grid_decode',
        location: location,
        summary: 'Bill decodes the power-grid relay loop tied to the S.S. Anne manifest.',
        area_type: area_type
      )
      WorldLink.queue_message(
        state,
        'story_alert',
        'Team Gas debuted in Kanto by hijacking Rocket power sabotage behind Lt. Surge\'s gym.',
        source: 'kanto_story',
        area_type: area_type
      )

      event = vermilion_power_event_result(location)
      story['event_history'] << event
      story['latest_event'] = event
      event
    end

    def vermilion_power_sabotage_cleared?(state)
      ensure_kanto_story(state)['event_history'].any? { |event| event['event_id'] == VERMILION_POWER_EVENT_ID }
    end

    def complete_lt_surge_battle(state, location: 'Vermilion Gym', area_type: 'route')
      story = ensure_kanto_story(state)
      return { 'status' => 'blocked_missing_vermilion_sabotage', 'event_id' => LT_SURGE_EVENT_ID } unless vermilion_power_sabotage_cleared?(state)
      return { 'status' => 'already_cleared', 'event_id' => LT_SURGE_EVENT_ID } if lt_surge_battle_cleared?(state)

      add_story_flag(state, 'thunder_badge_obtained')
      add_story_flag(state, 'FLAG_NEXUS_THUNDER_BADGE')
      add_story_flag(state, 'FLAG_NEXUS_LT_SURGE_BATTLE')
      add_story_flag(state, 'FLAG_NEXUS_ROUTE11_PATH_UNLOCKED')
      add_story_flag(state, 'FLAG_NEXUS_VS_SEEKER_UNLOCKED')
      mark_cleared_event(story, LT_SURGE_EVENT_ID)
      EncounterWorld.unlock_fishing_rod(state, 'good_rod', source: 'Lt. Surge Route 11 clearance', area_type: area_type)
      CompanionProgress.record_scene(
        state,
        'red',
        'post_surge_route11',
        location: location,
        summary: 'Red stays with Antman as the Thunder Badge opens the road east.',
        area_type: area_type
      )
      CompanionProgress.record_scene(
        state,
        'misty',
        'surge_respect_scene',
        location: location,
        summary: "Misty logs Surge's respect beat and warns that Rocket will adapt.",
        area_type: area_type
      )
      WorldLink.queue_message(
        state,
        'story_alert',
        'Antman earned the Thunder Badge, unlocked the Good Rod and VS Seeker lead, and opened Route 11.',
        source: 'kanto_story',
        area_type: area_type
      )

      story['current_act'] = 'act_4_rock_tunnel_celadon_lavender'
      event = lt_surge_event_result(location)
      story['event_history'] << event
      story['latest_event'] = event
      event
    end

    def lt_surge_battle_cleared?(state)
      ensure_kanto_story(state)['event_history'].any? { |event| event['event_id'] == LT_SURGE_EVENT_ID }
    end

    def complete_route_11_handoff(state, location: 'Route 11', area_type: 'route')
      story = ensure_kanto_story(state)
      return { 'status' => 'blocked_missing_thunder_badge', 'event_id' => ROUTE_11_EVENT_ID } unless lt_surge_battle_cleared?(state)
      return { 'status' => 'already_cleared', 'event_id' => ROUTE_11_EVENT_ID } if route_11_handoff_cleared?(state)

      add_story_flag(state, 'FLAG_NEXUS_ROUTE11_REACHED')
      add_story_flag(state, 'FLAG_NEXUS_RED_ROUTE11_EASTBOUND')
      add_story_flag(state, 'FLAG_NEXUS_MISTY_ROUTE11_FAREWELL')
      add_story_flag(state, 'FLAG_NEXUS_BILL_ROUTE11_SIGNAL_DECODE')
      add_story_flag(state, 'FLAG_NEXUS_ROCKET_GAS_ROUTE11_FALLOUT')
      add_story_flag(state, 'FLAG_NEXUS_SNORLAX_ROADBLOCK_TEASED')
      mark_cleared_event(story, ROUTE_11_EVENT_ID)
      FactionWar.record_activity(
        state,
        'team_rocket',
        'kanto',
        location,
        'post_surge_blame_shift',
        threat_delta: 1,
        area_type: area_type
      )
      FactionWar.record_activity(
        state,
        'team_gas',
        'kanto',
        location,
        'route_11_fallout',
        threat_delta: 1,
        area_type: area_type
      )
      CompanionProgress.record_scene(
        state,
        'red',
        'route_11_eastbound',
        location: location,
        summary: 'Red stays with Antman as the journey turns east from Vermilion.',
        area_type: area_type
      )
      CompanionProgress.record_scene(
        state,
        'misty',
        'route_11_farewell',
        location: location,
        summary: 'Misty rotates to water-route support after the Route 11 checkpoint.',
        area_type: area_type
      )
      CompanionProgress.record_scene(
        state,
        'bill',
        'route_11_signal_decode',
        location: location,
        summary: 'Bill decodes a Nexus pulse from the Route 11 relay pole.',
        area_type: area_type
      )
      WorldLink.queue_message(
        state,
        'story_alert',
        'Route 11 opened after Surge, but a Snorlax roadblock is forcing the Diglett Cave detour.',
        source: 'kanto_story',
        area_type: area_type
      )

      event = route_11_event_result(location)
      story['event_history'] << event
      story['latest_event'] = event
      event
    end

    def route_11_handoff_cleared?(state)
      ensure_kanto_story(state)['event_history'].any? { |event| event['event_id'] == ROUTE_11_EVENT_ID }
    end

    def complete_diglett_cave_detour(state, location: "Diglett's Cave", area_type: 'cave')
      story = ensure_kanto_story(state)
      return { 'status' => 'blocked_missing_route_11_handoff', 'event_id' => DIGLETT_CAVE_EVENT_ID } unless route_11_handoff_cleared?(state)
      return { 'status' => 'already_cleared', 'event_id' => DIGLETT_CAVE_EVENT_ID } if diglett_cave_detour_cleared?(state)

      add_story_flag(state, 'FLAG_NEXUS_DIGLETT_CAVE_DETOUR_REACHED')
      add_story_flag(state, 'FLAG_NEXUS_RED_DIGLETT_CAVE_GUARD')
      add_story_flag(state, 'FLAG_NEXUS_BILL_DIGLETT_CAVE_RELAY_MAP')
      add_story_flag(state, 'FLAG_NEXUS_ROCKET_GOLD_DUST_CAVE_ARGUMENT')
      add_story_flag(state, 'FLAG_NEXUS_SNORLAX_ROUTE12_BLOCK_CONFIRMED')
      add_story_flag(state, 'FLAG_NEXUS_ECHO_FLUTE_LEAD_SEEN')
      mark_cleared_event(story, DIGLETT_CAVE_EVENT_ID)
      mark_cleared_event(story, ROCKET_GOLD_DUST_CAVE_EVENT_ID)
      FactionWar.record_activity(
        state,
        'team_rocket',
        'kanto',
        location,
        'stolen_cave_survey_crates',
        threat_delta: 1,
        area_type: area_type
      )
      FactionWar.record_activity(
        state,
        'team_gold_dust',
        'kanto',
        location,
        'cave_survey_claim',
        threat_delta: 1,
        area_type: area_type
      )
      FactionWar.record_conflict(
        state,
        'team_rocket',
        'team_gold_dust',
        location,
        'stolen Diglett Cave survey crates expose the next resource dispute',
        intensity: 1,
        area_type: area_type
      )
      CompanionProgress.record_scene(
        state,
        'red',
        'diglett_cave_guard',
        location: location,
        summary: 'Red keeps Antman moving through the cave detour instead of quick-jumping the route.',
        area_type: area_type
      )
      CompanionProgress.record_scene(
        state,
        'bill',
        'diglett_cave_relay_map',
        location: location,
        summary: 'Bill maps a Nexus relay under Diglett Cave and marks the Echo Flute lead.',
        area_type: area_type
      )
      WorldLink.queue_message(
        state,
        'story_alert',
        'Diglett Cave confirmed the Snorlax block and exposed the Echo Flute as the next waking lead.',
        source: 'kanto_story',
        area_type: area_type
      )

      event = diglett_cave_event_result(location)
      story['event_history'] << event
      story['latest_event'] = event
      event
    end

    def diglett_cave_detour_cleared?(state)
      ensure_kanto_story(state)['event_history'].any? { |event| event['event_id'] == DIGLETT_CAVE_EVENT_ID }
    end

    def complete_route_2_east_field_lab(state, location: 'Route 2 East Field Lab', area_type: 'route')
      story = ensure_kanto_story(state)
      return { 'status' => 'blocked_missing_diglett_cave_detour', 'event_id' => ROUTE_2_EAST_LAB_EVENT_ID } unless diglett_cave_detour_cleared?(state)
      return { 'status' => 'already_cleared', 'event_id' => ROUTE_2_EAST_LAB_EVENT_ID } if route_2_east_field_lab_cleared?(state)

      add_story_flag(state, 'FLAG_NEXUS_ROUTE2_EAST_FIELD_LAB_REACHED')
      add_story_flag(state, 'FLAG_NEXUS_RED_ROUTE2_EAST_EXIT')
      add_story_flag(state, 'FLAG_NEXUS_BILL_ECHO_FLUTE_DECODER')
      add_story_flag(state, 'FLAG_NEXUS_OAK_AIDE_FIELD_TOOL_BRIEF')
      add_story_flag(state, 'FLAG_NEXUS_ROCKET_MOONLIGHT_SLEEP_SIGNAL')
      add_story_flag(state, 'FLAG_NEXUS_LAVENDER_SIGNAL_PATH_TEASED')
      add_story_flag(state, 'FLAG_NEXUS_ROUTE9_ROCK_TUNNEL_PATH_UNLOCKED')
      mark_cleared_event(story, ROUTE_2_EAST_LAB_EVENT_ID)
      mark_cleared_event(story, ROCKET_MOONLIGHT_SLEEP_EVENT_ID)
      FactionWar.record_activity(
        state,
        'team_rocket',
        'kanto',
        location,
        'sleep_signal_residue',
        threat_delta: 1,
        area_type: area_type
      )
      FactionWar.record_activity(
        state,
        'team_moonlight',
        'kanto',
        location,
        'lavender_sleep_frequency',
        threat_delta: 2,
        area_type: area_type
      )
      FactionWar.record_conflict(
        state,
        'team_rocket',
        'team_moonlight',
        location,
        'Rocket traces overlap with Moonlight sleep residue aimed at Lavender',
        intensity: 1,
        area_type: area_type
      )
      CompanionProgress.record_scene(
        state,
        'red',
        'route_2_east_exit',
        location: location,
        summary: 'Red confirms the Route 2 east exit keeps the Kanto journey physical.',
        area_type: area_type
      )
      CompanionProgress.record_scene(
        state,
        'bill',
        'echo_flute_decoder',
        location: location,
        summary: 'Bill and an Oak aide tune the Echo Flute lead into a sleep-frequency decoder.',
        area_type: area_type
      )
      WorldLink.queue_message(
        state,
        'story_alert',
        'Route 2 east decoded the Echo Flute lead, tied Rocket to Moonlight sleep traces, and opened Route 9 toward Rock Tunnel.',
        source: 'kanto_story',
        area_type: area_type
      )

      event = route_2_east_lab_event_result(location)
      story['event_history'] << event
      story['latest_event'] = event
      event
    end

    def route_2_east_field_lab_cleared?(state)
      ensure_kanto_story(state)['event_history'].any? { |event| event['event_id'] == ROUTE_2_EAST_LAB_EVENT_ID }
    end

    def complete_route_9_rock_tunnel_approach(state, location: 'Route 9', area_type: 'route')
      story = ensure_kanto_story(state)
      return { 'status' => 'blocked_missing_route_2_east_lab', 'event_id' => ROUTE_9_EVENT_ID } unless route_2_east_field_lab_cleared?(state)
      return { 'status' => 'already_cleared', 'event_id' => ROUTE_9_EVENT_ID } if route_9_rock_tunnel_approach_cleared?(state)

      add_story_flag(state, 'FLAG_NEXUS_ROUTE9_ROCK_TUNNEL_APPROACH_REACHED')
      add_story_flag(state, 'FLAG_NEXUS_RED_ROUTE9_TRAINER_LANE')
      add_story_flag(state, 'FLAG_NEXUS_BILL_ROCK_TUNNEL_DARKNESS_WARNING')
      add_story_flag(state, 'FLAG_NEXUS_TEAM_MOONLIGHT_ROUTE9_DEBUT')
      add_story_flag(state, 'FLAG_NEXUS_ROCKET_ROUTE9_SUPPLY_CACHE')
      add_story_flag(state, 'FLAG_NEXUS_LAVENDER_TOWER_SIGNAL_CONFIRMED')
      add_story_flag(state, 'FLAG_NEXUS_ROCK_TUNNEL_ENTRY_UNLOCKED')
      mark_cleared_event(story, ROUTE_9_EVENT_ID)
      mark_cleared_event(story, TEAM_MOONLIGHT_ROUTE_9_EVENT_ID)
      mark_cleared_event(story, ROCKET_ROUTE_9_CACHE_EVENT_ID)
      FactionWar.record_activity(
        state,
        'team_moonlight',
        'kanto',
        location,
        'route_9_sleep_marker',
        threat_delta: 2,
        area_type: area_type
      )
      FactionWar.record_activity(
        state,
        'team_rocket',
        'kanto',
        location,
        'rock_tunnel_supply_cache',
        threat_delta: 1,
        area_type: area_type
      )
      FactionWar.record_conflict(
        state,
        'team_rocket',
        'team_moonlight',
        location,
        'Rocket cache sits beside Moonlight route marker near the Lavender signal',
        intensity: 1,
        area_type: area_type
      )
      CompanionProgress.record_scene(
        state,
        'red',
        'route_9_trainer_lane',
        location: location,
        summary: 'Red turns Route 9 into a training lane before Rock Tunnel.',
        area_type: area_type
      )
      CompanionProgress.record_scene(
        state,
        'bill',
        'rock_tunnel_darkness_warning',
        location: location,
        summary: 'Bill warns that Rock Tunnel needs darkness planning before the Lavender signal is followed.',
        area_type: area_type
      )
      WorldLink.queue_message(
        state,
        'story_alert',
        'Route 9 exposed Team Moonlight on the road, a Rocket supply cache, and the Lavender tower signal before Rock Tunnel.',
        source: 'kanto_story',
        area_type: area_type
      )

      event = route_9_event_result(location)
      story['event_history'] << event
      story['latest_event'] = event
      event
    end

    def route_9_rock_tunnel_approach_cleared?(state)
      ensure_kanto_story(state)['event_history'].any? { |event| event['event_id'] == ROUTE_9_EVENT_ID }
    end

    def complete_rock_tunnel_interior(state, location: 'Rock Tunnel', area_type: 'cave')
      story = ensure_kanto_story(state)
      return { 'status' => 'blocked_missing_route_9_approach', 'event_id' => ROCK_TUNNEL_EVENT_ID } unless route_9_rock_tunnel_approach_cleared?(state)
      return { 'status' => 'already_cleared', 'event_id' => ROCK_TUNNEL_EVENT_ID } if rock_tunnel_interior_cleared?(state)

      add_story_flag(state, 'FLAG_NEXUS_ROCK_TUNNEL_INTERIOR_REACHED')
      add_story_flag(state, 'FLAG_NEXUS_RED_ROCK_TUNNEL_GUIDANCE')
      add_story_flag(state, 'FLAG_NEXUS_BILL_LAVENDER_ECHO_TRACE')
      add_story_flag(state, 'FLAG_NEXUS_TEAM_MOONLIGHT_CAVE_PRESSURE')
      add_story_flag(state, 'FLAG_NEXUS_ROCKET_DARK_CACHE')
      add_story_flag(state, 'FLAG_NEXUS_FLASH_LANTERN_NEEDED')
      add_story_flag(state, 'FLAG_NEXUS_CAVE_LANTERN_UNLOCKED')
      add_story_flag(state, 'FLAG_NEXUS_LAVENDER_EXIT_PATH_UNLOCKED')
      mark_cleared_event(story, ROCK_TUNNEL_EVENT_ID)
      mark_cleared_event(story, BILL_LAVENDER_ECHO_EVENT_ID)
      mark_cleared_event(story, TEAM_MOONLIGHT_CAVE_EVENT_ID)
      mark_cleared_event(story, ROCKET_DARK_CACHE_EVENT_ID)
      mark_cleared_event(story, FLASH_LANTERN_EVENT_ID)
      mark_cleared_event(story, LAVENDER_EXIT_EVENT_ID)
      FieldTools.unlock_tool(
        state,
        'cave_lantern',
        source: 'Rock Tunnel dark cache',
        area_type: area_type
      )
      FactionWar.record_activity(
        state,
        'team_moonlight',
        'kanto',
        location,
        'cave_dream_pressure',
        threat_delta: 2,
        area_type: area_type
      )
      FactionWar.record_activity(
        state,
        'team_rocket',
        'kanto',
        location,
        'dark_cache_surveillance',
        threat_delta: 1,
        area_type: area_type
      )
      FactionWar.record_conflict(
        state,
        'team_rocket',
        'team_moonlight',
        location,
        'Rocket dark cache exposes Giovanni watching Team Moonlight pressure the tunnel',
        intensity: 2,
        area_type: area_type
      )
      CompanionProgress.record_scene(
        state,
        'red',
        'rock_tunnel_guidance',
        location: location,
        summary: 'Red stays with Antman through a brief blackout and guides the Rock Tunnel trainer path.',
        area_type: area_type
      )
      CompanionProgress.record_scene(
        state,
        'bill',
        'lavender_echo_trace',
        location: location,
        summary: 'Bill traces the Echo Flute frequency through Rock Tunnel toward Lavender.',
        area_type: area_type
      )
      WorldLink.queue_message(
        state,
        'story_alert',
        'Rock Tunnel exposed Moonlight cave pressure, a Rocket dark cache, and the Lavender exit path after the Cave Lantern came online.',
        source: 'kanto_story',
        area_type: area_type
      )

      event = rock_tunnel_event_result(location)
      story['event_history'] << event
      story['latest_event'] = event
      event
    end

    def rock_tunnel_interior_cleared?(state)
      ensure_kanto_story(state)['event_history'].any? { |event| event['event_id'] == ROCK_TUNNEL_EVENT_ID }
    end

    def storage_anomalies(state)
      state['storage_anomalies'] ||= []
    end

    def field_healing_charges_for(state)
      case FieldHealing.policy(state)
      when 'full'
        0
      when 'restricted'
        1
      else
        3
      end
    end

    def add_story_flag(state, flag)
      state['story_flags'] ||= []
      state['story_flags'] << flag unless state['story_flags'].include?(flag)
    end

    def has_story_flag?(state, flag)
      (state['story_flags'] || []).include?(flag)
    end

    def mark_cleared_event(story, event_id)
      story['cleared_events'] << event_id unless story['cleared_events'].include?(event_id)
    end

    def reward_result(state, location)
      {
        'status' => 'applied',
        'reward_id' => BROCK_REWARD_ID,
        'location' => location.to_s,
        'current_act' => ensure_kanto_story(state)['current_act'],
        'unlocked_qol' => GameplayOptions.ensure_options(state)['unlocked_qol'].dup,
        'portable_pc_access_level' => PortablePC.ensure_portable_pc(state)['access_level'],
        'field_healing_charges' => FieldHealing.ensure_field_healing(state)['charges']
      }
    end

    def museum_event_result(location, partner_id)
      {
        'status' => 'cleared',
        'event_id' => MUSEUM_EVENT_ID,
        'location' => location.to_s,
        'partner_id' => partner_id.to_s,
        'factions' => %w[team_rocket team_phoenix],
        'next_hook' => 'mt_moon_rocket_moon_stone_operation'
      }
    end

    def mt_moon_event_result(location, rival_id)
      {
        'status' => 'cleared',
        'event_id' => MT_MOON_EVENT_ID,
        'location' => location.to_s,
        'rival_id' => rival_id.to_s,
        'factions' => %w[team_rocket team_gold_dust],
        'linked_events' => [GOLD_DUST_INVOICE_EVENT_ID, AVA_CLEFAIRY_EVENT_ID],
        'next_hook' => 'nugget_bridge_world_circuit_qualifier'
      }
    end

    def nugget_bridge_event_result(location, rival_ids)
      {
        'status' => 'cleared',
        'event_id' => NUGGET_BRIDGE_EVENT_ID,
        'location' => location.to_s,
        'rival_ids' => rival_ids.map(&:to_s),
        'companion_setup' => 'misty_cerulean_bridge_crisis',
        'next_hook' => 'misty_battle'
      }
    end

    def misty_event_result(gym_location, join_location)
      {
        'status' => 'cleared',
        'event_id' => MISTY_EVENT_ID,
        'gym_location' => gym_location.to_s,
        'join_location' => join_location.to_s,
        'badge' => 'Cascade Badge',
        'unlocks' => %w[old_rod rematch_board_tier_1 misty_following_companion],
        'next_hook' => 'bill_storage_metadata_anomaly'
      }
    end

    def bill_event_result(location, anomaly)
      {
        'status' => 'cleared',
        'event_id' => BILL_EVENT_ID,
        'location' => location.to_s,
        'companion_id' => 'bill',
        'anomaly_id' => anomaly['anomaly_id'],
        'next_hook' => 'ss_anne_foreign_trainers'
      }
    end

    def ss_anne_event_result(location, rival_id)
      {
        'status' => 'cleared',
        'event_id' => SS_ANNE_EVENT_ID,
        'location' => location.to_s,
        'rival_id' => rival_id.to_s,
        'linked_events' => [BLUE_SS_ANNE_EVENT_ID, ROCKET_MANIFEST_EVENT_ID, 'red_worldlink_mt_moon_note'],
        'factions' => %w[team_rocket],
        'next_hook' => 'lt_surge_battle'
      }
    end

    def vermilion_power_event_result(location)
      {
        'status' => 'cleared',
        'event_id' => VERMILION_POWER_EVENT_ID,
        'location' => location.to_s,
        'linked_events' => [ROCKET_GAS_POWER_EVENT_ID, TEAM_GAS_DEBUT_EVENT_ID, BILL_POWER_GRID_EVENT_ID],
        'factions' => %w[team_rocket team_gas],
        'companion_setup' => 'red_misty_surge_prep',
        'next_hook' => 'lt_surge_battle'
      }
    end

    def lt_surge_event_result(location)
      {
        'status' => 'cleared',
        'event_id' => LT_SURGE_EVENT_ID,
        'location' => location.to_s,
        'badge' => 'Thunder Badge',
        'unlocks' => %w[good_rod vs_seeker route_11_path],
        'next_hook' => 'route_11_handoff'
      }
    end

    def route_11_event_result(location)
      {
        'status' => 'cleared',
        'event_id' => ROUTE_11_EVENT_ID,
        'location' => location.to_s,
        'linked_events' => %w[red_route_11_eastbound misty_route_11_farewell bill_route_11_signal_decode rocket_gas_route_11_fallout snorlax_roadblock_teased],
        'next_hook' => 'diglett_cave_detour'
      }
    end

    def diglett_cave_event_result(location)
      {
        'status' => 'cleared',
        'event_id' => DIGLETT_CAVE_EVENT_ID,
        'location' => location.to_s,
        'linked_events' => [ROCKET_GOLD_DUST_CAVE_EVENT_ID, 'snorlax_route_12_block_confirmed', 'echo_flute_lead_seen'],
        'factions' => %w[team_rocket team_gold_dust],
        'next_hook' => 'route_2_east_field_lab'
      }
    end

    def route_2_east_lab_event_result(location)
      {
        'status' => 'cleared',
        'event_id' => ROUTE_2_EAST_LAB_EVENT_ID,
        'location' => location.to_s,
        'linked_events' => [ROCKET_MOONLIGHT_SLEEP_EVENT_ID, 'bill_echo_flute_decoder', 'oak_aide_field_tool_brief', 'lavender_signal_path_teased'],
        'factions' => %w[team_rocket team_moonlight],
        'next_hook' => 'route_9_rock_tunnel_approach'
      }
    end

    def route_9_event_result(location)
      {
        'status' => 'cleared',
        'event_id' => ROUTE_9_EVENT_ID,
        'location' => location.to_s,
        'linked_events' => [
          TEAM_MOONLIGHT_ROUTE_9_EVENT_ID,
          ROCKET_ROUTE_9_CACHE_EVENT_ID,
          'lavender_tower_signal_confirmed',
          'rock_tunnel_entry_unlocked'
        ],
        'factions' => %w[team_moonlight team_rocket],
        'next_hook' => 'rock_tunnel_interior'
      }
    end

    def rock_tunnel_event_result(location)
      {
        'status' => 'cleared',
        'event_id' => ROCK_TUNNEL_EVENT_ID,
        'location' => location.to_s,
        'linked_events' => [
          BILL_LAVENDER_ECHO_EVENT_ID,
          TEAM_MOONLIGHT_CAVE_EVENT_ID,
          ROCKET_DARK_CACHE_EVENT_ID,
          FLASH_LANTERN_EVENT_ID,
          LAVENDER_EXIT_EVENT_ID
        ],
        'factions' => %w[team_moonlight team_rocket],
        'unlocks' => %w[cave_lantern lavender_exit_path],
        'next_hook' => 'lavender_outskirts'
      }
    end

    def storage_anomaly_result(location)
      {
        'anomaly_id' => BILL_STORAGE_ANOMALY_ID,
        'source' => 'Bill',
        'location' => location.to_s,
        'linked_systems' => %w[pc portable_pc worldlink_feed region_progress],
        'summary' => 'Storage metadata points to region IDs Antman has not unlocked yet.'
      }
    end

    def record_rival_story_clue(state, rival_id, location, summary, area_type)
      rival = RivalProgress.ensure_rival(state, rival_id)
      activity = {
        'category' => 'rival_story_clue',
        'location' => location.to_s,
        'summary' => summary.to_s
      }
      RivalProgress.record_activity(rival, activity)
      WorldLink.queue_message(state, activity['category'], activity['summary'], source: rival['rival_id'], area_type: area_type)
    end

    def rival_display_name(rival_id)
      RivalProgress.rival_seed(rival_id)['display_name']
    end

    def companion_display_name(companion_id)
      CompanionProgress.companion_seed(companion_id)['display_name']
    end

    def already_applied_result(state)
      {
        'status' => 'already_applied',
        'reward_id' => BROCK_REWARD_ID,
        'current_act' => ensure_kanto_story(state)['current_act']
      }
    end
  end
end
