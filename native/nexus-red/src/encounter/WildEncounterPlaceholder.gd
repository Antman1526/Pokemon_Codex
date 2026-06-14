extends Control

signal encounter_finished(result)

var save_state
var encounter_data: Dictionary = {}
var dialogue_label: Label


func _ready() -> void:
	if encounter_data.is_empty() and save_state:
		encounter_data = save_state.active_encounter_data
	_build_encounter_screen()


func _unhandled_input(event: InputEvent) -> void:
	if event.is_action_pressed("confirm"):
		finish_placeholder_catch()
	if event.is_action_pressed("cancel"):
		finish_placeholder_run()


func _build_encounter_screen() -> void:
	var backdrop := ColorRect.new()
	backdrop.color = Color("7fcf74")
	backdrop.set_anchors_preset(Control.PRESET_FULL_RECT)
	add_child(backdrop)

	var grass_band := ColorRect.new()
	grass_band.color = Color("3f8d47")
	grass_band.anchor_left = 0.0
	grass_band.anchor_top = 0.48
	grass_band.anchor_right = 1.0
	grass_band.anchor_bottom = 0.78
	add_child(grass_band)

	var player_side := ColorRect.new()
	player_side.color = Color("d6b36f")
	player_side.anchor_left = 0.06
	player_side.anchor_top = 0.62
	player_side.anchor_right = 0.44
	player_side.anchor_bottom = 0.82
	add_child(player_side)

	var wild_side := ColorRect.new()
	wild_side.color = Color("f5efe4")
	wild_side.anchor_left = 0.56
	wild_side.anchor_top = 0.2
	wild_side.anchor_right = 0.94
	wild_side.anchor_bottom = 0.42
	add_child(wild_side)

	var title := Label.new()
	title.text = "Route 1 wild encounter placeholder"
	title.anchor_left = 0.05
	title.anchor_top = 0.04
	title.anchor_right = 0.95
	title.anchor_bottom = 0.12
	title.add_theme_font_size_override("font_size", 32)
	title.add_theme_color_override("font_color", Color("14243d"))
	add_child(title)

	var player_label := Label.new()
	player_label.text = "Antman keeps %s ready." % _player_starter()
	player_label.anchor_left = 0.08
	player_label.anchor_top = 0.68
	player_label.anchor_right = 0.42
	player_label.anchor_bottom = 0.76
	player_label.add_theme_font_size_override("font_size", 22)
	add_child(player_label)

	var wild_label := Label.new()
	wild_label.text = "Wild %s Lv. %d appeared!" % [_wild_species(), _wild_level()]
	wild_label.anchor_left = 0.58
	wild_label.anchor_top = 0.26
	wild_label.anchor_right = 0.92
	wild_label.anchor_bottom = 0.34
	wild_label.add_theme_font_size_override("font_size", 22)
	add_child(wild_label)

	dialogue_label = Label.new()
	dialogue_label.text = "Red: Keep your hand steady. Press Z or Enter to record a placeholder catch, or X/Esc to run."
	dialogue_label.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	dialogue_label.anchor_left = 0.06
	dialogue_label.anchor_top = 0.82
	dialogue_label.anchor_right = 0.94
	dialogue_label.anchor_bottom = 0.95
	dialogue_label.add_theme_font_size_override("font_size", 20)
	dialogue_label.add_theme_color_override("font_color", Color("14243d"))
	add_child(dialogue_label)


func finish_placeholder_catch() -> void:
	emit_signal("encounter_finished", "placeholder_catch")


func finish_placeholder_run() -> void:
	emit_signal("encounter_finished", "placeholder_run")


func _player_starter() -> String:
	if save_state and save_state.player_starter != "":
		return save_state.player_starter
	return "first partner"


func _wild_species() -> String:
	return str(encounter_data.get("species", "creature"))


func _wild_level() -> int:
	return int(encounter_data.get("level", 1))
