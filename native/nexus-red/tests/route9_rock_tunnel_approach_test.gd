extends SceneTree


func _init() -> void:
	print("route9_rock_tunnel_approach_test")
	var save_state_script := load("res://src/save/SaveState.gd")
	var lab_scene := load("res://scenes/world/Route2EastFieldLab.tscn")
	var route9_scene := load("res://scenes/world/Route9RockTunnelApproach.tscn")

	if save_state_script == null or lab_scene == null or route9_scene == null:
		push_error("Route 9 Rock Tunnel approach resources did not load.")
		quit(1)
		return

	var save_state = save_state_script.new()
	save_state.start_new_game("Antman")
	save_state.enter_route_2_east_field_lab()

	var lab = lab_scene.instantiate()
	lab.save_state = save_state
	root.add_child(lab)
	lab._ready()

	var route9_seen := [false]
	lab.go_to_route_9_rock_tunnel_approach.connect(func() -> void:
		route9_seen[0] = true
	)

	lab.trigger_route_9_rock_tunnel_entry()
	if route9_seen[0]:
		push_error("Route 9 should stay locked before the field lab decodes the Rock Tunnel path.")
		quit(1)
		return
	if lab.dialogue_label == null or not lab.dialogue_label.text.contains("Rock Tunnel"):
		push_error("Locked Route 9 entry did not point back to Rock Tunnel prep.")
		quit(1)
		return

	lab.trigger_route_2_field_lab_scene()
	lab.trigger_route_9_rock_tunnel_entry()
	if not route9_seen[0]:
		push_error("Route 2 field lab did not emit Route 9 after the Rock Tunnel path unlock.")
		quit(1)
		return

	var route9 = route9_scene.instantiate()
	route9.save_state = save_state
	root.add_child(route9)
	route9._ready()
	if save_state.current_scene != "route_9_rock_tunnel_approach":
		push_error("Route 9 Rock Tunnel approach did not update current scene.")
		quit(1)
		return
	if not save_state.story_flags.get("route_9_rock_tunnel_approach_reached", false):
		push_error("Route 9 Rock Tunnel approach reached flag missing.")
		quit(1)
		return
	if not save_state.worldlink_queue.has("wl_route_9_rock_tunnel_approach_reached"):
		push_error("WorldLink queue missing Route 9 arrival.")
		quit(1)
		return

	route9.trigger_route_9_approach_scene()
	for flag_name in [
		"red_route_9_trainer_lane_seen",
		"bill_rock_tunnel_darkness_warning_seen",
		"team_moonlight_route_9_debut_seen",
		"rocket_route_9_supply_cache_seen",
		"lavender_tower_signal_confirmed",
		"rock_tunnel_entry_unlocked",
	]:
		if not save_state.story_flags.get(flag_name, false):
			push_error("Route 9 approach flag missing: " + flag_name)
			quit(1)
			return
	for queue_id in [
		"wl_red_route_9_trainer_lane",
		"wl_bill_rock_tunnel_darkness_warning",
		"wl_team_moonlight_route_9_debut",
		"wl_rocket_route_9_supply_cache",
		"wl_lavender_tower_signal_confirmed",
		"wl_rock_tunnel_entry_unlocked",
	]:
		if not save_state.worldlink_queue.has(queue_id):
			push_error("WorldLink missing Route 9 id: " + queue_id)
			quit(1)
			return
	for required_text in ["Red", "Bill", "Moonlight", "Rocket", "Lavender", "Rock Tunnel", "Echo Flute", "trainer lane"]:
		if route9.dialogue_label == null or not route9.dialogue_label.text.contains(required_text):
			push_error("Route 9 dialogue missing: " + required_text)
			quit(1)
			return

	var returned := [false]
	route9.go_to_route_2_east_field_lab.connect(func() -> void:
		returned[0] = true
	)
	route9.return_to_route_2_east_field_lab()
	if not returned[0]:
		push_error("Route 9 scene did not emit return to Route 2 field lab.")
		quit(1)
		return

	route9.free()
	lab.free()
	print("Native Route 9 Rock Tunnel approach smoke test passed.")
	quit(0)
