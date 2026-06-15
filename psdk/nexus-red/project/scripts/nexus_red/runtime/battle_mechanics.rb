# frozen_string_literal: true

module NexusRed
  module BattleMechanics
    module_function

    def ensure_mechanics(state)
      state['battle_mechanics'] ||= build_mechanics
    end

    def mechanic_enabled?(state, mechanic_id)
      ensure_mechanics(state)['enabled_mechanics'].include?(mechanic_id.to_s)
    end

    def ai_profile_for(_state, difficulty_mode)
      profile = SeedData.gameplay_systems.dig('boss_difficulty_modes', difficulty_mode.to_s)
      raise ArgumentError, "Unknown Nexus Red boss difficulty mode: #{difficulty_mode}" if profile.nil?

      profile['ai_profile']
    end

    def gimmick_status(state, gimmick_id)
      mechanics = ensure_mechanics(state)
      id = gimmick_id.to_s
      rule = gimmick_rules[id]
      raise ArgumentError, "Unknown Nexus Red gimmick: #{gimmick_id}" if rule.nil?

      unlock = mechanics['gimmick_unlocks'][id]
      state_name = if unlock
                     unlock['mode']
                   elsif preview_available?(state, rule['first_preview'])
                     'preview'
                   else
                     'locked'
                   end
      {
        'gimmick_id' => id,
        'state' => state_name,
        'first_preview' => rule['first_preview'],
        'full_unlock' => rule['full_unlock'],
        'rule' => rule['rule']
      }
    end

    def unlock_gimmick(state, gimmick_id, mode:, source:)
      mechanics = ensure_mechanics(state)
      id = gimmick_id.to_s
      raise ArgumentError, "Unknown Nexus Red gimmick: #{gimmick_id}" unless gimmick_rules.key?(id)

      selected_mode = mode.to_s
      raise ArgumentError, "Unknown Nexus Red gimmick unlock mode: #{mode}" unless %w[preview full].include?(selected_mode)

      mechanics['gimmick_unlocks'][id] = {
        'mode' => selected_mode,
        'source' => source.to_s
      }
      mechanics
    end

    def build_mechanics
      {
        'enabled_mechanics' => battle_seed['required'].dup,
        'gimmick_gating' => gimmick_rules.transform_values(&:dup),
        'gimmick_unlocks' => {}
      }
    end

    def preview_available?(state, preview_rule)
      case preview_rule.to_s
      when 'after_hoenn'
        completed_regions(state).include?('hoenn')
      else
        false
      end
    end

    def completed_regions(state)
      RegionProgress.ensure_progress(state)['completed_regions']
    end

    def battle_seed
      SeedData.gameplay_systems['battle_mechanics']
    end

    def gimmick_rules
      battle_seed['gimmick_gating']
    end
  end
end
