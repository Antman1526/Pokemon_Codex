# frozen_string_literal: true

module NexusRed
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
end
