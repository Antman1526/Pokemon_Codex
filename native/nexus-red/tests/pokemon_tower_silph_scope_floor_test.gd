extends SceneTree


func _init() -> void:
	print("pokemon_tower_silph_scope_floor_test")
	var save_state_script := load("res://src/save/SaveState.gd")
	var first_floor_scene := load("res://scenes/world/PokemonTowerFirstFloor.tscn")
	var silph_scope_scene := load("res://scenes/world/PokemonTowerSilphScopeFloor.tscn")

	if save_state_script == null or first_floor_scene == null or silph_scope_scene == null:
		push_error("Pokemon Tower Silph Scope floor resources did not load.")
		quit(1)
		return

	var save_state = save_state_script.new()
	save_state.start_new_game("Antman")
	save_state.enter_pokemon_tower_first_floor()

	var first_floor = first_floor_scene.instantiate()
	first_floor.save_state = save_state
	root.add_child(first_floor)
	first_floor._ready()

	var deeper_seen := [false]
	first_floor.go_to_pokemon_tower_silph_scope_floor.connect(func() -> void:
		deeper_seen[0] = true
	)

	first_floor.trigger_deeper_tower_path()
	if deeper_seen[0]:
		push_error("Pokemon Tower deeper path should stay locked before Silph Scope is obtained.")
		quit(1)
		return
	if first_floor.dialogue_label == null or not first_floor.dialogue_label.text.contains("Silph Scope"):
		push_error("Locked deeper tower path did not require the Silph Scope.")
		quit(1)
		return

	save_state.set_flag("silph_scope_obtained", true)
	save_state.set_flag("pokemon_tower_deeper_path_unlocked", true)
	first_floor.trigger_deeper_tower_path()
	if not deeper_seen[0]:
		push_error("Pokemon Tower first floor did not emit Silph Scope floor after unlock.")
		quit(1)
		return

	var silph_floor = silph_scope_scene.instantiate()
	silph_floor.save_state = save_state
	root.add_child(silph_floor)
	silph_floor._ready()
	if save_state.current_scene != "pokemon_tower_silph_scope_floor":
		push_error("Pokemon Tower Silph Scope floor did not update current scene.")
		quit(1)
		return
	if not save_state.story_flags.get("pokemon_tower_silph_scope_floor_reached", false):
		push_error("Pokemon Tower Silph Scope floor reached flag missing.")
		quit(1)
		return
	if not save_state.worldlink_queue.has("wl_pokemon_tower_silph_scope_floor_reached"):
		push_error("WorldLink queue missing Pokemon Tower Silph Scope floor arrival.")
		quit(1)
		return

	silph_floor.trigger_pokemon_tower_silph_scope_floor_scene()
	for flag_name in [
		"red_silph_scope_guard_seen",
		"bill_silph_scope_reading_seen",
		"marowak_spirit_revealed",
		"cubone_grief_scene_seen",
		"team_moonlight_tower_ritual_seen",
		"rocket_mr_fuji_hold_seen",
		"mr_fuji_rescue_path_unlocked",
		"poke_flute_lead_unlocked",
	]:
		if not save_state.story_flags.get(flag_name, false):
			push_error("Pokemon Tower Silph Scope floor flag missing: " + flag_name)
			quit(1)
			return
	for queue_id in [
		"wl_red_silph_scope_guard",
		"wl_bill_silph_scope_reading",
		"wl_marowak_spirit_revealed",
		"wl_cubone_grief_scene",
		"wl_team_moonlight_tower_ritual",
		"wl_rocket_mr_fuji_hold",
		"wl_mr_fuji_rescue_path_unlocked",
		"wl_poke_flute_lead_unlocked",
	]:
		if not save_state.worldlink_queue.has(queue_id):
			push_error("WorldLink missing Pokemon Tower Silph Scope floor id: " + queue_id)
			quit(1)
			return
	for required_text in ["Red", "Bill", "Silph Scope", "Marowak", "Cubone", "Mr. Fuji", "Rocket", "Moonlight", "Poke Flute"]:
		if silph_floor.dialogue_label == null or not silph_floor.dialogue_label.text.contains(required_text):
			push_error("Pokemon Tower Silph Scope floor dialogue missing: " + required_text)
			quit(1)
			return

	var returned := [false]
	silph_floor.go_to_pokemon_tower_first_floor.connect(func() -> void:
		returned[0] = true
	)
	silph_floor.return_to_pokemon_tower_first_floor()
	if not returned[0]:
		push_error("Pokemon Tower Silph Scope floor did not emit return to first floor.")
		quit(1)
		return

	silph_floor.free()
	first_floor.free()
	print("Native Pokemon Tower Silph Scope floor smoke test passed.")
	quit(0)
