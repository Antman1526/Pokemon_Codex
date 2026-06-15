# frozen_string_literal: true

module NexusRed
  module PartyStorage
    PARTY_LIMIT = 6

    module_function

    def add_species(state, species)
      species_name = species.to_s
      if party_full?(state)
        pc_box_species(state) << species_name unless pc_box_species(state).include?(species_name)
        storage_result(species_name, 'pc')
      else
        party_species(state) << species_name unless party_species(state).include?(species_name)
        storage_result(species_name, 'party')
      end
    end

    def party_full?(state)
      party_species(state).length >= PARTY_LIMIT
    end

    def party_species(state)
      state['party_species'] ||= []
    end

    def pc_box_species(state)
      state['pc_box_species'] ||= []
    end

    def storage_result(species, storage)
      {
        'species' => species,
        'storage' => storage
      }
    end
  end
end
