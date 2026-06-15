# frozen_string_literal: true

module NexusRed
  module KantoStory
    BROCK_REWARD_ID = 'brock_red_field_kit'

    module_function

    def ensure_kanto_story(state)
      state['kanto_story'] ||= {
        'current_act' => 'act_1_pallet_to_pewter',
        'cleared_events' => [],
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

    def already_applied_result(state)
      {
        'status' => 'already_applied',
        'reward_id' => BROCK_REWARD_ID,
        'current_act' => ensure_kanto_story(state)['current_act']
      }
    end
  end
end
