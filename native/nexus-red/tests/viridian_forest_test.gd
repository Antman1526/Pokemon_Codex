extends SceneTree


func _init() -> void:
	print("viridian_forest_test")
	var save_state_script := load("res://src/save/SaveState.gd")
	var route2_scene := load("res://scenes/world/Route2ForestGate.tscn")
	var forest_scene := load("res://scenes/world/ViridianForest.tscn")

	if save_state_script == null or route2_scene == null or forest_scene == null:
		push_error("Viridian Forest resources did not load.")
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
	save_state.enter_route_2_forest_gate()

	var route2 = route2_scene.instantiate()
	route2.save_state = save_state
	root.add_child(route2)
	route2._ready()

	var forest_transition_seen := [false]
	route2.go_to_viridian_forest.connect(func() -> void:
		forest_transition_seen[0] = true
	)
	route2.trigger_viridian_forest_entry()
	if not forest_transition_seen[0]:
		push_error("Route 2 did not emit Viridian Forest transition.")
		quit(1)
		return

	var forest = forest_scene.instantiate()
	forest.save_state = save_state
	root.add_child(forest)
	forest._ready()
	if save_state.current_scene != "viridian_forest":
		push_error("Viridian Forest did not update current scene.")
		quit(1)
		return
	if not save_state.story_flags.get("viridian_forest_reached", false):
		push_error("Viridian Forest reached flag missing.")
		quit(1)
		return
	if not save_state.story_flags.get("red_viridian_forest_scene_seen", false):
		push_error("Red Viridian Forest scene flag missing.")
		quit(1)
		return

	forest.trigger_rocket_scout_scene()
	if not save_state.story_flags.get("rocket_forest_scout_seen", false):
		push_error("Rocket forest scout flag missing.")
		quit(1)
		return
	if forest.dialogue_label == null or not forest.dialogue_label.text.contains("Rocket scout"):
		push_error("Viridian Forest did not show Rocket scout dialogue.")
		quit(1)
		return

	var route3_seen := [false]
	forest.go_to_route_3.connect(func() -> void:
		route3_seen[0] = true
	)
	forest.exit_to_route_3()
	if not route3_seen[0]:
		push_error("Viridian Forest did not emit Route 3 transition.")
		quit(1)
		return

	var back_seen := [false]
	forest.go_to_route_2_forest_gate.connect(func() -> void:
		back_seen[0] = true
	)
	forest.return_to_route_2_forest_gate()
	if not back_seen[0]:
		push_error("Viridian Forest did not emit return to Route 2 forest gate.")
		quit(1)
		return

	forest.free()
	route2.free()
	print("Native Viridian Forest smoke test passed.")
	quit(0)
