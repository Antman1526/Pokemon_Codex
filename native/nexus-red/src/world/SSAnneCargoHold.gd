extends Control

signal go_to_ss_anne_main_deck
signal go_to_ss_anne_captain_cabin

var save_state
var dialogue_label: Label


func _ready() -> void:
	_build_cargo_hold()
	if save_state:
		save_state.enter_ss_anne_cargo_hold()
	_update_intro_dialogue()


func _unhandled_input(event: InputEvent) -> void:
	if event.is_action_pressed("confirm"):
		trigger_cargo_hold_investigation()
	if event.is_action_pressed("ui_right"):
		trigger_captain_cabin_entry()
	if event.is_action_pressed("cancel"):
		return_to_main_deck()


func _build_cargo_hold() -> void:
	var floor := ColorRect.new()
	floor.color = Color("4b463e")
	floor.set_anchors_preset(Control.PRESET_FULL_RECT)
	add_child(floor)

	var crates := ColorRect.new()
	crates.color = Color("8b5d36")
	crates.anchor_left = 0.1
	crates.anchor_top = 0.18
	crates.anchor_right = 0.46
	crates.anchor_bottom = 0.52
	add_child(crates)

	var marked_crate := ColorRect.new()
	marked_crate.color = Color("30394d")
	marked_crate.anchor_left = 0.56
	marked_crate.anchor_top = 0.22
	marked_crate.anchor_right = 0.82
	marked_crate.anchor_bottom = 0.44
	add_child(marked_crate)

	var waterline := ColorRect.new()
	waterline.color = Color("285f75")
	waterline.anchor_left = 0.04
	waterline.anchor_top = 0.6
	waterline.anchor_right = 0.96
	waterline.anchor_bottom = 0.68
	add_child(waterline)

	var header := Label.new()
	header.text = "S.S. Anne Cargo Hold"
	header.anchor_left = 0.04
	header.anchor_top = 0.04
	header.anchor_right = 0.8
	header.anchor_bottom = 0.1
	header.add_theme_font_size_override("font_size", 32)
	header.add_theme_color_override("font_color", Color("f4ead5"))
	add_child(header)

	var crate_label := Label.new()
	crate_label.text = "Rocket crates"
	crate_label.anchor_left = 0.18
	crate_label.anchor_top = 0.32
	crate_label.anchor_right = 0.42
	crate_label.anchor_bottom = 0.38
	crate_label.add_theme_font_size_override("font_size", 18)
	crate_label.add_theme_color_override("font_color", Color("fff1d5"))
	add_child(crate_label)

	var symbol_label := Label.new()
	symbol_label.text = "Nexus Order mark"
	symbol_label.anchor_left = 0.58
	symbol_label.anchor_top = 0.3
	symbol_label.anchor_right = 0.82
	symbol_label.anchor_bottom = 0.36
	symbol_label.add_theme_font_size_override("font_size", 16)
	symbol_label.add_theme_color_override("font_color", Color("fff1d5"))
	add_child(symbol_label)

	dialogue_label = Label.new()
	dialogue_label.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	dialogue_label.anchor_left = 0.06
	dialogue_label.anchor_top = 0.72
	dialogue_label.anchor_right = 0.94
	dialogue_label.anchor_bottom = 0.95
	dialogue_label.add_theme_font_size_override("font_size", 20)
	dialogue_label.add_theme_color_override("font_color", Color("f4ead5"))
	add_child(dialogue_label)


func trigger_cargo_hold_investigation() -> void:
	if save_state:
		save_state.record_ss_anne_cargo_hold_investigation()
	dialogue_label.text = "Red: Rocket hid a cargo manifest down here. Misty says the lower-deck waterline is wrong, and Bill found a Nexus Order symbol burned into one crate. This points us toward the Captain before Rocket can move the shipment."


func trigger_captain_cabin_entry() -> void:
	if save_state == null or not bool(save_state.story_flags.get("ss_anne_captain_path_unlocked", false)):
		dialogue_label.text = "Red: The Captain Cabin is still guarded. We need the cargo manifest and Bill's crate decode before we can prove why the Trail Cutter is in danger."
		return
	emit_signal("go_to_ss_anne_captain_cabin")


func return_to_main_deck() -> void:
	emit_signal("go_to_ss_anne_main_deck")


func _update_intro_dialogue() -> void:
	dialogue_label.text = "Red: This is the S.S. Anne Cargo Hold. Press Z/Enter to investigate Rocket crates with Misty and Bill, Right to approach the Captain Cabin, or X/Esc to return to the main deck."
