extends SceneTree


func _init() -> void:
	print("route2_catch_tutorial_test")
	var save_state_script := load("res://src/save/SaveState.gd")
	var encounter_service_script := load("res://src/encounter/EncounterService.gd")
	var route2_scene := load("res://scenes/world/Route2ForestGate.tscn")
	var encounter_scene := load("res://scenes/encounter/WildEncounterPlaceholder.tscn")

	if save_state_script == null or encounter_service_script == null or route2_scene == null or encounter_scene == null:
		push_error("Route 2 catch tutorial resources did not load.")
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
	save_state.enter_route_2_forest_gate()

	var service = encounter_service_script.new()
	var encounter: Dictionary = service.pick_route_2_encounter(save_state)
	if encounter.get("id", "") != "route_2_red_catch_tutorial_pidgey":
		push_error("Route 2 first tutorial encounter id was not deterministic.")
		quit(1)
		return
	if encounter.get("species", "") != "Pidgey" or int(encounter.get("level", 0)) != 4:
		push_error("Route 2 first tutorial encounter did not match expected Pidgey Lv. 4.")
		quit(1)
		return
	if encounter.get("return_scene", "") != "route_2_forest_gate":
		push_error("Route 2 first tutorial encounter did not target the forest gate return scene.")
		quit(1)
		return

	var route2 = route2_scene.instantiate()
	route2.save_state = save_state
	root.add_child(route2)
	route2._ready()

	var encounter_seen := [false]
	route2.start_wild_encounter.connect(func(encounter_data: Dictionary) -> void:
		encounter_seen[0] = true
		if encounter_data.get("id", "") != "route_2_red_catch_tutorial_pidgey":
			push_error("Route 2 scene emitted the wrong tutorial encounter.")
			quit(1)
	)
	route2.trigger_route_2_catch_tutorial()
	if not encounter_seen[0]:
		push_error("Route 2 did not emit catch tutorial encounter.")
		quit(1)
		return
	if save_state.active_encounter_id != "route_2_red_catch_tutorial_pidgey":
		push_error("Route 2 did not set the active tutorial encounter.")
		quit(1)
		return
	if save_state.encounter_return_scene != "route_2_forest_gate":
		push_error("Route 2 did not preserve its return scene for the encounter.")
		quit(1)
		return
	if not save_state.story_flags.get("route_2_catch_tutorial_seen", false):
		push_error("Route 2 catch tutorial seen flag missing.")
		quit(1)
		return

	var encounter_screen = encounter_scene.instantiate()
	encounter_screen.save_state = save_state
	encounter_screen.encounter_data = save_state.active_encounter_data
	root.add_child(encounter_screen)
	encounter_screen._ready()
	encounter_screen.attack_wild()
	encounter_screen.attempt_capture()
	save_state.finish_wild_encounter("catch_success")

	if not save_state.story_flags.get("route_2_catch_tutorial_caught", false):
		push_error("Route 2 catch tutorial caught flag missing.")
		quit(1)
		return
	if not save_state.captured_creatures.has("Pidgey"):
		push_error("Captured creatures did not include Route 2 Pidgey.")
		quit(1)
		return

	var migration_encounter: Dictionary = service.pick_route_2_encounter(save_state)
	if migration_encounter.get("id", "") != "route_2_migration_treecko":
		push_error("Route 2 normal grass did not surface the first migration starter after the catch tutorial.")
		quit(1)
		return
	if migration_encounter.get("species", "") != "Treecko":
		push_error("Route 2 normal grass migration encounter was not Treecko.")
		quit(1)
		return

	encounter_screen.free()
	route2.free()
	print("Native Route 2 catch tutorial smoke test passed.")
	quit(0)
