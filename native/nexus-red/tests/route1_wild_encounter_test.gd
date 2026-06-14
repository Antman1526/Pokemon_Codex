extends SceneTree


func _init() -> void:
	print("route1_wild_encounter_test")
	var save_state_script := load("res://src/save/SaveState.gd")
	var encounter_service_script := load("res://src/encounter/EncounterService.gd")
	var encounter_scene := load("res://scenes/encounter/WildEncounterPlaceholder.tscn")
	var route_scene := load("res://scenes/world/Route1.tscn")

	if save_state_script == null or encounter_service_script == null or encounter_scene == null or route_scene == null:
		push_error("Route 1 wild encounter resources did not load.")
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

	var service = encounter_service_script.new()
	var encounter: Dictionary = service.pick_route_1_encounter(save_state)
	if encounter.get("id", "") != "route_1_first_wild":
		push_error("Route 1 first encounter id was not deterministic.")
		quit(1)
		return
	if encounter.get("species", "") != "Rattata" or int(encounter.get("level", 0)) != 3:
		push_error("Route 1 first encounter did not match expected Rattata Lv. 3.")
		quit(1)
		return

	var route = route_scene.instantiate()
	route.save_state = save_state
	root.add_child(route)
	route._ready()
	route.trigger_route_1_wild_encounter()
	if save_state.active_encounter_id != "route_1_first_wild":
		push_error("Route 1 did not start the first wild encounter.")
		quit(1)
		return

	var encounter_screen = encounter_scene.instantiate()
	encounter_screen.save_state = save_state
	encounter_screen.encounter_data = save_state.active_encounter_data
	root.add_child(encounter_screen)
	encounter_screen._ready()
	encounter_screen.finish_placeholder_catch()
	save_state.finish_wild_encounter("placeholder_catch")

	if save_state.active_encounter_id != "":
		push_error("Active encounter id did not clear.")
		quit(1)
		return
	if save_state.last_encounter_result != "placeholder_catch":
		push_error("Last encounter result was not recorded.")
		quit(1)
		return
	if not save_state.story_flags.get("route_1_first_wild_seen", false):
		push_error("Route 1 first wild seen flag missing.")
		quit(1)
		return
	if not save_state.story_flags.get("route_1_first_wild_caught", false):
		push_error("Route 1 first wild caught flag missing.")
		quit(1)
		return
	if not save_state.captured_creatures.has("Rattata"):
		push_error("Captured creatures did not include Rattata.")
		quit(1)
		return
	if not save_state.party_roster.has("Bulbasaur") or not save_state.party_roster.has("Rattata"):
		push_error("Party roster did not include starter and caught creature.")
		quit(1)
		return

	encounter_screen.free()
	route.free()
	print("Native Route 1 wild encounter smoke test passed.")
	quit(0)
