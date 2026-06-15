extends Control

signal go_to_pewter_city
signal go_to_mt_moon_interior_1

var save_state
var dialogue_label: Label


func _ready() -> void:
	_build_entrance()
	if save_state:
		save_state.enter_mt_moon_entrance()
	_update_intro_dialogue()


func _unhandled_input(event: InputEvent) -> void:
	if event.is_action_pressed("confirm"):
		trigger_faction_conflict()
	if event.is_action_pressed("ui_up"):
		trigger_cave_entry()
	if event.is_action_pressed("cancel"):
		return_to_pewter_city()


func _build_entrance() -> void:
	var ground := ColorRect.new()
	ground.color = Color("786b5b")
	ground.set_anchors_preset(Control.PRESET_FULL_RECT)
	add_child(ground)

	var cliff := ColorRect.new()
	cliff.color = Color("4c4441")
	cliff.anchor_left = 0.56
	cliff.anchor_top = 0.0
	cliff.anchor_right = 1.0
	cliff.anchor_bottom = 1.0
	add_child(cliff)

	var cave := ColorRect.new()
	cave.color = Color("1f2430")
	cave.anchor_left = 0.66
	cave.anchor_top = 0.24
	cave.anchor_right = 0.9
	cave.anchor_bottom = 0.58
	add_child(cave)

	var path := ColorRect.new()
	path.color = Color("c4a46a")
	path.anchor_left = 0.0
	path.anchor_top = 0.48
	path.anchor_right = 0.72
	path.anchor_bottom = 0.62
	add_child(path)

	var header := Label.new()
	header.text = "Mt. Moon Entrance"
	header.anchor_left = 0.04
	header.anchor_top = 0.04
	header.anchor_right = 0.5
	header.anchor_bottom = 0.1
	header.add_theme_font_size_override("font_size", 32)
	header.add_theme_color_override("font_color", Color("fff2c7"))
	add_child(header)

	var cave_label := Label.new()
	cave_label.text = "Cave mouth"
	cave_label.anchor_left = 0.68
	cave_label.anchor_top = 0.36
	cave_label.anchor_right = 0.88
	cave_label.anchor_bottom = 0.42
	cave_label.add_theme_font_size_override("font_size", 20)
	cave_label.add_theme_color_override("font_color", Color("fff2c7"))
	add_child(cave_label)

	dialogue_label = Label.new()
	dialogue_label.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	dialogue_label.anchor_left = 0.06
	dialogue_label.anchor_top = 0.76
	dialogue_label.anchor_right = 0.94
	dialogue_label.anchor_bottom = 0.95
	dialogue_label.add_theme_font_size_override("font_size", 20)
	dialogue_label.add_theme_color_override("font_color", Color("fff2c7"))
	add_child(dialogue_label)


func trigger_faction_conflict() -> void:
	if save_state:
		save_state.record_mt_moon_faction_conflict()
	dialogue_label.text = "Team Rocket shoves a fossil crate toward the cave, but Team Gold Dust cuts them off with hired miners. Red pulls Antman back as both sides argue over a third reading: the Nexus Fossil."


func trigger_cave_entry() -> void:
	if save_state and not bool(save_state.story_flags.get("rocket_gold_dust_mt_moon_conflict_seen", false)):
		dialogue_label.text = "Red: Watch the entrance conflict first. If we walk in blind, both teams can pin the fossil theft on us."
		return
	dialogue_label.text = "Red: Inside, Rocket is taking the left tunnel and Team Gold Dust is cutting right. We move before they find the third signal."
	emit_signal("go_to_mt_moon_interior_1")


func return_to_pewter_city() -> void:
	emit_signal("go_to_pewter_city")


func _update_intro_dialogue() -> void:
	dialogue_label.text = "Red: Mt. Moon is louder than it should be. Press Z/Enter to watch the fossil conflict, Up to enter the cave, or X/Esc to return to Pewter City."
