extends SceneTree


func _init() -> void:
	print("mt_moon_fossil_decision_test")
	var save_state_script := load("res://src/save/SaveState.gd")
	var interior_scene := load("res://scenes/world/MtMoonInterior1.tscn")
	var decision_scene := load("res://scenes/world/MtMoonFossilDecision.tscn")

	if save_state_script == null or interior_scene == null or decision_scene == null:
		push_error("Mt. Moon fossil decision resources did not load.")
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
	save_state.enter_mt_moon_interior_1()

	var interior = interior_scene.instantiate()
	interior.save_state = save_state
	root.add_child(interior)
	interior._ready()

	var decision_seen := [false]
	interior.go_to_mt_moon_fossil_decision.connect(func() -> void:
		decision_seen[0] = true
	)
	interior.trigger_fossil_decision_scene()
	if decision_seen[0]:
		push_error("Fossil decision should stay locked before both faction battles are finished.")
		quit(1)
		return
	if interior.dialogue_label == null or not interior.dialogue_label.text.contains("both"):
		push_error("Locked fossil decision should mention both faction battles.")
		quit(1)
		return

	save_state.start_battle_placeholder("mt_moon_rocket_left_path")
	save_state.finish_battle_placeholder("placeholder_win")
	save_state.start_battle_placeholder("mt_moon_gold_dust_right_path")
	save_state.finish_battle_placeholder("placeholder_win")
	interior.trigger_fossil_decision_scene()
	if not decision_seen[0]:
		push_error("Mt. Moon interior did not emit fossil decision transition.")
		quit(1)
		return

	var decision = decision_scene.instantiate()
	decision.save_state = save_state
	root.add_child(decision)
	decision._ready()
	if save_state.current_scene != "mt_moon_fossil_decision":
		push_error("Fossil decision scene did not update current scene.")
		quit(1)
		return
	if not save_state.story_flags.get("mt_moon_fossil_decision_reached", false):
		push_error("Fossil decision reached flag missing.")
		quit(1)
		return
	if not save_state.story_flags.get("nexus_fossil_deeper_signal_seen", false):
		push_error("Nexus Fossil deeper signal flag missing.")
		quit(1)
		return

	decision.choose_dome_fossil()
	if not save_state.story_flags.get("mt_moon_fossil_choice_made", false):
		push_error("Fossil choice made flag missing.")
		quit(1)
		return
	if not save_state.story_flags.get("dome_fossil_chosen", false):
		push_error("Dome Fossil choice flag missing.")
		quit(1)
		return
	if save_state.story_flags.get("helix_fossil_chosen", false):
		push_error("Helix Fossil should not be chosen after choosing Dome Fossil.")
		quit(1)
		return
	if save_state.worldlink_queue.has("wl_mt_moon_fossil_choice_made") == false:
		push_error("WorldLink queue missing fossil choice made.")
		quit(1)
		return
	for required_text in ["Dome Fossil", "Helix Fossil", "Nexus Fossil"]:
		if not decision.dialogue_label.text.contains(required_text):
			push_error("Fossil decision dialogue missing: " + required_text)
			quit(1)
			return

	var interior_return_seen := [false]
	decision.go_to_mt_moon_interior_1.connect(func() -> void:
		interior_return_seen[0] = true
	)
	decision.return_to_mt_moon_interior_1()
	if not interior_return_seen[0]:
		push_error("Fossil decision did not emit return to Mt. Moon interior.")
		quit(1)
		return

	decision.free()
	interior.free()
	print("Native Mt. Moon fossil decision smoke test passed.")
	quit(0)
