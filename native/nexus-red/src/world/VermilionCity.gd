extends Control

signal go_to_route_5_underground_path

var save_state
var dialogue_label: Label


func _ready() -> void:
	_build_city()
	if save_state:
		save_state.enter_vermilion_city()
	_update_intro_dialogue()


func _unhandled_input(event: InputEvent) -> void:
	if event.is_action_pressed("confirm"):
		trigger_vermilion_arrival_scene()
	if event.is_action_pressed("cancel"):
		return_to_route_5_underground_path()


func _build_city() -> void:
	var ground := ColorRect.new()
	ground.color = Color("d4b05f")
	ground.set_anchors_preset(Control.PRESET_FULL_RECT)
	add_child(ground)

	var water := ColorRect.new()
	water.color = Color("3f9fd4")
	water.anchor_left = 0.02
	water.anchor_top = 0.62
	water.anchor_right = 0.96
	water.anchor_bottom = 0.94
	add_child(water)

	var harbor := ColorRect.new()
	harbor.color = Color("7c6650")
	harbor.anchor_left = 0.18
	harbor.anchor_top = 0.52
	harbor.anchor_right = 0.74
	harbor.anchor_bottom = 0.66
	add_child(harbor)

	var center := ColorRect.new()
	center.color = Color("d94d4d")
	center.anchor_left = 0.12
	center.anchor_top = 0.18
	center.anchor_right = 0.32
	center.anchor_bottom = 0.34
	add_child(center)

	var mart := ColorRect.new()
	mart.color = Color("4d76d9")
	mart.anchor_left = 0.36
	mart.anchor_top = 0.18
	mart.anchor_right = 0.56
	mart.anchor_bottom = 0.34
	add_child(mart)

	var gym := ColorRect.new()
	gym.color = Color("dfc74d")
	gym.anchor_left = 0.68
	gym.anchor_top = 0.16
	gym.anchor_right = 0.9
	gym.anchor_bottom = 0.36
	add_child(gym)

	var header := Label.new()
	header.text = "Vermilion City"
	header.anchor_left = 0.04
	header.anchor_top = 0.04
	header.anchor_right = 0.6
	header.anchor_bottom = 0.1
	header.add_theme_font_size_override("font_size", 32)
	header.add_theme_color_override("font_color", Color("392b13"))
	add_child(header)

	var harbor_label := Label.new()
	harbor_label.text = "Harbor / S.S. Anne"
	harbor_label.anchor_left = 0.26
	harbor_label.anchor_top = 0.56
	harbor_label.anchor_right = 0.7
	harbor_label.anchor_bottom = 0.62
	harbor_label.add_theme_font_size_override("font_size", 18)
	harbor_label.add_theme_color_override("font_color", Color("fff1d5"))
	add_child(harbor_label)

	var gym_label := Label.new()
	gym_label.text = "Lt. Surge"
	gym_label.anchor_left = 0.72
	gym_label.anchor_top = 0.24
	gym_label.anchor_right = 0.88
	gym_label.anchor_bottom = 0.3
	gym_label.add_theme_font_size_override("font_size", 18)
	gym_label.add_theme_color_override("font_color", Color("392b13"))
	add_child(gym_label)

	dialogue_label = Label.new()
	dialogue_label.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	dialogue_label.anchor_left = 0.06
	dialogue_label.anchor_top = 0.74
	dialogue_label.anchor_right = 0.94
	dialogue_label.anchor_bottom = 0.95
	dialogue_label.add_theme_font_size_override("font_size", 20)
	dialogue_label.add_theme_color_override("font_color", Color("392b13"))
	add_child(dialogue_label)


func trigger_vermilion_arrival_scene() -> void:
	if save_state:
		save_state.record_vermilion_arrival_scene()
	dialogue_label.text = "Red: Vermilion is busier than Cerulean. Misty is checking the harbor, Bill is chasing an S.S. Anne ticket lead, and Surge's gym power is flickering like Rocket touched the wiring."


func return_to_route_5_underground_path() -> void:
	emit_signal("go_to_route_5_underground_path")


func _update_intro_dialogue() -> void:
	dialogue_label.text = "Red: Vermilion City. The harbor, S.S. Anne, and Lt. Surge all matter here. Press Z/Enter to scout with Red, Misty, and Bill, or X/Esc to return to Route 5."
