extends Control

signal go_to_pokemon_tower_first_floor
signal go_to_pokemon_tower_fuji_rescue

var save_state
var dialogue_label: Label


func _ready() -> void:
	_build_silph_scope_floor()
	if save_state:
		save_state.enter_pokemon_tower_silph_scope_floor()
	_update_intro_dialogue()


func _unhandled_input(event: InputEvent) -> void:
	if event.is_action_pressed("confirm"):
		trigger_pokemon_tower_silph_scope_floor_scene()
	if event.is_action_pressed("ui_right"):
		trigger_fuji_rescue_path()
	if event.is_action_pressed("cancel"):
		return_to_pokemon_tower_first_floor()


func _build_silph_scope_floor() -> void:
	var floor := ColorRect.new()
	floor.color = Color("2c2738")
	floor.set_anchors_preset(Control.PRESET_FULL_RECT)
	add_child(floor)

	var memorial_path := ColorRect.new()
	memorial_path.color = Color("635672")
	memorial_path.anchor_left = 0.08
	memorial_path.anchor_top = 0.5
	memorial_path.anchor_right = 0.92
	memorial_path.anchor_bottom = 0.68
	add_child(memorial_path)

	var silph_scope_beam := ColorRect.new()
	silph_scope_beam.color = Color("68b8c4")
	silph_scope_beam.anchor_left = 0.16
	silph_scope_beam.anchor_top = 0.18
	silph_scope_beam.anchor_right = 0.28
	silph_scope_beam.anchor_bottom = 0.46
	add_child(silph_scope_beam)

	var marowak_spirit := ColorRect.new()
	marowak_spirit.color = Color("d8d0ee")
	marowak_spirit.anchor_left = 0.38
	marowak_spirit.anchor_top = 0.2
	marowak_spirit.anchor_right = 0.56
	marowak_spirit.anchor_bottom = 0.44
	add_child(marowak_spirit)

	var cubone_corner := ColorRect.new()
	cubone_corner.color = Color("9f9272")
	cubone_corner.anchor_left = 0.2
	cubone_corner.anchor_top = 0.72
	cubone_corner.anchor_right = 0.36
	cubone_corner.anchor_bottom = 0.9
	add_child(cubone_corner)

	var rocket_hold := ColorRect.new()
	rocket_hold.color = Color("2a2025")
	rocket_hold.anchor_left = 0.64
	rocket_hold.anchor_top = 0.2
	rocket_hold.anchor_right = 0.86
	rocket_hold.anchor_bottom = 0.42
	add_child(rocket_hold)

	var moonlight_ritual := ColorRect.new()
	moonlight_ritual.color = Color("7562ba")
	moonlight_ritual.anchor_left = 0.62
	moonlight_ritual.anchor_top = 0.72
	moonlight_ritual.anchor_right = 0.84
	moonlight_ritual.anchor_bottom = 0.9
	add_child(moonlight_ritual)

	var header := Label.new()
	header.text = "Pokemon Tower - Silph Scope Floor"
	header.anchor_left = 0.04
	header.anchor_top = 0.04
	header.anchor_right = 0.92
	header.anchor_bottom = 0.1
	header.add_theme_font_size_override("font_size", 32)
	header.add_theme_color_override("font_color", Color("f3eaff"))
	add_child(header)

	var scope_label := Label.new()
	scope_label.text = "Silph Scope reading"
	scope_label.anchor_left = 0.12
	scope_label.anchor_top = 0.47
	scope_label.anchor_right = 0.36
	scope_label.anchor_bottom = 0.54
	scope_label.add_theme_font_size_override("font_size", 16)
	scope_label.add_theme_color_override("font_color", Color("f3eaff"))
	add_child(scope_label)

	var spirit_label := Label.new()
	spirit_label.text = "Marowak spirit"
	spirit_label.anchor_left = 0.38
	spirit_label.anchor_top = 0.45
	spirit_label.anchor_right = 0.58
	spirit_label.anchor_bottom = 0.52
	spirit_label.add_theme_font_size_override("font_size", 16)
	spirit_label.add_theme_color_override("font_color", Color("f3eaff"))
	add_child(spirit_label)

	var cubone_label := Label.new()
	cubone_label.text = "Cubone grief scene"
	cubone_label.anchor_left = 0.18
	cubone_label.anchor_top = 0.91
	cubone_label.anchor_right = 0.42
	cubone_label.anchor_bottom = 0.98
	cubone_label.add_theme_font_size_override("font_size", 16)
	cubone_label.add_theme_color_override("font_color", Color("f3eaff"))
	add_child(cubone_label)

	var rocket_label := Label.new()
	rocket_label.text = "Rocket holds Mr. Fuji"
	rocket_label.anchor_left = 0.6
	rocket_label.anchor_top = 0.43
	rocket_label.anchor_right = 0.9
	rocket_label.anchor_bottom = 0.5
	rocket_label.add_theme_font_size_override("font_size", 16)
	rocket_label.add_theme_color_override("font_color", Color("f3eaff"))
	add_child(rocket_label)

	var moonlight_label := Label.new()
	moonlight_label.text = "Moonlight ritual"
	moonlight_label.anchor_left = 0.62
	moonlight_label.anchor_top = 0.91
	moonlight_label.anchor_right = 0.86
	moonlight_label.anchor_bottom = 0.98
	moonlight_label.add_theme_font_size_override("font_size", 16)
	moonlight_label.add_theme_color_override("font_color", Color("f3eaff"))
	add_child(moonlight_label)

	dialogue_label = Label.new()
	dialogue_label.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	dialogue_label.anchor_left = 0.06
	dialogue_label.anchor_top = 0.1
	dialogue_label.anchor_right = 0.94
	dialogue_label.anchor_bottom = 0.18
	dialogue_label.add_theme_font_size_override("font_size", 19)
	dialogue_label.add_theme_color_override("font_color", Color("f3eaff"))
	add_child(dialogue_label)


func trigger_pokemon_tower_silph_scope_floor_scene() -> void:
	if save_state:
		save_state.record_pokemon_tower_silph_scope_floor_scene()
	dialogue_label.text = "Red: The Silph Scope is showing Marowak's spirit clearly. Bill says Team Moonlight twisted the grief signal, Rocket is holding Mr. Fuji above us, Cubone is reacting to the truth, and the Poke Flute lead opens once we break this floor's pressure."


func trigger_fuji_rescue_path() -> void:
	if save_state == null or not bool(save_state.story_flags.get("mr_fuji_rescue_path_unlocked", false)) or not bool(save_state.story_flags.get("poke_flute_lead_unlocked", false)):
		dialogue_label.text = "Red: Mr. Fuji is still hidden behind the Silph Scope pressure. Reveal Marowak, Cubone, Rocket, Moonlight, and the Poke Flute lead first."
		return
	dialogue_label.text = "Red: Mr. Fuji is above us, and Rocket knows the Poke Flute can wake Snorlax. I am with you."
	emit_signal("go_to_pokemon_tower_fuji_rescue")


func return_to_pokemon_tower_first_floor() -> void:
	emit_signal("go_to_pokemon_tower_first_floor")


func _update_intro_dialogue() -> void:
	dialogue_label.text = "Red: This Silph Scope floor is the real Pokemon Tower turn. Press Z/Enter to reveal Marowak, Cubone, Mr. Fuji, Rocket, Moonlight, Bill's reading, and the Poke Flute lead. Press Right for Mr. Fuji's rescue or X/Esc to return."
