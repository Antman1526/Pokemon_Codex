extends SceneTree


func _init() -> void:
	print("nugget_bridge_recruiter_test")
	var save_state_script := load("res://src/save/SaveState.gd")
	var cerulean_scene := load("res://scenes/world/CeruleanCity.tscn")
	var bridge_scene := load("res://scenes/world/NuggetBridge.tscn")
	var battle_scene := load("res://scenes/battle/BattlePlaceholder.tscn")

	if save_state_script == null or cerulean_scene == null or bridge_scene == null or battle_scene == null:
		push_error("Nugget Bridge recruiter resources did not load.")
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

	var bridge_transition_seen := [false]
	cerulean.go_to_nugget_bridge.connect(func() -> void:
		bridge_transition_seen[0] = true
	)
	cerulean.trigger_nugget_bridge_entry()
	if bridge_transition_seen[0]:
		push_error("Nugget Bridge entry should stay locked before Misty's intro.")
		quit(1)
		return
	if cerulean.dialogue_label == null or not cerulean.dialogue_label.text.contains("Misty"):
		push_error("Locked Nugget Bridge entry should point back to Misty.")
		quit(1)
		return

	save_state.record_misty_cerulean_intro()
	cerulean.trigger_nugget_bridge_entry()
	if not bridge_transition_seen[0]:
		push_error("Cerulean did not emit Nugget Bridge transition after Misty's intro.")
		quit(1)
		return

	var bridge = bridge_scene.instantiate()
	bridge.save_state = save_state
	root.add_child(bridge)
	bridge._ready()
	if save_state.current_scene != "nugget_bridge":
		push_error("Nugget Bridge did not update current scene.")
		quit(1)
		return
	if not save_state.story_flags.get("nugget_bridge_reached", false):
		push_error("Nugget Bridge reached flag missing.")
		quit(1)
		return

	bridge.trigger_bridge_scouting()
	if not save_state.story_flags.get("red_misty_nugget_bridge_scout_seen", false):
		push_error("Red and Misty Nugget Bridge scouting flag missing.")
		quit(1)
		return
	if save_state.worldlink_queue.has("wl_nugget_bridge_scouting") == false:
		push_error("WorldLink queue missing Nugget Bridge scouting.")
		quit(1)
		return
	for required_text in ["Red", "Misty", "Rocket", "Gold Dust"]:
		if not bridge.dialogue_label.text.contains(required_text):
			push_error("Nugget Bridge scouting dialogue missing: " + required_text)
			quit(1)
			return

	var battle_seen := [false]
	bridge.start_battle_placeholder.connect(func(battle_id: String) -> void:
		battle_seen[0] = true
		if battle_id != "nugget_bridge_recruiter_1":
			push_error("Nugget Bridge emitted the wrong battle id.")
			quit(1)
	)
	bridge.trigger_recruiter_battle()
	if not battle_seen[0]:
		push_error("Nugget Bridge did not emit recruiter battle.")
		quit(1)
		return
	if not save_state.story_flags.get("nugget_bridge_recruiter_1_battle_started", false):
		push_error("Nugget Bridge recruiter battle started flag missing.")
		quit(1)
		return

	save_state.start_battle_placeholder("nugget_bridge_recruiter_1")
	var battle = battle_scene.instantiate()
	battle.save_state = save_state
	battle.battle_id = "nugget_bridge_recruiter_1"
	root.add_child(battle)
	battle._ready()
	if battle.battle_data.get("opponent", {}).get("display_name", "") != "Bridge Recruiter":
		push_error("Nugget Bridge recruiter battle data did not load.")
		quit(1)
		return
	if battle.dialogue_label == null or not battle.dialogue_label.text.contains("Bridge Recruiter"):
		push_error("Nugget Bridge recruiter battle did not render recruiter dialogue.")
		quit(1)
		return

	battle.finish_placeholder_battle()
	save_state.finish_battle_placeholder("placeholder_win")
	if not save_state.story_flags.get("nugget_bridge_recruiter_1_battle_finished", false):
		push_error("Nugget Bridge recruiter battle finished flag missing.")
		quit(1)
		return
	if save_state.worldlink_queue.has("nugget_bridge_recruiter_1_battle_finished") == false:
		push_error("WorldLink queue missing Nugget Bridge recruiter battle completion.")
		quit(1)
		return

	battle.free()
	bridge.free()
	cerulean.free()
	print("Native Nugget Bridge recruiter smoke test passed.")
	quit(0)
