# frozen_string_literal: true

module NexusRed
  module CenterMartServices
    module_function

    def ensure_services(state)
      state['center_mart'] ||= build_services
    end

    def use_nurse_service(state, service_id, location:, area_type: 'route')
      services = ensure_services(state)
      id = service_id.to_s
      raise ArgumentError, "Unknown Nexus Red Nurse Joy service: #{service_id}" unless services['nurse_joy_services'].include?(id)

      entry = {
        'service_id' => id,
        'location' => location.to_s
      }
      services['service_history'] << entry
      if daily_service?(id)
        services['daily_services_claimed'] << id unless services['daily_services_claimed'].include?(id)
      end

      WorldLink.queue_message(
        state,
        'service_update',
        "Nurse Joy service used: #{id} at #{location}.",
        source: 'center_mart',
        area_type: area_type
      )
    end

    def terminal_available?(state, feature_id)
      ensure_services(state)['terminal_features'].include?(feature_id.to_s)
    end

    def unlock_terminal_feature(state, feature_id)
      services = ensure_services(state)
      id = feature_id.to_s
      raise ArgumentError, "Unknown Nexus Red terminal feature: #{feature_id}" unless all_terminal_features.include?(id)

      services['terminal_features'] << id unless services['terminal_features'].include?(id)
      services
    end

    def unlock_mart_tier(state, tier_id)
      services = ensure_services(state)
      tier = tier_id.to_s
      services['mart_tiers'] << tier unless services['mart_tiers'].include?(tier)
      services
    end

    def mart_inventory(state, mart_id)
      services = ensure_services(state)
      rules = mart_rules
      inventory = []
      inventory << 'basic_balls' if rules['core_balls_immediate']
      inventory << 'core_medicine' if rules['core_medicine_immediate']
      inventory << 'rare_candies' if rules['rare_candies_after_first_badge'] && services['mart_tiers'].include?('after_first_badge')
      inventory << 'specialty_mart' if rules['specialty_marts'].include?(mart_id.to_s)
      inventory
    end

    def build_services
      rules = mart_rules
      {
        'money' => rules['starting_money'],
        'nurse_joy_services' => center_mart_seed['nurse_joy_services'].dup,
        'terminal_features' => initial_terminal_features,
        'mart_tiers' => ['base'],
        'service_history' => [],
        'daily_services_claimed' => []
      }
    end

    def initial_terminal_features
      all_terminal_features.select do |feature|
        %w[pc worldlink_feed difficulty_settings move_reminder_deleter].include?(feature)
      end
    end

    def all_terminal_features
      center_mart_seed['pokecenter_terminal']
    end

    def center_mart_seed
      SeedData.gameplay_systems['pokemon_center_and_mart']
    end

    def mart_rules
      center_mart_seed['mart_rules']
    end

    def daily_service?(service_id)
      service_id == 'daily_wellness_gift'
    end
  end
end
