extends SceneTree


func _init() -> void:
	print("route25_bill_intro_test")
	var save_state_script := load("res://src/save/SaveState.gd")
	var cerulean_scene := load("res://scenes/world/CeruleanCity.tscn")
	var route25_scene := load("res://scenes/world/Route25Bill.tscn")

	if save_state_script == null or cerulean_scene == null or route25_scene == null:
		push_error("Route 25 Bill intro resources did not load.")
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

	var route25_seen := [false]
	cerulean.go_to_route_25_bill.connect(func() -> void:
		route25_seen[0] = true
	)

	cerulean.trigger_route_25_bill_entry()
	if route25_seen[0]:
		push_error("Route 25 should stay locked before Cascade Badge.")
		quit(1)
		return
	if cerulean.dialogue_label == null or not cerulean.dialogue_label.text.contains("Cascade Badge"):
		push_error("Locked Route 25 entry did not point back to Cascade Badge.")
		quit(1)
		return

	save_state.set_flag("cascade_badge_earned", true)
	save_state.set_flag("misty_recurring_friend_unlocked", true)
	cerulean.trigger_route_25_bill_entry()
	if not route25_seen[0]:
		push_error("Cerulean did not emit Route 25 transition after Cascade Badge.")
		quit(1)
		return

	var route25 = route25_scene.instantiate()
	route25.save_state = save_state
	root.add_child(route25)
	route25._ready()
	if save_state.current_scene != "route_25_bill":
		push_error("Route 25 Bill scene did not update current scene.")
		quit(1)
		return
	if not save_state.story_flags.get("route_25_bill_reached", false):
		push_error("Route 25 Bill reached flag missing.")
		quit(1)
		return
	if not save_state.worldlink_queue.has("wl_route_25_bill_reached"):
		push_error("WorldLink queue missing Route 25 Bill arrival.")
		quit(1)
		return

	route25.trigger_bill_intro()
	if not save_state.story_flags.get("bill_route25_intro_seen", false):
		push_error("Bill Route 25 intro flag missing.")
		quit(1)
		return
	if not save_state.story_flags.get("bill_storage_network_clue_seen", false):
		push_error("Bill storage network clue flag missing.")
		quit(1)
		return
	if not save_state.story_flags.get("nexus_network_first_decode_seen", false):
		push_error("First Nexus network decode flag missing.")
		quit(1)
		return
	for queue_id in ["wl_bill_route25_intro", "wl_bill_storage_network_clue", "wl_nexus_network_first_decode"]:
		if not save_state.worldlink_queue.has(queue_id):
			push_error("WorldLink queue missing Route 25 Bill id: " + queue_id)
			quit(1)
			return
	for required_text in ["Bill", "Misty", "Red", "Nexus", "WorldLink"]:
		if route25.dialogue_label == null or not route25.dialogue_label.text.contains(required_text):
			push_error("Bill intro dialogue missing: " + required_text)
			quit(1)
			return

	var returned := [false]
	route25.go_to_cerulean_city.connect(func() -> void:
		returned[0] = true
	)
	route25.return_to_cerulean_city()
	if not returned[0]:
		push_error("Route 25 Bill scene did not emit return to Cerulean City.")
		quit(1)
		return

	route25.free()
	cerulean.free()
	print("Native Route 25 Bill intro smoke test passed.")
	quit(0)
