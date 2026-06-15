extends SceneTree


func _init() -> void:
	print("pewter_city_test")
	var save_state_script := load("res://src/save/SaveState.gd")
	var route3_scene := load("res://scenes/world/Route3.tscn")
	var pewter_scene := load("res://scenes/world/PewterCity.tscn")

	if save_state_script == null or route3_scene == null or pewter_scene == null:
		push_error("Pewter City resources did not load.")
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
	save_state.enter_route_3()

	var route3 = route3_scene.instantiate()
	route3.save_state = save_state
	root.add_child(route3)
	route3._ready()

	var pewter_transition_seen := [false]
	route3.go_to_pewter_city.connect(func() -> void:
		pewter_transition_seen[0] = true
	)
	route3.trigger_pewter_city_entry()
	if not pewter_transition_seen[0]:
		push_error("Route 3 did not emit Pewter City transition.")
		quit(1)
		return

	var pewter = pewter_scene.instantiate()
	pewter.save_state = save_state
	root.add_child(pewter)
	pewter._ready()
	if save_state.current_scene != "pewter_city":
		push_error("Pewter City did not update current scene.")
		quit(1)
		return
	if not save_state.story_flags.get("pewter_city_reached", false):
		push_error("Pewter City reached flag missing.")
		quit(1)
		return

	pewter.trigger_brock_intro()
	if not save_state.story_flags.get("brock_pewter_intro_seen", false):
		push_error("Brock intro flag missing.")
		quit(1)
		return
	if pewter.dialogue_label == null or not pewter.dialogue_label.text.contains("Brock:"):
		push_error("Pewter City did not show Brock dialogue.")
		quit(1)
		return

	pewter.trigger_red_training()
	if not save_state.story_flags.get("red_pewter_training_seen", false):
		push_error("Red Pewter training flag missing.")
		quit(1)
		return
	if not pewter.dialogue_label.text.contains("Red:"):
		push_error("Pewter City did not show Red training dialogue.")
		quit(1)
		return

	var back_seen := [false]
	pewter.go_to_route_3.connect(func() -> void:
		back_seen[0] = true
	)
	pewter.return_to_route_3()
	if not back_seen[0]:
		push_error("Pewter City did not emit return to Route 3.")
		quit(1)
		return

	pewter.free()
	route3.free()
	print("Native Pewter City smoke test passed.")
	quit(0)
