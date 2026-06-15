extends Control

signal go_to_cerulean_city
signal start_battle_placeholder(battle_id)

const FIRST_RECRUITER_BATTLE_ID := "nugget_bridge_recruiter_1"
const CAPTAIN_BATTLE_ID := "nugget_bridge_captain"

var save_state
var dialogue_label: Label


func _ready() -> void:
	_build_bridge()
	if save_state:
		save_state.enter_nugget_bridge()
	_update_intro_dialogue()


func _unhandled_input(event: InputEvent) -> void:
	if event.is_action_pressed("confirm"):
		trigger_bridge_scouting()
	if event.is_action_pressed("ui_up"):
		trigger_recruiter_battle()
	if event.is_action_pressed("ui_right"):
		trigger_bridge_captain_battle()
	if event.is_action_pressed("cancel"):
		return_to_cerulean_city()


func _build_bridge() -> void:
	var water := ColorRect.new()
	water.color = Color("4aa2c6")
	water.set_anchors_preset(Control.PRESET_FULL_RECT)
	add_child(water)

	var bridge := ColorRect.new()
	bridge.color = Color("b28a57")
	bridge.anchor_left = 0.38
	bridge.anchor_top = 0.0
	bridge.anchor_right = 0.58
	bridge.anchor_bottom = 1.0
	add_child(bridge)

	var city_gate := ColorRect.new()
	city_gate.color = Color("d8c487")
	city_gate.anchor_left = 0.22
	city_gate.anchor_top = 0.72
	city_gate.anchor_right = 0.74
	city_gate.anchor_bottom = 0.92
	add_child(city_gate)

	var recruiter_post := ColorRect.new()
	recruiter_post.color = Color("b92732")
	recruiter_post.anchor_left = 0.42
	recruiter_post.anchor_top = 0.24
	recruiter_post.anchor_right = 0.54
	recruiter_post.anchor_bottom = 0.36
	add_child(recruiter_post)

	var gold_marker := ColorRect.new()
	gold_marker.color = Color("d6b14d")
	gold_marker.anchor_left = 0.54
	gold_marker.anchor_top = 0.36
	gold_marker.anchor_right = 0.66
	gold_marker.anchor_bottom = 0.48
	add_child(gold_marker)

	var header := Label.new()
	header.text = "Nugget Bridge"
	header.anchor_left = 0.04
	header.anchor_top = 0.04
	header.anchor_right = 0.54
	header.anchor_bottom = 0.1
	header.add_theme_font_size_override("font_size", 32)
	header.add_theme_color_override("font_color", Color("102841"))
	add_child(header)

	var recruiter_label := Label.new()
	recruiter_label.text = "Recruiter line"
	recruiter_label.anchor_left = 0.6
	recruiter_label.anchor_top = 0.26
	recruiter_label.anchor_right = 0.88
	recruiter_label.anchor_bottom = 0.32
	recruiter_label.add_theme_font_size_override("font_size", 18)
	recruiter_label.add_theme_color_override("font_color", Color("102841"))
	add_child(recruiter_label)

	dialogue_label = Label.new()
	dialogue_label.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	dialogue_label.anchor_left = 0.06
	dialogue_label.anchor_top = 0.76
	dialogue_label.anchor_right = 0.94
	dialogue_label.anchor_bottom = 0.95
	dialogue_label.add_theme_font_size_override("font_size", 20)
	dialogue_label.add_theme_color_override("font_color", Color("102841"))
	add_child(dialogue_label)


func trigger_bridge_scouting() -> void:
	if save_state:
		save_state.record_nugget_bridge_scouting()
	dialogue_label.text = "Red: Rocket is using the bridge line as cover. Misty: Gold Dust is flashing prize money at the same Trainers. Antman, take the first recruiter and we break their rhythm."


func trigger_recruiter_battle() -> void:
	if save_state:
		save_state.start_battle_placeholder(FIRST_RECRUITER_BATTLE_ID)
	dialogue_label.text = "Bridge Recruiter: Beat me and maybe Rocket or Gold Dust will make you an offer."
	emit_signal("start_battle_placeholder", FIRST_RECRUITER_BATTLE_ID)


func trigger_bridge_captain_battle() -> void:
	if save_state and not bool(save_state.story_flags.get("nugget_bridge_recruiter_1_battle_finished", false)):
		dialogue_label.text = "Misty: Clear the first recruiter before we push the captain. Rocket and Gold Dust are watching how Antman handles pressure."
		return
	if save_state:
		save_state.start_battle_placeholder(CAPTAIN_BATTLE_ID)
	dialogue_label.text = "Bridge Captain: Rocket pays for control. Gold Dust pays for results. Show me which offer scares you more."
	emit_signal("start_battle_placeholder", CAPTAIN_BATTLE_ID)


func show_bridge_resolution() -> void:
	dialogue_label.text = "Misty: The bridge is clear enough for now. Rocket and Gold Dust lost their cover, so my gym is open when Antman is ready."


func return_to_cerulean_city() -> void:
	emit_signal("go_to_cerulean_city")


func _update_intro_dialogue() -> void:
	dialogue_label.text = "Misty: Nugget Bridge is packed. Press Z/Enter to scout with Red and Misty, Up for the first recruiter, Right for the bridge captain, or X/Esc to return to Cerulean City."
