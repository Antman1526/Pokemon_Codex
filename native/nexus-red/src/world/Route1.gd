extends Control

const PlayerAvatar := preload("res://src/world/PlayerAvatar.gd")
const WorldLinkPanel := preload("res://src/worldlink/WorldLinkPanel.gd")
const EncounterService := preload("res://src/encounter/EncounterService.gd")
const RED_ROUTE_FLAG := "red_route_1_companion_scene_seen"
const BLUE_BATTLE_FLAG := "blue_battle_placeholder_seen"

signal start_battle_placeholder(battle_id)
signal start_wild_encounter(encounter_data)

var save_state
var dialogue_label: Label
var player: ColorRect
var worldlink_panel: PanelContainer
var encounter_service := EncounterService.new()


func _ready() -> void:
	_build_route()
	if save_state:
		save_state.enter_route_1()


func _unhandled_input(event: InputEvent) -> void:
	if event.is_action_pressed("confirm"):
		if save_state and not save_state.story_flags.get(RED_ROUTE_FLAG, false):
			trigger_red_scene()
		else:
			trigger_blue_battle_placeholder()
	if event.is_action_pressed("cancel"):
		trigger_route_1_wild_encounter()
	if event.is_action_pressed("worldlink"):
		_toggle_worldlink()


func _build_route() -> void:
	var grass := ColorRect.new()
	grass.color = Color("78b85a")
	grass.set_anchors_preset(Control.PRESET_FULL_RECT)
	add_child(grass)

	var path := ColorRect.new()
	path.color = Color("d6b36f")
	path.anchor_left = 0.42
	path.anchor_top = 0.0
	path.anchor_right = 0.58
	path.anchor_bottom = 1.0
	add_child(path)

	for i in range(6):
		var tall_grass := ColorRect.new()
		tall_grass.color = Color("4f9b47")
		tall_grass.position = Vector2(110 + i * 165, 160 + (i % 2) * 210)
		tall_grass.size = Vector2(100, 64)
		add_child(tall_grass)

	var header := Label.new()
	header.text = "Route 1"
	header.anchor_left = 0.04
	header.anchor_top = 0.04
	header.anchor_right = 0.4
	header.anchor_bottom = 0.1
	header.add_theme_font_size_override("font_size", 32)
	header.add_theme_color_override("font_color", Color("14243d"))
	add_child(header)

	var red_marker := ColorRect.new()
	red_marker.color = Color("b92732")
	red_marker.position = Vector2(720, 220)
	red_marker.size = Vector2(34, 34)
	add_child(red_marker)

	var blue_marker := ColorRect.new()
	blue_marker.color = Color("3159b7")
	blue_marker.position = Vector2(720, 420)
	blue_marker.size = Vector2(34, 34)
	add_child(blue_marker)

	player = PlayerAvatar.new()
	player.position = Vector2(610, 560)
	add_child(player)

	dialogue_label = Label.new()
	dialogue_label.text = "Route 1 opens north. Press arrows to move. Press Z or Enter for Red's first companion scene, then Blue's battle placeholder. Press X or Esc to check the grass. Press W for WorldLink."
	dialogue_label.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	dialogue_label.anchor_left = 0.06
	dialogue_label.anchor_top = 0.82
	dialogue_label.anchor_right = 0.94
	dialogue_label.anchor_bottom = 0.95
	dialogue_label.add_theme_font_size_override("font_size", 20)
	dialogue_label.add_theme_color_override("font_color", Color("14243d"))
	add_child(dialogue_label)


func trigger_red_scene() -> void:
	if save_state:
		save_state.record_red_route_1_scene()
	dialogue_label.text = "Red: These tracks are wrong for Route 1. Stay close, Antman. Your partner should see the world before the world starts chasing you."


func trigger_blue_battle_placeholder() -> void:
	if save_state:
		save_state.record_blue_battle_placeholder()
	dialogue_label.text = "Blue: There you are. I already know your first partner and I already know mine. Battle system is next, but remember this: I am not waiting for you."
	emit_signal("start_battle_placeholder", "blue_route_1")


func trigger_route_1_wild_encounter() -> void:
	var encounter := encounter_service.pick_route_1_encounter(save_state)
	if encounter.is_empty():
		dialogue_label.text = "The grass rustles, but no encounter data is ready yet."
		return
	if save_state:
		save_state.start_wild_encounter(encounter)
	dialogue_label.text = "The grass shakes. Red raises a hand: first wild encounter incoming."
	emit_signal("start_wild_encounter", encounter)


func _toggle_worldlink() -> void:
	if worldlink_panel:
		worldlink_panel.visible = not worldlink_panel.visible
		return
	worldlink_panel = WorldLinkPanel.new()
	worldlink_panel.anchor_left = 0.58
	worldlink_panel.anchor_top = 0.08
	worldlink_panel.anchor_right = 0.96
	worldlink_panel.anchor_bottom = 0.76
	worldlink_panel.save_state = save_state
	add_child(worldlink_panel)
