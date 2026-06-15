extends Control

signal go_to_rocket_hideout_entry
signal go_to_rocket_hideout_b2f

var save_state
var dialogue_label: Label


func _ready() -> void:
	_build_b1f()
	if save_state:
		save_state.enter_celadon_rocket_hideout_b1f()
	_update_intro_dialogue()


func _unhandled_input(event: InputEvent) -> void:
	if event.is_action_pressed("confirm"):
		trigger_rocket_hideout_b1f_scene()
	if event.is_action_pressed("ui_right"):
		trigger_rocket_hideout_b2f_entry()
	if event.is_action_pressed("cancel"):
		return_to_rocket_hideout_entry()


func _build_b1f() -> void:
	var floor := ColorRect.new()
	floor.color = Color("2b2730")
	floor.set_anchors_preset(Control.PRESET_FULL_RECT)
	add_child(floor)

	var upper_walkway := ColorRect.new()
	upper_walkway.color = Color("514b57")
	upper_walkway.anchor_left = 0.08
	upper_walkway.anchor_top = 0.18
	upper_walkway.anchor_right = 0.92
	upper_walkway.anchor_bottom = 0.3
	add_child(upper_walkway)

	var lower_walkway := ColorRect.new()
	lower_walkway.color = Color("514b57")
	lower_walkway.anchor_left = 0.08
	lower_walkway.anchor_top = 0.58
	lower_walkway.anchor_right = 0.92
	lower_walkway.anchor_bottom = 0.7
	add_child(lower_walkway)

	var spinner_lane := ColorRect.new()
	spinner_lane.color = Color("6f5d83")
	spinner_lane.anchor_left = 0.18
	spinner_lane.anchor_top = 0.32
	spinner_lane.anchor_right = 0.82
	spinner_lane.anchor_bottom = 0.56
	add_child(spinner_lane)

	var machine_bank := ColorRect.new()
	machine_bank.color = Color("315f78")
	machine_bank.anchor_left = 0.1
	machine_bank.anchor_top = 0.74
	machine_bank.anchor_right = 0.34
	machine_bank.anchor_bottom = 0.88
	add_child(machine_bank)

	var gold_dust_cache := ColorRect.new()
	gold_dust_cache.color = Color("b88a2a")
	gold_dust_cache.anchor_left = 0.66
	gold_dust_cache.anchor_top = 0.74
	gold_dust_cache.anchor_right = 0.88
	gold_dust_cache.anchor_bottom = 0.88
	add_child(gold_dust_cache)

	var moonlight_leak := ColorRect.new()
	moonlight_leak.color = Color("6d65bf")
	moonlight_leak.anchor_left = 0.42
	moonlight_leak.anchor_top = 0.73
	moonlight_leak.anchor_right = 0.58
	moonlight_leak.anchor_bottom = 0.9
	add_child(moonlight_leak)

	var header := Label.new()
	header.text = "Celadon Rocket Hideout - B1F"
	header.anchor_left = 0.04
	header.anchor_top = 0.04
	header.anchor_right = 0.9
	header.anchor_bottom = 0.1
	header.add_theme_font_size_override("font_size", 32)
	header.add_theme_color_override("font_color", Color("f3e8df"))
	add_child(header)

	var spinner_label := Label.new()
	spinner_label.text = "Rocket spinner maze"
	spinner_label.anchor_left = 0.34
	spinner_label.anchor_top = 0.39
	spinner_label.anchor_right = 0.7
	spinner_label.anchor_bottom = 0.45
	spinner_label.add_theme_font_size_override("font_size", 18)
	spinner_label.add_theme_color_override("font_color", Color("f3e8df"))
	add_child(spinner_label)

	var machine_label := Label.new()
	machine_label.text = "Silph Scope machine trace"
	machine_label.anchor_left = 0.08
	machine_label.anchor_top = 0.89
	machine_label.anchor_right = 0.4
	machine_label.anchor_bottom = 0.95
	machine_label.add_theme_font_size_override("font_size", 16)
	machine_label.add_theme_color_override("font_color", Color("f3e8df"))
	add_child(machine_label)

	var gold_label := Label.new()
	gold_label.text = "Gold Dust cache"
	gold_label.anchor_left = 0.66
	gold_label.anchor_top = 0.89
	gold_label.anchor_right = 0.9
	gold_label.anchor_bottom = 0.95
	gold_label.add_theme_font_size_override("font_size", 16)
	gold_label.add_theme_color_override("font_color", Color("f3e8df"))
	add_child(gold_label)

	var moonlight_label := Label.new()
	moonlight_label.text = "Moonlight signal bleed"
	moonlight_label.anchor_left = 0.38
	moonlight_label.anchor_top = 0.67
	moonlight_label.anchor_right = 0.64
	moonlight_label.anchor_bottom = 0.73
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


func trigger_rocket_hideout_b1f_scene() -> void:
	if save_state:
		save_state.record_celadon_rocket_hideout_b1f_scene()
	dialogue_label.text = "Red: B1F is a Rocket spinner maze. Bill says the Silph Scope machine trace runs below us, Gold Dust already slipped in for a cache, Team Moonlight signal bleed is warping the tiles, and the Lift Key trail points down to B2F."


func trigger_rocket_hideout_b2f_entry() -> void:
	if save_state == null or not save_state.story_flags.get("rocket_hideout_b2f_path_unlocked", false):
		dialogue_label.text = "Red: We map the spinner maze, Silph Scope machine trace, Gold Dust cache, Moonlight signal bleed, and Lift Key trail before pushing to B2F."
		return
	dialogue_label.text = "Red: B2F is the next hideout route. Stay close; Rocket wants us separated before the Lift Key."
	emit_signal("go_to_rocket_hideout_b2f")


func return_to_rocket_hideout_entry() -> void:
	emit_signal("go_to_rocket_hideout_entry")


func _update_intro_dialogue() -> void:
	dialogue_label.text = "Red: This is Rocket Hideout B1F. Press Z/Enter to map the spinner maze, Bill's Silph Scope machine trace, Gold Dust infiltration, Team Moonlight signal bleed, and the Lift Key trail. Press Right for the future B2F path or X/Esc to return."
