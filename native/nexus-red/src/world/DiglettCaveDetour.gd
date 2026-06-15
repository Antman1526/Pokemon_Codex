extends Control

signal go_to_route_11

var save_state
var dialogue_label: Label


func _ready() -> void:
	_build_cave()
	if save_state:
		save_state.enter_diglett_cave_detour()
	_update_intro_dialogue()


func _unhandled_input(event: InputEvent) -> void:
	if event.is_action_pressed("confirm"):
		trigger_diglett_cave_detour_scene()
	if event.is_action_pressed("cancel"):
		return_to_route_11()


func _build_cave() -> void:
	var stone := ColorRect.new()
	stone.color = Color("5e554d")
	stone.set_anchors_preset(Control.PRESET_FULL_RECT)
	add_child(stone)

	var tunnel := ColorRect.new()
	tunnel.color = Color("332c28")
	tunnel.anchor_left = 0.12
	tunnel.anchor_top = 0.18
	tunnel.anchor_right = 0.88
	tunnel.anchor_bottom = 0.72
	add_child(tunnel)

	var diglett_path := ColorRect.new()
	diglett_path.color = Color("b78f5c")
	diglett_path.anchor_left = 0.2
	diglett_path.anchor_top = 0.42
	diglett_path.anchor_right = 0.82
	diglett_path.anchor_bottom = 0.54
	add_child(diglett_path)

	var relay := ColorRect.new()
	relay.color = Color("3f6d7d")
	relay.anchor_left = 0.1
	relay.anchor_top = 0.2
	relay.anchor_right = 0.24
	relay.anchor_bottom = 0.38
	add_child(relay)

	var faction_crates := ColorRect.new()
	faction_crates.color = Color("b59645")
	faction_crates.anchor_left = 0.62
	faction_crates.anchor_top = 0.58
	faction_crates.anchor_right = 0.88
	faction_crates.anchor_bottom = 0.7
	add_child(faction_crates)

	var header := Label.new()
	header.text = "Diglett's Cave - Nexus Detour"
	header.anchor_left = 0.04
	header.anchor_top = 0.04
	header.anchor_right = 0.82
	header.anchor_bottom = 0.1
	header.add_theme_font_size_override("font_size", 32)
	header.add_theme_color_override("font_color", Color("f5e6c7"))
	add_child(header)

	var relay_label := Label.new()
	relay_label.text = "Nexus relay"
	relay_label.anchor_left = 0.115
	relay_label.anchor_top = 0.255
	relay_label.anchor_right = 0.24
	relay_label.anchor_bottom = 0.32
	relay_label.add_theme_font_size_override("font_size", 15)
	relay_label.add_theme_color_override("font_color", Color("f5e6c7"))
	add_child(relay_label)

	var crate_label := Label.new()
	crate_label.text = "Gold Dust crates"
	crate_label.anchor_left = 0.645
	crate_label.anchor_top = 0.61
	crate_label.anchor_right = 0.88
	crate_label.anchor_bottom = 0.67
	crate_label.add_theme_font_size_override("font_size", 15)
	crate_label.add_theme_color_override("font_color", Color("2b2216"))
	add_child(crate_label)

	dialogue_label = Label.new()
	dialogue_label.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	dialogue_label.anchor_left = 0.06
	dialogue_label.anchor_top = 0.78
	dialogue_label.anchor_right = 0.94
	dialogue_label.anchor_bottom = 0.96
	dialogue_label.add_theme_font_size_override("font_size", 20)
	dialogue_label.add_theme_color_override("font_color", Color("f5e6c7"))
	add_child(dialogue_label)


func trigger_diglett_cave_detour_scene() -> void:
	if save_state:
		save_state.record_diglett_cave_detour_scene()
	dialogue_label.text = "Red: Diglett's Cave keeps us moving while Snorlax blocks Route 12. Bill mapped a Nexus relay through these tunnels, Rocket is yelling at Gold Dust over stolen cave survey crates, and the only clean way to wake Snorlax later is an Echo Flute lead."


func return_to_route_11() -> void:
	emit_signal("go_to_route_11")


func _update_intro_dialogue() -> void:
	dialogue_label.text = "Red: Diglett's Cave is the detour, not a shortcut. Press Z/Enter to map the tunnel with Bill's relay notes, or X/Esc to return to Route 11."
