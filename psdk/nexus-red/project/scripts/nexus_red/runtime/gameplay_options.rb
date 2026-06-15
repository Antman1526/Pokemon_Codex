# frozen_string_literal: true

module NexusRed
  module GameplayOptions
    module_function

    def ensure_options(state)
      options = state['gameplay_options'] ||= {}
      default_mode = SeedData.gameplay_systems.dig('system_profile', 'default_difficulty') || 'standard'
      options['difficulty_mode'] ||= default_mode
      options['difficulty_profile'] ||= difficulty_profile(options['difficulty_mode'])
      options['level_caps_enabled'] = true if options['level_caps_enabled'].nil?
      options['infinite_repel_enabled'] = false if options['infinite_repel_enabled'].nil?
      options['nuzlocke_enabled'] = options['difficulty_mode'] == 'nuzlocke' if options['nuzlocke_enabled'].nil?
      options['nuzlocke_rules'] ||= nuzlocke_rules_for(options['difficulty_mode'])
      options['starting_money'] ||= SeedData.starting_money
      options['unlocked_qol'] ||= start_enabled_qol
      options['disabled_options'] ||= []
      options
    end

    def set_difficulty(state, mode)
      options = ensure_options(state)
      selected = mode.to_s
      profile = difficulty_profile(selected)
      options['difficulty_mode'] = selected
      options['difficulty_profile'] = profile
      options['nuzlocke_enabled'] = selected == 'nuzlocke'
      options['nuzlocke_rules'] = nuzlocke_rules_for(selected)
      options['level_caps_enabled'] = true if profile['cap_type'] == 'hard' || selected == 'nuzlocke'
      options
    end

    def toggle_option(state, option_id, enabled)
      options = ensure_options(state)
      id = option_id.to_s
      raise ArgumentError, "Unknown Nexus Red gameplay option: #{option_id}" unless known_option?(id)

      case id
      when 'infinite_repel_toggle'
        options['infinite_repel_enabled'] = enabled == true
      when 'level_caps'
        options['level_caps_enabled'] = enabled == true
      when 'built_in_nuzlocke_tools'
        options['nuzlocke_enabled'] = enabled == true
      else
        options[id] = enabled == true
      end

      if enabled == true
        options['disabled_options'].delete(id)
      else
        options['disabled_options'] << id unless options['disabled_options'].include?(id)
      end
      options
    end

    def unlock_qol(state, tier)
      options = ensure_options(state)
      unlocks = SeedData.gameplay_systems.dig('qol_systems', 'unlocks', tier.to_s) ||
        raise(ArgumentError, "Unknown Nexus Red QoL unlock tier: #{tier}")
      unlocks.each { |unlock| options['unlocked_qol'] << unlock unless options['unlocked_qol'].include?(unlock) }
      options['latest_qol_unlock'] = tier.to_s
      options
    end

    def rare_candy_mart_available?(state)
      ensure_options(state)['unlocked_qol'].include?('rare_candy_mart')
    end

    def level_caps_enabled?(state)
      ensure_options(state)['level_caps_enabled'] == true
    end

    def difficulty_profile(mode)
      profile = SeedData.gameplay_systems.dig('difficulty_modes', mode.to_s)
      raise ArgumentError, "Unknown Nexus Red difficulty mode: #{mode}" if profile.nil?

      profile.dup
    end

    def nuzlocke_rules_for(mode)
      mode.to_s == 'nuzlocke' ? difficulty_profile('nuzlocke').fetch('rules', []).dup : []
    end

    def start_enabled_qol
      SeedData.gameplay_systems.dig('qol_systems', 'start_enabled').dup
    end

    def known_option?(option_id)
      SeedData.gameplay_systems.dig('qol_systems', 'must_have').include?(option_id) ||
        SeedData.gameplay_systems.dig('qol_systems', 'start_enabled').include?(option_id)
    end
  end
end
