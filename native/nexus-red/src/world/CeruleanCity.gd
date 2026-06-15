extends Control

signal go_to_route_4_cerulean_approach

var save_state
var dialogue_label: Label


func _ready() -> void:
	_build_city()
	if save_state:
		save_state.enter_cerulean_city()
	_update_intro_dialogue()


func _unhandled_input(event: InputEvent) -> void:
	if event.is_action_pressed("confirm"):
		trigger_misty_intro()
	if event.is_action_pressed("cancel"):
		return_to_route_4_cerulean_approach()


func _build_city() -> void:
	var ground := ColorRect.new()
	ground.color = Color("6bb6c9")
	ground.set_anchors_preset(Control.PRESET_FULL_RECT)
	add_child(ground)

	var plaza := ColorRect.new()
	plaza.color = Color("d8c487")
	plaza.anchor_left = 0.18
	plaza.anchor_top = 0.38
	plaza.anchor_right = 0.78
	plaza.anchor_bottom = 0.66
	add_child(plaza)

	var gym := ColorRect.new()
	gym.color = Color("2b6fae")
	gym.anchor_left = 0.58
	gym.anchor_top = 0.16
	gym.anchor_right = 0.88
	gym.anchor_bottom = 0.36
	add_child(gym)

	var bridge := ColorRect.new()
	bridge.color = Color("8f7655")
	bridge.anchor_left = 0.34
	bridge.anchor_top = 0.02
	bridge.anchor_right = 0.47
	bridge.anchor_bottom = 0.38
	add_child(bridge)

	var center := ColorRect.new()
	center.color = Color("d94d4d")
	center.anchor_left = 0.12
	center.anchor_top = 0.14
	center.anchor_right = 0.34
	center.anchor_bottom = 0.32
	add_child(center)

	var header := Label.new()
	header.text = "Cerulean City"
	header.anchor_left = 0.04
	header.anchor_top = 0.04
	header.anchor_right = 0.54
	header.anchor_bottom = 0.1
	header.add_theme_font_size_override("font_size", 32)
	header.add_theme_color_override("font_color", Color("102841"))
	add_child(header)

	var bridge_label := Label.new()
	bridge_label.text = "Nugget Bridge"
	bridge_label.anchor_left = 0.3
	bridge_label.anchor_top = 0.22
	bridge_label.anchor_right = 0.54
	bridge_label.anchor_bottom = 0.28
	bridge_label.add_theme_font_size_override("font_size", 18)
	bridge_label.add_theme_color_override("font_color", Color("102841"))
	add_child(bridge_label)

	var gym_label := Label.new()
	gym_label.text = "Misty's Gym"
	gym_label.anchor_left = 0.62
	gym_label.anchor_top = 0.22
	gym_label.anchor_right = 0.84
	gym_label.anchor_bottom = 0.28
	gym_label.add_theme_font_size_override("font_size", 18)
	gym_label.add_theme_color_override("font_color", Color("e8f8ff"))
	add_child(gym_label)

	dialogue_label = Label.new()
	dialogue_label.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	dialogue_label.anchor_left = 0.06
	dialogue_label.anchor_top = 0.76
	dialogue_label.anchor_right = 0.94
	dialogue_label.anchor_bottom = 0.95
	dialogue_label.add_theme_font_size_override("font_size", 20)
	dialogue_label.add_theme_color_override("font_color", Color("102841"))
	add_child(dialogue_label)


func trigger_misty_intro() -> void:
	if save_state:
		save_state.record_misty_cerulean_intro()
	dialogue_label.text = "Misty: Red, Antman, you dragged Rocket and Gold Dust right to my city? Fine. Nugget Bridge first. If they are recruiting up there, my gym waits until Cerulean is safe."


func return_to_route_4_cerulean_approach() -> void:
	emit_signal("go_to_route_4_cerulean_approach")


func _update_intro_dialogue() -> void:
	dialogue_label.text = "Red: Cerulean City. Misty is near the gym, but Nugget Bridge is already crowded. Press Z/Enter to meet Misty, or X/Esc to step back to Route 4."
