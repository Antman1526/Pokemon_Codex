extends SceneTree


func _init() -> void:
	print("wild_encounter_loop_test")
	var save_state_script := load("res://src/save/SaveState.gd")
	var encounter_service_script := load("res://src/encounter/EncounterService.gd")
	var encounter_scene := load("res://scenes/encounter/WildEncounterPlaceholder.tscn")

	if save_state_script == null or encounter_service_script == null or encounter_scene == null:
		push_error("Wild encounter loop resources did not load.")
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
	save_state.start_wild_encounter(encounter)

	var screen = encounter_scene.instantiate()
	screen.save_state = save_state
	screen.encounter_data = save_state.active_encounter_data
	root.add_child(screen)
	screen._ready()

	if screen.wild_hp <= 0 or screen.wild_max_hp <= 0:
		push_error("Wild encounter did not initialize HP.")
		quit(1)
		return
	if screen.wild_hp != screen.wild_max_hp:
		push_error("Wild encounter should begin at full HP.")
		quit(1)
		return

	var results: Array[String] = []
	screen.encounter_finished.connect(func(result: String) -> void:
		results.append(result)
	)

	screen.attempt_capture()
	if not results.is_empty():
		push_error("Capture should not succeed at full HP in the first loop.")
		quit(1)
		return

	var starting_hp: int = screen.wild_hp
	screen.attack_wild()
	if screen.wild_hp >= starting_hp:
		push_error("Attack did not lower wild HP.")
		quit(1)
		return
	if screen.dialogue_label == null or not screen.dialogue_label.text.contains("Red:"):
		push_error("Red coaching line was not shown after attack.")
		quit(1)
		return

	screen.attempt_capture()
	if results.size() != 1 or results[0] != "catch_success":
		push_error("Damaged first wild encounter did not produce catch_success.")
		quit(1)
		return
	save_state.finish_wild_encounter(results[0])

	if save_state.last_encounter_result != "catch_success":
		push_error("Save state did not record catch_success.")
		quit(1)
		return
	if not save_state.story_flags.get("route_1_first_wild_caught", false):
		push_error("Route 1 first wild caught flag missing after catch_success.")
		quit(1)
		return
	if not save_state.captured_creatures.has("Rattata"):
		push_error("Rattata was not added to captured creatures after catch_success.")
		quit(1)
		return

	screen.free()
	print("Native wild encounter loop smoke test passed.")
	quit(0)
