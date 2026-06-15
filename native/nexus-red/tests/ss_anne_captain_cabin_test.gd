extends SceneTree


func _init() -> void:
	print("ss_anne_captain_cabin_test")
	var save_state_script := load("res://src/save/SaveState.gd")
	var cargo_scene := load("res://scenes/world/SSAnneCargoHold.tscn")
	var captain_scene := load("res://scenes/world/SSAnneCaptainCabin.tscn")

	if save_state_script == null or cargo_scene == null or captain_scene == null:
		push_error("S.S. Anne Captain cabin resources did not load.")
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
	save_state.enter_ss_anne_cargo_hold()

	var cargo = cargo_scene.instantiate()
	cargo.save_state = save_state
	root.add_child(cargo)
	cargo._ready()

	var captain_seen := [false]
	cargo.go_to_ss_anne_captain_cabin.connect(func() -> void:
		captain_seen[0] = true
	)

	cargo.trigger_captain_cabin_entry()
	if captain_seen[0]:
		push_error("Captain cabin should stay locked before the cargo investigation.")
		quit(1)
		return
	if cargo.dialogue_label == null or not cargo.dialogue_label.text.contains("cargo manifest"):
		push_error("Locked Captain cabin did not point back to the cargo manifest.")
		quit(1)
		return

	save_state.record_ss_anne_cargo_hold_investigation()
	cargo.trigger_captain_cabin_entry()
	if not captain_seen[0]:
		push_error("Cargo hold did not emit Captain cabin transition after investigation.")
		quit(1)
		return

	var captain = captain_scene.instantiate()
	captain.save_state = save_state
	root.add_child(captain)
	captain._ready()
	if save_state.current_scene != "ss_anne_captain_cabin":
		push_error("Captain cabin did not update current scene.")
		quit(1)
		return
	if not save_state.story_flags.get("ss_anne_captain_cabin_reached", false):
		push_error("Captain cabin reached flag missing.")
		quit(1)
		return
	if not save_state.worldlink_queue.has("wl_ss_anne_captain_cabin_reached"):
		push_error("WorldLink queue missing Captain cabin arrival.")
		quit(1)
		return

	captain.trigger_captain_cabin_scene()
	for flag_name in [
		"captain_seasick_scene_seen",
		"trail_cutter_obtained",
		"trail_cutter_field_tool_unlocked",
		"surge_gym_access_unlocked",
	]:
		if not save_state.story_flags.get(flag_name, false):
			push_error("Captain cabin flag missing: " + flag_name)
			quit(1)
			return
	for queue_id in [
		"wl_captain_seasick_scene_seen",
		"wl_trail_cutter_obtained",
		"wl_trail_cutter_field_tool_unlocked",
		"wl_surge_gym_access_unlocked",
	]:
		if not save_state.worldlink_queue.has(queue_id):
			push_error("WorldLink missing Captain cabin id: " + queue_id)
			quit(1)
			return
	for required_text in ["Red", "Misty", "Bill", "Captain", "Trail Cutter", "Surge"]:
		if captain.dialogue_label == null or not captain.dialogue_label.text.contains(required_text):
			push_error("Captain cabin dialogue missing: " + required_text)
			quit(1)
			return

	var returned := [false]
	captain.go_to_ss_anne_cargo_hold.connect(func() -> void:
		returned[0] = true
	)
	captain.return_to_cargo_hold()
	if not returned[0]:
		push_error("Captain cabin did not emit return to cargo hold.")
		quit(1)
		return

	captain.free()
	cargo.free()
	print("Native S.S. Anne Captain cabin smoke test passed.")
	quit(0)
