extends Control

signal go_to_route_1
signal go_to_route_2_forest_gate

var save_state
var dialogue_label: Label


func _ready() -> void:
	_build_city()
	if save_state:
		save_state.enter_viridian_city()
	_update_intro_dialogue()


func _unhandled_input(event: InputEvent) -> void:
	if event.is_action_pressed("confirm"):
		interact_pokemon_center()
	if event.is_action_pressed("menu"):
		interact_poke_mart()
	if event.is_action_pressed("worldlink"):
		interact_red_companion()
	if event.is_action_pressed("ui_up"):
		if save_state and save_state.story_flags.get("viridian_rocket_clue_found", false):
			trigger_route_2_gate_entry()
		else:
			investigate_rocket_clue()
	if event.is_action_pressed("cancel"):
		emit_signal("go_to_route_1")


func _build_city() -> void:
	var grass := ColorRect.new()
	grass.color = Color("6fbf66")
	grass.set_anchors_preset(Control.PRESET_FULL_RECT)
	add_child(grass)

	var road := ColorRect.new()
	road.color = Color("d8c17a")
	road.anchor_left = 0.0
	road.anchor_top = 0.48
	road.anchor_right = 1.0
	road.anchor_bottom = 0.64
	add_child(road)

	var center := ColorRect.new()
	center.color = Color("d94a5d")
	center.anchor_left = 0.1
	center.anchor_top = 0.18
	center.anchor_right = 0.34
	center.anchor_bottom = 0.38
	add_child(center)

	var mart := ColorRect.new()
	mart.color = Color("4f7fd8")
	mart.anchor_left = 0.62
	mart.anchor_top = 0.18
	mart.anchor_right = 0.86
	mart.anchor_bottom = 0.38
	add_child(mart)

	var north_gate := ColorRect.new()
	north_gate.color = Color("42543a")
	north_gate.anchor_left = 0.44
	north_gate.anchor_top = 0.02
	north_gate.anchor_right = 0.56
	north_gate.anchor_bottom = 0.12
	add_child(north_gate)

	var header := Label.new()
	header.text = "Viridian City"
	header.anchor_left = 0.04
	header.anchor_top = 0.04
	header.anchor_right = 0.38
	header.anchor_bottom = 0.1
	header.add_theme_font_size_override("font_size", 32)
	header.add_theme_color_override("font_color", Color("14243d"))
	add_child(header)

	var center_label := Label.new()
	center_label.text = "Pokemon Center"
	center_label.anchor_left = 0.12
	center_label.anchor_top = 0.24
	center_label.anchor_right = 0.32
	center_label.anchor_bottom = 0.32
	center_label.add_theme_font_size_override("font_size", 20)
	add_child(center_label)

	var mart_label := Label.new()
	mart_label.text = "Poke Mart"
	mart_label.anchor_left = 0.66
	mart_label.anchor_top = 0.24
	mart_label.anchor_right = 0.84
	mart_label.anchor_bottom = 0.32
	mart_label.add_theme_font_size_override("font_size", 20)
	add_child(mart_label)

	dialogue_label = Label.new()
	dialogue_label.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	dialogue_label.anchor_left = 0.06
	dialogue_label.anchor_top = 0.8
	dialogue_label.anchor_right = 0.94
	dialogue_label.anchor_bottom = 0.95
	dialogue_label.add_theme_font_size_override("font_size", 20)
	dialogue_label.add_theme_color_override("font_color", Color("14243d"))
	add_child(dialogue_label)


func interact_pokemon_center() -> void:
	if save_state:
		save_state.record_viridian_center_visit()
	dialogue_label.text = "Nurse Joy: Your party is healed. Red says Viridian is where the simple journey starts feeling bigger."


func interact_poke_mart() -> void:
	if save_state:
		save_state.record_viridian_mart_visit()
	var money := 0
	if save_state:
		money = save_state.player_money
	dialogue_label.text = "Poke Mart Clerk: Basic field supplies are ready. Antman's travel fund is $%d." % money


func interact_red_companion() -> void:
	if save_state:
		save_state.record_viridian_red_scene()
	dialogue_label.text = "Red: Viridian is quiet because everyone thinks quiet means safe. It does not. Check the Mart shipment logs before we push north."


func investigate_rocket_clue() -> void:
	if save_state:
		save_state.record_viridian_rocket_clue()
	dialogue_label.text = "A supply slip behind the Mart has a Rocket stamp pressed into the corner. Red folds it carefully: first clue, not the last."


func trigger_route_2_gate_entry() -> void:
	if save_state and not save_state.story_flags.get("viridian_rocket_clue_found", false):
		save_state.record_viridian_rocket_clue()
	dialogue_label.text = "Red: Route 2 is the next step. If Rocket activity is already touching Viridian, the Viridian Forest Gate is where we start tracking it."
	emit_signal("go_to_route_2_forest_gate")


func _update_intro_dialogue() -> void:
	dialogue_label.text = "Nurse Joy waves from the Pokemon Center while the Poke Mart clerk stocks early-route supplies. Press Z/Enter for Center, Tab for Mart, W for Red, Up for Rocket clue or north gate, X/Esc to return south."
