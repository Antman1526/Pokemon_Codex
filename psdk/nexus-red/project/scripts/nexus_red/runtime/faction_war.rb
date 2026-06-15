# frozen_string_literal: true

module NexusRed
  module FactionWar
    module_function

    def ensure_faction(state, faction_id)
      id = faction_id.to_s
      state['faction_progress'][id] ||= build_faction_progress(id)
    end

    def record_activity(state, faction_id, region, location, operation, threat_delta: 1, area_type: 'route')
      faction = ensure_faction(state, faction_id)
      activity = {
        'category' => 'villain_alert',
        'region' => region.to_s,
        'location' => location.to_s,
        'operation' => operation.to_s,
        'threat_delta' => threat_delta.to_i,
        'summary' => "#{faction['display_name']} activity detected at #{location}: #{operation}."
      }
      faction['threat_level'] += activity['threat_delta']
      faction['region_activity'][activity['region']] ||= []
      faction['region_activity'][activity['region']] << activity
      faction['latest_activity'] = activity
      WorldLink.queue_message(state, activity['category'], activity['summary'], source: faction['faction_id'], area_type: area_type)
    end

    def record_conflict(state, faction_a_id, faction_b_id, location, cause, intensity: 1, area_type: 'route')
      faction_a = ensure_faction(state, faction_a_id)
      faction_b = ensure_faction(state, faction_b_id)
      conflict = {
        'category' => 'villain_alert',
        'opponent' => faction_b['faction_id'],
        'location' => location.to_s,
        'cause' => cause.to_s,
        'intensity' => intensity.to_i,
        'summary' => "#{faction_a['display_name']} clashed with #{faction_b['display_name']} at #{location}: #{cause}."
      }
      mirror = conflict.merge(
        'opponent' => faction_a['faction_id'],
        'summary' => "#{faction_b['display_name']} clashed with #{faction_a['display_name']} at #{location}: #{cause}."
      )
      faction_a['conflicts'] << conflict
      faction_b['conflicts'] << mirror
      faction_a['threat_level'] += conflict['intensity']
      faction_b['threat_level'] += conflict['intensity']
      faction_a['latest_activity'] = conflict
      faction_b['latest_activity'] = mirror
      WorldLink.queue_message(state, conflict['category'], conflict['summary'], source: faction_a['faction_id'], area_type: area_type)
    end

    def reveal_hidden_faction(state, faction_id, region, evidence, area_type: 'route')
      faction = ensure_faction(state, faction_id)
      faction['revealed'] = true
      activity = {
        'category' => 'villain_alert',
        'region' => region.to_s,
        'evidence' => evidence.to_s,
        'summary' => "#{faction['display_name']} was exposed through #{evidence}."
      }
      faction['latest_activity'] = activity
      WorldLink.queue_message(state, activity['category'], activity['summary'], source: faction['faction_id'], area_type: area_type)
    end

    def build_faction_progress(faction_id)
      seed = faction_seed(faction_id)
      {
        'faction_id' => seed['faction_id'],
        'display_name' => seed['display_name'],
        'leader' => seed['leader'],
        'role' => seed['role'],
        'active_enemy_faction' => seed['active_enemy_faction'] == true,
        'revealed' => faction_id != SeedData.hidden_meta_villain,
        'threat_level' => 0,
        'region_activity' => {},
        'conflicts' => [],
        'latest_activity' => nil
      }
    end

    def faction_seed(faction_id)
      SeedData.factions['factions'].find { |faction| faction['faction_id'] == faction_id.to_s } ||
        raise(ArgumentError, "Unknown Nexus Red faction: #{faction_id}")
    end
  end
end
