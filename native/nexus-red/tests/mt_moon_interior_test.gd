extends SceneTree


func _init() -> void:
	print("mt_moon_interior_test")
	var save_state_script := load("res://src/save/SaveState.gd")
	var entrance_scene := load("res://scenes/world/MtMoonEntrance.tscn")
	var interior_scene := load("res://scenes/world/MtMoonInterior1.tscn")

	if save_state_script == null or entrance_scene == null or interior_scene == null:
		push_error("Mt. Moon interior resources did not load.")
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
	save_state.enter_mt_moon_entrance()

	var entrance = entrance_scene.instantiate()
	entrance.save_state = save_state
	root.add_child(entrance)
	entrance._ready()

	var cave_entry_seen := [false]
	entrance.go_to_mt_moon_interior_1.connect(func() -> void:
		cave_entry_seen[0] = true
	)
	entrance.trigger_cave_entry()
	if cave_entry_seen[0]:
		push_error("Mt. Moon cave entry should stay locked before the faction conflict.")
		quit(1)
		return
	if entrance.dialogue_label == null or not entrance.dialogue_label.text.contains("conflict"):
		push_error("Locked cave entry should point back to the faction conflict.")
		quit(1)
		return

	save_state.record_mt_moon_faction_conflict()
	entrance.trigger_cave_entry()
	if not cave_entry_seen[0]:
		push_error("Mt. Moon entrance did not emit interior transition after faction conflict.")
		quit(1)
		return

	var interior = interior_scene.instantiate()
	interior.save_state = save_state
	root.add_child(interior)
	interior._ready()
	if save_state.current_scene != "mt_moon_interior_1":
		push_error("Mt. Moon interior did not update current scene.")
		quit(1)
		return
	if not save_state.story_flags.get("mt_moon_interior_1_reached", false):
		push_error("Mt. Moon interior reached flag missing.")
		quit(1)
		return
	if not save_state.story_flags.get("red_mt_moon_interior_support_seen", false):
		push_error("Red Mt. Moon interior support flag missing.")
		quit(1)
		return

	interior.trigger_split_path_scouting()
	if not save_state.story_flags.get("rocket_mt_moon_left_path_seen", false):
		push_error("Rocket left path flag missing.")
		quit(1)
		return
	if not save_state.story_flags.get("gold_dust_mt_moon_right_path_seen", false):
		push_error("Gold Dust right path flag missing.")
		quit(1)
		return
	if not save_state.story_flags.get("fossil_choice_setup_seen", false):
		push_error("Fossil choice setup flag missing.")
		quit(1)
		return
	if not save_state.worldlink_queue.has("wl_fossil_choice_setup"):
		push_error("WorldLink queue missing fossil choice setup.")
		quit(1)
		return
	if interior.dialogue_label == null:
		push_error("Mt. Moon interior dialogue label missing.")
		quit(1)
		return
	for required_text in ["Team Rocket", "Team Gold Dust", "Dome Fossil", "Helix Fossil", "Nexus Fossil"]:
		if not interior.dialogue_label.text.contains(required_text):
			push_error("Mt. Moon interior dialogue missing: " + required_text)
			quit(1)
			return

	var entrance_return_seen := [false]
	interior.go_to_mt_moon_entrance.connect(func() -> void:
		entrance_return_seen[0] = true
	)
	interior.return_to_mt_moon_entrance()
	if not entrance_return_seen[0]:
		push_error("Mt. Moon interior did not emit return to entrance.")
		quit(1)
		return

	interior.free()
	entrance.free()
	print("Native Mt. Moon interior smoke test passed.")
	quit(0)
