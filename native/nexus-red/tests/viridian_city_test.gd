extends SceneTree


func _init() -> void:
	print("viridian_city_test")
	var save_state_script := load("res://src/save/SaveState.gd")
	var route_scene := load("res://scenes/world/Route1.tscn")
	var viridian_scene := load("res://scenes/world/ViridianCity.tscn")

	if save_state_script == null or route_scene == null or viridian_scene == null:
		push_error("Viridian City resources did not load.")
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
	save_state.start_wild_encounter({
		"id": "route_1_first_wild",
		"species": "Rattata",
		"level": 3,
	})
	save_state.finish_wild_encounter("catch_success")

	var route = route_scene.instantiate()
	route.save_state = save_state
	root.add_child(route)
	route._ready()

	var transition_seen := [false]
	route.go_to_viridian_city.connect(func() -> void:
		transition_seen[0] = true
	)
	route.trigger_viridian_city_entry()
	if not transition_seen[0]:
		push_error("Route 1 did not emit Viridian transition.")
		quit(1)
		return

	var city = viridian_scene.instantiate()
	city.save_state = save_state
	root.add_child(city)
	city._ready()
	if save_state.current_scene != "viridian_city":
		push_error("Viridian City did not update current scene.")
		quit(1)
		return
	if not save_state.story_flags.get("viridian_city_reached", false):
		push_error("Viridian City reached flag missing.")
		quit(1)
		return
	if city.dialogue_label == null or not city.dialogue_label.text.contains("Nurse Joy"):
		push_error("Viridian intro did not mention Nurse Joy.")
		quit(1)
		return

	city.interact_pokemon_center()
	if not save_state.story_flags.get("viridian_center_visited", false):
		push_error("Pokemon Center interaction did not set flag.")
		quit(1)
		return
	if not city.dialogue_label.text.contains("healed"):
		push_error("Pokemon Center interaction did not update dialogue.")
		quit(1)
		return

	city.interact_poke_mart()
	if not save_state.story_flags.get("viridian_mart_visited", false):
		push_error("Poke Mart interaction did not set flag.")
		quit(1)
		return
	if not city.dialogue_label.text.contains("$100000"):
		push_error("Poke Mart interaction did not show starting money.")
		quit(1)
		return

	city.free()
	route.free()
	print("Native Viridian City smoke test passed.")
	quit(0)
