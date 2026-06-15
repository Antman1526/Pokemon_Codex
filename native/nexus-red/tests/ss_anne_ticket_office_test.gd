extends SceneTree


func _init() -> void:
	print("ss_anne_ticket_office_test")
	var save_state_script := load("res://src/save/SaveState.gd")
	var vermilion_scene := load("res://scenes/world/VermilionCity.tscn")
	var ticket_scene := load("res://scenes/world/SSAnneTicketOffice.tscn")

	if save_state_script == null or vermilion_scene == null or ticket_scene == null:
		push_error("S.S. Anne ticket office resources did not load.")
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
	save_state.enter_vermilion_city()

	var vermilion = vermilion_scene.instantiate()
	vermilion.save_state = save_state
	root.add_child(vermilion)
	vermilion._ready()

	var ticket_seen := [false]
	vermilion.go_to_ss_anne_ticket_office.connect(func() -> void:
		ticket_seen[0] = true
	)

	vermilion.trigger_ss_anne_ticket_office_entry()
	if ticket_seen[0]:
		push_error("S.S. Anne ticket office should stay locked before the harbor/ticket lead.")
		quit(1)
		return
	if vermilion.dialogue_label == null or not vermilion.dialogue_label.text.contains("harbor"):
		push_error("Locked S.S. Anne ticket entry did not point back to harbor scouting.")
		quit(1)
		return

	save_state.set_flag("vermilion_harbor_scouted", true)
	save_state.set_flag("ss_anne_ticket_lead_seen", true)
	vermilion.trigger_ss_anne_ticket_office_entry()
	if not ticket_seen[0]:
		push_error("Vermilion did not emit S.S. Anne ticket office transition after harbor scouting.")
		quit(1)
		return

	var ticket = ticket_scene.instantiate()
	ticket.save_state = save_state
	root.add_child(ticket)
	ticket._ready()
	if save_state.current_scene != "ss_anne_ticket_office":
		push_error("S.S. Anne ticket office did not update current scene.")
		quit(1)
		return
	if not save_state.story_flags.get("ss_anne_ticket_office_reached", false):
		push_error("S.S. Anne ticket office reached flag missing.")
		quit(1)
		return
	if not save_state.worldlink_queue.has("wl_ss_anne_ticket_office_reached"):
		push_error("WorldLink queue missing S.S. Anne ticket office arrival.")
		quit(1)
		return

	ticket.trigger_ticket_office_scene()
	for flag_name in [
		"ss_anne_manifest_checked",
		"bill_manifest_decode_seen",
		"red_harbor_guard_scene_seen",
		"ss_anne_boarding_pass_earned",
	]:
		if not save_state.story_flags.get(flag_name, false):
			push_error("S.S. Anne ticket office flag missing: " + flag_name)
			quit(1)
			return
	for queue_id in [
		"wl_ss_anne_manifest_checked",
		"wl_bill_manifest_decode_seen",
		"wl_red_harbor_guard_scene",
		"wl_ss_anne_boarding_pass_earned",
	]:
		if not save_state.worldlink_queue.has(queue_id):
			push_error("WorldLink queue missing S.S. Anne id: " + queue_id)
			quit(1)
			return
	for required_text in ["Red", "Misty", "Bill", "S.S. Anne", "Rocket", "boarding pass"]:
		if ticket.dialogue_label == null or not ticket.dialogue_label.text.contains(required_text):
			push_error("S.S. Anne ticket scene dialogue missing: " + required_text)
			quit(1)
			return

	var returned := [false]
	ticket.go_to_vermilion_city.connect(func() -> void:
		returned[0] = true
	)
	ticket.return_to_vermilion_city()
	if not returned[0]:
		push_error("S.S. Anne ticket office did not emit return to Vermilion City.")
		quit(1)
		return

	ticket.free()
	vermilion.free()
	print("Native S.S. Anne ticket office smoke test passed.")
	quit(0)
