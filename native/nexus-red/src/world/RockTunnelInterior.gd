extends Control

signal go_to_route_9_rock_tunnel_approach
signal go_to_lavender_outskirts

var save_state
var dialogue_label: Label


func _ready() -> void:
	_build_tunnel()
	if save_state:
		save_state.enter_rock_tunnel_interior()
	_update_intro_dialogue()


func _unhandled_input(event: InputEvent) -> void:
	if event.is_action_pressed("confirm"):
		trigger_rock_tunnel_interior_scene()
	if event.is_action_pressed("ui_right"):
		trigger_lavender_exit()
	if event.is_action_pressed("cancel"):
		return_to_route_9_rock_tunnel_approach()


func _build_tunnel() -> void:
	var darkness := ColorRect.new()
	darkness.color = Color("19171f")
	darkness.set_anchors_preset(Control.PRESET_FULL_RECT)
	add_child(darkness)

	var main_path := ColorRect.new()
	main_path.color = Color("4b443d")
	main_path.anchor_left = 0.08
	main_path.anchor_top = 0.48
	main_path.anchor_right = 0.92
	main_path.anchor_bottom = 0.64
	add_child(main_path)

	var upper_path := ColorRect.new()
	upper_path.color = Color("36313b")
	upper_path.anchor_left = 0.22
	upper_path.anchor_top = 0.2
	upper_path.anchor_right = 0.58
	upper_path.anchor_bottom = 0.34
	add_child(upper_path)

	var moonlight_signal := ColorRect.new()
	moonlight_signal.color = Color("6b65ad")
	moonlight_signal.anchor_left = 0.6
	moonlight_signal.anchor_top = 0.18
	moonlight_signal.anchor_right = 0.78
	moonlight_signal.anchor_bottom = 0.34
	add_child(moonlight_signal)

	var rocket_cache := ColorRect.new()
	rocket_cache.color = Color("2b2525")
	rocket_cache.anchor_left = 0.16
	rocket_cache.anchor_top = 0.66
	rocket_cache.anchor_right = 0.36
	rocket_cache.anchor_bottom = 0.78
	add_child(rocket_cache)

	var lavender_exit := ColorRect.new()
	lavender_exit.color = Color("8d7db6")
	lavender_exit.anchor_left = 0.76
	lavender_exit.anchor_top = 0.5
	lavender_exit.anchor_right = 0.94
	lavender_exit.anchor_bottom = 0.72
	add_child(lavender_exit)

	var header := Label.new()
	header.text = "Rock Tunnel - Interior"
	header.anchor_left = 0.04
	header.anchor_top = 0.04
	header.anchor_right = 0.76
	header.anchor_bottom = 0.1
	header.add_theme_font_size_override("font_size", 32)
	header.add_theme_color_override("font_color", Color("f0e6d2"))
	add_child(header)

	var red_label := Label.new()
	red_label.text = "Red"
	red_label.anchor_left = 0.1
	red_label.anchor_top = 0.42
	red_label.anchor_right = 0.22
	red_label.anchor_bottom = 0.48
	red_label.add_theme_font_size_override("font_size", 18)
	red_label.add_theme_color_override("font_color", Color("f7e6d0"))
	add_child(red_label)

	var moonlight_label := Label.new()
	moonlight_label.text = "Moonlight pressure"
	moonlight_label.anchor_left = 0.6
	moonlight_label.anchor_top = 0.35
	moonlight_label.anchor_right = 0.84
	moonlight_label.anchor_bottom = 0.41
	moonlight_label.add_theme_font_size_override("font_size", 16)
	moonlight_label.add_theme_color_override("font_color", Color("f2eaff"))
	add_child(moonlight_label)

	var cache_label := Label.new()
	cache_label.text = "Rocket dark cache"
	cache_label.anchor_left = 0.16
	cache_label.anchor_top = 0.79
	cache_label.anchor_right = 0.42
	cache_label.anchor_bottom = 0.85
	cache_label.add_theme_font_size_override("font_size", 16)
	cache_label.add_theme_color_override("font_color", Color("f0d8d8"))
	add_child(cache_label)

	var exit_label := Label.new()
	exit_label.text = "Lavender echo"
	exit_label.anchor_left = 0.76
	exit_label.anchor_top = 0.73
	exit_label.anchor_right = 0.96
	exit_label.anchor_bottom = 0.79
	exit_label.add_theme_font_size_override("font_size", 16)
	exit_label.add_theme_color_override("font_color", Color("f3eaff"))
	add_child(exit_label)

	dialogue_label = Label.new()
	dialogue_label.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	dialogue_label.anchor_left = 0.06
	dialogue_label.anchor_top = 0.84
	dialogue_label.anchor_right = 0.94
	dialogue_label.anchor_bottom = 0.98
	dialogue_label.add_theme_font_size_override("font_size", 20)
	dialogue_label.add_theme_color_override("font_color", Color("f0e6d2"))
	add_child(dialogue_label)


func trigger_rock_tunnel_interior_scene() -> void:
	if save_state:
		save_state.record_rock_tunnel_interior_scene()
	dialogue_label.text = "Red: Rock Tunnel is dark, but I am with you. Bill says the Echo Flute trace is bouncing toward Lavender, Team Moonlight is pressuring the cave with sleep signals, and Rocket hid a dark cache near the exit. We need a Flash Lantern plan before pushing deeper."


func return_to_route_9_rock_tunnel_approach() -> void:
	emit_signal("go_to_route_9_rock_tunnel_approach")


func trigger_lavender_exit() -> void:
	if save_state and not bool(save_state.story_flags.get("lavender_exit_path_unlocked", false)):
		dialogue_label.text = "Red: Lavender is through this exit, but we need to inspect Rock Tunnel's Echo Flute trace, Team Moonlight pressure, and Rocket cache before we step out."
		return
	dialogue_label.text = "Red: Lavender is ahead. Bill's Echo Flute trace is pulling straight toward Pokemon Tower."
	emit_signal("go_to_lavender_outskirts")


func _update_intro_dialogue() -> void:
	dialogue_label.text = "Red: This is Rock Tunnel. Press Z/Enter to inspect Bill's Lavender Echo Flute trace, Team Moonlight's pressure, Rocket's cache, and the Flash Lantern problem, Right for Lavender, or X/Esc to return to Route 9."
