extends SceneTree


func _init() -> void:
	print("celadon_rocket_command_floor_test")
	var save_state_script := load("res://src/save/SaveState.gd")
	var elevator_scene := load("res://scenes/world/CeladonRocketHideoutElevator.tscn")
	var command_floor_scene := load("res://scenes/world/CeladonRocketCommandFloor.tscn")
	var battle_scene := load("res://scenes/battle/BattlePlaceholder.tscn")

	if save_state_script == null or elevator_scene == null or command_floor_scene == null or battle_scene == null:
		push_error("Celadon Rocket command floor resources did not load.")
		quit(1)
		return

	var save_state = save_state_script.new()
	save_state.start_new_game("Antman")
	save_state.enter_celadon_rocket_hideout_elevator()

	var elevator = elevator_scene.instantiate()
	elevator.save_state = save_state
	root.add_child(elevator)
	elevator._ready()

	var command_floor_seen := [false]
	elevator.go_to_rocket_command_floor.connect(func() -> void:
		command_floor_seen[0] = true
	)

	elevator.trigger_rocket_command_floor_entry()
	if command_floor_seen[0]:
		push_error("Rocket command floor should stay locked before elevator routing is decoded.")
		quit(1)
		return
	if elevator.dialogue_label == null or not elevator.dialogue_label.text.contains("command floor"):
		push_error("Locked command floor did not explain the elevator routing requirement.")
		quit(1)
		return

	elevator.trigger_rocket_hideout_elevator_scene()
	elevator.trigger_rocket_command_floor_entry()
	if not command_floor_seen[0]:
		push_error("Rocket Hideout elevator did not emit command floor after decoding.")
		quit(1)
		return

	var command_floor = command_floor_scene.instantiate()
	command_floor.save_state = save_state
	root.add_child(command_floor)
	command_floor._ready()
	if save_state.current_scene != "celadon_rocket_command_floor":
		push_error("Rocket command floor did not update current scene.")
		quit(1)
		return
	if not save_state.story_flags.get("celadon_rocket_command_floor_reached", false):
		push_error("Rocket command floor reached flag missing.")
		quit(1)
		return
	if not save_state.worldlink_queue.has("wl_celadon_rocket_command_floor_reached"):
		push_error("WorldLink queue missing Rocket command floor arrival.")
		quit(1)
		return

	command_floor.trigger_rocket_command_floor_scene()
	for flag_name in [
		"red_command_floor_door_guard_seen",
		"bill_nexus_order_command_terminal_seen",
		"giovanni_first_confrontation_seen",
		"rocket_silph_scope_cache_seen",
		"gold_dust_command_floor_ledger_seen",
		"team_moonlight_command_floor_signal_seen",
		"giovanni_command_floor_battle_unlocked",
	]:
		if not save_state.story_flags.get(flag_name, false):
			push_error("Rocket command floor flag missing: " + flag_name)
			quit(1)
			return
	for queue_id in [
		"wl_red_command_floor_door_guard",
		"wl_bill_nexus_order_command_terminal",
		"wl_giovanni_first_confrontation",
		"wl_rocket_silph_scope_cache",
		"wl_gold_dust_command_floor_ledger",
		"wl_team_moonlight_command_floor_signal",
		"wl_giovanni_command_floor_battle_unlocked",
	]:
		if not save_state.worldlink_queue.has(queue_id):
			push_error("WorldLink missing Rocket command floor id: " + queue_id)
			quit(1)
			return
	for required_text in ["Red", "Bill", "Giovanni", "Silph Scope", "Gold Dust", "Moonlight", "Nexus Order", "Pokemon Tower", "Erika"]:
		if command_floor.dialogue_label == null or not command_floor.dialogue_label.text.contains(required_text):
			push_error("Rocket command floor dialogue missing: " + required_text)
			quit(1)
			return

	var battle_seen := [false]
	command_floor.start_battle_placeholder.connect(func(battle_id: String) -> void:
		battle_seen[0] = true
		if battle_id != "giovanni_celadon_command_floor":
			push_error("Rocket command floor emitted wrong battle id: " + battle_id)
			quit(1)
	)
	command_floor.trigger_giovanni_command_floor_battle()
	if not battle_seen[0]:
		push_error("Rocket command floor did not emit Giovanni battle.")
		quit(1)
		return
	if save_state.active_battle_id != "giovanni_celadon_command_floor":
		push_error("Giovanni command floor battle was not active in save state.")
		quit(1)
		return
	if not save_state.story_flags.get("giovanni_command_floor_battle_started", false):
		push_error("Giovanni command floor battle started flag missing.")
		quit(1)
		return

	var battle = battle_scene.instantiate()
	battle.save_state = save_state
	battle.battle_id = "giovanni_celadon_command_floor"
	root.add_child(battle)
	battle._ready()
	battle.finish_placeholder_battle()
	save_state.finish_battle_placeholder("placeholder_win")
	if not save_state.story_flags.get("giovanni_command_floor_battle_finished", false):
		push_error("Giovanni command floor battle finished flag missing.")
		quit(1)
		return
	if not save_state.story_flags.get("silph_scope_obtained", false):
		push_error("Silph Scope obtained flag missing.")
		quit(1)
		return
	if not save_state.story_flags.get("pokemon_tower_deeper_path_unlocked", false):
		push_error("Pokemon Tower deeper path unlock flag missing.")
		quit(1)
		return
	if not save_state.story_flags.get("erika_gym_path_unlocked", false):
		push_error("Erika gym path unlock flag missing.")
		quit(1)
		return
	for queue_id in [
		"wl_giovanni_command_floor_battle_finished",
		"wl_silph_scope_obtained",
		"wl_pokemon_tower_deeper_path_unlocked",
		"wl_erika_gym_path_unlocked",
	]:
		if not save_state.worldlink_queue.has(queue_id):
			push_error("WorldLink missing Rocket command floor post-battle id: " + queue_id)
			quit(1)
			return

	var returned := [false]
	command_floor.go_to_rocket_hideout_elevator.connect(func() -> void:
		returned[0] = true
	)
	command_floor.return_to_rocket_hideout_elevator()
	if not returned[0]:
		push_error("Rocket command floor did not emit return to elevator.")
		quit(1)
		return

	battle.free()
	command_floor.free()
	elevator.free()
	print("Native Celadon Rocket command floor smoke test passed.")
	quit(0)
