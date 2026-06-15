extends SceneTree


func _init() -> void:
	print("route3_migration_scene_test")
	var save_state_script := load("res://src/save/SaveState.gd")
	var route2_scene := load("res://scenes/world/Route2ForestGate.tscn")
	var route3_scene := load("res://scenes/world/Route3.tscn")

	if save_state_script == null or route2_scene == null or route3_scene == null:
		push_error("Route 3 migration scene resources did not load.")
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

	var route3_transition_seen := [false]
	route2.go_to_route_3.connect(func() -> void:
		route3_transition_seen[0] = true
	)
	route2.trigger_route_3_entry()
	if not route3_transition_seen[0]:
		push_error("Route 2 did not emit Route 3 transition.")
		quit(1)
		return

	var route3 = route3_scene.instantiate()
	route3.save_state = save_state
	root.add_child(route3)
	route3._ready()
	if save_state.current_scene != "route_3":
		push_error("Route 3 did not update current scene.")
		quit(1)
		return
	if not save_state.story_flags.get("route_3_reached", false):
		push_error("Route 3 reached flag missing.")
		quit(1)
		return
	if not save_state.story_flags.get("red_route_3_migration_scene_seen", false):
		push_error("Route 3 Red migration flag missing.")
		quit(1)
		return

	var migration_seen := [false]
	route3.start_wild_encounter.connect(func(encounter_data: Dictionary) -> void:
		migration_seen[0] = true
		if encounter_data.get("id", "") != "route_3_migration_chespin":
			push_error("Route 3 emitted the wrong migration encounter.")
			quit(1)
	)
	route3.trigger_route_3_migration_encounter()
	if not migration_seen[0]:
		push_error("Route 3 did not emit migration encounter.")
		quit(1)
		return
	if save_state.active_encounter_id != "route_3_migration_chespin":
		push_error("Route 3 migration encounter was not active in save state.")
		quit(1)
		return
	if save_state.encounter_return_scene != "route_3":
		push_error("Route 3 migration encounter did not return to Route 3.")
		quit(1)
		return
	save_state.finish_wild_encounter("catch_success")
	if not save_state.captured_creatures.has("Chespin"):
		push_error("Route 3 migration catch did not record Chespin.")
		quit(1)
		return

	var back_seen := [false]
	route3.go_to_route_2_forest_gate.connect(func() -> void:
		back_seen[0] = true
	)
	route3.return_to_route_2_forest_gate()
	if not back_seen[0]:
		push_error("Route 3 did not emit return to Route 2 forest gate.")
		quit(1)
		return

	route3.free()
	route2.free()
	print("Native Route 3 migration scene smoke test passed.")
	quit(0)
