extends Control

signal go_to_celadon_city
signal go_to_game_corner_hideout_entry
signal start_battle_placeholder(battle_id)

var save_state
var dialogue_label: Label


func _ready() -> void:
	_build_exterior()
	if save_state:
		save_state.enter_celadon_game_corner_exterior()
	_update_intro_dialogue()


func _unhandled_input(event: InputEvent) -> void:
	if event.is_action_pressed("confirm"):
		trigger_game_corner_exterior_scene()
	if event.is_action_pressed("ui_down"):
		trigger_game_corner_guard_battle()
	if event.is_action_pressed("ui_right"):
		trigger_game_corner_hideout_entry()
	if event.is_action_pressed("cancel"):
		return_to_celadon_city()


func _build_exterior() -> void:
	var street := ColorRect.new()
	street.color = Color("c9ad73")
	street.set_anchors_preset(Control.PRESET_FULL_RECT)
	add_child(street)

	var building := ColorRect.new()
	building.color = Color("3a293f")
	building.anchor_left = 0.18
	building.anchor_top = 0.18
	building.anchor_right = 0.82
	building.anchor_bottom = 0.54
	add_child(building)

	var sign := ColorRect.new()
	sign.color = Color("d6bd4d")
	sign.anchor_left = 0.34
	sign.anchor_top = 0.22
	sign.anchor_right = 0.66
	sign.anchor_bottom = 0.32
	add_child(sign)

	var guard := ColorRect.new()
	guard.color = Color("222027")
	guard.anchor_left = 0.66
	guard.anchor_top = 0.56
	guard.anchor_right = 0.72
	guard.anchor_bottom = 0.68
	add_child(guard)

	var poster := ColorRect.new()
	poster.color = Color("7064b8")
	poster.anchor_left = 0.16
	poster.anchor_top = 0.62
	poster.anchor_right = 0.3
	poster.anchor_bottom = 0.76
	add_child(poster)

	var header := Label.new()
	header.text = "Celadon Game Corner - Exterior"
	header.anchor_left = 0.04
	header.anchor_top = 0.04
	header.anchor_right = 0.82
	header.anchor_bottom = 0.1
	header.add_theme_font_size_override("font_size", 32)
	header.add_theme_color_override("font_color", Color("241a2d"))
	add_child(header)

	var sign_label := Label.new()
	sign_label.text = "Game Corner"
	sign_label.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	sign_label.anchor_left = 0.34
	sign_label.anchor_top = 0.24
	sign_label.anchor_right = 0.66
	sign_label.anchor_bottom = 0.3
	sign_label.add_theme_font_size_override("font_size", 22)
	sign_label.add_theme_color_override("font_color", Color("241a2d"))
	add_child(sign_label)

	var guard_label := Label.new()
	guard_label.text = "Rocket floor guard"
	guard_label.anchor_left = 0.58
	guard_label.anchor_top = 0.69
	guard_label.anchor_right = 0.86
	guard_label.anchor_bottom = 0.75
	guard_label.add_theme_font_size_override("font_size", 18)
	guard_label.add_theme_color_override("font_color", Color("241a2d"))
	add_child(guard_label)

	var poster_label := Label.new()
	poster_label.text = "Moonlight sleep coin"
	poster_label.anchor_left = 0.12
	poster_label.anchor_top = 0.77
	poster_label.anchor_right = 0.36
	poster_label.anchor_bottom = 0.83
	poster_label.add_theme_font_size_override("font_size", 16)
	poster_label.add_theme_color_override("font_color", Color("241a2d"))
	add_child(poster_label)

	dialogue_label = Label.new()
	dialogue_label.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	dialogue_label.anchor_left = 0.06
	dialogue_label.anchor_top = 0.84
	dialogue_label.anchor_right = 0.94
	dialogue_label.anchor_bottom = 0.98
	dialogue_label.add_theme_font_size_override("font_size", 20)
	dialogue_label.add_theme_color_override("font_color", Color("241a2d"))
	add_child(dialogue_label)


func trigger_game_corner_exterior_scene() -> void:
	if save_state:
		save_state.record_celadon_game_corner_exterior_scene()
	dialogue_label.text = "Red: The Game Corner guard keeps watching the poster, not the door. Bill says the Coin Case is echoing the Silph Scope signal, Rocket wired the front to misdirect trainers, and Team Moonlight's sleep coin ad is trying to make everyone ignore the pattern."


func trigger_game_corner_guard_battle() -> void:
	if save_state == null or not save_state.story_flags.get("game_corner_guard_battle_unlocked", false):
		dialogue_label.text = "Red: Press the guard too early and Rocket will scatter. Check the Game Corner front with Bill's signal first."
		return
	if save_state:
		save_state.start_battle_placeholder("rocket_game_corner_guard")
	dialogue_label.text = "Rocket Guard: No kids past the games. Red: Then we do this the loud way."
	emit_signal("start_battle_placeholder", "rocket_game_corner_guard")


func trigger_game_corner_hideout_entry() -> void:
	if save_state == null or not save_state.story_flags.get("game_corner_hideout_entry_unlocked", false):
		dialogue_label.text = "Red: The hideout switch is still hidden. Beat the guard first and watch what he protects."
		return
	dialogue_label.text = "Red: The poster switch lead is confirmed. The Rocket Hideout entrance is the next step, but we map it before going deep."
	emit_signal("go_to_game_corner_hideout_entry")


func return_to_celadon_city() -> void:
	emit_signal("go_to_celadon_city")


func _update_intro_dialogue() -> void:
	dialogue_label.text = "Red: This is the Game Corner exterior. Press Z/Enter to inspect the Rocket guard, Bill's Coin Case signal, Team Moonlight's sleep coin ad, and the Silph Scope echo. Press Down to challenge the guard, Right for the hideout-entry lead, or X/Esc to return to Celadon."
