extends Control

signal go_to_pokemon_tower_fuji_rescue
signal start_wild_encounter(encounter_data)

const SNORLAX_STATIC_PATH := "res://content/encounters/route_12_snorlax_static.json"

var save_state
var dialogue_label: Label
var snorlax_encounter: Dictionary = {}


func _ready() -> void:
	snorlax_encounter = _load_json(SNORLAX_STATIC_PATH)
	_build_route_12()
	if save_state:
		save_state.enter_route_12_snorlax_wake()
	_update_intro_dialogue()


func _unhandled_input(event: InputEvent) -> void:
	if event.is_action_pressed("confirm"):
		trigger_route_12_snorlax_wake_scene()
	if event.is_action_pressed("ui_down"):
		trigger_snorlax_static_encounter()
	if event.is_action_pressed("cancel"):
		return_to_pokemon_tower_fuji_rescue()


func _build_route_12() -> void:
	var road := ColorRect.new()
	road.color = Color("6f9a74")
	road.set_anchors_preset(Control.PRESET_FULL_RECT)
	add_child(road)

	var boardwalk := ColorRect.new()
	boardwalk.color = Color("b89964")
	boardwalk.anchor_left = 0.08
	boardwalk.anchor_top = 0.48
	boardwalk.anchor_right = 0.92
	boardwalk.anchor_bottom = 0.66
	add_child(boardwalk)

	var water := ColorRect.new()
	water.color = Color("5fa3c6")
	water.anchor_left = 0.08
	water.anchor_top = 0.72
	water.anchor_right = 0.92
	water.anchor_bottom = 0.92
	add_child(water)

	var snorlax_block := ColorRect.new()
	snorlax_block.color = Color("33434f")
	snorlax_block.anchor_left = 0.4
	snorlax_block.anchor_top = 0.22
	snorlax_block.anchor_right = 0.62
	snorlax_block.anchor_bottom = 0.44
	add_child(snorlax_block)

	var red_guard := ColorRect.new()
	red_guard.color = Color("b92732")
	red_guard.anchor_left = 0.18
	red_guard.anchor_top = 0.28
	red_guard.anchor_right = 0.3
	red_guard.anchor_bottom = 0.44
	add_child(red_guard)

	var moonlight_echo := ColorRect.new()
	moonlight_echo.color = Color("7562ba")
	moonlight_echo.anchor_left = 0.7
	moonlight_echo.anchor_top = 0.24
	moonlight_echo.anchor_right = 0.86
	moonlight_echo.anchor_bottom = 0.42
	add_child(moonlight_echo)

	var flute_signal := ColorRect.new()
	flute_signal.color = Color("dce8ec")
	flute_signal.anchor_left = 0.18
	flute_signal.anchor_top = 0.72
	flute_signal.anchor_right = 0.34
	flute_signal.anchor_bottom = 0.88
	add_child(flute_signal)

	var header := Label.new()
	header.text = "Route 12 - Snorlax Wake"
	header.anchor_left = 0.04
	header.anchor_top = 0.04
	header.anchor_right = 0.92
	header.anchor_bottom = 0.1
	header.add_theme_font_size_override("font_size", 32)
	header.add_theme_color_override("font_color", Color("14243d"))
	add_child(header)

	var snorlax_label := Label.new()
	snorlax_label.text = "Snorlax roadblock"
	snorlax_label.anchor_left = 0.38
	snorlax_label.anchor_top = 0.45
	snorlax_label.anchor_right = 0.66
	snorlax_label.anchor_bottom = 0.52
	snorlax_label.add_theme_font_size_override("font_size", 16)
	snorlax_label.add_theme_color_override("font_color", Color("14243d"))
	add_child(snorlax_label)

	var red_label := Label.new()
	red_label.text = "Red guards the road"
	red_label.anchor_left = 0.12
	red_label.anchor_top = 0.45
	red_label.anchor_right = 0.36
	red_label.anchor_bottom = 0.52
	red_label.add_theme_font_size_override("font_size", 16)
	red_label.add_theme_color_override("font_color", Color("14243d"))
	add_child(red_label)

	var moonlight_label := Label.new()
	moonlight_label.text = "Moonlight sleep echo"
	moonlight_label.anchor_left = 0.66
	moonlight_label.anchor_top = 0.43
	moonlight_label.anchor_right = 0.9
	moonlight_label.anchor_bottom = 0.5
	moonlight_label.add_theme_font_size_override("font_size", 16)
	moonlight_label.add_theme_color_override("font_color", Color("14243d"))
	add_child(moonlight_label)

	var flute_label := Label.new()
	flute_label.text = "Poke Flute signal"
	flute_label.anchor_left = 0.14
	flute_label.anchor_top = 0.89
	flute_label.anchor_right = 0.38
	flute_label.anchor_bottom = 0.96
	flute_label.add_theme_font_size_override("font_size", 16)
	flute_label.add_theme_color_override("font_color", Color("14243d"))
	add_child(flute_label)

	dialogue_label = Label.new()
	dialogue_label.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	dialogue_label.anchor_left = 0.06
	dialogue_label.anchor_top = 0.1
	dialogue_label.anchor_right = 0.94
	dialogue_label.anchor_bottom = 0.2
	dialogue_label.add_theme_font_size_override("font_size", 19)
	dialogue_label.add_theme_color_override("font_color", Color("14243d"))
	add_child(dialogue_label)


func trigger_route_12_snorlax_wake_scene() -> void:
	if save_state:
		save_state.record_route_12_snorlax_wake_scene()
	dialogue_label.text = "Red: Route 12 is finally moving again. Bill confirms the Poke Flute signal is clean, Snorlax is waking, and the last Team Moonlight sleep echo is breaking off the road."


func trigger_snorlax_static_encounter() -> void:
	if save_state:
		save_state.record_route_12_snorlax_static_encounter()
		save_state.start_wild_encounter(snorlax_encounter)
	dialogue_label.text = "The Poke Flute plays. Snorlax opened its eyes on Route 12."
	emit_signal("start_wild_encounter", snorlax_encounter)


func return_to_pokemon_tower_fuji_rescue() -> void:
	emit_signal("go_to_pokemon_tower_fuji_rescue")


func _update_intro_dialogue() -> void:
	dialogue_label.text = "Red: Route 12 is blocked by Snorlax, but we have the Poke Flute now. Press Z/Enter to clear the Moonlight sleep echo, Down to wake Snorlax, or X/Esc to return."


func _load_json(path: String) -> Dictionary:
	if not FileAccess.file_exists(path):
		return {}
	var file := FileAccess.open(path, FileAccess.READ)
	if file == null:
		return {}
	var parsed = JSON.parse_string(file.get_as_text())
	if typeof(parsed) == TYPE_DICTIONARY:
		return parsed
	return {}
