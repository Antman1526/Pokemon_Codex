extends SceneTree


func _init() -> void:
	print("route8_celadon_road_test")
	var save_state_script := load("res://src/save/SaveState.gd")
	var tower_scene := load("res://scenes/world/PokemonTowerFirstFloor.tscn")
	var route8_scene := load("res://scenes/world/Route8CeladonRoad.tscn")

	if save_state_script == null or tower_scene == null or route8_scene == null:
		push_error("Route 8 Celadon road resources did not load.")
		quit(1)
		return

	var save_state = save_state_script.new()
	save_state.start_new_game("Antman")
	save_state.enter_pokemon_tower_first_floor()

	var tower = tower_scene.instantiate()
	tower.save_state = save_state
	root.add_child(tower)
	tower._ready()

	var route8_seen := [false]
	tower.go_to_route_8_celadon_road.connect(func() -> void:
		route8_seen[0] = true
	)

	tower.trigger_route_8_celadon_lead()
	if route8_seen[0]:
		push_error("Route 8 should stay locked before the Pokemon Tower first floor investigation is complete.")
		quit(1)
		return
	if tower.dialogue_label == null or not tower.dialogue_label.text.contains("Silph Scope"):
		push_error("Locked Route 8 lead did not point back to the Silph Scope clue.")
		quit(1)
		return

	tower.trigger_pokemon_tower_first_floor_scene()
	tower.trigger_route_8_celadon_lead()
	if not route8_seen[0]:
		push_error("Pokemon Tower did not emit Route 8 after Silph Scope lead unlock.")
		quit(1)
		return

	var route8 = route8_scene.instantiate()
	route8.save_state = save_state
	root.add_child(route8)
	route8._ready()
	if save_state.current_scene != "route_8_celadon_road":
		push_error("Route 8 Celadon road did not update current scene.")
		quit(1)
		return
	if not save_state.story_flags.get("route_8_celadon_road_reached", false):
		push_error("Route 8 Celadon road reached flag missing.")
		quit(1)
		return
	if not save_state.worldlink_queue.has("wl_route_8_celadon_road_reached"):
		push_error("WorldLink queue missing Route 8 arrival.")
		quit(1)
		return

	route8.trigger_route_8_celadon_road_scene()
	for flag_name in [
		"red_route_8_westbound_seen",
		"bill_silph_scope_celadon_trace_seen",
		"rocket_celadon_game_corner_lead_seen",
		"team_moonlight_route_8_shadow_seen",
		"underground_path_to_celadon_unlocked",
		"celadon_city_teased",
	]:
		if not save_state.story_flags.get(flag_name, false):
			push_error("Route 8 Celadon road flag missing: " + flag_name)
			quit(1)
			return
	for queue_id in [
		"wl_red_route_8_westbound",
		"wl_bill_silph_scope_celadon_trace",
		"wl_rocket_celadon_game_corner_lead",
		"wl_team_moonlight_route_8_shadow",
		"wl_underground_path_to_celadon_unlocked",
		"wl_celadon_city_teased",
	]:
		if not save_state.worldlink_queue.has(queue_id):
			push_error("WorldLink missing Route 8 id: " + queue_id)
			quit(1)
			return
	for required_text in ["Red", "Bill", "Rocket", "Moonlight", "Route 8", "Celadon", "Silph Scope", "Game Corner", "Underground Path"]:
		if route8.dialogue_label == null or not route8.dialogue_label.text.contains(required_text):
			push_error("Route 8 dialogue missing: " + required_text)
			quit(1)
			return

	var returned := [false]
	route8.go_to_pokemon_tower_first_floor.connect(func() -> void:
		returned[0] = true
	)
	route8.return_to_pokemon_tower_first_floor()
	if not returned[0]:
		push_error("Route 8 scene did not emit return to Pokemon Tower.")
		quit(1)
		return

	route8.free()
	tower.free()
	print("Native Route 8 Celadon road smoke test passed.")
	quit(0)
