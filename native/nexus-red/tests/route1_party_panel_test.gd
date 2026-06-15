extends SceneTree


func _init() -> void:
	print("route1_party_panel_test")
	var save_state_script := load("res://src/save/SaveState.gd")
	var route_scene := load("res://scenes/world/Route1.tscn")

	if save_state_script == null or route_scene == null:
		push_error("Route 1 party panel resources did not load.")
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
	route._toggle_party_panel()

	if route.party_panel == null:
		push_error("Route 1 party panel did not open.")
		quit(1)
		return
	if not route.party_panel.visible:
		push_error("Route 1 party panel should be visible after toggle.")
		quit(1)
		return

	var text: String = route.party_panel.get_summary_text()
	if not text.contains("Party Status"):
		push_error("Party panel summary missing title.")
		quit(1)
		return
	if not text.contains("Bulbasaur") or not text.contains("Rattata"):
		push_error("Party panel did not show starter and caught Rattata.")
		quit(1)
		return
	if not text.contains("Captured: Rattata"):
		push_error("Party panel did not show captured creatures.")
		quit(1)
		return

	route._toggle_party_panel()
	if route.party_panel.visible:
		push_error("Route 1 party panel did not hide on second toggle.")
		quit(1)
		return

	route.free()
	print("Native Route 1 party panel smoke test passed.")
	quit(0)
