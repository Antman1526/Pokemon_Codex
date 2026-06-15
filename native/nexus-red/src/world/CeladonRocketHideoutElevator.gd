extends Control

signal go_to_rocket_hideout_b3f
signal go_to_rocket_command_floor

var save_state
var dialogue_label: Label


func _ready() -> void:
	_build_elevator()
	if save_state:
		save_state.enter_celadon_rocket_hideout_elevator()
	_update_intro_dialogue()


func _unhandled_input(event: InputEvent) -> void:
	if event.is_action_pressed("confirm"):
		trigger_rocket_hideout_elevator_scene()
	if event.is_action_pressed("ui_right"):
		trigger_rocket_command_floor_entry()
	if event.is_action_pressed("cancel"):
		return_to_rocket_hideout_b3f()


func _build_elevator() -> void:
	var floor := ColorRect.new()
	floor.color = Color("22212a")
	floor.set_anchors_preset(Control.PRESET_FULL_RECT)
	add_child(floor)

	var elevator_shaft := ColorRect.new()
	elevator_shaft.color = Color("3a3541")
	elevator_shaft.anchor_left = 0.12
	elevator_shaft.anchor_top = 0.18
	elevator_shaft.anchor_right = 0.36
	elevator_shaft.anchor_bottom = 0.82
	add_child(elevator_shaft)

	var control_panel := ColorRect.new()
	control_panel.color = Color("7e8794")
	control_panel.anchor_left = 0.42
	control_panel.anchor_top = 0.22
	control_panel.anchor_right = 0.6
	control_panel.anchor_bottom = 0.46
	add_child(control_panel)

	var nexus_override := ColorRect.new()
	nexus_override.color = Color("315f78")
	nexus_override.anchor_left = 0.64
	nexus_override.anchor_top = 0.18
	nexus_override.anchor_right = 0.88
	nexus_override.anchor_bottom = 0.38
	add_child(nexus_override)

	var gold_ledger := ColorRect.new()
	gold_ledger.color = Color("b98d2d")
	gold_ledger.anchor_left = 0.42
	gold_ledger.anchor_top = 0.58
	gold_ledger.anchor_right = 0.6
	gold_ledger.anchor_bottom = 0.78
	add_child(gold_ledger)

	var moonlight_signal := ColorRect.new()
	moonlight_signal.color = Color("6d65bf")
	moonlight_signal.anchor_left = 0.64
	moonlight_signal.anchor_top = 0.58
	moonlight_signal.anchor_right = 0.88
	moonlight_signal.anchor_bottom = 0.78
	add_child(moonlight_signal)

	var header := Label.new()
	header.text = "Celadon Rocket Hideout - Elevator"
	header.anchor_left = 0.04
	header.anchor_top = 0.04
	header.anchor_right = 0.92
	header.anchor_bottom = 0.1
	header.add_theme_font_size_override("font_size", 32)
	header.add_theme_color_override("font_color", Color("f3e8df"))
	add_child(header)

	var shaft_label := Label.new()
	shaft_label.text = "Rocket elevator shaft"
	shaft_label.anchor_left = 0.12
	shaft_label.anchor_top = 0.83
	shaft_label.anchor_right = 0.38
	shaft_label.anchor_bottom = 0.89
	shaft_label.add_theme_font_size_override("font_size", 17)
	shaft_label.add_theme_color_override("font_color", Color("f3e8df"))
	add_child(shaft_label)

	var panel_label := Label.new()
	panel_label.text = "Restored Rocket panel"
	panel_label.anchor_left = 0.39
	panel_label.anchor_top = 0.47
	panel_label.anchor_right = 0.64
	panel_label.anchor_bottom = 0.53
	panel_label.add_theme_font_size_override("font_size", 16)
	panel_label.add_theme_color_override("font_color", Color("f3e8df"))
	add_child(panel_label)

	var nexus_label := Label.new()
	nexus_label.text = "Nexus Order override"
	nexus_label.anchor_left = 0.63
	nexus_label.anchor_top = 0.39
	nexus_label.anchor_right = 0.9
	nexus_label.anchor_bottom = 0.45
	nexus_label.add_theme_font_size_override("font_size", 16)
	nexus_label.add_theme_color_override("font_color", Color("f3e8df"))
	add_child(nexus_label)

	var gold_label := Label.new()
	gold_label.text = "Gold Dust ledger"
	gold_label.anchor_left = 0.42
	gold_label.anchor_top = 0.79
	gold_label.anchor_right = 0.62
	gold_label.anchor_bottom = 0.85
	gold_label.add_theme_font_size_override("font_size", 16)
	gold_label.add_theme_color_override("font_color", Color("f3e8df"))
	add_child(gold_label)

	var moonlight_label := Label.new()
	moonlight_label.text = "Moonlight sleep signal"
	moonlight_label.anchor_left = 0.63
	moonlight_label.anchor_top = 0.79
	moonlight_label.anchor_right = 0.9
	moonlight_label.anchor_bottom = 0.85
	moonlight_label.add_theme_font_size_override("font_size", 16)
	moonlight_label.add_theme_color_override("font_color", Color("f3e8df"))
	add_child(moonlight_label)

	dialogue_label = Label.new()
	dialogue_label.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	dialogue_label.anchor_left = 0.06
	dialogue_label.anchor_top = 0.1
	dialogue_label.anchor_right = 0.94
	dialogue_label.anchor_bottom = 0.17
	dialogue_label.add_theme_font_size_override("font_size", 19)
	dialogue_label.add_theme_color_override("font_color", Color("f3e8df"))
	add_child(dialogue_label)


func trigger_rocket_hideout_elevator_scene() -> void:
	if save_state:
		save_state.record_celadon_rocket_hideout_elevator_scene()
	dialogue_label.text = "Red: I will hold the elevator guard line. Bill decoded the Nexus Order override, the Rocket elevator panel is restored, Gold Dust left a ledger on Giovanni's command floor route, and Moonlight hid a sleep signal in the shaft. The command floor is open."


func trigger_rocket_command_floor_entry() -> void:
	if save_state == null or not save_state.story_flags.get("rocket_command_floor_path_unlocked", false):
		dialogue_label.text = "Red: The command floor is still locked. Let Bill decode the Nexus Order override and restore Rocket's elevator panel first."
		return
	dialogue_label.text = "Red: Giovanni's command floor is exposed. I am with you until the door."
	emit_signal("go_to_rocket_command_floor")


func return_to_rocket_hideout_b3f() -> void:
	emit_signal("go_to_rocket_hideout_b3f")


func _update_intro_dialogue() -> void:
	dialogue_label.text = "Red: This elevator is the route to Giovanni. Press Z/Enter to inspect the Rocket panel, Nexus Order override, Gold Dust ledger, Moonlight sleep signal, and command floor route. Press Right for the command floor or X/Esc to return to B3F."
