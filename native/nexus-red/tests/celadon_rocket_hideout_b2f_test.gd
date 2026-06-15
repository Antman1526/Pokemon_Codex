extends SceneTree


func _init() -> void:
	print("celadon_rocket_hideout_b2f_test")
	var save_state_script := load("res://src/save/SaveState.gd")
	var b1f_scene := load("res://scenes/world/CeladonRocketHideoutB1F.tscn")
	var b2f_scene := load("res://scenes/world/CeladonRocketHideoutB2F.tscn")
	var battle_scene := load("res://scenes/battle/BattlePlaceholder.tscn")

	if save_state_script == null or b1f_scene == null or b2f_scene == null or battle_scene == null:
		push_error("Celadon Rocket Hideout B2F resources did not load.")
		quit(1)
		return

	var save_state = save_state_script.new()
	save_state.start_new_game("Antman")
	save_state.enter_celadon_rocket_hideout_b1f()

	var b1f = b1f_scene.instantiate()
	b1f.save_state = save_state
	root.add_child(b1f)
	b1f._ready()

	var b2f_seen := [false]
	b1f.go_to_rocket_hideout_b2f.connect(func() -> void:
		b2f_seen[0] = true
	)

	b1f.trigger_rocket_hideout_b2f_entry()
	if b2f_seen[0]:
		push_error("Rocket Hideout B2F should stay locked before B1F scouting.")
		quit(1)
		return
	if b1f.dialogue_label == null or not b1f.dialogue_label.text.contains("Lift Key"):
		push_error("Locked B2F path did not explain the B1F scouting requirement.")
		quit(1)
		return

	b1f.trigger_rocket_hideout_b1f_scene()
	b1f.trigger_rocket_hideout_b2f_entry()
	if not b2f_seen[0]:
		push_error("Rocket Hideout B1F did not emit B2F after scouting.")
		quit(1)
		return

	var b2f = b2f_scene.instantiate()
	b2f.save_state = save_state
	root.add_child(b2f)
	b2f._ready()
	if save_state.current_scene != "celadon_rocket_hideout_b2f":
		push_error("Rocket Hideout B2F did not update current scene.")
		quit(1)
		return
	if not save_state.story_flags.get("celadon_rocket_hideout_b2f_reached", false):
		push_error("Rocket Hideout B2F reached flag missing.")
		quit(1)
		return
	if not save_state.worldlink_queue.has("wl_celadon_rocket_hideout_b2f_reached"):
		push_error("WorldLink queue missing Rocket Hideout B2F arrival.")
		quit(1)
		return

	b2f.trigger_rocket_hideout_b2f_scene()
	for flag_name in [
		"red_hideout_b2f_patrol_warning_seen",
		"bill_stolen_silph_scope_crate_seen",
		"rocket_hideout_b2f_patrol_battle_unlocked",
		"rocket_gold_dust_b2f_conflict_seen",
		"team_moonlight_control_room_interference_seen",
		"lift_key_b3f_route_seen",
	]:
		if not save_state.story_flags.get(flag_name, false):
			push_error("Rocket Hideout B2F flag missing: " + flag_name)
			quit(1)
			return
	for queue_id in [
		"wl_red_hideout_b2f_patrol_warning",
		"wl_bill_stolen_silph_scope_crate",
		"wl_rocket_hideout_b2f_patrol_unlocked",
		"wl_rocket_gold_dust_b2f_conflict",
		"wl_team_moonlight_control_room_interference",
		"wl_lift_key_b3f_route_seen",
	]:
		if not save_state.worldlink_queue.has(queue_id):
			push_error("WorldLink missing Rocket Hideout B2F id: " + queue_id)
			quit(1)
			return
	for required_text in ["Red", "Bill", "Rocket", "Gold Dust", "Moonlight", "Silph Scope", "Lift Key", "patrol", "B3F"]:
		if b2f.dialogue_label == null or not b2f.dialogue_label.text.contains(required_text):
			push_error("Rocket Hideout B2F dialogue missing: " + required_text)
			quit(1)
			return

	var b3f_seen := [false]
	b2f.go_to_rocket_hideout_b3f.connect(func() -> void:
		b3f_seen[0] = true
	)
	b2f.trigger_rocket_hideout_b3f_entry()
	if b3f_seen[0]:
		push_error("Rocket Hideout B3F should stay locked before the B2F patrol battle is finished.")
		quit(1)
		return

	var battle_seen := [false]
	b2f.start_battle_placeholder.connect(func(battle_id: String) -> void:
		battle_seen[0] = true
		if battle_id != "rocket_hideout_b2f_patrol":
			push_error("Rocket Hideout B2F emitted wrong battle id: " + battle_id)
			quit(1)
	)
	b2f.trigger_rocket_hideout_b2f_patrol_battle()
	if not battle_seen[0]:
		push_error("Rocket Hideout B2F did not emit patrol battle.")
		quit(1)
		return
	if save_state.active_battle_id != "rocket_hideout_b2f_patrol":
		push_error("Rocket Hideout B2F patrol was not active in save state.")
		quit(1)
		return
	if not save_state.story_flags.get("rocket_hideout_b2f_patrol_battle_started", false):
		push_error("Rocket Hideout B2F patrol started flag missing.")
		quit(1)
		return

	var battle = battle_scene.instantiate()
	battle.save_state = save_state
	battle.battle_id = "rocket_hideout_b2f_patrol"
	root.add_child(battle)
	battle._ready()
	battle.finish_placeholder_battle()
	save_state.finish_battle_placeholder("placeholder_win")
	if not save_state.story_flags.get("rocket_hideout_b2f_patrol_battle_finished", false):
		push_error("Rocket Hideout B2F patrol finished flag missing.")
		quit(1)
		return
	if not save_state.story_flags.get("rocket_hideout_b3f_path_unlocked", false):
		push_error("Rocket Hideout B3F path unlock flag missing.")
		quit(1)
		return
	for queue_id in [
		"wl_rocket_hideout_b2f_patrol_finished",
		"wl_rocket_hideout_b3f_path_unlocked",
	]:
		if not save_state.worldlink_queue.has(queue_id):
			push_error("WorldLink missing Rocket Hideout B2F post-battle id: " + queue_id)
			quit(1)
			return

	b2f.trigger_rocket_hideout_b3f_entry()
	if not b3f_seen[0]:
		push_error("Rocket Hideout B2F did not emit B3F after patrol battle.")
		quit(1)
		return

	var returned := [false]
	b2f.go_to_rocket_hideout_b1f.connect(func() -> void:
		returned[0] = true
	)
	b2f.return_to_rocket_hideout_b1f()
	if not returned[0]:
		push_error("Rocket Hideout B2F did not emit return to B1F.")
		quit(1)
		return

	battle.free()
	b2f.free()
	b1f.free()
	print("Native Celadon Rocket Hideout B2F smoke test passed.")
	quit(0)
