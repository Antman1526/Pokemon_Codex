extends Control

signal go_to_route_3

var save_state
var dialogue_label: Label


func _ready() -> void:
	_build_city()
	if save_state:
		save_state.enter_pewter_city()
	_update_intro_dialogue()


func _unhandled_input(event: InputEvent) -> void:
	if event.is_action_pressed("confirm"):
		trigger_brock_intro()
	if event.is_action_pressed("ui_down"):
		trigger_red_training()
	if event.is_action_pressed("cancel"):
		return_to_route_3()


func _build_city() -> void:
	var ground := ColorRect.new()
	ground.color = Color("b5ad95")
	ground.set_anchors_preset(Control.PRESET_FULL_RECT)
	add_child(ground)

	var road := ColorRect.new()
	road.color = Color("d2c497")
	road.anchor_left = 0.0
	road.anchor_top = 0.48
	road.anchor_right = 1.0
	road.anchor_bottom = 0.64
	add_child(road)

	var gym := ColorRect.new()
	gym.color = Color("7d6f5b")
	gym.anchor_left = 0.58
	gym.anchor_top = 0.16
	gym.anchor_right = 0.9
	gym.anchor_bottom = 0.4
	add_child(gym)

	var museum := ColorRect.new()
	museum.color = Color("9aa8b1")
	museum.anchor_left = 0.08
	museum.anchor_top = 0.16
	museum.anchor_right = 0.38
	museum.anchor_bottom = 0.38
	add_child(museum)

	var header := Label.new()
	header.text = "Pewter City"
	header.anchor_left = 0.04
	header.anchor_top = 0.04
	header.anchor_right = 0.42
	header.anchor_bottom = 0.1
	header.add_theme_font_size_override("font_size", 32)
	header.add_theme_color_override("font_color", Color("14243d"))
	add_child(header)

	var gym_label := Label.new()
	gym_label.text = "Pewter Gym"
	gym_label.anchor_left = 0.63
	gym_label.anchor_top = 0.25
	gym_label.anchor_right = 0.86
	gym_label.anchor_bottom = 0.32
	gym_label.add_theme_font_size_override("font_size", 22)
	gym_label.add_theme_color_override("font_color", Color("fff2c7"))
	add_child(gym_label)

	var museum_label := Label.new()
	museum_label.text = "Museum"
	museum_label.anchor_left = 0.17
	museum_label.anchor_top = 0.25
	museum_label.anchor_right = 0.32
	museum_label.anchor_bottom = 0.32
	museum_label.add_theme_font_size_override("font_size", 22)
	museum_label.add_theme_color_override("font_color", Color("14243d"))
	add_child(museum_label)

	dialogue_label = Label.new()
	dialogue_label.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	dialogue_label.anchor_left = 0.06
	dialogue_label.anchor_top = 0.78
	dialogue_label.anchor_right = 0.94
	dialogue_label.anchor_bottom = 0.95
	dialogue_label.add_theme_font_size_override("font_size", 20)
	dialogue_label.add_theme_color_override("font_color", Color("14243d"))
	add_child(dialogue_label)


func trigger_brock_intro() -> void:
	if save_state:
		save_state.record_brock_pewter_intro()
	dialogue_label.text = "Brock: I heard you came through Viridian Forest with Red. Good. I want challengers who learn from the road, not just from type charts."


func trigger_red_training() -> void:
	if save_state:
		save_state.record_red_pewter_training()
	dialogue_label.text = "Red: Brock is friendly, not soft. Check your levels, bring answers for Rock-types, and do not let the expanded starter pool make you careless."


func return_to_route_3() -> void:
	emit_signal("go_to_route_3")


func _update_intro_dialogue() -> void:
	dialogue_label.text = "Pewter City opens around the gym and museum. Press Z/Enter for Brock, Down for Red's training advice, or X/Esc to return to Route 3."
