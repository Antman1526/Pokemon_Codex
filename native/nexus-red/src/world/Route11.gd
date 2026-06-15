extends Control

signal go_to_vermilion_power_sabotage

var save_state
var dialogue_label: Label


func _ready() -> void:
	_build_route()
	if save_state:
		save_state.enter_route_11()
	_update_intro_dialogue()


func _unhandled_input(event: InputEvent) -> void:
	if event.is_action_pressed("confirm"):
		trigger_route_11_handoff_scene()
	if event.is_action_pressed("cancel"):
		return_to_vermilion_power_sabotage()


func _build_route() -> void:
	var grass := ColorRect.new()
	grass.color = Color("6eb15d")
	grass.set_anchors_preset(Control.PRESET_FULL_RECT)
	add_child(grass)

	var road := ColorRect.new()
	road.color = Color("d7bd75")
	road.anchor_left = 0.08
	road.anchor_top = 0.42
	road.anchor_right = 0.94
	road.anchor_bottom = 0.58
	add_child(road)

	var relay_pole := ColorRect.new()
	relay_pole.color = Color("66503c")
	relay_pole.anchor_left = 0.18
	relay_pole.anchor_top = 0.18
	relay_pole.anchor_right = 0.22
	relay_pole.anchor_bottom = 0.48
	add_child(relay_pole)

	var cave_sign := ColorRect.new()
	cave_sign.color = Color("4d4b46")
	cave_sign.anchor_left = 0.66
	cave_sign.anchor_top = 0.18
	cave_sign.anchor_right = 0.88
	cave_sign.anchor_bottom = 0.36
	add_child(cave_sign)

	var snorlax_shadow := ColorRect.new()
	snorlax_shadow.color = Color("31414b")
	snorlax_shadow.anchor_left = 0.72
	snorlax_shadow.anchor_top = 0.58
	snorlax_shadow.anchor_right = 0.94
	snorlax_shadow.anchor_bottom = 0.78
	add_child(snorlax_shadow)

	var gas_trace := ColorRect.new()
	gas_trace.color = Color("96a75a")
	gas_trace.anchor_left = 0.3
	gas_trace.anchor_top = 0.3
	gas_trace.anchor_right = 0.58
	gas_trace.anchor_bottom = 0.38
	add_child(gas_trace)

	var header := Label.new()
	header.text = "Route 11 - Eastbound Road"
	header.anchor_left = 0.04
	header.anchor_top = 0.04
	header.anchor_right = 0.78
	header.anchor_bottom = 0.1
	header.add_theme_font_size_override("font_size", 32)
	header.add_theme_color_override("font_color", Color("12351b"))
	add_child(header)

	var sign_label := Label.new()
	sign_label.text = "Diglett's Cave relay"
	sign_label.anchor_left = 0.68
	sign_label.anchor_top = 0.235
	sign_label.anchor_right = 0.88
	sign_label.anchor_bottom = 0.3
	sign_label.add_theme_font_size_override("font_size", 16)
	sign_label.add_theme_color_override("font_color", Color("f0ead6"))
	add_child(sign_label)

	var shadow_label := Label.new()
	shadow_label.text = "sleeping roadblock"
	shadow_label.anchor_left = 0.735
	shadow_label.anchor_top = 0.655
	shadow_label.anchor_right = 0.93
	shadow_label.anchor_bottom = 0.72
	shadow_label.add_theme_font_size_override("font_size", 16)
	shadow_label.add_theme_color_override("font_color", Color("f0ead6"))
	add_child(shadow_label)

	dialogue_label = Label.new()
	dialogue_label.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	dialogue_label.anchor_left = 0.06
	dialogue_label.anchor_top = 0.78
	dialogue_label.anchor_right = 0.94
	dialogue_label.anchor_bottom = 0.96
	dialogue_label.add_theme_font_size_override("font_size", 20)
	dialogue_label.add_theme_color_override("font_color", Color("12351b"))
	add_child(dialogue_label)


func trigger_route_11_handoff_scene() -> void:
	if save_state:
		save_state.record_route_11_handoff_scene()
	dialogue_label.text = "Red: Route 11 is our first road after Surge, and I am staying with you, Antman. Misty says she will rotate to water-route support after this checkpoint. Bill decoded a Nexus pulse from the relay pole, Rocket and Team Gas are fighting over who poisoned the grid, and a Snorlax roadblock is forcing everyone toward Diglett's Cave."


func return_to_vermilion_power_sabotage() -> void:
	emit_signal("go_to_vermilion_power_sabotage")


func _update_intro_dialogue() -> void:
	dialogue_label.text = "Red: Thunder Badge opened Route 11. Press Z/Enter to read the eastbound road with Misty and Bill, or X/Esc to return to the Vermilion service yard."
