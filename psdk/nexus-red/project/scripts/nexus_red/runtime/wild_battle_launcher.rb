# frozen_string_literal: true

module NexusRed
  module WildBattleLauncher
    module_function

    def launch_pending_request(state)
      request = MapEventBridge.consume_pending_battle_request(state)
      return { 'status' => 'no_pending_battle' } if request.nil?

      payload = build_launch_payload(request)
      launch_history(state) << payload
      state['last_wild_battle_launch'] = payload
      payload
    end

    def execute_pending_request(state)
      payload = launch_pending_request(state)
      return payload unless payload['status'] == 'launch_prepared' && psdk_runtime_available?

      execute_launch_payload(payload)
      payload['status'] = 'battle_scene_called'
      state['last_wild_battle_launch'] = payload
      launch_history(state)[-1] = payload
      payload
    end

    def execute_launch_payload(payload)
      battle_info = Battle::Logic::BattleInfo.new
      battle_info.add_party(0, *battle_info.player_basic_info)
      party = [
        PFM::Pokemon.generate_from_hash(
          id: payload['psdk_species_symbol'].to_sym,
          level: payload['level'].to_i
        )
      ]
      battle_info.add_party(1, party)
      $scene.call_scene(Battle::Scene, battle_info)
      battle_info
    end

    def build_launch_payload(request)
      species_key = request['psdk_species_key'].to_s
      level = request['level'].to_i
      raise ArgumentError, 'Cannot launch wild battle without a PSDK species key' if species_key.empty?
      raise ArgumentError, "Invalid wild battle level: #{request['level']}" unless level.positive?

      {
        'status' => 'launch_prepared',
        'psdk_command_family' => 'wild_battle',
        'psdk_binding_strategy' => 'battle_info_wild_party',
        'psdk_runtime_available' => psdk_runtime_available?,
        'source_event_id' => request['event_id'],
        'route_id' => request['route_id'],
        'route_name' => request['route_name'],
        'psdk_map_id' => request['psdk_map_id'],
        'species' => request['species'],
        'species_key' => species_key,
        'psdk_species_symbol' => species_symbol(species_key),
        'level' => level,
        'encounter_id' => request['encounter_id'],
        'channel' => request['channel'],
        'battle_kind' => request['kind'],
        'tags' => request['tags'].dup,
        'psdk_script_lines' => build_psdk_script_lines(species_key, level)
      }
    end

    def build_psdk_script_lines(species_key, level)
      symbol = species_symbol(species_key)
      [
        'bi = Battle::Logic::BattleInfo.new',
        'bi.add_party(0, *bi.player_basic_info)',
        'party = []',
        "party << PFM::Pokemon.generate_from_hash(id: :#{symbol}, level: #{level.to_i})",
        'bi.add_party(1, party)',
        '$scene.call_scene(Battle::Scene, bi)'
      ]
    end

    def species_symbol(species_key)
      species_key.to_s.downcase
    end

    def psdk_runtime_available?
      defined?(Battle::Logic::BattleInfo) && defined?(PFM::Pokemon) && defined?(Battle::Scene) && defined?($scene)
    end

    def launch_history(state)
      state['wild_battle_launch_history'] ||= []
    end
  end
end
