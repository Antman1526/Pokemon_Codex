extends SceneTree


func _init() -> void:
	print("misty_gym_placeholder_test")
	var save_state_script := load("res://src/save/SaveState.gd")
	var cerulean_scene := load("res://scenes/world/CeruleanCity.tscn")
	var battle_scene := load("res://scenes/battle/BattlePlaceholder.tscn")

	if save_state_script == null or cerulean_scene == null or battle_scene == null:
		push_error("Misty gym placeholder resources did not load.")
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

	var battle_seen := [false]
	cerulean.start_battle_placeholder.connect(func(battle_id: String) -> void:
		battle_seen[0] = true
		if battle_id != "misty_cerulean_gym":
			push_error("Cerulean emitted the wrong battle id.")
			quit(1)
	)

	cerulean.trigger_misty_gym_battle()
	if battle_seen[0]:
		push_error("Misty gym should stay locked before Nugget Bridge is cleared.")
		quit(1)
		return
	if cerulean.dialogue_label == null or not cerulean.dialogue_label.text.contains("Nugget Bridge"):
		push_error("Locked Misty gym did not point back to Nugget Bridge.")
		quit(1)
		return

	save_state.set_flag("misty_gym_unlocked", true)
	cerulean.trigger_misty_gym_battle()
	if not battle_seen[0]:
		push_error("Cerulean did not emit Misty gym battle.")
		quit(1)
		return
	if not save_state.story_flags.get("misty_cerulean_gym_started", false):
		push_error("Misty gym started flag missing after trigger.")
		quit(1)
		return

	save_state.start_battle_placeholder("misty_cerulean_gym")
	var battle = battle_scene.instantiate()
	battle.save_state = save_state
	battle.battle_id = "misty_cerulean_gym"
	root.add_child(battle)
	battle._ready()
	if battle.battle_data.get("opponent", {}).get("display_name", "") != "Misty":
		push_error("Misty battle data did not load.")
		quit(1)
		return
	if battle.dialogue_label == null or not battle.dialogue_label.text.contains("Misty"):
		push_error("Misty battle did not render Misty dialogue.")
		quit(1)
		return

	battle.finish_placeholder_battle()
	save_state.finish_battle_placeholder("placeholder_win")
	if not save_state.story_flags.get("misty_cerulean_gym_finished", false):
		push_error("Misty gym finished flag missing.")
		quit(1)
		return
	if not save_state.story_flags.get("cascade_badge_earned", false):
		push_error("Cascade Badge flag missing.")
		quit(1)
		return
	if not save_state.worldlink_queue.has("wl_misty_cascade_badge_earned"):
		push_error("WorldLink missing Misty Cascade Badge update.")
		quit(1)
		return

	battle.free()
	cerulean.free()
	print("Native Misty gym placeholder smoke test passed.")
	quit(0)
