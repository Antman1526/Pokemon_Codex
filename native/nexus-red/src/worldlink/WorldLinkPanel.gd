extends PanelContainer


func _ready() -> void:
	_build_worldlink()


func _build_worldlink() -> void:
	var box := VBoxContainer.new()
	box.add_theme_constant_override("separation", 10)
	add_child(box)

	var title := Label.new()
	title.text = "WorldLink"
	title.add_theme_font_size_override("font_size", 28)
	title.add_theme_color_override("font_color", Color("b92732"))
	box.add_child(title)

	var feed := Label.new()
	feed.text = "Opening Feed\n- Red marked strange Route 1 tracks.\n- Blue is already asking about the first battle.\n- Oak flagged a regional migration anomaly.\n- Nexus Island: locked until all regions converge."
	feed.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	feed.add_theme_font_size_override("font_size", 18)
	box.add_child(feed)

	var checklist := Label.new()
	checklist.text = "Checklist\n[ ] Visit Oak\n[ ] Choose first partner\n[ ] Step onto Route 1"
	checklist.add_theme_font_size_override("font_size", 16)
	box.add_child(checklist)
