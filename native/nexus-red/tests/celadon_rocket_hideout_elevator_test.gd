extends SceneTree


func _init() -> void:
	print("celadon_rocket_hideout_elevator_test")
	var save_state_script := load("res://src/save/SaveState.gd")
	var b3f_scene := load("res://scenes/world/CeladonRocketHideoutB3F.tscn")
	var elevator_scene := load("res://scenes/world/CeladonRocketHideoutElevator.tscn")

	if save_state_script == null or b3f_scene == null or elevator_scene == null:
		push_error("Celadon Rocket Hideout elevator resources did not load.")
		quit(1)
		return

	var save_state = save_state_script.new()
	save_state.start_new_game("Antman")
	save_state.enter_celadon_rocket_hideout_b3f()

	var b3f = b3f_scene.instantiate()
	b3f.save_state = save_state
	root.add_child(b3f)
	b3f._ready()

	var elevator_seen := [false]
	b3f.go_to_rocket_hideout_elevator.connect(func() -> void:
		elevator_seen[0] = true
	)

	b3f.trigger_rocket_hideout_elevator_entry()
	if elevator_seen[0]:
		push_error("Rocket Hideout elevator should stay locked before the Lift Key is obtained.")
		quit(1)
		return
	if b3f.dialogue_label == null or not b3f.dialogue_label.text.contains("Lift Key"):
		push_error("Locked elevator path did not explain the Lift Key requirement.")
		quit(1)
		return

	save_state.start_battle_placeholder("rocket_hideout_b3f_admin")
	save_state.finish_battle_placeholder("placeholder_win")
	b3f.trigger_rocket_hideout_elevator_entry()
	if not elevator_seen[0]:
		push_error("Rocket Hideout B3F did not emit elevator path after Lift Key.")
		quit(1)
		return

	var elevator = elevator_scene.instantiate()
	elevator.save_state = save_state
	root.add_child(elevator)
	elevator._ready()
	if save_state.current_scene != "celadon_rocket_hideout_elevator":
		push_error("Rocket Hideout elevator did not update current scene.")
		quit(1)
		return
	if not save_state.story_flags.get("celadon_rocket_hideout_elevator_reached", false):
		push_error("Rocket Hideout elevator reached flag missing.")
		quit(1)
		return
	if not save_state.worldlink_queue.has("wl_celadon_rocket_hideout_elevator_reached"):
		push_error("WorldLink queue missing Rocket Hideout elevator arrival.")
		quit(1)
		return

	var command_floor_seen := [false]
	elevator.go_to_rocket_command_floor.connect(func() -> void:
		command_floor_seen[0] = true
	)
	elevator.trigger_rocket_command_floor_entry()
	if command_floor_seen[0]:
		push_error("Rocket command floor should stay locked before elevator routing is decoded.")
		quit(1)
		return

	elevator.trigger_rocket_hideout_elevator_scene()
	for flag_name in [
		"red_hideout_elevator_guard_seen",
		"bill_nexus_order_elevator_override_seen",
		"rocket_elevator_panel_restored_seen",
		"gold_dust_elevator_ledger_decoded_seen",
		"team_moonlight_elevator_sleep_signal_seen",
		"giovanni_command_floor_route_seen",
		"rocket_command_floor_path_unlocked",
	]:
		if not save_state.story_flags.get(flag_name, false):
			push_error("Rocket Hideout elevator flag missing: " + flag_name)
			quit(1)
			return
	for queue_id in [
		"wl_red_hideout_elevator_guard",
		"wl_bill_nexus_order_elevator_override",
		"wl_rocket_elevator_panel_restored",
		"wl_gold_dust_elevator_ledger_decoded",
		"wl_team_moonlight_elevator_sleep_signal",
		"wl_giovanni_command_floor_route_seen",
		"wl_rocket_command_floor_path_unlocked",
	]:
		if not save_state.worldlink_queue.has(queue_id):
			push_error("WorldLink missing Rocket Hideout elevator id: " + queue_id)
			quit(1)
			return
	for required_text in ["Red", "Bill", "Rocket", "Gold Dust", "Moonlight", "Nexus Order", "Giovanni", "elevator", "command floor"]:
		if elevator.dialogue_label == null or not elevator.dialogue_label.text.contains(required_text):
			push_error("Rocket Hideout elevator dialogue missing: " + required_text)
			quit(1)
			return

	elevator.trigger_rocket_command_floor_entry()
	if not command_floor_seen[0]:
		push_error("Rocket Hideout elevator did not emit command floor after decoding.")
		quit(1)
		return

	var returned := [false]
	elevator.go_to_rocket_hideout_b3f.connect(func() -> void:
		returned[0] = true
	)
	elevator.return_to_rocket_hideout_b3f()
	if not returned[0]:
		push_error("Rocket Hideout elevator did not emit return to B3F.")
		quit(1)
		return

	elevator.free()
	b3f.free()
	print("Native Celadon Rocket Hideout elevator smoke test passed.")
	quit(0)
