extends SceneTree


func _init() -> void:
	print("route5_underground_path_test")
	var save_state_script := load("res://src/save/SaveState.gd")
	var cerulean_scene := load("res://scenes/world/CeruleanCity.tscn")
	var route5_scene := load("res://scenes/world/Route5UndergroundPath.tscn")

	if save_state_script == null or cerulean_scene == null or route5_scene == null:
		push_error("Route 5 Underground Path resources did not load.")
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
	save_state.enter_cerulean_city()

	var cerulean = cerulean_scene.instantiate()
	cerulean.save_state = save_state
	root.add_child(cerulean)
	cerulean._ready()

	var route5_seen := [false]
	cerulean.go_to_route_5_underground_path.connect(func() -> void:
		route5_seen[0] = true
	)

	cerulean.trigger_route_5_underground_path_entry()
	if route5_seen[0]:
		push_error("Route 5 should stay locked before stolen TM recovery.")
		quit(1)
		return
	if cerulean.dialogue_label == null or not cerulean.dialogue_label.text.contains("stolen TM"):
		push_error("Locked Route 5 entry did not point back to the stolen TM.")
		quit(1)
		return

	save_state.set_flag("stolen_tm_recovered", true)
	save_state.set_flag("route_5_vermilion_path_unlocked", true)
	cerulean.trigger_route_5_underground_path_entry()
	if not route5_seen[0]:
		push_error("Cerulean did not emit Route 5 transition after stolen TM recovery.")
		quit(1)
		return

	var route5 = route5_scene.instantiate()
	route5.save_state = save_state
	root.add_child(route5)
	route5._ready()
	if save_state.current_scene != "route_5_underground_path":
		push_error("Route 5 did not update current scene.")
		quit(1)
		return
	if not save_state.story_flags.get("route_5_underground_path_reached", false):
		push_error("Route 5 reached flag missing.")
		quit(1)
		return
	if not save_state.worldlink_queue.has("wl_route_5_underground_path_reached"):
		push_error("WorldLink queue missing Route 5 arrival.")
		quit(1)
		return

	route5.trigger_underground_path_scouting()
	if not save_state.story_flags.get("underground_path_scouted", false):
		push_error("Underground Path scouted flag missing.")
		quit(1)
		return
	if not save_state.story_flags.get("vermilion_shipping_lead_seen", false):
		push_error("Vermilion shipping lead flag missing.")
		quit(1)
		return
	if not save_state.story_flags.get("vermilion_city_teased", false):
		push_error("Vermilion City teased flag missing.")
		quit(1)
		return
	for queue_id in ["wl_underground_path_scouted", "wl_vermilion_shipping_lead", "wl_vermilion_city_teased"]:
		if not save_state.worldlink_queue.has(queue_id):
			push_error("WorldLink queue missing Route 5 id: " + queue_id)
			quit(1)
			return
	for required_text in ["Red", "Misty", "Bill", "Underground Path", "Vermilion"]:
		if route5.dialogue_label == null or not route5.dialogue_label.text.contains(required_text):
			push_error("Route 5 scouting dialogue missing: " + required_text)
			quit(1)
			return

	var returned := [false]
	route5.go_to_cerulean_city.connect(func() -> void:
		returned[0] = true
	)
	route5.return_to_cerulean_city()
	if not returned[0]:
		push_error("Route 5 did not emit return to Cerulean City.")
		quit(1)
		return

	route5.free()
	cerulean.free()
	print("Native Route 5 Underground Path smoke test passed.")
	quit(0)
