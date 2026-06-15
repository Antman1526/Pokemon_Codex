extends Control

signal go_to_cerulean_city

var save_state
var dialogue_label: Label


func _ready() -> void:
	_build_route()
	if save_state:
		save_state.enter_route_5_underground_path()
	_update_intro_dialogue()


func _unhandled_input(event: InputEvent) -> void:
	if event.is_action_pressed("confirm"):
		trigger_underground_path_scouting()
	if event.is_action_pressed("cancel"):
		return_to_cerulean_city()


func _build_route() -> void:
	var grass := ColorRect.new()
	grass.color = Color("6faa66")
	grass.set_anchors_preset(Control.PRESET_FULL_RECT)
	add_child(grass)

	var path := ColorRect.new()
	path.color = Color("d9c286")
	path.anchor_left = 0.2
	path.anchor_top = 0.08
	path.anchor_right = 0.42
	path.anchor_bottom = 0.9
	add_child(path)

	var underground := ColorRect.new()
	underground.color = Color("7d6a55")
	underground.anchor_left = 0.54
	underground.anchor_top = 0.2
	underground.anchor_right = 0.86
	underground.anchor_bottom = 0.48
	add_child(underground)

	var rail := ColorRect.new()
	rail.color = Color("4b4f55")
	rail.anchor_left = 0.5
	rail.anchor_top = 0.62
	rail.anchor_right = 0.92
	rail.anchor_bottom = 0.72
	add_child(rail)

	var header := Label.new()
	header.text = "Route 5 - Underground Path"
	header.anchor_left = 0.04
	header.anchor_top = 0.04
	header.anchor_right = 0.72
	header.anchor_bottom = 0.1
	header.add_theme_font_size_override("font_size", 32)
	header.add_theme_color_override("font_color", Color("163617"))
	add_child(header)

	var entrance_label := Label.new()
	entrance_label.text = "Underground Path"
	entrance_label.anchor_left = 0.58
	entrance_label.anchor_top = 0.3
	entrance_label.anchor_right = 0.84
	entrance_label.anchor_bottom = 0.36
	entrance_label.add_theme_font_size_override("font_size", 18)
	entrance_label.add_theme_color_override("font_color", Color("fff1d5"))
	add_child(entrance_label)

	dialogue_label = Label.new()
	dialogue_label.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	dialogue_label.anchor_left = 0.06
	dialogue_label.anchor_top = 0.74
	dialogue_label.anchor_right = 0.94
	dialogue_label.anchor_bottom = 0.95
	dialogue_label.add_theme_font_size_override("font_size", 20)
	dialogue_label.add_theme_color_override("font_color", Color("163617"))
	add_child(dialogue_label)


func trigger_underground_path_scouting() -> void:
	if save_state:
		save_state.record_underground_path_scouting()
	dialogue_label.text = "Red: Underground Path is open. Misty says the tunnel is watched, and Bill traced the stolen TM route to Vermilion's docks. We are close to Surge, the S.S. Anne, and Rocket's shipping lane."


func return_to_cerulean_city() -> void:
	emit_signal("go_to_cerulean_city")


func _update_intro_dialogue() -> void:
	dialogue_label.text = "Red: Route 5 is the road south from Cerulean. Press Z/Enter to scout Underground Path with Misty and Bill's notes, or X/Esc to return to Cerulean."
