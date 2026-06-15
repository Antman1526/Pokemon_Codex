extends Control

signal go_to_ss_anne_ticket_office
signal go_to_ss_anne_cargo_hold
signal start_battle_placeholder(battle_id)

var save_state
var dialogue_label: Label


func _ready() -> void:
	_build_main_deck()
	if save_state:
		save_state.enter_ss_anne_main_deck()
	_update_intro_dialogue()


func _unhandled_input(event: InputEvent) -> void:
	if event.is_action_pressed("confirm"):
		trigger_deck_boarding_scene()
	if event.is_action_pressed("ui_right"):
		trigger_blue_ship_battle()
	if event.is_action_pressed("ui_down"):
		trigger_cargo_hold_entry()
	if event.is_action_pressed("cancel"):
		return_to_ticket_office()


func _build_main_deck() -> void:
	var deck := ColorRect.new()
	deck.color = Color("c9955e")
	deck.set_anchors_preset(Control.PRESET_FULL_RECT)
	add_child(deck)

	var ocean := ColorRect.new()
	ocean.color = Color("3f9fd4")
	ocean.anchor_left = 0.02
	ocean.anchor_top = 0.62
	ocean.anchor_right = 0.98
	ocean.anchor_bottom = 0.96
	add_child(ocean)

	var ship_cabin := ColorRect.new()
	ship_cabin.color = Color("e5e2c9")
	ship_cabin.anchor_left = 0.18
	ship_cabin.anchor_top = 0.16
	ship_cabin.anchor_right = 0.74
	ship_cabin.anchor_bottom = 0.42
	add_child(ship_cabin)

	var cargo_hatch := ColorRect.new()
	cargo_hatch.color = Color("4d4b4a")
	cargo_hatch.anchor_left = 0.72
	cargo_hatch.anchor_top = 0.46
	cargo_hatch.anchor_right = 0.9
	cargo_hatch.anchor_bottom = 0.58
	add_child(cargo_hatch)

	var gangway := ColorRect.new()
	gangway.color = Color("7a4d35")
	gangway.anchor_left = 0.04
	gangway.anchor_top = 0.48
	gangway.anchor_right = 0.28
	gangway.anchor_bottom = 0.58
	add_child(gangway)

	var header := Label.new()
	header.text = "S.S. Anne Main Deck"
	header.anchor_left = 0.04
	header.anchor_top = 0.04
	header.anchor_right = 0.8
	header.anchor_bottom = 0.1
	header.add_theme_font_size_override("font_size", 32)
	header.add_theme_color_override("font_color", Color("2d2118"))
	add_child(header)

	var cabin_label := Label.new()
	cabin_label.text = "Cabins / Captain"
	cabin_label.anchor_left = 0.32
	cabin_label.anchor_top = 0.27
	cabin_label.anchor_right = 0.66
	cabin_label.anchor_bottom = 0.33
	cabin_label.add_theme_font_size_override("font_size", 18)
	cabin_label.add_theme_color_override("font_color", Color("2d2118"))
	add_child(cabin_label)

	var cargo_label := Label.new()
	cargo_label.text = "Cargo Hold"
	cargo_label.anchor_left = 0.75
	cargo_label.anchor_top = 0.49
	cargo_label.anchor_right = 0.9
	cargo_label.anchor_bottom = 0.55
	cargo_label.add_theme_font_size_override("font_size", 16)
	cargo_label.add_theme_color_override("font_color", Color("fff1d5"))
	add_child(cargo_label)

	dialogue_label = Label.new()
	dialogue_label.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	dialogue_label.anchor_left = 0.06
	dialogue_label.anchor_top = 0.72
	dialogue_label.anchor_right = 0.94
	dialogue_label.anchor_bottom = 0.95
	dialogue_label.add_theme_font_size_override("font_size", 20)
	dialogue_label.add_theme_color_override("font_color", Color("2d2118"))
	add_child(dialogue_label)


func trigger_deck_boarding_scene() -> void:
	if save_state:
		save_state.record_ss_anne_deck_boarding_scene()
	dialogue_label.text = "Red: We made it onto the S.S. Anne. Misty says the tide feels wrong, Bill found Rocket cargo edits below deck, and Blue is already aboard looking for a battle. The Captain may have the Trail Cutter prototype."


func trigger_blue_ship_battle() -> void:
	if save_state and not bool(save_state.story_flags.get("blue_ship_rival_teased", false)):
		dialogue_label.text = "Red: Scout the main deck first. Blue is aboard, but we need to know where the passengers and Rocket watchers are standing."
		return
	if save_state:
		save_state.start_battle_placeholder("blue_ss_anne")
	dialogue_label.text = "Blue: Took you long enough to board. I heard Rocket is sniffing around cargo, but first I want to see if you can still keep up."
	emit_signal("start_battle_placeholder", "blue_ss_anne")


func trigger_cargo_hold_entry() -> void:
	if save_state and not bool(save_state.story_flags.get("blue_ss_anne_battle_finished", false)):
		dialogue_label.text = "Red: Handle Blue first. He saw Rocket cargo movement, and he will not stop blocking the main deck until Antman answers him."
		return
	emit_signal("go_to_ss_anne_cargo_hold")


func return_to_ticket_office() -> void:
	emit_signal("go_to_ss_anne_ticket_office")


func _update_intro_dialogue() -> void:
	dialogue_label.text = "Red: Stay sharp on the S.S. Anne Main Deck. Press Z/Enter to scout with Red, Misty, and Bill, Right to answer Blue's challenge, Down for the Cargo Hold, or X/Esc to return to the ticket office."
