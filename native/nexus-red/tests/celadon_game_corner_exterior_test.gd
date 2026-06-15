extends SceneTree


func _init() -> void:
	print("celadon_game_corner_exterior_test")
	var save_state_script := load("res://src/save/SaveState.gd")
	var city_scene := load("res://scenes/world/CeladonCity.tscn")
	var exterior_scene := load("res://scenes/world/CeladonGameCornerExterior.tscn")
	var battle_scene := load("res://scenes/battle/BattlePlaceholder.tscn")

	if save_state_script == null or city_scene == null or exterior_scene == null or battle_scene == null:
		push_error("Celadon Game Corner exterior resources did not load.")
		quit(1)
		return

	var save_state = save_state_script.new()
	save_state.start_new_game("Antman")
	save_state.enter_celadon_city()

	var city = city_scene.instantiate()
	city.save_state = save_state
	root.add_child(city)
	city._ready()

	var exterior_seen := [false]
	city.go_to_game_corner_exterior.connect(func() -> void:
		exterior_seen[0] = true
	)

	city.trigger_game_corner_exterior_entry()
	if exterior_seen[0]:
		push_error("Game Corner exterior should stay locked before Celadon scouting is complete.")
		quit(1)
		return
	if city.dialogue_label == null or not city.dialogue_label.text.contains("Game Corner"):
		push_error("Locked Game Corner exterior entry did not explain the Game Corner path.")
		quit(1)
		return

	city.trigger_celadon_city_arrival_scene()
	city.trigger_game_corner_exterior_entry()
	if not exterior_seen[0]:
		push_error("Celadon City did not emit Game Corner exterior after investigation unlock.")
		quit(1)
		return

	var exterior = exterior_scene.instantiate()
	exterior.save_state = save_state
	root.add_child(exterior)
	exterior._ready()
	if save_state.current_scene != "celadon_game_corner_exterior":
		push_error("Game Corner exterior did not update current scene.")
		quit(1)
		return
	if not save_state.story_flags.get("game_corner_exterior_reached", false):
		push_error("Game Corner exterior reached flag missing.")
		quit(1)
		return
	if not save_state.worldlink_queue.has("wl_game_corner_exterior_reached"):
		push_error("WorldLink queue missing Game Corner exterior arrival.")
		quit(1)
		return

	exterior.trigger_game_corner_exterior_scene()
	for flag_name in [
		"red_game_corner_door_guard_seen",
		"bill_coin_case_signal_seen",
		"rocket_game_corner_guard_exposed",
		"team_moonlight_sleep_coin_seen",
		"game_corner_guard_battle_unlocked",
	]:
		if not save_state.story_flags.get(flag_name, false):
			push_error("Game Corner exterior flag missing: " + flag_name)
			quit(1)
			return
	for required_text in ["Red", "Bill", "Rocket", "Moonlight", "Game Corner", "Coin Case", "Silph Scope"]:
		if exterior.dialogue_label == null or not exterior.dialogue_label.text.contains(required_text):
			push_error("Game Corner exterior dialogue missing: " + required_text)
			quit(1)
			return

	var battle_seen := [false]
	exterior.start_battle_placeholder.connect(func(battle_id: String) -> void:
		battle_seen[0] = true
		if battle_id != "rocket_game_corner_guard":
			push_error("Game Corner exterior emitted wrong battle id: " + battle_id)
			quit(1)
	)
	exterior.trigger_game_corner_guard_battle()
	if not battle_seen[0]:
		push_error("Game Corner exterior did not emit the Rocket guard battle.")
		quit(1)
		return
	if save_state.active_battle_id != "rocket_game_corner_guard":
		push_error("Rocket Game Corner guard battle was not active in save state.")
		quit(1)
		return
	if not save_state.story_flags.get("rocket_game_corner_guard_battle_started", false):
		push_error("Rocket Game Corner guard battle started flag missing.")
		quit(1)
		return

	var battle = battle_scene.instantiate()
	battle.save_state = save_state
	battle.battle_id = "rocket_game_corner_guard"
	root.add_child(battle)
	battle._ready()
	battle.finish_placeholder_battle()
	save_state.finish_battle_placeholder("placeholder_win")
	if not save_state.story_flags.get("rocket_game_corner_guard_battle_finished", false):
		push_error("Rocket Game Corner guard battle finished flag missing.")
		quit(1)
		return
	if not save_state.story_flags.get("rocket_hideout_switch_lead_seen", false):
		push_error("Rocket hideout switch lead flag missing.")
		quit(1)
		return
	if not save_state.story_flags.get("game_corner_hideout_entry_unlocked", false):
		push_error("Game Corner hideout entry unlock flag missing.")
		quit(1)
		return
	for queue_id in [
		"wl_rocket_game_corner_guard_battle_finished",
		"wl_rocket_hideout_switch_lead_seen",
		"wl_game_corner_hideout_entry_unlocked",
	]:
		if not save_state.worldlink_queue.has(queue_id):
			push_error("WorldLink missing Game Corner post-battle id: " + queue_id)
			quit(1)
			return

	var hideout_seen := [false]
	exterior.go_to_game_corner_hideout_entry.connect(func() -> void:
		hideout_seen[0] = true
	)
	exterior.trigger_game_corner_hideout_entry()
	if not hideout_seen[0]:
		push_error("Game Corner exterior did not emit the hideout-entry lead after guard battle.")
		quit(1)
		return

	var returned := [false]
	exterior.go_to_celadon_city.connect(func() -> void:
		returned[0] = true
	)
	exterior.return_to_celadon_city()
	if not returned[0]:
		push_error("Game Corner exterior did not emit return to Celadon City.")
		quit(1)
		return

	battle.free()
	exterior.free()
	city.free()
	print("Native Celadon Game Corner exterior smoke test passed.")
	quit(0)
