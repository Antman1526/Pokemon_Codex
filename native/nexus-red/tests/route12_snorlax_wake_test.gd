extends SceneTree


func _init() -> void:
	print("route12_snorlax_wake_test")
	var save_state_script := load("res://src/save/SaveState.gd")
	var fuji_scene := load("res://scenes/world/PokemonTowerFujiRescue.tscn")
	var route12_scene := load("res://scenes/world/Route12SnorlaxWake.tscn")

	if save_state_script == null or fuji_scene == null or route12_scene == null:
		push_error("Route 12 Snorlax wake resources did not load.")
		quit(1)
		return

	var save_state = save_state_script.new()
	save_state.start_new_game("Antman")
	save_state.enter_pokemon_tower_fuji_rescue()

	var fuji = fuji_scene.instantiate()
	fuji.save_state = save_state
	root.add_child(fuji)
	fuji._ready()

	var route12_seen := [false]
	fuji.go_to_route_12_snorlax_wake.connect(func() -> void:
		route12_seen[0] = true
	)

	fuji.trigger_route_12_snorlax_wake_path()
	if route12_seen[0]:
		push_error("Route 12 Snorlax wake should stay locked before Poke Flute is obtained.")
		quit(1)
		return
	if fuji.dialogue_label == null or not fuji.dialogue_label.text.contains("Poke Flute"):
		push_error("Locked Route 12 path did not point back to the Poke Flute.")
		quit(1)
		return

	save_state.set_flag("poke_flute_obtained", true)
	save_state.set_flag("snorlax_wake_path_unlocked", true)
	fuji.trigger_route_12_snorlax_wake_path()
	if not route12_seen[0]:
		push_error("Fuji rescue did not emit Route 12 Snorlax wake after Poke Flute unlock.")
		quit(1)
		return

	var route12 = route12_scene.instantiate()
	route12.save_state = save_state
	root.add_child(route12)
	route12._ready()
	if save_state.current_scene != "route_12_snorlax_wake":
		push_error("Route 12 Snorlax wake did not update current scene.")
		quit(1)
		return
	if not save_state.story_flags.get("route_12_snorlax_wake_reached", false):
		push_error("Route 12 Snorlax wake reached flag missing.")
		quit(1)
		return
	if not save_state.worldlink_queue.has("wl_route_12_snorlax_wake_reached"):
		push_error("WorldLink queue missing Route 12 Snorlax arrival.")
		quit(1)
		return

	route12.trigger_route_12_snorlax_wake_scene()
	for flag_name in [
		"red_route_12_flute_guard_seen",
		"bill_poke_flute_signal_confirmed",
		"team_moonlight_sleep_echo_cleared",
		"snorlax_roadblock_cleared",
		"route_12_south_path_unlocked",
	]:
		if not save_state.story_flags.get(flag_name, false):
			push_error("Route 12 Snorlax wake flag missing: " + flag_name)
			quit(1)
			return
	for queue_id in [
		"wl_red_route_12_flute_guard",
		"wl_bill_poke_flute_signal_confirmed",
		"wl_team_moonlight_sleep_echo_cleared",
		"wl_snorlax_roadblock_cleared",
		"wl_route_12_south_path_unlocked",
	]:
		if not save_state.worldlink_queue.has(queue_id):
			push_error("WorldLink missing Route 12 Snorlax id: " + queue_id)
			quit(1)
			return
	for required_text in ["Red", "Bill", "Poke Flute", "Snorlax", "Moonlight", "Route 12"]:
		if route12.dialogue_label == null or not route12.dialogue_label.text.contains(required_text):
			push_error("Route 12 Snorlax dialogue missing: " + required_text)
			quit(1)
			return

	var encounter_seen := [false]
	route12.start_wild_encounter.connect(func(encounter_data: Dictionary) -> void:
		encounter_seen[0] = true
		if str(encounter_data.get("id", "")) != "route_12_snorlax_static":
			push_error("Route 12 emitted wrong encounter id: " + str(encounter_data.get("id", "")))
			quit(1)
		if str(encounter_data.get("species", "")) != "Snorlax":
			push_error("Route 12 static encounter was not Snorlax.")
			quit(1)
	)
	route12.trigger_snorlax_static_encounter()
	if not encounter_seen[0]:
		push_error("Route 12 Snorlax wake did not emit static encounter.")
		quit(1)
		return
	if save_state.active_encounter_id != "route_12_snorlax_static":
		push_error("Route 12 Snorlax encounter was not active in save state.")
		quit(1)
		return
	if not save_state.story_flags.get("snorlax_static_encounter_seen", false):
		push_error("Snorlax static encounter seen flag missing.")
		quit(1)
		return
	if not save_state.worldlink_queue.has("wl_snorlax_static_encounter_seen"):
		push_error("WorldLink missing Snorlax static encounter id.")
		quit(1)
		return

	var returned := [false]
	route12.go_to_pokemon_tower_fuji_rescue.connect(func() -> void:
		returned[0] = true
	)
	route12.return_to_pokemon_tower_fuji_rescue()
	if not returned[0]:
		push_error("Route 12 Snorlax wake did not emit return to Fuji rescue.")
		quit(1)
		return

	route12.free()
	fuji.free()
	print("Native Route 12 Snorlax wake smoke test passed.")
	quit(0)
