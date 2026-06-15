extends SceneTree


func _init() -> void:
	print("route4_cerulean_approach_test")
	var save_state_script := load("res://src/save/SaveState.gd")
	var decision_scene := load("res://scenes/world/MtMoonFossilDecision.tscn")
	var route4_scene := load("res://scenes/world/Route4CeruleanApproach.tscn")

	if save_state_script == null or decision_scene == null or route4_scene == null:
		push_error("Route 4 Cerulean approach resources did not load.")
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
	save_state.enter_mt_moon_fossil_decision()

	var decision = decision_scene.instantiate()
	decision.save_state = save_state
	root.add_child(decision)
	decision._ready()

	var route4_transition_seen := [false]
	decision.go_to_route_4_cerulean_approach.connect(func() -> void:
		route4_transition_seen[0] = true
	)
	decision.proceed_to_route_4_cerulean_approach()
	if route4_transition_seen[0]:
		push_error("Route 4 transition should stay locked until a fossil is chosen.")
		quit(1)
		return
	if decision.dialogue_label == null or not decision.dialogue_label.text.contains("choose one fossil"):
		push_error("Locked Route 4 transition should remind the player to choose one fossil.")
		quit(1)
		return

	decision.choose_helix_fossil()
	decision.proceed_to_route_4_cerulean_approach()
	if not route4_transition_seen[0]:
		push_error("Fossil decision did not emit Route 4 transition after choosing a fossil.")
		quit(1)
		return

	var route4 = route4_scene.instantiate()
	route4.save_state = save_state
	root.add_child(route4)
	route4._ready()
	if save_state.current_scene != "route_4_cerulean_approach":
		push_error("Route 4 Cerulean approach did not update current scene.")
		quit(1)
		return
	if not save_state.story_flags.get("route_4_cerulean_approach_reached", false):
		push_error("Route 4 Cerulean approach reached flag missing.")
		quit(1)
		return
	if save_state.worldlink_queue.has("wl_route_4_cerulean_approach") == false:
		push_error("WorldLink queue missing Route 4 approach arrival.")
		quit(1)
		return

	route4.trigger_red_cerulean_warning()
	if not save_state.story_flags.get("red_route_4_cerulean_warning_seen", false):
		push_error("Red Route 4 Cerulean warning flag missing.")
		quit(1)
		return
	if not save_state.story_flags.get("cerulean_bridge_threat_teased", false):
		push_error("Cerulean bridge threat tease flag missing.")
		quit(1)
		return
	if save_state.worldlink_queue.has("wl_red_route_4_cerulean_warning") == false:
		push_error("WorldLink queue missing Red Route 4 warning.")
		quit(1)
		return
	for required_text in ["Red", "Cerulean", "Misty", "Rocket", "Gold Dust"]:
		if not route4.dialogue_label.text.contains(required_text):
			push_error("Route 4 dialogue missing: " + required_text)
			quit(1)
			return

	var return_seen := [false]
	route4.go_to_mt_moon_fossil_decision.connect(func() -> void:
		return_seen[0] = true
	)
	route4.return_to_mt_moon_fossil_decision()
	if not return_seen[0]:
		push_error("Route 4 approach did not emit return to fossil decision.")
		quit(1)
		return

	route4.free()
	decision.free()
	print("Native Route 4 Cerulean approach smoke test passed.")
	quit(0)
