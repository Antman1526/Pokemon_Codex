extends SceneTree


func _init() -> void:
	print("pokemon_tower_first_floor_test")
	var save_state_script := load("res://src/save/SaveState.gd")
	var lavender_scene := load("res://scenes/world/LavenderOutskirts.tscn")
	var tower_scene := load("res://scenes/world/PokemonTowerFirstFloor.tscn")

	if save_state_script == null or lavender_scene == null or tower_scene == null:
		push_error("Pokemon Tower first floor resources did not load.")
		quit(1)
		return

	var save_state = save_state_script.new()
	save_state.start_new_game("Antman")
	save_state.enter_lavender_outskirts()

	var lavender = lavender_scene.instantiate()
	lavender.save_state = save_state
	root.add_child(lavender)
	lavender._ready()

	var tower_seen := [false]
	lavender.go_to_pokemon_tower_first_floor.connect(func() -> void:
		tower_seen[0] = true
	)

	lavender.trigger_pokemon_tower_entry()
	if tower_seen[0]:
		push_error("Pokemon Tower should stay locked before Lavender outskirts scene is complete.")
		quit(1)
		return
	if lavender.dialogue_label == null or not lavender.dialogue_label.text.contains("Pokemon Tower"):
		push_error("Locked Pokemon Tower entry did not point back to the tower signal.")
		quit(1)
		return

	lavender.trigger_lavender_outskirts_scene()
	lavender.trigger_pokemon_tower_entry()
	if not tower_seen[0]:
		push_error("Lavender did not emit Pokemon Tower after entry unlock.")
		quit(1)
		return

	var tower = tower_scene.instantiate()
	tower.save_state = save_state
	root.add_child(tower)
	tower._ready()
	if save_state.current_scene != "pokemon_tower_first_floor":
		push_error("Pokemon Tower first floor did not update current scene.")
		quit(1)
		return
	if not save_state.story_flags.get("pokemon_tower_first_floor_reached", false):
		push_error("Pokemon Tower first floor reached flag missing.")
		quit(1)
		return
	if not save_state.worldlink_queue.has("wl_pokemon_tower_first_floor_reached"):
		push_error("WorldLink queue missing Pokemon Tower first floor arrival.")
		quit(1)
		return

	tower.trigger_pokemon_tower_first_floor_scene()
	for flag_name in [
		"red_pokemon_tower_guard_seen",
		"bill_tower_echo_flute_distortion_seen",
		"team_moonlight_tower_pressure_seen",
		"rocket_tower_grunt_seen",
		"cubone_mr_fuji_thread_seen",
		"silph_scope_need_seen",
		"pokemon_tower_deeper_path_locked",
	]:
		if not save_state.story_flags.get(flag_name, false):
			push_error("Pokemon Tower first floor flag missing: " + flag_name)
			quit(1)
			return
	for queue_id in [
		"wl_red_pokemon_tower_guard",
		"wl_bill_tower_echo_flute_distortion",
		"wl_team_moonlight_tower_pressure",
		"wl_rocket_tower_grunt_seen",
		"wl_cubone_mr_fuji_thread",
		"wl_silph_scope_need_seen",
		"wl_pokemon_tower_deeper_path_locked",
	]:
		if not save_state.worldlink_queue.has(queue_id):
			push_error("WorldLink missing Pokemon Tower id: " + queue_id)
			quit(1)
			return
	for required_text in ["Red", "Bill", "Moonlight", "Rocket", "Pokemon Tower", "Echo Flute", "Cubone", "Mr. Fuji", "Silph Scope"]:
		if tower.dialogue_label == null or not tower.dialogue_label.text.contains(required_text):
			push_error("Pokemon Tower dialogue missing: " + required_text)
			quit(1)
			return

	tower.trigger_deeper_tower_path()
	if tower.dialogue_label == null or not tower.dialogue_label.text.contains("Silph Scope"):
		push_error("Locked deeper tower path did not require the Silph Scope.")
		quit(1)
		return

	var returned := [false]
	tower.go_to_lavender_outskirts.connect(func() -> void:
		returned[0] = true
	)
	tower.return_to_lavender_outskirts()
	if not returned[0]:
		push_error("Pokemon Tower scene did not emit return to Lavender outskirts.")
		quit(1)
		return

	tower.free()
	lavender.free()
	print("Native Pokemon Tower first floor smoke test passed.")
	quit(0)
