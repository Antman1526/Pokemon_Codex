extends Control

signal go_to_celadon_underground_path

var save_state
var dialogue_label: Label


func _ready() -> void:
	_build_city()
	if save_state:
		save_state.enter_celadon_city()
	_update_intro_dialogue()


func _unhandled_input(event: InputEvent) -> void:
	if event.is_action_pressed("confirm"):
		trigger_celadon_city_arrival_scene()
	if event.is_action_pressed("cancel"):
		return_to_celadon_underground_path()


func _build_city() -> void:
	var grass := ColorRect.new()
	grass.color = Color("79b05f")
	grass.set_anchors_preset(Control.PRESET_FULL_RECT)
	add_child(grass)

	var plaza := ColorRect.new()
	plaza.color = Color("d8bd79")
	plaza.anchor_left = 0.08
	plaza.anchor_top = 0.34
	plaza.anchor_right = 0.92
	plaza.anchor_bottom = 0.78
	add_child(plaza)

	var game_corner := ColorRect.new()
	game_corner.color = Color("3b2c3f")
	game_corner.anchor_left = 0.58
	game_corner.anchor_top = 0.18
	game_corner.anchor_right = 0.86
	game_corner.anchor_bottom = 0.36
	add_child(game_corner)

	var gym := ColorRect.new()
	gym.color = Color("6fb05f")
	gym.anchor_left = 0.12
	gym.anchor_top = 0.18
	gym.anchor_right = 0.38
	gym.anchor_bottom = 0.36
	add_child(gym)

	var moonlight_ad := ColorRect.new()
	moonlight_ad.color = Color("6e65b8")
	moonlight_ad.anchor_left = 0.42
	moonlight_ad.anchor_top = 0.42
	moonlight_ad.anchor_right = 0.56
	moonlight_ad.anchor_bottom = 0.58
	add_child(moonlight_ad)

	var mart := ColorRect.new()
	mart.color = Color("4b79ce")
	mart.anchor_left = 0.12
	mart.anchor_top = 0.56
	mart.anchor_right = 0.34
	mart.anchor_bottom = 0.72
	add_child(mart)

	var header := Label.new()
	header.text = "Celadon City - Arrival"
	header.anchor_left = 0.04
	header.anchor_top = 0.04
	header.anchor_right = 0.78
	header.anchor_bottom = 0.1
	header.add_theme_font_size_override("font_size", 32)
	header.add_theme_color_override("font_color", Color("14243d"))
	add_child(header)

	var game_corner_label := Label.new()
	game_corner_label.text = "Game Corner exterior"
	game_corner_label.anchor_left = 0.59
	game_corner_label.anchor_top = 0.24
	game_corner_label.anchor_right = 0.84
	game_corner_label.anchor_bottom = 0.3
	game_corner_label.add_theme_font_size_override("font_size", 18)
	game_corner_label.add_theme_color_override("font_color", Color("f8eada"))
	add_child(game_corner_label)

	var gym_label := Label.new()
	gym_label.text = "Erika / Celadon Gym"
	gym_label.anchor_left = 0.14
	gym_label.anchor_top = 0.24
	gym_label.anchor_right = 0.36
	gym_label.anchor_bottom = 0.3
	gym_label.add_theme_font_size_override("font_size", 18)
	gym_label.add_theme_color_override("font_color", Color("103516"))
	add_child(gym_label)

	var ad_label := Label.new()
	ad_label.text = "Moonlight dream ad"
	ad_label.anchor_left = 0.38
	ad_label.anchor_top = 0.59
	ad_label.anchor_right = 0.62
	ad_label.anchor_bottom = 0.65
	ad_label.add_theme_font_size_override("font_size", 16)
	ad_label.add_theme_color_override("font_color", Color("14243d"))
	add_child(ad_label)

	dialogue_label = Label.new()
	dialogue_label.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	dialogue_label.anchor_left = 0.06
	dialogue_label.anchor_top = 0.82
	dialogue_label.anchor_right = 0.94
	dialogue_label.anchor_bottom = 0.98
	dialogue_label.add_theme_font_size_override("font_size", 20)
	dialogue_label.add_theme_color_override("font_color", Color("14243d"))
	add_child(dialogue_label)


func trigger_celadon_city_arrival_scene() -> void:
	if save_state:
		save_state.record_celadon_city_arrival_scene()
	dialogue_label.text = "Red: Celadon is bigger than it looks. Bill says the Silph Scope signal is bouncing off the Game Corner exterior, Rocket is hiding in plain sight, Team Moonlight bought dream ads across the plaza, and Erika's gym is watching how we move before we go inside."


func return_to_celadon_underground_path() -> void:
	emit_signal("go_to_celadon_underground_path")


func _update_intro_dialogue() -> void:
	dialogue_label.text = "Red: Welcome to Celadon. Press Z/Enter to scout the Game Corner exterior, Bill's Silph Scope signal, Rocket's public front, Team Moonlight's city ad, and Erika's gym tease. Press X/Esc to return to the Underground Path."
