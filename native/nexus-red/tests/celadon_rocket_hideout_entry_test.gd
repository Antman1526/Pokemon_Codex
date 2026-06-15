extends SceneTree


func _init() -> void:
	print("celadon_rocket_hideout_entry_test")
	var save_state_script := load("res://src/save/SaveState.gd")
	var exterior_scene := load("res://scenes/world/CeladonGameCornerExterior.tscn")
	var hideout_scene := load("res://scenes/world/CeladonRocketHideoutEntry.tscn")

	if save_state_script == null or exterior_scene == null or hideout_scene == null:
		push_error("Celadon Rocket Hideout entry resources did not load.")
		quit(1)
		return

	var save_state = save_state_script.new()
	save_state.start_new_game("Antman")
	save_state.enter_celadon_game_corner_exterior()

	var exterior = exterior_scene.instantiate()
	exterior.save_state = save_state
	root.add_child(exterior)
	exterior._ready()

	var hideout_seen := [false]
	exterior.go_to_game_corner_hideout_entry.connect(func() -> void:
		hideout_seen[0] = true
	)

	exterior.trigger_game_corner_hideout_entry()
	if hideout_seen[0]:
		push_error("Rocket Hideout entry should stay locked before the poster-switch lead is unlocked.")
		quit(1)
		return
	if exterior.dialogue_label == null or not exterior.dialogue_label.text.contains("hideout"):
		push_error("Locked hideout entry did not explain the hideout switch.")
		quit(1)
		return

	save_state.set_flag("game_corner_hideout_entry_unlocked", true)
	exterior.trigger_game_corner_hideout_entry()
	if not hideout_seen[0]:
		push_error("Game Corner exterior did not emit Rocket Hideout entry after unlock.")
		quit(1)
		return

	var hideout = hideout_scene.instantiate()
	hideout.save_state = save_state
	root.add_child(hideout)
	hideout._ready()
	if save_state.current_scene != "celadon_rocket_hideout_entry":
		push_error("Rocket Hideout entry did not update current scene.")
		quit(1)
		return
	if not save_state.story_flags.get("celadon_rocket_hideout_entry_reached", false):
		push_error("Rocket Hideout entry reached flag missing.")
		quit(1)
		return
	if not save_state.worldlink_queue.has("wl_celadon_rocket_hideout_entry_reached"):
		push_error("WorldLink queue missing Rocket Hideout entry arrival.")
		quit(1)
		return

	hideout.trigger_rocket_hideout_entry_scene()
	for flag_name in [
		"red_hideout_entry_watch_seen",
		"bill_hideout_elevator_signal_seen",
		"rocket_lift_key_required_seen",
		"giovanni_hideout_command_seen",
		"team_moonlight_rocket_interference_seen",
		"rocket_hideout_b1f_path_unlocked",
	]:
		if not save_state.story_flags.get(flag_name, false):
			push_error("Rocket Hideout entry flag missing: " + flag_name)
			quit(1)
			return
	for queue_id in [
		"wl_red_hideout_entry_watch",
		"wl_bill_hideout_elevator_signal",
		"wl_rocket_lift_key_required",
		"wl_giovanni_hideout_command",
		"wl_team_moonlight_rocket_interference",
		"wl_rocket_hideout_b1f_path_unlocked",
	]:
		if not save_state.worldlink_queue.has(queue_id):
			push_error("WorldLink missing Rocket Hideout entry id: " + queue_id)
			quit(1)
			return
	for required_text in ["Red", "Bill", "Rocket", "Giovanni", "Moonlight", "elevator", "Lift Key", "Silph Scope", "Hideout"]:
		if hideout.dialogue_label == null or not hideout.dialogue_label.text.contains(required_text):
			push_error("Rocket Hideout entry dialogue missing: " + required_text)
			quit(1)
			return

	var b1f_seen := [false]
	hideout.go_to_rocket_hideout_b1f.connect(func() -> void:
		b1f_seen[0] = true
	)
	hideout.trigger_rocket_hideout_b1f_entry()
	if not b1f_seen[0]:
		push_error("Rocket Hideout entry did not emit the B1F path after scouting.")
		quit(1)
		return

	var returned := [false]
	hideout.go_to_game_corner_exterior.connect(func() -> void:
		returned[0] = true
	)
	hideout.return_to_game_corner_exterior()
	if not returned[0]:
		push_error("Rocket Hideout entry did not emit return to Game Corner exterior.")
		quit(1)
		return

	hideout.free()
	exterior.free()
	print("Native Celadon Rocket Hideout entry smoke test passed.")
	quit(0)
