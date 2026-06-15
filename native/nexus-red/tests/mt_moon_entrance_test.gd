extends SceneTree


func _init() -> void:
	print("mt_moon_entrance_test")
	var save_state_script := load("res://src/save/SaveState.gd")
	var pewter_scene := load("res://scenes/world/PewterCity.tscn")
	var mt_moon_scene := load("res://scenes/world/MtMoonEntrance.tscn")

	if save_state_script == null or pewter_scene == null or mt_moon_scene == null:
		push_error("Mt. Moon entrance resources did not load.")
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
	save_state.enter_pewter_city()

	var pewter = pewter_scene.instantiate()
	pewter.save_state = save_state
	root.add_child(pewter)
	pewter._ready()

	var mt_moon_departure_seen := [false]
	pewter.go_to_mt_moon_entrance.connect(func() -> void:
		mt_moon_departure_seen[0] = true
	)
	pewter.trigger_mt_moon_departure()
	if mt_moon_departure_seen[0]:
		push_error("Pewter should not allow Mt. Moon departure before the museum anomaly.")
		quit(1)
		return
	if not pewter.dialogue_label.text.contains("museum"):
		push_error("Locked Mt. Moon departure should point back to the museum anomaly.")
		quit(1)
		return

	save_state.start_battle_placeholder("brock_pewter_gym")
	save_state.finish_battle_placeholder("placeholder_win")
	save_state.record_pewter_museum_anomaly()
	pewter.trigger_mt_moon_departure()
	if not mt_moon_departure_seen[0]:
		push_error("Pewter did not emit Mt. Moon departure after museum anomaly.")
		quit(1)
		return

	var mt_moon = mt_moon_scene.instantiate()
	mt_moon.save_state = save_state
	root.add_child(mt_moon)
	mt_moon._ready()
	if save_state.current_scene != "mt_moon_entrance":
		push_error("Mt. Moon entrance did not update current scene.")
		quit(1)
		return
	if not save_state.story_flags.get("mt_moon_entrance_reached", false):
		push_error("Mt. Moon entrance reached flag missing.")
		quit(1)
		return
	if not save_state.story_flags.get("red_mt_moon_warning_seen", false):
		push_error("Red Mt. Moon warning flag missing.")
		quit(1)
		return

	mt_moon.trigger_faction_conflict()
	if not save_state.story_flags.get("rocket_gold_dust_mt_moon_conflict_seen", false):
		push_error("Rocket/Gold Dust Mt. Moon conflict flag missing.")
		quit(1)
		return
	if not save_state.story_flags.get("nexus_fossil_hint_seen", false):
		push_error("Nexus Fossil hint flag missing.")
		quit(1)
		return
	if not save_state.worldlink_queue.has("wl_gold_dust_mt_moon_arrival"):
		push_error("WorldLink queue missing Gold Dust Mt. Moon arrival.")
		quit(1)
		return
	if mt_moon.dialogue_label == null or not mt_moon.dialogue_label.text.contains("Team Rocket") or not mt_moon.dialogue_label.text.contains("Team Gold Dust"):
		push_error("Mt. Moon conflict dialogue did not name Team Rocket and Team Gold Dust.")
		quit(1)
		return
	if not mt_moon.dialogue_label.text.contains("Nexus Fossil"):
		push_error("Mt. Moon conflict dialogue did not introduce Nexus Fossil.")
		quit(1)
		return

	var pewter_return_seen := [false]
	mt_moon.go_to_pewter_city.connect(func() -> void:
		pewter_return_seen[0] = true
	)
	mt_moon.return_to_pewter_city()
	if not pewter_return_seen[0]:
		push_error("Mt. Moon entrance did not emit return to Pewter City.")
		quit(1)
		return

	mt_moon.free()
	pewter.free()
	print("Native Mt. Moon entrance smoke test passed.")
	quit(0)
