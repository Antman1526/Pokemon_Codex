extends Control

signal go_to_vermilion_city
signal start_battle_placeholder(battle_id)

var save_state
var dialogue_label: Label


func _ready() -> void:
	_build_power_sabotage()
	if save_state:
		save_state.enter_vermilion_power_sabotage()
	_update_intro_dialogue()


func _unhandled_input(event: InputEvent) -> void:
	if event.is_action_pressed("confirm"):
		trigger_power_sabotage_scene()
	if event.is_action_pressed("ui_right"):
		trigger_surge_gym_battle()
	if event.is_action_pressed("cancel"):
		return_to_vermilion_city()


func _build_power_sabotage() -> void:
	var ground := ColorRect.new()
	ground.color = Color("5b553f")
	ground.set_anchors_preset(Control.PRESET_FULL_RECT)
	add_child(ground)

	var gym := ColorRect.new()
	gym.color = Color("e1c84c")
	gym.anchor_left = 0.08
	gym.anchor_top = 0.18
	gym.anchor_right = 0.36
	gym.anchor_bottom = 0.48
	add_child(gym)

	var substation := ColorRect.new()
	substation.color = Color("48505d")
	substation.anchor_left = 0.48
	substation.anchor_top = 0.16
	substation.anchor_right = 0.88
	substation.anchor_bottom = 0.48
	add_child(substation)

	var gas_cloud := ColorRect.new()
	gas_cloud.color = Color("778b50")
	gas_cloud.anchor_left = 0.56
	gas_cloud.anchor_top = 0.42
	gas_cloud.anchor_right = 0.92
	gas_cloud.anchor_bottom = 0.62
	add_child(gas_cloud)

	var rocket_van := ColorRect.new()
	rocket_van.color = Color("2b2b32")
	rocket_van.anchor_left = 0.12
	rocket_van.anchor_top = 0.54
	rocket_van.anchor_right = 0.34
	rocket_van.anchor_bottom = 0.66
	add_child(rocket_van)

	var header := Label.new()
	header.text = "Vermilion Power Sabotage"
	header.anchor_left = 0.04
	header.anchor_top = 0.04
	header.anchor_right = 0.9
	header.anchor_bottom = 0.1
	header.add_theme_font_size_override("font_size", 32)
	header.add_theme_color_override("font_color", Color("fff0bd"))
	add_child(header)

	var gym_label := Label.new()
	gym_label.text = "Surge Gym"
	gym_label.anchor_left = 0.13
	gym_label.anchor_top = 0.3
	gym_label.anchor_right = 0.32
	gym_label.anchor_bottom = 0.36
	gym_label.add_theme_font_size_override("font_size", 18)
	gym_label.add_theme_color_override("font_color", Color("332b10"))
	add_child(gym_label)

	var gas_label := Label.new()
	gas_label.text = "Team Gas fumes"
	gas_label.anchor_left = 0.6
	gas_label.anchor_top = 0.49
	gas_label.anchor_right = 0.86
	gas_label.anchor_bottom = 0.55
	gas_label.add_theme_font_size_override("font_size", 16)
	gas_label.add_theme_color_override("font_color", Color("fff0bd"))
	add_child(gas_label)

	var rocket_label := Label.new()
	rocket_label.text = "Rocket van"
	rocket_label.anchor_left = 0.16
	rocket_label.anchor_top = 0.575
	rocket_label.anchor_right = 0.34
	rocket_label.anchor_bottom = 0.63
	rocket_label.add_theme_font_size_override("font_size", 16)
	rocket_label.add_theme_color_override("font_color", Color("f4ead5"))
	add_child(rocket_label)

	dialogue_label = Label.new()
	dialogue_label.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	dialogue_label.anchor_left = 0.06
	dialogue_label.anchor_top = 0.72
	dialogue_label.anchor_right = 0.94
	dialogue_label.anchor_bottom = 0.95
	dialogue_label.add_theme_font_size_override("font_size", 20)
	dialogue_label.add_theme_color_override("font_color", Color("fff0bd"))
	add_child(dialogue_label)


func trigger_power_sabotage_scene() -> void:
	if save_state:
		save_state.record_vermilion_power_sabotage_scene()
	dialogue_label.text = "Red: Rocket opened the power room, but Team Gas flooded the grid with poison exhaust and stole the credit. Misty is clearing the harbor vents, Bill decoded the relay loop, and Surge says Antman can challenge him once the fumes break."


func trigger_surge_gym_battle() -> void:
	if save_state and not bool(save_state.story_flags.get("surge_gym_battle_unlocked", false)):
		dialogue_label.text = "Lt. Surge: No battle until you finish exposing that power sabotage. Clear the fumes, then come earn the Thunder Badge."
		return
	if save_state:
		save_state.start_battle_placeholder("lt_surge_vermilion_gym")
	dialogue_label.text = "Lt. Surge: Red and Misty helped you prep, but this one is yours, Antman. Win and the Thunder Badge opens the road east."
	emit_signal("start_battle_placeholder", "lt_surge_vermilion_gym")


func return_to_vermilion_city() -> void:
	emit_signal("go_to_vermilion_city")


func _update_intro_dialogue() -> void:
	dialogue_label.text = "Red: Trail Cutter got us behind Surge's gym. Press Z/Enter to expose the Rocket and Team Gas power sabotage with Misty and Bill, Right for Lt. Surge's gym, or X/Esc to return to Vermilion."
