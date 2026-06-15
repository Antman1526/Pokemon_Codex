extends SceneTree


func _init() -> void:
	print("ss_anne_boarding_test")
	var save_state_script := load("res://src/save/SaveState.gd")
	var ticket_scene := load("res://scenes/world/SSAnneTicketOffice.tscn")
	var deck_scene := load("res://scenes/world/SSAnneMainDeck.tscn")

	if save_state_script == null or ticket_scene == null or deck_scene == null:
		push_error("S.S. Anne boarding resources did not load.")
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
	save_state.enter_ss_anne_ticket_office()

	var ticket = ticket_scene.instantiate()
	ticket.save_state = save_state
	root.add_child(ticket)
	ticket._ready()

	var boarding_seen := [false]
	ticket.go_to_ss_anne_main_deck.connect(func() -> void:
		boarding_seen[0] = true
	)

	ticket.trigger_ss_anne_boarding()
	if boarding_seen[0]:
		push_error("S.S. Anne boarding should stay locked before the boarding pass is earned.")
		quit(1)
		return
	if ticket.dialogue_label == null or not ticket.dialogue_label.text.contains("boarding pass"):
		push_error("Locked S.S. Anne boarding did not point back to the boarding pass.")
		quit(1)
		return

	save_state.set_flag("ss_anne_boarding_pass_earned", true)
	ticket.trigger_ss_anne_boarding()
	if not boarding_seen[0]:
		push_error("Ticket office did not emit S.S. Anne boarding after boarding pass.")
		quit(1)
		return

	var deck = deck_scene.instantiate()
	deck.save_state = save_state
	root.add_child(deck)
	deck._ready()
	if save_state.current_scene != "ss_anne_main_deck":
		push_error("S.S. Anne deck did not update current scene.")
		quit(1)
		return
	if not save_state.story_flags.get("ss_anne_main_deck_reached", false):
		push_error("S.S. Anne main deck reached flag missing.")
		quit(1)
		return
	if not save_state.worldlink_queue.has("wl_ss_anne_boarded"):
		push_error("WorldLink queue missing S.S. Anne boarded update.")
		quit(1)
		return

	deck.trigger_deck_boarding_scene()
	for flag_name in [
		"ss_anne_boarded",
		"red_ss_anne_boarding_scene_seen",
		"blue_ship_rival_teased",
		"rocket_cargo_hold_clue_seen",
		"captain_trail_cutter_lead_seen",
	]:
		if not save_state.story_flags.get(flag_name, false):
			push_error("S.S. Anne deck flag missing: " + flag_name)
			quit(1)
			return
	for queue_id in [
		"wl_red_ss_anne_boarding_scene",
		"wl_blue_ship_rival_tease",
		"wl_rocket_cargo_hold_clue",
		"wl_captain_trail_cutter_lead",
	]:
		if not save_state.worldlink_queue.has(queue_id):
			push_error("WorldLink queue missing S.S. Anne deck id: " + queue_id)
			quit(1)
			return
	for required_text in ["Red", "Misty", "Bill", "Blue", "Rocket", "cargo", "Trail Cutter"]:
		if deck.dialogue_label == null or not deck.dialogue_label.text.contains(required_text):
			push_error("S.S. Anne deck dialogue missing: " + required_text)
			quit(1)
			return

	var returned := [false]
	deck.go_to_ss_anne_ticket_office.connect(func() -> void:
		returned[0] = true
	)
	deck.return_to_ticket_office()
	if not returned[0]:
		push_error("S.S. Anne deck did not emit return to ticket office.")
		quit(1)
		return

	deck.free()
	ticket.free()
	print("Native S.S. Anne boarding smoke test passed.")
	quit(0)
