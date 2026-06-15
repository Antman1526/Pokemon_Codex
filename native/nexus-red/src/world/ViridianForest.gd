extends Control

signal go_to_route_2_forest_gate
signal go_to_route_3

var save_state
var dialogue_label: Label


func _ready() -> void:
	_build_forest()
	if save_state:
		save_state.enter_viridian_forest()
	_update_intro_dialogue()


func _unhandled_input(event: InputEvent) -> void:
	if event.is_action_pressed("confirm"):
		trigger_rocket_scout_scene()
	if event.is_action_pressed("ui_up"):
		exit_to_route_3()
	if event.is_action_pressed("cancel"):
		return_to_route_2_forest_gate()


func _build_forest() -> void:
	var canopy := ColorRect.new()
	canopy.color = Color("1f5d3a")
	canopy.set_anchors_preset(Control.PRESET_FULL_RECT)
	add_child(canopy)

	var path := ColorRect.new()
	path.color = Color("8f7448")
	path.anchor_left = 0.42
	path.anchor_top = 0.0
	path.anchor_right = 0.58
	path.anchor_bottom = 1.0
	add_child(path)

	for i in range(8):
		var tree := ColorRect.new()
		tree.color = Color("123f2a")
		tree.position = Vector2(70 + (i % 4) * 280, 120 + int(i / 4) * 300)
		tree.size = Vector2(110, 130)
		add_child(tree)

	var clearing := ColorRect.new()
	clearing.color = Color("4f8f45")
	clearing.anchor_left = 0.28
	clearing.anchor_top = 0.38
	clearing.anchor_right = 0.72
	clearing.anchor_bottom = 0.62
	add_child(clearing)

	var rocket_marker := ColorRect.new()
	rocket_marker.color = Color("2a2a2a")
	rocket_marker.anchor_left = 0.62
	rocket_marker.anchor_top = 0.42
	rocket_marker.anchor_right = 0.66
	rocket_marker.anchor_bottom = 0.5
	add_child(rocket_marker)

	var red_marker := ColorRect.new()
	red_marker.color = Color("b92732")
	red_marker.anchor_left = 0.34
	red_marker.anchor_top = 0.48
	red_marker.anchor_right = 0.38
	red_marker.anchor_bottom = 0.56
	add_child(red_marker)

	var header := Label.new()
	header.text = "Viridian Forest"
	header.anchor_left = 0.04
	header.anchor_top = 0.04
	header.anchor_right = 0.46
	header.anchor_bottom = 0.1
	header.add_theme_font_size_override("font_size", 32)
	header.add_theme_color_override("font_color", Color("e8f4d8"))
	add_child(header)

	dialogue_label = Label.new()
	dialogue_label.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	dialogue_label.anchor_left = 0.06
	dialogue_label.anchor_top = 0.78
	dialogue_label.anchor_right = 0.94
	dialogue_label.anchor_bottom = 0.95
	dialogue_label.add_theme_font_size_override("font_size", 20)
	dialogue_label.add_theme_color_override("font_color", Color("eef6d8"))
	add_child(dialogue_label)


func trigger_rocket_scout_scene() -> void:
	if save_state:
		save_state.record_rocket_forest_scout()
	dialogue_label.text = "Rocket scout: The boss only asked for migration readings, not a fight. Red steps forward: Then you picked the wrong forest."


func exit_to_route_3() -> void:
	emit_signal("go_to_route_3")


func return_to_route_2_forest_gate() -> void:
	emit_signal("go_to_route_2_forest_gate")


func _update_intro_dialogue() -> void:
	dialogue_label.text = "Red: Viridian Forest is the first place the journey stops feeling simple. Press Z/Enter for the Rocket scout scene, Up for Route 3, or X/Esc to return to the gate."
