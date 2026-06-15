# frozen_string_literal: true

module NexusRed
  module RivalProgress
    module_function

    def ensure_rival(state, rival_id)
      id = rival_id.to_s
      state['rival_progress'][id] ||= build_rival_progress(id)
    end

    def record_badge(state, rival_id, leader, badge, location: nil, area_type: 'route')
      rival = ensure_rival(state, rival_id)
      badge_entry = {
        'leader' => leader.to_s,
        'badge' => badge.to_s,
        'location' => location.to_s
      }
      rival['badges'].reject! { |entry| entry['badge'] == badge_entry['badge'] }
      rival['badges'] << badge_entry
      rival['badge_count'] = rival['badges'].length

      activity = {
        'category' => 'rival_badge',
        'leader' => badge_entry['leader'],
        'badge' => badge_entry['badge'],
        'location' => badge_entry['location'],
        'summary' => "#{rival['display_name']} defeated #{badge_entry['leader']} and earned the #{badge_entry['badge']}."
      }
      record_activity(rival, activity)
      WorldLink.queue_message(state, activity['category'], activity['summary'], source: rival['rival_id'], area_type: area_type)
    end

    def record_capture(state, rival_id, species, location, rare: false, area_type: 'route')
      rival = ensure_rival(state, rival_id)
      capture = {
        'species' => species.to_s,
        'location' => location.to_s,
        'rare' => rare == true
      }
      rival['captures'] << capture

      category = capture['rare'] ? 'rival_rare_capture' : 'rival_capture_common'
      rarity_text = capture['rare'] ? 'rare ' : ''
      activity = {
        'category' => category,
        'species' => capture['species'],
        'location' => capture['location'],
        'rare' => capture['rare'],
        'summary' => "#{rival['display_name']} caught a #{rarity_text}#{capture['species']} at #{capture['location']}."
      }
      record_activity(rival, activity)
      WorldLink.queue_message(state, category, activity['summary'], source: rival['rival_id'], area_type: area_type)
    end

    def record_region_entry(state, rival_id, region, hub: nil, objective: nil, area_type: 'route')
      rival = ensure_rival(state, rival_id)
      rival['current_region'] = region.to_s
      rival['last_known_location'] = hub.to_s unless hub.nil?

      activity = {
        'category' => 'rival_region_entry',
        'region' => rival['current_region'],
        'hub' => hub.to_s,
        'objective' => objective.to_s,
        'summary' => region_entry_summary(rival, hub, objective)
      }
      record_activity(rival, activity)
      WorldLink.queue_message(state, activity['category'], activity['summary'], source: rival['rival_id'], area_type: area_type)
    end

    def build_rival_progress(rival_id)
      seed = rival_seed(rival_id)
      {
        'rival_id' => seed['rival_id'],
        'display_name' => seed['display_name'],
        'current_region' => normalize_region(seed['origin_region']),
        'last_known_location' => seed['origin_region'],
        'badge_count' => 0,
        'badges' => [],
        'captures' => [],
        'latest_activity' => nil,
        'relationship' => seed['relationship_defaults'].dup,
        'notification_behavior' => seed['notification_behavior']
      }
    end

    def rival_seed(rival_id)
      SeedData.rivals_worldlink['rivals'].find { |rival| rival['rival_id'] == rival_id.to_s } ||
        raise(ArgumentError, "Unknown Nexus Red rival: #{rival_id}")
    end

    def normalize_region(region)
      region.to_s.downcase.gsub(/[^a-z0-9]+/, '_').gsub(/\A_+|_+\z/, '')
    end

    def record_activity(rival, activity)
      rival['latest_activity'] = activity
    end

    def region_entry_summary(rival, hub, objective)
      summary = "#{rival['display_name']} entered #{rival['current_region']}"
      summary += " through #{hub}" unless hub.nil? || hub.to_s.empty?
      summary += " while #{objective}" unless objective.nil? || objective.to_s.empty?
      "#{summary}."
    end
  end
end
