extends Control

signal encounter_finished(result)

const CaptureRules := preload("res://src/encounter/CaptureRules.gd")

var save_state
var encounter_data: Dictionary = {}
var dialogue_label: Label
var wild_status_label: Label
var wild_hp := 0
var wild_max_hp := 0
var action_count := 0
var capture_attempts := 0
var capture_rules := CaptureRules.new()


func _ready() -> void:
	if encounter_data.is_empty() and save_state:
		encounter_data = save_state.active_encounter_data
	_initialize_loop_state()
	_build_encounter_screen()


func _unhandled_input(event: InputEvent) -> void:
	if event.is_action_pressed("confirm"):
		if action_count == 0:
			attack_wild()
		else:
			attempt_capture()
	if event.is_action_pressed("cancel"):
		run_from_encounter()


func _initialize_loop_state() -> void:
	wild_max_hp = capture_rules.calculate_max_hp(encounter_data)
	wild_hp = wild_max_hp
	action_count = 0
	capture_attempts = 0


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

	wild_status_label = Label.new()
	wild_status_label.text = _wild_status_text()
	wild_status_label.anchor_left = 0.58
	wild_status_label.anchor_top = 0.34
	wild_status_label.anchor_right = 0.92
	wild_status_label.anchor_bottom = 0.4
	wild_status_label.add_theme_font_size_override("font_size", 18)
	add_child(wild_status_label)

	dialogue_label = Label.new()
	dialogue_label.text = "Red: Keep your hand steady. Press Z or Enter to weaken it first, then press again to throw. X/Esc runs."
	dialogue_label.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	dialogue_label.anchor_left = 0.06
	dialogue_label.anchor_top = 0.82
	dialogue_label.anchor_right = 0.94
	dialogue_label.anchor_bottom = 0.95
	dialogue_label.add_theme_font_size_override("font_size", 20)
	dialogue_label.add_theme_color_override("font_color", Color("14243d"))
	add_child(dialogue_label)


func attack_wild() -> void:
	var damage := capture_rules.calculate_attack_damage(_player_starter(), encounter_data)
	wild_hp = max(1, wild_hp - damage)
	action_count += 1
	_update_wild_status()
	if dialogue_label:
		dialogue_label.text = "Red: Good. You lowered %s to %d/%d HP. Now throw clean before it slips away." % [_wild_species(), wild_hp, wild_max_hp]


func attempt_capture() -> void:
	capture_attempts += 1
	var result := capture_rules.capture_result(wild_hp, wild_max_hp)
	if result == CaptureRules.CATCH_SUCCESS:
		if dialogue_label:
			dialogue_label.text = "Red: That's it. %s is caught. First field capture logged." % _wild_species()
		emit_signal("encounter_finished", result)
		return
	if dialogue_label:
		dialogue_label.text = "Red: Not yet. Weaken it first so the capture sticks."


func finish_placeholder_catch() -> void:
	attempt_capture()


func finish_placeholder_run() -> void:
	run_from_encounter()


func run_from_encounter() -> void:
	emit_signal("encounter_finished", "placeholder_run")


func _player_starter() -> String:
	if save_state and save_state.player_starter != "":
		return save_state.player_starter
	return "first partner"


func _wild_species() -> String:
	return str(encounter_data.get("species", "creature"))


func _wild_level() -> int:
	return int(encounter_data.get("level", 1))


func _wild_status_text() -> String:
	return "%s HP: %d/%d" % [_wild_species(), wild_hp, wild_max_hp]


func _update_wild_status() -> void:
	if wild_status_label:
		wild_status_label.text = _wild_status_text()
