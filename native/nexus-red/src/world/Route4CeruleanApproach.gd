extends Control

signal go_to_mt_moon_fossil_decision
signal go_to_cerulean_city

var save_state
var dialogue_label: Label


func _ready() -> void:
	_build_route()
	if save_state:
		save_state.enter_route_4_cerulean_approach()
	_update_intro_dialogue()


func _unhandled_input(event: InputEvent) -> void:
	if event.is_action_pressed("confirm"):
		trigger_red_cerulean_warning()
	if event.is_action_pressed("ui_right"):
		trigger_cerulean_city_entry()
	if event.is_action_pressed("cancel"):
		return_to_mt_moon_fossil_decision()


func _build_route() -> void:
	var grass := ColorRect.new()
	grass.color = Color("7bbb68")
	grass.set_anchors_preset(Control.PRESET_FULL_RECT)
	add_child(grass)

	var cave_mouth := ColorRect.new()
	cave_mouth.color = Color("463d39")
	cave_mouth.anchor_left = 0.02
	cave_mouth.anchor_top = 0.28
	cave_mouth.anchor_right = 0.22
	cave_mouth.anchor_bottom = 0.64
	add_child(cave_mouth)

	var path := ColorRect.new()
	path.color = Color("d9b46d")
	path.anchor_left = 0.16
	path.anchor_top = 0.46
	path.anchor_right = 0.92
	path.anchor_bottom = 0.6
	add_child(path)

	var water := ColorRect.new()
	water.color = Color("5aa6c9")
	water.anchor_left = 0.72
	water.anchor_top = 0.1
	water.anchor_right = 1.0
	water.anchor_bottom = 0.36
	add_child(water)

	var bridge_shadow := ColorRect.new()
	bridge_shadow.color = Color("7e6d4b")
	bridge_shadow.anchor_left = 0.72
	bridge_shadow.anchor_top = 0.34
	bridge_shadow.anchor_right = 0.96
	bridge_shadow.anchor_bottom = 0.42
	add_child(bridge_shadow)

	var header := Label.new()
	header.text = "Route 4 - Cerulean Approach"
	header.anchor_left = 0.04
	header.anchor_top = 0.04
	header.anchor_right = 0.74
	header.anchor_bottom = 0.1
	header.add_theme_font_size_override("font_size", 32)
	header.add_theme_color_override("font_color", Color("14243d"))
	add_child(header)

	var sign := Label.new()
	sign.text = "Cerulean City ahead"
	sign.anchor_left = 0.67
	sign.anchor_top = 0.44
	sign.anchor_right = 0.96
	sign.anchor_bottom = 0.5
	sign.add_theme_font_size_override("font_size", 20)
	sign.add_theme_color_override("font_color", Color("14243d"))
	add_child(sign)

	dialogue_label = Label.new()
	dialogue_label.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	dialogue_label.anchor_left = 0.06
	dialogue_label.anchor_top = 0.76
	dialogue_label.anchor_right = 0.94
	dialogue_label.anchor_bottom = 0.95
	dialogue_label.add_theme_font_size_override("font_size", 20)
	dialogue_label.add_theme_color_override("font_color", Color("14243d"))
	add_child(dialogue_label)


func trigger_red_cerulean_warning() -> void:
	if save_state:
		save_state.record_red_route_4_cerulean_warning()
	dialogue_label.text = "Red: Cerulean is not just Misty's gym. Rocket and Gold Dust both ran east, and the bridge crowd feels staged. We warn Misty before the city turns into their next fossil market."


func return_to_mt_moon_fossil_decision() -> void:
	emit_signal("go_to_mt_moon_fossil_decision")


func trigger_cerulean_city_entry() -> void:
	if save_state and not bool(save_state.story_flags.get("red_route_4_cerulean_warning_seen", false)):
		dialogue_label.text = "Red: Before we enter Cerulean, talk this through with me. Misty needs facts, not panic."
		return
	dialogue_label.text = "Red: Cerulean City is ahead. We find Misty first, then we handle Nugget Bridge."
	emit_signal("go_to_cerulean_city")


func _update_intro_dialogue() -> void:
	dialogue_label.text = "Red: Route 4 is the breath after Mt. Moon. Press Z/Enter to talk through the Cerulean plan, Right for Cerulean City, or X/Esc to step back toward the fossil table."
