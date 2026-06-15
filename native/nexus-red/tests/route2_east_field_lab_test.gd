extends SceneTree


func _init() -> void:
	print("route2_east_field_lab_test")
	var save_state_script := load("res://src/save/SaveState.gd")
	var cave_scene := load("res://scenes/world/DiglettCaveDetour.tscn")
	var lab_scene := load("res://scenes/world/Route2EastFieldLab.tscn")

	if save_state_script == null or cave_scene == null or lab_scene == null:
		push_error("Route 2 east field lab resources did not load.")
		quit(1)
		return

	var save_state = save_state_script.new()
	save_state.start_new_game("Antman")
	save_state.enter_diglett_cave_detour()

	var cave = cave_scene.instantiate()
	cave.save_state = save_state
	root.add_child(cave)
	cave._ready()

	var lab_seen := [false]
	cave.go_to_route_2_east_field_lab.connect(func() -> void:
		lab_seen[0] = true
	)

	cave.trigger_route_2_east_field_lab_entry()
	if lab_seen[0]:
		push_error("Route 2 east field lab should stay locked before the Echo Flute lead.")
		quit(1)
		return
	if cave.dialogue_label == null or not cave.dialogue_label.text.contains("Echo Flute"):
		push_error("Locked Route 2 field lab entry did not point back to the Echo Flute lead.")
		quit(1)
		return

	cave.trigger_diglett_cave_detour_scene()
	cave.trigger_route_2_east_field_lab_entry()
	if not lab_seen[0]:
		push_error("Diglett's Cave did not emit Route 2 field lab after the Echo Flute lead.")
		quit(1)
		return

	var lab = lab_scene.instantiate()
	lab.save_state = save_state
	root.add_child(lab)
	lab._ready()
	if save_state.current_scene != "route_2_east_field_lab":
		push_error("Route 2 east field lab did not update current scene.")
		quit(1)
		return
	if not save_state.story_flags.get("route_2_east_field_lab_reached", false):
		push_error("Route 2 east field lab reached flag missing.")
		quit(1)
		return
	if not save_state.worldlink_queue.has("wl_route_2_east_field_lab_reached"):
		push_error("WorldLink queue missing Route 2 field lab arrival.")
		quit(1)
		return

	lab.trigger_route_2_field_lab_scene()
	for flag_name in [
		"red_route_2_east_exit_seen",
		"bill_echo_flute_decoder_seen",
		"oak_aide_field_tool_brief_seen",
		"rocket_moonlight_sleep_signal_seen",
		"lavender_signal_path_teased",
		"route_9_rock_tunnel_path_unlocked",
	]:
		if not save_state.story_flags.get(flag_name, false):
			push_error("Route 2 field lab flag missing: " + flag_name)
			quit(1)
			return
	for queue_id in [
		"wl_red_route_2_east_exit",
		"wl_bill_echo_flute_decoder",
		"wl_oak_aide_field_tool_brief",
		"wl_rocket_moonlight_sleep_signal",
		"wl_lavender_signal_path_teased",
		"wl_route_9_rock_tunnel_path_unlocked",
	]:
		if not save_state.worldlink_queue.has(queue_id):
			push_error("WorldLink missing Route 2 field lab id: " + queue_id)
			quit(1)
			return
	for required_text in ["Red", "Bill", "Oak", "Rocket", "Moonlight", "Echo Flute", "Lavender", "Rock Tunnel"]:
		if lab.dialogue_label == null or not lab.dialogue_label.text.contains(required_text):
			push_error("Route 2 field lab dialogue missing: " + required_text)
			quit(1)
			return

	var returned := [false]
	lab.go_to_diglett_cave_detour.connect(func() -> void:
		returned[0] = true
	)
	lab.return_to_diglett_cave_detour()
	if not returned[0]:
		push_error("Route 2 field lab scene did not emit return to Diglett's Cave.")
		quit(1)
		return

	lab.free()
	cave.free()
	print("Native Route 2 east field lab smoke test passed.")
	quit(0)
