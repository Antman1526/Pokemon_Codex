extends Control

signal go_to_cerulean_city

var save_state
var dialogue_label: Label


func _ready() -> void:
	_build_route()
	if save_state:
		save_state.enter_route_25_bill()
	_update_intro_dialogue()


func _unhandled_input(event: InputEvent) -> void:
	if event.is_action_pressed("confirm"):
		trigger_bill_intro()
	if event.is_action_pressed("cancel"):
		return_to_cerulean_city()


func _build_route() -> void:
	var grass := ColorRect.new()
	grass.color = Color("75b96f")
	grass.set_anchors_preset(Control.PRESET_FULL_RECT)
	add_child(grass)

	var path := ColorRect.new()
	path.color = Color("d8c487")
	path.anchor_left = 0.1
	path.anchor_top = 0.46
	path.anchor_right = 0.9
	path.anchor_bottom = 0.64
	add_child(path)

	var water := ColorRect.new()
	water.color = Color("4aa7d8")
	water.anchor_left = 0.04
	water.anchor_top = 0.68
	water.anchor_right = 0.96
	water.anchor_bottom = 0.92
	add_child(water)

	var cottage := ColorRect.new()
	cottage.color = Color("c78454")
	cottage.anchor_left = 0.58
	cottage.anchor_top = 0.18
	cottage.anchor_right = 0.86
	cottage.anchor_bottom = 0.42
	add_child(cottage)

	var header := Label.new()
	header.text = "Route 25 - Bill's Cottage"
	header.anchor_left = 0.04
	header.anchor_top = 0.04
	header.anchor_right = 0.72
	header.anchor_bottom = 0.1
	header.add_theme_font_size_override("font_size", 32)
	header.add_theme_color_override("font_color", Color("15341f"))
	add_child(header)

	var cottage_label := Label.new()
	cottage_label.text = "Sea Cottage"
	cottage_label.anchor_left = 0.62
	cottage_label.anchor_top = 0.28
	cottage_label.anchor_right = 0.84
	cottage_label.anchor_bottom = 0.34
	cottage_label.add_theme_font_size_override("font_size", 18)
	cottage_label.add_theme_color_override("font_color", Color("fff1d5"))
	add_child(cottage_label)

	dialogue_label = Label.new()
	dialogue_label.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	dialogue_label.anchor_left = 0.06
	dialogue_label.anchor_top = 0.74
	dialogue_label.anchor_right = 0.94
	dialogue_label.anchor_bottom = 0.95
	dialogue_label.add_theme_font_size_override("font_size", 20)
	dialogue_label.add_theme_color_override("font_color", Color("15341f"))
	add_child(dialogue_label)


func trigger_bill_intro() -> void:
	if save_state:
		save_state.record_bill_route25_intro()
	dialogue_label.text = "Bill: Red, Misty, Antman - look at this WorldLink trace. The storage network is reading Nexus echoes from regions Antman has not reached yet. This is bigger than Rocket stealing fossils."


func return_to_cerulean_city() -> void:
	emit_signal("go_to_cerulean_city")


func _update_intro_dialogue() -> void:
	dialogue_label.text = "Red: Route 25 is quiet after Cerulean, but Bill's cottage is lit up. Misty said he found a WorldLink pattern that points past Kanto. Press Z/Enter to meet Bill, or X/Esc to return to Cerulean."
