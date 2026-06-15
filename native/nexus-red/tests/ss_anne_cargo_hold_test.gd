extends SceneTree


func _init() -> void:
	print("ss_anne_cargo_hold_test")
	var save_state_script := load("res://src/save/SaveState.gd")
	var deck_scene := load("res://scenes/world/SSAnneMainDeck.tscn")
	var cargo_scene := load("res://scenes/world/SSAnneCargoHold.tscn")

	if save_state_script == null or deck_scene == null or cargo_scene == null:
		push_error("S.S. Anne cargo hold resources did not load.")
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
	save_state.enter_ss_anne_main_deck()

	var deck = deck_scene.instantiate()
	deck.save_state = save_state
	root.add_child(deck)
	deck._ready()

	var cargo_seen := [false]
	deck.go_to_ss_anne_cargo_hold.connect(func() -> void:
		cargo_seen[0] = true
	)

	deck.trigger_cargo_hold_entry()
	if cargo_seen[0]:
		push_error("Cargo hold should stay locked before Blue's S.S. Anne battle is complete.")
		quit(1)
		return
	if deck.dialogue_label == null or not deck.dialogue_label.text.contains("Blue"):
		push_error("Locked cargo hold did not point back to Blue's ship battle.")
		quit(1)
		return

	save_state.set_flag("blue_ss_anne_battle_finished", true)
	save_state.set_flag("blue_ss_anne_rival_respect_seen", true)
	deck.trigger_cargo_hold_entry()
	if not cargo_seen[0]:
		push_error("Main deck did not emit cargo hold transition after Blue battle.")
		quit(1)
		return

	var cargo = cargo_scene.instantiate()
	cargo.save_state = save_state
	root.add_child(cargo)
	cargo._ready()
	if save_state.current_scene != "ss_anne_cargo_hold":
		push_error("Cargo hold did not update current scene.")
		quit(1)
		return
	if not save_state.story_flags.get("ss_anne_cargo_hold_reached", false):
		push_error("Cargo hold reached flag missing.")
		quit(1)
		return
	if not save_state.worldlink_queue.has("wl_ss_anne_cargo_hold_reached"):
		push_error("WorldLink queue missing cargo hold arrival.")
		quit(1)
		return

	cargo.trigger_cargo_hold_investigation()
	for flag_name in [
		"rocket_cargo_manifest_recovered",
		"nexus_order_crate_symbol_seen",
		"bill_cargo_decode_seen",
		"misty_lower_deck_waterline_seen",
		"red_cargo_hold_guard_seen",
		"ss_anne_captain_path_unlocked",
	]:
		if not save_state.story_flags.get(flag_name, false):
			push_error("Cargo hold flag missing: " + flag_name)
			quit(1)
			return
	for queue_id in [
		"wl_rocket_cargo_manifest_recovered",
		"wl_nexus_order_crate_symbol_seen",
		"wl_bill_cargo_decode_seen",
		"wl_ss_anne_captain_path_unlocked",
	]:
		if not save_state.worldlink_queue.has(queue_id):
			push_error("WorldLink missing cargo hold id: " + queue_id)
			quit(1)
			return
	for required_text in ["Red", "Misty", "Bill", "Rocket", "Nexus Order", "Captain"]:
		if cargo.dialogue_label == null or not cargo.dialogue_label.text.contains(required_text):
			push_error("Cargo hold dialogue missing: " + required_text)
			quit(1)
			return

	var returned := [false]
	cargo.go_to_ss_anne_main_deck.connect(func() -> void:
		returned[0] = true
	)
	cargo.return_to_main_deck()
	if not returned[0]:
		push_error("Cargo hold did not emit return to main deck.")
		quit(1)
		return

	cargo.free()
	deck.free()
	print("Native S.S. Anne cargo hold smoke test passed.")
	quit(0)
