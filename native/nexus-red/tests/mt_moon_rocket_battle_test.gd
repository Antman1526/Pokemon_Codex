extends SceneTree


func _init() -> void:
	print("mt_moon_rocket_battle_test")
	var save_state_script := load("res://src/save/SaveState.gd")
	var interior_scene := load("res://scenes/world/MtMoonInterior1.tscn")
	var battle_scene := load("res://scenes/battle/BattlePlaceholder.tscn")

	if save_state_script == null or interior_scene == null or battle_scene == null:
		push_error("Mt. Moon Rocket battle resources did not load.")
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
	save_state.enter_mt_moon_interior_1()

	var interior = interior_scene.instantiate()
	interior.save_state = save_state
	root.add_child(interior)
	interior._ready()

	var battle_seen := [false]
	interior.start_battle_placeholder.connect(func(battle_id: String) -> void:
		battle_seen[0] = true
		if battle_id != "mt_moon_rocket_left_path":
			push_error("Mt. Moon interior emitted the wrong battle id.")
			quit(1)
	)
	interior.trigger_rocket_left_path_battle()
	if battle_seen[0]:
		push_error("Rocket left-path battle should stay locked before fossil split scouting.")
		quit(1)
		return
	if interior.dialogue_label == null or not interior.dialogue_label.text.contains("split"):
		push_error("Locked Rocket battle should point back to split-path scouting.")
		quit(1)
		return

	save_state.record_mt_moon_split_path_scouting()
	interior.trigger_rocket_left_path_battle()
	if not battle_seen[0]:
		push_error("Mt. Moon interior did not emit Rocket left-path battle.")
		quit(1)
		return
	if not save_state.story_flags.get("mt_moon_rocket_left_battle_started", false):
		push_error("Mt. Moon Rocket battle started flag missing.")
		quit(1)
		return
	if not save_state.story_flags.get("red_mt_moon_tag_setup_seen", false):
		push_error("Red tag setup flag missing.")
		quit(1)
		return

	save_state.start_battle_placeholder("mt_moon_rocket_left_path")
	var battle = battle_scene.instantiate()
	battle.save_state = save_state
	battle.battle_id = "mt_moon_rocket_left_path"
	root.add_child(battle)
	battle._ready()
	if battle.battle_data.get("opponent", {}).get("display_name", "") != "Rocket Grunt":
		push_error("Mt. Moon Rocket battle data did not load.")
		quit(1)
		return
	if battle.dialogue_label == null or not battle.dialogue_label.text.contains("Rocket Grunt"):
		push_error("Mt. Moon Rocket battle did not render Rocket dialogue.")
		quit(1)
		return

	battle.finish_placeholder_battle()
	save_state.finish_battle_placeholder("placeholder_win")
	if not save_state.story_flags.get("mt_moon_rocket_left_battle_finished", false):
		push_error("Mt. Moon Rocket battle finished flag missing.")
		quit(1)
		return
	if not save_state.worldlink_queue.has("mt_moon_rocket_left_battle_finished"):
		push_error("WorldLink queue missing Mt. Moon Rocket battle completion.")
		quit(1)
		return

	battle.free()
	interior.free()
	print("Native Mt. Moon Rocket battle smoke test passed.")
	quit(0)
