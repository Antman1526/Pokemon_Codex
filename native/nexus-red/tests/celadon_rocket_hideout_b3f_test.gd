extends SceneTree


func _init() -> void:
	print("celadon_rocket_hideout_b3f_test")
	var save_state_script := load("res://src/save/SaveState.gd")
	var b2f_scene := load("res://scenes/world/CeladonRocketHideoutB2F.tscn")
	var b3f_scene := load("res://scenes/world/CeladonRocketHideoutB3F.tscn")
	var battle_scene := load("res://scenes/battle/BattlePlaceholder.tscn")

	if save_state_script == null or b2f_scene == null or b3f_scene == null or battle_scene == null:
		push_error("Celadon Rocket Hideout B3F resources did not load.")
		quit(1)
		return

	var save_state = save_state_script.new()
	save_state.start_new_game("Antman")
	save_state.enter_celadon_rocket_hideout_b2f()

	var b2f = b2f_scene.instantiate()
	b2f.save_state = save_state
	root.add_child(b2f)
	b2f._ready()

	var b3f_seen := [false]
	b2f.go_to_rocket_hideout_b3f.connect(func() -> void:
		b3f_seen[0] = true
	)

	b2f.trigger_rocket_hideout_b3f_entry()
	if b3f_seen[0]:
		push_error("Rocket Hideout B3F should stay locked before the B2F patrol is cleared.")
		quit(1)
		return
	if b2f.dialogue_label == null or not b2f.dialogue_label.text.contains("patrol"):
		push_error("Locked B3F path did not explain the B2F patrol requirement.")
		quit(1)
		return

	save_state.start_battle_placeholder("rocket_hideout_b2f_patrol")
	save_state.finish_battle_placeholder("placeholder_win")
	b2f.trigger_rocket_hideout_b3f_entry()
	if not b3f_seen[0]:
		push_error("Rocket Hideout B2F did not emit B3F after the patrol battle.")
		quit(1)
		return

	var b3f = b3f_scene.instantiate()
	b3f.save_state = save_state
	root.add_child(b3f)
	b3f._ready()
	if save_state.current_scene != "celadon_rocket_hideout_b3f":
		push_error("Rocket Hideout B3F did not update current scene.")
		quit(1)
		return
	if not save_state.story_flags.get("celadon_rocket_hideout_b3f_reached", false):
		push_error("Rocket Hideout B3F reached flag missing.")
		quit(1)
		return
	if not save_state.worldlink_queue.has("wl_celadon_rocket_hideout_b3f_reached"):
		push_error("WorldLink queue missing Rocket Hideout B3F arrival.")
		quit(1)
		return

	b3f.trigger_rocket_hideout_b3f_scene()
	for flag_name in [
		"red_hideout_b3f_lift_key_warning_seen",
		"bill_nexus_order_elevator_trace_seen",
		"rocket_admin_lift_key_battle_unlocked",
		"gold_dust_ledger_recovered_seen",
		"team_moonlight_sleep_panel_seen",
		"giovanni_elevator_route_seen",
	]:
		if not save_state.story_flags.get(flag_name, false):
			push_error("Rocket Hideout B3F flag missing: " + flag_name)
			quit(1)
			return
	for queue_id in [
		"wl_red_hideout_b3f_lift_key_warning",
		"wl_bill_nexus_order_elevator_trace",
		"wl_rocket_admin_lift_key_battle_unlocked",
		"wl_gold_dust_ledger_recovered",
		"wl_team_moonlight_sleep_panel",
		"wl_giovanni_elevator_route_seen",
	]:
		if not save_state.worldlink_queue.has(queue_id):
			push_error("WorldLink missing Rocket Hideout B3F id: " + queue_id)
			quit(1)
			return
	for required_text in ["Red", "Bill", "Rocket Admin", "Gold Dust", "Moonlight", "Nexus Order", "Lift Key", "Giovanni", "elevator"]:
		if b3f.dialogue_label == null or not b3f.dialogue_label.text.contains(required_text):
			push_error("Rocket Hideout B3F dialogue missing: " + required_text)
			quit(1)
			return

	var elevator_seen := [false]
	b3f.go_to_rocket_hideout_elevator.connect(func() -> void:
		elevator_seen[0] = true
	)
	b3f.trigger_rocket_hideout_elevator_entry()
	if elevator_seen[0]:
		push_error("Rocket Hideout elevator should stay locked before the B3F admin battle is finished.")
		quit(1)
		return

	var battle_seen := [false]
	b3f.start_battle_placeholder.connect(func(battle_id: String) -> void:
		battle_seen[0] = true
		if battle_id != "rocket_hideout_b3f_admin":
			push_error("Rocket Hideout B3F emitted wrong battle id: " + battle_id)
			quit(1)
	)
	b3f.trigger_rocket_hideout_b3f_admin_battle()
	if not battle_seen[0]:
		push_error("Rocket Hideout B3F did not emit admin battle.")
		quit(1)
		return
	if save_state.active_battle_id != "rocket_hideout_b3f_admin":
		push_error("Rocket Hideout B3F admin was not active in save state.")
		quit(1)
		return
	if not save_state.story_flags.get("rocket_admin_lift_key_battle_started", false):
		push_error("Rocket Hideout B3F admin started flag missing.")
		quit(1)
		return

	var battle = battle_scene.instantiate()
	battle.save_state = save_state
	battle.battle_id = "rocket_hideout_b3f_admin"
	root.add_child(battle)
	battle._ready()
	battle.finish_placeholder_battle()
	save_state.finish_battle_placeholder("placeholder_win")
	if not save_state.story_flags.get("rocket_admin_lift_key_battle_finished", false):
		push_error("Rocket Hideout B3F admin finished flag missing.")
		quit(1)
		return
	if not save_state.story_flags.get("rocket_lift_key_obtained", false):
		push_error("Rocket Lift Key obtained flag missing.")
		quit(1)
		return
	if not save_state.story_flags.get("rocket_hideout_elevator_path_unlocked", false):
		push_error("Rocket Hideout elevator path unlock flag missing.")
		quit(1)
		return
	for queue_id in [
		"wl_rocket_admin_lift_key_battle_finished",
		"wl_rocket_lift_key_obtained",
		"wl_rocket_hideout_elevator_path_unlocked",
	]:
		if not save_state.worldlink_queue.has(queue_id):
			push_error("WorldLink missing Rocket Hideout B3F post-battle id: " + queue_id)
			quit(1)
			return

	b3f.trigger_rocket_hideout_elevator_entry()
	if not elevator_seen[0]:
		push_error("Rocket Hideout B3F did not emit elevator path after admin battle.")
		quit(1)
		return

	var returned := [false]
	b3f.go_to_rocket_hideout_b2f.connect(func() -> void:
		returned[0] = true
	)
	b3f.return_to_rocket_hideout_b2f()
	if not returned[0]:
		push_error("Rocket Hideout B3F did not emit return to B2F.")
		quit(1)
		return

	battle.free()
	b3f.free()
	b2f.free()
	print("Native Celadon Rocket Hideout B3F smoke test passed.")
	quit(0)
