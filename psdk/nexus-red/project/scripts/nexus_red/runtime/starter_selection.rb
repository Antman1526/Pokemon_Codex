# frozen_string_literal: true

module NexusRed
  module StarterSelection
    module_function

    def ensure_selection(state)
      state['starter_selection'] ||= build_selection
    end

    def available_partners(state)
      ensure_selection(state)['available_partners']
    end

    def select_partner(state, species, source: 'Professor Oak', area_type: 'route')
      selection = ensure_selection(state)
      raise ArgumentError, 'Nexus Red starter has already been chosen' if starter_chosen?(state)

      partner = find_partner(selection, species)
      raise ArgumentError, "Unknown Nexus Red starter partner: #{species}" if partner.nil?

      selection['selected_partner'] = partner
      selection['rival_assignments'] = build_rival_assignments(partner['species'])
      PartyStorage.add_species(state, partner['species'])
      state['story_flags'] ||= []
      state['story_flags'] << 'starter_chosen' unless state['story_flags'].include?('starter_chosen')

      WorldLink.queue_message(
        state,
        'story_unlock',
        "#{source} registered #{partner['species']} as Antman's first partner.",
        source: 'starter_selection',
        area_type: area_type
      )
    end

    def starter_chosen?(state)
      !ensure_selection(state)['selected_partner'].nil?
    end

    def rival_assignment(state, rival_id)
      ensure_selection(state)['rival_assignments'][rival_id.to_s]
    end

    def build_selection
      selector = SeedData.starter_selector
      {
        'story_context' => selector['story_context'].dup,
        'selection_rules' => selector['selection_rules'].dup,
        'available_partners' => selector['selectable_partners'].map(&:dup),
        'selected_partner' => nil,
        'rival_assignments' => {}
      }
    end

    def find_partner(selection, species)
      selection['available_partners'].find { |partner| partner['species'] == species.to_s }
    end

    def build_rival_assignments(player_species)
      {
        'blue' => SeedData.blue_counter_for(player_species),
        'ava' => first_available_from(SeedData.starter_selector['ava_priority_pool'], SeedData.starter_selector['ava_fallback'], [player_species]),
        'dax' => first_available_from(SeedData.starter_selector['dax_priority_pool'], SeedData.starter_selector['dax_fallback'], [player_species])
      }
    end

    def first_available_from(priority_pool, fallback, excluded_species)
      priority_pool.find { |species| !excluded_species.include?(species) } || fallback
    end
  end
end
