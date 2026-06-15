extends Control

signal go_to_pokemon_tower_first_floor

var save_state
var dialogue_label: Label


func _ready() -> void:
	_build_route()
	if save_state:
		save_state.enter_route_8_celadon_road()
	_update_intro_dialogue()


func _unhandled_input(event: InputEvent) -> void:
	if event.is_action_pressed("confirm"):
		trigger_route_8_celadon_road_scene()
	if event.is_action_pressed("cancel"):
		return_to_pokemon_tower_first_floor()


func _build_route() -> void:
	var grass := ColorRect.new()
	grass.color = Color("6f8f55")
	grass.set_anchors_preset(Control.PRESET_FULL_RECT)
	add_child(grass)

	var road := ColorRect.new()
	road.color = Color("d1b875")
	road.anchor_left = 0.06
	road.anchor_top = 0.48
	road.anchor_right = 0.94
	road.anchor_bottom = 0.62
	add_child(road)

	var lavender_gate := ColorRect.new()
	lavender_gate.color = Color("8c7fa4")
	lavender_gate.anchor_left = 0.06
	lavender_gate.anchor_top = 0.28
	lavender_gate.anchor_right = 0.24
	lavender_gate.anchor_bottom = 0.48
	add_child(lavender_gate)

	var underground_entrance := ColorRect.new()
	underground_entrance.color = Color("5b4b35")
	underground_entrance.anchor_left = 0.5
	underground_entrance.anchor_top = 0.28
	underground_entrance.anchor_right = 0.68
	underground_entrance.anchor_bottom = 0.48
	add_child(underground_entrance)

	var celadon_hint := ColorRect.new()
	celadon_hint.color = Color("7a9961")
	celadon_hint.anchor_left = 0.78
	celadon_hint.anchor_top = 0.3
	celadon_hint.anchor_right = 0.94
	celadon_hint.anchor_bottom = 0.52
	add_child(celadon_hint)

	var moonlight_shadow := ColorRect.new()
	moonlight_shadow.color = Color("7464a9")
	moonlight_shadow.anchor_left = 0.3
	moonlight_shadow.anchor_top = 0.64
	moonlight_shadow.anchor_right = 0.44
	moonlight_shadow.anchor_bottom = 0.76
	add_child(moonlight_shadow)

	var rocket_mark := ColorRect.new()
	rocket_mark.color = Color("2f292d")
	rocket_mark.anchor_left = 0.68
	rocket_mark.anchor_top = 0.64
	rocket_mark.anchor_right = 0.82
	rocket_mark.anchor_bottom = 0.76
	add_child(rocket_mark)

	var header := Label.new()
	header.text = "Route 8 - Celadon Road"
	header.anchor_left = 0.04
	header.anchor_top = 0.04
	header.anchor_right = 0.8
	header.anchor_bottom = 0.1
	header.add_theme_font_size_override("font_size", 32)
	header.add_theme_color_override("font_color", Color("19351c"))
	add_child(header)

	var underground_label := Label.new()
	underground_label.text = "Underground Path"
	underground_label.anchor_left = 0.48
	underground_label.anchor_top = 0.22
	underground_label.anchor_right = 0.72
	underground_label.anchor_bottom = 0.28
	underground_label.add_theme_font_size_override("font_size", 16)
	underground_label.add_theme_color_override("font_color", Color("f3ead7"))
	add_child(underground_label)

	var celadon_label := Label.new()
	celadon_label.text = "Celadon lead"
	celadon_label.anchor_left = 0.78
	celadon_label.anchor_top = 0.54
	celadon_label.anchor_right = 0.96
	celadon_label.anchor_bottom = 0.6
	celadon_label.add_theme_font_size_override("font_size", 16)
	celadon_label.add_theme_color_override("font_color", Color("f6ffe8"))
	add_child(celadon_label)

	var pressure_label := Label.new()
	pressure_label.text = "Moonlight shadow / Rocket Game Corner mark"
	pressure_label.anchor_left = 0.25
	pressure_label.anchor_top = 0.77
	pressure_label.anchor_right = 0.9
	pressure_label.anchor_bottom = 0.83
	pressure_label.add_theme_font_size_override("font_size", 16)
	pressure_label.add_theme_color_override("font_color", Color("f6ffe8"))
	add_child(pressure_label)

	dialogue_label = Label.new()
	dialogue_label.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	dialogue_label.anchor_left = 0.06
	dialogue_label.anchor_top = 0.86
	dialogue_label.anchor_right = 0.94
	dialogue_label.anchor_bottom = 0.98
	dialogue_label.add_theme_font_size_override("font_size", 20)
	dialogue_label.add_theme_color_override("font_color", Color("19351c"))
	add_child(dialogue_label)


func trigger_route_8_celadon_road_scene() -> void:
	if save_state:
		save_state.record_route_8_celadon_road_scene()
	dialogue_label.text = "Red: Route 8 keeps us on foot toward Celadon. Bill traced the Silph Scope signal west, Rocket's Game Corner front is the cleanest lead, and Team Moonlight left a shadow behind us from Pokemon Tower. The Underground Path to Celadon is open."


func return_to_pokemon_tower_first_floor() -> void:
	emit_signal("go_to_pokemon_tower_first_floor")


func _update_intro_dialogue() -> void:
	dialogue_label.text = "Red: Route 8 is the physical road from Lavender toward Celadon. Press Z/Enter to trace Bill's Silph Scope lead, Rocket's Game Corner front, Team Moonlight's shadow, and the Underground Path, or X/Esc to return to Pokemon Tower."
