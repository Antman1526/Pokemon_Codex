extends SceneTree


func _init() -> void:
	print("rock_tunnel_interior_test")
	var save_state_script := load("res://src/save/SaveState.gd")
	var route9_scene := load("res://scenes/world/Route9RockTunnelApproach.tscn")
	var tunnel_scene := load("res://scenes/world/RockTunnelInterior.tscn")

	if save_state_script == null or route9_scene == null or tunnel_scene == null:
		push_error("Rock Tunnel interior resources did not load.")
		quit(1)
		return

	var save_state = save_state_script.new()
	save_state.start_new_game("Antman")
	save_state.enter_route_9_rock_tunnel_approach()

	var route9 = route9_scene.instantiate()
	route9.save_state = save_state
	root.add_child(route9)
	route9._ready()

	var tunnel_seen := [false]
	route9.go_to_rock_tunnel_interior.connect(func() -> void:
		tunnel_seen[0] = true
	)

	route9.trigger_rock_tunnel_entry()
	if tunnel_seen[0]:
		push_error("Rock Tunnel should stay locked before Route 9 scouting is complete.")
		quit(1)
		return
	if route9.dialogue_label == null or not route9.dialogue_label.text.contains("Rock Tunnel"):
		push_error("Locked Rock Tunnel entry did not point back to route scouting.")
		quit(1)
		return

	route9.trigger_route_9_approach_scene()
	route9.trigger_rock_tunnel_entry()
	if not tunnel_seen[0]:
		push_error("Route 9 did not emit Rock Tunnel after entry unlock.")
		quit(1)
		return

	var tunnel = tunnel_scene.instantiate()
	tunnel.save_state = save_state
	root.add_child(tunnel)
	tunnel._ready()
	if save_state.current_scene != "rock_tunnel_interior":
		push_error("Rock Tunnel interior did not update current scene.")
		quit(1)
		return
	if not save_state.story_flags.get("rock_tunnel_interior_reached", false):
		push_error("Rock Tunnel interior reached flag missing.")
		quit(1)
		return
	if not save_state.worldlink_queue.has("wl_rock_tunnel_interior_reached"):
		push_error("WorldLink queue missing Rock Tunnel arrival.")
		quit(1)
		return

	tunnel.trigger_rock_tunnel_interior_scene()
	for flag_name in [
		"red_rock_tunnel_guidance_seen",
		"bill_lavender_echo_trace_seen",
		"team_moonlight_cave_pressure_seen",
		"rocket_dark_cache_seen",
		"flash_lantern_needed_seen",
		"lavender_exit_path_unlocked",
	]:
		if not save_state.story_flags.get(flag_name, false):
			push_error("Rock Tunnel interior flag missing: " + flag_name)
			quit(1)
			return
	for queue_id in [
		"wl_red_rock_tunnel_guidance",
		"wl_bill_lavender_echo_trace",
		"wl_team_moonlight_cave_pressure",
		"wl_rocket_dark_cache",
		"wl_flash_lantern_needed",
		"wl_lavender_exit_path_unlocked",
	]:
		if not save_state.worldlink_queue.has(queue_id):
			push_error("WorldLink missing Rock Tunnel id: " + queue_id)
			quit(1)
			return
	for required_text in ["Red", "Bill", "Moonlight", "Rocket", "Lavender", "Echo Flute", "Flash Lantern", "Rock Tunnel"]:
		if tunnel.dialogue_label == null or not tunnel.dialogue_label.text.contains(required_text):
			push_error("Rock Tunnel dialogue missing: " + required_text)
			quit(1)
			return

	var returned := [false]
	tunnel.go_to_route_9_rock_tunnel_approach.connect(func() -> void:
		returned[0] = true
	)
	tunnel.return_to_route_9_rock_tunnel_approach()
	if not returned[0]:
		push_error("Rock Tunnel scene did not emit return to Route 9.")
		quit(1)
		return

	tunnel.free()
	route9.free()
	print("Native Rock Tunnel interior smoke test passed.")
	quit(0)
