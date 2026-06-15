# frozen_string_literal: true

module NexusRed
  module FieldHealing
    module_function

    def ensure_field_healing(state)
      state['field_healing'] ||= {
        'unlocked' => false,
        'source' => nil,
        'charges' => 0,
        'max_charges' => 0,
        'usage_history' => [],
        'last_result' => nil
      }
    end

    def unlock(state, source:, charges: 3, area_type: 'route')
      healing = ensure_field_healing(state)
      healing['unlocked'] = true
      healing['source'] = source.to_s
      healing['charges'] = charges.to_i
      healing['max_charges'] = [healing['max_charges'].to_i, charges.to_i].max

      WorldLink.queue_message(
        state,
        'qol_unlock',
        "Field healing unlocked by #{healing['source']}.",
        source: 'field_healing',
        area_type: area_type
      )
    end

    def policy(state)
      GameplayOptions.ensure_options(state).dig('difficulty_profile', 'portable_healing') || 'limited'
    end

    def available?(state, area_type: 'route')
      return false unless ensure_field_healing(state)['unlocked']
      return false if restricted_area?(state, area_type)
      return true unless charge_required?(state)

      ensure_field_healing(state)['charges'].to_i.positive?
    end

    def set_party_condition(state, species, hp_percent:, status:)
      party_conditions(state)[species.to_s] = {
        'hp_percent' => hp_percent.to_i,
        'status' => status.to_s
      }
    end

    def heal_team(state, location:, area_type: 'route')
      guard = availability_guard(state, area_type)
      return record_result(state, guard) unless guard.nil?

      species = PartyStorage.party_species(state)
      species.each { |name| restore_condition(state, name) }
      consume_charge(state)
      record_result(
        state,
        {
          'status' => 'healed',
          'policy' => policy(state),
          'location' => location.to_s,
          'healed_species' => species.dup,
          'charges_remaining' => ensure_field_healing(state)['charges']
        }
      )
    end

    def restore_species(state, species, location:, area_type: 'route')
      name = species.to_s
      return record_result(state, missing_result(name)) unless PartyStorage.party_species(state).include?(name)

      guard = availability_guard(state, area_type)
      return record_result(state, guard) unless guard.nil?

      restore_condition(state, name)
      consume_charge(state)
      record_result(
        state,
        {
          'status' => 'restored',
          'policy' => policy(state),
          'location' => location.to_s,
          'species' => name,
          'charges_remaining' => ensure_field_healing(state)['charges']
        }
      )
    end

    def party_conditions(state)
      state['party_conditions'] ||= {}
    end

    def restore_condition(state, species)
      party_conditions(state)[species.to_s] = {
        'hp_percent' => 100,
        'status' => 'ok'
      }
    end

    def availability_guard(state, area_type)
      healing = ensure_field_healing(state)
      return { 'status' => 'locked' } unless healing['unlocked']
      return { 'status' => 'restricted_area', 'policy' => policy(state), 'area_type' => area_type.to_s } if restricted_area?(state, area_type)
      return { 'status' => 'no_charges', 'policy' => policy(state), 'charges_remaining' => healing['charges'] } if charge_required?(state) && !healing['charges'].to_i.positive?

      nil
    end

    def restricted_area?(state, area_type)
      policy(state) == 'restricted' && SeedData.worldlink_paused_area?(area_type)
    end

    def charge_required?(state)
      %w[limited restricted player_selected].include?(policy(state))
    end

    def consume_charge(state)
      return unless charge_required?(state)

      healing = ensure_field_healing(state)
      healing['charges'] = [healing['charges'].to_i - 1, 0].max
    end

    def record_result(state, result)
      healing = ensure_field_healing(state)
      healing['last_result'] = result
      if %w[healed restored].include?(result['status'])
        healing['usage_history'] << {
          'status' => result['status'],
          'location' => result['location'],
          'policy' => result['policy'],
          'charges_remaining' => result['charges_remaining']
        }
      end
      result
    end

    def missing_result(species)
      {
        'status' => 'missing_from_party',
        'species' => species
      }
    end
  end
end
