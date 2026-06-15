extends Control

signal go_to_ss_anne_cargo_hold

var save_state
var dialogue_label: Label


func _ready() -> void:
	_build_captain_cabin()
	if save_state:
		save_state.enter_ss_anne_captain_cabin()
	_update_intro_dialogue()


func _unhandled_input(event: InputEvent) -> void:
	if event.is_action_pressed("confirm"):
		trigger_captain_cabin_scene()
	if event.is_action_pressed("cancel"):
		return_to_cargo_hold()


func _build_captain_cabin() -> void:
	var floor := ColorRect.new()
	floor.color = Color("3d4c5c")
	floor.set_anchors_preset(Control.PRESET_FULL_RECT)
	add_child(floor)

	var desk := ColorRect.new()
	desk.color = Color("785032")
	desk.anchor_left = 0.12
	desk.anchor_top = 0.2
	desk.anchor_right = 0.46
	desk.anchor_bottom = 0.42
	add_child(desk)

	var bed := ColorRect.new()
	bed.color = Color("c9d7df")
	bed.anchor_left = 0.58
	bed.anchor_top = 0.18
	bed.anchor_right = 0.86
	bed.anchor_bottom = 0.5
	add_child(bed)

	var cutter_case := ColorRect.new()
	cutter_case.color = Color("d5b24c")
	cutter_case.anchor_left = 0.2
	cutter_case.anchor_top = 0.5
	cutter_case.anchor_right = 0.42
	cutter_case.anchor_bottom = 0.62
	add_child(cutter_case)

	var header := Label.new()
	header.text = "S.S. Anne Captain Cabin"
	header.anchor_left = 0.04
	header.anchor_top = 0.04
	header.anchor_right = 0.9
	header.anchor_bottom = 0.1
	header.add_theme_font_size_override("font_size", 32)
	header.add_theme_color_override("font_color", Color("f4ead5"))
	add_child(header)

	var bed_label := Label.new()
	bed_label.text = "Captain"
	bed_label.anchor_left = 0.64
	bed_label.anchor_top = 0.3
	bed_label.anchor_right = 0.82
	bed_label.anchor_bottom = 0.36
	bed_label.add_theme_font_size_override("font_size", 18)
	bed_label.add_theme_color_override("font_color", Color("26313c"))
	add_child(bed_label)

	var cutter_label := Label.new()
	cutter_label.text = "Trail Cutter"
	cutter_label.anchor_left = 0.23
	cutter_label.anchor_top = 0.535
	cutter_label.anchor_right = 0.42
	cutter_label.anchor_bottom = 0.59
	cutter_label.add_theme_font_size_override("font_size", 16)
	cutter_label.add_theme_color_override("font_color", Color("3a2a16"))
	add_child(cutter_label)

	dialogue_label = Label.new()
	dialogue_label.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	dialogue_label.anchor_left = 0.06
	dialogue_label.anchor_top = 0.72
	dialogue_label.anchor_right = 0.94
	dialogue_label.anchor_bottom = 0.95
	dialogue_label.add_theme_font_size_override("font_size", 20)
	dialogue_label.add_theme_color_override("font_color", Color("f4ead5"))
	add_child(dialogue_label)


func trigger_captain_cabin_scene() -> void:
	if save_state:
		save_state.record_ss_anne_captain_cabin_scene()
	dialogue_label.text = "Captain: Red, Misty, Bill, and Antman pulled Rocket's manifest out of my own cargo hold? Then take the Trail Cutter. It replaces Cut in the field, opens Lt. Surge's gym route, and keeps your team free for real battles."


func return_to_cargo_hold() -> void:
	emit_signal("go_to_ss_anne_cargo_hold")


func _update_intro_dialogue() -> void:
	dialogue_label.text = "Red: This is the Captain's cabin. Press Z/Enter to help the Captain, secure the Trail Cutter, and open the path toward Surge, or X/Esc to return to the cargo hold."
