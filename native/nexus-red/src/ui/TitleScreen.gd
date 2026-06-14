extends Control

signal start_new_game

const GOLD := Color("ffd36b")
const RED := Color("b92732")
const DEEP_BLUE := Color("14243d")
const PANEL := Color("fff4d6")


func _ready() -> void:
	_build_title_screen()


func _build_title_screen() -> void:
	var sky := ColorRect.new()
	sky.color = DEEP_BLUE
	sky.set_anchors_preset(Control.PRESET_FULL_RECT)
	add_child(sky)

	var dawn_band := ColorRect.new()
	dawn_band.color = Color("f49b5f")
	dawn_band.anchor_top = 0.64
	dawn_band.anchor_right = 1.0
	dawn_band.anchor_bottom = 1.0
	add_child(dawn_band)

	var nexus_rift := ColorRect.new()
	nexus_rift.color = Color(RED.r, RED.g, RED.b, 0.78)
	nexus_rift.anchor_left = 0.44
	nexus_rift.anchor_top = 0.12
	nexus_rift.anchor_right = 0.56
	nexus_rift.anchor_bottom = 0.62
	add_child(nexus_rift)

	var root := VBoxContainer.new()
	root.set_anchors_preset(Control.PRESET_FULL_RECT)
	root.alignment = BoxContainer.ALIGNMENT_CENTER
	root.add_theme_constant_override("separation", 18)
	add_child(root)

	var title := Label.new()
	title.text = "POKEMON NEXUS RED"
	title.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	title.add_theme_color_override("font_color", GOLD)
	title.add_theme_font_size_override("font_size", 56)
	root.add_child(title)

	var subtitle := Label.new()
	subtitle.text = "Classic FireRed spirit. Native PC/Mac scale."
	subtitle.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	subtitle.add_theme_color_override("font_color", Color.WHITE)
	subtitle.add_theme_font_size_override("font_size", 22)
	root.add_child(subtitle)

	var menu_panel := PanelContainer.new()
	menu_panel.custom_minimum_size = Vector2(340, 110)
	root.add_child(menu_panel)

	var menu_box := VBoxContainer.new()
	menu_box.add_theme_constant_override("separation", 8)
	menu_panel.add_child(menu_box)

	var new_game := Button.new()
	new_game.text = "New Game"
	new_game.pressed.connect(func() -> void: emit_signal("start_new_game"))
	menu_box.add_child(new_game)

	var world_hint := Label.new()
	world_hint.text = "W: WorldLink once your journey begins"
	world_hint.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	world_hint.add_theme_color_override("font_color", PANEL)
	world_hint.add_theme_font_size_override("font_size", 16)
	root.add_child(world_hint)
