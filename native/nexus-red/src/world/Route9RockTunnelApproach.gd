extends Control

signal go_to_route_2_east_field_lab
signal go_to_rock_tunnel_interior

var save_state
var dialogue_label: Label


func _ready() -> void:
	_build_route()
	if save_state:
		save_state.enter_route_9_rock_tunnel_approach()
	_update_intro_dialogue()


func _unhandled_input(event: InputEvent) -> void:
	if event.is_action_pressed("confirm"):
		trigger_route_9_approach_scene()
	if event.is_action_pressed("ui_right"):
		trigger_rock_tunnel_entry()
	if event.is_action_pressed("cancel"):
		return_to_route_2_east_field_lab()


func _build_route() -> void:
	var grass := ColorRect.new()
	grass.color = Color("6da15c")
	grass.set_anchors_preset(Control.PRESET_FULL_RECT)
	add_child(grass)

	var trainer_lane := ColorRect.new()
	trainer_lane.color = Color("d5b46e")
	trainer_lane.anchor_left = 0.08
	trainer_lane.anchor_top = 0.46
	trainer_lane.anchor_right = 0.72
	trainer_lane.anchor_bottom = 0.6
	add_child(trainer_lane)

	var tunnel_mouth := ColorRect.new()
	tunnel_mouth.color = Color("2f2d2f")
	tunnel_mouth.anchor_left = 0.72
	tunnel_mouth.anchor_top = 0.22
	tunnel_mouth.anchor_right = 0.94
	tunnel_mouth.anchor_bottom = 0.58
	add_child(tunnel_mouth)

	var moonlight_marker := ColorRect.new()
	moonlight_marker.color = Color("6f5f94")
	moonlight_marker.anchor_left = 0.48
	moonlight_marker.anchor_top = 0.2
	moonlight_marker.anchor_right = 0.62
	moonlight_marker.anchor_bottom = 0.34
	add_child(moonlight_marker)

	var rocket_cache := ColorRect.new()
	rocket_cache.color = Color("343038")
	rocket_cache.anchor_left = 0.18
	rocket_cache.anchor_top = 0.64
	rocket_cache.anchor_right = 0.38
	rocket_cache.anchor_bottom = 0.74
	add_child(rocket_cache)

	var header := Label.new()
	header.text = "Route 9 - Rock Tunnel Approach"
	header.anchor_left = 0.04
	header.anchor_top = 0.04
	header.anchor_right = 0.82
	header.anchor_bottom = 0.1
	header.add_theme_font_size_override("font_size", 32)
	header.add_theme_color_override("font_color", Color("102e18"))
	add_child(header)

	var lane_label := Label.new()
	lane_label.text = "trainer lane"
	lane_label.anchor_left = 0.28
	lane_label.anchor_top = 0.5
	lane_label.anchor_right = 0.48
	lane_label.anchor_bottom = 0.56
	lane_label.add_theme_font_size_override("font_size", 18)
	lane_label.add_theme_color_override("font_color", Color("332710"))
	add_child(lane_label)

	var tunnel_label := Label.new()
	tunnel_label.text = "Rock Tunnel"
	tunnel_label.anchor_left = 0.765
	tunnel_label.anchor_top = 0.37
	tunnel_label.anchor_right = 0.94
	tunnel_label.anchor_bottom = 0.43
	tunnel_label.add_theme_font_size_override("font_size", 18)
	tunnel_label.add_theme_color_override("font_color", Color("f6ead4"))
	add_child(tunnel_label)

	dialogue_label = Label.new()
	dialogue_label.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	dialogue_label.anchor_left = 0.06
	dialogue_label.anchor_top = 0.78
	dialogue_label.anchor_right = 0.94
	dialogue_label.anchor_bottom = 0.96
	dialogue_label.add_theme_font_size_override("font_size", 20)
	dialogue_label.add_theme_color_override("font_color", Color("102e18"))
	add_child(dialogue_label)


func trigger_route_9_approach_scene() -> void:
	if save_state:
		save_state.record_route_9_approach_scene()
	dialogue_label.text = "Red: Route 9 is a trainer lane, so we train before Rock Tunnel. Bill warns the cave is dark and the Echo Flute signal points toward Lavender. Team Moonlight finally stepped into the open, and Rocket left a supply cache near their mark."


func trigger_rock_tunnel_entry() -> void:
	if save_state and not bool(save_state.story_flags.get("rock_tunnel_entry_unlocked", false)):
		dialogue_label.text = "Red: Rock Tunnel is not a shortcut. Scout Route 9 first so we know where Team Moonlight, Rocket, and the Lavender signal are pulling from."
		return
	dialogue_label.text = "Red: Rock Tunnel is open. Stay close, watch the echoes, and keep Bill's Echo Flute trace in mind."
	emit_signal("go_to_rock_tunnel_interior")


func return_to_route_2_east_field_lab() -> void:
	emit_signal("go_to_route_2_east_field_lab")


func _update_intro_dialogue() -> void:
	dialogue_label.text = "Red: Route 9 is the approach to Rock Tunnel. Press Z/Enter to scout the trainer lane, Moonlight mark, Rocket cache, and Lavender signal, Right to enter Rock Tunnel, or X/Esc to return to Route 2."
