extends SceneTree


func _init() -> void:
	print("pokemon_tower_fuji_rescue_test")
	var save_state_script := load("res://src/save/SaveState.gd")
	var silph_scope_scene := load("res://scenes/world/PokemonTowerSilphScopeFloor.tscn")
	var fuji_scene := load("res://scenes/world/PokemonTowerFujiRescue.tscn")
	var battle_scene := load("res://scenes/battle/BattlePlaceholder.tscn")

	if save_state_script == null or silph_scope_scene == null or fuji_scene == null or battle_scene == null:
		push_error("Pokemon Tower Fuji rescue resources did not load.")
		quit(1)
		return

	var save_state = save_state_script.new()
	save_state.start_new_game("Antman")
	save_state.enter_pokemon_tower_silph_scope_floor()

	var silph_floor = silph_scope_scene.instantiate()
	silph_floor.save_state = save_state
	root.add_child(silph_floor)
	silph_floor._ready()

	var rescue_seen := [false]
	silph_floor.go_to_pokemon_tower_fuji_rescue.connect(func() -> void:
		rescue_seen[0] = true
	)

	silph_floor.trigger_fuji_rescue_path()
	if rescue_seen[0]:
		push_error("Fuji rescue path should stay locked before Silph Scope floor is resolved.")
		quit(1)
		return
	if silph_floor.dialogue_label == null or not silph_floor.dialogue_label.text.contains("Mr. Fuji"):
		push_error("Locked Fuji rescue path did not point back to Mr. Fuji.")
		quit(1)
		return

	silph_floor.trigger_pokemon_tower_silph_scope_floor_scene()
	silph_floor.trigger_fuji_rescue_path()
	if not rescue_seen[0]:
		push_error("Silph Scope floor did not emit Fuji rescue after rescue path unlock.")
		quit(1)
		return

	var fuji = fuji_scene.instantiate()
	fuji.save_state = save_state
	root.add_child(fuji)
	fuji._ready()
	if save_state.current_scene != "pokemon_tower_fuji_rescue":
		push_error("Pokemon Tower Fuji rescue did not update current scene.")
		quit(1)
		return
	if not save_state.story_flags.get("pokemon_tower_fuji_rescue_reached", false):
		push_error("Pokemon Tower Fuji rescue reached flag missing.")
		quit(1)
		return
	if not save_state.worldlink_queue.has("wl_pokemon_tower_fuji_rescue_reached"):
		push_error("WorldLink queue missing Pokemon Tower Fuji rescue arrival.")
		quit(1)
		return

	fuji.trigger_pokemon_tower_fuji_rescue_scene()
	for flag_name in [
		"red_fuji_rescue_guard_seen",
		"bill_fuji_signal_clean_seen",
		"rocket_tower_fuji_guard_seen",
		"team_moonlight_retreat_signal_seen",
		"fuji_rescue_battle_unlocked",
	]:
		if not save_state.story_flags.get(flag_name, false):
			push_error("Pokemon Tower Fuji rescue setup flag missing: " + flag_name)
			quit(1)
			return
	for queue_id in [
		"wl_red_fuji_rescue_guard",
		"wl_bill_fuji_signal_clean",
		"wl_rocket_tower_fuji_guard_seen",
		"wl_team_moonlight_retreat_signal",
		"wl_fuji_rescue_battle_unlocked",
	]:
		if not save_state.worldlink_queue.has(queue_id):
			push_error("WorldLink missing Pokemon Tower Fuji rescue setup id: " + queue_id)
			quit(1)
			return
	for required_text in ["Red", "Bill", "Rocket", "Moonlight", "Mr. Fuji", "Poke Flute", "Snorlax"]:
		if fuji.dialogue_label == null or not fuji.dialogue_label.text.contains(required_text):
			push_error("Pokemon Tower Fuji rescue dialogue missing: " + required_text)
			quit(1)
			return

	var battle_seen := [false]
	fuji.start_battle_placeholder.connect(func(battle_id: String) -> void:
		battle_seen[0] = true
		if battle_id != "rocket_tower_fuji_guard":
			push_error("Fuji rescue emitted wrong battle id: " + battle_id)
			quit(1)
	)
	fuji.trigger_fuji_rescue_battle()
	if not battle_seen[0]:
		push_error("Pokemon Tower Fuji rescue did not emit Rocket guard battle.")
		quit(1)
		return
	if save_state.active_battle_id != "rocket_tower_fuji_guard":
		push_error("Rocket tower Fuji guard battle was not active in save state.")
		quit(1)
		return
	if not save_state.story_flags.get("rocket_tower_fuji_guard_battle_started", false):
		push_error("Rocket tower Fuji guard battle started flag missing.")
		quit(1)
		return

	var battle = battle_scene.instantiate()
	battle.save_state = save_state
	battle.battle_id = "rocket_tower_fuji_guard"
	root.add_child(battle)
	battle._ready()
	battle.finish_placeholder_battle()
	save_state.finish_battle_placeholder("placeholder_win")
	for flag_name in [
		"rocket_tower_fuji_guard_battle_finished",
		"mr_fuji_rescued",
		"poke_flute_obtained",
		"snorlax_wake_path_unlocked",
	]:
		if not save_state.story_flags.get(flag_name, false):
			push_error("Pokemon Tower Fuji rescue reward flag missing: " + flag_name)
			quit(1)
			return
	for queue_id in [
		"wl_rocket_tower_fuji_guard_battle_finished",
		"wl_mr_fuji_rescued",
		"wl_poke_flute_obtained",
		"wl_snorlax_wake_path_unlocked",
	]:
		if not save_state.worldlink_queue.has(queue_id):
			push_error("WorldLink missing Pokemon Tower Fuji rescue reward id: " + queue_id)
			quit(1)
			return

	var returned := [false]
	fuji.go_to_pokemon_tower_silph_scope_floor.connect(func() -> void:
		returned[0] = true
	)
	fuji.return_to_pokemon_tower_silph_scope_floor()
	if not returned[0]:
		push_error("Pokemon Tower Fuji rescue did not emit return to Silph Scope floor.")
		quit(1)
		return

	battle.free()
	fuji.free()
	silph_floor.free()
	print("Native Pokemon Tower Fuji rescue smoke test passed.")
	quit(0)
