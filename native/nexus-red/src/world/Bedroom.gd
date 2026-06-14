extends Control

const WorldLinkPanel := preload("res://src/worldlink/WorldLinkPanel.gd")

signal go_to_oak_lab

var save_state
var dialogue_label: Label
var worldlink_panel: PanelContainer
var mom_scene_seen := false


func _ready() -> void:
	_build_bedroom()


func _unhandled_input(event: InputEvent) -> void:
	if event.is_action_pressed("confirm"):
		if mom_scene_seen:
			emit_signal("go_to_oak_lab")
		else:
			_play_mom_scene()
	if event.is_action_pressed("worldlink"):
		_toggle_worldlink()


func _build_bedroom() -> void:
	var floor := ColorRect.new()
	floor.color = Color("d8b77a")
	floor.set_anchors_preset(Control.PRESET_FULL_RECT)
	add_child(floor)

	var rug := ColorRect.new()
	rug.color = Color("b92732")
	rug.anchor_left = 0.22
	rug.anchor_top = 0.52
	rug.anchor_right = 0.58
	rug.anchor_bottom = 0.78
	add_child(rug)

	var bed := ColorRect.new()
	bed.color = Color("5f8fd3")
	bed.anchor_left = 0.08
	bed.anchor_top = 0.18
	bed.anchor_right = 0.28
	bed.anchor_bottom = 0.45
	add_child(bed)

	var desk := ColorRect.new()
	desk.color = Color("7c4f2c")
	desk.anchor_left = 0.68
	desk.anchor_top = 0.18
	desk.anchor_right = 0.9
	desk.anchor_bottom = 0.36
	add_child(desk)

	var header := Label.new()
	header.text = "Antman's Bedroom"
	header.anchor_left = 0.05
	header.anchor_top = 0.05
	header.anchor_right = 0.95
	header.anchor_bottom = 0.12
	header.add_theme_font_size_override("font_size", 32)
	header.add_theme_color_override("font_color", Color("14243d"))
	add_child(header)

	dialogue_label = Label.new()
	dialogue_label.text = "Morning news crackles downstairs. Press Z or Enter to talk with Mom. Press W for WorldLink."
	dialogue_label.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	dialogue_label.anchor_left = 0.06
	dialogue_label.anchor_top = 0.82
	dialogue_label.anchor_right = 0.94
	dialogue_label.anchor_bottom = 0.95
	dialogue_label.add_theme_color_override("font_color", Color("14243d"))
	dialogue_label.add_theme_font_size_override("font_size", 22)
	add_child(dialogue_label)


func _play_mom_scene() -> void:
	mom_scene_seen = true
	if save_state:
		save_state.set_flag("mom_opening_scene_seen", true)
	if dialogue_label:
		dialogue_label.text = "Mom: Antman, Professor Oak called. Red saw impossible tracks near Route 1, and the League news says creatures are migrating where they shouldn't. Oak is waiting at the lab. Press Z or Enter again."


func _toggle_worldlink() -> void:
	if worldlink_panel:
		worldlink_panel.visible = not worldlink_panel.visible
		return
	worldlink_panel = WorldLinkPanel.new()
	worldlink_panel.anchor_left = 0.58
	worldlink_panel.anchor_top = 0.08
	worldlink_panel.anchor_right = 0.96
	worldlink_panel.anchor_bottom = 0.76
	add_child(worldlink_panel)
