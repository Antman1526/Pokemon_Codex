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

    def deposit_species(state, species)
      species_name = species.to_s
      return operation_result('missing_from_party', species_name) unless party_species(state).include?(species_name)

      party_species(state).delete(species_name)
      pc_box_species(state) << species_name unless pc_box_species(state).include?(species_name)
      operation_result('deposited', species_name, storage: 'pc')
    end

    def withdraw_species(state, species)
      species_name = species.to_s
      return operation_result('missing_from_pc', species_name) unless pc_box_species(state).include?(species_name)
      return operation_result('party_full', species_name, storage: 'pc') if party_full?(state)

      pc_box_species(state).delete(species_name)
      party_species(state) << species_name unless party_species(state).include?(species_name)
      operation_result('withdrawn', species_name, storage: 'party')
    end

    def swap_species(state, party_species:, pc_species:)
      party_name = party_species.to_s
      pc_name = pc_species.to_s
      return operation_result('missing_from_party', party_name) unless self.party_species(state).include?(party_name)
      return operation_result('missing_from_pc', pc_name) unless pc_box_species(state).include?(pc_name)

      party_index = self.party_species(state).index(party_name)
      pc_index = pc_box_species(state).index(pc_name)
      self.party_species(state)[party_index] = pc_name
      pc_box_species(state)[pc_index] = party_name
      {
        'status' => 'swapped',
        'party_species' => pc_name,
        'pc_species' => party_name
      }
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

    def operation_result(status, species, storage: nil)
      result = {
        'status' => status,
        'species' => species
      }
      result['storage'] = storage unless storage.nil?
      result
    end
  end
end
