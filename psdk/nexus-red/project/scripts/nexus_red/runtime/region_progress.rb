# frozen_string_literal: true

module NexusRed
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
end
