extends PanelContainer

const OPENING_FEED_PATH := "res://content/worldlink/opening_feed.json"
const ROUTE_1_BATCH_PATH := "res://content/worldlink/route_1_rival_batch.json"
const VIRIDIAN_BATCH_PATH := "res://content/worldlink/viridian_story_batch.json"
const ROUTE_1_RUMORS_PATH := "res://content/encounters/route_1_rumors.json"

var save_state


func _ready() -> void:
	_build_worldlink()


func _build_worldlink() -> void:
	_clear_children()

	var box := VBoxContainer.new()
	box.add_theme_constant_override("separation", 10)
	add_child(box)

	var title := Label.new()
	title.text = "WorldLink"
	title.add_theme_font_size_override("font_size", 28)
	title.add_theme_color_override("font_color", Color("b92732"))
	box.add_child(title)

	var feed := Label.new()
	feed.text = _build_feed_text()
	feed.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	feed.add_theme_font_size_override("font_size", 18)
	box.add_child(feed)

	var checklist := Label.new()
	checklist.text = _build_checklist_text()
	checklist.add_theme_font_size_override("font_size", 16)
	box.add_child(checklist)


func _clear_children() -> void:
	for child in get_children():
		remove_child(child)
		child.free()


func _build_feed_text() -> String:
	var item_index := _build_item_index()
	var ids := _active_message_ids()
	var feed_lines: Array[String] = ["Feed"]
	var rumor_lines: Array[String] = ["Route 1 Rumors"]

	for message_id in ids:
		var item: Dictionary = item_index.get(message_id, {})
		var text := _message_text(message_id, item)
		if message_id.begins_with("rumor_"):
			rumor_lines.append("- " + text)
		else:
			feed_lines.append("- " + text)

	if rumor_lines.size() == 1:
		rumor_lines.append("- No confirmed Route 1 rumors yet.")

	return "\n".join(feed_lines) + "\n\n" + "\n".join(rumor_lines)


func _build_checklist_text() -> String:
	return "Checklist\n%s Visit Oak\n%s Choose first partner\n%s Step onto Route 1\n%s Finish Blue Route 1 battle\n%s Check Route 1 rumors\n%s Reach Viridian City\n%s Talk to Red in Viridian\n%s Find Viridian Rocket clue" % [
		_checkmark(_flag("mom_opening_scene_seen")),
		_checkmark(_flag("starter_chosen")),
		_checkmark(_flag("route_1_reached")),
		_checkmark(_flag("blue_route_1_battle_finished")),
		_checkmark(_flag("route_1_rumors_unlocked")),
		_checkmark(_flag("viridian_city_reached")),
		_checkmark(_flag("viridian_red_scene_seen")),
		_checkmark(_flag("viridian_rocket_clue_found")),
	]


func _checkmark(done: bool) -> String:
	if done:
		return "[x]"
	return "[ ]"


func _flag(flag_name: String) -> bool:
	if save_state == null:
		return false
	return bool(save_state.story_flags.get(flag_name, false))


func _active_message_ids() -> Array:
	if save_state != null and save_state.worldlink_queue.size() > 0:
		return save_state.worldlink_queue
	return [
		"red_route_1_tracks",
		"blue_first_battle_pressure",
		"oak_world_migration_alert",
		"nexus_island_locked",
	]


func _build_item_index() -> Dictionary:
	var index := {}
	_add_feed_items(index, OPENING_FEED_PATH, "feed")
	_add_feed_items(index, ROUTE_1_BATCH_PATH, "feed")
	_add_feed_items(index, VIRIDIAN_BATCH_PATH, "feed")
	_add_feed_items(index, ROUTE_1_RUMORS_PATH, "rumors")
	return index


func _add_feed_items(index: Dictionary, path: String, key: String) -> void:
	var data := _load_json(path)
	var items: Array = data.get(key, [])
	for item in items:
		if typeof(item) == TYPE_DICTIONARY and item.has("id"):
			index[item.get("id")] = item


func _load_json(path: String) -> Dictionary:
	if not FileAccess.file_exists(path):
		return {}
	var file := FileAccess.open(path, FileAccess.READ)
	if file == null:
		return {}
	var parsed = JSON.parse_string(file.get_as_text())
	if typeof(parsed) == TYPE_DICTIONARY:
		return parsed
	return {}


func _message_text(message_id: String, item: Dictionary) -> String:
	if item.has("text"):
		return str(item.get("text"))
	if message_id.begins_with("starter_chosen_"):
		return "Antman chose " + _pretty_id(message_id.trim_prefix("starter_chosen_")) + " as his first partner."
	if message_id.begins_with("blue_chose_"):
		return "Blue chose " + _pretty_id(message_id.trim_prefix("blue_chose_")) + " and immediately started talking strategy."
	if message_id == "route_1_reached":
		return "Antman reached Route 1 with Red watching the grass line."
	if message_id == "red_route_1_companion":
		return "Red joined Antman on Route 1 and marked the first anomaly trail."
	if message_id == "blue_route_1_battle_placeholder":
		return "Blue forced the first Route 1 battle beat. Full battle logic is the next combat milestone."
	if message_id == "blue_route_1_battle_finished":
		return "Blue's first Route 1 battle beat is complete. WorldLink activity is starting to spread."
	return "Update: " + _pretty_id(message_id)


func _pretty_id(raw_id: String) -> String:
	var words := raw_id.split("_")
	for index in range(words.size()):
		words[index] = words[index].capitalize()
	return " ".join(words)
