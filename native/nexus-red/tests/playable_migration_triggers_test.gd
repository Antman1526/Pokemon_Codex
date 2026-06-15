extends SceneTree


func _init() -> void:
	print("playable_migration_triggers_test")
	var save_state_script := load("res://src/save/SaveState.gd")
	var encounter_service_script := load("res://src/encounter/EncounterService.gd")
	var route1_scene := load("res://scenes/world/Route1.tscn")
	var route2_scene := load("res://scenes/world/Route2ForestGate.tscn")

	if save_state_script == null or encounter_service_script == null or route1_scene == null or route2_scene == null:
		push_error("Playable migration trigger resources did not load.")
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

	var service = encounter_service_script.new()
	var route1_pick: Dictionary = service.pick_early_migration_encounter("route_1", save_state)
	if route1_pick.get("id", "") != "route_1_migration_bulbasaur":
		push_error("Route 1 migration picker did not return the first Route 1 migration encounter.")
		quit(1)
		return

	var route1 = route1_scene.instantiate()
	route1.save_state = save_state
	root.add_child(route1)
	route1._ready()

	var route1_seen := [false]
	route1.start_wild_encounter.connect(func(encounter_data: Dictionary) -> void:
		route1_seen[0] = true
		if encounter_data.get("id", "") != "route_1_migration_bulbasaur":
			push_error("Route 1 emitted the wrong migration encounter.")
			quit(1)
	)
	route1.trigger_route_1_migration_encounter()
	if not route1_seen[0]:
		push_error("Route 1 did not emit a migration encounter.")
		quit(1)
		return
	if save_state.active_encounter_id != "route_1_migration_bulbasaur":
		push_error("Route 1 migration encounter was not active in save state.")
		quit(1)
		return
	save_state.finish_wild_encounter("catch_success")
	if not save_state.captured_creatures.has("Bulbasaur"):
		push_error("Route 1 migration catch did not record Bulbasaur.")
		quit(1)
		return

	var route1_next: Dictionary = service.pick_early_migration_encounter("route_1", save_state)
	if route1_next.get("id", "") != "route_1_migration_charmander":
		push_error("Route 1 migration picker did not skip captured Bulbasaur.")
		quit(1)
		return

	save_state.enter_route_2_forest_gate()
	var route2 = route2_scene.instantiate()
	route2.save_state = save_state
	root.add_child(route2)
	route2._ready()

	var route2_seen := [false]
	route2.start_wild_encounter.connect(func(encounter_data: Dictionary) -> void:
		route2_seen[0] = true
		if encounter_data.get("id", "") != "route_2_migration_treecko":
			push_error("Route 2 emitted the wrong migration encounter.")
			quit(1)
	)
	route2.trigger_route_2_migration_encounter()
	if not route2_seen[0]:
		push_error("Route 2 did not emit a migration encounter.")
		quit(1)
		return
	if save_state.active_encounter_id != "route_2_migration_treecko":
		push_error("Route 2 migration encounter was not active in save state.")
		quit(1)
		return
	if save_state.encounter_return_scene != "route_2_forest_gate":
		push_error("Route 2 migration encounter did not preserve the Route 2 return scene.")
		quit(1)
		return

	route2.free()
	route1.free()
	print("Native playable migration trigger smoke test passed.")
	quit(0)
