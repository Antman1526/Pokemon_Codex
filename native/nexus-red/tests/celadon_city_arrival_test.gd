extends SceneTree


func _init() -> void:
	print("celadon_city_arrival_test")
	var save_state_script := load("res://src/save/SaveState.gd")
	var underground_scene := load("res://scenes/world/CeladonUndergroundPath.tscn")
	var celadon_scene := load("res://scenes/world/CeladonCity.tscn")

	if save_state_script == null or underground_scene == null or celadon_scene == null:
		push_error("Celadon City arrival resources did not load.")
		quit(1)
		return

	var save_state = save_state_script.new()
	save_state.start_new_game("Antman")
	save_state.enter_celadon_underground_path()

	var underground = underground_scene.instantiate()
	underground.save_state = save_state
	root.add_child(underground)
	underground._ready()

	var city_seen := [false]
	underground.go_to_celadon_city.connect(func() -> void:
		city_seen[0] = true
	)

	underground.trigger_celadon_city_entry()
	if city_seen[0]:
		push_error("Celadon City should stay locked before the Underground Path scene unlocks arrival.")
		quit(1)
		return
	if underground.dialogue_label == null or not underground.dialogue_label.text.contains("Celadon"):
		push_error("Locked Celadon City entry did not explain the Celadon path.")
		quit(1)
		return

	underground.trigger_celadon_underground_path_scene()
	underground.trigger_celadon_city_entry()
	if not city_seen[0]:
		push_error("Celadon Underground Path did not emit Celadon City after unlock.")
		quit(1)
		return

	var celadon = celadon_scene.instantiate()
	celadon.save_state = save_state
	root.add_child(celadon)
	celadon._ready()
	if save_state.current_scene != "celadon_city":
		push_error("Celadon City did not update current scene.")
		quit(1)
		return
	if not save_state.story_flags.get("celadon_city_reached", false):
		push_error("Celadon City reached flag missing.")
		quit(1)
		return
	if not save_state.worldlink_queue.has("wl_celadon_city_reached"):
		push_error("WorldLink queue missing Celadon City arrival.")
		quit(1)
		return

	celadon.trigger_celadon_city_arrival_scene()
	for flag_name in [
		"red_celadon_city_arrival_seen",
		"bill_game_corner_exterior_signal_seen",
		"rocket_game_corner_front_seen",
		"team_moonlight_celadon_ad_seen",
		"erika_gym_teased_seen",
		"game_corner_investigation_unlocked",
	]:
		if not save_state.story_flags.get(flag_name, false):
			push_error("Celadon City arrival flag missing: " + flag_name)
			quit(1)
			return
	for queue_id in [
		"wl_red_celadon_city_arrival",
		"wl_bill_game_corner_exterior_signal",
		"wl_rocket_game_corner_front",
		"wl_team_moonlight_celadon_ad",
		"wl_erika_gym_teased",
		"wl_game_corner_investigation_unlocked",
	]:
		if not save_state.worldlink_queue.has(queue_id):
			push_error("WorldLink missing Celadon City arrival id: " + queue_id)
			quit(1)
			return
	for required_text in ["Red", "Bill", "Rocket", "Moonlight", "Celadon", "Game Corner", "Silph Scope", "Erika"]:
		if celadon.dialogue_label == null or not celadon.dialogue_label.text.contains(required_text):
			push_error("Celadon City dialogue missing: " + required_text)
			quit(1)
			return

	var returned := [false]
	celadon.go_to_celadon_underground_path.connect(func() -> void:
		returned[0] = true
	)
	celadon.return_to_celadon_underground_path()
	if not returned[0]:
		push_error("Celadon City did not emit return to Celadon Underground Path.")
		quit(1)
		return

	celadon.free()
	underground.free()
	print("Native Celadon City arrival smoke test passed.")
	quit(0)
