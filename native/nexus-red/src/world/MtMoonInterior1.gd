extends Control

signal go_to_mt_moon_entrance
signal go_to_mt_moon_fossil_decision
signal start_battle_placeholder(battle_id)

var save_state
var dialogue_label: Label


func _ready() -> void:
	_build_room()
	if save_state:
		save_state.enter_mt_moon_interior_1()
	_update_intro_dialogue()


func _unhandled_input(event: InputEvent) -> void:
	if event.is_action_pressed("confirm"):
		trigger_split_path_scouting()
	if event.is_action_pressed("ui_left"):
		trigger_rocket_left_path_battle()
	if event.is_action_pressed("ui_right"):
		trigger_gold_dust_right_path_battle()
	if event.is_action_pressed("ui_down"):
		trigger_fossil_decision_scene()
	if event.is_action_pressed("cancel"):
		return_to_mt_moon_entrance()


func _build_room() -> void:
	var floor := ColorRect.new()
	floor.color = Color("3f3944")
	floor.set_anchors_preset(Control.PRESET_FULL_RECT)
	add_child(floor)

	var left_tunnel := ColorRect.new()
	left_tunnel.color = Color("2b2f3a")
	left_tunnel.anchor_left = 0.04
	left_tunnel.anchor_top = 0.24
	left_tunnel.anchor_right = 0.34
	left_tunnel.anchor_bottom = 0.58
	add_child(left_tunnel)

	var right_tunnel := ColorRect.new()
	right_tunnel.color = Color("5d4a24")
	right_tunnel.anchor_left = 0.66
	right_tunnel.anchor_top = 0.24
	right_tunnel.anchor_right = 0.96
	right_tunnel.anchor_bottom = 0.58
	add_child(right_tunnel)

	var fossil_table := ColorRect.new()
	fossil_table.color = Color("8a7865")
	fossil_table.anchor_left = 0.4
	fossil_table.anchor_top = 0.34
	fossil_table.anchor_right = 0.6
	fossil_table.anchor_bottom = 0.52
	add_child(fossil_table)

	var header := Label.new()
	header.text = "Mt. Moon Interior 1"
	header.anchor_left = 0.04
	header.anchor_top = 0.04
	header.anchor_right = 0.48
	header.anchor_bottom = 0.1
	header.add_theme_font_size_override("font_size", 32)
	header.add_theme_color_override("font_color", Color("fff2c7"))
	add_child(header)

	var left_label := Label.new()
	left_label.text = "Rocket left path"
	left_label.anchor_left = 0.08
	left_label.anchor_top = 0.38
	left_label.anchor_right = 0.32
	left_label.anchor_bottom = 0.44
	left_label.add_theme_font_size_override("font_size", 19)
	left_label.add_theme_color_override("font_color", Color("fff2c7"))
	add_child(left_label)

	var right_label := Label.new()
	right_label.text = "Gold Dust right path"
	right_label.anchor_left = 0.69
	right_label.anchor_top = 0.38
	right_label.anchor_right = 0.94
	right_label.anchor_bottom = 0.44
	right_label.add_theme_font_size_override("font_size", 19)
	right_label.add_theme_color_override("font_color", Color("fff2c7"))
	add_child(right_label)

	var table_label := Label.new()
	table_label.text = "Fossil table"
	table_label.anchor_left = 0.42
	table_label.anchor_top = 0.4
	table_label.anchor_right = 0.59
	table_label.anchor_bottom = 0.46
	table_label.add_theme_font_size_override("font_size", 18)
	table_label.add_theme_color_override("font_color", Color("1f2430"))
	add_child(table_label)

	dialogue_label = Label.new()
	dialogue_label.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	dialogue_label.anchor_left = 0.06
	dialogue_label.anchor_top = 0.74
	dialogue_label.anchor_right = 0.94
	dialogue_label.anchor_bottom = 0.95
	dialogue_label.add_theme_font_size_override("font_size", 20)
	dialogue_label.add_theme_color_override("font_color", Color("fff2c7"))
	add_child(dialogue_label)


func trigger_split_path_scouting() -> void:
	if save_state:
		save_state.record_mt_moon_split_path_scouting()
	dialogue_label.text = "Red marks the split: Team Rocket drags the Dome Fossil crate down the left tunnel, Team Gold Dust chases the Helix Fossil signal to the right, and the Nexus Fossil pulse keeps coming from below both paths."


func trigger_rocket_left_path_battle() -> void:
	if save_state and not bool(save_state.story_flags.get("fossil_choice_setup_seen", false)):
		dialogue_label.text = "Red: Scout the split first. Rocket wants us to rush left before we understand the cave."
		return
	if save_state:
		save_state.start_battle_placeholder("mt_moon_rocket_left_path")
	dialogue_label.text = "Red: I will hold the second Rocket here. Take the left-path runner before that Dome Fossil crate disappears."
	emit_signal("start_battle_placeholder", "mt_moon_rocket_left_path")


func trigger_gold_dust_right_path_battle() -> void:
	if save_state and not bool(save_state.story_flags.get("fossil_choice_setup_seen", false)):
		dialogue_label.text = "Red: Scout the split first. Gold Dust is counting on us missing the Helix signal."
		return
	if save_state:
		save_state.start_battle_placeholder("mt_moon_gold_dust_right_path")
	dialogue_label.text = "Red: I will keep the fossil table clear. Stop that Gold Dust Prospector before they stake a claim on the Helix signal."
	emit_signal("start_battle_placeholder", "mt_moon_gold_dust_right_path")


func trigger_fossil_decision_scene() -> void:
	if save_state and (
		not bool(save_state.story_flags.get("mt_moon_rocket_left_battle_finished", false))
		or not bool(save_state.story_flags.get("mt_moon_gold_dust_right_battle_finished", false))
	):
		dialogue_label.text = "Red: We need to pressure both factions before touching the fossil table."
		return
	dialogue_label.text = "Red: Dome and Helix are stable enough to move. The Nexus Fossil signal is deeper, and it is still calling."
	emit_signal("go_to_mt_moon_fossil_decision")


func return_to_mt_moon_entrance() -> void:
	emit_signal("go_to_mt_moon_entrance")


func _update_intro_dialogue() -> void:
	dialogue_label.text = "Red: This is the first split. Press Z/Enter to scout, Left for Rocket, Right for Gold Dust, Down for the fossil table, or X/Esc to return to the Mt. Moon entrance."
