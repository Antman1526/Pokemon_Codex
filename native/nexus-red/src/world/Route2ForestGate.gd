extends Control

const EncounterService := preload("res://src/encounter/EncounterService.gd")

signal go_to_viridian_city
signal start_wild_encounter(encounter_data)

var save_state
var dialogue_label: Label
var encounter_service := EncounterService.new()


func _ready() -> void:
	_build_gate()
	if save_state:
		save_state.enter_route_2_forest_gate()
	_update_intro_dialogue()


func _unhandled_input(event: InputEvent) -> void:
	if event.is_action_pressed("confirm"):
		trigger_route_2_catch_tutorial()
	if event.is_action_pressed("cancel"):
		return_to_viridian_city()


func _build_gate() -> void:
	var grass := ColorRect.new()
	grass.color = Color("5fa95e")
	grass.set_anchors_preset(Control.PRESET_FULL_RECT)
	add_child(grass)

	var trail := ColorRect.new()
	trail.color = Color("d7bd78")
	trail.anchor_left = 0.42
	trail.anchor_top = 0.0
	trail.anchor_right = 0.58
	trail.anchor_bottom = 1.0
	add_child(trail)

	var forest_edge := ColorRect.new()
	forest_edge.color = Color("234f37")
	forest_edge.anchor_left = 0.0
	forest_edge.anchor_top = 0.0
	forest_edge.anchor_right = 1.0
	forest_edge.anchor_bottom = 0.24
	add_child(forest_edge)

	var gate := ColorRect.new()
	gate.color = Color("8a623d")
	gate.anchor_left = 0.34
	gate.anchor_top = 0.24
	gate.anchor_right = 0.66
	gate.anchor_bottom = 0.44
	add_child(gate)

	var header := Label.new()
	header.text = "Route 2"
	header.anchor_left = 0.04
	header.anchor_top = 0.04
	header.anchor_right = 0.38
	header.anchor_bottom = 0.1
	header.add_theme_font_size_override("font_size", 32)
	header.add_theme_color_override("font_color", Color("eef6d8"))
	add_child(header)

	var gate_label := Label.new()
	gate_label.text = "Viridian Forest Gate"
	gate_label.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	gate_label.anchor_left = 0.34
	gate_label.anchor_top = 0.3
	gate_label.anchor_right = 0.66
	gate_label.anchor_bottom = 0.38
	gate_label.add_theme_font_size_override("font_size", 22)
	gate_label.add_theme_color_override("font_color", Color("fff2c7"))
	add_child(gate_label)

	dialogue_label = Label.new()
	dialogue_label.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	dialogue_label.anchor_left = 0.06
	dialogue_label.anchor_top = 0.78
	dialogue_label.anchor_right = 0.94
	dialogue_label.anchor_bottom = 0.95
	dialogue_label.add_theme_font_size_override("font_size", 20)
	dialogue_label.add_theme_color_override("font_color", Color("14243d"))
	add_child(dialogue_label)


func inspect_gate() -> void:
	dialogue_label.text = "A fresh boot print cuts across the Route 2 trail. Red points toward the Viridian Forest Gate and lowers his voice: Rocket activity is moving north."


func trigger_route_2_catch_tutorial() -> void:
	var encounter := encounter_service.pick_route_2_encounter(save_state)
	if encounter.is_empty():
		dialogue_label.text = "Red checks the grass line, but the Route 2 encounter table is not ready yet."
		return
	if save_state:
		save_state.start_wild_encounter(encounter)
	dialogue_label.text = "Red: Pidgey is circling low. This is a clean catch tutorial before Viridian Forest gets risky."
	emit_signal("start_wild_encounter", encounter)


func return_to_viridian_city() -> void:
	emit_signal("go_to_viridian_city")


func _update_intro_dialogue() -> void:
	dialogue_label.text = "Red: This is Route 2 and the Viridian Forest Gate. The trees are too quiet, and Rocket activity this close to town means somebody is testing the road ahead. Press Z/Enter for the catch tutorial."
