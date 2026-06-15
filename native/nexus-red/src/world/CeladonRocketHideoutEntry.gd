extends Control

signal go_to_game_corner_exterior
signal go_to_rocket_hideout_b1f

var save_state
var dialogue_label: Label


func _ready() -> void:
	_build_hideout()
	if save_state:
		save_state.enter_celadon_rocket_hideout_entry()
	_update_intro_dialogue()


func _unhandled_input(event: InputEvent) -> void:
	if event.is_action_pressed("confirm"):
		trigger_rocket_hideout_entry_scene()
	if event.is_action_pressed("ui_right"):
		trigger_rocket_hideout_b1f_entry()
	if event.is_action_pressed("cancel"):
		return_to_game_corner_exterior()


func _build_hideout() -> void:
	var floor := ColorRect.new()
	floor.color = Color("343036")
	floor.set_anchors_preset(Control.PRESET_FULL_RECT)
	add_child(floor)

	var corridor := ColorRect.new()
	corridor.color = Color("5b555e")
	corridor.anchor_left = 0.08
	corridor.anchor_top = 0.42
	corridor.anchor_right = 0.92
	corridor.anchor_bottom = 0.58
	add_child(corridor)

	var stairwell := ColorRect.new()
	stairwell.color = Color("2f2731")
	stairwell.anchor_left = 0.08
	stairwell.anchor_top = 0.18
	stairwell.anchor_right = 0.26
	stairwell.anchor_bottom = 0.38
	add_child(stairwell)

	var elevator := ColorRect.new()
	elevator.color = Color("7a657d")
	elevator.anchor_left = 0.68
	elevator.anchor_top = 0.18
	elevator.anchor_right = 0.88
	elevator.anchor_bottom = 0.4
	add_child(elevator)

	var terminal := ColorRect.new()
	terminal.color = Color("315f78")
	terminal.anchor_left = 0.38
	terminal.anchor_top = 0.2
	terminal.anchor_right = 0.56
	terminal.anchor_bottom = 0.36
	add_child(terminal)

	var moonlight_mark := ColorRect.new()
	moonlight_mark.color = Color("6c63b5")
	moonlight_mark.anchor_left = 0.38
	moonlight_mark.anchor_top = 0.62
	moonlight_mark.anchor_right = 0.56
	moonlight_mark.anchor_bottom = 0.76
	add_child(moonlight_mark)

	var header := Label.new()
	header.text = "Celadon Rocket Hideout - Entry"
	header.anchor_left = 0.04
	header.anchor_top = 0.04
	header.anchor_right = 0.9
	header.anchor_bottom = 0.1
	header.add_theme_font_size_override("font_size", 32)
	header.add_theme_color_override("font_color", Color("f3e8df"))
	add_child(header)

	var elevator_label := Label.new()
	elevator_label.text = "Elevator / Lift Key"
	elevator_label.anchor_left = 0.67
	elevator_label.anchor_top = 0.41
	elevator_label.anchor_right = 0.9
	elevator_label.anchor_bottom = 0.47
	elevator_label.add_theme_font_size_override("font_size", 18)
	elevator_label.add_theme_color_override("font_color", Color("f3e8df"))
	add_child(elevator_label)

	var terminal_label := Label.new()
	terminal_label.text = "Giovanni command terminal"
	terminal_label.anchor_left = 0.32
	terminal_label.anchor_top = 0.14
	terminal_label.anchor_right = 0.62
	terminal_label.anchor_bottom = 0.2
	terminal_label.add_theme_font_size_override("font_size", 16)
	terminal_label.add_theme_color_override("font_color", Color("f3e8df"))
	add_child(terminal_label)

	var moonlight_label := Label.new()
	moonlight_label.text = "Moonlight interference"
	moonlight_label.anchor_left = 0.34
	moonlight_label.anchor_top = 0.77
	moonlight_label.anchor_right = 0.62
	moonlight_label.anchor_bottom = 0.83
	moonlight_label.add_theme_font_size_override("font_size", 16)
	moonlight_label.add_theme_color_override("font_color", Color("f3e8df"))
	add_child(moonlight_label)

	dialogue_label = Label.new()
	dialogue_label.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	dialogue_label.anchor_left = 0.06
	dialogue_label.anchor_top = 0.84
	dialogue_label.anchor_right = 0.94
	dialogue_label.anchor_bottom = 0.98
	dialogue_label.add_theme_font_size_override("font_size", 20)
	dialogue_label.add_theme_color_override("font_color", Color("f3e8df"))
	add_child(dialogue_label)


func trigger_rocket_hideout_entry_scene() -> void:
	if save_state:
		save_state.record_celadon_rocket_hideout_entry_scene()
	dialogue_label.text = "Red: This Rocket Hideout entry is too clean. Bill says the elevator is broadcasting the same Silph Scope pattern, the Lift Key is required deeper in, Giovanni left a command on that terminal, and Team Moonlight interference is already scraping Rocket's signal."


func trigger_rocket_hideout_b1f_entry() -> void:
	if save_state == null or not save_state.story_flags.get("rocket_hideout_b1f_path_unlocked", false):
		dialogue_label.text = "Red: We need to map the elevator signal, Lift Key requirement, and Giovanni command before we move deeper into the Hideout."
		return
	dialogue_label.text = "Red: B1F is open as the next hideout route. We move carefully; Rocket built this place to split trainers up."
	emit_signal("go_to_rocket_hideout_b1f")


func return_to_game_corner_exterior() -> void:
	emit_signal("go_to_game_corner_exterior")


func _update_intro_dialogue() -> void:
	dialogue_label.text = "Red: The poster switch opened the Rocket Hideout entry. Press Z/Enter to map Bill's elevator signal, the Lift Key barrier, Giovanni's command, Team Moonlight interference, and the Silph Scope link. Press Right for the B1F path or X/Esc to return to the Game Corner exterior."
