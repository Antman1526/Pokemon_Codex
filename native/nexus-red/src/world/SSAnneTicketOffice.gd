extends Control

signal go_to_vermilion_city

var save_state
var dialogue_label: Label


func _ready() -> void:
	_build_ticket_office()
	if save_state:
		save_state.enter_ss_anne_ticket_office()
	_update_intro_dialogue()


func _unhandled_input(event: InputEvent) -> void:
	if event.is_action_pressed("confirm"):
		trigger_ticket_office_scene()
	if event.is_action_pressed("cancel"):
		return_to_vermilion_city()


func _build_ticket_office() -> void:
	var floor := ColorRect.new()
	floor.color = Color("d5c48d")
	floor.set_anchors_preset(Control.PRESET_FULL_RECT)
	add_child(floor)

	var counter := ColorRect.new()
	counter.color = Color("7a4d35")
	counter.anchor_left = 0.12
	counter.anchor_top = 0.22
	counter.anchor_right = 0.88
	counter.anchor_bottom = 0.36
	add_child(counter)

	var harbor_window := ColorRect.new()
	harbor_window.color = Color("4aa7d8")
	harbor_window.anchor_left = 0.1
	harbor_window.anchor_top = 0.5
	harbor_window.anchor_right = 0.9
	harbor_window.anchor_bottom = 0.64
	add_child(harbor_window)

	var manifest_table := ColorRect.new()
	manifest_table.color = Color("4d6b4d")
	manifest_table.anchor_left = 0.56
	manifest_table.anchor_top = 0.4
	manifest_table.anchor_right = 0.82
	manifest_table.anchor_bottom = 0.52
	add_child(manifest_table)

	var header := Label.new()
	header.text = "S.S. Anne Ticket Office"
	header.anchor_left = 0.04
	header.anchor_top = 0.04
	header.anchor_right = 0.8
	header.anchor_bottom = 0.1
	header.add_theme_font_size_override("font_size", 32)
	header.add_theme_color_override("font_color", Color("2f2415"))
	add_child(header)

	var counter_label := Label.new()
	counter_label.text = "Harbor Counter"
	counter_label.anchor_left = 0.36
	counter_label.anchor_top = 0.26
	counter_label.anchor_right = 0.66
	counter_label.anchor_bottom = 0.32
	counter_label.add_theme_font_size_override("font_size", 18)
	counter_label.add_theme_color_override("font_color", Color("fff1d5"))
	add_child(counter_label)

	var manifest_label := Label.new()
	manifest_label.text = "Manifest Desk"
	manifest_label.anchor_left = 0.6
	manifest_label.anchor_top = 0.43
	manifest_label.anchor_right = 0.8
	manifest_label.anchor_bottom = 0.5
	manifest_label.add_theme_font_size_override("font_size", 16)
	manifest_label.add_theme_color_override("font_color", Color("fff1d5"))
	add_child(manifest_label)

	dialogue_label = Label.new()
	dialogue_label.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	dialogue_label.anchor_left = 0.06
	dialogue_label.anchor_top = 0.72
	dialogue_label.anchor_right = 0.94
	dialogue_label.anchor_bottom = 0.95
	dialogue_label.add_theme_font_size_override("font_size", 20)
	dialogue_label.add_theme_color_override("font_color", Color("2f2415"))
	add_child(dialogue_label)


func trigger_ticket_office_scene() -> void:
	if save_state:
		save_state.record_ss_anne_ticket_office_scene()
	dialogue_label.text = "Bill: The S.S. Anne manifest was edited after Rocket reached Vermilion. Red, keep the harbor doors covered. Misty, watch the waterline. Antman, this boarding pass gets us onto the ship before the fake passengers vanish."


func return_to_vermilion_city() -> void:
	emit_signal("go_to_vermilion_city")


func _update_intro_dialogue() -> void:
	dialogue_label.text = "Red: This is the S.S. Anne Ticket Office. Bill can read the manifest, Misty can spot harbor movement, and I will watch for Rocket. Press Z/Enter to work the counter, or X/Esc to return to Vermilion."
