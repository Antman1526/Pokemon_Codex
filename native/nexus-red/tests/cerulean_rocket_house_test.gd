extends SceneTree


func _init() -> void:
	print("cerulean_rocket_house_test")
	var save_state_script := load("res://src/save/SaveState.gd")
	var cerulean_scene := load("res://scenes/world/CeruleanCity.tscn")
	var house_scene := load("res://scenes/world/CeruleanRocketHouse.tscn")
	var battle_scene := load("res://scenes/battle/BattlePlaceholder.tscn")

	if save_state_script == null or cerulean_scene == null or house_scene == null or battle_scene == null:
		push_error("Cerulean Rocket house resources did not load.")
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

	var house_seen := [false]
	cerulean.go_to_cerulean_rocket_house.connect(func() -> void:
		house_seen[0] = true
	)

	cerulean.trigger_cerulean_rocket_house_entry()
	if house_seen[0]:
		push_error("Rocket house should stay locked before Bill's intro.")
		quit(1)
		return
	if cerulean.dialogue_label == null or not cerulean.dialogue_label.text.contains("Bill"):
		push_error("Locked Rocket house entry did not point back to Bill.")
		quit(1)
		return

	save_state.set_flag("bill_route25_intro_seen", true)
	cerulean.trigger_cerulean_rocket_house_entry()
	if not house_seen[0]:
		push_error("Cerulean did not emit Rocket house transition after Bill's intro.")
		quit(1)
		return

	var house = house_scene.instantiate()
	house.save_state = save_state
	root.add_child(house)
	house._ready()
	if save_state.current_scene != "cerulean_rocket_house":
		push_error("Rocket house did not update current scene.")
		quit(1)
		return
	if not save_state.story_flags.get("cerulean_rocket_house_reached", false):
		push_error("Rocket house reached flag missing.")
		quit(1)
		return

	house.trigger_house_investigation()
	if not save_state.story_flags.get("cerulean_house_theft_seen", false):
		push_error("Cerulean house theft flag missing.")
		quit(1)
		return
	if not save_state.story_flags.get("rocket_stolen_tm_clue_seen", false):
		push_error("Rocket stolen TM clue flag missing.")
		quit(1)
		return

	var battle_seen := [false]
	house.start_battle_placeholder.connect(func(battle_id: String) -> void:
		battle_seen[0] = true
		if battle_id != "cerulean_rocket_house_thief":
			push_error("Rocket house emitted wrong battle id.")
			quit(1)
	)
	house.trigger_rocket_thief_battle()
	if not battle_seen[0]:
		push_error("Rocket house did not emit Rocket thief battle.")
		quit(1)
		return
	if not save_state.story_flags.get("cerulean_rocket_house_thief_battle_started", false):
		push_error("Rocket house thief battle started flag missing.")
		quit(1)
		return

	save_state.start_battle_placeholder("cerulean_rocket_house_thief")
	var battle = battle_scene.instantiate()
	battle.save_state = save_state
	battle.battle_id = "cerulean_rocket_house_thief"
	root.add_child(battle)
	battle._ready()
	if battle.battle_data.get("opponent", {}).get("display_name", "") != "Rocket TM Thief":
		push_error("Rocket house battle data did not load.")
		quit(1)
		return

	battle.finish_placeholder_battle()
	save_state.finish_battle_placeholder("placeholder_win")
	if not save_state.story_flags.get("cerulean_rocket_house_thief_battle_finished", false):
		push_error("Rocket house thief battle finished flag missing.")
		quit(1)
		return
	if not save_state.story_flags.get("stolen_tm_recovered", false):
		push_error("Stolen TM recovered flag missing.")
		quit(1)
		return
	if not save_state.story_flags.get("route_5_vermilion_path_unlocked", false):
		push_error("Route 5 Vermilion path unlock flag missing.")
		quit(1)
		return
	for queue_id in ["wl_cerulean_house_theft_seen", "wl_stolen_tm_recovered", "wl_route_5_vermilion_path_unlocked"]:
		if not save_state.worldlink_queue.has(queue_id):
			push_error("WorldLink queue missing Cerulean Rocket house id: " + queue_id)
			quit(1)
			return

	battle.free()
	house.free()
	cerulean.free()
	print("Native Cerulean Rocket house smoke test passed.")
	quit(0)
