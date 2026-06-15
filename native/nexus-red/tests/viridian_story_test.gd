extends SceneTree


func _init() -> void:
	print("viridian_story_test")
	var save_state_script := load("res://src/save/SaveState.gd")
	var viridian_scene := load("res://scenes/world/ViridianCity.tscn")
	var worldlink_panel_script := load("res://src/worldlink/WorldLinkPanel.gd")

	if save_state_script == null or viridian_scene == null or worldlink_panel_script == null:
		push_error("Viridian story resources did not load.")
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

	var city = viridian_scene.instantiate()
	city.save_state = save_state
	root.add_child(city)
	city._ready()

	city.interact_red_companion()
	if not save_state.story_flags.get("viridian_red_scene_seen", false):
		push_error("Viridian Red scene flag missing.")
		quit(1)
		return
	if not save_state.story_flags.get("worldlink_viridian_story_batch_queued", false):
		push_error("Viridian WorldLink batch was not queued.")
		quit(1)
		return
	if not save_state.worldlink_queue.has("wl_red_viridian_checkin"):
		push_error("WorldLink queue missing Red Viridian checkin.")
		quit(1)
		return
	if not city.dialogue_label.text.contains("Red:"):
		push_error("Red companion dialogue did not display.")
		quit(1)
		return

	city.investigate_rocket_clue()
	if not save_state.story_flags.get("viridian_rocket_clue_found", false):
		push_error("Viridian Rocket clue flag missing.")
		quit(1)
		return
	if not save_state.worldlink_queue.has("wl_rocket_viridian_clue"):
		push_error("WorldLink queue missing Rocket Viridian clue.")
		quit(1)
		return
	if not city.dialogue_label.text.contains("Rocket"):
		push_error("Rocket clue dialogue did not display.")
		quit(1)
		return

	var panel = worldlink_panel_script.new()
	panel.save_state = save_state
	root.add_child(panel)
	panel._ready()
	var feed_text: String = panel._build_feed_text()
	if not feed_text.contains("Viridian") or not feed_text.contains("Rocket"):
		push_error("WorldLink feed did not render Viridian Rocket update.")
		quit(1)
		return

	panel.free()
	city.free()
	print("Native Viridian story smoke test passed.")
	quit(0)
