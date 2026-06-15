extends SceneTree


func _init() -> void:
	print("pewter_museum_anomaly_test")
	var save_state_script := load("res://src/save/SaveState.gd")
	var pewter_scene := load("res://scenes/world/PewterCity.tscn")

	if save_state_script == null or pewter_scene == null:
		push_error("Pewter Museum anomaly resources did not load.")
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
	save_state.enter_pewter_city()

	var pewter = pewter_scene.instantiate()
	pewter.save_state = save_state
	root.add_child(pewter)
	pewter._ready()

	pewter.investigate_museum_anomaly()
	if save_state.story_flags.get("pewter_museum_anomaly_seen", false):
		push_error("Museum anomaly should stay locked before Brock's badge.")
		quit(1)
		return
	if pewter.dialogue_label == null or not pewter.dialogue_label.text.contains("Brock"):
		push_error("Locked museum anomaly should point Antman back to Brock.")
		quit(1)
		return

	save_state.start_battle_placeholder("brock_pewter_gym")
	save_state.finish_battle_placeholder("placeholder_win")
	pewter.investigate_museum_anomaly()
	if not save_state.story_flags.get("pewter_museum_anomaly_seen", false):
		push_error("Museum anomaly flag missing after Brock badge.")
		quit(1)
		return
	if not save_state.story_flags.get("worldlink_pewter_museum_batch_queued", false):
		push_error("Pewter Museum WorldLink batch flag missing.")
		quit(1)
		return
	if not save_state.worldlink_queue.has("wl_red_pewter_museum_scan"):
		push_error("WorldLink queue missing Red museum scan.")
		quit(1)
		return
	if not save_state.worldlink_queue.has("wl_rocket_pewter_museum_anomaly"):
		push_error("WorldLink queue missing Rocket museum anomaly.")
		quit(1)
		return
	if not save_state.worldlink_queue.has("wl_bill_fossil_energy_ping"):
		push_error("WorldLink queue missing Bill fossil energy ping.")
		quit(1)
		return
	if not pewter.dialogue_label.text.contains("Pewter Museum") or not pewter.dialogue_label.text.contains("Rocket"):
		push_error("Museum anomaly dialogue did not mention Pewter Museum and Rocket.")
		quit(1)
		return

	pewter.free()
	print("Native Pewter Museum anomaly smoke test passed.")
	quit(0)
