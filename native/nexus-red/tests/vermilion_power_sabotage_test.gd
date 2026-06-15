extends SceneTree


func _init() -> void:
	print("vermilion_power_sabotage_test")
	var save_state_script := load("res://src/save/SaveState.gd")
	var vermilion_scene := load("res://scenes/world/VermilionCity.tscn")
	var sabotage_scene := load("res://scenes/world/VermilionPowerSabotage.tscn")

	if save_state_script == null or vermilion_scene == null or sabotage_scene == null:
		push_error("Vermilion power sabotage resources did not load.")
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
	save_state.enter_vermilion_city()

	var vermilion = vermilion_scene.instantiate()
	vermilion.save_state = save_state
	root.add_child(vermilion)
	vermilion._ready()

	var sabotage_seen := [false]
	vermilion.go_to_vermilion_power_sabotage.connect(func() -> void:
		sabotage_seen[0] = true
	)

	vermilion.trigger_surge_power_sabotage_entry()
	if sabotage_seen[0]:
		push_error("Surge power sabotage should stay locked before Trail Cutter.")
		quit(1)
		return
	if vermilion.dialogue_label == null or not vermilion.dialogue_label.text.contains("Trail Cutter"):
		push_error("Locked Surge route did not point back to Trail Cutter.")
		quit(1)
		return

	save_state.record_ss_anne_captain_cabin_scene()
	vermilion.trigger_surge_power_sabotage_entry()
	if not sabotage_seen[0]:
		push_error("Vermilion did not emit power sabotage transition after Trail Cutter.")
		quit(1)
		return

	var sabotage = sabotage_scene.instantiate()
	sabotage.save_state = save_state
	root.add_child(sabotage)
	sabotage._ready()
	if save_state.current_scene != "vermilion_power_sabotage":
		push_error("Power sabotage scene did not update current scene.")
		quit(1)
		return
	if not save_state.story_flags.get("vermilion_power_sabotage_reached", false):
		push_error("Power sabotage reached flag missing.")
		quit(1)
		return
	if not save_state.worldlink_queue.has("wl_vermilion_power_sabotage_reached"):
		push_error("WorldLink queue missing power sabotage arrival.")
		quit(1)
		return

	sabotage.trigger_power_sabotage_scene()
	for flag_name in [
		"rocket_gas_power_sabotage_seen",
		"team_gas_kanto_debut_seen",
		"red_misty_surge_prep_seen",
		"bill_power_grid_decode_seen",
		"surge_gym_battle_unlocked",
	]:
		if not save_state.story_flags.get(flag_name, false):
			push_error("Power sabotage flag missing: " + flag_name)
			quit(1)
			return
	for queue_id in [
		"wl_rocket_gas_power_sabotage",
		"wl_team_gas_kanto_debut",
		"wl_red_misty_surge_prep",
		"wl_bill_power_grid_decode",
		"wl_surge_gym_battle_unlocked",
	]:
		if not save_state.worldlink_queue.has(queue_id):
			push_error("WorldLink missing power sabotage id: " + queue_id)
			quit(1)
			return
	for required_text in ["Red", "Misty", "Bill", "Rocket", "Team Gas", "Surge"]:
		if sabotage.dialogue_label == null or not sabotage.dialogue_label.text.contains(required_text):
			push_error("Power sabotage dialogue missing: " + required_text)
			quit(1)
			return

	var returned := [false]
	sabotage.go_to_vermilion_city.connect(func() -> void:
		returned[0] = true
	)
	sabotage.return_to_vermilion_city()
	if not returned[0]:
		push_error("Power sabotage scene did not emit return to Vermilion.")
		quit(1)
		return

	sabotage.free()
	vermilion.free()
	print("Native Vermilion power sabotage smoke test passed.")
	quit(0)
