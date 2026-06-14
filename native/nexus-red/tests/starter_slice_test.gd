extends SceneTree


func _init() -> void:
	print("starter_slice_test")
	var save_state_script := load("res://src/save/SaveState.gd")
	var selector_script := load("res://src/starter/StarterSelector.gd")
	var oak_lab_scene := load("res://scenes/world/OakLab.tscn")

	if save_state_script == null or selector_script == null or oak_lab_scene == null:
		push_error("Starter slice resources did not load.")
		quit(1)
		return

	var save_state = save_state_script.new()
	save_state.start_new_game("Antman")

	var selector = selector_script.new()
	root.add_child(selector)
	selector._ready()
	selector.starter_selected.connect(func(selection: Dictionary) -> void:
		save_state.choose_starter(selection)
	)
	selector.choose_starter("Bulbasaur")

	if save_state.player_starter != "Bulbasaur":
		push_error("Player starter was not saved.")
		quit(1)
		return
	if save_state.blue_starter != "Charmander":
		push_error("Blue starter was not assigned as expected.")
		quit(1)
		return
	if save_state.ava_starter == "" or save_state.dax_starter == "":
		push_error("Ava or Dax starter assignment is missing.")
		quit(1)
		return
	if save_state.ava_starter in [save_state.player_starter, save_state.blue_starter]:
		push_error("Ava starter duplicated the player or Blue.")
		quit(1)
		return
	if save_state.dax_starter in [save_state.player_starter, save_state.blue_starter, save_state.ava_starter]:
		push_error("Dax starter duplicated another lab assignment.")
		quit(1)
		return
	if not save_state.story_flags.get("starter_chosen", false):
		push_error("Starter chosen flag was not set.")
		quit(1)
		return
	if not save_state.story_flags.get("blue_pressure_scene_seen", false):
		push_error("Blue pressure flag was not set.")
		quit(1)
		return

	var oak_lab = oak_lab_scene.instantiate()
	oak_lab.save_state = save_state
	root.add_child(oak_lab)
	oak_lab._ready()

	print("Native starter slice smoke test passed.")
	quit(0)
