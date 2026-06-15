extends SceneTree


func _init() -> void:
	print("route11_handoff_test")
	var save_state_script := load("res://src/save/SaveState.gd")
	var sabotage_scene := load("res://scenes/world/VermilionPowerSabotage.tscn")
	var route11_scene := load("res://scenes/world/Route11.tscn")

	if save_state_script == null or sabotage_scene == null or route11_scene == null:
		push_error("Route 11 handoff resources did not load.")
		quit(1)
		return

	var save_state = save_state_script.new()
	save_state.start_new_game("Antman")
	save_state.enter_vermilion_power_sabotage()

	var sabotage = sabotage_scene.instantiate()
	sabotage.save_state = save_state
	root.add_child(sabotage)
	sabotage._ready()

	var route11_seen := [false]
	sabotage.go_to_route_11.connect(func() -> void:
		route11_seen[0] = true
	)

	sabotage.trigger_route_11_entry()
	if route11_seen[0]:
		push_error("Route 11 should stay locked before the Thunder Badge.")
		quit(1)
		return
	if sabotage.dialogue_label == null or not sabotage.dialogue_label.text.contains("Thunder Badge"):
		push_error("Locked Route 11 entry did not point back to the Thunder Badge.")
		quit(1)
		return

	save_state.set_flag("thunder_badge_earned", true)
	save_state.set_flag("route_11_path_unlocked", true)
	sabotage.trigger_route_11_entry()
	if not route11_seen[0]:
		push_error("Power sabotage scene did not emit Route 11 after Thunder Badge.")
		quit(1)
		return

	var route11 = route11_scene.instantiate()
	route11.save_state = save_state
	root.add_child(route11)
	route11._ready()
	if save_state.current_scene != "route_11":
		push_error("Route 11 scene did not update current scene.")
		quit(1)
		return
	if not save_state.story_flags.get("route_11_reached", false):
		push_error("Route 11 reached flag missing.")
		quit(1)
		return
	if not save_state.worldlink_queue.has("wl_route_11_reached"):
		push_error("WorldLink queue missing Route 11 arrival.")
		quit(1)
		return

	route11.trigger_route_11_handoff_scene()
	for flag_name in [
		"red_route_11_eastbound_scene_seen",
		"misty_route_11_farewell_seen",
		"bill_route_11_signal_decode_seen",
		"rocket_gas_route_11_fallout_seen",
		"snorlax_roadblock_teased",
	]:
		if not save_state.story_flags.get(flag_name, false):
			push_error("Route 11 handoff flag missing: " + flag_name)
			quit(1)
			return
	for queue_id in [
		"wl_red_route_11_eastbound_scene",
		"wl_misty_route_11_farewell",
		"wl_bill_route_11_signal_decode",
		"wl_rocket_gas_route_11_fallout",
		"wl_snorlax_roadblock_teased",
	]:
		if not save_state.worldlink_queue.has(queue_id):
			push_error("WorldLink missing Route 11 id: " + queue_id)
			quit(1)
			return
	for required_text in ["Red", "Misty", "Bill", "Rocket", "Team Gas", "Snorlax", "Nexus"]:
		if route11.dialogue_label == null or not route11.dialogue_label.text.contains(required_text):
			push_error("Route 11 dialogue missing: " + required_text)
			quit(1)
			return

	var returned := [false]
	route11.go_to_vermilion_power_sabotage.connect(func() -> void:
		returned[0] = true
	)
	route11.return_to_vermilion_power_sabotage()
	if not returned[0]:
		push_error("Route 11 scene did not emit return to Vermilion power sabotage.")
		quit(1)
		return

	route11.free()
	sabotage.free()
	print("Native Route 11 handoff smoke test passed.")
	quit(0)
