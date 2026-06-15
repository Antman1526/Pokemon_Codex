extends SceneTree


func _init() -> void:
	print("vermilion_city_arrival_test")
	var save_state_script := load("res://src/save/SaveState.gd")
	var route5_scene := load("res://scenes/world/Route5UndergroundPath.tscn")
	var vermilion_scene := load("res://scenes/world/VermilionCity.tscn")

	if save_state_script == null or route5_scene == null or vermilion_scene == null:
		push_error("Vermilion City arrival resources did not load.")
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
	save_state.enter_route_5_underground_path()

	var route5 = route5_scene.instantiate()
	route5.save_state = save_state
	root.add_child(route5)
	route5._ready()

	var vermilion_seen := [false]
	route5.go_to_vermilion_city.connect(func() -> void:
		vermilion_seen[0] = true
	)

	route5.trigger_vermilion_city_entry()
	if vermilion_seen[0]:
		push_error("Vermilion should stay locked before Underground Path scouting.")
		quit(1)
		return
	if route5.dialogue_label == null or not route5.dialogue_label.text.contains("Underground Path"):
		push_error("Locked Vermilion entry did not point back to Underground Path scouting.")
		quit(1)
		return

	save_state.set_flag("underground_path_scouted", true)
	save_state.set_flag("vermilion_shipping_lead_seen", true)
	route5.trigger_vermilion_city_entry()
	if not vermilion_seen[0]:
		push_error("Route 5 did not emit Vermilion transition after scouting.")
		quit(1)
		return

	var vermilion = vermilion_scene.instantiate()
	vermilion.save_state = save_state
	root.add_child(vermilion)
	vermilion._ready()
	if save_state.current_scene != "vermilion_city":
		push_error("Vermilion City did not update current scene.")
		quit(1)
		return
	if not save_state.story_flags.get("vermilion_city_reached", false):
		push_error("Vermilion City reached flag missing.")
		quit(1)
		return
	if not save_state.worldlink_queue.has("wl_vermilion_city_reached"):
		push_error("WorldLink queue missing Vermilion arrival.")
		quit(1)
		return

	vermilion.trigger_vermilion_arrival_scene()
	if not save_state.story_flags.get("vermilion_harbor_scouted", false):
		push_error("Vermilion harbor scouted flag missing.")
		quit(1)
		return
	if not save_state.story_flags.get("ss_anne_ticket_lead_seen", false):
		push_error("S.S. Anne ticket lead flag missing.")
		quit(1)
		return
	if not save_state.story_flags.get("surge_power_sabotage_teased", false):
		push_error("Surge power sabotage tease flag missing.")
		quit(1)
		return
	for queue_id in ["wl_vermilion_harbor_scouted", "wl_ss_anne_ticket_lead", "wl_surge_power_sabotage_teased"]:
		if not save_state.worldlink_queue.has(queue_id):
			push_error("WorldLink queue missing Vermilion id: " + queue_id)
			quit(1)
			return
	for required_text in ["Red", "Misty", "Bill", "S.S. Anne", "Surge", "Rocket"]:
		if vermilion.dialogue_label == null or not vermilion.dialogue_label.text.contains(required_text):
			push_error("Vermilion arrival dialogue missing: " + required_text)
			quit(1)
			return

	var returned := [false]
	vermilion.go_to_route_5_underground_path.connect(func() -> void:
		returned[0] = true
	)
	vermilion.return_to_route_5_underground_path()
	if not returned[0]:
		push_error("Vermilion did not emit return to Route 5.")
		quit(1)
		return

	vermilion.free()
	route5.free()
	print("Native Vermilion City arrival smoke test passed.")
	quit(0)
