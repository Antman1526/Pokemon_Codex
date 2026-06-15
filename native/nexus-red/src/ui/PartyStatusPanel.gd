extends PanelContainer

var save_state
var summary_label: Label


func _ready() -> void:
	_build_panel()


func refresh() -> void:
	if summary_label:
		summary_label.text = get_summary_text()


func get_summary_text() -> String:
	var party_entries: Array[String] = []
	if save_state != null:
		for species in save_state.party_roster:
			party_entries.append("- " + str(species))
	if party_entries.is_empty():
		party_entries.append("- No party creatures yet")

	var captured := "None"
	if save_state != null and save_state.captured_creatures.size() > 0:
		captured = ", ".join(save_state.captured_creatures)

	return "Party Status\n%s\nCaptured: %s\nField Lead: %s" % [
		"\n".join(party_entries),
		captured,
		_field_lead(),
	]


func _build_panel() -> void:
	var box := VBoxContainer.new()
	box.add_theme_constant_override("separation", 8)
	add_child(box)

	var title := Label.new()
	title.text = "Party Status"
	title.add_theme_font_size_override("font_size", 24)
	title.add_theme_color_override("font_color", Color("14243d"))
	box.add_child(title)

	summary_label = Label.new()
	summary_label.text = get_summary_text()
	summary_label.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	summary_label.add_theme_font_size_override("font_size", 18)
	box.add_child(summary_label)


func _field_lead() -> String:
	if save_state != null and save_state.party_roster.size() > 0:
		return str(save_state.party_roster[0])
	return "None"
