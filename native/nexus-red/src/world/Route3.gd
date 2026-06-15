extends Control

const EncounterService := preload("res://src/encounter/EncounterService.gd")
const FIRST_ROUTE_3_MIGRATION_ID := "route_3_migration_chespin"

signal go_to_route_2_forest_gate
signal start_wild_encounter(encounter_data)

var save_state
var dialogue_label: Label
var encounter_service := EncounterService.new()


func _ready() -> void:
	_build_route()
	if save_state:
		save_state.enter_route_3()
	_update_intro_dialogue()


func _unhandled_input(event: InputEvent) -> void:
	if event.is_action_pressed("confirm"):
		trigger_route_3_migration_encounter()
	if event.is_action_pressed("cancel"):
		return_to_route_2_forest_gate()


func _build_route() -> void:
	var grass := ColorRect.new()
	grass.color = Color("70b85c")
	grass.set_anchors_preset(Control.PRESET_FULL_RECT)
	add_child(grass)

	var path := ColorRect.new()
	path.color = Color("d4b070")
	path.anchor_left = 0.0
	path.anchor_top = 0.44
	path.anchor_right = 1.0
	path.anchor_bottom = 0.6
	add_child(path)

	var ridge := ColorRect.new()
	ridge.color = Color("8a7a54")
	ridge.anchor_left = 0.0
	ridge.anchor_top = 0.08
	ridge.anchor_right = 1.0
	ridge.anchor_bottom = 0.18
	add_child(ridge)

	for i in range(5):
		var tall_grass := ColorRect.new()
		tall_grass.color = Color("4d9847")
		tall_grass.position = Vector2(120 + i * 190, 260 + (i % 2) * 120)
		tall_grass.size = Vector2(110, 72)
		add_child(tall_grass)

	var header := Label.new()
	header.text = "Route 3"
	header.anchor_left = 0.04
	header.anchor_top = 0.04
	header.anchor_right = 0.4
	header.anchor_bottom = 0.1
	header.add_theme_font_size_override("font_size", 32)
	header.add_theme_color_override("font_color", Color("14243d"))
	add_child(header)

	var pewter_sign := Label.new()
	pewter_sign.text = "Pewter approach"
	pewter_sign.anchor_left = 0.7
	pewter_sign.anchor_top = 0.36
	pewter_sign.anchor_right = 0.94
	pewter_sign.anchor_bottom = 0.42
	pewter_sign.add_theme_font_size_override("font_size", 20)
	pewter_sign.add_theme_color_override("font_color", Color("14243d"))
	add_child(pewter_sign)

	dialogue_label = Label.new()
	dialogue_label.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	dialogue_label.anchor_left = 0.06
	dialogue_label.anchor_top = 0.78
	dialogue_label.anchor_right = 0.94
	dialogue_label.anchor_bottom = 0.95
	dialogue_label.add_theme_font_size_override("font_size", 20)
	dialogue_label.add_theme_color_override("font_color", Color("14243d"))
	add_child(dialogue_label)


func trigger_route_3_migration_encounter() -> void:
	var encounter := encounter_service.pick_early_migration_encounter("route_3", save_state)
	if encounter.is_empty():
		dialogue_label.text = "Red checks Oak's migration scanner, but Route 3 migration data is not ready yet."
		return
	if save_state:
		save_state.start_wild_encounter(encounter)
	dialogue_label.text = "Red: Route 3 migration signal locked. This closes the first full starter migration loop before Pewter."
	emit_signal("start_wild_encounter", encounter)


func return_to_route_2_forest_gate() -> void:
	emit_signal("go_to_route_2_forest_gate")


func _update_intro_dialogue() -> void:
	dialogue_label.text = "Red: Route 3 carries the final early migration group. Press Z/Enter for Route 3 migration, or X/Esc to return to the Viridian Forest Gate."
