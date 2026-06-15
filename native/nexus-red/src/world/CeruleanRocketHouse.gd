extends Control

signal go_to_cerulean_city
signal start_battle_placeholder(battle_id)

var save_state
var dialogue_label: Label


func _ready() -> void:
	_build_house()
	if save_state:
		save_state.enter_cerulean_rocket_house()
	_update_intro_dialogue()


func _unhandled_input(event: InputEvent) -> void:
	if event.is_action_pressed("confirm"):
		trigger_house_investigation()
	if event.is_action_pressed("ui_right"):
		trigger_rocket_thief_battle()
	if event.is_action_pressed("cancel"):
		return_to_cerulean_city()


func _build_house() -> void:
	var floor := ColorRect.new()
	floor.color = Color("d7bb86")
	floor.set_anchors_preset(Control.PRESET_FULL_RECT)
	add_child(floor)

	var broken_wall := ColorRect.new()
	broken_wall.color = Color("80624d")
	broken_wall.anchor_left = 0.68
	broken_wall.anchor_top = 0.12
	broken_wall.anchor_right = 0.9
	broken_wall.anchor_bottom = 0.42
	add_child(broken_wall)

	var rug := ColorRect.new()
	rug.color = Color("4f8fbd")
	rug.anchor_left = 0.18
	rug.anchor_top = 0.42
	rug.anchor_right = 0.54
	rug.anchor_bottom = 0.62
	add_child(rug)

	var table := ColorRect.new()
	table.color = Color("9a673d")
	table.anchor_left = 0.18
	table.anchor_top = 0.2
	table.anchor_right = 0.42
	table.anchor_bottom = 0.34
	add_child(table)

	var header := Label.new()
	header.text = "Cerulean Rocket House"
	header.anchor_left = 0.04
	header.anchor_top = 0.04
	header.anchor_right = 0.68
	header.anchor_bottom = 0.1
	header.add_theme_font_size_override("font_size", 32)
	header.add_theme_color_override("font_color", Color("2f241d"))
	add_child(header)

	var wall_label := Label.new()
	wall_label.text = "Broken wall"
	wall_label.anchor_left = 0.7
	wall_label.anchor_top = 0.24
	wall_label.anchor_right = 0.88
	wall_label.anchor_bottom = 0.3
	wall_label.add_theme_font_size_override("font_size", 18)
	wall_label.add_theme_color_override("font_color", Color("fff1d5"))
	add_child(wall_label)

	dialogue_label = Label.new()
	dialogue_label.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	dialogue_label.anchor_left = 0.06
	dialogue_label.anchor_top = 0.74
	dialogue_label.anchor_right = 0.94
	dialogue_label.anchor_bottom = 0.95
	dialogue_label.add_theme_font_size_override("font_size", 20)
	dialogue_label.add_theme_color_override("font_color", Color("2f241d"))
	add_child(dialogue_label)


func trigger_house_investigation() -> void:
	if save_state:
		save_state.record_cerulean_house_theft()
	dialogue_label.text = "Red: Rocket smashed through the wall and stole a TM. Misty is checking on the family, and Bill says the thief's notes mention Vermilion shipping routes."


func trigger_rocket_thief_battle() -> void:
	if save_state and not bool(save_state.story_flags.get("cerulean_house_theft_seen", false)):
		dialogue_label.text = "Red: Check the broken wall first. The thief left more than footprints."
		return
	if save_state:
		save_state.start_battle_placeholder("cerulean_rocket_house_thief")
	dialogue_label.text = "Rocket TM Thief: That TM is already sold south of Cerulean. You want it back? Battle me for it."
	emit_signal("start_battle_placeholder", "cerulean_rocket_house_thief")


func return_to_cerulean_city() -> void:
	emit_signal("go_to_cerulean_city")


func _update_intro_dialogue() -> void:
	dialogue_label.text = "Red: This is the burglarized Cerulean house. Press Z/Enter to inspect the theft, Right to confront the Rocket thief, or X/Esc to return to Cerulean."
