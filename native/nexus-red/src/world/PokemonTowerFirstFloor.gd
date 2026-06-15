extends Control

signal go_to_lavender_outskirts

var save_state
var dialogue_label: Label


func _ready() -> void:
	_build_tower()
	if save_state:
		save_state.enter_pokemon_tower_first_floor()
	_update_intro_dialogue()


func _unhandled_input(event: InputEvent) -> void:
	if event.is_action_pressed("confirm"):
		trigger_pokemon_tower_first_floor_scene()
	if event.is_action_pressed("ui_right"):
		trigger_deeper_tower_path()
	if event.is_action_pressed("cancel"):
		return_to_lavender_outskirts()


func _build_tower() -> void:
	var floor := ColorRect.new()
	floor.color = Color("3f344d")
	floor.set_anchors_preset(Control.PRESET_FULL_RECT)
	add_child(floor)

	var hall := ColorRect.new()
	hall.color = Color("6c5c7e")
	hall.anchor_left = 0.08
	hall.anchor_top = 0.52
	hall.anchor_right = 0.92
	hall.anchor_bottom = 0.68
	add_child(hall)

	var memorial := ColorRect.new()
	memorial.color = Color("b8abc9")
	memorial.anchor_left = 0.2
	memorial.anchor_top = 0.22
	memorial.anchor_right = 0.42
	memorial.anchor_bottom = 0.48
	add_child(memorial)

	var stair_shadow := ColorRect.new()
	stair_shadow.color = Color("221b2d")
	stair_shadow.anchor_left = 0.72
	stair_shadow.anchor_top = 0.22
	stair_shadow.anchor_right = 0.9
	stair_shadow.anchor_bottom = 0.48
	add_child(stair_shadow)

	var moonlight_pressure := ColorRect.new()
	moonlight_pressure.color = Color("7567bd")
	moonlight_pressure.anchor_left = 0.5
	moonlight_pressure.anchor_top = 0.3
	moonlight_pressure.anchor_right = 0.64
	moonlight_pressure.anchor_bottom = 0.44
	add_child(moonlight_pressure)

	var rocket_grunt := ColorRect.new()
	rocket_grunt.color = Color("2c252a")
	rocket_grunt.anchor_left = 0.82
	rocket_grunt.anchor_top = 0.58
	rocket_grunt.anchor_right = 0.92
	rocket_grunt.anchor_bottom = 0.72
	add_child(rocket_grunt)

	var header := Label.new()
	header.text = "Pokemon Tower - First Floor"
	header.anchor_left = 0.04
	header.anchor_top = 0.04
	header.anchor_right = 0.84
	header.anchor_bottom = 0.1
	header.add_theme_font_size_override("font_size", 32)
	header.add_theme_color_override("font_color", Color("f3eaff"))
	add_child(header)

	var memorial_label := Label.new()
	memorial_label.text = "Cubone memorial"
	memorial_label.anchor_left = 0.2
	memorial_label.anchor_top = 0.49
	memorial_label.anchor_right = 0.44
	memorial_label.anchor_bottom = 0.55
	memorial_label.add_theme_font_size_override("font_size", 16)
	memorial_label.add_theme_color_override("font_color", Color("f3eaff"))
	add_child(memorial_label)

	var stair_label := Label.new()
	stair_label.text = "deeper tower locked"
	stair_label.anchor_left = 0.68
	stair_label.anchor_top = 0.49
	stair_label.anchor_right = 0.94
	stair_label.anchor_bottom = 0.55
	stair_label.add_theme_font_size_override("font_size", 16)
	stair_label.add_theme_color_override("font_color", Color("f3eaff"))
	add_child(stair_label)

	var pressure_label := Label.new()
	pressure_label.text = "Moonlight pressure + Rocket lookout"
	pressure_label.anchor_left = 0.46
	pressure_label.anchor_top = 0.73
	pressure_label.anchor_right = 0.94
	pressure_label.anchor_bottom = 0.79
	pressure_label.add_theme_font_size_override("font_size", 16)
	pressure_label.add_theme_color_override("font_color", Color("f3eaff"))
	add_child(pressure_label)

	dialogue_label = Label.new()
	dialogue_label.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	dialogue_label.anchor_left = 0.06
	dialogue_label.anchor_top = 0.82
	dialogue_label.anchor_right = 0.94
	dialogue_label.anchor_bottom = 0.98
	dialogue_label.add_theme_font_size_override("font_size", 20)
	dialogue_label.add_theme_color_override("font_color", Color("f3eaff"))
	add_child(dialogue_label)


func trigger_pokemon_tower_first_floor_scene() -> void:
	if save_state:
		save_state.record_pokemon_tower_first_floor_scene()
	dialogue_label.text = "Red: Pokemon Tower is heavier than Lavender outside. Bill says the Echo Flute is distorting here, Team Moonlight is using the grief in this place, and a Rocket grunt is watching the stairs. Cubone and Mr. Fuji are tied to the signal, but we need the Silph Scope before going deeper."


func trigger_deeper_tower_path() -> void:
	dialogue_label.text = "Red: The deeper Pokemon Tower path stays locked until we get the Silph Scope. Without it, the Echo Flute and Bill's readings are just noise."


func return_to_lavender_outskirts() -> void:
	emit_signal("go_to_lavender_outskirts")


func _update_intro_dialogue() -> void:
	dialogue_label.text = "Red: This is Pokemon Tower's first floor. Press Z/Enter to inspect Bill's Echo Flute distortion, Team Moonlight pressure, Rocket's lookout, Cubone, Mr. Fuji, and the Silph Scope problem, Right to test the deeper path, or X/Esc to return to Lavender."
