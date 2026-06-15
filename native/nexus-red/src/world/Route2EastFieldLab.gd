extends Control

signal go_to_diglett_cave_detour

var save_state
var dialogue_label: Label


func _ready() -> void:
	_build_lab()
	if save_state:
		save_state.enter_route_2_east_field_lab()
	_update_intro_dialogue()


func _unhandled_input(event: InputEvent) -> void:
	if event.is_action_pressed("confirm"):
		trigger_route_2_field_lab_scene()
	if event.is_action_pressed("cancel"):
		return_to_diglett_cave_detour()


func _build_lab() -> void:
	var grass := ColorRect.new()
	grass.color = Color("6ca958")
	grass.set_anchors_preset(Control.PRESET_FULL_RECT)
	add_child(grass)

	var lab := ColorRect.new()
	lab.color = Color("d8d0b4")
	lab.anchor_left = 0.14
	lab.anchor_top = 0.16
	lab.anchor_right = 0.5
	lab.anchor_bottom = 0.48
	add_child(lab)

	var cave_exit := ColorRect.new()
	cave_exit.color = Color("3c342f")
	cave_exit.anchor_left = 0.62
	cave_exit.anchor_top = 0.24
	cave_exit.anchor_right = 0.88
	cave_exit.anchor_bottom = 0.5
	add_child(cave_exit)

	var route_path := ColorRect.new()
	route_path.color = Color("d9bb78")
	route_path.anchor_left = 0.08
	route_path.anchor_top = 0.56
	route_path.anchor_right = 0.92
	route_path.anchor_bottom = 0.68
	add_child(route_path)

	var signal_table := ColorRect.new()
	signal_table.color = Color("587ca6")
	signal_table.anchor_left = 0.22
	signal_table.anchor_top = 0.3
	signal_table.anchor_right = 0.42
	signal_table.anchor_bottom = 0.4
	add_child(signal_table)

	var header := Label.new()
	header.text = "Route 2 East Field Lab"
	header.anchor_left = 0.04
	header.anchor_top = 0.04
	header.anchor_right = 0.78
	header.anchor_bottom = 0.1
	header.add_theme_font_size_override("font_size", 32)
	header.add_theme_color_override("font_color", Color("14351f"))
	add_child(header)

	var lab_label := Label.new()
	lab_label.text = "Oak aide lab"
	lab_label.anchor_left = 0.24
	lab_label.anchor_top = 0.2
	lab_label.anchor_right = 0.48
	lab_label.anchor_bottom = 0.26
	lab_label.add_theme_font_size_override("font_size", 18)
	lab_label.add_theme_color_override("font_color", Color("2a261c"))
	add_child(lab_label)

	var cave_label := Label.new()
	cave_label.text = "Diglett's Cave exit"
	cave_label.anchor_left = 0.65
	cave_label.anchor_top = 0.34
	cave_label.anchor_right = 0.88
	cave_label.anchor_bottom = 0.4
	cave_label.add_theme_font_size_override("font_size", 16)
	cave_label.add_theme_color_override("font_color", Color("f5e6c7"))
	add_child(cave_label)

	dialogue_label = Label.new()
	dialogue_label.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	dialogue_label.anchor_left = 0.06
	dialogue_label.anchor_top = 0.76
	dialogue_label.anchor_right = 0.94
	dialogue_label.anchor_bottom = 0.96
	dialogue_label.add_theme_font_size_override("font_size", 20)
	dialogue_label.add_theme_color_override("font_color", Color("14351f"))
	add_child(dialogue_label)


func trigger_route_2_field_lab_scene() -> void:
	if save_state:
		save_state.record_route_2_field_lab_scene()
	dialogue_label.text = "Red: Route 2 proves we are still walking Kanto the real way. Bill and Oak's aide tuned the Echo Flute decoder, Rocket and Team Moonlight left a sleep signal pointed at Lavender, and the next physical road is back through Route 9 toward Rock Tunnel."


func return_to_diglett_cave_detour() -> void:
	emit_signal("go_to_diglett_cave_detour")


func _update_intro_dialogue() -> void:
	dialogue_label.text = "Red: This Route 2 field lab is where Bill turns the Echo Flute lead into a plan. Press Z/Enter to decode the signal, or X/Esc to return to Diglett's Cave."
