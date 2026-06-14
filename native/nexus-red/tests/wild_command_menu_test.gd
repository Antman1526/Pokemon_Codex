extends SceneTree


func _init() -> void:
	print("wild_command_menu_test")
	var save_state_script := load("res://src/save/SaveState.gd")
	var encounter_service_script := load("res://src/encounter/EncounterService.gd")
	var encounter_scene := load("res://scenes/encounter/WildEncounterPlaceholder.tscn")

	if save_state_script == null or encounter_service_script == null or encounter_scene == null:
		push_error("Wild command menu resources did not load.")
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

	if screen.command_menu == null:
		push_error("Command menu was not created.")
		quit(1)
		return
	if screen.fight_button == null or screen.catch_button == null or screen.run_button == null:
		push_error("Fight/Catch/Run buttons were not created.")
		quit(1)
		return
	if screen.fight_button.text != "Fight" or screen.catch_button.text != "Catch" or screen.run_button.text != "Run":
		push_error("Command button labels are incorrect.")
		quit(1)
		return
	if screen.catch_button.disabled:
		push_error("Catch button should be visible and enabled even before capture is likely.")
		quit(1)
		return

	var results: Array[String] = []
	screen.encounter_finished.connect(func(result: String) -> void:
		results.append(result)
	)

	var starting_hp: int = screen.wild_hp
	screen.fight_button.pressed.emit()
	if screen.wild_hp >= starting_hp:
		push_error("Fight command did not lower wild HP.")
		quit(1)
		return
	if screen.fight_button.disabled:
		push_error("Fight command should remain visible and enabled after attacking.")
		quit(1)
		return

	screen.catch_button.pressed.emit()
	if results.size() != 1 or results[0] != "catch_success":
		push_error("Catch command did not produce catch_success after damage.")
		quit(1)
		return

	var second_screen = encounter_scene.instantiate()
	second_screen.save_state = save_state
	second_screen.encounter_data = encounter
	root.add_child(second_screen)
	second_screen._ready()
	var run_results: Array[String] = []
	second_screen.encounter_finished.connect(func(result: String) -> void:
		run_results.append(result)
	)
	second_screen.run_button.pressed.emit()
	if run_results.size() != 1 or run_results[0] != "placeholder_run":
		push_error("Run command did not produce placeholder_run.")
		quit(1)
		return

	screen.free()
	second_screen.free()
	print("Native wild command menu smoke test passed.")
	quit(0)
