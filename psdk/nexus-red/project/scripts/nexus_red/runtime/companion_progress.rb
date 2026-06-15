# frozen_string_literal: true

module NexusRed
  module CompanionProgress
    module_function

    def ensure_companion(state, companion_id)
      id = companion_id.to_s
      state['companion_progress'][id] ||= build_companion_progress(state, id)
    end

    def activate_companion(state, companion_id, location: nil, reason: nil, following: false, area_type: 'route')
      companion = ensure_companion(state, companion_id)
      companion['active'] = true
      companion['following'] = following == true
      companion['last_known_location'] = location.to_s unless location.nil?

      activity = {
        'category' => 'companion_request',
        'location' => location.to_s,
        'reason' => reason.to_s,
        'summary' => activation_summary(companion, location, reason)
      }
      record_activity(companion, activity)
      WorldLink.queue_message(state, activity['category'], activity['summary'], source: companion['companion_id'], area_type: area_type)
    end

    def record_scene(state, companion_id, scene_id, location: nil, summary: nil, area_type: 'route')
      companion = ensure_companion(state, companion_id)
      scene = scene_id.to_s
      companion['scene_flags'] << scene unless companion['scene_flags'].include?(scene)
      companion['last_known_location'] = location.to_s unless location.nil?

      activity = {
        'category' => 'companion_scene',
        'scene_id' => scene,
        'location' => location.to_s,
        'summary' => summary.to_s.empty? ? "#{companion['display_name']} shared a companion moment." : summary.to_s
      }
      record_activity(companion, activity)
      WorldLink.queue_message(state, activity['category'], activity['summary'], source: companion['companion_id'], area_type: area_type)
    end

    def tag_battle_ready?(state, companion_id, context: 'field')
      companion = ensure_companion(state, companion_id)
      return false unless companion['active']
      return false unless companion['tag_battle_eligible']
      return false if context.to_s == 'gym_battle' && !companion['gym_battle_partner']

      true
    end

    def build_companion_progress(state, companion_id)
      seed = companion_seed(companion_id)
      primary = companion_id == SeedData.companions['primary_companion']
      {
        'companion_id' => seed['companion_id'],
        'display_name' => seed['display_name'],
        'role' => seed['role'],
        'active_from' => seed['active_from'],
        'active' => primary || state['active_companion'] == companion_id,
        'following' => primary || state['active_companion'] == companion_id,
        'tag_battle_eligible' => seed['tag_battle_eligible'] == true,
        'gym_battle_partner' => seed['gym_battle_partner'] == true,
        'last_known_location' => seed['active_from'],
        'scene_flags' => [],
        'latest_activity' => nil
      }
    end

    def companion_seed(companion_id)
      SeedData.companions['companions'].find { |companion| companion['companion_id'] == companion_id.to_s } ||
        raise(ArgumentError, "Unknown Nexus Red companion: #{companion_id}")
    end

    def activation_summary(companion, location, reason)
      summary = "#{companion['display_name']} joined Antman's travel party"
      summary += " at #{location}" unless location.nil? || location.to_s.empty?
      summary += " because #{reason}" unless reason.nil? || reason.to_s.empty?
      "#{summary}."
    end

    def record_activity(companion, activity)
      companion['latest_activity'] = activity
    end
  end
end
