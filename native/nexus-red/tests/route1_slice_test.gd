extends SceneTree


func _init() -> void:
	print("route1_slice_test")
	var save_state_script := load("res://src/save/SaveState.gd")
	var route_scene := load("res://scenes/world/Route1.tscn")
	var player_script := load("res://src/world/PlayerAvatar.gd")

	if save_state_script == null or route_scene == null or player_script == null:
		push_error("Route 1 slice resources did not load.")
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

	var route = route_scene.instantiate()
	route.save_state = save_state
	root.add_child(route)
	route._ready()

	if not save_state.story_flags.get("route_1_reached", false):
		push_error("Route 1 reached flag was not set.")
		quit(1)
		return

	route.trigger_red_scene()
	if not save_state.story_flags.get("red_route_1_companion_scene_seen", false):
		push_error("Red Route 1 companion flag was not set.")
		quit(1)
		return

	route.trigger_blue_battle_placeholder()
	if not save_state.story_flags.get("blue_battle_placeholder_seen", false):
		push_error("Blue battle placeholder flag was not set.")
		quit(1)
		return

	var player = player_script.new()
	player.position = Vector2(610, 560)
	player._ready()
	if player.move_speed <= 0:
		push_error("Player avatar move speed must be positive.")
		quit(1)
		return
	player.free()
	route.free()

	print("Native Route 1 slice smoke test passed.")
	quit(0)
