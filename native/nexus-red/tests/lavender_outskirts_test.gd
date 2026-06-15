extends SceneTree


func _init() -> void:
	print("lavender_outskirts_test")
	var save_state_script := load("res://src/save/SaveState.gd")
	var tunnel_scene := load("res://scenes/world/RockTunnelInterior.tscn")
	var lavender_scene := load("res://scenes/world/LavenderOutskirts.tscn")

	if save_state_script == null or tunnel_scene == null or lavender_scene == null:
		push_error("Lavender outskirts resources did not load.")
		quit(1)
		return

	var save_state = save_state_script.new()
	save_state.start_new_game("Antman")
	save_state.enter_rock_tunnel_interior()

	var tunnel = tunnel_scene.instantiate()
	tunnel.save_state = save_state
	root.add_child(tunnel)
	tunnel._ready()

	var lavender_seen := [false]
	tunnel.go_to_lavender_outskirts.connect(func() -> void:
		lavender_seen[0] = true
	)

	tunnel.trigger_lavender_exit()
	if lavender_seen[0]:
		push_error("Lavender exit should stay locked before Rock Tunnel interior scene is complete.")
		quit(1)
		return
	if tunnel.dialogue_label == null or not tunnel.dialogue_label.text.contains("Lavender"):
		push_error("Locked Lavender exit did not point back to the Rock Tunnel signal.")
		quit(1)
		return

	tunnel.trigger_rock_tunnel_interior_scene()
	tunnel.trigger_lavender_exit()
	if not lavender_seen[0]:
		push_error("Rock Tunnel did not emit Lavender outskirts after exit unlock.")
		quit(1)
		return

	var lavender = lavender_scene.instantiate()
	lavender.save_state = save_state
	root.add_child(lavender)
	lavender._ready()
	if save_state.current_scene != "lavender_outskirts":
		push_error("Lavender outskirts did not update current scene.")
		quit(1)
		return
	if not save_state.story_flags.get("lavender_outskirts_reached", false):
		push_error("Lavender outskirts reached flag missing.")
		quit(1)
		return
	if not save_state.worldlink_queue.has("wl_lavender_outskirts_reached"):
		push_error("WorldLink queue missing Lavender outskirts arrival.")
		quit(1)
		return

	lavender.trigger_lavender_outskirts_scene()
	for flag_name in [
		"red_lavender_arrival_seen",
		"bill_pokemon_tower_signal_decode_seen",
		"team_moonlight_lavender_presence_seen",
		"rocket_lavender_surveillance_seen",
		"pokemon_tower_signal_confirmed",
		"pokemon_tower_entry_unlocked",
	]:
		if not save_state.story_flags.get(flag_name, false):
			push_error("Lavender outskirts flag missing: " + flag_name)
			quit(1)
			return
	for queue_id in [
		"wl_red_lavender_arrival",
		"wl_bill_pokemon_tower_signal_decode",
		"wl_team_moonlight_lavender_presence",
		"wl_rocket_lavender_surveillance",
		"wl_pokemon_tower_signal_confirmed",
		"wl_pokemon_tower_entry_unlocked",
	]:
		if not save_state.worldlink_queue.has(queue_id):
			push_error("WorldLink missing Lavender id: " + queue_id)
			quit(1)
			return
	for required_text in ["Red", "Bill", "Moonlight", "Rocket", "Lavender", "Pokemon Tower", "Echo Flute"]:
		if lavender.dialogue_label == null or not lavender.dialogue_label.text.contains(required_text):
			push_error("Lavender outskirts dialogue missing: " + required_text)
			quit(1)
			return

	var returned := [false]
	lavender.go_to_rock_tunnel_interior.connect(func() -> void:
		returned[0] = true
	)
	lavender.return_to_rock_tunnel_interior()
	if not returned[0]:
		push_error("Lavender scene did not emit return to Rock Tunnel.")
		quit(1)
		return

	lavender.free()
	tunnel.free()
	print("Native Lavender outskirts smoke test passed.")
	quit(0)
