extends SceneTree


func _init() -> void:
	print("celadon_rocket_hideout_b1f_test")
	var save_state_script := load("res://src/save/SaveState.gd")
	var entry_scene := load("res://scenes/world/CeladonRocketHideoutEntry.tscn")
	var b1f_scene := load("res://scenes/world/CeladonRocketHideoutB1F.tscn")

	if save_state_script == null or entry_scene == null or b1f_scene == null:
		push_error("Celadon Rocket Hideout B1F resources did not load.")
		quit(1)
		return

	var save_state = save_state_script.new()
	save_state.start_new_game("Antman")
	save_state.enter_celadon_rocket_hideout_entry()

	var entry = entry_scene.instantiate()
	entry.save_state = save_state
	root.add_child(entry)
	entry._ready()

	var b1f_seen := [false]
	entry.go_to_rocket_hideout_b1f.connect(func() -> void:
		b1f_seen[0] = true
	)

	entry.trigger_rocket_hideout_b1f_entry()
	if b1f_seen[0]:
		push_error("Rocket Hideout B1F should stay locked before the entry scene is mapped.")
		quit(1)
		return
	if entry.dialogue_label == null or not entry.dialogue_label.text.contains("Lift Key"):
		push_error("Locked B1F path did not explain the Lift Key/elevator scouting requirement.")
		quit(1)
		return

	entry.trigger_rocket_hideout_entry_scene()
	entry.trigger_rocket_hideout_b1f_entry()
	if not b1f_seen[0]:
		push_error("Rocket Hideout entry did not emit B1F after the entry scene unlock.")
		quit(1)
		return

	var b1f = b1f_scene.instantiate()
	b1f.save_state = save_state
	root.add_child(b1f)
	b1f._ready()
	if save_state.current_scene != "celadon_rocket_hideout_b1f":
		push_error("Rocket Hideout B1F did not update current scene.")
		quit(1)
		return
	if not save_state.story_flags.get("celadon_rocket_hideout_b1f_reached", false):
		push_error("Rocket Hideout B1F reached flag missing.")
		quit(1)
		return
	if not save_state.worldlink_queue.has("wl_celadon_rocket_hideout_b1f_reached"):
		push_error("WorldLink queue missing Rocket Hideout B1F arrival.")
		quit(1)
		return

	b1f.trigger_rocket_hideout_b1f_scene()
	for flag_name in [
		"red_hideout_b1f_maze_guard_seen",
		"bill_silph_scope_machine_trace_seen",
		"rocket_spinner_maze_seen",
		"gold_dust_hideout_infiltration_seen",
		"team_moonlight_hideout_signal_bleed_seen",
		"lift_key_deeper_trail_seen",
		"rocket_hideout_b2f_path_unlocked",
	]:
		if not save_state.story_flags.get(flag_name, false):
			push_error("Rocket Hideout B1F flag missing: " + flag_name)
			quit(1)
			return
	for queue_id in [
		"wl_red_hideout_b1f_maze_guard",
		"wl_bill_silph_scope_machine_trace",
		"wl_rocket_spinner_maze",
		"wl_gold_dust_hideout_infiltration",
		"wl_team_moonlight_hideout_signal_bleed",
		"wl_lift_key_deeper_trail",
		"wl_rocket_hideout_b2f_path_unlocked",
	]:
		if not save_state.worldlink_queue.has(queue_id):
			push_error("WorldLink missing Rocket Hideout B1F id: " + queue_id)
			quit(1)
			return
	for required_text in ["Red", "Bill", "Rocket", "Gold Dust", "Moonlight", "spinner", "Silph Scope", "Lift Key", "B2F"]:
		if b1f.dialogue_label == null or not b1f.dialogue_label.text.contains(required_text):
			push_error("Rocket Hideout B1F dialogue missing: " + required_text)
			quit(1)
			return

	var b2f_seen := [false]
	b1f.go_to_rocket_hideout_b2f.connect(func() -> void:
		b2f_seen[0] = true
	)
	b1f.trigger_rocket_hideout_b2f_entry()
	if not b2f_seen[0]:
		push_error("Rocket Hideout B1F did not emit the B2F path after scouting.")
		quit(1)
		return

	var returned := [false]
	b1f.go_to_rocket_hideout_entry.connect(func() -> void:
		returned[0] = true
	)
	b1f.return_to_rocket_hideout_entry()
	if not returned[0]:
		push_error("Rocket Hideout B1F did not emit return to hideout entry.")
		quit(1)
		return

	b1f.free()
	entry.free()
	print("Native Celadon Rocket Hideout B1F smoke test passed.")
	quit(0)
