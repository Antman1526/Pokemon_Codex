extends SceneTree


func _init() -> void:
	print("diglett_cave_detour_test")
	var save_state_script := load("res://src/save/SaveState.gd")
	var route11_scene := load("res://scenes/world/Route11.tscn")
	var cave_scene := load("res://scenes/world/DiglettCaveDetour.tscn")

	if save_state_script == null or route11_scene == null or cave_scene == null:
		push_error("Diglett's Cave detour resources did not load.")
		quit(1)
		return

	var save_state = save_state_script.new()
	save_state.start_new_game("Antman")
	save_state.set_flag("thunder_badge_earned", true)
	save_state.set_flag("route_11_path_unlocked", true)

	var route11 = route11_scene.instantiate()
	route11.save_state = save_state
	root.add_child(route11)
	route11._ready()

	var cave_seen := [false]
	route11.go_to_diglett_cave_detour.connect(func() -> void:
		cave_seen[0] = true
	)

	route11.trigger_diglett_cave_entry()
	if cave_seen[0]:
		push_error("Diglett's Cave should stay locked before the Route 11 handoff scene.")
		quit(1)
		return
	if route11.dialogue_label == null or not route11.dialogue_label.text.contains("Snorlax"):
		push_error("Locked Diglett's Cave entry did not point back to the Snorlax roadblock.")
		quit(1)
		return

	route11.trigger_route_11_handoff_scene()
	route11.trigger_diglett_cave_entry()
	if not cave_seen[0]:
		push_error("Route 11 did not emit Diglett's Cave after the roadblock handoff.")
		quit(1)
		return

	var cave = cave_scene.instantiate()
	cave.save_state = save_state
	root.add_child(cave)
	cave._ready()
	if save_state.current_scene != "diglett_cave_detour":
		push_error("Diglett's Cave detour did not update current scene.")
		quit(1)
		return
	if not save_state.story_flags.get("diglett_cave_detour_reached", false):
		push_error("Diglett's Cave detour reached flag missing.")
		quit(1)
		return
	if not save_state.worldlink_queue.has("wl_diglett_cave_detour_reached"):
		push_error("WorldLink queue missing Diglett's Cave arrival.")
		quit(1)
		return

	cave.trigger_diglett_cave_detour_scene()
	for flag_name in [
		"red_diglett_cave_guard_seen",
		"bill_diglett_cave_relay_map_seen",
		"rocket_gold_dust_cave_argument_seen",
		"snorlax_route_12_block_confirmed",
		"echo_flute_lead_seen",
	]:
		if not save_state.story_flags.get(flag_name, false):
			push_error("Diglett's Cave detour flag missing: " + flag_name)
			quit(1)
			return
	for queue_id in [
		"wl_red_diglett_cave_guard",
		"wl_bill_diglett_cave_relay_map",
		"wl_rocket_gold_dust_cave_argument",
		"wl_snorlax_route_12_block_confirmed",
		"wl_echo_flute_lead_seen",
	]:
		if not save_state.worldlink_queue.has(queue_id):
			push_error("WorldLink missing Diglett's Cave id: " + queue_id)
			quit(1)
			return
	for required_text in ["Red", "Bill", "Rocket", "Gold Dust", "Snorlax", "Echo Flute", "Nexus", "Diglett"]:
		if cave.dialogue_label == null or not cave.dialogue_label.text.contains(required_text):
			push_error("Diglett's Cave dialogue missing: " + required_text)
			quit(1)
			return

	var returned := [false]
	cave.go_to_route_11.connect(func() -> void:
		returned[0] = true
	)
	cave.return_to_route_11()
	if not returned[0]:
		push_error("Diglett's Cave scene did not emit return to Route 11.")
		quit(1)
		return

	cave.free()
	route11.free()
	print("Native Diglett's Cave detour smoke test passed.")
	quit(0)
