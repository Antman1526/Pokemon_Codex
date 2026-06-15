# frozen_string_literal: true

require 'json'

module NexusRed
  module SeedData
    REGISTRY_FILES = {
      starter_selector: 'oak_lab_first_partner_selector.json',
      early_encounters: 'routes_1_to_3_migration_encounters.json',
      regions: 'world_region_progression_spine.json',
      factions: 'custom_faction_war_registry.json',
      companions: 'core_companion_registry.json',
      rivals_worldlink: 'rival_worldlink_registry.json',
      gameplay_systems: 'gameplay_systems_registry.json'
    }.freeze

    module_function

    def root_path
      @root_path ||= locate_project_root
    end

    def generated_path
      File.join(root_path, 'Data', 'nexus_red_seed', 'generated')
    end

    def registry(name)
      key = name.to_sym
      filename = REGISTRY_FILES.fetch(key) { raise ArgumentError, "Unknown Nexus Red registry: #{name}" }
      read_json(File.join(generated_path, filename))
    end

    def starter_selector
      registry(:starter_selector)
    end

    def early_encounters
      registry(:early_encounters)
    end

    def regions
      registry(:regions)
    end

    def factions
      registry(:factions)
    end

    def companions
      registry(:companions)
    end

    def rivals_worldlink
      registry(:rivals_worldlink)
    end

    def gameplay_systems
      registry(:gameplay_systems)
    end

    def all
      REGISTRY_FILES.keys.each_with_object({}) { |key, acc| acc[key] = registry(key) }
    end

    def starter_species
      starter_selector['selectable_partners'].map { |partner| partner['species'] }
    end

    def blue_counter_for(species)
      starter_selector['blue_counter_rules'][species.to_s]
    end

    def encounters_for_route(route_id)
      route = early_encounters['route_targets'][route_id.to_s]
      route ? route['encounters'] : []
    end

    def region_order
      regions['region_unlocks'].map { |region| region['region_id'] }
    end

    def final_region
      regions['final_region']
    end

    def primary_faction
      factions['primary_antagonist']
    end

    def hidden_meta_villain
      factions['hidden_meta_villain']
    end

    def red_primary_companion?
      companions['primary_companion'] == 'red'
    end

    def companion_ids
      companions['companions'].map { |companion| companion['companion_id'] }
    end

    def rival_ids
      rivals_worldlink['rivals'].map { |rival| rival['rival_id'] }
    end

    def starting_rival_ids
      rivals_worldlink['starting_rivals']
    end

    def worldlink_paused_area?(area_type)
      pause_list = rivals_worldlink.dig('worldlink_settings', 'delivery_rules', 'pause_and_digest') || []
      pause_list.include?(area_type.to_s)
    end

    def all_base_species_before_final_boss?
      gameplay_systems.dig('pokedex_and_availability', 'all_base_species_before_final_boss') == true
    end

    def starting_money
      gameplay_systems.dig('pokemon_center_and_mart', 'mart_rules', 'starting_money')
    end

    def gameplay_option_available?(option_id)
      gameplay_systems.dig('qol_systems', 'must_have').include?(option_id.to_s)
    end

    def read_json(path)
      JSON.parse(File.read(path))
    rescue Errno::ENOENT
      raise "Missing Nexus Red seed registry: #{path}"
    rescue JSON::ParserError => e
      raise "Invalid Nexus Red seed JSON #{path}: #{e.message}"
    end

    def locate_project_root
      candidates = [
        Dir.pwd,
        File.expand_path('../..', __dir__),
        File.expand_path('../../..', __dir__)
      ]
      candidates.find { |path| File.exist?(File.join(path, 'Data', 'nexus_red_seed', 'import_manifest.json')) } || Dir.pwd
    end
  end

  module RuntimeState
    module_function

    def build
      {
        'current_region' => 'kanto',
        'active_companion' => 'red',
        'worldlink_unlocked' => false,
        'worldlink_unread_count' => 0,
        'worldlink_recent_messages' => [],
        'worldlink_paused_messages' => [],
        'rival_progress' => {},
        'companion_progress' => {},
        'faction_progress' => {},
        'gameplay_options' => {
          'difficulty_mode' => 'standard',
          'level_caps_enabled' => true,
          'infinite_repel_enabled' => false,
          'nuzlocke_enabled' => false
        }
      }
    end
  end

  module WorldLink
    module_function

    def queue_message(state, category, text, source: 'system', area_type: 'route')
      message = build_message(state, category, text, source, area_type)
      if SeedData.worldlink_paused_area?(area_type)
        state['worldlink_paused_messages'] << message
        message['delivery'] = 'paused'
      else
        push_recent_message(state, message)
        message['delivery'] = 'immediate'
      end
      message
    end

    def release_digest(state)
      messages = state['worldlink_paused_messages']
      digest = {
        'title' => 'While You Were Away',
        'items' => messages.dup
      }
      messages.each { |message| push_recent_message(state, message.merge('delivery' => 'digest')) }
      state['worldlink_paused_messages'] = []
      digest
    end

    def mark_all_read(state)
      state['worldlink_unread_count'] = 0
      state['worldlink_recent_messages'].each { |message| message['read'] = true }
      state['worldlink_paused_messages'].each { |message| message['read'] = true }
    end

    def build_message(state, category, text, source, area_type)
      {
        'id' => format('wl_%04d', next_message_index(state)),
        'category' => category.to_s,
        'source' => source.to_s,
        'area_type' => area_type.to_s,
        'text' => text.to_s,
        'read' => false
      }
    end

    def next_message_index(state)
      state['worldlink_message_index'] ||= 0
      state['worldlink_message_index'] += 1
    end

    def push_recent_message(state, message)
      capacity = SeedData.rivals_worldlink.dig('worldlink_settings', 'recent_message_capacity') || 32
      state['worldlink_recent_messages'] << message
      state['worldlink_recent_messages'].shift while state['worldlink_recent_messages'].length > capacity
      state['worldlink_unread_count'] += 1 unless message['read']
    end
  end

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

  module RegionProgress
    module_function

    def ensure_progress(state)
      state['region_progress'] ||= build_progress(state)
    end

    def current_region_seed(state)
      region_seed(state['current_region']) || raise(ArgumentError, "Unknown Nexus Red region: #{state['current_region']}")
    end

    def can_enter_region?(state, region_id)
      ensure_progress(state)['unlocked_regions'].include?(region_id.to_s)
    end

    def advance_to_next_region(state, completion_flag:, transition_hub:, area_type: 'route')
      progress = ensure_progress(state)
      current = progress['current_region']
      next_region = next_region_id(current)
      raise ArgumentError, "#{current} is the final Nexus Red region" if next_region.nil?

      mark_region_completed(progress, current)
      switch_region(state, progress, next_region)

      transition = {
        'category' => 'story_unlock',
        'from_region' => current,
        'to_region' => next_region,
        'completion_flag' => completion_flag.to_s,
        'transition_hub' => transition_hub.to_s,
        'summary' => "#{region_display_name(next_region)} unlocked through #{transition_hub}."
      }
      progress['latest_transition'] = transition
      WorldLink.queue_message(state, transition['category'], transition['summary'], source: 'region_progress', area_type: area_type)
    end

    def complete_current_region(state, completion_flag:, area_type: 'route')
      progress = ensure_progress(state)
      current = progress['current_region']
      mark_region_completed(progress, current)
      transition = {
        'category' => 'story_unlock',
        'from_region' => current,
        'to_region' => nil,
        'completion_flag' => completion_flag.to_s,
        'transition_hub' => nil,
        'summary' => "#{region_display_name(current)} chapter complete."
      }
      progress['latest_transition'] = transition
      WorldLink.queue_message(state, transition['category'], transition['summary'], source: 'region_progress', area_type: area_type)
    end

    def final_region_unlocked?(state)
      ensure_progress(state)['current_region'] == SeedData.final_region
    end

    def journey_complete?(state)
      ensure_progress(state)['completed_regions'].include?(SeedData.final_region)
    end

    def build_progress(state)
      current = state['current_region'] || SeedData.regions['current_region']
      {
        'current_region' => current,
        'unlocked_regions' => [current],
        'completed_regions' => [],
        'region_history' => [current],
        'final_region' => SeedData.final_region,
        'latest_transition' => nil
      }
    end

    def switch_region(state, progress, next_region)
      state['current_region'] = next_region
      progress['current_region'] = next_region
      progress['unlocked_regions'] = [next_region]
      progress['region_history'] << next_region unless progress['region_history'].include?(next_region)
    end

    def mark_region_completed(progress, region_id)
      progress['completed_regions'] << region_id unless progress['completed_regions'].include?(region_id)
    end

    def next_region_id(region_id)
      order = SeedData.region_order
      index = order.index(region_id.to_s)
      return nil if index.nil?

      order[index + 1]
    end

    def region_seed(region_id)
      SeedData.regions['region_unlocks'].find { |region| region['region_id'] == region_id.to_s }
    end

    def region_display_name(region_id)
      seed = region_seed(region_id)
      seed ? seed['display_name'] : region_id.to_s
    end
  end

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

  module FieldTools
    module_function

    def ensure_tools(state)
      state['field_tools'] ||= {
        'unlocked_tools' => [],
        'known_replacements' => replacements.dup,
        'tool_sources' => {},
        'latest_unlock' => nil
      }
    end

    def unlock_tool(state, tool_id, source:, area_type: 'route')
      tools = ensure_tools(state)
      id = tool_id.to_s
      raise ArgumentError, "Unknown Nexus Red field tool: #{tool_id}" unless replacements.key?(id)

      tools['unlocked_tools'] << id unless tools['unlocked_tools'].include?(id)
      tools['tool_sources'][id] = source.to_s
      unlock = {
        'category' => 'story_unlock',
        'tool_id' => id,
        'hm_replacement' => replacements[id],
        'source' => source.to_s,
        'summary' => "#{tool_display_name(id)} unlocked as the #{replacements[id]} field replacement."
      }
      tools['latest_unlock'] = unlock
      WorldLink.queue_message(state, unlock['category'], unlock['summary'], source: 'field_tools', area_type: area_type)
    end

    def has_tool?(state, tool_id)
      ensure_tools(state)['unlocked_tools'].include?(tool_id.to_s)
    end

    def can_use_replacement?(state, hm_name)
      replacement = replacements.find { |_tool_id, replaced_hm| replaced_hm == hm_name.to_s }
      return false if replacement.nil?

      has_tool?(state, replacement.first)
    end

    def expanded_dig_actions(state)
      has_tool?(state, 'dig_kit') ? field_tools_seed['expanded_dig'].dup : []
    end

    def expanded_fly_actions(state)
      has_tool?(state, 'sky_pass') ? field_tools_seed['expanded_fly'].dup : []
    end

    def replacements
      field_tools_seed['hm_replacements']
    end

    def field_tools_seed
      SeedData.gameplay_systems['field_tools']
    end

    def tool_display_name(tool_id)
      tool_id.to_s.split('_').map(&:capitalize).join(' ')
    end
  end
end

if defined?(PFM::GameState)
  class PFM::GameState
    attr_accessor :nexus_red

    on_player_initialize(:nexus_red) { @nexus_red = NexusRed::RuntimeState.build }
    on_expand_global_variables(:nexus_red) { @nexus_red ||= NexusRed::RuntimeState.build }
  end
end
