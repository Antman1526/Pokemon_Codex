extends SceneTree


func _init() -> void:
	print("ss_anne_blue_battle_test")
	var save_state_script := load("res://src/save/SaveState.gd")
	var deck_scene := load("res://scenes/world/SSAnneMainDeck.tscn")
	var battle_scene := load("res://scenes/battle/BattlePlaceholder.tscn")

	if save_state_script == null or deck_scene == null or battle_scene == null:
		push_error("S.S. Anne Blue battle resources did not load.")
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

	var battle_seen := [false]
	deck.start_battle_placeholder.connect(func(battle_id: String) -> void:
		battle_seen[0] = true
		if battle_id != "blue_ss_anne":
			push_error("S.S. Anne deck emitted the wrong battle id.")
			quit(1)
	)

	deck.trigger_blue_ship_battle()
	if battle_seen[0]:
		push_error("Blue ship battle should stay locked before deck scouting.")
		quit(1)
		return
	if deck.dialogue_label == null or not deck.dialogue_label.text.contains("main deck"):
		push_error("Locked Blue ship battle did not point back to main deck scouting.")
		quit(1)
		return

	save_state.set_flag("blue_ship_rival_teased", true)
	deck.trigger_blue_ship_battle()
	if not battle_seen[0]:
		push_error("S.S. Anne deck did not emit Blue ship battle after scouting.")
		quit(1)
		return
	if not save_state.story_flags.get("blue_ss_anne_battle_started", false):
		push_error("Blue S.S. Anne battle started flag missing after trigger.")
		quit(1)
		return

	save_state.start_battle_placeholder("blue_ss_anne")
	var battle = battle_scene.instantiate()
	battle.save_state = save_state
	battle.battle_id = "blue_ss_anne"
	root.add_child(battle)
	battle._ready()
	if battle.battle_data.get("opponent", {}).get("display_name", "") != "Blue":
		push_error("Blue S.S. Anne battle data did not load.")
		quit(1)
		return
	if battle.dialogue_label == null or not battle.dialogue_label.text.contains("Blue"):
		push_error("Blue S.S. Anne battle did not render Blue dialogue.")
		quit(1)
		return
	if not battle.dialogue_label.text.contains("placeholder"):
		push_error("Blue S.S. Anne battle should remain a placeholder battle engine slice.")
		quit(1)
		return
	var opponent_summary: String = battle._opponent_summary()
	if not opponent_summary.contains("Charmander"):
		push_error("Blue S.S. Anne battle did not include Blue's dynamic starter.")
		quit(1)
		return

	battle.finish_placeholder_battle()
	save_state.finish_battle_placeholder("placeholder_win")
	if not save_state.story_flags.get("blue_ss_anne_battle_finished", false):
		push_error("Blue S.S. Anne battle finished flag missing.")
		quit(1)
		return
	if not save_state.story_flags.get("blue_ss_anne_rival_respect_seen", false):
		push_error("Blue S.S. Anne respect flag missing.")
		quit(1)
		return
	for queue_id in ["wl_blue_ss_anne_battle_finished", "wl_blue_ss_anne_rival_respect"]:
		if not save_state.worldlink_queue.has(queue_id):
			push_error("WorldLink missing Blue S.S. Anne id: " + queue_id)
			quit(1)
			return

	battle.free()
	deck.free()
	print("Native S.S. Anne Blue battle smoke test passed.")
	quit(0)
