extends PanelContainer

signal starter_selected(selection)

const STARTER_DATA_PATH := "res://content/starters/starter_choices.json"

var save_state
var starter_data: Dictionary = {}
var selected_starter := ""
var status_label: Label


func _ready() -> void:
	starter_data = _load_starter_data()
	_build_selector()


func _load_starter_data() -> Dictionary:
	var file := FileAccess.open(STARTER_DATA_PATH, FileAccess.READ)
	if file == null:
		push_error("Missing starter data: " + STARTER_DATA_PATH)
		return {"starters": [], "blue_counter_rules": {}}
	var parsed = JSON.parse_string(file.get_as_text())
	if typeof(parsed) != TYPE_DICTIONARY:
		push_error("Invalid starter data JSON.")
		return {"starters": [], "blue_counter_rules": {}}
	return parsed


func _build_selector() -> void:
	var root := VBoxContainer.new()
	root.add_theme_constant_override("separation", 8)
	add_child(root)

	var title := Label.new()
	title.text = "Choose Your First Partner"
	title.add_theme_font_size_override("font_size", 24)
	title.add_theme_color_override("font_color", Color("b92732"))
	root.add_child(title)

	var scroll := ScrollContainer.new()
	scroll.custom_minimum_size = Vector2(900, 250)
	root.add_child(scroll)

	var grid := GridContainer.new()
	grid.columns = 6
	grid.add_theme_constant_override("h_separation", 8)
	grid.add_theme_constant_override("v_separation", 8)
	scroll.add_child(grid)

	for starter in starter_data.get("starters", []):
		var button := Button.new()
		button.text = "%s\n%s" % [starter.get("species", ""), starter.get("origin_region", "")]
		button.custom_minimum_size = Vector2(136, 54)
		button.pressed.connect(choose_starter.bind(starter.get("species", "")))
		grid.add_child(button)

	status_label = Label.new()
	status_label.text = "All 27 regional starters and 12 bonus starters are available in Oak's selector."
	status_label.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	status_label.add_theme_font_size_override("font_size", 16)
	root.add_child(status_label)


func choose_starter(species_name: String) -> void:
	selected_starter = species_name
	var selection := _build_selection(species_name)
	if status_label:
		status_label.text = "You chose %s. Blue takes %s. Ava takes %s. Dax takes %s." % [
			selection.get("player_starter", ""),
			selection.get("blue_starter", ""),
			selection.get("ava_starter", ""),
			selection.get("dax_starter", ""),
		]
	emit_signal("starter_selected", selection)


func _build_selection(species_name: String) -> Dictionary:
	var starter: Dictionary = _find_starter(species_name)
	var blue: String = str(starter_data.get("blue_counter_rules", {}).get(species_name, "Charmander"))
	var ava: String = _first_available(starter_data.get("ava_priority_pool", []), [species_name, blue], str(starter_data.get("ava_fallback", "Chikorita")))
	var dax: String = _first_available(starter_data.get("dax_priority_pool", []), [species_name, blue, ava], str(starter_data.get("dax_fallback", "Cyndaquil")))
	return {
		"player_starter": species_name,
		"player_starter_group": starter.get("origin_region", "unknown"),
		"blue_starter": blue,
		"ava_starter": ava,
		"dax_starter": dax,
	}


func _find_starter(species_name: String) -> Dictionary:
	for starter in starter_data.get("starters", []):
		if starter.get("species", "") == species_name:
			return starter
	return {"species": species_name, "origin_region": "unknown"}


func _first_available(pool: Array, blocked: Array, fallback: String) -> String:
	for candidate in pool:
		if not blocked.has(candidate):
			return candidate
	if not blocked.has(fallback):
		return fallback
	for starter in starter_data.get("starters", []):
		var species: String = str(starter.get("species", ""))
		if not blocked.has(species):
			return species
	return fallback
