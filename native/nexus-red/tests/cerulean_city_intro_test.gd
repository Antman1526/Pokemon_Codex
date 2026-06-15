extends SceneTree


func _init() -> void:
	print("cerulean_city_intro_test")
	var save_state_script := load("res://src/save/SaveState.gd")
	var route4_scene := load("res://scenes/world/Route4CeruleanApproach.tscn")
	var cerulean_scene := load("res://scenes/world/CeruleanCity.tscn")

	if save_state_script == null or route4_scene == null or cerulean_scene == null:
		push_error("Cerulean City intro resources did not load.")
		quit(1)
		return

	var save_state = save_state_script.new()
	save_state.start_new_game("Antman")
	save_state.choose_starter({
		"player_starter": "Bulbasaur",
		"player_starter_group": "kanto",
		"blue_starter": "Charmander",
		"ava_starter": "Chikorita",
		"dax_starter": "Cyndaquil",
	})
	save_state.choose_mt_moon_fossil("dome")

	var route4 = route4_scene.instantiate()
	route4.save_state = save_state
	root.add_child(route4)
	route4._ready()

	var cerulean_transition_seen := [false]
	route4.go_to_cerulean_city.connect(func() -> void:
		cerulean_transition_seen[0] = true
	)
	route4.trigger_cerulean_city_entry()
	if cerulean_transition_seen[0]:
		push_error("Cerulean City entry should stay locked until Red's Route 4 warning is seen.")
		quit(1)
		return
	if route4.dialogue_label == null or not route4.dialogue_label.text.contains("talk this through"):
		push_error("Locked Cerulean City entry should point back to Red's Route 4 warning.")
		quit(1)
		return

	route4.trigger_red_cerulean_warning()
	route4.trigger_cerulean_city_entry()
	if not cerulean_transition_seen[0]:
		push_error("Route 4 did not emit Cerulean City transition after Red's warning.")
		quit(1)
		return

	var cerulean = cerulean_scene.instantiate()
	cerulean.save_state = save_state
	root.add_child(cerulean)
	cerulean._ready()
	if save_state.current_scene != "cerulean_city":
		push_error("Cerulean City did not update current scene.")
		quit(1)
		return
	if not save_state.story_flags.get("cerulean_city_reached", false):
		push_error("Cerulean City reached flag missing.")
		quit(1)
		return
	if save_state.worldlink_queue.has("wl_cerulean_city_reached") == false:
		push_error("WorldLink queue missing Cerulean City reached.")
		quit(1)
		return

	cerulean.trigger_misty_intro()
	if not save_state.story_flags.get("misty_cerulean_intro_seen", false):
		push_error("Misty Cerulean intro flag missing.")
		quit(1)
		return
	if not save_state.story_flags.get("nugget_bridge_threat_setup_seen", false):
		push_error("Nugget Bridge threat setup flag missing.")
		quit(1)
		return
	if save_state.worldlink_queue.has("wl_misty_cerulean_intro") == false:
		push_error("WorldLink queue missing Misty Cerulean intro.")
		quit(1)
		return
	for required_text in ["Misty", "Red", "Nugget Bridge", "Rocket", "Gold Dust"]:
		if not cerulean.dialogue_label.text.contains(required_text):
			push_error("Cerulean intro dialogue missing: " + required_text)
			quit(1)
			return

	var route4_return_seen := [false]
	cerulean.go_to_route_4_cerulean_approach.connect(func() -> void:
		route4_return_seen[0] = true
	)
	cerulean.return_to_route_4_cerulean_approach()
	if not route4_return_seen[0]:
		push_error("Cerulean City did not emit return to Route 4.")
		quit(1)
		return

	cerulean.free()
	route4.free()
	print("Native Cerulean City intro smoke test passed.")
	quit(0)
