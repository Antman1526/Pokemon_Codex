extends Control

signal go_to_mt_moon_interior_1
signal go_to_route_4_cerulean_approach

var save_state
var dialogue_label: Label


func _ready() -> void:
	_build_scene()
	if save_state:
		save_state.enter_mt_moon_fossil_decision()
	_update_intro_dialogue()


func _unhandled_input(event: InputEvent) -> void:
	if event.is_action_pressed("ui_left"):
		choose_dome_fossil()
	if event.is_action_pressed("ui_right"):
		choose_helix_fossil()
	if event.is_action_pressed("ui_down"):
		proceed_to_route_4_cerulean_approach()
	if event.is_action_pressed("cancel"):
		return_to_mt_moon_interior_1()


func _build_scene() -> void:
	var floor := ColorRect.new()
	floor.color = Color("443a32")
	floor.set_anchors_preset(Control.PRESET_FULL_RECT)
	add_child(floor)

	var table := ColorRect.new()
	table.color = Color("a58d68")
	table.anchor_left = 0.24
	table.anchor_top = 0.28
	table.anchor_right = 0.76
	table.anchor_bottom = 0.58
	add_child(table)

	var dome := ColorRect.new()
	dome.color = Color("6d5a43")
	dome.anchor_left = 0.3
	dome.anchor_top = 0.36
	dome.anchor_right = 0.43
	dome.anchor_bottom = 0.5
	add_child(dome)

	var helix := ColorRect.new()
	helix.color = Color("7f714c")
	helix.anchor_left = 0.57
	helix.anchor_top = 0.36
	helix.anchor_right = 0.7
	helix.anchor_bottom = 0.5
	add_child(helix)

	var pulse := ColorRect.new()
	pulse.color = Color("b92732")
	pulse.anchor_left = 0.46
	pulse.anchor_top = 0.62
	pulse.anchor_right = 0.54
	pulse.anchor_bottom = 0.7
	add_child(pulse)

	var header := Label.new()
	header.text = "Mt. Moon Fossil Decision"
	header.anchor_left = 0.04
	header.anchor_top = 0.04
	header.anchor_right = 0.58
	header.anchor_bottom = 0.1
	header.add_theme_font_size_override("font_size", 32)
	header.add_theme_color_override("font_color", Color("fff2c7"))
	add_child(header)

	var dome_label := Label.new()
	dome_label.text = "Dome Fossil"
	dome_label.anchor_left = 0.29
	dome_label.anchor_top = 0.42
	dome_label.anchor_right = 0.45
	dome_label.anchor_bottom = 0.48
	dome_label.add_theme_font_size_override("font_size", 18)
	dome_label.add_theme_color_override("font_color", Color("fff2c7"))
	add_child(dome_label)

	var helix_label := Label.new()
	helix_label.text = "Helix Fossil"
	helix_label.anchor_left = 0.56
	helix_label.anchor_top = 0.42
	helix_label.anchor_right = 0.72
	helix_label.anchor_bottom = 0.48
	helix_label.add_theme_font_size_override("font_size", 18)
	helix_label.add_theme_color_override("font_color", Color("fff2c7"))
	add_child(helix_label)

	dialogue_label = Label.new()
	dialogue_label.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	dialogue_label.anchor_left = 0.06
	dialogue_label.anchor_top = 0.74
	dialogue_label.anchor_right = 0.94
	dialogue_label.anchor_bottom = 0.95
	dialogue_label.add_theme_font_size_override("font_size", 20)
	dialogue_label.add_theme_color_override("font_color", Color("fff2c7"))
	add_child(dialogue_label)


func choose_dome_fossil() -> void:
	if save_state:
		save_state.choose_mt_moon_fossil("dome")
	dialogue_label.text = "Antman secures the Dome Fossil while Red watches the Helix Fossil stabilize. The Nexus Fossil signal keeps pulsing below the table."


func choose_helix_fossil() -> void:
	if save_state:
		save_state.choose_mt_moon_fossil("helix")
	dialogue_label.text = "Antman secures the Helix Fossil while Red watches the Dome Fossil stabilize. The Nexus Fossil signal keeps pulsing below the table."


func return_to_mt_moon_interior_1() -> void:
	emit_signal("go_to_mt_moon_interior_1")


func proceed_to_route_4_cerulean_approach() -> void:
	if save_state and not bool(save_state.story_flags.get("mt_moon_fossil_choice_made", false)):
		dialogue_label.text = "Red: We need to choose one fossil before leaving this table. Dome or Helix first, then Cerulean."
		return
	dialogue_label.text = "Red: Route 4 opens east. Cerulean is next, and if Rocket and Gold Dust are both moving, Misty needs to know."
	emit_signal("go_to_route_4_cerulean_approach")


func _update_intro_dialogue() -> void:
	dialogue_label.text = "Red: Choose one now: Left for Dome Fossil, Right for Helix Fossil. Press Down for Route 4 after the choice. The Nexus Fossil is not on this table; it is deeper."
