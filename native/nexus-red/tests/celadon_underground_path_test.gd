extends SceneTree


func _init() -> void:
	print("celadon_underground_path_test")
	var save_state_script := load("res://src/save/SaveState.gd")
	var route8_scene := load("res://scenes/world/Route8CeladonRoad.tscn")
	var underground_scene := load("res://scenes/world/CeladonUndergroundPath.tscn")

	if save_state_script == null or route8_scene == null or underground_scene == null:
		push_error("Celadon Underground Path resources did not load.")
		quit(1)
		return

	var save_state = save_state_script.new()
	save_state.start_new_game("Antman")
	save_state.enter_route_8_celadon_road()

	var route8 = route8_scene.instantiate()
	route8.save_state = save_state
	root.add_child(route8)
	route8._ready()

	var underground_seen := [false]
	route8.go_to_celadon_underground_path.connect(func() -> void:
		underground_seen[0] = true
	)

	route8.trigger_celadon_underground_entry()
	if underground_seen[0]:
		push_error("Celadon Underground Path should stay locked before Route 8 scouting is complete.")
		quit(1)
		return
	if route8.dialogue_label == null or not route8.dialogue_label.text.contains("Underground Path"):
		push_error("Locked Underground Path entry did not point back to Route 8 scouting.")
		quit(1)
		return

	route8.trigger_route_8_celadon_road_scene()
	route8.trigger_celadon_underground_entry()
	if not underground_seen[0]:
		push_error("Route 8 did not emit Celadon Underground Path after unlock.")
		quit(1)
		return

	var underground = underground_scene.instantiate()
	underground.save_state = save_state
	root.add_child(underground)
	underground._ready()
	if save_state.current_scene != "celadon_underground_path":
		push_error("Celadon Underground Path did not update current scene.")
		quit(1)
		return
	if not save_state.story_flags.get("celadon_underground_path_reached", false):
		push_error("Celadon Underground Path reached flag missing.")
		quit(1)
		return
	if not save_state.worldlink_queue.has("wl_celadon_underground_path_reached"):
		push_error("WorldLink queue missing Celadon Underground Path arrival.")
		quit(1)
		return

	underground.trigger_celadon_underground_path_scene()
	for flag_name in [
		"red_celadon_underpass_guard_seen",
		"bill_game_corner_signal_trace_seen",
		"rocket_underpass_smuggler_seen",
		"team_moonlight_dream_poster_seen",
		"silph_scope_game_corner_confirmed",
		"celadon_city_arrival_unlocked",
	]:
		if not save_state.story_flags.get(flag_name, false):
			push_error("Celadon Underground Path flag missing: " + flag_name)
			quit(1)
			return
	for queue_id in [
		"wl_red_celadon_underpass_guard",
		"wl_bill_game_corner_signal_trace",
		"wl_rocket_underpass_smuggler",
		"wl_team_moonlight_dream_poster",
		"wl_silph_scope_game_corner_confirmed",
		"wl_celadon_city_arrival_unlocked",
	]:
		if not save_state.worldlink_queue.has(queue_id):
			push_error("WorldLink missing Celadon Underground Path id: " + queue_id)
			quit(1)
			return
	for required_text in ["Red", "Bill", "Rocket", "Moonlight", "Celadon", "Game Corner", "Silph Scope", "Underground Path"]:
		if underground.dialogue_label == null or not underground.dialogue_label.text.contains(required_text):
			push_error("Celadon Underground Path dialogue missing: " + required_text)
			quit(1)
			return

	var returned := [false]
	underground.go_to_route_8_celadon_road.connect(func() -> void:
		returned[0] = true
	)
	underground.return_to_route_8_celadon_road()
	if not returned[0]:
		push_error("Celadon Underground Path did not emit return to Route 8.")
		quit(1)
		return

	underground.free()
	route8.free()
	print("Native Celadon Underground Path smoke test passed.")
	quit(0)
