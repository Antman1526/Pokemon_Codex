extends SceneTree


func _init() -> void:
	print("battle_placeholder_test")
	var save_state_script := load("res://src/save/SaveState.gd")
	var battle_scene := load("res://scenes/battle/BattlePlaceholder.tscn")
	var route_scene := load("res://scenes/world/Route1.tscn")

	if save_state_script == null or battle_scene == null or route_scene == null:
		push_error("Battle placeholder resources did not load.")
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
	save_state.enter_route_1()

	var route = route_scene.instantiate()
	route.save_state = save_state
	root.add_child(route)
	route._ready()
	route.trigger_blue_battle_placeholder()
	if not save_state.story_flags.get("blue_battle_placeholder_seen", false):
		push_error("Blue placeholder route flag was not set.")
		quit(1)
		return

	save_state.start_battle_placeholder("blue_route_1")
	var battle = battle_scene.instantiate()
	battle.save_state = save_state
	battle.battle_id = "blue_route_1"
	root.add_child(battle)
	battle._ready()
	battle.finish_placeholder_battle()
	save_state.finish_battle_placeholder("placeholder_win")

	if save_state.active_battle_id != "":
		push_error("Active battle id did not clear.")
		quit(1)
		return
	if save_state.last_battle_result != "placeholder_win":
		push_error("last_battle_result was not recorded.")
		quit(1)
		return
	if not save_state.story_flags.get("blue_route_1_battle_started", false):
		push_error("Blue Route 1 battle start flag missing.")
		quit(1)
		return
	if not save_state.story_flags.get("blue_route_1_battle_finished", false):
		push_error("Blue Route 1 battle finish flag missing.")
		quit(1)
		return

	battle.free()
	route.free()
	print("Native battle placeholder smoke test passed.")
	quit(0)
