# frozen_string_literal: true

module NexusRed
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
end
