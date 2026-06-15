# frozen_string_literal: true

module NexusRed
  module PortablePC
    module_function

    def ensure_portable_pc(state)
      state['portable_pc'] ||= {
        'unlocked' => false,
        'access_level' => 'locked',
        'source' => nil,
        'opened_count' => 0,
        'last_action' => nil
      }
    end

    def unlock(state, source:, access_level: 'full', area_type: 'route')
      pc = ensure_portable_pc(state)
      pc['unlocked'] = true
      pc['access_level'] = access_level.to_s
      pc['source'] = source.to_s

      WorldLink.queue_message(
        state,
        'qol_unlock',
        "Portable PC #{pc['access_level']} access unlocked by #{pc['source']}.",
        source: 'portable_pc',
        area_type: area_type
      )
    end

    def unlocked?(state)
      ensure_portable_pc(state)['unlocked'] == true
    end

    def open(state)
      return locked_result unless unlocked?(state)

      pc = ensure_portable_pc(state)
      pc['opened_count'] += 1
      summary(state).merge('status' => 'open')
    end

    def summary(state)
      {
        'status' => unlocked?(state) ? 'available' : 'locked',
        'access_level' => ensure_portable_pc(state)['access_level'],
        'party_species' => PartyStorage.party_species(state).dup,
        'pc_box_species' => PartyStorage.pc_box_species(state).dup,
        'party_count' => PartyStorage.party_species(state).length,
        'pc_count' => PartyStorage.pc_box_species(state).length,
        'party_limit' => PartyStorage::PARTY_LIMIT,
        'party_full' => PartyStorage.party_full?(state)
      }
    end

    def deposit(state, species)
      return locked_result(species) unless unlocked?(state)

      record_action(state, PartyStorage.deposit_species(state, species))
    end

    def withdraw(state, species)
      return locked_result(species) unless unlocked?(state)

      record_action(state, PartyStorage.withdraw_species(state, species))
    end

    def swap(state, party_species:, pc_species:)
      return locked_result unless unlocked?(state)

      record_action(
        state,
        PartyStorage.swap_species(
          state,
          party_species: party_species,
          pc_species: pc_species
        )
      )
    end

    def record_action(state, result)
      ensure_portable_pc(state)['last_action'] = result
      result
    end

    def locked_result(species = nil)
      result = { 'status' => 'locked' }
      result['species'] = species.to_s unless species.nil?
      result
    end
  end
end
