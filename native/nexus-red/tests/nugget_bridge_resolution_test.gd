extends SceneTree


func _init() -> void:
	print("nugget_bridge_resolution_test")
	var save_state_script := load("res://src/save/SaveState.gd")
	var bridge_scene := load("res://scenes/world/NuggetBridge.tscn")
	var battle_scene := load("res://scenes/battle/BattlePlaceholder.tscn")

	if save_state_script == null or bridge_scene == null or battle_scene == null:
		push_error("Nugget Bridge resolution resources did not load.")
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
	save_state.enter_nugget_bridge()

	var bridge = bridge_scene.instantiate()
	bridge.save_state = save_state
	root.add_child(bridge)
	bridge._ready()

	var captain_battle_seen := [false]
	bridge.start_battle_placeholder.connect(func(battle_id: String) -> void:
		captain_battle_seen[0] = true
		if battle_id != "nugget_bridge_captain":
			push_error("Nugget Bridge emitted the wrong captain battle id.")
			quit(1)
	)
	bridge.trigger_bridge_captain_battle()
	if captain_battle_seen[0]:
		push_error("Nugget Bridge captain should stay locked before the first recruiter is defeated.")
		quit(1)
		return
	if bridge.dialogue_label == null or not bridge.dialogue_label.text.contains("first recruiter"):
		push_error("Locked captain battle should point back to the first recruiter.")
		quit(1)
		return

	save_state.start_battle_placeholder("nugget_bridge_recruiter_1")
	save_state.finish_battle_placeholder("placeholder_win")
	bridge.trigger_bridge_captain_battle()
	if not captain_battle_seen[0]:
		push_error("Nugget Bridge did not emit captain battle after first recruiter.")
		quit(1)
		return
	if not save_state.story_flags.get("nugget_bridge_captain_battle_started", false):
		push_error("Nugget Bridge captain battle started flag missing.")
		quit(1)
		return

	save_state.start_battle_placeholder("nugget_bridge_captain")
	var battle = battle_scene.instantiate()
	battle.save_state = save_state
	battle.battle_id = "nugget_bridge_captain"
	root.add_child(battle)
	battle._ready()
	if battle.battle_data.get("opponent", {}).get("display_name", "") != "Bridge Captain":
		push_error("Nugget Bridge captain battle data did not load.")
		quit(1)
		return
	if battle.dialogue_label == null or not battle.dialogue_label.text.contains("Bridge Captain"):
		push_error("Nugget Bridge captain battle did not render captain dialogue.")
		quit(1)
		return

	battle.finish_placeholder_battle()
	save_state.finish_battle_placeholder("placeholder_win")
	if not save_state.story_flags.get("nugget_bridge_captain_battle_finished", false):
		push_error("Nugget Bridge captain battle finished flag missing.")
		quit(1)
		return
	if not save_state.story_flags.get("nugget_bridge_crisis_cleared", false):
		push_error("Nugget Bridge crisis cleared flag missing.")
		quit(1)
		return
	if not save_state.story_flags.get("misty_gym_unlocked", false):
		push_error("Misty gym unlocked flag missing after bridge crisis.")
		quit(1)
		return
	if save_state.worldlink_queue.has("wl_nugget_bridge_crisis_cleared") == false:
		push_error("WorldLink queue missing Nugget Bridge crisis cleared.")
		quit(1)
		return

	bridge.show_bridge_resolution()
	for required_text in ["Misty", "gym", "Rocket", "Gold Dust"]:
		if not bridge.dialogue_label.text.contains(required_text):
			push_error("Nugget Bridge resolution dialogue missing: " + required_text)
			quit(1)
			return

	battle.free()
	bridge.free()
	print("Native Nugget Bridge resolution smoke test passed.")
	quit(0)
