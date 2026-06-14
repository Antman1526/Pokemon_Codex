extends SceneTree


func _init() -> void:
	print("worldlink_route1_test")
	var save_state_script := load("res://src/save/SaveState.gd")
	var worldlink_panel_script := load("res://src/worldlink/WorldLinkPanel.gd")

	if save_state_script == null or worldlink_panel_script == null:
		push_error("WorldLink Route 1 resources did not load.")
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
	save_state.enter_route_1()
	save_state.record_red_route_1_scene()
	save_state.record_blue_battle_placeholder()
	save_state.start_battle_placeholder("blue_route_1")
	save_state.finish_battle_placeholder("placeholder_win")

	if not save_state.story_flags.get("route_1_rumors_unlocked", false):
		push_error("Route 1 rumors were not unlocked after Blue battle.")
		quit(1)
		return
	if not save_state.story_flags.get("worldlink_route_1_rival_batch_queued", false):
		push_error("Route 1 rival WorldLink batch was not queued.")
		quit(1)
		return

	var expected_queue_ids := [
		"wl_blue_route_1_battle_done",
		"wl_ava_route_1_capture",
		"wl_dax_route_1_training",
		"wl_red_route_1_checkin",
		"wl_silver_johto_tease",
		"rumor_route_1_unusual_tracks",
	]
	for queue_id in expected_queue_ids:
		if not save_state.worldlink_queue.has(queue_id):
			push_error("WorldLink queue missing expected id: " + queue_id)
			quit(1)
			return

	var panel = worldlink_panel_script.new()
	panel.save_state = save_state
	root.add_child(panel)
	panel._ready()
	if panel.get_child_count() == 0:
		push_error("WorldLink panel did not build content.")
		quit(1)
		return

	panel.free()
	print("Native Route 1 WorldLink smoke test passed.")
	quit(0)
