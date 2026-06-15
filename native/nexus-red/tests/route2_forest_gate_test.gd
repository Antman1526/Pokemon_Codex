extends SceneTree


func _init() -> void:
	print("route2_forest_gate_test")
	var save_state_script := load("res://src/save/SaveState.gd")
	var viridian_scene := load("res://scenes/world/ViridianCity.tscn")
	var route2_scene := load("res://scenes/world/Route2ForestGate.tscn")

	if save_state_script == null or viridian_scene == null or route2_scene == null:
		push_error("Route 2 forest gate resources did not load.")
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
	save_state.enter_viridian_city()
	save_state.record_viridian_rocket_clue()

	var city = viridian_scene.instantiate()
	city.save_state = save_state
	root.add_child(city)
	city._ready()

	var transition_seen := [false]
	city.go_to_route_2_forest_gate.connect(func() -> void:
		transition_seen[0] = true
	)
	city.trigger_route_2_gate_entry()
	if not transition_seen[0]:
		push_error("Viridian did not emit Route 2 forest gate transition.")
		quit(1)
		return

	var route2 = route2_scene.instantiate()
	route2.save_state = save_state
	root.add_child(route2)
	route2._ready()
	if save_state.current_scene != "route_2_forest_gate":
		push_error("Route 2 forest gate did not update current scene.")
		quit(1)
		return
	if not save_state.story_flags.get("route_2_forest_gate_reached", false):
		push_error("Route 2 forest gate reached flag missing.")
		quit(1)
		return
	if not save_state.story_flags.get("red_route_2_warning_seen", false):
		push_error("Red Route 2 warning flag missing.")
		quit(1)
		return
	if route2.dialogue_label == null or not route2.dialogue_label.text.contains("Rocket activity"):
		push_error("Route 2 forest gate did not show Red Rocket warning.")
		quit(1)
		return

	var back_seen := [false]
	route2.go_to_viridian_city.connect(func() -> void:
		back_seen[0] = true
	)
	route2.return_to_viridian_city()
	if not back_seen[0]:
		push_error("Route 2 forest gate did not emit return to Viridian.")
		quit(1)
		return

	route2.free()
	city.free()
	print("Native Route 2 forest gate smoke test passed.")
	quit(0)
