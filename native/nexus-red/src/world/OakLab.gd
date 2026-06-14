extends Control

const StarterSelector := preload("res://src/starter/StarterSelector.gd")

signal return_to_bedroom
signal go_to_route_1

var save_state
var dialogue_label: Label
var selector: PanelContainer
var depart_button: Button


func _ready() -> void:
	_build_lab()


func _build_lab() -> void:
	var floor := ColorRect.new()
	floor.color = Color("d7e8ef")
	floor.set_anchors_preset(Control.PRESET_FULL_RECT)
	add_child(floor)

	var counter := ColorRect.new()
	counter.color = Color("f4f0c8")
	counter.anchor_left = 0.08
	counter.anchor_top = 0.1
	counter.anchor_right = 0.92
	counter.anchor_bottom = 0.26
	add_child(counter)

	var title := Label.new()
	title.text = "Professor Oak's Lab"
	title.anchor_left = 0.05
	title.anchor_top = 0.04
	title.anchor_right = 0.95
	title.anchor_bottom = 0.1
	title.add_theme_font_size_override("font_size", 32)
	title.add_theme_color_override("font_color", Color("14243d"))
	add_child(title)

	dialogue_label = Label.new()
	dialogue_label.text = "Professor Oak: Antman, the world is wider than this town. Pick the first partner you trust. Red will walk with you, but this choice is yours."
	dialogue_label.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	dialogue_label.anchor_left = 0.06
	dialogue_label.anchor_top = 0.78
	dialogue_label.anchor_right = 0.94
	dialogue_label.anchor_bottom = 0.95
	dialogue_label.add_theme_font_size_override("font_size", 20)
	dialogue_label.add_theme_color_override("font_color", Color("14243d"))
	add_child(dialogue_label)

	selector = StarterSelector.new()
	selector.save_state = save_state
	selector.anchor_left = 0.06
	selector.anchor_top = 0.28
	selector.anchor_right = 0.94
	selector.anchor_bottom = 0.75
	selector.starter_selected.connect(_on_starter_chosen)
	add_child(selector)

	depart_button = Button.new()
	depart_button.text = "Step onto Route 1"
	depart_button.visible = false
	depart_button.anchor_left = 0.36
	depart_button.anchor_top = 0.68
	depart_button.anchor_right = 0.64
	depart_button.anchor_bottom = 0.75
	depart_button.pressed.connect(_depart_to_route_1)
	add_child(depart_button)


func _on_starter_chosen(selection: Dictionary) -> void:
	if save_state:
		save_state.choose_starter(selection)
	dialogue_label.text = "Blue: You picked %s? Fine. I will take %s and prove I am ahead of you before Route 1." % [selection.get("player_starter", ""), selection.get("blue_starter", "")]
	if depart_button:
		depart_button.visible = true


func _depart_to_route_1() -> void:
	emit_signal("go_to_route_1")
