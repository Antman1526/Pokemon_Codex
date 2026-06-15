extends SceneTree


func _init() -> void:
	print("brock_gym_placeholder_test")
	var save_state_script := load("res://src/save/SaveState.gd")
	var pewter_scene := load("res://scenes/world/PewterCity.tscn")
	var battle_scene := load("res://scenes/battle/BattlePlaceholder.tscn")

	if save_state_script == null or pewter_scene == null or battle_scene == null:
		push_error("Brock gym placeholder resources did not load.")
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

	var battle_seen := [false]
	pewter.start_battle_placeholder.connect(func(battle_id: String) -> void:
		battle_seen[0] = true
		if battle_id != "brock_pewter_gym":
			push_error("Pewter emitted the wrong battle id.")
			quit(1)
	)
	pewter.trigger_brock_gym_challenge()
	if not battle_seen[0]:
		push_error("Pewter did not emit Brock gym battle.")
		quit(1)
		return
	if not save_state.story_flags.get("brock_pewter_gym_started", false):
		push_error("Brock gym started flag missing after trigger.")
		quit(1)
		return

	save_state.start_battle_placeholder("brock_pewter_gym")
	var battle = battle_scene.instantiate()
	battle.save_state = save_state
	battle.battle_id = "brock_pewter_gym"
	root.add_child(battle)
	battle._ready()
	if battle.battle_data.get("opponent", {}).get("display_name", "") != "Brock":
		push_error("Brock battle data did not load.")
		quit(1)
		return
	if battle.dialogue_label == null or not battle.dialogue_label.text.contains("Brock"):
		push_error("Brock battle did not render Brock dialogue.")
		quit(1)
		return

	battle.finish_placeholder_battle()
	save_state.finish_battle_placeholder("placeholder_win")
	if not save_state.story_flags.get("brock_pewter_gym_finished", false):
		push_error("Brock gym finished flag missing.")
		quit(1)
		return
	if not save_state.story_flags.get("brock_pewter_badge_earned", false):
		push_error("Brock badge flag missing.")
		quit(1)
		return

	battle.free()
	pewter.free()
	print("Native Brock gym placeholder smoke test passed.")
	quit(0)
