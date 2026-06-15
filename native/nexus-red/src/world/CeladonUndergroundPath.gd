extends Control

signal go_to_route_8_celadon_road
signal go_to_celadon_city

var save_state
var dialogue_label: Label


func _ready() -> void:
	_build_path()
	if save_state:
		save_state.enter_celadon_underground_path()
	_update_intro_dialogue()


func _unhandled_input(event: InputEvent) -> void:
	if event.is_action_pressed("confirm"):
		trigger_celadon_underground_path_scene()
	if event.is_action_pressed("ui_right"):
		trigger_celadon_city_entry()
	if event.is_action_pressed("cancel"):
		return_to_route_8_celadon_road()


func _build_path() -> void:
	var floor := ColorRect.new()
	floor.color = Color("4c4033")
	floor.set_anchors_preset(Control.PRESET_FULL_RECT)
	add_child(floor)

	var tunnel := ColorRect.new()
	tunnel.color = Color("8a7355")
	tunnel.anchor_left = 0.08
	tunnel.anchor_top = 0.46
	tunnel.anchor_right = 0.92
	tunnel.anchor_bottom = 0.62
	add_child(tunnel)

	var east_stairs := ColorRect.new()
	east_stairs.color = Color("5a4735")
	east_stairs.anchor_left = 0.08
	east_stairs.anchor_top = 0.24
	east_stairs.anchor_right = 0.24
	east_stairs.anchor_bottom = 0.46
	add_child(east_stairs)

	var celadon_stairs := ColorRect.new()
	celadon_stairs.color = Color("6b8252")
	celadon_stairs.anchor_left = 0.76
	celadon_stairs.anchor_top = 0.24
	celadon_stairs.anchor_right = 0.92
	celadon_stairs.anchor_bottom = 0.46
	add_child(celadon_stairs)

	var rocket_runner := ColorRect.new()
	rocket_runner.color = Color("2d2529")
	rocket_runner.anchor_left = 0.58
	rocket_runner.anchor_top = 0.64
	rocket_runner.anchor_right = 0.72
	rocket_runner.anchor_bottom = 0.76
	add_child(rocket_runner)

	var dream_poster := ColorRect.new()
	dream_poster.color = Color("7767b5")
	dream_poster.anchor_left = 0.32
	dream_poster.anchor_top = 0.24
	dream_poster.anchor_right = 0.48
	dream_poster.anchor_bottom = 0.42
	add_child(dream_poster)

	var header := Label.new()
	header.text = "Celadon Underground Path"
	header.anchor_left = 0.04
	header.anchor_top = 0.04
	header.anchor_right = 0.84
	header.anchor_bottom = 0.1
	header.add_theme_font_size_override("font_size", 32)
	header.add_theme_color_override("font_color", Color("f4ead9"))
	add_child(header)

	var poster_label := Label.new()
	poster_label.text = "Moonlight dream poster"
	poster_label.anchor_left = 0.28
	poster_label.anchor_top = 0.2
	poster_label.anchor_right = 0.58
	poster_label.anchor_bottom = 0.26
	poster_label.add_theme_font_size_override("font_size", 16)
	poster_label.add_theme_color_override("font_color", Color("f4ead9"))
	add_child(poster_label)

	var runner_label := Label.new()
	runner_label.text = "Rocket smuggler route"
	runner_label.anchor_left = 0.54
	runner_label.anchor_top = 0.77
	runner_label.anchor_right = 0.86
	runner_label.anchor_bottom = 0.83
	runner_label.add_theme_font_size_override("font_size", 16)
	runner_label.add_theme_color_override("font_color", Color("f4ead9"))
	add_child(runner_label)

	var city_label := Label.new()
	city_label.text = "Celadon City exit"
	city_label.anchor_left = 0.72
	city_label.anchor_top = 0.18
	city_label.anchor_right = 0.94
	city_label.anchor_bottom = 0.24
	city_label.add_theme_font_size_override("font_size", 16)
	city_label.add_theme_color_override("font_color", Color("f4ead9"))
	add_child(city_label)

	dialogue_label = Label.new()
	dialogue_label.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	dialogue_label.anchor_left = 0.06
	dialogue_label.anchor_top = 0.86
	dialogue_label.anchor_right = 0.94
	dialogue_label.anchor_bottom = 0.98
	dialogue_label.add_theme_font_size_override("font_size", 20)
	dialogue_label.add_theme_color_override("font_color", Color("f4ead9"))
	add_child(dialogue_label)


func trigger_celadon_underground_path_scene() -> void:
	if save_state:
		save_state.record_celadon_underground_path_scene()
	dialogue_label.text = "Red: Celadon is above us. Bill says the Silph Scope signal is strongest near the Game Corner, Rocket is using this Underground Path for smugglers, and Team Moonlight planted a dream poster here to keep the Lavender pressure connected."


func return_to_route_8_celadon_road() -> void:
	emit_signal("go_to_route_8_celadon_road")


func trigger_celadon_city_entry() -> void:
	if save_state == null or not save_state.story_flags.get("celadon_city_arrival_unlocked", false):
		dialogue_label.text = "Red: Celadon City is right above us, but we need Bill's Game Corner signal trace before we step into Rocket's public front."
		return
	dialogue_label.text = "Red: Celadon City is open. Stay close; the Game Corner looks public, and that is exactly why Rocket chose it."
	emit_signal("go_to_celadon_city")


func _update_intro_dialogue() -> void:
	dialogue_label.text = "Red: This Underground Path connects Route 8 to Celadon without breaking the journey. Press Z/Enter to trace Bill's Game Corner signal, Rocket's smuggler route, Team Moonlight's dream poster, and the Silph Scope lead. Press Right for Celadon City or X/Esc to return to Route 8."
