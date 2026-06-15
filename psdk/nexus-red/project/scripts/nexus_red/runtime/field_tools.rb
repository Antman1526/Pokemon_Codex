# frozen_string_literal: true

module NexusRed
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
