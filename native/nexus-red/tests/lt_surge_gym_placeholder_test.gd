extends SceneTree


func _init() -> void:
	print("lt_surge_gym_placeholder_test")
	var save_state_script := load("res://src/save/SaveState.gd")
	var sabotage_scene := load("res://scenes/world/VermilionPowerSabotage.tscn")
	var battle_scene := load("res://scenes/battle/BattlePlaceholder.tscn")

	if save_state_script == null or sabotage_scene == null or battle_scene == null:
		push_error("Lt. Surge gym placeholder resources did not load.")
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
	save_state.enter_vermilion_power_sabotage()

	var sabotage = sabotage_scene.instantiate()
	sabotage.save_state = save_state
	root.add_child(sabotage)
	sabotage._ready()

	var battle_seen := [false]
	sabotage.start_battle_placeholder.connect(func(battle_id: String) -> void:
		battle_seen[0] = true
		if battle_id != "lt_surge_vermilion_gym":
			push_error("Power sabotage emitted the wrong battle id.")
			quit(1)
	)

	sabotage.trigger_surge_gym_battle()
	if battle_seen[0]:
		push_error("Lt. Surge gym should stay locked before the sabotage scene is resolved.")
		quit(1)
		return
	if sabotage.dialogue_label == null or not sabotage.dialogue_label.text.contains("power sabotage"):
		push_error("Locked Surge gym did not point back to power sabotage.")
		quit(1)
		return

	save_state.record_vermilion_power_sabotage_scene()
	sabotage.trigger_surge_gym_battle()
	if not battle_seen[0]:
		push_error("Power sabotage scene did not emit Lt. Surge gym battle.")
		quit(1)
		return
	if not save_state.story_flags.get("surge_vermilion_gym_started", false):
		push_error("Lt. Surge gym started flag missing after trigger.")
		quit(1)
		return

	save_state.start_battle_placeholder("lt_surge_vermilion_gym")
	var battle = battle_scene.instantiate()
	battle.save_state = save_state
	battle.battle_id = "lt_surge_vermilion_gym"
	root.add_child(battle)
	battle._ready()
	if battle.battle_data.get("opponent", {}).get("display_name", "") != "Lt. Surge":
		push_error("Lt. Surge battle data did not load.")
		quit(1)
		return
	if battle.dialogue_label == null or not battle.dialogue_label.text.contains("Lt. Surge"):
		push_error("Lt. Surge battle did not render Surge dialogue.")
		quit(1)
		return

	battle.finish_placeholder_battle()
	save_state.finish_battle_placeholder("placeholder_win")
	if not save_state.story_flags.get("surge_vermilion_gym_finished", false):
		push_error("Lt. Surge gym finished flag missing.")
		quit(1)
		return
	if not save_state.story_flags.get("thunder_badge_earned", false):
		push_error("Thunder Badge flag missing.")
		quit(1)
		return
	if not save_state.story_flags.get("route_11_path_unlocked", false):
		push_error("Route 11 path unlock flag missing.")
		quit(1)
		return
	if not save_state.worldlink_queue.has("wl_thunder_badge_earned"):
		push_error("WorldLink missing Thunder Badge update.")
		quit(1)
		return
	if not save_state.worldlink_queue.has("wl_route_11_path_unlocked"):
		push_error("WorldLink missing Route 11 unlock update.")
		quit(1)
		return

	battle.free()
	sabotage.free()
	print("Native Lt. Surge gym placeholder smoke test passed.")
	quit(0)
