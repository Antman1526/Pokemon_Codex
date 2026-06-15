extends Control

signal go_to_rock_tunnel_interior
signal go_to_pokemon_tower_first_floor

var save_state
var dialogue_label: Label


func _ready() -> void:
	_build_outskirts()
	if save_state:
		save_state.enter_lavender_outskirts()
	_update_intro_dialogue()


func _unhandled_input(event: InputEvent) -> void:
	if event.is_action_pressed("confirm"):
		trigger_lavender_outskirts_scene()
	if event.is_action_pressed("ui_right"):
		trigger_pokemon_tower_entry()
	if event.is_action_pressed("cancel"):
		return_to_rock_tunnel_interior()


func _build_outskirts() -> void:
	var dusk := ColorRect.new()
	dusk.color = Color("5c5872")
	dusk.set_anchors_preset(Control.PRESET_FULL_RECT)
	add_child(dusk)

	var road := ColorRect.new()
	road.color = Color("c6ae83")
	road.anchor_left = 0.06
	road.anchor_top = 0.58
	road.anchor_right = 0.94
	road.anchor_bottom = 0.7
	add_child(road)

	var town_edge := ColorRect.new()
	town_edge.color = Color("8d799e")
	town_edge.anchor_left = 0.18
	town_edge.anchor_top = 0.22
	town_edge.anchor_right = 0.48
	town_edge.anchor_bottom = 0.5
	add_child(town_edge)

	var tower_shadow := ColorRect.new()
	tower_shadow.color = Color("2b2438")
	tower_shadow.anchor_left = 0.62
	tower_shadow.anchor_top = 0.1
	tower_shadow.anchor_right = 0.82
	tower_shadow.anchor_bottom = 0.54
	add_child(tower_shadow)

	var moonlight_mark := ColorRect.new()
	moonlight_mark.color = Color("796bc0")
	moonlight_mark.anchor_left = 0.5
	moonlight_mark.anchor_top = 0.36
	moonlight_mark.anchor_right = 0.62
	moonlight_mark.anchor_bottom = 0.48
	add_child(moonlight_mark)

	var rocket_watch := ColorRect.new()
	rocket_watch.color = Color("2f2a2e")
	rocket_watch.anchor_left = 0.84
	rocket_watch.anchor_top = 0.48
	rocket_watch.anchor_right = 0.94
	rocket_watch.anchor_bottom = 0.62
	add_child(rocket_watch)

	var header := Label.new()
	header.text = "Lavender Outskirts"
	header.anchor_left = 0.04
	header.anchor_top = 0.04
	header.anchor_right = 0.78
	header.anchor_bottom = 0.1
	header.add_theme_font_size_override("font_size", 32)
	header.add_theme_color_override("font_color", Color("f4ecff"))
	add_child(header)

	var town_label := Label.new()
	town_label.text = "Lavender town edge"
	town_label.anchor_left = 0.21
	town_label.anchor_top = 0.51
	town_label.anchor_right = 0.5
	town_label.anchor_bottom = 0.57
	town_label.add_theme_font_size_override("font_size", 16)
	town_label.add_theme_color_override("font_color", Color("f8edff"))
	add_child(town_label)

	var tower_label := Label.new()
	tower_label.text = "Pokemon Tower signal"
	tower_label.anchor_left = 0.58
	tower_label.anchor_top = 0.55
	tower_label.anchor_right = 0.9
	tower_label.anchor_bottom = 0.61
	tower_label.add_theme_font_size_override("font_size", 16)
	tower_label.add_theme_color_override("font_color", Color("f8edff"))
	add_child(tower_label)

	var pressure_label := Label.new()
	pressure_label.text = "Moonlight + Rocket pressure"
	pressure_label.anchor_left = 0.49
	pressure_label.anchor_top = 0.28
	pressure_label.anchor_right = 0.92
	pressure_label.anchor_bottom = 0.34
	pressure_label.add_theme_font_size_override("font_size", 16)
	pressure_label.add_theme_color_override("font_color", Color("f8edff"))
	add_child(pressure_label)

	dialogue_label = Label.new()
	dialogue_label.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	dialogue_label.anchor_left = 0.06
	dialogue_label.anchor_top = 0.78
	dialogue_label.anchor_right = 0.94
	dialogue_label.anchor_bottom = 0.96
	dialogue_label.add_theme_font_size_override("font_size", 20)
	dialogue_label.add_theme_color_override("font_color", Color("f4ecff"))
	add_child(dialogue_label)


func trigger_lavender_outskirts_scene() -> void:
	if save_state:
		save_state.record_lavender_outskirts_scene()
	dialogue_label.text = "Red: Lavender feels quiet, but not safe. Bill says the Echo Flute is matching a Pokemon Tower signal. Team Moonlight is already near the graves, and Rocket is watching the road like Giovanni expected us here."


func return_to_rock_tunnel_interior() -> void:
	emit_signal("go_to_rock_tunnel_interior")


func trigger_pokemon_tower_entry() -> void:
	if save_state and not bool(save_state.story_flags.get("pokemon_tower_entry_unlocked", false)):
		dialogue_label.text = "Red: Pokemon Tower is calling, but we need Bill to confirm the Echo Flute signal and identify the Moonlight and Rocket pressure first."
		return
	dialogue_label.text = "Red: Pokemon Tower is open. Stay close and do not trust the echoes."
	emit_signal("go_to_pokemon_tower_first_floor")


func _update_intro_dialogue() -> void:
	dialogue_label.text = "Red: Lavender is the first town where the journey feels different. Press Z/Enter to decode Bill's Pokemon Tower Echo Flute signal, Team Moonlight presence, and Rocket surveillance, Right for Pokemon Tower, or X/Esc to return to Rock Tunnel."
